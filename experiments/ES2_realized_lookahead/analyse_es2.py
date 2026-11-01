"""ES2 analysis, written before any data (questions.md, frozen as `ES2-frozen`; operational note 1).

  python experiments/ES2_realized_lookahead/analyse_es2.py            # writes results.md
  python experiments/ES2_realized_lookahead/analyse_es2.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_es2 import ARMS, SEEDS, WPY  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261031)
NAME = {"c": "v11", "r": "r (realized look-ahead)", "x": "sham"}
SHOW = ("forage", "gather", "talk", "give", "rest", "explore", "play", "make", "hunt", "care", "put", "take")
MIN_CELL = 100                              # ranking: actions with at least this many closed updates in a situation
MIN_ACT = 10_000                            # per-action guard: actions with at least this many closed updates per arm


def rank(x):
    x = np.asarray(x, float)
    o = np.argsort(x, kind="mergesort")
    r = np.empty(len(x))
    r[o] = np.arange(len(x))
    for v in np.unique(x):
        m = x == v
        r[m] = r[m].mean()
    return r


def spearman(a, b):
    if len(a) < 3 or np.std(a) == 0 or np.std(b) == 0:
        return None
    return float(np.corrcoef(rank(a), rank(b))[0, 1])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {a: {} for a in ARMS}
    for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json"))):
        r = json.load(open(f))
        runs[r["arm"]][r["seed"]] = r
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    present = all(sorted(runs[a]) == sorted(SEEDS) for a in ARMS)
    fps = {r["code_hash"] for a in ARMS for r in runs[a].values()} | \
          {r["code_hash_after"] for a in ARMS for r in runs[a].values()}
    mism = sum(sum(r["mismatch"].values()) for a in ARMS for r in runs[a].values())
    ok = "All: PASS" in zero and present and len(fps) == 1 and mism == 0
    L = ["# ES2 — Do minds learn more accurately when they look ahead by their real next choice? Results", "",
         "Frozen as `ES2-frozen` (operational note 1). run_es2.py, analyse_es2.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)} of {len(SEEDS) * len(ARMS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_es2`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Every habit update replays under its arm's rule (mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**",
         "", f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    seeds = sorted(set(runs["c"]) & set(runs["r"]) & set(runs["x"]))
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])
    F = ["n", "sum_abs", "sum_signed", "censored", "sum_q", "sum_G"]

    def cal(a, field, act=None):
        j = F.index(field)
        return np.array([float(sum(v[j] for k, v in runs[a][s]["cal"].items()
                                   if act is None or k.split("|", 1)[1] == act)) for s in seeds])

    def col(a, k):
        return np.array([float(runs[a][s]["sums"].get(k, 0.0)) for s in seeds])

    def ratio(num, den):
        point = num.sum() / den.sum() if den.sum() else float("nan")
        with np.errstate(invalid="ignore", divide="ignore"):
            reps = (W @ num) / (W @ den)
        return point, reps

    def diff(num, den, a, b="c"):
        pa, ra = ratio(num[a], den[a])
        pb, rb = ratio(num[b], den[b])
        lo, hi = np.nanpercentile(ra - rb, [2.5, 97.5])
        return pa - pb, lo, hi

    def rat(num, den, a, b="c"):
        pa, ra = ratio(num[a], den[a])
        pb, rb = ratio(num[b], den[b])
        with np.errstate(invalid="ignore", divide="ignore"):
            lo, hi = np.nanpercentile(ra / rb, [2.5, 97.5])
        return pa / pb if pb else float("nan"), lo, hi

    ext = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in ARMS}
    L += [f"Paired seeds: {n}. Extinct: v11 {ext['c']}, r {ext['r']}, sham {ext['x']}.", ""]

    ABS = {a: cal(a, "sum_abs") for a in ARMS}
    NN = {a: cal(a, "n") for a in ARMS}
    dr, dx = diff(ABS, NN, "r"), diff(ABS, NN, "x")
    L += ["## Primary — calibration error across all actions: mean |q - G| (habit updates started in years 100-200)", "",
          "| arm | mean abs(q - G) | updates closed | censored at death |", "|---|---|---|---|"]
    for a in ARMS:
        L.append(f"| {NAME[a]} | {ratio(ABS[a], NN[a])[0]:.4f} | {NN[a].sum():,.0f} | {cal(a, 'censored').sum():,.0f} |")
    L += ["", f"**r - v11: {dr[0]:+.4f} [{dr[1]:+.4f}, {dr[2]:+.4f}]**; sham - v11: {dx[0]:+.4f} [{dx[1]:+.4f}, {dx[2]:+.4f}].", ""]

    # frozen secondary: ranking accuracy within situations
    def ranking(a, s):
        cells = defaultdict(list)
        for k, v in runs[a][s]["cal"].items():
            ctx, act = k.split("|", 1)
            if v[0] >= MIN_CELL:
                cells[ctx].append((v[4] / v[0], v[5] / v[0]))
        rs = [spearman([x[0] for x in c], [x[1] for x in c]) for c in cells.values() if len(c) >= 3]
        rs = [x for x in rs if x is not None]
        return float(np.mean(rs)) if rs else float("nan")
    RK = {a: np.array([ranking(a, s) for s in seeds]) for a in ARMS}
    good = ~np.isnan(RK["c"]) & ~np.isnan(RK["r"])
    d = RK["r"][good] - RK["c"][good]
    if good.sum():
        bs = [d[RNG.integers(0, len(d), len(d))].mean() for _ in range(REPS)]
        lo, hi = np.percentile(bs, [2.5, 97.5])
    else:
        lo = hi = float("nan")
    L += ["## Frozen secondary — ranking accuracy (Spearman of mean q against mean G across actions, within a situation; "
          "averaged per world)", "", "| arm | mean over worlds |", "|---|---|"]
    for a in ARMS:
        L.append(f"| {NAME[a]} | {np.nanmean(RK[a]):.3f} |")
    L += ["", f"r - v11 (paired, worlds with both): {d.mean() if len(d) else float('nan'):+.3f} [{lo:+.3f}, {hi:+.3f}] "
              f"over {int(good.sum())} worlds.", ""]

    L += ["## Secondary — signed bias q - G by action (years 100-200)", "", "| action | v11 | r | sham |", "|---|---|---|---|"]
    for act in SHOW:
        cells = []
        for a in ARMS:
            nn, ss = cal(a, "n", act), cal(a, "sum_signed", act)
            cells.append(f"{ss.sum() / nn.sum():+.3f}" if nn.sum() else "-")
        L.append(f"| {act} | " + " | ".join(cells) + " |")
    L.append("")
    ay = {a: col(a, "adult_weeks") / WPY for a in ARMS}
    mk = {a: col(a, "adult_makes") for a in ARMS}
    fw = {a: col(a, "food_with") for a in ARMS}
    tool = {a: col(a, "food_with") - col(a, "food_without") for a in ARMS}
    L += ["| secondary (years 100-200) | v11 | r | sham | r ÷ v11 [95%] |", "|---|---|---|---|---|"]
    for label, num, den, dd in (("makes per adult-year", mk, ay, 3), ("foraged food per adult-year", fw, ay, 1),
                                ("tools' share of foraged food", tool, fw, 4)):
        q = rat(num, den, "r")
        L.append(f"| {label} | " + " | ".join(f"{ratio(num[a], den[a])[0]:.{dd}f}" for a in ARMS) +
                 f" | {q[0]:.3f} [{q[1]:.3f}, {q[2]:.3f}] |")
    inst = {a: (sum(runs[a][s]["instinct"][1] for s in seeds) / max(1, sum(runs[a][s]["instinct"][0] for s in seeds)))
            for a in ARMS}
    L += ["", "Described (Gemini): instinct share of the options' score variance, Var(score - 0.6 q) / Var(score), on "
              "every 20th decision: " + "; ".join(f"{NAME[a]} {inst[a]:.3f}" for a in ARMS) + ".", ""]

    # guards
    flags = {}
    worst = []
    for act in sorted({k.split("|", 1)[1] for a in ARMS for s in seeds for k in runs[a][s]["cal"]}):
        nc, nr = cal("c", "n", act), cal("r", "n", act)
        if nc.sum() >= MIN_ACT and nr.sum() >= MIN_ACT:
            rise = cal("r", "sum_abs", act).sum() / nr.sum() - cal("c", "sum_abs", act).sum() / nc.sum()
            worst.append((rise, act))
    worst.sort(reverse=True)
    flags["calibration by action"] = bool(worst) and worst[0][0] > 0.10
    upd = {a: col(a, "updates") for a in ARMS}
    drop = {a: col(a, "held_dropped") for a in ARMS}
    dshare = {a: drop[a].sum() / upd[a].sum() if upd[a].sum() else 0.0 for a in ARMS}
    flags["uncompleted updates"] = any(v >= 0.01 for v in dshare.values())
    pop = {a: col(a, "living_weeks") for a in ARMS}
    span = {a: np.full(n, 100.0 * WPY) for a in ARMS}
    rp, rpx = rat(pop, span, "r"), rat(pop, span, "x")
    flags["population"] = rp[0] < 0.90 and rp[2] < 1.0
    ad = {a: col(a, "adult_deaths") * 1000.0 for a in ARMS}
    dd_, ddx = diff(ad, ay, "r"), diff(ad, ay, "x")
    base = ratio(ad["c"], ay["c"])[0]
    flags["adult deaths"] = dd_[0] > 0 and dd_[1] > 0 and dd_[0] > 0.10 * base
    flags["extinctions"] = ext["r"] - ext["c"] >= 3
    L += ["## Guards", "", "| guard | r against v11 [95%] | sham against v11 | raised |", "|---|---|---|---|",
          f"| calibration by action (largest rise in mean abs(q - G), actions with >= {MIN_ACT:,} updates; > 0.10) | "
          f"{worst[0][1] if worst else '-'} {worst[0][0] if worst else float('nan'):+.3f} | | "
          f"{'**RAISED**' if flags['calibration by action'] else 'no'} |",
          f"| uncompleted (dropped) held updates (>= 1% of updates in any arm) | r {dshare['r']:.5f} | v11 {dshare['c']:.5f} | "
          f"{'**RAISED**' if flags['uncompleted updates'] else 'no'} |",
          f"| population (r ÷ v11 < 0.90, upper < 1) | {rp[0]:.3f} [{rp[1]:.3f}, {rp[2]:.3f}] | {rpx[0]:.3f} | "
          f"{'**RAISED**' if flags['population'] else 'no'} |",
          f"| adult deaths per 1,000 adult-years (r − v11 > 0, lower > 0, > 10% of v11's {base:.1f}) | "
          f"{dd_[0]:+.2f} [{dd_[1]:+.2f}, {dd_[2]:+.2f}] | {ddx[0]:+.2f} | {'**RAISED**' if flags['adult deaths'] else 'no'} |",
          f"| extinctions (r − v11 ≥ 3) | {ext['r'] - ext['c']:+d} | {ext['x'] - ext['c']:+d} | "
          f"{'**RAISED**' if flags['extinctions'] else 'no'} |", ""]

    supported = dr[0] < 0 and dr[2] < 0 and dr[0] < dx[0] and not any(flags.values())
    L += ["## The frozen decision", "",
          f"- r - v11 {dr[0]:+.4f} [{dr[1]:+.4f}, {dr[2]:+.4f}] (< 0 with upper < 0); sham - v11 {dx[0]:+.4f} (r must be "
          f"below it); guard flags: {', '.join(k for k, v in flags.items() if v) or 'none'}.", "",
          f"**{'SUPPORTED' if supported else 'NOT SUPPORTED'}.** (A test in a copy; making and ranking are reported, not "
          "decisive; adoption only by the safe path in CLAUDE.md, with a confirmatory run.)", ""]
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
