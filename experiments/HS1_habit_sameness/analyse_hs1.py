"""HS1 analysis in the frozen order (questions.md, `HS1-frozen`). Written and smoke-tested before any data.

  python experiments/HS1_habit_sameness/analyse_hs1.py           # writes results.md
  python experiments/HS1_habit_sameness/analyse_hs1.py --smoke   # throwaway smoke outputs; writes nothing
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from pathlib import Path

import numpy as np
from scipy.stats import wilcoxon

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_hs1 import ARMS, OUT, SEEDS, YEARS  # noqa: E402


def corr(a, b):
    if a is None or b is None:
        return None
    a, b = np.asarray(a), np.asarray(b)
    if a.std() == 0 or b.std() == 0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def boot(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None, None, None
    rng = random.Random(2026)
    b = sorted(statistics.median(rng.choice(xs) for _ in xs) for _ in range(10000))
    return statistics.median(xs), b[249], b[9749]


def per_world(D, seeds):
    """For each world: mean over its children of r_par, r_same, r_other. Other-world strangers come from the next seed's
    pool at the child's birth year (or the nearest earlier year with one), drawn by one Random(2026) in seed order."""
    rng = random.Random(2026)
    out = {}
    for i, s in enumerate(seeds):
        nxt = D[seeds[(i + 1) % len(seeds)]]
        pool = {int(k): v for k, v in nxt["pool"].items() if v}
        rp, rs, ro = [], [], []
        for by, child, par, same in D[s]["children"]:
            years = [y for y in pool if y <= by]
            other = rng.choice(pool[max(years)]) if years else None
            rp.append(corr(child, par))
            rs.append(corr(child, same))
            ro.append(corr(child, other))
        m = lambda xs: statistics.fmean([x for x in xs if x is not None]) if any(x is not None for x in xs) else None  # noqa: E731
        out[s] = {"n": len(D[s]["children"]), "r_par": m(rp), "r_same": m(rs), "r_other": m(ro),
                  "alive_end": D[s]["alive_end"], "survived": D[s]["final_tick"] >= D[s]["years"] * 52}
    return out


def main(out=OUT, seeds=SEEDS, write=True):
    L = []
    w = L.append
    w("# HS1 — Why are everyone's habits alike? Same world, or same nature? Results\n")
    w(f"Frozen as `HS1-frozen`. `code_tc1`, control world; arms N (no copying, primary) and W (today); seeds "
      f"{seeds[0]}–{seeds[-1]} ({len(seeds)}); {YEARS} years.\n")
    z = out / "zero.txt"
    zero_ok = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    present = all((out / f"{a}_seed_{s}.json").exists() for a in ARMS for s in seeds)
    D = {a: {s: json.loads((out / f"{a}_seed_{s}.json").read_text(encoding="utf-8")) for s in seeds} for a in ARMS} if present else {}
    W = {a: per_world(D[a], seeds) for a in D}
    usable = {a: sum(1 for v in W[a].values() if v["r_same"] is not None and v["r_other"] is not None) for a in W}
    enough = present and all(usable[a] >= min(16, len(seeds)) for a in W)
    valid = zero_ok and present and enough
    w("## Validity\n")
    w(f"- Zero check (observer leaves the world unchanged, both arms): **{'yes' if zero_ok else 'no'}**")
    w(f"- All {len(ARMS) * len(seeds)} replays present: **{'yes' if present else 'no'}**")
    w(f"- Worlds with children reaching 20 and an other-world stranger: "
      + (", ".join(f"{a.upper()} {usable[a]}" for a in W) if W else "–") + f" (need {min(16, len(seeds))} each)")
    w(f"\n**{'Valid.' if valid else 'NOT VALID: no outcome is shown.'}**\n")
    if not valid:
        text = "\n".join(L) + "\n"
        if write:
            (HERE / "results.md").write_text(text, encoding="utf-8")
        print(text)
        return
    w("## Population first (rule 18)\n")
    w("| arm | children reaching 20 (all worlds) | per world, median | worlds alive at the end |")
    w("|---|---|---|---|")
    for a in ("n", "w"):
        ns = [v["n"] for v in W[a].values()]
        w(f"| {a.upper()} | {sum(ns)} | {statistics.median(ns):.0f} | {sum(v['survived'] for v in W[a].values())} of {len(seeds)} |")
    w("\n## Sameness: a child at 20 against parents, a stranger of the same world, and a stranger of another world\n")
    w("| arm | r with parents | r with same-world stranger | r with other-world stranger | nature share (r_other ÷ r_same) | world share | Wilcoxon r_same vs r_other |")
    w("|---|---|---|---|---|---|---|")
    reading = None
    for a in ("n", "w"):
        V = [v for v in W[a].values() if v["r_same"] is not None and v["r_other"] is not None]
        ns = [v["r_other"] / v["r_same"] for v in V if v["r_same"]]
        nat = boot(ns)
        ws = boot([1 - x for x in ns])
        d = [v["r_same"] - v["r_other"] for v in V]
        p = wilcoxon(d).pvalue if any(d) else 1.0
        f = lambda t: "–" if t[0] is None else f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"  # noqa: E731
        w(f"| {a.upper()} | {f(boot([v['r_par'] for v in V]))} | {f(boot([v['r_same'] for v in V]))} | "
          f"{f(boot([v['r_other'] for v in V]))} | {f(nat)} | {f(ws)} | {p:.3g} |")
        if a == "n":
            med_same = statistics.median(v["r_same"] for v in V)
            med_other = statistics.median(v["r_other"] for v in V)
            if med_other >= 0.9 * med_same and nat[1] >= 0.9:
                reading = "Mostly nature: a stranger from another world is nearly as like a child as a stranger from their own."
            elif med_same > med_other and p < 0.05 and nat[2] < 0.9:
                reading = "The world adds sameness: strangers from the child's own world are measurably more alike."
            else:
                reading = "Unresolved at this sample."
    w(f"\n**Frozen reading (N, no copying): {reading}**\n")
    w("Medians over worlds of per-world means, with 95% bootstrap intervals (10,000 resamples, `random.Random(2026)`). "
      "W is described beside N; no reading is made for W.")
    text = "\n".join(L) + "\n"
    if write:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        (HERE / "output_smoke" / "zero.txt").write_text((OUT / "zero.txt").read_text(encoding="utf-8"), encoding="utf-8")
        main(out=HERE / "output_smoke", seeds=(9601, 9602), write=False)
    else:
        main()
