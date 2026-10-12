"""WS1: exact values behind every statistical claim (added 12 October 2026, after the frozen analysis, on a reviewer's
request; NOT pre-registered, and changes no reading). Uses the frozen analysis's own functions and method: exact
two-sided sign test on worlds that differ (analyse_mc1l.sign_test); effect = reference arm's extinction share minus the
other's, paired by seed; 95% percentile bootstrap over seeds, 10,000 resamples, random.Random(2026). Adds what the frozen
script did not print: unrounded p-values, and the sham's effect and interval.

  python experiments/WS1_world_size/stats_trace.py
"""
import random
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "MC1L_moving_camp_large"))
from analyse_mc1l import sign_test  # noqa: E402
import json  # noqa: E402

SEEDS = range(3001, 3257)


def extinct(arm, s):
    p = json.loads((HERE / "output" / f"{arm}_seed_{s}.json").read_text(encoding="utf-8"))["pops"]
    return not (len(p) == 12 and p[-1] > 0)


E = {a: {s: extinct(a, s) for s in SEEDS} for a in ("c", "l", "lp", "p", "s")}
print("| comparison | died out (ref vs other) | saved / lost | exact sign test p | effect (ref - other) | 95% interval |")
print("|---|---|---|---|---|---|")
for name, ref, x in (("Q1 L vs C", "c", "l"), ("Q2 LP vs L", "l", "lp"), ("Q3 P vs C", "c", "p"), ("sham S vs C", "c", "s")):
    saved = sum(1 for s in SEEDS if E[ref][s] and not E[x][s])
    lost = sum(1 for s in SEEDS if not E[ref][s] and E[x][s])
    d = [int(E[ref][s]) - int(E[x][s]) for s in SEEDS]
    rng = random.Random(2026)
    boots = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(10000))
    print(f"| {name} | {sum(E[ref].values())} vs {sum(E[x].values())} | {saved} / {lost} | {sign_test(saved, lost):.3g} "
          f"| {sum(d) / len(d):+.3f} | [{boots[249]:+.3f}, {boots[9749]:+.3f}] |")
