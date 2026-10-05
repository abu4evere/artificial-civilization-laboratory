"""E9.3 planners autopsy (E9_3_planners_autopsy.md). Read-only replays of E9 A2-full, seeds 301–304, 120 years.

  python experiments/E9_anticipation/run_e93.py all
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "code_a2"))
from acl.config import Config  # noqa: E402
from acl.world import World  # noqa: E402

SEEDS = (301, 302, 303, 304)
WPY, WPS = 52, 13
OUT = HERE / "output_e93"
TRAITS = ("care", "diligence", "anxiety", "curiosity", "kindness")


class Probe:
    def __init__(self):
        self.pops = []
        self.max_ed = defaultdict(float)
        self.short_now = set()
        self.short_prev = set()
        self.cohort = {}           # pid -> record for the winter under way
        self.rows = []
        self.planned_years = defaultdict(set)

    def __call__(self, world, events):
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        year = tick // WPY
        if self.cohort:
            for e in events:
                a = e.get("a")
                if e["k"] == "give" and a in self.cohort:
                    self.cohort[a]["given"] += e.get("amount", 0.0)
                elif e["k"] == "put" and a in self.cohort and e.get("thing") in ("food", "seeds"):
                    self.cohort[a]["put"] += e.get("amount", 0.0)
                elif e["k"] == "death" and e.get("cause") == "starvation" and a in world.people:
                    dead = world.people[a]
                    if a in self.cohort:
                        self.cohort[a]["starved"] = True
                    cid = dead.caregiver or dead.mother
                    if cid in self.cohort and dead.age(tick) < 12 * WPY:
                        self.cohort[cid]["child_starved"] = True
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        for p in living:
            if s == 3 and p.starving:
                self.short_now.add(p.id)
            if s == 2 and p.age(world.tick) >= 16 * WPY:
                self.max_ed[p.id] = max(self.max_ed[p.id], p.edible())
        if wk == 3 * WPS:                          # first week of winter
            self.cohort = {}
            for p in living:
                if p.age(world.tick) < 16 * WPY or p.id not in self.max_ed:
                    continue
                planner = self.max_ed[p.id] >= 80
                if planner:
                    self.planned_years[p.id].add(year)
                if planner or p.id in self.short_prev:
                    self.cohort[p.id] = {
                        "pid": p.id, "planner": planner, "year": year, "age": round(p.age(world.tick) / WPY, 1),
                        "generation": p.generation, "genes": {k: round(p.genes[k], 2) for k in TRAITS},
                        "foraging_skill": round(p.skills["foraging"], 2), "dependents": len(world.dependents(p.id)),
                        "expect_winter": p.expect.get("short@3", 0.0), "food_start": round(p.edible(), 1),
                        "given": 0.0, "put": 0.0, "starved": False, "child_starved": False, "food_end": None}
            self.max_ed = defaultdict(float)
        if wk == WPY - 1:                          # last week of winter
            for pid, r in self.cohort.items():
                q = world.people.get(pid)
                r["food_end"] = round(q.edible(), 1) if q and q.alive else None
                self.rows.append(r)
            self.cohort = {}
            self.short_prev, self.short_now = self.short_now, set()



def run(seed):
    saved = json.loads((HERE / "output" / f"a2full_seed_{seed}.json").read_text(encoding="utf-8"))
    w = World(Config(seed=seed, anticipation_weight=1.0))
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
    rows = probe.rows
    res = {"seed": seed, "replay_matches_e9": probe.pops == saved["pops"], "rows": rows,
           "planned_years": {k: sorted(v) for k, v in probe.planned_years.items()}}
    OUT.mkdir(exist_ok=True)
    (OUT / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: replay matches E9 {res['replay_matches_e9']}, rows {len(rows)}", flush=True)


def verify(seed=304, years=20):
    hs = []
    for with_probe in (False, True):
        w = World(Config(seed=seed, anticipation_weight=1.0))
        if with_probe:
            w.observers.append(Probe())
        for _ in range(years * WPY):
            w.step()
        hs.append(w.state_hash())
    ok = hs[0] == hs[1]
    print("verify:", "READ-ONLY" if ok else "CHANGES THE WORLD", flush=True)
    return ok


if __name__ == "__main__":
    if sys.argv[1] == "verify":
        sys.exit(0 if verify() else 1)
    elif sys.argv[1] == "all":
        me = [sys.executable, str(Path(__file__).resolve())]
        if subprocess.call(me + ["verify"]) != 0:
            sys.exit("ABORT")
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda s: subprocess.call(me + [str(s)]), SEEDS))
    else:
        run(int(sys.argv[1]))
