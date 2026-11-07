"""LW1 analysis, written before any data (questions.md, frozen as `LW1-frozen`).

  python experiments/LW1_learners_wish/analyse_lw1.py                      # writes results.md
  python experiments/LW1_learners_wish/analyse_lw1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_lw1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261109)
ARMS = ("c", "w", "x")
NAME = {"c": "v15", "w": "LW", "x": "sham"}
WPY = R.WPY
LY = 1000 * WPY


def pct(x):
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {a: {} for a in ARMS}
    for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json"))):
        r = json.load(open(f))
        if r["arm"] in runs:
            runs[r["arm"]][r["seed"]] = r
    zero = ""
    for name in ("zero_cloud.log", "zero_local.log"):
        if (HERE / name).exists():
            zero = (HERE / name).read_text(encoding="utf-8", errors="replace")
            break
    R.base.setup(R.CODE)
    fp_now = R.base.fingerprint(R.CODE)
    m = re.search(r"code_lw1 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    if SMOKE:
        seeds = sorted(set.intersection(*[set(runs[a]) for a in ARMS if runs[a]]))
        present = len(seeds) > 0
    else:
        seeds = sorted(R.SEEDS)
        present = all(sorted(runs[a]) == seeds for a in ARMS)
    allr = [r for a in ARMS for r in runs[a].values()]
    fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
    ok = bool(zero_ok and present and fps == {fp_now})
    L = ["# LW1: a learner's wish for the part they could not follow (results)", "",
         "Frozen as `LW1-frozen`. run_lw1.py, analyse_lw1.py (written before data).", "", "## Validity", "",
         f"- Zero checks (All: PASS, `code_lw1` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(allr)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_lw1`'s: **{'yes' if fps == {fp_now} else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        finish(L)
        return
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def col(a, key, top=False):
        return np.array([float(runs[a][s].get(key, 0) if top else runs[a][s]["sums"].get(key, 0)) for s in seeds])

    def rate(a, num, den, per=1.0, top=False):
        nu, de = col(a, num, top), col(a, den, top)
        with np.errstate(invalid="ignore", divide="ignore"):
            return (nu.sum() / de.sum() * per if de.sum() else float("nan")), (W @ nu) / (W @ de) * per

    def ratio(a, num, den, per=1.0):
        pa, ra = rate(a, num, den, per)
        pc, rc = rate("c", num, den, per)
        with np.errstate(invalid="ignore", divide="ignore"):
            return pa / pc if pc else float("nan"), ra / rc, pa, pc

    def diff(a, num, den, per=1.0, top=False):
        pa, ra = rate(a, num, den, per, top)
        pc, rc = rate("c", num, den, per, top)
        return pa - pc, ra - rc, pa, pc

    ext = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in ARMS}

    def guards(a):
        out, rows = [], []
        r, rr, pa, pc = ratio(a, "death_starvation", "living_weeks", LY)
        lo, hi = pct(rr)
        rows.append(("starvation deaths per 1,000 living-years (ratio)", pa, pc, r, lo, hi))
        if r > 1.25 and lo > 1:
            out.append("starvation")
        d, dr, pa, pc = diff(a, "death_killed", "living_weeks", LY)
        lo, hi = pct(dr)
        rows.append(("killing deaths per 1,000 living-years (difference)", pa, pc, d, lo, hi))
        if d > 0.05 and lo > 0:
            out.append("killing")
        d, dr, pa, pc = diff(a, "census_health", "census_adults")
        lo, hi = pct(dr)
        rows.append(("adult health, mean (difference)", pa, pc, d, lo, hi))
        if d < -5 and hi < 0:
            out.append("adult health")
        lw_a, lw_c = col(a, "living_weeks"), col("c", "living_weeks")
        with np.errstate(invalid="ignore", divide="ignore"):
            r, rr = lw_a.sum() / lw_c.sum(), (W @ lw_a) / (W @ lw_c)
        lo, hi = pct(rr)
        rows.append(("living-weeks (ratio)", lw_a.sum(), lw_c.sum(), r, lo, hi))
        if r < 0.90 and hi < 1:
            out.append("population")
        rows.append(("extinct worlds (extra)", ext[a], ext["c"], ext[a] - ext["c"], float("nan"), float("nan")))
        if ext[a] - ext["c"] >= 3:
            out.append("extinction")
        r, rr, pa, pc = ratio(a, "child_deaths", "child_weeks", LY)
        lo, hi = pct(rr)
        rows.append(("child deaths per 1,000 child-years (ratio)", pa, pc, r, lo, hi))
        if r > 1.25 and lo > 1 and pa - pc >= 3:
            out.append("child deaths")
        r, rr, pa, pc = ratio(a, "child_death_starvation", "child_weeks", LY)
        lo, hi = pct(rr)
        rows.append(("child starvation deaths per 1,000 child-years (ratio)", pa, pc, r, lo, hi))
        if r > 1.25 and lo > 1:
            out.append("child starvation")
        r, rr, pa, pc = ratio(a, "gifts_kin_children", "adult_weeks", 1000)
        lo, hi = pct(rr)
        rows.append(("food gifts to kin's children per 1,000 adult-weeks (ratio)", pa, pc, r, lo, hi))
        if r < 0.80 and hi < 1:
            out.append("gifts to kin's children")
        return out, rows

    def fmtd(t):
        lo, hi = pct(t[1])
        return f"{t[0]:+.4f} [{lo:+.4f}, {hi:+.4f}]"

    co = {a: diff(a, "lw_learned", "lw_kinds", top=True) for a in ("w", "x")}
    G = guards("w")
    passes = pct(co["w"][1])[0] > 0
    reading = "harm" if G[0] else ("supported" if passes else "no harm, no effect")
    L += ["## Reading (frozen)", "",
          f"- **LW: {reading}.** Guards raised: {', '.join(G[0]) if G[0] else 'none'}. Co-primary (invented kinds learned "
          f"by a non-inventor within 5 years): LW {co['w'][2]:.4f} against v15 {co['w'][3]:.4f}: {fmtd(co['w'])}.",
          f"- Sham: {co['x'][2]:.4f} against v15: {fmtd(co['x'])}; guards raised: {', '.join(guards('x')[0]) or 'none'}.",
          "", "Rule: \"supported\" if no guard is raised and the co-primary's lower bound is above 0; \"harm\" if any guard is "
          "raised; \"no harm, no effect\" otherwise. A supported reading goes to a confirmatory run on new seeds.", ""]
    L += ["## Co-primary and secondary", "", "| arm | kinds | learned by a non-inventor | share | made by a non-inventor | share |"
          " failed pairs | learned a missing part | share |", "|---|---|---|---|---|---|---|---|---|"]
    for a in ARMS:
        k = col(a, "lw_kinds", True).sum()
        le = col(a, "lw_learned", True).sum()
        mo = col(a, "lw_made_other", True).sum()
        pr = col(a, "lw_pairs", True).sum()
        gp = col(a, "lw_pairs_got_part", True).sum()
        L.append(f"| {NAME[a]} | {int(k):,} | {int(le):,} | {le / k if k else float('nan'):.4f} | {int(mo):,} | "
                 f"{mo / k if k else float('nan'):.4f} | {int(pr):,} | {int(gp):,} | {gp / pr if pr else float('nan'):.4f} |")
    L += ["", f"- Made by a non-inventor, LW − v15: {fmtd(diff('w', 'lw_made_other', 'lw_kinds', top=True))}.",
          f"- Failed pairs that learned a missing part within 5 years, LW − v15: "
          f"{fmtd(diff('w', 'lw_pairs_got_part', 'lw_pairs', top=True))}.", ""]
    L += ["## Guards (LW against v15)", "", "| guard | LW | v15 | ratio or difference [95%] |", "|---|---|---|---|"]
    for lab, pa, pc, v, lo, hi in G[1]:
        L.append(f"| {lab} | {pa:,.4f} | {pc:,.4f} | {v:+.4f} [{lo:+.4f}, {hi:+.4f}] |" if "difference" in lab or "extra" in lab
                 else f"| {lab} | {pa:,.4f} | {pc:,.4f} | {v:.4f} [{lo:.4f}, {hi:.4f}] |")
    wish = {a: {} for a in ARMS}
    for a in ARMS:
        for s in seeds:
            for k, v in runs[a][s].get("wish", {}).items():
                wish[a][k] = wish[a].get(k, 0) + v
    L += ["", "## Described", "", f"- Wishes in LW: {wish['w']} (formed; met, a lesson shown for a wish; ended known or "
          "expired).", "", "| arm | grown weeks foraging share | grown weeks talking share |", "|---|---|---|"]
    for a in ARMS:
        aw = col(a, "adult_weeks").sum() or 1
        L.append(f"| {NAME[a]} | {col(a, 'grown_weeks_forage').sum() / aw:.4f} | {col(a, 'grown_weeks_talk').sum() / aw:.4f} |")
    L.append("")
    finish(L)


def finish(L):
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
