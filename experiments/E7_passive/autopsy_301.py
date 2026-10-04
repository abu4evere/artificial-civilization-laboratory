"""E7.5: autopsy of seed 301 (E7 code). Watch-only replay to year 135.

Questions: what exactly appeared in year 115, who did it, why that person, why that world, and did fired clay
matter. The probe reads events and people; it changes nothing. The replay is checked against the saved E7 run
(population at every 10-year sample) before any answer is trusted.

    python experiments/E7_passive/autopsy_301.py     -> output/autopsy_301.json
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "code_e7"))
sys.path.insert(1, str(HERE.parent / "E6_novelty"))
from acl.config import WEEKS_PER_YEAR, Config  # noqa: E402
from acl.world import World  # noqa: E402
from novelty import LASTING_PROPS, profile  # noqa: E402

SEED, YEARS = 301, 135
saved = json.loads((HERE / "output" / "e7" / f"seed_{SEED}.json").read_text(encoding="utf-8"))
late = [n for n in saved["novelties"] if n["lasting"] and n["first_year"] > 100]
assert len(late) == 1, late
TARGET = eval(late[0]["key"])          # ('make', ('made', profile)) as the recorder wrote it
KIND = TARGET[1][1]


def props_of(e):
    p = e.get("props") or {k: e[k] for k in LASTING_PROPS if k in e}
    return p or None


class Probe:
    def __init__(self):
        self.of_kind = []            # every make/play of a thing of the target kind: [tick, kind, actor, sig]
        self.sigs = set()
        self.learn = []              # learning any of those sigs: [tick, learner, source, sig, how]
        self.fired = []              # passive firings: [tick, actor, sig]
        self.make_counts = Counter()  # all 'make' events per year, for context

    def __call__(self, world, events):
        tick = world.tick - 1
        for e in events:
            k = e["k"]
            if k == "make":
                self.make_counts[tick // WEEKS_PER_YEAR] += 1
            if k in ("make", "play"):
                pr = props_of(e)
                if pr and profile(pr, 100) == KIND:
                    self.of_kind.append([tick, k, e.get("a"), e.get("thing")])
                    self.sigs.add(e.get("thing"))
            elif k == "learn" and e.get("thing") in self.sigs:
                self.learn.append([tick, e.get("a"), e.get("b"), e.get("thing"), e.get("how")])
            elif k == "consequence" and e.get("what") == "ceramic_passive":
                self.fired.append([tick, e.get("a"), e.get("thing")])


def person_card(world, pid):
    p = world.people[pid]
    name = lambda i: world.people[i].name if i in world.people else None
    return {"id": pid, "name": p.name, "born_year": p.birth // WEEKS_PER_YEAR,
            "age_at_115": round((115 * WEEKS_PER_YEAR - p.birth) / WEEKS_PER_YEAR, 1),
            "generation": getattr(p, "generation", None), "genes": {k: round(v, 2) for k, v in p.genes.items()},
            "mother": name(p.mother), "father": name(p.father), "alive": p.alive,
            "death": [p.death_tick // WEEKS_PER_YEAR, p.death_cause] if not p.alive else None,
            "skills": {k: round(v, 2) for k, v in p.skills.items()},
            "recipes_now": sorted(p.recipes)[:40]}


def main():
    w = World(Config(seed=SEED))
    probe = Probe()
    w.observers.append(probe)
    pops = []
    for y in range(YEARS):
        for _ in range(WEEKS_PER_YEAR):
            w.step()
        if y % 10 == 9:
            pops.append(len(w.living()))
    saved_pops = [s["population"] for s in saved["samples"]][: len(pops)]
    matches = pops == saved_pops
    print("replay matches saved run:", matches, pops, saved_pops)

    of_kind = probe.of_kind
    first_make = next(x for x in of_kind if x[1] == "make")
    first_any = of_kind[0]
    makers_first10 = sorted({x[2] for x in of_kind if x[1] == "make" and x[0] - first_make[0] <= 10 * WEEKS_PER_YEAR})
    by_sig = defaultdict(list)
    for x in of_kind:
        by_sig[x[3]].append(x)
    recipe_of = {s: (w.knowledge.get(s) or {}) for s in probe.sigs}
    involves_clay = {s: ("clay" in s) for s in probe.sigs}
    fired_before = [f for f in probe.fired if f[0] < first_make[0]]
    out = {
        "replay_matches_saved": matches,
        "target": late[0],
        "kind_profile": dict(KIND),
        "first_ever_of_kind": {"year": first_any[0] // WEEKS_PER_YEAR, "how": first_any[1], "who": first_any[2], "sig": first_any[3]},
        "first_deliberate_make": {"year": first_make[0] // WEEKS_PER_YEAR, "who": first_make[2], "sig": first_make[3]},
        "makers_in_first_10_years": makers_first10,
        "sigs_of_this_kind": {s: {"events": len(v), "first_year": v[0][0] // WEEKS_PER_YEAR,
                                  "recipe": recipe_of[s].get("recipe"), "first_by": recipe_of[s].get("first_by"),
                                  "first_year_known": (recipe_of[s].get("first_tick") or 0) // WEEKS_PER_YEAR,
                                  "involves_clay": involves_clay[s]} for s, v in by_sig.items()},
        "learning_of_these": [[t // WEEKS_PER_YEAR, a, b, s, h] for t, a, b, s, h in probe.learn][:60],
        "people": {pid: person_card(w, pid) for pid in {first_make[2], first_any[2], *makers_first10} if pid},
        "passive_firings_before_year_115": len(fired_before),
        "passive_firings_total_to_135": len(probe.fired),
        "makes_per_year_105_125": {y: probe.make_counts[y] for y in range(105, 126)},
        "population_by_decade": pops,
    }
    (HERE / "output" / "autopsy_301.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("first_ever_of_kind", "first_deliberate_make", "makers_in_first_10_years",
                                          "sigs_of_this_kind", "passive_firings_before_year_115")}, indent=1, default=str))


if __name__ == "__main__":
    main()
