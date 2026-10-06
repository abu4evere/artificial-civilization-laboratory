"""W1 — the winter ledger (questions.md). Read-only replays of E13R arms A (B2 off) and B (B2 on), seeds 501-516, on an
instrumented copy of the E13R code that only counts food where it moves.

Checks before any replay: the instrumented code's world equals the E13R code's world (state hash, 20 years, both arms),
and the probe does not touch the world. Each replay's population must equal the saved E13R run.

  python experiments/W1_winter_ledger/run_w1.py all
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E13R = HERE.parent / "E13R_replication"
E7 = HERE.parent / "E7_passive"
CODES = {"ledger": HERE / "code_ledger", "e13r": E13R / "code_e13r"}
ARMS = {"a": {}, "b": {"b2_mode": 1}}
SEEDS = tuple(range(501, 517))
WPY, WPS = 52, 13
WINTER = 3 * WPS
OUT = HERE / "output"


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(arm, seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **ARMS[arm]))


def stash_of(world):
    """Food and seed in stashes, in total and by owner."""
    total, by_owner = 0.0, defaultdict(float)
    for row in world.tiles:
        for t in row:
            for st in t.stash or ():
                total += st[1] + st[2]
                by_owner[st[0]] += st[1] + st[2]
    return total, by_owner


class Probe:
    def __init__(self):
        self.pops = []
        self.flows = defaultdict(lambda: defaultdict(float))     # season -> key -> amount
        self.winters = []                                       # one row per winter
        self.households = []
        self.runs_out = []
        self.cur = None
        self.first_short = {}

    def __call__(self, world, events):
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        if tick % 520 == 519:
            self.pops.append(len(world.living()))
        led = getattr(world, "ledger", None)
        if led is None:
            world.ledger = {}
        else:
            for k, v in led.items():
                self.flows[s][k] += v
            led.clear()
        f = self.flows[s]
        for e in events:
            k = e["k"]
            if k == "forage":
                f["gathered_forage"] += e.get("got", 0.0)
            elif k == "hunt" and e.get("success"):
                f["gathered_hunt"] += e.get("meat", 0.0)
            elif k == "take":
                f["taken_own" if e.get("own") else "taken_other"] += e.get("food", 0.0)
            elif k == "put" and e.get("thing") in ("food", "seeds"):
                f["put_" + e.get("into", "?")] += e.get("amount", 0.0)
            elif k == "give":
                f["given"] += e.get("amount", 0.0)
            elif k == "steal":
                f["stolen"] += e.get("amount", 0.0)
            elif k == "inherit":
                f["inherited"] += e.get("food", 0.0)
        living = world.living()
        adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
        if wk == WINTER:
            stash_total, by_owner = stash_of(world)
            held = sum(p.edible() for p in living)
            seeds = sum(p.seeds for p in living)
            self.cur = {"year": tick // WPY, "held": round(held, 1), "seeds": round(seeds, 1),
                        "stash": round(stash_total, 1), "people": len(living)}
            from acl.matter import carry_capacity
            c = world.cfg
            for p in living:
                deps = world.dependents(p.id)
                if deps and p.age(world.tick) >= 16 * WPY:
                    stock = p.edible() + sum(d.edible() for d in deps) + by_owner.get(p.id, 0.0)
                    need = 13 * (p.need(c, world.tick) + sum(d.need(c, world.tick) for d in deps))
                    self.households.append({"stock": round(stock, 1), "need": round(need, 1),
                                            "carry": round(carry_capacity(world, p), 1), "deps": len(deps),
                                            "own_stash": round(by_owner.get(p.id, 0.0), 1)})
            self.first_short = {p.id: [round(p.edible(), 1), None, bool(world.dependents(p.id))] for p in adults}
        if s == 3 and self.first_short:
            for p in adults:
                row = self.first_short.get(p.id)
                if row and row[1] is None and p.starving:
                    row[1] = wk - WINTER
        if wk == WPY - 1 and self.cur is not None:
            self.cur["held_end"] = round(sum(p.edible() for p in living), 1)
            self.cur["stash_end"] = round(stash_of(world)[0], 1)
            self.winters.append(self.cur)
            self.runs_out.extend(self.first_short.values())
            self.cur, self.first_short = None, {}

    def results(self):
        return {"pops": self.pops, "flows": {str(s): dict(v) for s, v in self.flows.items()}, "winters": self.winters,
                "households": self.households, "runs_out": self.runs_out}


def run(arm, seed):
    setup("ledger")
    w = make_world(arm, seed)
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
        if not w.living():
            break
    saved = json.loads((E13R / "output" / f"{arm}_seed_{seed}.json").read_text(encoding="utf-8"))
    res = {"arm": arm, "seed": seed, "replay_matches": probe.pops == saved["pops"], **probe.results()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: replay matches {res['replay_matches']}", flush=True)


def state_hash(code, arm, probe, seed=501, years=20):
    setup(code)
    w = make_world(arm, seed)
    if probe:
        w.observers.append(Probe())
    for _ in range(years * WPY):
        w.step()
    return w.state_hash()


def verify(arm):
    """The instrumented code, with its probe, must leave the world exactly as the E13R code does without one."""
    me = [sys.executable, str(Path(__file__).resolve())]
    h_plain = subprocess.run(me + ["hash", "e13r", arm, "0"], capture_output=True, text=True).stdout.strip()
    h_led = subprocess.run(me + ["hash", "ledger", arm, "1"], capture_output=True, text=True).stdout.strip()
    ok = bool(h_plain) and h_plain == h_led
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "verify.txt", "a", encoding="utf-8") as f:
        f.write(f"arm {arm} seed 501, 20 years: instrumented code with probe {'EQUALS' if ok else 'DIFFERS FROM'} "
                f"the E13R code\n")
    print(f"verify {arm}:", "EQUAL" if ok else "DIFFERENT", flush=True)
    return ok


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "hash":
        print(state_hash(sys.argv[2], sys.argv[3], sys.argv[4] == "1"))
    elif cmd == "verify":
        sys.exit(0 if verify(sys.argv[2]) else 1)
    elif cmd == "all":
        me = [sys.executable, str(Path(__file__).resolve())]
        for arm in ARMS:
            if subprocess.call(me + ["verify", arm]) != 0:
                sys.exit("ABORT: the instrumented code or the probe changes the world")
        jobs = [(a, s) for a in ARMS for s in SEEDS if not (OUT / f"{a}_seed_{s}.json").exists()]
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda j: subprocess.call(me + [j[0], str(j[1])]), jobs))
        print("ALL DONE", flush=True)
    else:
        run(cmd, int(sys.argv[2]))
