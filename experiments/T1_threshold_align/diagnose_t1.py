"""T1 — why the manipulation check failed (exploratory, read-only; written after the frozen analysis, labelled as such).
Replays T1 worlds (deterministic) with an observer that, for partners exactly 3 tiles apart, records whether a "join"
option was among their four top-scored options, whether it was chosen, what was chosen instead, and where the partner
who moved ended up.

  python experiments/T1_threshold_align/diagnose_t1.py      -> diagnose.md
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_t1 as R  # noqa: E402

SEEDS, YEARS = (501, 601, 811, 1101), 20


class Probe:
    def __init__(self):
        self.n = Counter()
        self.prev = {}

    def __call__(self, world, events):
        from acl.util import distance
        c, tick = world.cfg, world.tick
        dist = lambda a, b: distance(a, b, c.width, c.height)
        for w in world.living():
            if w.sex != "F" or not (c.fertile_from <= w.years(tick) < c.fertile_until) or not w.partner:
                continue
            m = world.people[w.partner]
            if not m.alive or w.id not in self.prev or m.id not in self.prev:
                continue
            d0 = dist(self.prev[w.id], self.prev[m.id])        # distance when they chose this week's actions
            if d0 != 3:
                continue
            self.n["pairs_at_3"] += 1
            d1 = dist(w.loc, m.loc)
            self.n[f"after|{'together' if d1 <= 2 else '3' if d1 == 3 else 'further'}"] += 1
            for p in (w, m):
                cons = p.considered or []
                self.n["pw"] += 1
                self.n["join_top4"] += any(o[0] == "join" for o in cons)
                ch = next((o[0] for o in cons if o[3]), "none")
                self.n[f"chosen|{ch}"] += 1
        self.prev = {p.id: p.loc for p in world.living()}


def main():
    R.setup("t1")
    total = Counter()
    for seed in SEEDS:
        w = R.make_world(seed, **R.ON)
        pr = Probe()
        w.observers.append(pr)
        for _ in range(YEARS * 52):
            w.step()
        total.update(pr.n)
    n = total
    L = ["# T1 diagnosis (exploratory, read-only; seeds " + ", ".join(map(str, SEEDS)) + f"; first {YEARS} years)\n",
         f"Couple-weeks starting at exactly 3 tiles: {n['pairs_at_3']:,}. A week later: together (≤ 2) "
         f"{n['after|together'] / n['pairs_at_3']:.1%}, still 3 {n['after|3'] / n['pairs_at_3']:.1%}, further "
         f"{n['after|further'] / n['pairs_at_3']:.1%}.\n",
         f"Partner-weeks at 3 tiles: {n['pw']:,}; a \"join\" option among the four top-scored: "
         f"{n['join_top4'] / n['pw']:.1%}.\n", "| action chosen | share |", "|---|---|"]
    for k, v in sorted(((k.split("|")[1], v) for k, v in n.items() if k.startswith("chosen|")), key=lambda x: -x[1]):
        L.append(f"| {k} | {v / n['pw']:.1%} |")
    text = "\n".join(L) + "\n"
    (HERE / "diagnose.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
