"""E13 pilot (read-only, descriptive). Replays E9 A2-full (A2 code, weight 1.0), seeds 301–304, 120 years.
1. Planners' habit value for foraging in autumn situations with 2+ weeks of food, against comparison adults'.
2. Adult-weeks in which a non-planner is within sight of a planner who is foraging that autumn week.
3. How often planners are the best fed / most respected adult within sight.

  python experiments/E13_following/run_pilot.py all
"""
from __future__ import annotations

import json
import statistics
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E9 = HERE.parent / "E9_anticipation"
sys.path.insert(0, str(E9 / "code_a2"))
from acl.config import Config  # noqa: E402
from acl.person import A, N_ACTIONS  # noqa: E402
from acl.world import World  # noqa: E402

SEEDS = (301, 302, 303, 304)
WPY, WPS = 52, 13
AUTUMN = 2
OUT = HERE / "output_pilot"


def autumn_forage_q(p):
    """Habit value of foraging in autumn with 2+ weeks of food (both company states, both food levels)."""
    vals = []
    for f in (2, 3):
        for comp in (0, 4):
            ctx = f * 8 + comp + AUTUMN
            vals.append(p.q[ctx * N_ACTIONS + A["forage"]])
    return sum(vals) / len(vals)


def respect_of(world, pid):
    return sum(q.rel[pid].respect for q in world.living() if pid in q.rel)


class Probe:
    def __init__(self):
        self.pops = []
        self.max_ed = defaultdict(float)
        self.short_now, self.short_prev = set(), set()
        self.qrows = []
        self.seen_foraging = 0
        self.autumn_adult_weeks = 0
        self.top_fed = []
        self.top_resp = []

    def __call__(self, world, events):
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        c = world.cfg
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
        if wk == 2 * WPS:
            self.max_ed = defaultdict(float)
        if s == 2:
            for p in adults:
                self.max_ed[p.id] = max(self.max_ed[p.id], p.edible())
        if s == 3:
            for p in adults:
                if p.starving:
                    self.short_now.add(p.id)
        if wk == 3 * WPS:                       # first week of winter: planners of this autumn, and their habits
            planners = {pid for pid, v in self.max_ed.items() if v >= 80}
            self.planners = planners
            for p in adults:
                if p.id in planners or p.id in self.short_prev:
                    self.qrows.append({"planner": p.id in planners, "q": round(autumn_forage_q(p), 4)})
        if wk == WPY - 1:
            self.short_prev, self.short_now = self.short_now, set()
        # sightings of planners foraging in autumn need this autumn's planners: use those holding 80+ so far
        if s == 2:
            foraging_planners = [p for p in adults if self.max_ed.get(p.id, 0) >= 80
                                 and next((x[0] for x in (p.considered or []) if x[3]), None) == "forage"]
            for p in adults:
                self.autumn_adult_weeks += 1
                if any(q.id != p.id and max(abs(q.loc[0] - p.loc[0]), abs(q.loc[1] - p.loc[1])) <= c.perception
                       for q in foraging_planners):
                    self.seen_foraging += 1
            if wk == 2 * WPS + 6:               # mid-autumn: rank planners among those within sight
                for q in [p for p in adults if self.max_ed.get(p.id, 0) >= 80]:
                    around = [o for o in world.people_near(q.loc, c.perception) if o.age(world.tick) >= 16 * WPY]
                    if len(around) >= 2:
                        self.top_fed.append(max(around, key=lambda o: o.edible()).id == q.id)
                        resp = {o.id: respect_of(world, o.id) for o in around}
                        self.top_resp.append(max(resp, key=resp.get) == q.id)


def run(seed):
    saved = json.loads((E9 / "output" / f"a2full_seed_{seed}.json").read_text(encoding="utf-8"))
    w = World(Config(seed=seed, anticipation_weight=1.0))
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
    res = {"seed": seed, "replay_matches_e9": probe.pops == saved["pops"], "qrows": probe.qrows,
           "seen_foraging": probe.seen_foraging, "autumn_adult_weeks": probe.autumn_adult_weeks,
           "top_fed": probe.top_fed, "top_resp": probe.top_resp}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: replay matches E9 {res['replay_matches_e9']}", flush=True)


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
