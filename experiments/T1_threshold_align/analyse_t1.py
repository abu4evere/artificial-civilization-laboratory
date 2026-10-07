"""T1 analysis in the frozen order (preregistration.md, `T1-frozen`). Written and smoke-tested before any T1 data.

Operational details written with this file, before data:
- The manipulation check compares T1 with C1 on C1's 32 seeds (501-516, 1101-1116), years 0-39: the share of apart
  couple-weeks at exactly 3 tiles must be at most half of C1's pooled share.
- "Couples apart" per couple is computed as in `C1_couples_apart/reconcile.py`: apart ÷ (woman-weeks with a living
  partner who is not pregnant), all years.

  python experiments/T1_threshold_align/analyse_t1.py
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "F1_baseline_fragility"))
import analyse_f1 as A  # noqa: E402

SEEDS = tuple(range(501, 517)) + tuple(range(601, 617)) + tuple(range(811, 819)) + tuple(range(1101, 1125))
C1_SEEDS = tuple(range(501, 517)) + tuple(range(1101, 1117))


def load(out, seeds):
    R = {}
    for s in seeds:
        r = json.loads((out / f"seed_{s}.json").read_text(encoding="utf-8"))
        r["Y"] = {int(k): v for k, v in r["years"].items()}
        r["extinct"] = not (len(r["pops"]) == 12 and r["pops"][-1] > 0)
        r["E"] = (r["final_tick"] - 1) // 52 if r["extinct"] else None
        R[s] = r
    return R


def per_couple_apart(R):
    n = Counter()
    for r in R.values():
        for v in r["Y"].values():
            n.update({k: x for k, x in v.items() if k == "woman_weeks" or k.startswith("r_")})
    checked = n["woman_weeks"] - n["r_no_partner"] - n["r_partner_dead"] - n["r_pregnant"]
    return n["r_apart"] / checked if checked else None


def main(out=HERE / "output", f1out=EXP / "F1_baseline_fragility" / "output", c1out=EXP / "C1_couples_apart" / "output",
         seeds=SEEDS, c1_seeds=C1_SEEDS, write=True):
    T = load(out, seeds)
    C = load(f1out, seeds)
    L = []
    w = L.append
    w("# T1 — Align the two thresholds: results\n")
    w("Frozen as `T1-frozen`. Copy of the control code with the partner pull beginning beyond 2 tiles; F1's 64 seeds, "
      "paired with F1's replays. A2-full people, 120 years.\n")
    w("## Validity\n")
    ok_zero = "All: PASS" in (out / "zero.txt").read_text(encoding="utf-8")
    ok_code = all(r["code_hash"] == r["code_hash_after"] for r in T.values())
    for label, ok in (("Zero checks (setting off reproduces the control world; on, it differs)", ok_zero),
                      ("Code unchanged during runs", ok_code)):
        w(f"- {label}: **{'yes' if ok else 'NO'}**")
    valid = ok_zero and ok_code
    w(f"\n**{'Valid' if valid else 'NOT VALID: recorded, not interpreted'}.**\n")

    w("## Baseline (rule 14)\n")
    dc = sum(r["extinct"] for r in C.values())
    w(f"Control (F1) on these seeds: {dc} of {len(seeds)} died out.\n")

    w("## Manipulation check\n")
    c1n, t1n = Counter(), Counter()
    for s in c1_seeds:
        c1n.update(json.loads((c1out / f"seed_{s}.json").read_text(encoding="utf-8"))["n"])
        if s in T:
            t1n.update(T[s]["c1"]["n"])
    c3 = c1n["dist|3"] / c1n["apart"] if c1n["apart"] else None
    t3 = t1n["dist|3"] / t1n["apart"] if t1n["apart"] else None
    manip = c3 is not None and t3 is not None and t3 <= c3 / 2
    w(f"- Apart couple-weeks at exactly 3 tiles (years 0–39, seeds {c1_seeds[0]}–{c1_seeds[-1]}): C1 {A.fmt(c3)}, "
      f"T1 {A.fmt(t3)} (must be at most half): **{'yes' if manip else 'NO'}**")
    ca = c1n["apart"] / c1n["couple_weeks"] if c1n["couple_weeks"] else None
    ta = t1n["apart"] / t1n["couple_weeks"] if t1n["couple_weeks"] else None
    w(f"- Beside it: couples apart, share of couple-weeks (same window): C1 {A.fmt(ca)}, T1 {A.fmt(ta)}.\n")

    w("## Extinction (the frozen outcome)\n")
    dt = sum(r["extinct"] for r in T.values())
    saved = [s for s in seeds if C[s]["extinct"] and not T[s]["extinct"]]
    lost = [s for s in seeds if not C[s]["extinct"] and T[s]["extinct"]]
    w("| | control (F1) | T1 |")
    w("|---|---|---|")
    w(f"| worlds died out | {dc} of {len(seeds)} | **{dt} of {len(seeds)}** |")
    for t in (40, 80, 119):
        w(f"| median population, year {t} | {statistics.median(C[s]['Y'].get(t, {}).get('n', 0) for s in seeds):.0f} | "
          f"{statistics.median(T[s]['Y'].get(t, {}).get('n', 0) for s in seeds):.0f} |")
    rc = A.rates(None, [(r, 0, (r["E"] + 1) if r["extinct"] else 120) for r in C.values()])
    rt = A.rates(None, [(r, 0, (r["E"] + 1) if r["extinct"] else 120) for r in T.values()])
    for k in ("births_per_woman_year", "child_deaths_per_birth", "starving_share", "block_no_partner", "block_apart"):
        w(f"| {k} | {A.fmt(rc[k])} | {A.fmt(rt[k])} |")
    w(f"| couples apart, per partnered non-pregnant woman-week | {A.fmt(per_couple_apart(C))} | {A.fmt(per_couple_apart(T))} |")
    w(f"\nPaired: saved {len(saved)} {saved}; lost {len(lost)} {lost}.\n")
    if dt <= 15:
        verdict = "**Large effect:** the threshold gap mattered a great deal."
    elif dt <= 20:
        verdict = "**Modest effect.**"
    else:
        verdict = "**No effect, or worse:** the gap was not a driver of extinction."
    w(f"Frozen bands (≤ 15 large, 16–20 modest, ≥ 21 none or worse): {dt} of {len(seeds)}: {verdict}")
    if not manip:
        w("\n**The manipulation check failed: under the frozen rule the outcome is not read.**")
    if not valid:
        w("\n**Not valid: recorded, not interpreted.**")
    text = "\n".join(L) + "\n"
    if write:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
