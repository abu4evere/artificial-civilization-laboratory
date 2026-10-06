"""F2 analysis in the frozen order (preregistration.md, `F2-frozen`). Written and smoke-tested before any F2 data.

Operational definitions written with this file, before data (the design left them open):
- A world dies out as in F1: nobody alive at year 120.
- Manipulation check: over all 64 worlds, the share of woman-weeks (16-45) with no partner under perfect finding must be
  **at most half** of F1's on the same seeds. Otherwise the switch did not deliver perfect finding and nothing is read.
- Beside it (not a check): the share of single women with **no eligible man anywhere in the world** (mid-year snapshots),
  which perfect finding cannot remove: the size story's own signature.

  python experiments/F2_perfect_search/analyse_f2.py
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
F1 = HERE.parent / "F1_baseline_fragility"
sys.path.insert(0, str(F1))
import analyse_f1 as A  # noqa: E402

SEEDS = tuple(range(501, 517)) + tuple(range(601, 617)) + tuple(range(811, 819)) + tuple(range(1101, 1125))


def load(out, seeds):
    R = {}
    for s in seeds:
        r = json.loads((out / f"seed_{s}.json").read_text(encoding="utf-8"))
        r["Y"] = {int(k): v for k, v in r["years"].items()}
        r["extinct"] = not (len(r["pops"]) == 12 and r["pops"][-1] > 0)
        r["E"] = (r["final_tick"] - 1) // A.WPY if r["extinct"] else None
        R[s] = r
    return R


def share(R, num, den):
    n = sum(v.get(num, 0) for r in R.values() for v in r["Y"].values())
    d = sum(v.get(den, 0) for r in R.values() for v in r["Y"].values())
    return n / d if d else None


def main(out=HERE / "output", f1out=F1 / "output", seeds=SEEDS, write=True):
    P = load(out, seeds)
    C = load(f1out, seeds)
    L = []
    w = L.append
    w("# F2 — Perfect partner finding: results\n")
    w(f"Frozen as `F2-frozen`. Diagnostic copy of the control code, oracle pairing on; paired with F1's replays of the same "
      f"{len(seeds)} seeds. A2-full people, 120 years.\n")
    w("## Validity\n")
    zero = (out / "zero.txt").read_text(encoding="utf-8")
    ok_zero = "All: PASS" in zero
    ok_code = all(r["code_hash"] == r["code_hash_after"] for r in P.values())
    ok_obs = "CHANGES" not in (f1out / "checks.txt").read_text(encoding="utf-8")
    for label, ok in (("Zero checks (switch off reproduces the control world; switch on pairs)", ok_zero),
                      ("Code unchanged during runs", ok_code), ("Observer read-only (F1's check)", ok_obs)):
        w(f"- {label}: **{'yes' if ok else 'NO'}**")
    valid = ok_zero and ok_code and ok_obs
    w(f"\n**{'Valid' if valid else 'NOT VALID: recorded, not interpreted'}.**\n")

    w("## Manipulation check\n")
    np_c = share(C, "r_no_partner", "woman_weeks")
    np_p = share(P, "r_no_partner", "woman_weeks")
    manip = np_c is not None and np_p is not None and np_p <= np_c / 2
    w(f"- Share of woman-weeks (16-45) with no partner: F1 {A.fmt(np_c)}, F2 {A.fmt(np_p)} (must be at most half): "
      f"**{'yes' if manip else 'NO'}**")
    w(f"- Oracle pairings made: {sum(r['oracle_pairs'] for r in P.values())} in {len(seeds)} worlds.")
    sw_c = share(C, "women_single_no_mate", "women_single")
    sw_p = share(P, "women_single_no_mate", "women_single")
    w(f"- Beside it: single women with no eligible man anywhere in the world (share of single-woman snapshots): F1 "
      f"{A.fmt(sw_c)}, F2 {A.fmt(sw_p)}.\n")

    w("## Population and extinction (the frozen outcome)\n")
    dc = sum(r["extinct"] for r in C.values())
    dp = sum(r["extinct"] for r in P.values())
    saved = [s for s in seeds if C[s]["extinct"] and not P[s]["extinct"]]
    lost = [s for s in seeds if not C[s]["extinct"] and P[s]["extinct"]]
    w(f"| | F1 (as now) | F2 (perfect finding) |")
    w("|---|---|---|")
    w(f"| worlds died out | {dc} of {len(seeds)} | **{dp} of {len(seeds)}** |")
    for t in (20, 40, 80, 119):
        a = [C[s]["Y"].get(t, {}).get("n", 0) for s in seeds]
        b = [P[s]["Y"].get(t, {}).get("n", 0) for s in seeds]
        w(f"| median population at year {t} | {statistics.median(a):.0f} | {statistics.median(b):.0f} |")
    for t in (20, 40):
        a = [C[s]["Y"].get(t, {}).get("women", 0) for s in seeds]
        b = [P[s]["Y"].get(t, {}).get("women", 0) for s in seeds]
        w(f"| median women 16-45 at year {t} | {statistics.median(a):.0f} | {statistics.median(b):.0f} |")
    w(f"\nPaired: saved by perfect finding {len(saved)} ({saved}); lost under it {len(lost)} ({lost}).\n")
    if dp <= 5:
        verdict = "**Search is the bottleneck (story A).** Next: design M2/M3 properly, anchored (rule 17)."
    elif dp >= 17:
        verdict = ("**Size is the bottleneck (story B).** Search is ruled out as the main cause; next: M1 (size) and "
                   "M4 (density).")
    else:
        verdict = ("**Both.** Search matters, and twenty is still too few for some worlds; compare F2's surviving and dying "
                   "worlds (read-only) before any design.")
    w(f"Frozen rule (≤ 5 search, ≥ 17 size, 6–16 both): {dp} of {len(seeds)}: {verdict}")
    if not manip:
        w("\n**The manipulation check failed: under the frozen rule nothing is read from this outcome.**")
    w("")

    w("## Worlds that still die under perfect finding (descriptive)\n")
    ext = [r for r in P.values() if r["extinct"]]
    if ext:
        w("| seed | E | last birth B | E − B | F1 died out? |")
        w("|---|---|---|---|---|")
        for r in sorted(ext, key=lambda r: r["E"]):
            B = max((b[0] for b in r["births"]), default=-1)
            w(f"| {r['seed']} | {r['E']} | {B} | {r['E'] - B} | {'yes' if C[r['seed']]['extinct'] else 'no'} |")
        t = A.rates(None, [(r, 0, r["E"] + 1) for r in ext])
        u = A.rates(None, [(r, 0, 120) for r in P.values() if not r["extinct"]])
        w("\n| measure | F2 extinct, whole life | F2 survivors, whole run |")
        w("|---|---|---|")
        for k in ("births_per_woman_year", "deaths_per_person_year", "child_deaths_per_birth", "starving_share",
                  "block_no_partner", "block_apart", "block_nursing", "block_eligible",
                  "cause_starvation", "cause_thirst", "cause_illness", "cause_old age"):
            w(f"| {k} | {A.fmt(t[k])} | {A.fmt(u[k])} |")
        ws = sum(v.get("women_single", 0) for r in ext for v in r["Y"].values())
        wf = sum(v.get("women_single_no_mate", 0) for r in ext for v in r["Y"].values())
        w(f"\nIn F2's dying worlds, single-woman-years {ws}, of which with no eligible man anywhere {wf} "
          f"({wf / max(1, ws):.0%}).")
        c = Counter(d[1] for r in ext for d in r["deaths"])
        w("Deaths by cause in F2's dying worlds: " + ", ".join(f"{k} {v}" for k, v in c.most_common()) + ".")
    if not valid:
        w("\n**Not valid: recorded, not interpreted.**")
    text = "\n".join(L) + "\n"
    if write:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
