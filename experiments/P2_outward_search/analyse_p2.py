"""P2 analysis in the frozen order (preregistration.md, `P2-frozen`). Written and smoke-tested before any data.

Operational details (written before data):
- Manipulation check: per world, the share of seeker-weeks with an eligible single of the other sex within sight
  (Encounters observer); P against C, paired over worlds (ties and worlds with no seeker-weeks in either arm
  excluded); passes if P is higher in more worlds than lower and the exact two-sided sign test gives p < 0.05.
- Effect = C's extinction share minus P's (positive = fewer extinctions under P), paired by seed; 95% interval:
  percentile bootstrap over seeds, 10,000 resamples, random.Random(2026).
- Half of F2's effect, in absolute terms: (1 − F2's extinctions ÷ F1's on F1's 64 seeds) ÷ 2 × C's extinction share.
- New pairings per seeker-year: people newly partnered after week one ÷ (seeker-weeks ÷ 52).
- The P2 log: in C, "taken" counts any explore step to the branch's (random) destination, which the general explore
  option shares; in P it counts only the outward (or fall-back) step. Take-up is therefore reported, not compared.

  python experiments/P2_outward_search/analyse_p2.py
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

SEEDS = tuple(range(2257, 2513))


def enc_share(r):
    e = r["enc"]
    return e["seeker_weeks_eligible_in_sight"] / e["seeker_weeks"] if e.get("seeker_weeks") else None


def main(out=HERE / "output", seeds=SEEDS, write=True, pilot=HERE / "output_pilot" / "pilot.md"):
    C, P, S = (load(out, seeds, a) for a in ("c", "p", "s"))
    L = []
    w = L.append
    w("# P2 — Leave when there is no one: results\n")
    w(f"Frozen as `P2-frozen`. {len(seeds)} new seeds ({seeds[0]}–{seeds[-1]}), 120 years; arms C (settings off), "
      "P (outward search), S (sham).\n")
    w("## Validity\n")
    ok_zero = "All: PASS" in (out / "zero.txt").read_text(encoding="utf-8")
    ok_pilot = "**PASS**" in pilot.read_text(encoding="utf-8")
    fps = {r["code_hash"] for R in (C, P, S) for r in R.values()}
    ok_code = len(fps) == 1 and all(r["code_hash"] == r["code_hash_after"] for R in (C, P, S) for r in R.values())
    for label, ok in (("Zero checks", ok_zero), ("Feasibility pilot", ok_pilot), ("Code unchanged", ok_code)):
        w(f"- {label}: **{'yes' if ok else 'NO'}**")
    valid = ok_zero and ok_pilot and ok_code
    w(f"\n**{'Valid' if valid else 'NOT VALID: recorded, not interpreted'}.**\n")
    dc = sum(r["extinct"] for r in C.values())
    mc = dc / len(seeds)
    w(f"## Baseline (rule 14)\n\nControl on these seeds: {dc} of {len(seeds)} died out ({mc:.1%}).\n")

    w("## Manipulation check\n")
    up = dn = 0
    for s in seeds:
        a, b = enc_share(C[s]), enc_share(P[s])
        if a is None or b is None or a == b:
            continue
        up += b > a
        dn += b < a
    pman = sign_test(up, dn)
    manip = up > dn and pman < 0.05
    pooled = []
    for R in (C, P, S):
        n = Counter()
        for r in R.values():
            n.update(r["enc"])
        pooled.append(n)
    w("| | C | P outward | S sham |")
    w("|---|---|---|---|")
    w("| seeker-weeks with an eligible single in sight (pooled) | " + " | ".join(
        A.fmt(n["seeker_weeks_eligible_in_sight"] / n["seeker_weeks"]) for n in pooled) + " |")
    w("| seeker-weeks (all worlds) | " + " | ".join(str(n["seeker_weeks"]) for n in pooled) + " |")
    w("| new pairings per seeker-year (people) | " + " | ".join(
        A.fmt(n["new_partnered_people"] / (n["seeker_weeks"] / 52)) for n in pooled) + " |")
    w(f"\nPer world, P against C: higher in {up}, lower in {dn}; exact two-sided sign test p = {pman:.3g}: "
      f"**{'passes' if manip else 'FAILS'}**\n")
    for a, n in zip("CPS", pooled):
        trig = sum(v for k, v in n.items() if k.startswith("trigger_"))
        w(f"- P2 log, {a}: trigger weeks {trig}; " + ", ".join(
            f"{k[8:]} {v} (taken {n['taken_' + k[8:]]})" for k, v in sorted(n.items()) if k.startswith("trigger_")))

    w("\n## Extinction (the frozen outcome)\n")
    rows = {}
    for name, X in (("P", P), ("S", S)):
        saved = [s for s in seeds if C[s]["extinct"] and not X[s]["extinct"]]
        lost = [s for s in seeds if not C[s]["extinct"] and X[s]["extinct"]]
        rows[name] = (sum(X[s]["extinct"] for s in seeds), len(saved), len(lost), sign_test(len(saved), len(lost)))
    w("| | C | P outward | S sham |")
    w("|---|---|---|---|")
    w(f"| worlds died out (of {len(seeds)}) | {dc} | **{rows['P'][0]}** | {rows['S'][0]} |")
    w(f"| paired against C: saved / lost | – | {rows['P'][1]} / {rows['P'][2]} | {rows['S'][1]} / {rows['S'][2]} |")
    w(f"| exact two-sided sign test | – | **p = {rows['P'][3]:.3f}** | p = {rows['S'][3]:.3f} |")
    rates = [A.rates(None, [(r, 0, (r["E"] + 1) if r["extinct"] else 120) for r in R.values()]) for R in (C, P, S)]
    for k in ("births_per_woman_year", "child_deaths_per_birth", "deaths_per_person_year", "starving_share",
              "block_no_partner") + tuple("cause_" + c for c in A.CAUSES):
        w(f"| {k} | " + " | ".join(A.fmt(r[k]) for r in rates) + " |")
    for t in (40, 80, 119):
        w(f"| median population, year {t} | " + " | ".join(
            f"{statistics.median(R[s]['Y'].get(t, {}).get('n', 0) for s in seeds):.0f}" for R in (C, P, S)) + " |")
    led = []
    for R in (C, P, S):
        n, hist = Counter(), None
        for r in R.values():
            n.update(r["ledger"]["n"])
            hist = r["ledger"]["hist"] if hist is None else [a + b for a, b in zip(hist, r["ledger"]["hist"])]
        led.append((n, hist))
    w("| ledger: median food held ÷ need at eating | " + " | ".join(A.fmt(median(h)) for _, h in led) + " |")
    w("| ledger: starving share of adult-weeks | " + " | ".join(
        A.fmt(n["starving"] / n["aw"]) if n["aw"] else "–" for n, _ in led) + " |")

    d = [int(C[s]["extinct"]) - int(P[s]["extinct"]) for s in seeds]
    eff = sum(d) / len(d)
    rng = random.Random(2026)
    boots = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(10000))
    lo, hi = boots[249], boots[9749]
    f1 = sum(ext_file(EXP / "F1_baseline_fragility" / "output" / f"seed_{s}.json") for s in F1_SEEDS)
    f2 = sum(ext_file(EXP / "F2_perfect_search" / "output" / f"seed_{s}.json") for s in F1_SEEDS)
    half_f2 = (1 - f2 / f1) / 2 * mc
    w(f"\n**Effect** (C − P extinction share): {eff:+.3f}, 95% interval [{lo:+.3f}, {hi:+.3f}]. Half of F2's effect on "
      f"these seeds: {half_f2:.3f} (F2's relative reduction {1 - f2 / f1:.2f}, halved, × C's share {mc:.3f}).\n")
    dp, _, _, pp = rows["P"]
    if not manip:
        verdict = "**the manipulation check failed: the outcome is not read.**"
    elif pp < 0.05 and dp < dc:
        verdict = "**Outward search saves worlds**; its size is the effect estimate."
    elif pp < 0.05 and dp > dc:
        verdict = "**Outward search harms survival** (to be examined read-only, starting with the costs)."
    elif hi < half_f2:
        verdict = "**P2 is genuinely weak**: any benefit is smaller than half of F2's."
    else:
        verdict = "**Unresolved** at 256 worlds; reported as such, the creator decides."
    w(f"Frozen rule: {verdict}")
    if rows["S"][3] < 0.05:
        w("\n**Caveat (frozen):** the sham reached p < 0.05 against the control: the noise is larger than the test assumes.")
    if not valid:
        w("\n**Not valid: recorded, not interpreted.**")
    w("\nP2 is not added to ACL's nature by this result; that is the creator's decision.")
    text = "\n".join(L) + "\n"
    if write:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
