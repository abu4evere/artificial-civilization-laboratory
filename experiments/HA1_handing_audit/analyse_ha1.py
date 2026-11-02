"""HA1 analysis, written before any data (questions.md, frozen as `HA1-frozen`).

The zero checks run on GitHub while the creator is using the PC (light use); their record is `zero_cloud.log` (the
cloud zero job's own output, saved from its log), or `zero_local.log` when run locally.

  python experiments/HA1_handing_audit/analyse_ha1.py            # writes results.md
  python experiments/HA1_handing_audit/analyse_ha1.py --smoke --dir <folder>
"""
from __future__ import annotations

import bisect
import glob
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_ha1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261101)
E_MIN, C_MIN = 0.10, 0.05
LATER = 5 * R.WPY
GROUPS = ("child", "12-15", "16+")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {}
    for f in sorted(glob.glob(str(OUTDIR / "h_seed_*.json"))):
        r = json.load(open(f))
        runs[r["seed"]] = r
    zero = ""
    for name in ("zero_cloud.log", "zero_local.log"):
        if (HERE / name).exists():
            zero = (HERE / name).read_text(encoding="utf-8", errors="replace")
            break
    R.base.setup(R.CODE)
    fp_now = R.base.fingerprint(R.CODE)
    m = re.search(r"fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    want = sorted(R.SEEDS) if not SMOKE else sorted(runs)
    present = sorted(runs) == want and len(want) > 0
    fps = {r["code_hash"] for r in runs.values()} | {r["code_hash_after"] for r in runs.values()}
    mism = sum(sum(r["mismatch"].values()) for r in runs.values())
    ok = bool(zero_ok and present and fps == {fp_now} and mism == 0)
    L = ["# HA1 — Why does handing stay rare? Results", "",
         "Frozen as `HA1-frozen`. run_ha1.py, analyse_ha1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks (All: PASS, same `code_v11` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(runs)} of {len(want)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_v11`'s: **{'yes' if fps == {fp_now} else 'NO'}**",
         f"- Every handing came from a decision seen with a handing option to that receiver (mismatches 0): "
         f"**{'yes' if mism == 0 else f'NO ({mism})'}**",
         "", f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    seeds = sorted(runs)
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def col(group, j):
        return np.array([float(sum(v[j] for g, v in runs[s]["by"].items() if group is None or g == group))
                         for s in seeds])

    def ratio(num, den):
        if den.sum() == 0:
            return None, None, None
        with np.errstate(invalid="ignore", divide="ignore"):
            bs = (W @ num) / (W @ den)
        bs = bs[np.isfinite(bs)]
        return num.sum() / den.sum(), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))

    def fmt(t, d=4):
        return "n/a" if t[0] is None else f"{t[0]:.{d}f} [{t[1]:.{d}f}, {t[2]:.{d}f}]"
    D, Rm, Nt, O, M = col(None, 0), col(None, 1), col(None, 2), col(None, 3), col(None, 4)
    E, C = ratio(O, D), ratio(M, O)
    if E[0] is None:
        verdict = "no data"
    elif E[0] < E_MIN:
        verdict = "opportunity-limited"
    elif C[0] is not None and C[0] < C_MIN:
        verdict = "choice-limited"
    else:
        verdict = "neither"
    L += ["## Primary (frozen)", "",
          f"Eligible decisions (a person holding a made thing, reaching the choice, years 100-200): {int(D.sum()):,}.", "",
          "| quantity | value [95%] |", "|---|---|",
          f"| **E**: share with at least one handing option | **{fmt(E)}** |",
          f"| **C**: mean softmax mass on handing, given an option | **{fmt(C)}** |", "",
          f"Rule (hierarchical, on the pooled point estimates): opportunity-limited if E < {E_MIN}; else choice-limited "
          f"if C < {C_MIN}; else neither.", "", f"**Reading: {verdict}.**", ""]

    hands = sum(r["sums"].get("hands", 0.0) for r in runs.values())
    ay = sum(r["sums"].get("adult_years", 0.0) for r in runs.values())
    L += ["## Secondary (described, not decisive)", "",
          "### The funnel (share of eligible decisions)", "",
          "| stage | share |", "|---|---|",
          f"| someone within reach with room | {Rm.sum() / D.sum():.4f} |",
          f"| someone with net > 0 | {Nt.sum() / D.sum():.4f} |",
          f"| a handing option | {O.sum() / D.sum():.4f} |",
          f"| expected handings (summed mass) | {M.sum():,.1f} |",
          f"| handings done | {int(hands):,} |",
          f"| handings per adult-year | {hands / ay:.3f} |" if ay else "| handings per adult-year | - |", ""]
    L += ["### By the giver's age", "", "| giver | decisions | E | C | top score minus best handing score |",
          "|---|---|---|---|---|"]
    for g in GROUPS:
        d, o, mm, gap = col(g, 0).sum(), col(g, 3).sum(), col(g, 4).sum(), col(g, 5).sum()
        L.append(f"| {g} | {int(d):,} | {o / d:.4f} | {mm / o:.4f} | {gap / o:.3f} |" if d and o
                 else f"| {g} | {int(d):,} | {o / d if d else 0:.4f} | - | - |")
    rel = defaultdict(lambda: [0, 0.0])
    for r in runs.values():
        for k, v in r["rel"].items():
            rel[k][0] += v[0]
            rel[k][1] += v[1]
    to = sum(v[0] for v in rel.values())
    tm = sum(v[1] for v in rel.values())
    hrel = defaultdict(int)
    for r in runs.values():
        for h in r["hands"]:
            hrel[h[3]] += 1
    L += ["", "### By relation", "", "| relation | share of handing options | share of handing mass | share of handings |",
          "|---|---|---|---|"]
    for k in ("kin", "partner", "other"):
        L.append(f"| {k} | {rel[k][0] / to:.3f} | {rel[k][1] / tm:.3f} | {hrel[k] / hands:.3f} |" if to and tm and hands
                 else f"| {k} | - | - | - |")
    # Knowledge with the object (an association, not proof of transmission)
    know = {0: [0, 0], 1: [0, 0]}                           # knew -> [handings counted, made the kind within 5 years]
    for r in runs.values():
        idx = defaultdict(list)
        for t, maker, kind in r["makes"]:
            idx[(maker, kind)].append(t)
        for v in idx.values():
            v.sort()
        end = r["final_tick"]
        for t, recv, kind, _, knew in r["hands"]:
            if t + LATER > end:
                continue
            ts = idx.get((recv, kind), [])
            j = bisect.bisect_right(ts, t)
            made = j < len(ts) and ts[j] <= t + LATER
            know[knew][0] += 1
            know[knew][1] += made
    L += ["", "### Knowledge with the object: receivers who made the kind they received within 5 years", "",
          "| receiver | handings counted | made it within 5 years |", "|---|---|---|"]
    for knew, name in ((0, "did not know the kind"), (1, "already knew it")):
        a, b = know[knew]
        L.append(f"| {name} | {a:,} | {b / a:.3f} |" if a else f"| {name} | 0 | - |")
    hold = defaultdict(int)
    for r in runs.values():
        for k, v in r["holders"].items():
            hold[k] += v
    th = sum(hold.values())
    L += ["", "### Who holds made things (yearly census, years 100-200)", "", "| holder | share of made things held |",
          "|---|---|"]
    for k in ("child", "12-15", "16-59", "60+"):
        L.append(f"| {k} | {hold[k] / th:.3f} |" if th else f"| {k} | - |")
    L.append("")
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
