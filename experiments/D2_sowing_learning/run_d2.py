"""D2 — why do sowers learn failure? (questions.md). Read-only replays of E13R's control (Arm A), seeds 501-516, on a
copy of the E13R code that only logs seed placements and changes to beliefs about sowing.

  python experiments/D2_sowing_learning/run_d2.py all
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
CODES = {"d2": HERE / "code_d2", "e13r": E13R / "code_e13r"}
SEEDS = tuple(range(501, 517))
WPY, WPS = 52, 13
OUT = HERE / "output"


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0))


class Probe:
    def __init__(self):
        self.pops = []
        self.sown_prev = {}
        self.cum_grown = defaultdict(float)          # tile -> crop grown so far
        self.harvests = defaultdict(list)            # tile -> [(tick, pid, crop)]
        self.records = []                            # sowings by the sower, followed for a year
        self.place_spot = {}                         # (pid, loc, tick) -> (contrast, spot)
        self.looks = []                              # looks at spots the looker sowed
        self.other_looks = [0, 0, 0]                 # looks at seed spots the looker did not sow: [n, positive, negative]

    def __call__(self, world, events):
        c = world.cfg
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        if tick % 520 == 519:
            self.pops.append(len(world.living()))
        log = getattr(world, "d2_log", None)
        if log is None:
            world.d2_log = []
            log = []
        new_seed = defaultdict(float)
        for e in events:
            if e["k"] == "put" and e.get("thing") == "seeds" and e.get("into") == "ground":
                loc = tuple(e["at"])
                amt = e.get("amount", 0.0) * 0.85
                new_seed[loc] += amt
                p = world.people.get(e["a"])
                key = f"seeds@{world.season}"
                self.records.append({"t": e["t"], "pid": e["a"], "loc": loc, "amt": round(amt, 2), "season": s,
                                     "key": key, "b0": (p.beliefs.get(key) if p else None), "grown0": self.cum_grown[loc],
                                     "src": defaultdict(float), "open": True, "b52": None})
            elif e["k"] == "harvest":
                self.harvests[tuple(e["at"])].append((world.tick, e["a"], e.get("crop", 0.0)))
        growing = s in (0, 1)
        tiles = set(self.sown_prev) | set(new_seed)
        for loc in tiles:
            t = world.tile(loc)
            gone = max(0.0, self.sown_prev.get(loc, 0.0) + new_seed.get(loc, 0.0) - t.sown)
            if growing and gone > 0:
                self.cum_grown[loc] += gone * c.seed_multiplier * (0.4 + 0.6 * t.fertility)
        self.sown_prev = {loc: world.tile(loc).sown for loc in tiles if world.tile(loc).sown > 0.01}
        open_by = defaultdict(list)
        for r in self.records:
            if r["open"]:
                open_by[(r["pid"], r["key"])].append(r)
        for rec in log:
            k = rec["k"]
            if k == "place":
                self.place_spot[(rec["pid"], tuple(rec["loc"]), rec["t"])] = (rec["contrast"], rec["spot"])
                continue
            mine = open_by.get((rec["pid"], rec["key"]), [])
            if k == "look":
                loc = tuple(rec["loc"])
                own = next((r for r in mine if r["loc"] == loc and r["t"] == rec["placed"]), None)
                for r in mine:
                    r["src"]["look at this spot" if r is own else "look at another spot"] += rec["change"]
                if own is not None:
                    at = self.place_spot.get((own["pid"], loc, own["t"]))
                    hv = [h for h in self.harvests.get(loc, []) if own["t"] < h[0] <= world.tick]
                    self.looks.append({"weeks": world.tick - own["t"], "season": own["season"], "then": rec["then"],
                                       "now": rec["now"], "change": rec["change"], "spot_then": at[1] if at else None,
                                       "spot_now": rec["spot"], "grown": round(self.cum_grown[loc] - own["grown0"], 2),
                                       "harvest_others": round(sum(h[2] for h in hv if h[1] != own["pid"]), 2),
                                       "harvest_self": round(sum(h[2] for h in hv if h[1] == own["pid"]), 2),
                                       "contrast_at_sowing": at[0] if at else None})
                elif not mine:
                    self.other_looks[0] += 1
                    self.other_looks[1] += rec["change"] > 0
                    self.other_looks[2] += rec["change"] < 0
            elif k in ("assoc", "fade"):
                for r in mine:
                    r["src"]["other surprise" if k == "assoc" else "fading"] += rec["change"]
        log.clear()
        for r in self.records:
            if r["open"] and world.tick - r["t"] >= WPY:
                p = world.people.get(r["pid"])
                r["b52"] = p.beliefs.get(r["key"]) if p is not None and p.alive else None
                hv = [h for h in self.harvests.get(r["loc"], []) if r["t"] < h[0] <= world.tick]
                sower = world.people.get(r["pid"])
                kin = {q.id for q in world.people.values() if sower is not None and q.id != r["pid"]
                       and world.kinship(sower, q) >= 0.5} if sower is not None else set()
                r["grown"] = round(self.cum_grown[r["loc"]] - r["grown0"], 2)
                r["h_self"] = round(sum(h[2] for h in hv if h[1] == r["pid"]), 2)
                r["h_kin"] = round(sum(h[2] for h in hv if h[1] in kin), 2)
                r["h_others"] = round(sum(h[2] for h in hv if h[1] != r["pid"] and h[1] not in kin), 2)
                r["open"] = False
        if wk == 0:
            for loc in list(self.harvests):
                self.harvests[loc] = [h for h in self.harvests[loc] if world.tick - h[0] <= 2 * WPY]

    def results(self):
        closed = []
        for r in self.records:
            if not r["open"]:
                r = dict(r)
                r["src"] = dict(r["src"])
                r["loc"] = list(r["loc"])
                r.pop("open")
                closed.append(r)
        return {"pops": self.pops, "records": closed, "looks": self.looks, "other_looks": self.other_looks}


def run(seed):
    setup("d2")
    w = make_world(seed)
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
        if not w.living():
            break
    saved = json.loads((E13R / "output" / f"a_seed_{seed}.json").read_text(encoding="utf-8"))
    res = {"seed": seed, "replay_matches": probe.pops == saved["pops"], **probe.results()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: replay matches {res['replay_matches']}", flush=True)


def state_hash(code, probe, seed=501, years=20):
    setup(code)
    w = make_world(seed)
    if probe:
        w.observers.append(Probe())
    for _ in range(years * WPY):
        w.step()
    return w.state_hash()


if __name__ == "__main__":
    cmd = sys.argv[1]
    me = [sys.executable, str(Path(__file__).resolve())]
    if cmd == "hash":
        print(state_hash(sys.argv[2], sys.argv[3] == "1"))
    elif cmd == "all":
        h0 = subprocess.run(me + ["hash", "e13r", "0"], capture_output=True, text=True).stdout.strip()
        h1 = subprocess.run(me + ["hash", "d2", "1"], capture_output=True, text=True).stdout.strip()
        ok = bool(h0) and h0 == h1
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "verify.txt").write_text(f"seed 501, 20 years: instrumented code with probe "
                                        f"{'EQUALS' if ok else 'DIFFERS FROM'} the E13R code\n", encoding="utf-8")
        print("verify:", "EQUAL" if ok else "DIFFERENT", flush=True)
        if not ok:
            sys.exit("ABORT: the instrumented code or the probe changes the world")
        jobs = [s for s in SEEDS if not (OUT / f"seed_{s}.json").exists()]
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda s: subprocess.call(me + [str(s)]), jobs))
        print("ALL DONE", flush=True)
    else:
        run(int(cmd))
