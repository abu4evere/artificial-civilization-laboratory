"""L1 — no growth in winter (preregistration.md, frozen as L1-frozen). Arms: C (the world as it is) and L (winter plant
regrowth factor 0). Same E13R code, same people (A2-full, anticipation 1.0); only the setting differs.

  python experiments/L1_no_winter_growth/run_l1.py pilot     # survival pilot: population only, stop rule
  python experiments/L1_no_winter_growth/run_l1.py all       # validity checks, then both arms on seeds 601-616
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
CODE = E13R / "code_e13r"
ARMS = {"c": {}, "l": {"season_growth": (1.3, 1.0, 0.5, 0.0)}}
SEEDS = tuple(range(601, 617))
PILOT = tuple(range(701, 705))
WPY, WPS = 52, 13
WINTER = 3 * WPS
OUT = HERE / "output"


def setup():
    sys.path.insert(0, str(CODE))
    sys.path.insert(1, str(E7))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


def make_world(arm, seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **ARMS[arm]))


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODE / "acl")


class PilotProbe:
    """The pilot reads population only (preregistration section 4)."""
    def __init__(self):
        self.pops = []

    def __call__(self, world, events):
        if (world.tick - 1) % 520 == 519:
            self.pops.append(len(world.living()))


class Probe:
    def __init__(self):
        self.pops = []
        self.land = []                                   # mid-autumn / mid-winter plant food on land per person
        self.n = defaultdict(lambda: defaultdict(float))  # season -> counters
        self.households = []                             # start of winter: stock, need
        self.carers = [0, 0]                             # start of winter: carers with any own stash, carers
        self.seed_sown = 0.0
        self.person_years = 0
        self.child_cohort = {}
        self.child_rows = []
        self.land_tiles = None

    def __call__(self, world, events):
        c = world.cfg
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        if self.land_tiles is None:
            self.land_tiles = [t for row in world.tiles for t in row if not t.water]
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        if wk == 0:
            self.person_years += len(living)
        n = self.n[s]
        got = defaultdict(float)
        for e in events:
            k = e["k"]
            if k == "forage":
                got[e["a"]] += e.get("got", 0.0)
                n["forage_food"] += e.get("got", 0.0)
            elif k == "hunt" and e.get("success"):
                n["hunt_food"] += e.get("meat", 0.0)
            elif k == "give":
                n["given"] += e.get("amount", 0.0)
            elif k == "put" and e.get("thing") == "seeds" and e.get("into") == "ground":
                self.seed_sown += e.get("amount", 0.0) * 0.85
            elif k == "put" and e.get("thing") in ("food", "seeds") and e.get("into") == "stash":
                n["stashed"] += e.get("amount", 0.0)
            elif k == "death" and e.get("cause") == "starvation":
                if e.get("a") in self.child_cohort:
                    self.child_cohort[e["a"]] = True
                elif s == 3 and e.get("age", 0) >= 16:
                    n["adult_starved"] += 1
        adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
        for p in adults:
            n["adult_weeks"] += 1
            chosen = next((x[0] for x in (p.considered or []) if x[3]), None)
            n["forage_choice"] += chosen == "forage"
            n["short"] += bool(p.starving)
            if p.id in got:
                n["forage_weeks"] += 1
        if wk % WPS == 6 and s in (2, 3) and living:
            self.land.append({"season": s, "per_person": round(sum(t.plants + t.crop for t in self.land_tiles) / len(living), 1)})
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
            self.child_cohort = {p.id: False for p in living if p.age(world.tick) < 12 * WPY}
        if wk == WPY - 1:
            self.child_rows.append([len(self.child_cohort), sum(self.child_cohort.values())])
            self.child_cohort = {}

    def results(self):
        return {"pops": self.pops, "land": self.land, "n": {str(s): dict(v) for s, v in self.n.items()},
                "households": self.households, "carers": self.carers, "seed_sown": round(self.seed_sown, 1),
                "person_years": self.person_years, "child_rows": self.child_rows}


def run(arm, seed, tag=""):
    setup()
    f0 = fingerprint()
    w = make_world(arm, seed)
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "state_hash": w.state_hash(), **probe.results()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{arm}_seed_{seed}{tag}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}{tag}: alive {len(w.living())}", flush=True)


def pilot(seed):
    setup()
    w = make_world("l", seed)
    probe = PilotProbe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
        if not w.living():
            break
    died = not w.living()
    (OUT / "pilot").mkdir(parents=True, exist_ok=True)
    (OUT / "pilot" / f"seed_{seed}.json").write_text(json.dumps({"seed": seed, "pops": probe.pops, "died_out": died}),
                                                     encoding="utf-8")
    print(f"pilot seed {seed}: {'DIED OUT' if died else 'survived'}; population every 10 years {probe.pops}", flush=True)


def verify(arm, seed=601, years=20):
    setup()
    hs = []
    for with_probe in (False, True):
        w = make_world(arm, seed)
        if with_probe:
            w.observers.append(Probe())
        for _ in range(years * WPY):
            w.step()
        hs.append(w.state_hash())
    ok = hs[0] == hs[1]
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "checks.txt", "a", encoding="utf-8") as f:
        f.write(f"probe arm {arm} seed {seed}, {years} years: {'READ-ONLY' if ok else 'CHANGES THE WORLD'}\n")
    print(f"verify {arm}:", "READ-ONLY" if ok else "CHANGES THE WORLD", flush=True)
    return ok


if __name__ == "__main__":
    cmd = sys.argv[1]
    me = [sys.executable, str(Path(__file__).resolve())]
    if cmd == "pilot":
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda s: subprocess.call(me + ["pilotone", str(s)]), PILOT))
        died = sum(json.loads((OUT / "pilot" / f"seed_{s}.json").read_text(encoding="utf-8"))["died_out"] for s in PILOT)
        verdict = "STOP: two or more pilot worlds died out" if died >= 2 else "PASS"
        (OUT / "pilot" / "verdict.txt").write_text(f"{died} of {len(PILOT)} pilot worlds died out: {verdict}\n", encoding="utf-8")
        print(f"pilot: {died} of {len(PILOT)} died out: {verdict}", flush=True)
        sys.exit(0 if died < 2 else 1)
    elif cmd == "pilotone":
        pilot(int(sys.argv[2]))
    elif cmd == "verify":
        sys.exit(0 if verify(sys.argv[2]) else 1)
    elif cmd == "all":
        v = (OUT / "pilot" / "verdict.txt")
        if not v.exists() or "PASS" not in v.read_text(encoding="utf-8"):
            sys.exit("ABORT: the survival pilot has not passed")
        for arm in ARMS:
            if subprocess.call(me + ["verify", arm]) != 0:
                sys.exit("ABORT: probe changes the world")
        jobs = [(a, s, "") for a in ARMS for s in SEEDS] + [("c", 601, "_rerun")]
        jobs = [j for j in jobs if not (OUT / f"{j[0]}_seed_{j[1]}{j[2]}.json").exists()]
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda j: subprocess.call(me + ["one", j[0], str(j[1]), j[2] or "-"]), jobs))
        print("ALL DONE", flush=True)
    elif cmd == "one":
        run(sys.argv[2], int(sys.argv[3]), "" if sys.argv[4] == "-" else sys.argv[4])
