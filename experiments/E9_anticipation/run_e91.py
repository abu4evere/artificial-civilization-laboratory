"""E9.1 reach autopsy (E9_1_reach_autopsy.md). Read-only replays of E9 A2-full, seeds 301–304, 120 years.

  python experiments/E9_anticipation/run_e91.py all
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
from acl import mind  # noqa: E402
from acl.config import Config  # noqa: E402
from acl.world import World  # noqa: E402

SEEDS = (301, 302, 303, 304)
WPY, WPS = 52, 13
OUT = HERE / "output_e91"


class Probe:
    def __init__(self):
        self.pops = []
        self.aut = defaultdict(lambda: {"weeks": 0, "acting": 0, "max_edible": 0.0, "exp": None})
        self.short_prev = set()
        self.cur_short = set()
        self.winter_cohort = {}       # pid -> row, for adults at the first week of winter
        self.rows = []

    def __call__(self, world, events):
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        c = world.cfg
        starved = {e["a"] for e in events if e["k"] == "death" and e.get("cause") == "starvation" and e.get("a")}
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        for pid in starved:
            if pid in self.winter_cohort:
                self.winter_cohort[pid]["starved"] = True
        for p in living:
            if s == 3 and p.starving:
                self.cur_short.add(p.id)
            if s == 2 and p.age(world.tick) >= 16 * WPY:
                a = self.aut[p.id]
                if a["exp"] is None:
                    a["exp"] = p.expect.get("short@3", 0.0)
                a["weeks"] += 1
                h = mind.hunger_of(world, p, sum(d.need(c, world.tick) for d in world.dependents(p.id)))
                if c.anticipation_weight * p.expect.get("short@3", 0.0) > h + 1e-9:
                    a["acting"] += 1
                a["max_edible"] = max(a["max_edible"], p.edible())
        if wk == 3 * WPS:                       # first week of winter
            for p in living:
                a = self.aut.pop(p.id, None)
                if a and a["weeks"] >= 10:
                    self.winter_cohort[p.id] = {"exp": round(a["exp"], 3), "acting_share": round(a["acting"] / a["weeks"], 3),
                                                "hit80": a["max_edible"] >= 80, "short_prev": p.id in self.short_prev,
                                                "entry": round(p.food + p.seeds, 1), "starved": False, "alive_spring": None}
            self.aut.clear()
        if wk == WPY - 1:                       # end of winter: close the cohort
            alive = {p.id for p in living}
            for pid, r in self.winter_cohort.items():
                r["alive_spring"] = pid in alive
                self.rows.append(r)
            self.winter_cohort = {}
            self.short_prev = set(self.cur_short)
            self.cur_short = set()


def run(seed):
    saved = json.loads((HERE / "output" / f"a2full_seed_{seed}.json").read_text(encoding="utf-8"))
    w = World(Config(seed=seed, anticipation_weight=1.0))
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
    res = {"seed": seed, "replay_matches_e9": probe.pops == saved["pops"], "rows": probe.rows}
    OUT.mkdir(exist_ok=True)
    (OUT / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: replay matches E9 {res['replay_matches_e9']}, adult-winters {len(probe.rows)}", flush=True)


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
