"""BN1 analysis, written before any data (questions.md, frozen as `BN1-frozen`).

The zero checks run on GitHub while the creator is using the PC (light use); their record is `zero_cloud.log` (saved
from the cloud zero job's log), or `zero_local.log` when run locally.

  python experiments/BN1_born_without_learned_content/analyse_bn1.py            # writes results.md
  python experiments/BN1_born_without_learned_content/analyse_bn1.py --smoke --dir <folder>
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
import run_bn1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261102)
ARMS = ("c", "z", "x", "s")
NAME = {"c": "v11", "z": "z (born at 0)", "x": "x (scrambled)", "s": "sham"}
MARGIN, SHAM_BAND, MIN_CELL, MIN_COVER = 0.02, 0.01, 30, 0.80
WPY = R.WPY


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {a: {} for a in ("c", "z", "x", "s", "r")}
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
    m = re.search(r"code_bn1 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    if SMOKE:
        seeds = sorted(set.intersection(*[set(runs[a]) for a in ARMS]))
        present = len(seeds) > 0 and len(runs["r"]) > 0
    else:
        seeds = sorted(R.SEEDS)
        present = all(sorted(runs[a]) == seeds for a in ARMS) and sorted(runs["r"]) == sorted(R.REF_SEEDS)
    allr = [r for a in runs for r in runs[a].values()]
    fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
    mism = sum(sum(r["mismatch"].values()) for r in allr)
    ok = bool(zero_ok and present and fps == {fp_now} and mism == 0)
    L = ["# BN1 — Born without learned content: results", "",
         "Frozen as `BN1-frozen`. run_bn1.py, analyse_bn1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks (All: PASS, same `code_bn1` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)} arm worlds, {len(runs['r'])} reference worlds): "
         f"**{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_bn1`'s: **{'yes' if fps == {fp_now} else 'NO'}**",
         f"- Every habit update replays exactly, and every newborn follows its arm's law (mismatches 0): "
         f"**{'yes' if mism == 0 else f'NO ({mism})'}**",
         "", f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    n = len(seeds)
    cells = sorted({k for a in ARMS + ("r",) for r in runs[a].values() for k in r["early"].get("0", {})})
    ci = {k: j for j, k in enumerate(cells)}

    def mat(a, field, cens="0", ss=None):
        ss = seeds if ss is None else ss
        M = np.zeros((len(cells), len(ss)))
        for j, s in enumerate(ss):
            for k, v in runs[a][s]["early"].get(cens, {}).items():
                M[ci[k], j] = v[field]
        return M
    N = {a: mat(a, 0) for a in ARMS}
    S = {a: mat(a, 1) for a in ARMS}
    SG = {a: mat(a, 2) for a in ARMS}
    ref = mat("r", 0, ss=sorted(runs["r"])).sum(axis=1)
    w = ref / ref.sum() if ref.sum() else ref
    common = (w > 0) & np.all(np.stack([N[a].sum(axis=1) >= MIN_CELL for a in ARMS]), axis=0)
    cover = {a: float(N[a][common].sum() / N[a].sum()) if N[a].sum() else 0.0 for a in ARMS}

    def E(nn, ss, valid):
        ww = np.where(valid, w, 0.0)
        with np.errstate(invalid="ignore", divide="ignore"):
            mean = np.where(valid, ss / np.where(nn > 0, nn, 1), 0.0)
        return (ww * mean).sum(axis=-1) / ww.sum(axis=-1)
    point = {a: float(E(N[a].sum(1), S[a].sum(1), common)) for a in ARMS}
    reps = {a: [] for a in ARMS}
    for start in range(0, REPS, 500):
        Wb = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(500, n))]).astype(float)
        Nr = {a: Wb @ N[a].T for a in ARMS}
        Sr = {a: Wb @ S[a].T for a in ARMS}
        valid = common[None, :] & np.all(np.stack([Nr[a] > 0 for a in ARMS]), axis=0)
        for a in ARMS:
            reps[a].append(E(Nr[a], Sr[a], valid))
    reps = {a: np.concatenate(v) for a, v in reps.items()}

    def diff(a, b):
        d = reps[a] - reps[b]
        d = d[np.isfinite(d)]
        return point[a] - point[b], float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))
    Dz, Ds, Dx, Dxz = diff("z", "c"), diff("s", "c"), diff("x", "c"), diff("x", "z")

    # Guards (z against v11)
    def col(a, key):
        return np.array([float(runs[a][s]["sums"].get(key, 0.0)) for s in seeds])
    Wg = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def rate_diff(num, den, scale):
        rz = (Wg @ col("z", num)) / (Wg @ col("z", den)) * scale
        rc = (Wg @ col("c", num)) / (Wg @ col("c", den)) * scale
        d = rz - rc
        pz = col("z", num).sum() / col("z", den).sum() * scale
        pc = col("c", num).sum() / col("c", den).sum() * scale
        return pz, pc, float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))
    cd = rate_diff("child_deaths", "child_weeks", 1000.0 * WPY)
    child_flag = (cd[0] - cd[1]) > 0.10 * cd[1] and cd[2] > 0
    pr = (Wg @ col("z", "living_weeks")) / (Wg @ col("c", "living_weeks"))
    pop = (col("z", "living_weeks").sum() / col("c", "living_weeks").sum(), float(np.percentile(pr, 2.5)),
           float(np.percentile(pr, 97.5)))
    pop_flag = pop[0] < 0.90 and pop[2] < 1.0
    ext = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in ARMS}
    ext_flag = ext["z"] - ext["c"] >= 3
    guards = [g for g, f in (("child deaths", child_flag), ("population", pop_flag), ("extinctions", ext_flag)) if f]

    if min(cover.values()) < MIN_COVER:
        verdict = "inconclusive (coverage)"
    elif abs(Ds[0]) > SHAM_BAND:
        verdict = "inconclusive (sham)"
    elif Dz[2] < -MARGIN:
        verdict = "z better"
    elif Dz[2] < MARGIN:
        verdict = "z not worse"
    elif Dz[1] > MARGIN:
        verdict = "z worse"
    else:
        verdict = "inconclusive"
    fmt = lambda t: f"{t[0]:+.4f} [{t[1]:+.4f}, {t[2]:+.4f}]"  # noqa: E731
    L += ["## Primary (frozen): early-life calibration (ages 52-103 weeks), standardized over cells", "",
          "| arm | E (mean abs(q - G)) | early-life updates | coverage |", "|---|---|---|---|"]
    for a in ARMS:
        L.append(f"| {NAME[a]} | {point[a]:.4f} | {int(N[a].sum()):,} | {cover[a]:.3f} |")
    L += ["", f"Common cells: {int(common.sum())} of {len(cells)}; weights from {len(runs['r'])} reference worlds.", "",
          "| contrast | difference [95%] |", "|---|---|",
          f"| **D_z = z - v11** | **{fmt(Dz)}** |", f"| sham - v11 | {fmt(Ds)} |",
          f"| x - v11 (content) | {fmt(Dx)} |", f"| x - z (level) | {fmt(Dxz)} |", "",
          f"Rule: inconclusive if coverage < {MIN_COVER} in any arm, or if the sham's point difference lies outside "
          f"+-{SHAM_BAND}; else z better if D_z's upper bound < -{MARGIN}; z not worse if its upper bound < "
          f"+{MARGIN}; z worse if its lower bound > +{MARGIN}; else inconclusive.", "",
          f"**Reading: {verdict}.**" + (f" **Guard raised: {', '.join(guards)}.**" if guards else " No guard raised."),
          "", "GPT's caution: this measures early-life calibration, not pure learning speed.", ""]
    L += ["## Guards (z against v11)", "",
          f"- Child deaths per 1,000 child-years: z {cd[0]:.2f}, v11 {cd[1]:.2f}; difference "
          f"[{cd[2]:+.2f}, {cd[3]:+.2f}]: **{'RAISED' if child_flag else 'not raised'}**",
          f"- Population z / v11: {pop[0]:.3f} [{pop[1]:.3f}, {pop[2]:.3f}]: **{'RAISED' if pop_flag else 'not raised'}**",
          f"- Extinctions: {', '.join(f'{NAME[a]} {ext[a]}' for a in ARMS)}: **{'RAISED' if ext_flag else 'not raised'}**",
          ""]
    L += ["## Secondary (described, not decisive)", "", "| arm | early signed bias mean(q - G) | death-closed early "
          "updates | all-age calibration | recipes per adult | making per adult-year | mean living |",
          "|---|---|---|---|---|---|---|"]
    for a in ARMS:
        nn, sg = N[a].sum(), SG[a].sum()
        dc = mat(a, 0, cens="1").sum()
        cal_n = sum(sum(v[0] for v in runs[a][s]["cal"].values()) for s in seeds)
        cal_s = sum(sum(v[1] for v in runs[a][s]["cal"].values()) for s in seeds)
        ad = sum(y[0] for s in seeds for y in runs[a][s]["yearly"].values())
        rc = sum(y[1] for s in seeds for y in runs[a][s]["yearly"].values())
        mk = col(a, "adult_makes").sum()
        aw = col(a, "adult_weeks").sum()
        lw = col(a, "living_weeks").sum()
        L.append(f"| {NAME[a]} | {sg / nn:+.4f} | {int(dc):,} | {cal_s / cal_n:.4f} | {rc / ad:.2f} | "
                 f"{mk / (aw / WPY):.4f} | {lw / (len(seeds) * 100 * WPY):.1f} |" if nn and cal_n and ad and aw
                 else f"| {NAME[a]} | - | - | - | - | - | - |")
    L.append("")
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
