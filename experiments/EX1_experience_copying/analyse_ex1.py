"""EX1 analysis, written before any data (questions.md, frozen as `EX1-frozen`; operational note 1).

  python experiments/EX1_habit_copying/analyse_ex1.py            # writes results.md
  python experiments/EX1_habit_copying/analyse_ex1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_ex1 import ARMS, SEEDS, SUMS  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261028)
COMMON = ("forage", "give", "talk", "gather")
SHOW = ("make", "forage", "give", "talk", "gather")
J = {k: i for i, k in enumerate(SUMS)}
LATE = 2


def sums(r, acts, era=None):
    era = LATE if era is None else era
    out = np.zeros(len(SUMS))
    for a in acts:
        out += np.array(r["cells"].get(f"{era}|{a}", [0.0] * len(SUMS)))
    return out


def bias(s):
    with np.errstate(divide="ignore", invalid="ignore"):
        return (s[..., J["q"]] - s[..., J["G"]]) / s[..., J["n"]]


def meanG(s):
    with np.errstate(divide="ignore", invalid="ignore"):
        return s[..., J["G"]] / s[..., J["n"]]


def pop(r):
    rows = [row for row in r["census"] if 100 <= row[0] < 200]
    return (sum(row[1] for row in rows), len(rows))


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
    L = ["# EX1 — Experience telling instead of habit copying. Results", "",
         "Frozen as `EX1-frozen` (operational note 1). run_ex1.py, analyse_ex1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)} of {len(SEEDS) * len(ARMS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_ex1`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- TD replay exact in every arm (mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    seeds = sorted(set(runs["v"]) & set(runs["e"]) & set(runs["x"]))
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])

    def arr(arm, acts):
        return np.stack([sums(runs[arm][s], acts) for s in seeds])

    def paired(fn, a, b, acts):
        A_, B_ = arr(a, acts), arr(b, acts)
        point = fn(A_.sum(0)) - fn(B_.sum(0))
        reps = fn(W @ A_) - fn(W @ B_)
        reps = reps[np.isfinite(reps)]
        lo, hi = np.percentile(reps, [2.5, 97.5]) if len(reps) else (float("nan"), float("nan"))
        return point, lo, hi

    allacts = runs["v"][seeds[0]]["actions"]
    L += [f"Paired seeds: {n}. Extinct by year 200: v {sum(runs['v'][s]['extinct'] for s in seeds)}, "
          f"e {sum(runs['e'][s]['extinct'] for s in seeds)}, x {sum(runs['x'][s]['extinct'] for s in seeds)}.", ""]
    L += ["## Calibration, years 100-200 (adults; bias = mean q − mean realised G)", "",
          "| measure | v (v8) | e (experience) | x (sham) | improvement v − e [95%] | sham: v − x [95%] |",
          "|---|---|---|---|---|---|"]
    rows = [("common actions' bias", COMMON, bias)] + [(f"{a} bias", (a,), bias) for a in SHOW] + \
           [("mean realised G, all actions", tuple(allacts), meanG)]
    res = {}
    for name, acts, fn in rows:
        vw, vs, vx = (fn(arr(a, acts).sum(0)) for a in ("v", "e", "x"))
        d = paired(fn, "v", "e", acts)
        dx = paired(fn, "v", "x", acts)
        res[name] = (vw, vs, vx, d)
        L.append(f"| {name} | {vw:+.4f} | {vs:+.4f} | {vx:+.4f} | {d[0]:+.4f} [{d[1]:+.4f}, {d[2]:+.4f}] | "
                 f"{dx[0]:+.4f} [{dx[1]:+.4f}, {dx[2]:+.4f}] |")
    L.append("")
    vw, vs, _, d = res["common actions' bias"]
    p_ok = d[0] >= 0.10 and d[1] > 0
    g = paired(meanG, "e", "v", tuple(allacts))
    h_ok = g[1] > -0.05
    ext_w = sum(runs["v"][s]["extinct"] for s in seeds)
    ext_s = sum(runs["e"][s]["extinct"] for s in seeds)
    pw = sum(pop(runs["v"][s])[0] for s in seeds) / max(sum(pop(runs["v"][s])[1] for s in seeds), 1)
    ps = sum(pop(runs["e"][s])[0] for s in seeds) / max(sum(pop(runs["e"][s])[1] for s in seeds), 1)
    px = sum(pop(runs["x"][s])[0] for s in seeds) / max(sum(pop(runs["x"][s])[1] for s in seeds), 1)
    flag_ext = ext_s - ext_w >= 3
    flag_pop = ps < 0.90 * pw
    L += ["## The frozen decision rule", "",
          f"- **P (calibration):** improvement in the common actions' bias, v − e = {d[0]:+.4f} [{d[1]:+.4f}, {d[2]:+.4f}]; "
          f"at least 0.10 with the lower bound above 0: **{'supports' if p_ok else 'does not support'}**",
          f"- **H (realised return):** e − v = {g[0]:+.4f} [{g[1]:+.4f}, {g[2]:+.4f}]; lower bound above −0.05: "
          f"**{'no harm' if h_ok else 'HARM'}**",
          f"- **F (flags):** extinct e {ext_s} vs v {ext_w} ({'FLAG' if flag_ext else 'no flag'}); mean population years "
          f"100-200 e {ps:.1f} vs v {pw:.1f} (ratio {ps / pw if pw else float("nan"):.3f}; {'FLAG' if flag_pop else 'no flag'}); sham {px:.1f}",
          f"- **D:** e's common bias {vs:+.3f} {'inside' if abs(vs) <= 0.10 else 'outside'} ±0.10 (reported, not a gate)", "",
          f"**{'The change is supported' if (p_ok and h_ok) else 'The change is not supported'} by the frozen rule"
          f"{'; flagged, so adoption is not recommended' if (flag_ext or flag_pop) else ''}.** Adoption is left to the creator.", ""]

    # Described: making, things held, told experiences (years 100-200)
    def cen(arm, k):
        i = runs[arm][seeds[0]]["census_fields"].index(k)
        return np.array([float(sum(row[i] for row in runs[arm][s]["census"] if 100 <= row[0] < 200)) for s in seeds])

    def dpair(num, den, a, b="v"):
        Na, Da, Nb, Db = cen(a, num), cen(a, den), cen(b, num), cen(b, den)
        point = Na.sum() / Da.sum() - Nb.sum() / Db.sum()
        with np.errstate(divide="ignore", invalid="ignore"):
            reps = (W @ Na) / (W @ Da) - (W @ Nb) / (W @ Db)
        reps = reps[np.isfinite(reps)]
        lo, hi = np.percentile(reps, [2.5, 97.5]) if len(reps) else (float("nan"), float("nan"))
        return point, lo, hi
    L += ["## Described: making and things held (years 100-200, per adult-year)", "",
          "| measure | v (v8) | e − v [95%] | sham − v [95%] |", "|---|---|---|---|"]
    for name, num in (("making events", "makes"), ("made things held", "items_adults")):
        ve, vx_ = dpair(num, "adults", "e"), dpair(num, "adults", "x")
        L.append(f"| {name} | {cen('v', num).sum() / cen('v', 'adults').sum():.4f} | {ve[0]:+.4f} [{ve[1]:+.4f}, "
                 f"{ve[2]:+.4f}] | {vx_[0]:+.4f} [{vx_[1]:+.4f}, {vx_[2]:+.4f}] |")
    told = sum(runs["e"][s]["told"].get("told", 0) for s in seeds)
    known = sum(runs["e"][s]["told"].get("told_known_situation", 0) for s in seeds)
    L += ["", f"Told experiences in arm e (all years): {told:,}; about a situation the listener had already learned in: "
              f"{known / told if told else float('nan'):.3f}.", ""]
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
