"""E3 forensics: where were births lost? Read-only recorder run on E1's code or E2's code.

Usage:
    python experiments/E3_births/forensics.py e1 101 102 ...
    python experiments/E3_births/forensics.py e2 101 102 ...

Runs each seed for 100 years with the same observers E1 and E2 had (historian, Lab) plus a BirthProbe,
checks the year-100 world against the saved snapshot of that experiment (must be identical), and writes
output/<code>_seed_<n>.json with one row of counts per year.
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
CODE = sys.argv[1]
sys.path.insert(0, str(HERE / "code_e1") if CODE == "e1" else str(ROOT))

from acl.config import CHILD_END, WEEKS_PER_YEAR, Config  # noqa: E402
from acl.historian import Historian  # noqa: E402
from acl.measure import Lab  # noqa: E402
from acl.runner import load_snapshot  # noqa: E402
from acl.util import distance  # noqa: E402
from acl.world import World  # noqa: E402

SAVED = ROOT / "experiments" / ("E1" if CODE == "e1" else "E2") / "output"
OUT = HERE / "output"


class BirthProbe:
    def __init__(self):
        self.rows = []
        self.c = Counter()
        self.island = None

    def _island(self, world, loc):
        if self.island is None:
            self.island = {}
            for i, comp in enumerate(world.landmasses()):
                for xy in comp:
                    self.island[xy] = i
        return self.island.get(tuple(loc))

    def __call__(self, world, events):
        cfg = world.cfg
        tick = world.tick - 1
        c = self.c
        for e in events:
            if e["k"] in ("pair", "pregnant", "birth"):
                c[e["k"]] += 1
        living = world.living()
        by_id = {p.id: p for p in living}
        # what fertile-age adults chose, and what was on their minds
        for d in world.week_decisions:
            p = by_id.get(d.agent_id)
            if p is None or not (16 <= p.years(tick) < 45):
                continue
            c["choice:" + d.chosen[0]] += 1
            c["choices"] += 1
            if p.partner is None and d.chosen[0] == "court":
                c["court_by_unpaired"] += 1
            if p.thoughts:
                c["mind:" + p.thoughts[0][0]] += 1
        for p in living:
            years = p.years(tick)
            if p.sex == "F" and 16 <= years < 45:
                c["fw"] += 1
                c["fw_health"] += p.health
                c["fw_food_weeks"] += min(10.0, p.edible() / max(1.0, p.need(cfg, tick)))
                if p.starving:
                    c["fw_starving"] += 1
                mate = by_id.get(p.partner) if p.partner else None
                if mate is None:
                    continue
                c["fw_partner"] += 1
                d = distance(p.loc, mate.loc, cfg.width, cfg.height)
                c["fw_partner_dist"] += min(d, 20)
                if d > cfg.camp_radius:
                    c["fw_apart"] += 1
                    a, b = self._island(world, p.loc), self._island(world, mate.loc)
                    if a is not None and b is not None and a != b:
                        c["fw_apart_water"] += 1
                    continue
                c["fw_together"] += 1
                if p.pregnant is not None:
                    c["blocked_pregnant"] += 1
                elif tick - p.last_birth < cfg.nursing_weeks and _youngest_alive(world, p):
                    c["blocked_nursing"] += 1
                elif p.health < 50:
                    c["blocked_health"] += 1
                elif p.starving:
                    c["blocked_starving"] += 1
                elif mate.age(tick) < CHILD_END:
                    c["blocked_mate_young"] += 1
                else:
                    c["fw_can_conceive"] += 1
            # unpaired adults: possible mates in reach this week, and on their island
            if p.stage(tick) == "adult" and p.partner is None and years < 45:
                c["ua"] += 1
                mine = self._island(world, p.loc)
                in_reach = pool = 0
                for q in living:
                    if (q.sex == p.sex or q.partner is not None or q.stage(tick) != "adult"
                            or abs(p.birth - q.birth) > 15 * WEEKS_PER_YEAR or world.kinship(p, q) > 0
                            or q.id in p.wards or p.id in q.wards):
                        continue
                    if self._island(world, q.loc) == mine:
                        pool += 1
                    if distance(p.loc, q.loc, cfg.width, cfg.height) <= cfg.reach:
                        in_reach += 1
                c["ua_pool_island"] += pool
                if in_reach:
                    c["ua_encounter"] += 1
                    c["ua_mates_in_reach"] += in_reach
        if tick % WEEKS_PER_YEAR == WEEKS_PER_YEAR - 1:
            row = dict(self.c)
            row["year"] = tick // WEEKS_PER_YEAR
            row["population"] = len(living)
            self.rows.append(row)
            self.c = Counter()


def _youngest_alive(world, p):
    for cid in reversed(p.children):
        child = world.people[cid]
        if child.mother == p.id:
            return child.alive
    return False


def run(seed, years=100):
    w = World(Config(seed=seed))
    h = Historian()
    probe = BirthProbe()
    w.observers += [h, Lab(h), probe]
    t0 = time.time()
    check = None
    for y in range(years):
        for _ in range(WEEKS_PER_YEAR):
            w.step()
        if not w.living():
            break
    if w.year >= 100 and (SAVED / f"seed_{seed}_year100.json.gz").exists():
        sw, _ = load_snapshot(SAVED / f"seed_{seed}_year100.json.gz")
        check = sw.state_hash() == w.state_hash()
    elif w.year < 100:
        # died out before year 100: compare with the saved end state instead
        sw, _ = load_snapshot(SAVED / f"seed_{seed}_end.json.gz")
        check = sw.tick == w.tick and sw.state_hash() == w.state_hash()
    OUT.mkdir(exist_ok=True)
    out = {"code": CODE, "seed": seed, "years": w.year, "identical": check, "seconds": round(time.time() - t0),
           "rows": probe.rows}
    (OUT / f"{CODE}_seed_{seed}.json").write_text(json.dumps(out), encoding="utf-8")
    return out


if __name__ == "__main__":
    for s in [int(a) for a in sys.argv[2:]]:
        if (OUT / f"{CODE}_seed_{s}.json").exists():
            print(f"{CODE} seed {s}: already done", flush=True)
            continue
        r = run(s)
        print(f"{CODE} seed {s}: {r['years']} years, {r['seconds']}s, identical to the saved run: {r['identical']}",
              flush=True)
