"""Population genetics in the finished E1/E2/E4 worlds. Read-only.

Temperament is already inherited (person.GENES; biology.give_birth: the parents' average plus random drift).
This asks what has happened to it, in 24 worlds under each code:
- does diversity within a world shrink (drift)?
- do islands become different kinds of people (divergence)?
- which tendencies does the world favour (selection: who survives to adulthood, who has children)?

Writes genetics.md.
"""
from __future__ import annotations

import math
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))

from acl.config import Config  # noqa: E402
from acl.person import GENES  # noqa: E402
from acl.runner import load_snapshot  # noqa: E402
from acl.world import World  # noqa: E402

WPY = 52
SRC = {("e1", "old"): ROOT / "experiments" / "E1" / "output", ("e2", "old"): ROOT / "experiments" / "E2" / "output",
       ("e1", "new"): HERE / "output" / "e1", ("e2", "new"): HERE / "output" / "e2"}
SEEDS = list(range(101, 109)) + list(range(201, 217))


def var(xs):
    return statistics.pvariance(xs) if len(xs) > 1 else 0.0


def fst(world, people):
    """Share of each trait's variation that lies between islands (0 = islands alike, 1 = wholly different)."""
    island = {}
    for i, comp in enumerate(world.landmasses()):
        for xy in comp:
            island[xy] = i
    groups = {}
    for p in people:
        groups.setdefault(island.get(p.loc, -1), []).append(p)
    groups = {k: v for k, v in groups.items() if len(v) >= 5 and k != -1}
    if len(groups) < 2:
        return None
    out = {}
    n = sum(len(v) for v in groups.values())
    for g in GENES:
        allv = [p.genes[g] for v in groups.values() for p in v]
        tot = var(allv)
        mean = sum(allv) / n
        between = sum(len(v) * (sum(p.genes[g] for p in v) / len(v) - mean) ** 2 for v in groups.values()) / n
        out[g] = between / tot if tot else 0.0
    return out


def slope(xs, ys):
    """Standardised association between a trait and an outcome (a correlation)."""
    n = len(xs)
    if n < 10:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy) if sx and sy else None


def main():
    L = ["# Population genetics in the finished worlds (read-only)", ""]
    w = L.append
    w("Temperament has been inherited since the first version: each child gets the average of the parents' 8 traits "
      "plus random drift (sd 0.08). Nothing else is inherited. This looks at what 200 years did to it, in 24 worlds "
      "under each code.")
    w("")
    for code in ("e1", "e2"):
        start_var, end_var = [], []
        fst_vals = {g: [] for g in GENES}
        worlds_fst = 0
        surv = {g: ([], []) for g in GENES}
        kids = {g: ([], []) for g in GENES}
        shift = {g: [] for g in GENES}
        for s in SEEDS:
            d = SRC[(code, "old" if s < 200 else "new")]
            w_end, _ = load_snapshot(d / f"seed_{s}_end.json.gz")
            founders = [p for p in World(Config(seed=s)).people.values()]
            living = w_end.living()
            for g in GENES:
                if len(living) >= 5:
                    start_var.append(var([p.genes[g] for p in founders]))
                    end_var.append(var([p.genes[g] for p in living]))
                    shift[g].append(sum(p.genes[g] for p in living) / len(living)
                                    - sum(p.genes[g] for p in founders) / len(founders))
            f = fst(w_end, living)
            if f:
                worlds_fst += 1
                for g in GENES:
                    fst_vals[g].append(f[g])
            # selection: everyone born in the world early enough to have had a full life
            for p in w_end.people.values():
                if p.generation == 0 or p.birth > 150 * WPY:
                    continue
                adult = p.death_tick is None or p.death_tick - p.birth >= 16 * WPY
                for g in GENES:
                    surv[g][0].append(p.genes[g])
                    surv[g][1].append(1.0 if adult else 0.0)
                    if adult:
                        kids[g][0].append(p.genes[g])
                        kids[g][1].append(len(p.children))
        w(f"## {code.upper()} code")
        w("")
        w(f"- **Diversity within a world:** mean trait variance among the founders {statistics.mean(start_var):.4f}; "
          f"among the living at the end {statistics.mean(end_var):.4f} "
          f"({100 * (statistics.mean(end_var) / statistics.mean(start_var) - 1):+.0f}%).")
        w(f"- **Islands becoming different:** in {worlds_fst} worlds with at least two islands holding 5+ people at the "
          "end, the share of each trait's variation that lies between islands (0 = alike, 1 = wholly different):")
        w("")
        w("| trait | between-island share (mean over worlds) | mean change from the founders | survival to 16 (correlation) | children, if adult (correlation) |")
        w("|---|---|---|---|---|")
        for g in GENES:
            fv = statistics.mean(fst_vals[g]) if fst_vals[g] else float("nan")
            sh = statistics.mean(shift[g]) if shift[g] else float("nan")
            sv = slope(*surv[g])
            kv = slope(*kids[g])
            fmt = lambda v: "–" if v is None else f"{v:+.3f}"  # noqa: E731
            w(f"| {g} | {fv:.3f} | {sh:+.3f} | {fmt(sv)} | {fmt(kv)} |")
        w("")
    w("Reading the correlations: positive means people with more of the trait were more likely to reach 16, or had "
      "more children. With thousands of people, values near ±0.05 are small but real; the sign is the point.")
    (HERE / "genetics.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("wrote", HERE / "genetics.md")


if __name__ == "__main__":
    main()
