"""VW1 analysis (questions.md, frozen as `VW1-frozen`). Written before data. CI1's eight guards and two co-primaries
(MP1's stages: any made part held; all made parts held at once), VW against v16, paired world bootstrap (10,000 draws,
NumPy seed 20261129).

  python experiments/VW1_value_of_wholes/analyse_vw1.py [--smoke] [--dir <output>]
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
import run_vw1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261129)
ARMS = ("c", "w", "x")
NAME = {"c": "v16", "w": "VW (the law)", "x": "sham"}
WPY = R.WPY
LY = 1000 * WPY


def pct(x):
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


def finish(L):
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


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
    m = re.search(r"code_vw1 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    if SMOKE:
        seeds = sorted(set.intersection(*[set(runs[a]) for a in ARMS if runs[a]]))
        present = len(seeds) > 0
    else:
        seeds = sorted(R.SEEDS)
        present = all(sorted(runs[a]) == seeds for a in ARMS)
    allr = [r for a in ARMS for r in runs[a].values()]
    fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
    bad = sum(r["parts_check"].get(k, 0) for r in allr for k in ("unexplained", "stage_E_without_event",
                                                                "stage_CD_without_all", "open_at_end"))
    logged = sum(r["parts_check"].get("tracked", 0) for r in allr)
    ok = bool(zero_ok and present and fps == {fp_now} and bad == 0)
    L = ["# VW1: what a valued whole needs is wanted (results)", "",
         "Frozen as `VW1-frozen`. run_vw1.py, analyse_vw1.py (written before data).", "", "## Validity", "",
         f"- Zero checks (All: PASS, `code_vw1` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(allr)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_vw1`'s: **{'yes' if fps == {fp_now} else 'NO'}**",
         f"- Part-tracking checks in every world ({logged:,} tracked parts): failures {bad}: "
         f"**{'yes' if bad == 0 else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        finish(L)
        return
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def col(a, key):
        return np.array([float(runs[a][s]["sums"].get(key, 0)) for s in seeds])

    def colf(a, fn):
        return np.array([float(fn(runs[a][s])) for s in seeds])

    def rate(a, num, den, per=1.0):
        nu, de = (col(a, num) if isinstance(num, str) else colf(a, num)), \
                 (col(a, den) if isinstance(den, str) else colf(a, den))
        with np.errstate(invalid="ignore", divide="ignore"):
            return (nu.sum() / de.sum() * per if de.sum() else float("nan")), (W @ nu) / (W @ de) * per

    def ratio(a, num, den, per=1.0):
        pa, ra = rate(a, num, den, per)
        pc, rc = rate("c", num, den, per)
        with np.errstate(invalid="ignore", divide="ignore"):
            return pa / pc if pc else float("nan"), ra / rc, pa, pc

    def diff(a, num, den, per=1.0):
        pa, ra = rate(a, num, den, per)
        pc, rc = rate("c", num, den, per)
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

    G = guards("w")
    Gx = guards("x")

    def stg(r, keys):
        return sum(r["stages"].get(f"stage_{k}", 0) for k in keys)

    def kinds(r):
        return r["stages"].get("kinds", 0)

    def share_diff(a, fnum, fden):
        nu = {b: colf(b, fnum) for b in (a, "c")}
        de = {b: colf(b, fden) for b in (a, "c")}
        with np.errstate(invalid="ignore", divide="ignore"):
            pa, pc = nu[a].sum() / de[a].sum(), nu["c"].sum() / de["c"].sum()
            bd = (W @ nu[a]) / (W @ de[a]) - (W @ nu["c"]) / (W @ de["c"])
        return pa, pc, pa - pc, pct(bd)

    co1 = {a: share_diff(a, lambda r: stg(r, "BCDE"), kinds) for a in ("w", "x")}
    co2 = {a: share_diff(a, lambda r: stg(r, "CDE"), kinds) for a in ("w", "x")}
    if G[0]:
        reading = "harm"
    elif co1["w"][3][0] > 0 and co2["w"][3][0] > 0:
        reading = "supported"
    elif co1["w"][3][0] > 0:
        reading = "partly supported"
    else:
        reading = "no harm, no effect"

    def fmt(t):
        return f"{t[0]:.4f} against v16 {t[1]:.4f}: {t[2]:+.4f} [{t[3][0]:+.4f}, {t[3][1]:+.4f}]"
    L += ["## Reading (frozen)", "",
          f"- **VW: {reading}.** Guards raised: {', '.join(G[0]) if G[0] else 'none'}.",
          f"- Co-primary 1, any made part held (MP1 stage B or beyond): VW {fmt(co1['w'])}.",
          f"- Co-primary 2, all made parts held at once (MP1 stage C or beyond): VW {fmt(co2['w'])}.",
          f"- Sham: co-primary 1 {fmt(co1['x'])}; co-primary 2 {fmt(co2['x'])}; guards raised: "
          f"{', '.join(Gx[0]) or 'none'}.", "",
          "Rule: 'supported' if no guard is raised and both co-primaries' lower bounds are above 0 (then a confirmatory "
          "run on new seeds); 'partly supported' if only co-primary 1's is; 'harm' if any guard is raised; 'no harm, no "
          "effect' otherwise.", ""]
    L += ["## Guards (VW against v16; the sham against v16 beside it)", "",
          "| guard | VW | v16 | VW vs v16 [95%] | sham vs v16 [95%] |", "|---|---|---|---|---|"]
    for (lab, pa, pc, v, lo, hi), (_, _, _, vx, lox, hix) in zip(G[1], Gx[1]):
        if "difference" in lab or "extra" in lab:
            L.append(f"| {lab} | {pa:,.4f} | {pc:,.4f} | {v:+.4f} [{lo:+.4f}, {hi:+.4f}] | {vx:+.4f} [{lox:+.4f}, {hix:+.4f}] |")
        else:
            L.append(f"| {lab} | {pa:,.4f} | {pc:,.4f} | {v:.4f} [{lo:.4f}, {hi:.4f}] | {vx:.4f} [{lox:.4f}, {hix:.4f}] |")
    L += ["", "## The stage funnel per arm (MP1's stages; new kinds needing a made part)", "",
          "| arm | kinds | A | B | C | D | E | made by a non-inventor |", "|---|---|---|---|---|---|---|---|"]
    for a in ARMS:
        k = colf(a, kinds).sum()
        cells = [f"{colf(a, lambda r, s=s: r['stages'].get(f'stage_{s}', 0)).sum() / k:.4f}" if k else "-" for s in "ABCDE"]
        mo = colf(a, lambda r: r["stages"].get("made_other", 0)).sum()
        L.append(f"| {NAME[a]} | {int(k):,} | " + " | ".join(cells) + f" | {int(mo):,} |")
    e = share_diff("w", lambda r: stg(r, "E"), kinds)
    mo = share_diff("w", lambda r: r["stages"].get("made_other", 0), kinds)
    L += ["", f"- Made again (stage E), VW − v16: {e[2]:+.4f} [{e[3][0]:+.4f}, {e[3][1]:+.4f}].",
          f"- Made by a non-inventor, VW − v16: {mo[2]:+.4f} [{mo[3][0]:+.4f}, {mo[3][1]:+.4f}].", "",
          "## By depth: co-primaries per arm", "", "| depth | arm | kinds | any part held | all parts held |",
          "|---|---|---|---|---|"]
    for d in (1, 2, 3):
        for a in ("c", "w"):
            cnt = {s: colf(a, lambda r, s=s, d=d: r["stages"].get(f"depth{d}_stage_{s}", 0)).sum() for s in "ABCDE"}
            tot = sum(cnt.values())
            if tot:
                L.append(f"| {d}{'+' if d == 3 else ''} | {NAME[a]} | {int(tot):,} | "
                         f"{sum(cnt[s] for s in 'BCDE') / tot:.4f} | {sum(cnt[s] for s in 'CDE') / tot:.4f} |")
    L += ["", "## Food-production displacement: the grown's weeks by action", "",
          "| arm | forage | gather | make | rest | talk |", "|---|---|---|---|---|---|"]
    for a in ARMS:
        gw = colf(a, lambda r: r["acts"].get("grown_weeks", 0)).sum()
        L.append(f"| {NAME[a]} | " + " | ".join(
            f"{colf(a, lambda r, k=k: r['acts'].get(f'doing_{k}', 0)).sum() / gw:.4f}" if gw else "-"
            for k in ("forage", "gather", "make", "rest", "talk")) + " |")
    L += ["", "## Make options offered: a part of a valued whole (one level) or only deeper", "",
          "| arm | make options | a part one level down | only deeper |", "|---|---|---|---|"]
    for a in ARMS:
        mk = colf(a, lambda r: r["mech"].get("make_offers", 0)).sum()
        l1 = colf(a, lambda r: r["mech"].get("offer_part_level1", 0)).sum()
        dp = colf(a, lambda r: r["mech"].get("offer_part_deeper_only", 0)).sum()
        L.append(f"| {NAME[a]} | {int(mk):,} | {l1 / mk:.4f} | {dp / mk:.4f} |" if mk else f"| {NAME[a]} | 0 | - | - |")
    L.append("")
    finish(L)


if __name__ == "__main__":
    main()
