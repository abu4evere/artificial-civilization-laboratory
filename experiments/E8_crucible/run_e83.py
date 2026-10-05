"""E8.3 starvation autopsy (E8_3_starvation_autopsy.md). Read-only replays of the E7 code, seeds 301–304, 120 years.

  python experiments/E8_crucible/run_e83.py all
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict, deque
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E7 = HERE.parent / "E7_passive"
sys.path.insert(0, str(E7 / "code_e7"))
from acl import matter  # noqa: E402
from acl.config import Config  # noqa: E402
from acl.world import World  # noqa: E402

SEEDS = (301, 302, 303, 304)
WPY, WPS = 52, 13
OUT = HERE / "output_e83"


class Probe:
    def __init__(self):
        self.pops = []
        self.hist = defaultdict(lambda: deque(maxlen=8))   # pid -> last 8 weeks
        self.deaths = []
        self.base_season = Counter()
        self.base_stage = Counter()
        self.base_starving_season = Counter()

    def _near(self, world, loc):
        c = world.cfg
        plants = stored = 0.0
        for dy in range(-c.reach, c.reach + 1):
            for dx in range(-c.reach, c.reach + 1):
                t = world.tile(((loc[0] + dx) % c.width, (loc[1] + dy) % c.height))
                plants += t.plants + t.crop
                stored += sum(st[1] + st[2] for st in t.stash)
        here = world.tile(loc)
        return round(here.plants + here.crop, 1), round(plants, 1), round(stored, 1)

    def __call__(self, world, events):
        tick = world.tick - 1
        week_in_season = (tick % WPY) % WPS
        season = (tick % WPY) // WPS
        for e in events:
            if e["k"] == "death" and e.get("cause") == "starvation" and e.get("a") in world.people:
                p = world.people[e["a"]]
                own, near, stored = self._near(world, p.loc)
                hist = list(self.hist[p.id])
                care = world.people.get(p.caregiver) if p.caregiver else None
                self.deaths.append({
                    "tick": tick, "year": tick // WPY, "season": season, "week_in_season": week_in_season,
                    "stage": p.stage(tick), "age": round(p.age(tick) / WPY, 1), "sick": bool(p.sick),
                    "carer_alive": bool(care and care.alive), "need": round(p.need(world.cfg, tick), 2),
                    "plants_own_tile": own, "plants_within_reach": near, "stored_within_reach": stored,
                    "holds_container": any(matter.factor(it, "carry") >= 1.4 for it in p.items),
                    "history": hist,
                })
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        for p in living:
            st = p.stage(world.tick)
            self.base_season[season] += 1
            self.base_stage[st] += 1
            if p.starving:
                self.base_starving_season[season] += 1
            chosen = next((x[0] for x in (p.considered or []) if x[3]), None)
            self.hist[p.id].append([round(p.edible(), 1), round(p.need(world.cfg, world.tick), 1), chosen,
                                    p.starving])


def run(seed):
    saved = json.loads((E7 / "output" / "e7" / f"seed_{seed}.json").read_text(encoding="utf-8"))
    w = World(Config(seed=seed))
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
    sp = [s["population"] for s in saved["samples"]][: len(probe.pops)]
    res = {"seed": seed, "replay_matches_saved": probe.pops == sp, "deaths": probe.deaths,
           "base_season": dict(probe.base_season), "base_stage": dict(probe.base_stage),
           "base_starving_season": dict(probe.base_starving_season)}
    OUT.mkdir(exist_ok=True)
    (OUT / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: replay matches {res['replay_matches_saved']}, starvation deaths {len(probe.deaths)}", flush=True)


def verify(seed=304, years=20):
    hs = []
    for with_probe in (False, True):
        w = World(Config(seed=seed))
        if with_probe:
            w.observers.append(Probe())
        for _ in range(years * WPY):
            w.step()
        hs.append(w.state_hash())
    ok = hs[0] == hs[1]
    OUT.mkdir(exist_ok=True)
    (OUT / "verify.txt").write_text(f"seed {seed}, {years} years: {'READ-ONLY' if ok else 'CHANGES THE WORLD'}\n")
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
