"""U — probe, pilot and main run (preregistration.md), written before any pilot or main data. The width comes from the
calibration verdict (run_u.py calibrate), by the frozen rule.

  python experiments/N4_uncertain_winters/run_u_main.py pilot
  python experiments/N4_uncertain_winters/run_u_main.py main
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_u import CODES, OUT, WPS, WPY, make_world, settings, setup  # noqa: E402

ARMS = ("c", "w", "p")
PILOT = tuple(range(811, 819))
SEEDS = tuple(range(901, 917))
WINTER = 3 * WPS


def chosen_half():
    v = (OUT / "calibration" / "verdict.txt").read_text(encoding="utf-8")
    return float(v.split("RULE: chosen half-width ")[1].split(" ")[0])


class PopProbe:
    def __init__(self):
        self.pops = []

    def __call__(self, world, events):
        if (world.tick - 1) % 520 == 519:
            self.pops.append(len(world.living()))


class Probe:
    def __init__(self):
        self.pops = []
        self.n = defaultdict(lambda: defaultdict(float))
        self.households = []
        self.carers = [0, 0]
        self.autumn = []
        self.land = None
        self.last_loc = {}

    def __call__(self, world, events):
        c = world.cfg
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        if self.land is None:
            self.land = [t for row in world.tiles for t in row if not t.water]
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        n = self.n[s]
        for e in events:
            if e["k"] == "give":
                n["given"] += e.get("amount", 0.0)
        adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
        for p in adults:
            n["adult_weeks"] += 1
            chosen = next((x[0] for x in (p.considered or []) if x[3]), None)
            n["forage_choice"] += chosen == "forage"
            prev = self.last_loc.get(p.id)
            if prev is not None:
                dx = min(abs(p.loc[0] - prev[0]), c.width - abs(p.loc[0] - prev[0]))
                dy = min(abs(p.loc[1] - prev[1]), c.height - abs(p.loc[1] - prev[1]))
                n["moved"] += max(dx, dy)
        self.last_loc = {p.id: p.loc for p in adults}
        if wk == 2 * WPS + 6:
            q = defaultdict(list)
            for t in self.land:
                q[(1 if t.y >= c.height // 2 else 0) * 2 + (1 if t.x >= c.width // 2 else 0)].append(t.plants + t.crop)
            tot = sum(sum(v) for v in q.values())
            self.autumn.append({"tile": tot / len(self.land),
                                "quarters": [sum(q[i]) / len(q[i]) if q[i] else None for i in range(4)],
                                "pp": tot / len(living) if living else None})
        if wk == WINTER:
            stash = defaultdict(float)
            for row in world.tiles:
                for t in row:
                    for st in t.stash or ():
                        stash[st[0]] += st[1] + st[2]
            for p in adults:
                deps = world.dependents(p.id)
                if deps:
                    self.carers[1] += 1
                    self.carers[0] += stash.get(p.id, 0.0) > 0
                    stock = p.edible() + sum(d.edible() for d in deps) + stash.get(p.id, 0.0)
                    need = 13 * (p.need(c, world.tick) + sum(d.need(c, world.tick) for d in deps))
                    self.households.append([round(stock, 1), round(need, 1)])

    def results(self):
        return {"pops": self.pops, "n": {str(s): dict(v) for s, v in self.n.items()}, "households": self.households,
                "carers": self.carers, "autumn": self.autumn}


def fingerprint():
    sys.path.insert(1, str(HERE.parent / "E7_passive"))
    from run_e7 import code_hash
    return code_hash(CODES["u"] / "acl")


def run_one(arm, seed, tag, half, years=120):
    setup("u")
    f0 = fingerprint()
    w = make_world(seed, **settings(arm, half))
    probe = Probe()
    w.observers.append(probe)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    d = w.to_dict()
    d.pop("cfg")
    res = {"arm": arm, "seed": seed, "half": half, "code_hash": f0, "code_hash_after": fingerprint(),
           "world_hash": hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest(), **probe.results()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{arm}_seed_{seed}{tag}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}{tag}: alive {len(w.living())}", flush=True)


def pilot_one(arm, seed, half):
    setup("u")
    w = make_world(seed, **settings(arm, half))
    probe = PopProbe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
        if not w.living():
            break
    (OUT / "pilot").mkdir(parents=True, exist_ok=True)
    (OUT / "pilot" / f"{arm}_seed_{seed}.json").write_text(
        json.dumps({"arm": arm, "seed": seed, "pops": probe.pops, "died_out": not w.living()}), encoding="utf-8")
    print(f"pilot {arm} seed {seed}: {'DIED OUT' if not w.living() else 'survived'}; {probe.pops}", flush=True)


def verify_probe(arm, half, seed=901, years=20):
    setup("u")
    hs = []
    for with_probe in (False, True):
        w = make_world(seed, **settings(arm, half))
        if with_probe:
            w.observers.append(Probe())
        for _ in range(years * WPY):
            w.step()
        hs.append(w.state_hash())
    ok = hs[0] == hs[1]
    with open(OUT / "checks.txt", "a", encoding="utf-8") as f:
        f.write(f"probe arm {arm} seed {seed}, {years} years: {'READ-ONLY' if ok else 'CHANGES THE WORLD'}\n")
    print(f"verify {arm}: {'READ-ONLY' if ok else 'CHANGES THE WORLD'}", flush=True)
    return ok


if __name__ == "__main__":
    cmd = sys.argv[1]
    me = [sys.executable, str(Path(__file__).resolve())]
    if cmd == "pilotone":
        pilot_one(sys.argv[2], int(sys.argv[3]), float(sys.argv[4]))
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]), "" if sys.argv[4] == "-" else sys.argv[4], float(sys.argv[5]))
    elif cmd == "verify":
        sys.exit(0 if verify_probe(sys.argv[2], float(sys.argv[3])) else 1)
    elif cmd == "pilot":
        half = chosen_half()
        jobs = [(a, s) for s in PILOT for a in ARMS]
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda j: subprocess.call(me + ["pilotone", j[0], str(j[1]), str(half)]), jobs))
        R = {(a, s): json.loads((OUT / "pilot" / f"{a}_seed_{s}.json").read_text(encoding="utf-8")) for a in ARMS for s in PILOT}
        died = {a: sum(R[(a, s)]["died_out"] for s in PILOT) for a in ARMS}
        allalive = sum(1 for s in PILOT if not any(R[(a, s)]["died_out"] for a in ARMS))
        ok = died["w"] - died["c"] <= 1 and died["p"] - died["c"] <= 1 and allalive >= 5
        line = (f"died out: C {died['c']}, W {died['w']}, P {died['p']} of 8; excess W {died['w'] - died['c']}, "
                f"P {died['p'] - died['c']} (limit 1); all three arms alive in {allalive} of 8 (need 5): "
                f"{'PASS' if ok else 'STOP'}")
        (OUT / "pilot" / "verdict.txt").write_text(line + "\n", encoding="utf-8")
        print("pilot: " + line, flush=True)
        sys.exit(0 if ok else 1)
    elif cmd == "main":
        v = OUT / "pilot" / "verdict.txt"
        if not v.exists() or "PASS" not in v.read_text(encoding="utf-8"):
            sys.exit("ABORT: the pilot has not passed")
        half = chosen_half()
        for arm in ARMS:
            if subprocess.call(me + ["verify", arm, str(half)]) != 0:
                sys.exit("ABORT: probe changes the world")
        jobs = [(a, s, "") for a in ARMS for s in SEEDS] + [("c", 901, "_rerun")]
        jobs = [j for j in jobs if not (OUT / f"{j[0]}_seed_{j[1]}{j[2]}.json").exists()]
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda j: subprocess.call(me + ["one", j[0], str(j[1]), j[2] or "-", str(half)]), jobs))
        print("ALL DONE", flush=True)
