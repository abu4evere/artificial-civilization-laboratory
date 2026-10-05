"""E13 runner (E13_preregistration.md). Arms: a (A2-full, E9 code), b (E13 code, B2 mode 1), c (B2 mode 2), and the
zero check (E13 code, B2 off; must equal E9 A2-full, seed 304). All at anticipation weight 1.0. Seeds 301–304, 120 years.

  python experiments/E13_following/run_e13.py all
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E7 = HERE.parent / "E7_passive"
E9 = HERE.parent / "E9_anticipation"
ARMS = {"a": (E9 / "code_a2", {}), "b": (HERE / "code_e13", {"b2_mode": 1}),
        "c": (HERE / "code_e13", {"b2_mode": 2}), "zero": (HERE / "code_e13", {})}
SEEDS = (301, 302, 303, 304)
WPY, WPS = 52, 13
AUTUMN = 2
OUT = HERE / "output"


def setup(arm):
    sys.path.insert(0, str(ARMS[arm][0]))
    sys.path.insert(1, str(E7))
    import acl
    assert Path(acl.__file__).resolve().parent == (ARMS[arm][0] / "acl").resolve()


def make_world(arm, seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **ARMS[arm][1]))


class Probe:
    def __init__(self):
        from acl.person import A, N_ACTIONS
        self.A, self.N = A, N_ACTIONS
        self.pops = []
        self.deaths = Counter()
        self.observed = set()                  # adults who ever saw a better-fed visible adult forage
        self.max_ed = defaultdict(float)
        self.near = defaultdict(lambda: defaultdict(int))
        self.forage = defaultdict(lambda: [0, 0])
        self.planned = defaultdict(set)
        self.rows = []
        self.planner_neighbours = []           # (year, [neighbour ids])
        self.habit = []
        self.child_cohort = {}
        self.child_rows = []

    def habit_value(self, p):
        vals = [p.q[(f * 8 + comp + AUTUMN) * self.N + self.A["forage"]] for f in (2, 3) for comp in (0, 4)]
        return sum(vals) / len(vals)

    def __call__(self, world, events):
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        year = tick // WPY
        c = world.cfg
        for e in events:
            if e["k"] == "death":
                if e.get("cause") == "starvation" and e.get("a") in self.child_cohort:
                    self.child_cohort[e["a"]]["starved"] = True
                self.deaths[e.get("cause")] += 1
        foragers = {e["a"] for e in events if e["k"] == "forage" and e.get("a")}
        living = world.living()
        adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
        if tick % 520 == 519:
            self.pops.append(len(living))
            if adults:
                self.habit.append(round(sum(self.habit_value(p) for p in adults) / len(adults), 4))
        # the same model rule as B2, applied in every arm, to know who ever saw a better-fed adult forage
        for p in adults:
            cands = [q for q in world.people_near(p.loc, c.perception, exclude=p.id)
                     if q.age(world.tick) >= 16 * WPY and q.edible() > p.edible()]
            if cands:
                m = min(cands, key=lambda q: (-q.edible(), q.id))
                if m.id in foragers:
                    self.observed.add(p.id)
        if wk == 2 * WPS:
            self.max_ed = defaultdict(float)
            self.near = defaultdict(lambda: defaultdict(int))
        if s == 2:
            for p in adults:
                self.max_ed[p.id] = max(self.max_ed[p.id], p.edible())
                for q in world.people_near(p.loc, c.perception, exclude=p.id):
                    if q.age(world.tick) >= 16 * WPY:
                        self.near[p.id][q.id] += 1
                f = self.forage[(year, p.id)]
                f[1] += 1
                f[0] += next((x[0] for x in (p.considered or []) if x[3]), None) == "forage"
        if wk == 3 * WPS:
            for p in adults:
                if self.forage.get((year, p.id), [0, 0])[1] < 10:
                    continue
                planned = self.max_ed.get(p.id, 0) >= 80
                if planned:
                    self.planned[p.id].add(year)
                    self.planner_neighbours.append((year, [q for q, n in self.near[p.id].items() if n >= 4]))
                f = self.forage[(year, p.id)]
                self.rows.append({"pid": p.id, "year": year, "planned": planned, "forage_share": round(f[0] / f[1], 3),
                                  "ever_observed": p.id in self.observed})
            self.child_cohort = {}
            for p in living:
                if p.age(world.tick) < 12 * WPY:
                    cid = p.caregiver or p.mother
                    carer = world.people.get(cid) if cid else None
                    self.child_cohort[p.id] = {"carer_food": round(carer.food + carer.seeds, 1) if carer and carer.alive else None,
                                               "starved": False}
        if wk == WPY - 1:
            self.child_rows.extend(self.child_cohort.values())
            self.child_cohort = {}

    def results(self):
        again = sum(1 for r in self.rows if r["planned"] and (r["year"] + 1) in self.planned[r["pid"]])
        nb = []
        for y, ids in self.planner_neighbours:
            for q in ids:
                f = self.forage.get((y + 1, q))
                if f and f[1] >= 10 and q not in {r["pid"] for r in self.rows if r["year"] == y and r["planned"]}:
                    nb.append(f[0] / f[1])
        return {"rows": self.rows, "planned_again": again, "neighbour_forage_next": nb, "habit": self.habit,
                "child_rows": self.child_rows, "deaths": dict(self.deaths)}


def fp(arm):
    sys.path.insert(1, str(E7))
    from run_e7 import code_hash
    return code_hash(ARMS[arm][0] / "acl")


def run(arm, seed):
    setup(arm)
    f0 = fp(arm)
    w = make_world(arm, seed)
    probe = Probe()
    w.observers.append(probe)
    t0 = time.time()
    for _ in range(120 * WPY):
        w.step()
        if not w.living():
            break
    e9 = json.loads((E9 / "output" / f"a2full_seed_{seed}.json").read_text(encoding="utf-8"))
    res = {"arm": arm, "seed": seed, "code_hash": f0, "code_hash_after": fp(arm), "pops": probe.pops,
           "matches_e9_a2full": probe.pops == e9["pops"], **probe.results(), "seconds": round(time.time() - t0)}
    OUT.mkdir(exist_ok=True)
    (OUT / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: alive {len(w.living())}, matches E9 {res['matches_e9_a2full']}, {res['seconds']}s", flush=True)


def verify(arm, seed=304, years=20):
    setup(arm)
    hs = []
    for with_probe in (False, True):
        w = make_world(arm, seed)
        if with_probe:
            w.observers.append(Probe())
        for _ in range(years * WPY):
            w.step()
        hs.append(w.state_hash())
    ok = hs[0] == hs[1]
    OUT.mkdir(exist_ok=True)
    with open(OUT / "verify.txt", "a", encoding="utf-8") as f:
        f.write(f"{arm} seed {seed}, {years} years: {'READ-ONLY' if ok else 'CHANGES THE WORLD'}\n")
    print(f"verify {arm}:", "READ-ONLY" if ok else "CHANGES THE WORLD", flush=True)
    return ok


if __name__ == "__main__":
    if sys.argv[1] == "verify":
        sys.exit(0 if verify(sys.argv[2]) else 1)
    elif sys.argv[1] == "all":
        me = [sys.executable, str(Path(__file__).resolve())]
        for arm in ("a", "b"):
            if subprocess.call(me + ["verify", arm]) != 0:
                sys.exit("ABORT: probe changes the world")
        jobs = [("zero", 304)] + [(a, s) for a in ("a", "b", "c") for s in SEEDS]
        jobs = [j for j in jobs if not (OUT / f"{j[0]}_seed_{j[1]}.json").exists()]
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda j: subprocess.call(me + [j[0], str(j[1])]), jobs))
        print("ALL DONE", flush=True)
    else:
        run(sys.argv[1], int(sys.argv[2]))
