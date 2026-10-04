"""E5 follow-up (read-only): is a 1000-year technique passed on, or reinvented by each generation?

Replays the last 100 years of a world from its year-900 snapshot with a probe that only reads events. Every
person who comes to hold the technique during those years is counted once, by how they got it: taught, copied by
watching, read from a mark, or invented it themselves in play. The replay is checked against
the original run's population at year 1000.

Usage: python experiments/E5_millennium/provenance.py <seed>   -> output/provenance_<seed>.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))

from acl.config import WEEKS_PER_YEAR  # noqa: E402
from acl.runner import load_snapshot  # noqa: E402

OUT = HERE / "output"
SIG = "(fiber+fiber)#fiber"
BELIEFS = ("fiber@3", "wood@3", "fiber@2")


class Probe:
    def __init__(self, world):
        self.holders = {p.id for p in world.living() if SIG in p.recipes}
        self.start_holders = len(self.holders)
        self.how = {}
        self.told = {b: 0 for b in BELIEFS}

    def __call__(self, world, events):
        for e in events:
            k = e["k"]
            if k == "learn" and e.get("thing") == SIG and e.get("a") not in self.holders:
                self.how[e["how"]] = self.how.get(e["how"], 0) + 1
                self.holders.add(e["a"])
            elif k in ("play", "make") and e.get("thing") == SIG and e.get("a") not in self.holders:
                self.how["invented it in play"] = self.how.get("invented it in play", 0) + 1
                self.holders.add(e["a"])
            elif k == "learn" and e.get("belief") in self.told:
                self.told[e["belief"]] += 1
        # people who lose the recipe (forgetting) can gain it again later
        living_holders = {p.id for p in world.living() if SIG in p.recipes}
        self.holders &= living_holders | {e.get("a") for e in events}


def main():
    seed = int(sys.argv[1])
    w, h = load_snapshot(OUT / f"seed_{seed}_year900.json.gz")
    probe = Probe(w)
    beliefs_start = {b: sum(1 for p in w.living() if p.beliefs.get(b, 0) >= 0.15) for b in BELIEFS}
    w.observers.append(probe)
    for _ in range(100 * WEEKS_PER_YEAR):
        w.step()
    orig = json.loads((OUT / f"seed_{seed}.json").read_text(encoding="utf-8"))
    end_holders = sum(1 for p in w.living() if SIG in p.recipes)
    out = {"seed": seed, "technique": SIG, "holders_year900": probe.start_holders, "holders_year1000": end_holders,
           "gained_by": probe.how, "alive_year1000_replay": len(w.living()),
           "alive_year1000_original": orig["divergence"][-1]["population"] if orig["divergence"][-1]["year"] == 1000 else None,
           "beliefs": {b: {"holders_year900": beliefs_start[b],
                           "holders_year1000": sum(1 for p in w.living() if p.beliefs.get(b, 0) >= 0.15),
                           "times_told": probe.told[b]} for b in BELIEFS}}
    (OUT / f"provenance_{seed}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out))


if __name__ == "__main__":
    main()
