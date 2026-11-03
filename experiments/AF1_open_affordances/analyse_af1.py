"""AF1 analysis, written before any data (questions.md, frozen as `AF1-frozen`).

  python experiments/AF1_open_affordances/analyse_af1.py                      # writes results.md
  python experiments/AF1_open_affordances/analyse_af1.py --smoke --dir <folder>
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
import run_af1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261106)
ARMS = ("c", "s", "k", "sk", "x")
NAME = {"c": "v11", "s": "S", "k": "K", "sk": "S+K", "x": "sham"}
MIN_GAIN, SHAM_BAND = 0.01, 0.01
WPY = R.WPY


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
    m = re.search(r"code_af1 fingerprint: ([0-9a-f]{64})", zero)
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
    L = ["# AF1 — Open what made things can do: results", "",
         "Frozen as `AF1-frozen`. run_af1.py, analyse_af1.py (written before data).", "", "## Validity", "",
         f"- Zero checks (All: PASS, same `code_af1` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_af1`'s: **{'yes' if fps == {fp_now} else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    arms = [a for a in ARMS if all(s in runs[a] for s in seeds)]
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def col(a, f):
        return np.array([float(f(runs[a][s])) for s in seeds])
    K = {a: col(a, lambda r: r["n_kinds"]) for a in arms}
    M = {a: col(a, lambda r: r["n_remade"]) for a in arms}
    point = {a: M[a].sum() / K[a].sum() if K[a].sum() else float("nan") for a in arms}
    with np.errstate(invalid="ignore", divide="ignore"):
        reps = {a: (W @ M[a]) / (W @ K[a]) for a in arms}

    def diff(a, b):
        return point[a] - point[b], *pct(reps[a] - reps[b])
    L += ["## Primary (frozen): R = share of kinds invented in years 100-195 whose own recipe is made again by choice "
          "within 5 years (lineage)", "", "| arm | R | kinds | remade |", "|---|---|---|---|"]
    for a in arms:
        L.append(f"| {NAME[a]} | {point[a]:.4f} | {int(K[a].sum()):,} | {int(M[a].sum()):,} |")
    pairs = [("s", "c"), ("k", "c"), ("sk", "c"), ("s", "x"), ("k", "x"), ("sk", "x"), ("sk", "s"), ("sk", "k"),
             ("x", "c")]
    D = {(a, b): diff(a, b) for a, b in pairs if a in arms and b in arms}
    L += ["", "| contrast | difference [95%] |", "|---|---|"]
    for (a, b), (pt, lo, hi) in D.items():
        L.append(f"| {NAME[a]} - {NAME[b]} | {pt:+.4f} [{lo:+.4f}, {hi:+.4f}] |")

    def positive(a):
        x, y = D.get((a, "c")), D.get((a, "x"))
        return bool(x and y and x[1] > 0 and y[1] > 0 and x[0] >= MIN_GAIN and y[0] >= MIN_GAIN)
    sham = D.get(("x", "c"))
    if sham and (sham[1] > SHAM_BAND or sham[2] < -SHAM_BAND):
        readings = {a: "inconclusive (sham)" for a in ("s", "k", "sk") if a in arms}
    else:
        readings = {a: ("positive" if positive(a) else "inconclusive") for a in ("s", "k", "sk") if a in arms}
    guards = {}
    for a in ("s", "k", "sk"):
        if a not in arms:
            continue
        lw_a, lw_c = col(a, lambda r: r["sums"].get("living_weeks", 0)), col("c", lambda r: r["sums"].get("living_weeks", 0))
        with np.errstate(invalid="ignore", divide="ignore"):
            pr = (W @ lw_a) / (W @ lw_c)
        pop = (lw_a.sum() / lw_c.sum(), *pct(pr))
        ext = sum(1 for s in seeds if runs[a][s]["extinct"]) - sum(1 for s in seeds if runs["c"][s]["extinct"])
        g = (["population"] if pop[0] < 0.90 and pop[2] < 1.0 else []) + (["extinctions"] if ext >= 3 else [])
        guards[a] = (pop, ext, g)
    L += ["", "Rule: inconclusive (sham) if the sham - v11 interval lies wholly outside +-0.01; otherwise an arm is "
          "\"positive\" only if arm - v11 and arm - sham both have intervals above 0 and both points are at least 0.01; "
          "otherwise \"inconclusive\".", ""]
    for a in ("s", "k", "sk"):
        if a in readings:
            L.append(f"**{NAME[a]}: {readings[a]}.**" + (f" **Guard raised: {', '.join(guards[a][2])}.**"
                                                       if guards[a][2] else " No guard raised."))
    L += ["", "## Guards (each arm against v11)", ""]
    for a, (pop, ext, g) in guards.items():
        L.append(f"- {NAME[a]}: population {pop[0]:.3f} [{pop[1]:.3f}, {pop[2]:.3f}]; extinctions beyond v11's {ext:+d}")
    L += ["", "## Secondary (described, not decisive)", "",
          "| arm | functional D=5 | D=10 | D=20 | known at 1 yr | 2 yr | 5 yr | stand-in makes per adult-year | "
          "made things per adult | materials per adult | makes per adult-year | kinds per 100 adult-years |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for a in arms:
        ks = [e for r in runs[a].values() for e in r["kinds"]]
        nk = len(ks) or 1
        f = [sum(e[7 + j] for e in ks) / nk for j in range(3)]
        av = [sum(1 for e in ks if e[4 + j]) / max(1, sum(1 for e in ks if e[4 + j] is not None)) for j in range(3)]
        su = lambda key: sum(r["sums"].get(key, 0) for r in runs[a].values())  # noqa: E731
        ay = su("adult_weeks") / WPY
        ca = su("census_adults") or 1
        L.append(f"| {NAME[a]} | {f[0]:.4f} | {f[1]:.4f} | {f[2]:.4f} | {av[0]:.3f} | {av[1]:.3f} | {av[2]:.3f} | "
                 f"{su('standin_makes') / ay:.5f} | {su('census_items') / ca:.2f} | {su('census_mats') / ca:.2f} | "
                 f"{su('adult_makes') / ay:.4f} | {100 * len(ks) / ay:.3f} |" if ay else f"| {NAME[a]} | - |")
    L.append("")
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
