"""S1 analysis in the frozen order (preregistration.md, `S1-frozen`). Written and smoke-tested before any main-run data.

Operational details (written before data):
- Extinct: the world does not reach year 120 with someone alive (12 decade marks, the last above 0), as in every study.
- Growth multiple: population at the year-119 snapshot ÷ founders; 0 for extinct worlds.
- Each primary comparison is paired by seed; effect = reference arm's extinction share minus the other arm's (positive
  = fewer extinctions); 95% percentile bootstrap over seeds, 10,000 resamples, random.Random(2026); half of F2's effect
  = (1 − F2's ÷ F1's extinctions on F1's 64 seeds) ÷ 2 × the reference arm's extinction share.
- Holm adjustment over the three primary sign-test p-values. Growth multiple: paired Wilcoxon signed-rank test
  (scipy.stats.wilcoxon, two-sided, zero differences dropped), secondary.

  python experiments/S1_world_size/analyse_s1.py
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "F1_baseline_fragility"))
sys.path.insert(0, str(EXP / "HF4_hunger_ledger"))
sys.path.insert(0, str(EXP / "MC1L_moving_camp_large"))
import analyse_f1 as A  # noqa: E402
from analyse_hf4 import median  # noqa: E402
from analyse_mc1l import F1_SEEDS, ext_file, load, sign_test  # noqa: E402

FOUNDERS = {"c": 20, "l": 20, "lp": 80, "p": 80, "s": 20}
NAMES = {"c": "C (40×40, 20)", "l": "L (80×80, 20)", "lp": "LP (80×80, 80)", "p": "P (40×40, 80)", "s": "S sham"}
PRIMARY = [("Does a larger world change survival?", "c", "l"),
           ("Does adding founders change survival, given the larger world?", "l", "lp"),
           ("Does adding founders change survival without more land?", "c", "p")]


def growth(r, arm):
    return 0.0 if r["extinct"] else r["Y"].get(119, {}).get("n", 0) / FOUNDERS[arm]


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, run = [0.0] * len(ps), 0.0
    for k, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - k) * ps[i]))
        adj[i] = run
    return adj


def main(out=HERE / "output", seeds=None, write=True, f1_ref=True):
    if seeds is None:
        n = json.loads((out / "pilot.json").read_text(encoding="utf-8"))["use_seeds"]
        seeds = tuple(range(3001, 3001 + n))
    D = {a: load(out, seeds, a) for a in NAMES}
    L = []
    w = L.append
    w("# S1 — World size: results\n")
    w(f"Frozen as `S1-frozen`. {len(seeds)} new seeds ({seeds[0]}–{seeds[-1]}), 120 years; arms: "
      + ", ".join(NAMES.values()) + ". Settings only, in `code_p2` with every setting off.\n")
    w("## Validity\n")
    ok_zero = "All: PASS" in (out / "zero.txt").read_text(encoding="utf-8")
    fps = {r["code_hash"] for R in D.values() for r in R.values()}
    ok_code = len(fps) == 1 and all(r["code_hash"] == r["code_hash_after"] for R in D.values() for r in R.values())
    for label, ok in (("Zero checks (40×40 and 80×80)", ok_zero), ("Code unchanged", ok_code)):
        w(f"- {label}: **{'yes' if ok else 'NO'}**")
    valid = ok_zero and ok_code
    w(f"\n**{'Valid' if valid else 'NOT VALID: recorded, not interpreted'}.**\n")

    ext = {a: sum(r["extinct"] for r in R.values()) for a, R in D.items()}
    w(f"## Baseline (rule 14)\n\nC died out in {ext['c']} of {len(seeds)} worlds ({ext['c'] / len(seeds):.1%}).\n")

    w("## Manipulation checks (week one, and during the run)\n")
    w("| | " + " | ".join(NAMES.values()) + " |")
    w("|---|" + "---|" * len(NAMES))
    for k, lab in (("land_per_founder", "land tiles per founder"), ("band_gap", "distance between founding bands"),
                   ("eligible_in_sight_per_founder", "possible partners in sight per founder")):
        w(f"| {lab} (week one, median) | " + " | ".join(
            f"{statistics.median(r['week1'][k] for r in R.values()):.2f}" for R in D.values()) + " |")
    enc = {a: Counter() for a in D}
    for a, R in D.items():
        for r in R.values():
            enc[a].update(r["enc"])
    w("| seeker-weeks with an eligible single in sight (whole run) | " + " | ".join(
        A.fmt(enc[a]["seeker_weeks_eligible_in_sight"] / enc[a]["seeker_weeks"]) if enc[a]["seeker_weeks"] else "–"
        for a in D) + " |")

    w("\n## Extinction and growth (the frozen outcomes)\n")
    w("| | " + " | ".join(NAMES.values()) + " |")
    w("|---|" + "---|" * len(NAMES))
    w(f"| worlds died out (of {len(seeds)}) | " + " | ".join(f"**{ext[a]}**" for a in D) + " |")
    w("| growth multiple (population at year 119 ÷ founders), median [IQR] | " + " | ".join(
        (lambda v: f"{statistics.median(v):.2f} [{statistics.quantiles(v, n=4)[0]:.2f}, {statistics.quantiles(v, n=4)[2]:.2f}]")(
            [growth(r, a) for r in R.values()]) for a, R in D.items()) + " |")
    w("| median population, year 119 | " + " | ".join(
        f"{statistics.median(r['Y'].get(119, {}).get('n', 0) for r in R.values()):.0f}" for R in D.values()) + " |")
    rates = {a: A.rates(None, [(r, 0, (r["E"] + 1) if r["extinct"] else 120) for r in R.values()]) for a, R in D.items()}
    for k in ("births_per_woman_year", "child_deaths_per_birth", "starving_share", "block_no_partner"):
        w(f"| {k} | " + " | ".join(A.fmt(rates[a][k]) for a in D) + " |")

    if f1_ref:
        f1 = sum(ext_file(EXP / "F1_baseline_fragility" / "output" / f"seed_{s}.json") for s in F1_SEEDS)
        f2 = sum(ext_file(EXP / "F2_perfect_search" / "output" / f"seed_{s}.json") for s in F1_SEEDS)
        rel = 1 - f2 / f1
    else:
        rel = 0.68
    rows, ps = [], []
    for q, ref, x in PRIMARY:
        saved = sum(1 for s in seeds if D[ref][s]["extinct"] and not D[x][s]["extinct"])
        lost = sum(1 for s in seeds if not D[ref][s]["extinct"] and D[x][s]["extinct"])
        p = sign_test(saved, lost)
        d = [int(D[ref][s]["extinct"]) - int(D[x][s]["extinct"]) for s in seeds]
        rng = random.Random(2026)
        boots = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(10000))
        lo, hi = boots[249], boots[9749]
        half = rel / 2 * ext[ref] / len(seeds)
        try:
            from scipy.stats import wilcoxon
            gd = [growth(D[x][s], x) - growth(D[ref][s], ref) for s in seeds]
            pw = wilcoxon([v for v in gd if v != 0]).pvalue if any(gd) else 1.0
        except ValueError:
            pw = 1.0
        rows.append((q, ref, x, saved, lost, p, sum(d) / len(d), lo, hi, half, pw))
        ps.append(p)
    adj = holm(ps)
    w("\n## The three primary questions\n")
    for (q, ref, x, saved, lost, p, eff, lo, hi, half, pw), pa in zip(rows, adj):
        if p < 0.05 and eff > 0:
            v = "**the change improves survival**; its size is the effect estimate"
        elif p < 0.05 and eff < 0:
            v = "**the change harms survival** (to be examined read-only)"
        elif max(abs(lo), abs(hi)) < half:
            v = "**no meaningful effect** (the interval excludes half of F2's effect)"
        else:
            v = "**unresolved** at this sample"
        if p < 0.05 and pa >= 0.05:
            v += "; **does not survive the Holm adjustment**"
        w(f"### {q}\n\n{NAMES[x]} against {NAMES[ref]}: died out {ext[x]} vs {ext[ref]}; saved / lost {saved} / {lost}; "
          f"exact sign test **p = {p:.3f}** (Holm-adjusted {pa:.3f}). Effect ({ref.upper()} − {x.upper()} extinction share) "
          f"{eff:+.3f}, 95% interval [{lo:+.3f}, {hi:+.3f}]; half of F2's effect {half:.3f}. Growth multiple, paired "
          f"Wilcoxon p = {pw:.3g}.\n\nFrozen rule: {v}.\n")
    s_saved = sum(1 for s in seeds if D["c"][s]["extinct"] and not D["s"][s]["extinct"])
    s_lost = sum(1 for s in seeds if not D["c"][s]["extinct"] and D["s"][s]["extinct"])
    sp = sign_test(s_saved, s_lost)
    w(f"Sham against C: died out {ext['s']} vs {ext['c']}; {s_saved} / {s_lost}; p = {sp:.3f}"
      + (" — **caveat (frozen): the sham reached p < 0.05; the noise is larger than the test assumes.**" if sp < 0.05 else "."))
    w(f"\n**Descriptive only:** LP against C (land and people together): died out {ext['lp']} vs {ext['c']}; "
      f"LP against P (land, given 80 founders): {ext['lp']} vs {ext['p']}.")
    if not valid:
        w("\n**Not valid: recorded, not interpreted.**")
    text = "\n".join(L) + "\n"
    if write:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
