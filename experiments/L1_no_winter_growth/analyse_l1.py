"""L1 analysis in the frozen order (preregistration.md section 7): validity, manipulation check, the frozen test of the
immediate-return hypothesis (section 8), how people met the winter, population, children's deaths last. Written before
any L1 data. Writes results.md.

  python experiments/L1_no_winter_growth/analyse_l1.py
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
SEEDS = tuple(range(601, 617))
SEASONS = ("spring", "summer", "autumn", "winter")


def pct(a, b, d=1):
    return f"{100 * a / b:.{d}f}%" if b else "–"


def main():
    D = {(a, s): json.loads((OUT / f"{a}_seed_{s}.json").read_text(encoding="utf-8")) for a in "cl" for s in SEEDS}
    rerun = json.loads((OUT / "c_seed_601_rerun.json").read_text(encoding="utf-8"))
    L = []
    w = L.append
    w("# L1 — No growth in winter: results\n")
    w("Frozen as `L1-frozen`. Arms: C (the world as it is) and L (winter plant regrowth 0). A2-full people, seeds 601–616, "
      "120 years.\n")

    w("## Validity\n")
    checks = (OUT / "checks.txt").read_text(encoding="utf-8").strip()
    pilot = (OUT / "pilot" / "verdict.txt").read_text(encoding="utf-8").strip()
    ok_probe = checks.count("READ-ONLY") >= 2 and "CHANGES" not in checks
    ok_code = all(r["code_hash"] == r["code_hash_after"] for r in D.values())
    ok_rerun = rerun["state_hash"] == D[("c", 601)]["state_hash"] and rerun["pops"] == D[("c", 601)]["pops"]
    for label, ok in (("Survival pilot: " + pilot, "PASS" in pilot), ("Probe read-only, both arms", ok_probe),
                      ("Code unchanged during runs", ok_code), ("Control reproduces itself on rerun (seed 601)", ok_rerun)):
        w(f"- {label}: **{'yes' if ok else 'NO'}**")
    valid = "PASS" in pilot and ok_probe and ok_code and ok_rerun
    w(f"\n**{'Valid' if valid else 'NOT VALID: outcomes are recorded but not interpreted'}.**\n")

    def pooled(a, s, key):
        return sum(D[(a, x)]["n"].get(str(s), {}).get(key, 0.0) for x in SEEDS)

    w("## Manipulation check: did winter get leaner?\n")
    land = {}
    for a in "cl":
        for s in (2, 3):
            vals = [x["per_person"] for sd in SEEDS for x in D[(a, sd)]["land"] if x["season"] == s]
            land[(a, s)] = statistics.median(vals) if vals else None
    yld = {a: pooled(a, 3, "forage_food") / pooled(a, 3, "forage_weeks") for a in "cl"}
    m1 = land[("l", 3)] / land[("c", 3)]
    m2 = yld["l"] / yld["c"]
    w(f"- **M1** plant food on land per person, mid-winter (median): C {land[('c', 3)]:.0f}, L {land[('l', 3)]:.0f} "
      f"(L ÷ C {m1:.2f}); mid-autumn: C {land[('c', 2)]:.0f}, L {land[('l', 2)]:.0f}.")
    w(f"- **M2** food per forage week in winter: C {yld['c']:.1f}, L {yld['l']:.1f} (L ÷ C {m2:.2f}).")
    leaner = m1 < 0.9 or m2 < 0.9
    w(f"\nWinter got leaner in L (M1 or M2 at least 10% lower): **{'yes' if leaner else 'no'}**.\n")

    w("## The frozen test of the immediate-return hypothesis\n")
    hh = {a: [h[0] / h[1] for sd in SEEDS for h in D[(a, sd)]["households"] if h[1] > 0] for a in "cl"}
    da = {a: statistics.median(hh[a]) if hh[a] else 0.0 for a in "cl"}
    db = {a: sum(D[(a, sd)]["carers"][0] for sd in SEEDS) / max(1, sum(D[(a, sd)]["carers"][1] for sd in SEEDS)) for a in "cl"}
    dc = {a: (pooled(a, 2, "forage_choice") / pooled(a, 2, "adult_weeks")) / (pooled(a, 1, "forage_choice") / pooled(a, 1, "adult_weeks"))
          for a in "cl"}
    dd = {a: sum(D[(a, sd)]["seed_sown"] for sd in SEEDS) / max(1, sum(D[(a, sd)]["person_years"] for sd in SEEDS)) for a in "cl"}
    t1 = da["c"] > 0 and da["l"] >= 2 * da["c"]
    t2 = db["l"] >= 3 * db["c"] and db["l"] >= 0.10
    t3 = dc["l"] >= 1.2 * dc["c"]
    w("| criterion | C | L | threshold | met |")
    w("|---|---|---|---|---|")
    w(f"| D-a median household stock ÷ winter need | {da['c']:.3f} | {da['l']:.3f} | L ≥ 2× C | {'yes' if t1 else 'no'} |")
    w(f"| D-b carers with food stashed, start of winter | {100 * db['c']:.1f}% | {100 * db['l']:.1f}% | L ≥ 3× C and ≥ 10% | {'yes' if t2 else 'no'} |")
    w(f"| D-c autumn ÷ summer share of weeks foraging | {dc['c']:.3f} | {dc['l']:.3f} | L ≥ 1.2× C | {'yes' if t3 else 'no'} |")
    met = t1 + t2 + t3
    w(f"\nD-d seed sown per person-year (descriptive): C {dd['c']:.2f}, L {dd['l']:.2f}.")
    w(f"\n**Criteria met: {met} of 3.** " + (
        "**Two or more: the immediate-return hypothesis takes a serious hit.**" if met >= 2 else
        "**Fewer than two: the hypothesis survives this test.** " +
        ("Winter did get leaner, so this null may be read as evidence that the absence of storage is not mainly caused "
         "by mild winters, and only for removing winter growth alone under ACL's current world structure." if leaner else
         "But winter did not get leaner (outcome A): this null says nothing about lean seasons, only that this setting "
         "did not make one.")))
    w("\n(Frozen: failure to create delayed-return behaviour is not evidence that lean seasons are irrelevant; it is "
      "evidence only that removing winter growth alone is insufficient under ACL's current world structure.)\n")

    w("## How people met the winter (descriptive)\n")
    w("| winter | C | L |")
    w("|---|---|---|")
    for label, f in (("share of adult winter-weeks spent foraging", lambda a: pooled(a, 3, "forage_choice") / pooled(a, 3, "adult_weeks")),
                     ("share of adult winter-weeks going short", lambda a: pooled(a, 3, "short") / pooled(a, 3, "adult_weeks")),
                     ("food given away per adult winter-week", lambda a: pooled(a, 3, "given") / pooled(a, 3, "adult_weeks")),
                     ("hunting's share of food gathered", lambda a: pooled(a, 3, "hunt_food") / max(1, pooled(a, 3, "hunt_food") + pooled(a, 3, "forage_food"))),
                     ("food stashed in autumn per adult autumn-week", lambda a: pooled(a, 2, "stashed") / pooled(a, 2, "adult_weeks")),
                     ("adult winter starvation deaths per 1,000 adult winter-weeks", lambda a: 1000 * pooled(a, 3, "adult_starved") / pooled(a, 3, "adult_weeks"))):
        w(f"| {label} | {f('c'):.4f} | {f('l'):.4f} |")

    w("\n## Population\n")
    for a, name in (("c", "C"), ("l", "L")):
        finals = [D[(a, s)]["pops"][-1] if len(D[(a, s)]["pops"]) == 12 else 0 for s in SEEDS]
        died = sum(1 for s in SEEDS if len(D[(a, s)]["pops"]) < 12 or D[(a, s)]["pops"][-1] == 0)
        w(f"- {name}: worlds that died out {died} of 16; final population median {statistics.median(finals):.0f}.")

    w("\n## Children's winter starvation (read last)\n")
    for a, name in (("c", "C"), ("l", "L")):
        cw = sum(r[0] for s in SEEDS for r in D[(a, s)]["child_rows"])
        cs = sum(r[1] for s in SEEDS for r in D[(a, s)]["child_rows"])
        w(f"- {name}: {cs:,} of {cw:,} child-winters ({pct(cs, cw, 2)}).")

    if not valid:
        w("\n**Not valid: recorded, not interpreted.**")
    (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
