"""E8.2 tool payoff (E8_2_tool_payoff.md). Read-only replays of the E7 code, seeds 301–304, 120 years.

  python experiments/E8_crucible/run_e82.py all
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
from acl import matter  # noqa: E402
from acl.config import Config  # noqa: E402
from acl.world import World  # noqa: E402

SEEDS = (301, 302, 303, 304)
WPY = 52
OUT = HERE / "output_e82"


def recipe_material_units(recipe: dict) -> int:
    """Raw material units a recipe consumes (1 per raw part; binder counts 1)."""
    if not recipe:
        return 1
    v = recipe.get("verb")
    if v == "strike":
        return 1
    if v == "shape":
        return 1
    if v == "heat":
        return 1 if recipe.get("part") in matter.MATERIALS else 0
    parts = recipe.get("parts", ())
    return sum(1 for x in parts if x in matter.MATERIALS) + 1


class Probe:
    def __init__(self):
        self.pops = []
        self.c = Counter()
        self.forage_got = defaultdict(list)       # pid -> food per foraging act
        self.tool_gain = defaultdict(float)       # id(item) -> upper-bound food added
        self.items = {}                           # id(item) -> (item, maker pid, cost units, made tick)
        self.hunts = Counter()
        self.food_ok = Counter()

    def __call__(self, world, events):
        tick = world.tick - 1
        c = world.cfg
        people = world.people
        for e in events:
            k, a = e["k"], e.get("a")
            if k == "forage" and a in people:
                p = people[a]
                if p.age(world.tick) < 16 * WPY:
                    continue
                got = e.get("got", 0.0)
                idx, f = matter.best_item(p, "forage")
                self.forage_got[a].append(got)
                self.c["forage_acts"] += 1
                self.c["food_foraged"] += got
                gain = got * (1 - 1 / f) if f > 1 else 0.0
                self.c["food_from_tools_ub"] += gain
                if idx >= 0:
                    self.tool_gain[id(p.items[idx])] += gain
                room = matter.carry_capacity(world, p) - p.edible()
                if room < 1.0:
                    self.c["forage_capped_by_carry"] += 1
            elif k in ("make", "play") and e.get("thing") and a in people:
                p = people[a]
                it = next((x for x in reversed(p.items) if x["sig"] == e["thing"]), None)
                if it is not None and id(it) not in self.items:
                    self.items[id(it)] = (it, a, recipe_material_units(p.recipes.get(e["thing"])), tick)
            elif k == "hunt":
                party = sorted(set([a] + list(e.get("party", []))))
                self.food_ok["hunter_weeks"] += len(party)
                tool = any(matter.best_item(people[x], "hunt")[1] > 1.0 for x in party if x in people)
                key = "with_tool" if tool else "without_tool"
                self.hunts[key + "_hunts"] += 1
                if e.get("success"):
                    self.hunts[key + "_success"] += 1
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        for p in living:
            if p.age(world.tick) < 16 * WPY:
                continue
            self.food_ok["adult_weeks"] += 1
            if p.edible() >= p.need(c, world.tick):
                self.food_ok["week_on_hand"] += 1
            if p.starving:
                self.food_ok["starving"] += 1

    def results(self):
        mean_forage = {pid: statistics.mean(v) for pid, v in self.forage_got.items() if v}
        overall = self.c["food_foraged"] / max(1, self.c["forage_acts"])
        payback = []
        for oid, (it, maker, units, t0) in self.items.items():
            per_week = mean_forage.get(maker, overall)
            cost = (1 + units) * per_week
            if cost > 0:
                payback.append(self.tool_gain.get(oid, 0.0) / cost)
        return {
            "forage": dict(self.c),
            "share_food_from_tools_ub": round(self.c["food_from_tools_ub"] / max(1e-9, self.c["food_foraged"]), 4),
            "mean_food_per_forage_week": round(overall, 2),
            "made_things": len(payback),
            "payback_median": round(statistics.median(payback), 3) if payback else None,
            "payback_share_ge1": round(sum(1 for x in payback if x >= 1) / len(payback), 3) if payback else None,
            "payback_share_ge2": round(sum(1 for x in payback if x >= 2) / len(payback), 3) if payback else None,
            "food": dict(self.food_ok),
            "hunts": dict(self.hunts),
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
