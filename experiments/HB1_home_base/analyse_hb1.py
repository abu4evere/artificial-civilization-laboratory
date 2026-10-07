"""HB1 analysis in the frozen order (preregistration.md, `HB1-frozen`). Written and smoke-tested before any HB1 data.

  python experiments/HB1_home_base/analyse_hb1.py
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
import analyse_f1 as A  # noqa: E402

SEEDS = tuple(range(501, 517)) + tuple(range(601, 617)) + tuple(range(811, 819)) + tuple(range(1101, 1125))


def load(out, seeds, prefix=""):
    R = {}
    for s in seeds:
        r = json.loads((out / f"{prefix}seed_{s}.json").read_text(encoding="utf-8"))
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
    k = min(saved, lost)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def compare(C, X, seeds):
    saved = [s for s in seeds if C[s]["extinct"] and not X[s]["extinct"]]
    lost = [s for s in seeds if not C[s]["extinct"] and X[s]["extinct"]]
    return sum(X[s]["extinct"] for s in seeds), saved, lost, sign_test(len(saved), len(lost))


def main(out=HERE / "output", f1out=EXP / "F1_baseline_fragility" / "output", seeds=SEEDS, write=True):
    C = load(f1out, seeds)
    H = load(out, seeds, "h_")
    S = load(out, seeds, "s_")
    L = []
    w = L.append
    w("# HB1 — A shared home base: results\n")
    w("Frozen as `HB1-frozen`. Arms on F1's 64 seeds, 120 years: C control (F1's replays), H shared home base, S sham "
      "(one extra random draw in week one).\n")
    w("## Validity\n")
    ok_zero = "All: PASS" in (out / "zero.txt").read_text(encoding="utf-8")
    pilot = (out / "pilot" / "verdict.txt").read_text(encoding="utf-8").strip()
    ok_code = all(r["code_hash"] == r["code_hash_after"] for r in list(H.values()) + list(S.values()))
    for label, ok in (("Zero checks", ok_zero), ("Feasibility pilot: " + pilot, "PASS" in pilot), ("Code unchanged", ok_code)):
        w(f"- {label}: **{'yes' if ok else 'NO'}**")
    valid = ok_zero and "PASS" in pilot and ok_code
    w(f"\n**{'Valid' if valid else 'NOT VALID: recorded, not interpreted'}.**\n")

    w("## Baseline (rule 14)\n")
    dc = sum(r["extinct"] for r in C.values())
    w(f"Control on these seeds: {dc} of {len(seeds)} died out.\n")

    w("## Manipulation check\n")
    ac, ah, as_ = per_couple_apart(C), per_couple_apart(H), per_couple_apart(S)
    manip = ac is not None and ah is not None and ah <= ac / 2
    w(f"- Couples apart, per partnered non-pregnant woman-week: C {A.fmt(ac)}, H {A.fmt(ah)} (must be at most half of "
      f"C's), S {A.fmt(as_)}: **{'yes' if manip else 'NO'}**\n")

    w("## Extinction (the frozen outcome)\n")
    dh, sh_, lh, ph = compare(C, H, seeds)
    ds, ss_, ls_, ps = compare(C, S, seeds)
    w("| | C control | H home base | S sham |")
    w("|---|---|---|---|")
    w(f"| worlds died out (of {len(seeds)}) | {dc} | **{dh}** | {ds} |")
    w(f"| paired against C: saved / lost | – | {len(sh_)} / {len(lh)} | {len(ss_)} / {len(ls_)} |")
    w(f"| exact two-sided sign test | – | **p = {ph:.3f}** | p = {ps:.3f} |")
    for t in (40, 80, 119):
        w(f"| median population, year {t} | " + " | ".join(
            f"{statistics.median(R[s]['Y'].get(t, {}).get('n', 0) for s in seeds):.0f}" for R in (C, H, S)) + " |")
    rates = [A.rates(None, [(r, 0, (r["E"] + 1) if r["extinct"] else 120) for r in R.values()]) for R in (C, H, S)]
    for k in ("births_per_woman_year", "block_no_partner", "child_deaths_per_birth", "starving_share", "cause_illness",
              "cause_starvation", "deaths_per_person_year"):
        w(f"| {k} | " + " | ".join(A.fmt(r[k]) for r in rates) + " |")
    w(f"\nH saved {sh_}; H lost {lh}.\n")
    if ph < 0.05 and dh < dc:
        verdict = "**HB1 reduces extinction.**"
    elif ph < 0.05 and dh > dc:
        verdict = "**HB1 increases extinction** (to be examined read-only: crowding, food near home)."
    else:
        verdict = "**No detectable effect on extinction at this sample.**"
    w(f"Frozen rule (paired sign test, p < 0.05): {verdict}")
    if ps < 0.05:
        w("\n**Caveat (frozen):** the sham itself reached p < 0.05 against the control: the noise is larger than the test "
          "assumes, and the reading above is reported with that caveat.")
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
