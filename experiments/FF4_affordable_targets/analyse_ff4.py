"""FF4 analysis (questions.md, frozen as `FF4-frozen`). Written before data. A check for harm only: CI1's eight guards,
f against v15, paired world bootstrap (10,000 draws, NumPy seed 20261123); EG1's measures re-measured per arm.

  python experiments/FF4_affordable_targets/analyse_ff4.py [--smoke] [--dir <output>]
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
import run_ff4 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261123)
ARMS = ("c", "f", "x")
NAME = {"c": "v15", "f": "f (the fix)", "x": "sham"}
WPY = R.WPY
LY = 1000 * WPY
BANDS = [b[2] for b in R.BANDS]


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
    m = re.search(r"code_ff4 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    if SMOKE:
        seeds = sorted(set.intersection(*[set(runs[a]) for a in ARMS if runs[a]]))
        present = len(seeds) > 0
    else:
        seeds = sorted(R.SEEDS)
        present = all(sorted(runs[a]) == seeds for a in ARMS)
    allr = [r for a in ARMS for r in runs[a].values()]
    fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
    bad = sum(r["check"].get(k, 0) for r in allr for k in ("forage_mismatch", "hunt_mismatch", "gather_mismatch",
                                                          "missing_entry"))
    logged = sum(r["check"].get("weeks", 0) for r in allr)
    ok = bool(zero_ok and present and fps == {fp_now} and bad == 0)
    L = ["# FF4: a whole action dropped because one target is too far (results)", "",
         "Frozen as `FF4-frozen`. run_ff4.py, analyse_ff4.py (written before data).", "", "## Validity", "",
         f"- Zero checks (All: PASS, `code_ff4` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(allr)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_ff4`'s: **{'yes' if fps == {fp_now} else 'NO'}**",
         f"- Hook check in every world (forage, hunt and gather offered exactly when the log predicts; {logged:,} "
         f"person-weeks aged 6+): mismatches {bad}: **{'yes' if bad == 0 else 'NO'}**", "",
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

    G = guards("f")
    reading = "harm: investigate" if G[0] else "no harm"
    L += ["## Reading (frozen)", "",
          f"- **f: {reading}.** Guards raised: {', '.join(G[0]) if G[0] else 'none'}.",
          f"- Sham: guards raised: {', '.join(guards('x')[0]) or 'none'}.", "",
          "Rule: \"no harm\" if no guard is raised (f is then adopted as nature v16 by the safe path; a fault fix has no "
          "confirmatory run); otherwise \"harm: investigate\".", ""]
    L += ["## Guards (f against v15; the sham against v15 beside it)", "",
          "| guard | f | v15 | f vs v15 [95%] | sham vs v15 [95%] |", "|---|---|---|---|---|"]
    Gx = guards("x")
    for (lab, pa, pc, v, lo, hi), (_, _, _, vx, lox, hix) in zip(G[1], Gx[1]):
        if "difference" in lab or "extra" in lab:
            L.append(f"| {lab} | {pa:,.4f} | {pc:,.4f} | {v:+.4f} [{lo:+.4f}, {hi:+.4f}] | {vx:+.4f} [{lox:+.4f}, {hix:+.4f}] |")
        else:
            L.append(f"| {lab} | {pa:,.4f} | {pc:,.4f} | {v:.4f} [{lo:.4f}, {hi:.4f}] | {vx:.4f} [{lox:.4f}, {hix:.4f}] |")

    # Described, with the flag rule: a ratio f / v15 outside [0.8, 1.25] with its interval wholly outside 1.
    def eg(r, part, starving=1, band=None, sex=None):
        t = 0
        for k, v in r["eg"].items():
            b, s, st = k.split("|")
            if int(st) != starving or (band and b != band) or (sex and s != sex):
                continue
            t += v.get(part, 0)
        return t

    flags = []

    def described(label, num, den, per=1.0):
        vals = {a: rate(a, num, den, per)[0] for a in ARMS}
        r, rr, _, _ = ratio("f", num, den, per)
        lo, hi = pct(rr)
        rx, rrx, _, _ = ratio("x", num, den, per)
        lox, hix = pct(rrx)
        flag = (r < 0.8 or r > 1.25) and (lo > 1 or hi < 1)
        if flag:
            flags.append(label)
        return (f"| {label} | {vals['c']:.4f} | {vals['f']:.4f} | {vals['x']:.4f} | {r:.4f} [{lo:.4f}, {hi:.4f}] | "
                f"{rx:.4f} [{lox:.4f}, {hix:.4f}] | {'FLAG' if flag else ''} |")

    L += ["", "## Described (not decisive; flagged if f / v15 is outside [0.8, 1.25] with its interval wholly outside 1)", "",
          "| measure | v15 | f | sham | f / v15 [95%] | sham / v15 [95%] | |", "|---|---|---|---|---|---|---|"]
    L.append(described("EG1's P: starving weeks blocked by energy alone", lambda r: eg(r, "c"), lambda r: eg(r, "weeks")))
    for part, lab in (("a", "starving weeks: food offered and chosen"), ("b", "starving weeks: offered, not chosen"),
                      ("d", "starving weeks: no food feasible")):
        L.append(described(lab, lambda r, part=part: eg(r, part), lambda r: eg(r, "weeks")))
    L.append(described("non-starving weeks blocked by energy alone", lambda r: eg(r, "c", 0), lambda r: eg(r, "weeks", 0)))
    for sx, sl in (("F", "women"), ("M", "men")):
        L.append(described(f"P, {sl} 30-49", lambda r, sx=sx: eg(r, "c", 1, "30-49", sx),
                           lambda r, sx=sx: eg(r, "weeks", 1, "30-49", sx)))
    L.append(described("starvation deaths at 6+ per 1,000 living-years at 6+",
                       lambda r: r["deaths6"].get("starvation_6plus", 0), lambda r: r["deaths6"].get("living_weeks_6plus", 0), LY))
    L.append(described("starvation deaths at 6+ with a blocked starving week in their last 4 decisions (share)",
                       lambda r: r["deaths6"].get("starvation_blocked_last4", 0), lambda r: r["deaths6"].get("starvation_6plus", 0)))
    for act in ("forage", "hunt", "gather", "rest", "make", "talk"):
        L.append(described(f"grown weeks: {act} (share)", lambda r, act=act: r["grown_acts"].get(act, 0),
                           lambda r: sum(r["grown_acts"].values())))
    L += ["", f"Flagged: {', '.join(flags) if flags else 'none'}. A flag asks for a read-only explanation before adoption; "
          "it is not a stop.", ""]

    L += ["## The fix at work (weeks where the best target was unaffordable but another was affordable; counted years)", "",
          "| arm | forage | of them starving | hunt | gather | logged person-weeks aged 6+ |", "|---|---|---|---|---|---|"]
    for a in ARMS:
        fx = {}
        for s in seeds:
            for k, v in runs[a][s]["fix"].items():
                fx[k] = fx.get(k, 0) + v
        wk = sum(eg(runs[a][s], "weeks", 1) + eg(runs[a][s], "weeks", 0) for s in seeds)
        L.append(f"| {NAME[a]} | {fx.get('forage', 0):,} | {fx.get('forage_starving', 0):,} | {fx.get('hunt', 0):,} | "
                 f"{fx.get('gather', 0):,} | {wk:,} |")
    L += ["", "In v15 and the sham these are the weeks the fix would have acted in; in f, the weeks it did.", ""]

    L += ["## EG1's split by age band and sex, starving weeks (share blocked by energy alone)", "",
          "| ages | v15 women | v15 men | f women | f men |", "|---|---|---|---|---|"]
    for b in BANDS:
        cells = []
        for a in ("c", "f"):
            for sx in ("F", "M"):
                c = sum(eg(runs[a][s], "c", 1, b, sx) for s in seeds)
                wks = sum(eg(runs[a][s], "weeks", 1, b, sx) for s in seeds)
                cells.append(f"{c / wks:.3f} ({wks:,})" if wks else "-")
        L.append(f"| {b} | " + " | ".join(cells) + " |")
    L.append("")
    finish(L)


if __name__ == "__main__":
    main()
