"""IW1 analysis, written before any data (questions.md, frozen as `IW1-frozen`; operational note 1).

  python experiments/IW1_item_worth/analyse_iw1.py            # writes results.md
  python experiments/IW1_item_worth/analyse_iw1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_iw1 import MAXN, SEEDS, WPY  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261031)
CUT = 6                                    # prior uses (frozen: "fewer than 6")


def rank(x):
    o = np.argsort(x, kind="mergesort")
    r = np.empty(len(x))
    r[o] = np.arange(len(x))
    for v in np.unique(x):                 # average ranks for ties
        m = x == v
        r[m] = r[m].mean()
    return r


def spearman(a, b):
    if len(a) < 3 or np.std(a) == 0 or np.std(b) == 0:
        return float("nan")
    return float(np.corrcoef(rank(np.asarray(a, float)), rank(np.asarray(b, float)))[0, 1])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {}
    for f in sorted(glob.glob(str(OUTDIR / "lp_seed_*.json"))):
        r = json.load(open(f))
        runs[r["seed"]] = r
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    present = sorted(runs) == sorted(SEEDS)
    fps = {r["code_hash"] for r in runs.values()} | {r["code_hash_after"] for r in runs.values()}
    mism = sum(sum(r["mismatch"].values()) for r in runs.values())
    ok = "All: PASS" in zero and present and len(fps) == 1 and mism == 0
    L = ["# IW1 — How does the worth of made things form? Results", "",
         "Frozen as `IW1-frozen` (operational note 1). run_iw1.py, analyse_iw1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({len(runs)} of {len(SEEDS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_v9`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Worth updates and make scores replay exactly (mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**",
         "", f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    seeds = sorted(runs)
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])

    def boot(num, den):
        point = num.sum() / den.sum() if den.sum() else float("nan")
        with np.errstate(invalid="ignore", divide="ignore"):
            reps = (W @ num) / (W @ den)
        lo, hi = np.nanpercentile(reps, [2.5, 97.5])
        return point, lo, hi

    def fmt(t, d=3):
        return f"{t[0]:+.{d}f} [{t[1]:+.{d}f}, {t[2]:+.{d}f}]"

    def fmtp(t, d=3):
        return f"{t[0]:.{d}f} [{t[1]:.{d}f}, {t[2]:.{d}f}]"

    # population
    liv = sum(sum(c[1] for c in runs[s]["census"]) for s in seeds)
    yrs = sum(len(runs[s]["census"]) for s in seeds)
    late = [c for s in seeds for c in runs[s]["census"] if 100 <= c[0] < 200]
    ext = sum(1 for s in seeds if runs[s]["extinct"])
    L += [f"Worlds: {n}; extinct {ext}. Mean living population {liv / yrs if yrs else float('nan'):.1f}; "
          f"adults in years 100-200: {np.mean([c[2] for c in late]) if late else float('nan'):.1f} per world-year.", ""]

    # per world: kind means, and makes (adults, years 100-200)
    Wm = {k: np.zeros(n) for k in ("nb", "ub", "felt_b", "na", "ua", "lt6", "nall", "unknown_b", "no_later",
                                    "off_n", "off_under", "off_unknown", "off_felt")}
    by_src = {}
    rhos = []
    for j, s in enumerate(seeds):
        r = runs[s]
        kinds = r["kinds"]
        mean = {k: v[1] / v[0] for k, v in kinds.items() if v[0] > 0}
        for sig, iv, uses, src, c0, f0, c1, f1 in r["makes"]:
            Wm["nall"][j] += 1
            Wm["lt6"][j] += uses < CUT
            if sig in mean:
                Wm["nb"][j] += 1
                Wm["ub"][j] += mean[sig] - iv
                Wm["felt_b"][j] += mean[sig]
                d = by_src.setdefault(src, [0, 0.0, 0])
                d[0] += 1
                d[1] += mean[sig] - iv
            else:
                Wm["unknown_b"][j] += 1
            if c1 > c0:
                Wm["na"][j] += 1
                Wm["ua"][j] += (f1 - f0) / (c1 - c0) - iv
            else:
                Wm["no_later"][j] += 1
        for sig, v in kinds.items():
            if v[3]:
                if sig in mean:
                    Wm["off_n"][j] += v[3]
                    Wm["off_under"][j] += v[3] * mean[sig] - v[4]
                    Wm["off_felt"][j] += v[3] * mean[sig]
                else:
                    Wm["off_unknown"][j] += v[3]
        xs = [(v[2], mean[k]) for k, v in kinds.items() if k in mean]
        if xs:
            rhos.append(spearman([a for a, _ in xs], [b for _, b in xs]))
    ub = boot(Wm["ub"], Wm["nb"])
    ua = boot(Wm["ua"], Wm["na"])
    felt_b = boot(Wm["felt_b"], Wm["nb"])
    lt6 = boot(Wm["lt6"], Wm["nall"])
    off = boot(Wm["off_under"], Wm["off_n"])
    L += ["## Q1 — Calibration at the make (adults, years 100-200)", "",
          f"Makes: {Wm['nall'].sum():,.0f}. Under-valuation = mean felt help of the kind - the maker's worth just before "
          "making (positive = worth below the help).", "",
          "| measure | value [95%] |", "|---|---|",
          f"| **(b) under-valuation, against everyone's uses of the kind** ({Wm['nb'].sum():,.0f} makes; kind never "
          f"used by anyone: {Wm['unknown_b'].sum():,.0f}) | **{fmt(ub)}** |",
          f"| (b) mean felt help per use of the kinds made | {fmtp(felt_b)} |",
          f"| (a) under-valuation, against the maker's own later uses ({Wm['na'].sum():,.0f} makes; no later use: "
          f"{Wm['no_later'].sum():,.0f}) | {fmt(ua)} |", ""]
    if by_src:
        L += ["| first source of the kind (the maker's) | makes | mean under-valuation (b) |", "|---|---|---|"]
        for src, (c, u, _) in sorted(by_src.items(), key=lambda x: -x[1][0]):
            L.append(f"| {src} | {c:,} | {u / c:+.3f} |")
        L.append("")

    # Q2
    bins = {"0": 0, "1-2": 0, "3-5": 0, "6+": 0}
    for s in seeds:
        for m in runs[s]["makes"]:
            u = m[2]
            bins["0" if u == 0 else "1-2" if u <= 2 else "3-5" if u <= 5 else "6+"] += 1
    tot = sum(bins.values())
    L += ["## Q2 — Experience: the maker's prior uses of the kind at each make", "",
          "| prior uses | makes | share |", "|---|---|---|"]
    for k, v in bins.items():
        L.append(f"| {k} | {v:,} | {v / tot if tot else float('nan'):.3f} |")
    L += ["", f"**Share resting on fewer than {CUT} uses: {fmtp(lt6)}.** (GPT: a diagnostic bin, not proof of "
          "inadequate learning.)", ""]

    # Q3
    traj = {}
    for s in seeds:
        for k, v in runs[s]["traj"].items():
            src, i = k.rsplit("|", 1)
            t = traj.setdefault(src, {})
            a = t.setdefault(int(i), [0, 0.0, 0.0])
            a[0] += v[0]
            a[1] += v[1]
            a[2] += v[2]
    L += ["## Q3 — Worth against uses, by how the person first got the kind (all ages, all years)", "",
          "Each cell: mean worth just before the use / mean felt help of that use (uses).", "",
          "| source | " + " | ".join(f"use {i}" for i in (0, 1, 2, 5, MAXN)) + "+ |",
          "|---|" + "---|" * 5]
    for src in sorted(traj, key=lambda x: -sum(v[0] for v in traj[x].values())):
        cells = []
        for i in (0, 1, 2, 5, MAXN):
            a = traj[src].get(i)
            cells.append(f"{a[1] / a[0]:.2f} / {a[2] / a[0]:.2f} ({a[0]:,})" if a and a[0] else "-")
        L.append(f"| {src} | " + " | ".join(cells) + " |")
    L.append("")

    # Q4
    fh = {}
    for s in seeds:
        for k, v in runs[s]["felt_hist"].items():
            fh[k] = fh.get(k, 0) + v
    callers = sorted({k.rsplit("|", 1)[0] for k in fh}, key=lambda c: -sum(v for k, v in fh.items() if k.startswith(c + "|")))
    L += ["## Q4 — Felt help per use (all ages, all years)", "",
          "| law that judged the use | uses | < 0 | 0-0.1 | 0.1-0.3 | > 0.3 |", "|---|---|---|---|---|---|"]
    for c in callers:
        row = [fh.get(f"{c}|{b}", 0) for b in ("<0", "0-0.1", "0.1-0.3", ">0.3")]
        t = sum(row)
        L.append(f"| `{c}` | {t:,} | " + " | ".join(f"{x / t:.3f}" for x in row) + " |")
    allu = sum(fh.values())
    over = sum(v for k, v in fh.items() if k.endswith("|0.1-0.3") or k.endswith("|>0.3"))
    L += ["", f"Share of all uses with felt help > 0.1: {over / allu if allu else float('nan'):.3f} of {allu:,}.", ""]

    # Q5
    lv = {}
    for s in seeds:
        for k, v in runs[s]["leave"].items():
            lv[k] = lv.get(k, 0) + v
    L += ["## Q5 — How kinds leave a person (classified by that person's own uses)", "",
          "| reason | helpful (own mean felt > 0.1) | unhelpful | never used by them |", "|---|---|---|---|"]
    for reason in ("limit", "forget", "death"):
        L.append(f"| {reason} | " + " | ".join(f"{lv.get(f'{reason}|{c}', 0):,}" for c in ("helpful", "unhelpful", "unused")) + " |")
    L.append("")

    # Q6, Q7, Q8
    rh = np.array([x for x in rhos if x == x])
    terms = {}
    for s in seeds:
        for k, v in runs[s]["terms"].items():
            terms[k] = terms.get(k, 0) + v
    tt = sum(terms.values())
    L += ["## Q6 — Are the kinds made the ones that help most?", "",
          f"Spearman correlation per world (late adult makes per kind against the kind's mean felt help): mean "
          f"{rh.mean() if len(rh) else float('nan'):.3f} over {len(rh)} worlds (min {rh.min() if len(rh) else float('nan'):.3f}, "
          f"max {rh.max() if len(rh) else float('nan'):.3f}).", "",
          "## Q7 — Offered but not chosen (adults, years 100-200)", "",
          f"Weeks: {Wm['off_n'].sum() + Wm['off_unknown'].sum():,.0f} (kind never used by anyone: "
          f"{Wm['off_unknown'].sum():,.0f}). Under-valuation (b): **{fmt(off)}**; mean felt help of the kinds offered "
          f"{fmtp(boot(Wm['off_felt'], Wm['off_n']))}.", ""]
    ob = {}
    for s in seeds:
        for k, v in runs[s]["offer_bins"].items():
            ob[k] = ob.get(k, 0) + v
    obt = sum(ob.values())
    L += ["Prior uses in these weeks: " + "; ".join(f"{k} {ob.get(k, 0) / obt if obt else float('nan'):.3f}"
                                                for k in ("0", "1-2", "3-5", "6+")) + ".", "",
          "## Q8 — Which term carries making's worth when it is offered (adults, years 100-200, all offers)", "",
          "| term | share |", "|---|---|"]
    for k in ("itemval", "part", "belief", "surprise"):
        L.append(f"| {k} | {terms.get(k, 0) / tt if tt else float('nan'):.3f} |")
    L.append("")

    # reading
    def reading(cut_u, cut_h):
        if ub[0] > cut_u and ub[1] > 0 and lt6[0] > 0.5:
            return "unlearned"
        if felt_b[0] < 0.10 and abs(ub[0]) <= cut_h:
            return "honest"
        return "mixed"
    main_r = reading(0.10, 0.05)
    L += ["## The frozen reading", "",
          f"- Under-valuation (b) {ub[0]:+.3f} (lower bound {ub[1]:+.3f}; needs > 0.10 and > 0 for 'unlearned'); "
          f"share of makes on fewer than {CUT} uses {lt6[0]:.3f} (needs > 0.5).",
          f"- Mean felt help (b) {felt_b[0]:.3f} (needs < 0.10 for 'honest', with worth within ±0.05).", "",
          f"**Reading: {main_r.upper()}.**", "",
          "Sensitivity (described, not decisive): "
          + "; ".join(f"threshold {cu:.2f} / ±{ch:.2f}: {reading(cu, ch)}" for cu, ch in ((0.05, 0.03), (0.15, 0.03),
                                                                                         (0.05, 0.05), (0.15, 0.05))) + ".", ""]
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
