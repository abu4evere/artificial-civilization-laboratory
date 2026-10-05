"""E11 runner (E11_preregistration.md). Arms: arm0 (E7 code), s1low, s1high (E11 code, loss weight 1.0, story
0.25 / 0.50), plus the zero-story check (E11 code, loss weight 1.0, story 0; must equal E10's O2 arm, seed 304).
Seeds 301–304, 120 years. Read-only probe.

  python experiments/E11_stories/run_e11.py all
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
E11 = HERE / "code_e11"
ARMS = {"arm0": (E7 / "code_e7", {}), "s1low": (E11, {"loss_weight": 1.0, "story_value": 0.25}),
        "s1high": (E11, {"loss_weight": 1.0, "story_value": 0.5}), "zero": (E11, {"loss_weight": 1.0})}
SEEDS = (301, 302, 303, 304)
WPY, WPS = 52, 13
OUT = HERE / "output"


def setup(arm):
    sys.path.insert(0, str(ARMS[arm][0]))
    sys.path.insert(1, str(E7))
    import acl
    assert Path(acl.__file__).resolve().parent == (ARMS[arm][0] / "acl").resolve()


def make_world(arm, seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, **ARMS[arm][1]))


class Probe:
    """Tracks deaths, bereavement and story-hearing from events, so the same groups exist in every arm."""

    def __init__(self):
        from acl.historian import classify
        self.classify = classify
        self.pops = []
        self.deaths = Counter()
        self.cause_of = {}                     # death eid -> cause
        self.bereaved = defaultdict(list)
        self.heard = defaultdict(list)         # pid -> ticks of hearing a hunger story (accepted or known)
        self.story_counts = Counter()
        self.autumn = defaultdict(lambda: {"weeks": 0, "forage": 0, "max_edible": 0.0})
        self.planned = defaultdict(set)        # pid -> years they held 80+ in autumn
        self.rows = []
        self.child_cohort = {}
        self.child_rows = []
        self.carriers_made = 0

    def __call__(self, world, events):
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        year = tick // WPY
        for e in events:
            k = e["k"]
            if k == "death":
                self.deaths[f"{e.get('cause')}@{s}"] += 1
                self.cause_of[e["id"]] = e.get("cause")
                if e.get("cause") == "starvation" and e.get("a") in world.people:
                    dead = world.people[e["a"]]
                    if dead.age(tick) < 12 * WPY:
                        self.deaths[f"child_starvation@{s}"] += 1
                        cid = dead.caregiver or dead.mother
                        if cid:
                            self.bereaved[cid].append(tick)
                    if dead.id in self.child_cohort:
                        self.child_cohort[dead.id]["starved"] = True
            elif k == "told" and self.cause_of.get(e.get("story")) == "starvation":
                self.story_counts["told"] += 1
                if e.get("heard") in ("accepted", "known"):
                    self.story_counts["heard"] += 1
                    self.heard[e.get("b")].append(tick)
            elif k in ("make", "play") and e.get("thing"):
                props = {x: e[x] for x in ("edge", "reach", "hard", "contain", "warm", "float") if x in e}
                if props and "carrier" in self.classify(props):
                    self.carriers_made += 1
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        if s == 2:
            for p in living:
                if p.age(world.tick) < 16 * WPY:
                    continue
                a = self.autumn[p.id]
                a["weeks"] += 1
                a["max_edible"] = max(a["max_edible"], p.edible())
                ch = next((x[0] for x in (p.considered or []) if x[3]), None)
                a["forage"] += ch == "forage"
        if wk == 3 * WPS:                      # first week of winter
            for p in living:
                a = self.autumn.pop(p.id, None)
                if a and a["weeks"] >= 10:
                    recent = lambda ts: any(0 < tick - t <= WPY for t in ts)
                    planned = a["max_edible"] >= 80
                    if planned:
                        self.planned[p.id].add(year)
                    self.rows.append({
                        "pid": p.id, "year": year, "forage_share": round(a["forage"] / a["weeks"], 3),
                        "planned": planned, "entry": round(p.food + p.seeds, 1),
                        "has_children": bool(world.dependents(p.id)),
                        "heard_recent": recent(self.heard.get(p.id, [])), "ever_heard": bool(self.heard.get(p.id)),
                        "bereaved_recent": recent(self.bereaved.get(p.id, [])), "ever_bereaved": bool(self.bereaved.get(p.id)),
                    })
            self.autumn.clear()
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


def fp(arm):
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
    saved = json.loads((E7 / "output" / "e7" / f"seed_{seed}.json").read_text(encoding="utf-8"))
    sp = [x["population"] for x in saved["samples"]][: len(probe.pops)]
    planned_again = sum(1 for r in probe.rows if r["planned"] and (r["year"] + 1) in probe.planned[r["pid"]])
    res = {"arm": arm, "seed": seed, "years": w.year, "code_hash": f0, "code_hash_after": fp(arm),
           "matches_saved_e7": probe.pops == sp, "pops": probe.pops, "deaths": dict(probe.deaths),
           "story_counts": dict(probe.story_counts), "rows": probe.rows, "child_rows": probe.child_rows,
           "planned_again": planned_again, "carriers_made": probe.carriers_made, "seconds": round(time.time() - t0)}
    OUT.mkdir(exist_ok=True)
    (OUT / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: {w.year} years, alive {len(w.living())}, {res['seconds']}s", flush=True)


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
        for arm in ("arm0", "s1high"):
            if subprocess.call(me + ["verify", arm]) != 0:
                sys.exit("ABORT: probe changes the world")
        jobs = [("zero", 304)] + [(a, s) for a in ("arm0", "s1low", "s1high") for s in SEEDS]
        jobs = [j for j in jobs if not (OUT / f"{j[0]}_seed_{j[1]}.json").exists()]
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda j: subprocess.call(me + [j[0], str(j[1])]), jobs))
        print("ALL DONE", flush=True)
    else:
        run(sys.argv[1], int(sys.argv[2]))
