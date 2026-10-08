"""MC1-L analysis in the frozen order (preregistration.md, `MC1L-frozen`). Written and smoke-tested before any data.

Operational details (written before data):
- Effect = C's extinction share minus M's (positive = fewer extinctions under M), paired by seed.
- 95% interval: percentile bootstrap over seeds, 10,000 resamples, random.Random(2026).
- Half of F2's effect, in absolute terms on these seeds: (1 − F2's extinctions ÷ F1's on F1's 64 seeds) ÷ 2 × C's
  extinction share here.

  python experiments/MC1L_moving_camp_large/analyse_mc1l.py
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from collections import Counter
from math import comb
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "F1_baseline_fragility"))
sys.path.insert(0, str(EXP / "HF4_hunger_ledger"))
import analyse_f1 as A  # noqa: E402
from analyse_hf4 import median  # noqa: E402

SEEDS = tuple(range(2001, 2257))
F1_SEEDS = tuple(range(501, 517)) + tuple(range(601, 617)) + tuple(range(811, 819)) + tuple(range(1101, 1125))


def load(out, seeds, arm):
    R = {}
    for s in seeds:
        r = json.loads((out / f"{arm}_seed_{s}.json").read_text(encoding="utf-8"))
        r["Y"] = {int(k): v for k, v in r["years"].items()}
        r["extinct"] = not (len(r["pops"]) == 12 and r["pops"][-1] > 0)
        r["E"] = (r["final_tick"] - 1) // 52 if r["extinct"] else None
        R[s] = r
    return R


def ext_file(path):
    p = json.loads(path.read_text(encoding="utf-8"))["pops"]
    return not (len(p) == 12 and p[-1] > 0)


def per_couple_apart(R):
    n = Counter()
    for r in R.values():
        for v in r["Y"].values():
            n.update({k: x for k, x in v.items() if k == "woman_weeks" or k.startswith("r_")})
    checked = n["woman_weeks"] - n["r_no_partner"] - n["r_partner_dead"] - n["r_pregnant"]
    return n["r_apart"] / checked if checked else None


def sign_test(saved, lost):
    n = saved + lost
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(comb(n, i) for i in range(min(saved, lost) + 1)) / 2 ** n)


def main(out=HERE / "output", seeds=SEEDS, write=True):
    C, M, S = (load(out, seeds, a) for a in ("c", "m", "s"))
    L = []
    w = L.append
    w("# MC1-L — The moving camp re-tested at proper power: results\n")
    w(f"Frozen as `MC1L-frozen`. MC1's code and setting unchanged; {len(seeds)} new seeds ({seeds[0]}–{seeds[-1]}), "
      "120 years; arms C (settings off), M (moving camp), S (sham).\n")
    w("## Validity\n")
    ok_checks = "All: PASS" in (out / "checks.txt").read_text(encoding="utf-8")
    ok_code = all(r["code_hash"] == r["code_hash_after"] for R in (C, M, S) for r in R.values())
    for label, ok in (("Fingerprint equals MC1's; zero check on two new seeds", ok_checks), ("Code unchanged", ok_code)):
        w(f"- {label}: **{'yes' if ok else 'NO'}**")
    valid = ok_checks and ok_code
    w(f"\n**{'Valid' if valid else 'NOT VALID: recorded, not interpreted'}.**\n")
    dc = sum(r["extinct"] for r in C.values())
    mc = dc / len(seeds)
    w(f"## Baseline (rule 14)\n\nControl on these seeds: {dc} of {len(seeds)} died out ({mc:.1%}).\n")

    w("## Manipulation check\n")
    ac, am, as_ = per_couple_apart(C), per_couple_apart(M), per_couple_apart(S)
    manip = ac is not None and am is not None and am <= ac / 2
    w(f"- Couples apart, per partnered non-pregnant woman-week: C {A.fmt(ac)}, M {A.fmt(am)} (≤ half of C's), "
      f"S {A.fmt(as_)}: **{'yes' if manip else 'NO'}**\n")

    w("## Extinction (the frozen outcome)\n")
    rows = {}
    for name, X in (("M", M), ("S", S)):
        saved = [s for s in seeds if C[s]["extinct"] and not X[s]["extinct"]]
        lost = [s for s in seeds if not C[s]["extinct"] and X[s]["extinct"]]
        rows[name] = (sum(X[s]["extinct"] for s in seeds), len(saved), len(lost), sign_test(len(saved), len(lost)))
    w("| | C | M moving camp | S sham |")
    w("|---|---|---|---|")
    w(f"| worlds died out (of {len(seeds)}) | {dc} | **{rows['M'][0]}** | {rows['S'][0]} |")
    w(f"| paired against C: saved / lost | – | {rows['M'][1]} / {rows['M'][2]} | {rows['S'][1]} / {rows['S'][2]} |")
    w(f"| exact two-sided sign test | – | **p = {rows['M'][3]:.3f}** | p = {rows['S'][3]:.3f} |")
    rates = [A.rates(None, [(r, 0, (r["E"] + 1) if r["extinct"] else 120) for r in R.values()]) for R in (C, M, S)]
    for k in ("births_per_woman_year", "child_deaths_per_birth", "starving_share", "block_no_partner"):
        w(f"| {k} | " + " | ".join(A.fmt(r[k]) for r in rates) + " |")
    for t in (40, 80, 119):
        w(f"| median population, year {t} | " + " | ".join(
            f"{statistics.median(R[s]['Y'].get(t, {}).get('n', 0) for s in seeds):.0f}" for R in (C, M, S)) + " |")
    led = []
    for R in (C, M, S):
        n, hist = Counter(), None
        for r in R.values():
            n.update(r["ledger"]["n"])
            hist = r["ledger"]["hist"] if hist is None else [a + b for a, b in zip(hist, r["ledger"]["hist"])]
        led.append((n, hist))
    w("| ledger: median food held ÷ need at eating | " + " | ".join(A.fmt(median(h)) for _, h in led) + " |")

    # effect size and the frozen null reading
    d = [int(C[s]["extinct"]) - int(M[s]["extinct"]) for s in seeds]
    eff = sum(d) / len(d)
    rng = random.Random(2026)
    boots = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(10000))
    lo, hi = boots[249], boots[9749]
    f1 = sum(ext_file(EXP / "F1_baseline_fragility" / "output" / f"seed_{s}.json") for s in F1_SEEDS)
    f2 = sum(ext_file(EXP / "F2_perfect_search" / "output" / f"seed_{s}.json") for s in F1_SEEDS)
    half_f2 = (1 - f2 / f1) / 2 * mc
    w(f"\n**Effect** (C − M extinction share): {eff:+.3f}, 95% interval [{lo:+.3f}, {hi:+.3f}]. Half of F2's effect on "
      f"these seeds: {half_f2:.3f} (F2's relative reduction {1 - f2 / f1:.2f}, halved, × C's share {mc:.3f}).\n")
    dm, _, _, pm = rows["M"]
    if pm < 0.05 and dm < dc:
        verdict = "**Co-residence saves worlds: MC1 is real**; its size is the effect estimate."
    elif pm < 0.05 and dm > dc:
        verdict = "**Co-residence harms survival** (to be examined read-only)."
    elif hi < half_f2:
        verdict = "**MC1 is genuinely weak**: any benefit is smaller than half of F2's; move to P2 with confidence."
    else:
        verdict = "**Still unresolved** at this sample; reported as such, the creator decides."
    w(f"Frozen rule: {verdict}")
    if rows["S"][3] < 0.05:
        w("\n**Caveat (frozen):** the sham reached p < 0.05 against the control: the noise is larger than the test assumes.")
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
