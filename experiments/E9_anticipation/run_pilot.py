"""E9 pilot: read-only. How hungry do people get in each season, and how often would A2's anticipation (computed
in the shadow, with the thirst mechanism's own numbers) change the pull toward food? Feasibility only: these
results do not set A2's numbers, which are copied from the existing thirst mechanism.

  python experiments/E9_anticipation/run_pilot.py all
"""
from __future__ import annotations

import json
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E7 = HERE.parent / "E7_passive"
sys.path.insert(0, str(E7 / "code_e7"))
from acl import mind  # noqa: E402
from acl.config import Config  # noqa: E402
from acl.world import World  # noqa: E402

SEEDS = (301, 302, 303, 304)
WPY, WPS = 52, 13
RATE, WEIGHT = 0.1, 0.3 / 0.8        # copied from the thirst mechanism: learning rate, expected:felt weight
OUT = HERE / "output_pilot"


class Probe:
    def __init__(self):
        self.pops = []
        self.shadow = defaultdict(dict)                 # pid -> {season: expectation}, learned from hunger level
        self.shadow2 = defaultdict(dict)                # pid -> {season: expectation}, learned from going short (starving)
        self.would_change2 = Counter()
        self.lift2 = defaultdict(list)
        self.hunger_by_season = defaultdict(list)
        self.starving_by_season = Counter()
        self.weeks_by_season = Counter()
        self.would_change = Counter()                   # season -> adult-weeks where A2 would raise the pull
        self.lift = defaultdict(list)                   # season -> size of the raise when it happens
        self.winters = defaultdict(lambda: {"hungry": 0})
        self.cur_winter = defaultdict(int)
        self.deaths_prior_hungry_winters = []

    def __call__(self, world, events):
        tick = world.tick - 1
        s = (tick % WPY) // WPS
        for e in events:
            if e["k"] == "death" and e.get("cause") == "starvation" and e.get("a"):
                self.deaths_prior_hungry_winters.append(self.winters[e["a"]]["hungry"])
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        for p in living:
            if p.stage(world.tick) == "infant":
                continue
            h = mind.hunger_of(world, p)
            if p.age(world.tick) >= 16 * WPY:
                self.hunger_by_season[s].append(h)
                self.weeks_by_season[s] += 1
                self.starving_by_season[s] += bool(p.starving)
                nxt = self.shadow[p.id].get((s + 1) % 4, 0.0)
                felt = WEIGHT * nxt
                if felt > h + 1e-9:
                    self.would_change[s] += 1
                    self.lift[s].append(felt - h)
            if s == 3:
                self.cur_winter[p.id] = max(self.cur_winter[p.id], int(p.starving > 0))
            if p.age(world.tick) >= 16 * WPY:
                felt2 = WEIGHT * self.shadow2[p.id].get((s + 1) % 4, 0.0)
                if felt2 > h + 1e-9:
                    self.would_change2[s] += 1
                    self.lift2[s].append(felt2 - h)
            e = self.shadow[p.id].get(s)
            self.shadow[p.id][s] = h if e is None else e + RATE * (h - e)
            short = 1.0 if p.starving else 0.0
            e2 = self.shadow2[p.id].get(s)
            self.shadow2[p.id][s] = short if e2 is None else e2 + RATE * (short - e2)
        if tick % WPY == WPY - 1:                       # year's end: close the winter just lived
            for pid, hungry in self.cur_winter.items():
                self.winters[pid]["hungry"] += hungry
            self.cur_winter.clear()

    def results(self):
        S = ("spring", "summer", "autumn", "winter")
        exp_winter = [d.get(3) for d in self.shadow.values() if d.get(3) is not None]
        return {
            "mean_hunger": {S[k]: round(statistics.mean(v), 3) for k, v in self.hunger_by_season.items()},
            "starving_share": {S[k]: round(self.starving_by_season[k] / self.weeks_by_season[k], 4) for k in range(4)},
            "shadow_winter_expectation": {"n": len(exp_winter), "median": round(statistics.median(exp_winter), 3) if exp_winter else None,
                                          "share_over_0.3": round(sum(1 for x in exp_winter if x > 0.3) / len(exp_winter), 3) if exp_winter else None},
            "share_weeks_A2_would_raise_pull": {S[k]: round(self.would_change[k] / self.weeks_by_season[k], 3) for k in range(4)},
            "median_raise_when_it_does": {S[k]: round(statistics.median(v), 3) for k, v in self.lift.items() if v},
            "B_shadow_winter_expectation": {"median": round(statistics.median(x2), 3) if (x2 := [d.get(3) for d in self.shadow2.values() if d.get(3) is not None]) else None,
                                            "share_over_0.3": round(sum(1 for x in x2 if x > 0.3) / len(x2), 3) if x2 else None,
                                            "share_over_0.1": round(sum(1 for x in x2 if x > 0.1) / len(x2), 3) if x2 else None},
            "B_share_weeks_would_raise_pull": {S[k]: round(self.would_change2[k] / self.weeks_by_season[k], 3) for k in range(4)},
            "B_median_raise": {S[k]: round(statistics.median(v), 3) for k, v in self.lift2.items() if v},
            "starvation_deaths_by_prior_hungry_winters": dict(Counter(self.deaths_prior_hungry_winters)),
        }


def run(seed):
    saved = json.loads((E7 / "output" / "e7" / f"seed_{seed}.json").read_text(encoding="utf-8"))
    w = World(Config(seed=seed))
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
    sp = [s["population"] for s in saved["samples"]][: len(probe.pops)]
    res = {"seed": seed, "replay_matches_saved": probe.pops == sp, **probe.results()}
    OUT.mkdir(exist_ok=True)
    (OUT / f"seed_{seed}.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(f"seed {seed}: replay matches {res['replay_matches_saved']}", flush=True)


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
