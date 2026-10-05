"""E13R autopsy (read-only; questions.md). Replays E13R arms a and b, seeds 501-516, and records the children's and
the habit's questions.

  python experiments/E13R_replication/autopsy/run_autopsy.py all
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import run_e13r as R  # noqa: E402

WPY, WPS = 52, 13
OUT = HERE / "output"
BANDS = ((None, "no carer"), (5, "under 5"), (20, "5-20"), (50, "20-50"), (10 ** 9, "50+"))


def band(food):
    if food is None:
        return "no carer"
    for lim, name in BANDS[1:]:
        if food < lim:
            return name
    return "50+"


class Probe:
    def __init__(self):
        self.pops = []
        self.forage = defaultdict(lambda: [0, 0])        # season -> [forage weeks, adult weeks]
        self.short_winter = [0, 0]                       # adult winter-weeks going short, total
        self.adult_deaths_winter = 0
        self.births = 0
        self.entry = []                                  # adult food at start of winter
        self.exit = []                                   # adult food at end of winter
        self.cohort = {}
        self.child_rows = []
        self.stocked = {}                                # carer id -> [start, w4, w8, w12, given to others]
        self.stocked_rows = []
        self.deps_per_carer = []

    def __call__(self, world, events):
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        living = world.living()
        adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
        if tick % 520 == 519:
            self.pops.append(len(living))
        for e in events:
            k = e["k"]
            if k == "birth":
                self.births += 1
            elif k == "death" and e.get("cause") == "starvation":
                if e.get("a") in self.cohort:
                    c = self.cohort[e["a"]]
                    c["starved"] = True
                    c["death_week"] = wk - 3 * WPS
                elif s == 3 and e.get("age", 0) >= 16:
                    self.adult_deaths_winter += 1
            elif k == "give" and s == 3 and e.get("a") in self.stocked:
                q = world.people.get(e.get("b"))
                if q is None or q.caregiver != e["a"]:
                    self.stocked[e["a"]][4] += e.get("amount", 0.0)
        for p in adults:
            f = self.forage[s]
            f[1] += 1
            f[0] += next((x[0] for x in (p.considered or []) if x[3]), None) == "forage"
            if s == 3:
                self.short_winter[1] += 1
                self.short_winter[0] += bool(p.starving)
        if s == 3:
            for cid, c in self.cohort.items():
                ch = world.people.get(cid)
                if ch is not None and ch.alive:
                    carer = world.people.get(c["carer"]) if c["carer"] else None
                    c["carer_alive"] = bool(carer and carer.alive)
                    c["carer_food_last"] = round(carer.edible(), 1) if carer and carer.alive else None
            for pid, row in self.stocked.items():
                q = world.people.get(pid)
                for i, w in ((1, 4), (2, 8), (3, 12)):
                    if wk == 3 * WPS + w:
                        row[i] = round(q.edible(), 1) if q and q.alive else None
        if wk == 3 * WPS:
            self.entry.extend(round(p.edible(), 1) for p in adults)
            self.cohort, self.stocked = {}, {}
            carers = defaultdict(int)
            for p in living:
                if p.age(world.tick) < 12 * WPY:
                    cid = p.caregiver or p.mother
                    carer = world.people.get(cid) if cid else None
                    alive = bool(carer and carer.alive)
                    food = round(carer.edible(), 1) if alive else None
                    self.cohort[p.id] = {"carer": cid if alive else None, "band": band(food), "start_food": food,
                                         "age": round(p.age(world.tick) / WPY, 1), "starved": False,
                                         "death_week": None, "carer_alive": alive, "carer_food_last": food}
                    if alive:
                        carers[cid] += 1
            for cid, n in carers.items():
                self.deps_per_carer.append(n)
                q = world.people[cid]
                if q.edible() >= 20:
                    self.stocked[cid] = [round(q.edible(), 1), None, None, None, 0.0]
            for c in self.cohort.values():
                c["deps"] = carers.get(c["carer"], 0) if c["carer"] else 0
        if wk == WPY - 1:
            self.exit.extend(round(p.edible(), 1) for p in adults)
            self.child_rows.extend(self.cohort.values())
            self.stocked_rows.extend(self.stocked.values())
            self.cohort, self.stocked = {}, {}

    def results(self):
        return {"pops": self.pops, "forage": {str(k): v for k, v in self.forage.items()},
                "short_winter": self.short_winter, "adult_deaths_winter": self.adult_deaths_winter,
                "births": self.births, "entry": self.entry, "exit": self.exit, "child_rows": self.child_rows,
                "stocked_rows": self.stocked_rows, "deps_per_carer": self.deps_per_carer}


def run(arm, seed):
    R.setup(arm)
    w = R.make_world(arm, seed)
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
        if not w.living():
            break
    saved = json.loads((R.OUT / f"{arm}_seed_{seed}.json").read_text(encoding="utf-8"))
    res = {"arm": arm, "seed": seed, "replay_matches": probe.pops == saved["pops"], **probe.results()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: replay matches {res['replay_matches']}", flush=True)


def verify(arm, seed=501, years=20):
    R.setup(arm)
    hs = []
    for with_probe in (False, True):
        w = R.make_world(arm, seed)
        if with_probe:
            w.observers.append(Probe())
        for _ in range(years * WPY):
            w.step()
        hs.append(w.state_hash())
    ok = hs[0] == hs[1]
    OUT.mkdir(parents=True, exist_ok=True)
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
        jobs = [(a, s) for a in ("a", "b") for s in R.SEEDS if not (OUT / f"{a}_seed_{s}.json").exists()]
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda j: subprocess.call(me + [j[0], str(j[1])]), jobs))
        print("ALL DONE", flush=True)
    else:
        run(sys.argv[1], int(sys.argv[2]))
