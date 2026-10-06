"""U analysis in the frozen order (preregistration.md sections 5-8, with the operational definitions of section 10):
validity, manipulation check, population, the frozen predictions on paired worlds (pooled for completeness), the outcome
table, descriptives. Written and tested on a throwaway seed before any pilot or main data. Writes results.md.

  python experiments/N4_uncertain_winters/analyse_u.py
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
SEEDS = tuple(range(901, 917))
ARMS = ("c", "w", "p")
NAME = {"c": "C", "w": "W", "p": "P"}


def cv(xs):
    return statistics.pstdev(xs) / statistics.mean(xs) if len(xs) > 5 and statistics.mean(xs) > 0 else None


def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def f3(x):
    return "–" if x is None else f"{x:.3f}"


def ratio_met(num, den, k):
    """num ≥ k × den. Where den is zero the criterion is met only if num is positive (flagged in the report)."""
    if den == 0:
        return num > 0, True
    return num >= k * den, False


def main(out=OUT, seeds=SEEDS, years=120, rerun_seed=901, write=True):
    D = {(a, s): json.loads((out / f"{a}_seed_{s}.json").read_text(encoding="utf-8")) for a in ARMS for s in seeds}
    rerun = json.loads((out / f"c_seed_{rerun_seed}_rerun.json").read_text(encoding="utf-8"))
    L = []
    w = L.append
    w("# U — Uncertain years: results\n")
    w(f"Frozen as `U-frozen`. Arms: C (as now), W (wider years, world-wide), P (wider years, by quarter). A2-full people, "
      f"seeds {seeds[0]}–{seeds[-1]}, {years} years. Weather half-width {D[('w', seeds[0])]['half']} around 0.95.\n")

    w("## Validity\n")
    checks = (out / "checks.txt").read_text(encoding="utf-8").strip()
    pilot = (out / "pilot" / "verdict.txt").read_text(encoding="utf-8").strip()
    zero = (out / "zero.txt").read_text(encoding="utf-8")
    ok_probe = checks.count("READ-ONLY") >= 3 and "CHANGES" not in checks
    ok_code = all(r["code_hash"] == r["code_hash_after"] for r in D.values())
    ok_rerun = rerun["world_hash"] == D[("c", rerun_seed)]["world_hash"] and rerun["pops"] == D[("c", rerun_seed)]["pops"]
    ok_zero = "All: PASS" in zero
    for label, ok in (("Survival pilot: " + pilot, "PASS" in pilot), ("Probe read-only, all three arms", ok_probe),
                      ("Code unchanged during runs", ok_code),
                      (f"Control reproduces itself on rerun (seed {rerun_seed})", ok_rerun), ("P's zero checks", ok_zero)):
        w(f"- {label}: **{'yes' if ok else 'NO'}**")
    valid = "PASS" in pilot and ok_probe and ok_code and ok_rerun and ok_zero
    w(f"\n**{'Valid' if valid else 'NOT VALID: outcomes are recorded but not interpreted'}.**\n")

    n_dec = years // 10

    def alive(a, sd):
        return len(D[(a, sd)]["pops"]) == n_dec and D[(a, sd)]["pops"][-1] > 0
    paired = [sd for sd in seeds if all(alive(a, sd) for a in ARMS)]

    w("## Manipulation check (section 10, M1–M3)\n")
    cal = (out / "calibration" / "verdict.txt").read_text(encoding="utf-8") if (out / "calibration" / "verdict.txt").exists() else ""
    half = D[("w", seeds[0])]["half"]
    cal_cv = None
    for line in cal.splitlines():
        if line.startswith(f"half-width {half}:"):
            cal_cv = float(line.split("median CV ")[1].split(",")[0])

    def world_cv(a, sd):
        return cv([x["tile"] for x in D[(a, sd)]["autumn"][1:]])

    def quarter_cv(a, sd):
        au = D[(a, sd)]["autumn"][1:]
        return med([cv([x["quarters"][q] for x in au if x["quarters"][q] is not None]) for q in range(4)])

    def mean_tile(a, sd):
        au = D[(a, sd)]["autumn"][1:]
        return statistics.mean(x["tile"] for x in au) if au else None

    def food_pp(a, sd):
        return med([x["pp"] for x in D[(a, sd)]["autumn"][1:]])
    base = paired or list(seeds)
    m1w = {a: med([world_cv(a, sd) for sd in base]) for a in ARMS}
    m1q = {a: med([quarter_cv(a, sd) for sd in base]) for a in ARMS}
    m2 = {a: med([mean_tile(a, sd) for sd in base]) for a in ARMS}
    m3 = {a: med([food_pp(a, sd) for sd in base]) for a in ARMS}
    w(f"Over the {'paired' if paired else 'all'} seeds ({len(base)}); medians over worlds. Calibration's median CV at this "
      f"width: {f3(cal_cv)}.\n")
    w("| | C | W | P |")
    w("|---|---|---|---|")
    w(f"| M1 CV of mid-autumn food per land tile, whole world | {f3(m1w['c'])} | {f3(m1w['w'])} | {f3(m1w['p'])} |")
    w(f"| M1 CV of mid-autumn food per land tile, within a quarter (median of four) | {f3(m1q['c'])} | {f3(m1q['w'])} | {f3(m1q['p'])} |")
    w(f"| M2 mean mid-autumn food per land tile | {m2['c']:.2f} | {m2['w']:.2f} | {m2['p']:.2f} |")
    w(f"| M3 mid-autumn food on land per person | {m3['c']:.1f} | {m3['w']:.1f} | {m3['p']:.1f} |")
    target = 0.75 * cal_cv if cal_cv else None
    var_w = target is not None and m1w["w"] is not None and m1w["w"] >= target
    var_p = target is not None and m1q["p"] is not None and m1q["p"] >= target
    mean_w = abs(m2["w"] / m2["c"] - 1) <= 0.10
    mean_p = abs(m2["p"] / m2["c"] - 1) <= 0.10
    w(f"\n- Intended variability (M1 ≥ 0.75 × calibration's {f3(cal_cv)} = {f3(target)}): W, whole world "
      f"**{'yes' if var_w else 'no'}**; P, within a quarter **{'yes' if var_p else 'no'}**.")
    w(f"- Mean kept (M2 within 10% of C): W {m2['w'] / m2['c']:.3f} of C **{'yes' if mean_w else 'no'}**; "
      f"P {m2['p'] / m2['c']:.3f} of C **{'yes' if mean_p else 'no'}**.")
    manip = var_w and var_p
    if not (mean_w and mean_p):
        w("- **Flag (frozen):** an arm's average food moved more than 10% from C's: its differences from C may come from "
          "a richer or poorer world as well as a more variable one.")
    w("")

    w("## Population (reported beside every measure)\n")
    w("| arm | worlds died out | final population, median (all seeds) | final population, median (paired seeds) |")
    w("|---|---|---|---|")
    died = {a: sum(1 for s in seeds if not alive(a, s)) for a in ARMS}
    for a in ARMS:
        finals = [D[(a, s)]["pops"][-1] if alive(a, s) else 0 for s in seeds]
        pf = [D[(a, s)]["pops"][-1] for s in paired]
        w(f"| {NAME[a]} | {died[a]} of {len(seeds)} | {statistics.median(finals):.0f} | "
          + (f"{statistics.median(pf):.0f} |" if pf else "– |"))
    w(f"\nPaired seeds (all three arms alive at year {years}): {len(paired)} of {len(seeds)}.\n")
    collapse = died["w"] - died["c"] > 1 or died["p"] - died["c"] > 1

    def measures(sds):
        def P(a, s, key):
            return sum(D[(a, x)]["n"].get(str(s), {}).get(key, 0.0) for x in sds)

        def T(a, key):
            return sum(P(a, s, key) for s in range(4))
        hh = {a: [h[0] / h[1] for sd in sds for h in D[(a, sd)]["households"] if h[1] > 0] for a in ARMS}
        m = {}
        for a in ARMS:
            m[(a, "S1")] = statistics.median(hh[a]) if hh[a] else 0.0
            m[(a, "S2")] = sum(D[(a, sd)]["carers"][0] for sd in sds) / max(1, sum(D[(a, sd)]["carers"][1] for sd in sds))
            m[(a, "S3")] = ((P(a, 2, "forage_choice") / max(1, P(a, 2, "adult_weeks")))
                            / max(1e-9, P(a, 1, "forage_choice") / max(1, P(a, 1, "adult_weeks"))))
            m[(a, "G")] = T(a, "given") / max(1, T(a, "adult_weeks"))
            m[(a, "M")] = T(a, "moved") / max(1, T(a, "adult_weeks"))
        return m
    LAB = {"S1": "S1 median household stock ÷ winter need, start of winter",
           "S2": "S2 carers with food stashed, start of winter",
           "S3": "S3 autumn ÷ summer share of adult weeks foraging",
           "G": "G food given away per adult-week",
           "M": "M tiles moved per adult-week"}

    w("## The frozen predictions (verdict on paired worlds; pooled for completeness)\n")
    pm = measures(seeds)
    w("Pooled over all seeds: " + "; ".join(f"{k} " + " / ".join(f"{NAME[a]} {pm[(a, k)]:.3f}" for a in ARMS) for k in LAB) + ".\n")
    m = measures(paired)
    w(f"**Paired seeds ({len(paired)}), the verdict:**\n")
    w("| measure | C | W | P | W ≥ 1.5× C | W ≥ 1.25× P | P ≥ 1.5× C |")
    w("|---|---|---|---|---|---|---|")
    flags = []
    s_w = s_p = s_both = 0
    for k in ("S1", "S2", "S3"):
        a1, z1 = ratio_met(m[("w", k)], m[("c", k)], 1.5)
        a2, z2 = ratio_met(m[("w", k)], m[("p", k)], 1.25)
        a3, z3 = ratio_met(m[("p", k)], m[("c", k)], 1.5)
        if z1 or z2 or z3:
            flags.append(k)
        s_w += a1
        s_p += a3
        s_both += a1 and a2
        w(f"| {LAB[k]} | {m[('c', k)]:.3f} | {m[('w', k)]:.3f} | {m[('p', k)]:.3f} | {'yes' if a1 else 'no'} | "
          f"{'yes' if a2 else 'no'} | {'yes' if a3 else 'no'} |")
    w("\n| measure | C | W | P | P ≥ 1.2× W |")
    w("|---|---|---|---|---|")
    p2 = False
    for k in ("G", "M"):
        b, z = ratio_met(m[("p", k)], m[("w", k)], 1.2)
        if z:
            flags.append(k)
        p2 |= b
        w(f"| {LAB[k]} | {m[('c', k)]:.4f} | {m[('w', k)]:.4f} | {m[('p', k)]:.4f} | {'yes' if b else 'no'} |")
    if flags:
        w(f"\n(Flag: a zero denominator in {', '.join(flags)}; there the criterion is met only if the other value is positive.)")
    p1 = s_both >= 2
    w(f"\n- **Prediction 1** (storage rises in W, more than in C and in P: at least two storage measures with W ≥ 1.5× C "
      f"and W ≥ 1.25× P): {s_both} of 3: **{'met' if p1 else 'not met'}**.")
    w(f"- **Prediction 2** (sharing or moving: P ≥ 1.2× W on G or M): **{'met' if p2 else 'not met'}**.")
    w(f"- Storage rose (at least two measures ≥ 1.5× C) in W: {s_w} of 3; in P: {s_p} of 3.\n")

    w("## Outcome (section 8, mapped by section 10's rule)\n")
    if collapse:
        out_line = "**Collapse in W or P** (more than one world lost beyond C): the variability is too harsh for ACL's people; the design returns to the creator."
    elif p1:
        out_line = "**Storage rises in W, not P: H-L5 supported in its sharpened form.**" + (" Sharing or moving also rose in P." if p2 else "")
    elif s_w >= 2 and s_p >= 2:
        out_line = "**Storage rises in both alike: uncertainty matters but not its correlation; the sharpening fails.**"
    elif s_p >= 2 and s_p > s_w:
        out_line = "**Storage rises more in P than in W: falsifies H-L5's sharpened form.**"
    elif p2:
        out_line = "**Sharing or moving rises in P, storage not in W: the patchy half supported; correlated uncertainty absorbed some other way.**"
    elif s_w < 2 and s_p < 2:
        out_line = "**Nothing moves anywhere: uncertainty at this level is absorbed; H-L5 not supported here.**"
    else:
        out_line = "**Mixed: no row of section 8 fits; reported as it is.**"
    w(out_line)
    if not manip and not collapse:
        w("\n**The manipulation check did not show the intended variability: under the frozen rule a null here is not read "
          "as evidence about H-L5.**")
    if not p1 and s_w < 2 and manip:
        w("\n(Frozen reading of a null: this variability, in ACL's current world, is insufficient; not evidence that "
          "uncertainty is irrelevant.)")
    w("")

    w("## By season (descriptive, paired seeds)\n")
    w("| | season | C | W | P |")
    w("|---|---|---|---|---|")
    for s, sn in enumerate(("spring", "summer", "autumn", "winter")):
        for key, lab in (("forage_choice", "share of adult weeks foraging"), ("given", "food given per adult-week"),
                         ("moved", "tiles moved per adult-week")):
            vals = []
            for a in ARMS:
                num = sum(D[(a, x)]["n"].get(str(s), {}).get(key, 0.0) for x in paired)
                den = sum(D[(a, x)]["n"].get(str(s), {}).get("adult_weeks", 0.0) for x in paired)
                vals.append(f"{num / den:.4f}" if den else "–")
            w(f"| {lab} | {sn} | " + " | ".join(vals) + " |")

    if not valid:
        w("\n**Not valid: recorded, not interpreted.**")
    text = "\n".join(L) + "\n"
    if write:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)
    return text


if __name__ == "__main__":
    main()
