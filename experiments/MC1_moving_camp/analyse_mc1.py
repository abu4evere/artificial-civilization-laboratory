"""MC1 analysis in the frozen order (preregistration.md, `MC1-frozen`). Written and smoke-tested before any MC1 data.
Arms c (control, re-run in this copy; must reproduce F1), m (moving camp), s (sham).

  python experiments/MC1_moving_camp/analyse_mc1.py
"""
from __future__ import annotations

import json
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

SEEDS = tuple(range(501, 517)) + tuple(range(601, 617)) + tuple(range(811, 819)) + tuple(range(1101, 1125))


def load(out, seeds, arm):
    R = {}
    for s in seeds:
        r = json.loads((out / f"{arm}_seed_{s}.json").read_text(encoding="utf-8"))
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


def sign_test(saved, lost):
    n = saved + lost
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(comb(n, i) for i in range(min(saved, lost) + 1)) / 2 ** n)


def ledger(R):
    n, hist = Counter(), None
    for r in R.values():
        n.update(r["ledger"]["n"])
        h = r["ledger"]["hist"]
        hist = h if hist is None else [a + b for a, b in zip(hist, h)]
    return n, hist


def main(out=HERE / "output", seeds=SEEDS, write=True):
    C, M, S = (load(out, seeds, a) for a in ("c", "m", "s"))
    L = []
    w = L.append
    w("# MC1 — A camp that goes where the couple goes: results\n")
    w("Frozen as `MC1-frozen`. Arms on F1's 64 seeds, 120 years, one code copy: C control (settings off), M moving camp, "
      "S sham (one extra random draw in week one).\n")
    w("## Validity\n")
    ok_zero = "All: PASS" in (out / "zero.txt").read_text(encoding="utf-8")
    pilot = (out / "pilot" / "verdict.txt").read_text(encoding="utf-8").strip()
    ok_rep = all(r.get("reproduces") for r in C.values())
    ok_code = all(r["code_hash"] == r["code_hash_after"] for R in (C, M, S) for r in R.values())
    for label, ok in (("Zero checks", ok_zero), ("Feasibility pilot: " + pilot, "PASS" in pilot),
                      ("Control re-run reproduces F1's populations, all seeds", ok_rep), ("Code unchanged", ok_code)):
        w(f"- {label}: **{'yes' if ok else 'NO'}**")
    valid = ok_zero and "PASS" in pilot and ok_rep and ok_code
    w(f"\n**{'Valid' if valid else 'NOT VALID: recorded, not interpreted'}.**\n")
    dc = sum(r["extinct"] for r in C.values())
    w(f"## Baseline (rule 14)\n\nControl on these seeds: {dc} of {len(seeds)} died out.\n")

    w("## Manipulation check\n")
    ac, am, as_ = per_couple_apart(C), per_couple_apart(M), per_couple_apart(S)
    manip = ac is not None and am is not None and am <= ac / 2
    w(f"- Couples apart, per partnered non-pregnant woman-week: C {A.fmt(ac)}, M {A.fmt(am)} (must be at most half of "
      f"C's), S {A.fmt(as_)}: **{'yes' if manip else 'NO'}**\n")

    w("## Extinction (the frozen outcome)\n")
    rows = {}
    for name, X in (("M", M), ("S", S)):
        saved = [s for s in seeds if C[s]["extinct"] and not X[s]["extinct"]]
        lost = [s for s in seeds if not C[s]["extinct"] and X[s]["extinct"]]
        rows[name] = (sum(X[s]["extinct"] for s in seeds), saved, lost, sign_test(len(saved), len(lost)))
    w("| | C control | M moving camp | S sham |")
    w("|---|---|---|---|")
    w(f"| worlds died out (of {len(seeds)}) | {dc} | **{rows['M'][0]}** | {rows['S'][0]} |")
    w(f"| paired against C: saved / lost | – | {len(rows['M'][1])} / {len(rows['M'][2])} | {len(rows['S'][1])} / {len(rows['S'][2])} |")
    w(f"| exact two-sided sign test | – | **p = {rows['M'][3]:.3f}** | p = {rows['S'][3]:.3f} |")
    for t in (40, 80, 119):
        w(f"| median population, year {t} | " + " | ".join(
            f"{statistics.median(R[s]['Y'].get(t, {}).get('n', 0) for s in seeds):.0f}" for R in (C, M, S)) + " |")
    rates = [A.rates(None, [(r, 0, (r["E"] + 1) if r["extinct"] else 120) for r in R.values()]) for R in (C, M, S)]
    for k in ("births_per_woman_year", "block_no_partner", "child_deaths_per_birth", "starving_share", "cause_starvation",
              "cause_illness", "deaths_per_person_year"):
        w(f"| {k} | " + " | ".join(A.fmt(r[k]) for r in rates) + " |")
    led = [ledger(R) for R in (C, M, S)]
    w("| ledger: median food held ÷ need at eating | " + " | ".join(A.fmt(median(h)) for _, h in led) + " |")
    w("| ledger: starving share of adult-weeks | " + " | ".join(A.fmt(n["starving"] / n["aw"]) for n, _ in led) + " |")
    dm, sm, lm, pm = rows["M"]
    w(f"\nM saved {sm}; M lost {lm}.\n")
    if pm < 0.05 and dm < dc:
        verdict = "**MC1 reduces extinction.**"
    elif pm < 0.05 and dm > dc:
        verdict = "**MC1 increases extinction** (to be examined read-only, starting with the ledger)."
    else:
        verdict = "**No detectable effect on extinction at this sample.**"
    w(f"Frozen rule (paired sign test, p < 0.05): {verdict}")
    if rows["S"][3] < 0.05:
        w("\n**Caveat (frozen):** the sham itself reached p < 0.05 against the control: the noise is larger than the test "
          "assumes, and the reading above carries that caveat.")
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
