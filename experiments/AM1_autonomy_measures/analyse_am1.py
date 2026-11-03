"""AM1 analysis, written before any data (questions.md, frozen as `AM1-frozen`).

  python experiments/AM1_autonomy_measures/analyse_am1.py                      # writes results.md
  python experiments/AM1_autonomy_measures/analyse_am1.py --smoke --dir <folder>
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
import run_am1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261108)
ARMS = ("c", "h", "a", "t", "x")
NAME = {"c": "v11", "h": "no habits", "a": "fewer acts", "t": "more chance", "x": "sham"}


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
    m = re.search(r"code_v11 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    if SMOKE:
        seeds = sorted(set.intersection(*[set(runs[a]) for a in ARMS if runs[a]]))
        present = len(seeds) > 0
    else:
        seeds = sorted(R.SEEDS)
        present = all(sorted(runs[a]) == seeds for a in ARMS)
    allr = [r for a in ARMS for r in runs[a].values()]
    fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
    sane = all(runs["a"][s]["sums"].get("m3_g_made", 0) + runs["a"][s]["sums"].get("m3_m_made", 0) == 0
               for s in seeds if s in runs["a"])
    ok = bool(zero_ok and present and fps == {fp_now} and sane)
    L = ["# AM1: Measuring autonomy against constrained controls (results)", "",
         "Frozen as `AM1-frozen`. run_am1.py, analyse_am1.py (written before data).", "", "## Validity", "",
         f"- Zero checks (All: PASS, same `code_v11` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_v11`'s: **{'yes' if fps == {fp_now} else 'NO'}**",
         f"- Sanity (fewer acts completes no chain): **{'yes' if sane else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    arms = [a for a in ARMS if all(s in runs[a] for s in seeds)]
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def col(a, key):
        return np.array([float(runs[a][s]["sums"].get(key, 0)) for s in seeds])

    # --- M1: SC1's C12 within each arm (ridge, lambda 1, four folds of eight worlds)
    folds = {s: i % 4 for i, s in enumerate(seeds)}

    def m1_sse(a):
        def design(s):
            snaps = {(x[0], x[1]): x for x in runs[a][s]["snaps"]}
            XA, XB, Y = [], [], []
            for (pid, y), p in snaps.items():
                q = snaps.get((pid, y + 5))
                if q is None or y + 5 > 195:
                    continue
                ta, tb, sb = sum(p[5]), sum(q[5]), sum(q[6])
                if not (ta and tb and sb):
                    continue
                b0 = list(p[4]) + [p[2], 1.0 if p[3] == "M" else 0.0] + [v / sb for v in q[6]] + list(p[7])
                XA.append(b0)
                XB.append(b0 + [v / ta for v in p[5]])
                Y.append([v / tb for v in q[5]])
            return np.array(XA), np.array(XB), np.array(Y)
        D = {s: design(s) for s in seeds}
        out = []
        for which in (0, 1):
            sse = np.zeros(n)
            for f in range(4):
                tr = [s for s in seeds if folds[s] != f and len(D[s][2])]
                te = [s for s in seeds if folds[s] == f and len(D[s][2])]
                if not tr or not te:
                    continue
                X = np.vstack([D[s][which] for s in tr])
                Y = np.vstack([D[s][2] for s in tr])
                mu, sd = X.mean(0), X.std(0)
                sd[sd == 0] = 1.0
                Xs = np.hstack([(X - mu) / sd, np.ones((len(X), 1))])
                P = np.eye(Xs.shape[1])
                P[-1, -1] = 0.0
                B = np.linalg.solve(Xs.T @ Xs + 1.0 * P, Xs.T @ Y)
                for s in te:
                    Xt = np.hstack([(D[s][which] - mu) / sd, np.ones((len(D[s][which]), 1))])
                    sse[seeds.index(s)] = float(((D[s][2] - Xt @ B) ** 2).sum())
            out.append(sse)
        return out[0], out[1], sum(len(D[s][2]) for s in seeds)

    val, rep, info = {}, {}, {}
    for a in arms:
        if a == "a":
            continue
        sa, sb, npairs = m1_sse(a)
        with np.errstate(invalid="ignore", divide="ignore"):
            val[("M1", a)] = (sa.sum() - sb.sum()) / sa.sum() if sa.sum() else float("nan")
            rep[("M1", a)] = ((W @ sa) - (W @ sb)) / (W @ sa)
        info[("M1", a)] = f"person pairs {npairs:,}"

    # --- M3 and M5: P(made | gather chain) - P(made | matched chain), sums pooled per world
    for meas, pre in (("M3", "m3"), ("M5", "m5")):
        for a in arms:
            gc, gm, mc, mm = (col(a, f"{pre}_{k}") for k in ("g_chains", "g_made", "m_chains", "m_made"))
            with np.errstate(invalid="ignore", divide="ignore"):
                val[(meas, a)] = gm.sum() / gc.sum() - mm.sum() / mc.sum() if gc.sum() and mc.sum() else float("nan")
                rep[(meas, a)] = (W @ gm) / (W @ gc) - (W @ mm) / (W @ mc)
            info[(meas, a)] = f"gather chains {int(gc.sum()):,}, matched {int(mc.sum()):,}"

    L += ["## The three measures with frozen predictions (each predicted lower in no habits and in more chance)", "",
          "| measure | arm | value | arm − v11 [95%] | sample |", "|---|---|---|---|---|"]
    readings = {}
    for meas in ("M1", "M3", "M5"):
        for a in arms:
            if (meas, a) not in val:
                continue
            d = "" if a == "c" else "{:+.4f} [{:+.4f}, {:+.4f}]".format(
                val[(meas, a)] - val[(meas, "c")], *pct(rep[(meas, a)] - rep[(meas, "c")]))
            L.append(f"| {meas} | {NAME[a]} | {val[(meas, a)]:.4f} | {d} | {info[(meas, a)]} |")
        passes = {}
        for ctrl in ("h", "t"):
            if (meas, ctrl) in rep and (meas, "c") in rep:
                lo, hi = pct(rep[(meas, "c")] - rep[(meas, ctrl)])
                passes[ctrl] = lo > 0
        if passes.get("h") and passes.get("t"):
            rd = "validated"
        elif passes.get("h") or passes.get("t"):
            rd = "partly validated (by " + ("no habits" if passes.get("h") else "more chance") + " only)"
        else:
            rd = "not validated"
        unstable = False
        if (meas, "x") in rep and (meas, "h") in val:
            half = abs(val[(meas, "c")] - val[(meas, "h")]) / 2
            lo, hi = pct(rep[(meas, "x")] - rep[(meas, "c")])
            unstable = lo > half or hi < -half
        readings[meas] = rd + ("; unstable (sham)" if unstable else "")
    L += ["", "Rule: validated if v11 − no habits and v11 − more chance both have 95% intervals wholly above 0; partly "
          "validated if only one does; otherwise not validated (reported, not dropped). Unstable if the sham − v11 "
          "interval lies wholly outside ±(half the v11 − no habits point difference).", ""]
    for meas in ("M1", "M3", "M5"):
        L.append(f"**{meas}: {readings.get(meas, 'not computed')}.**")
    L.append("")

    # --- described: M2, M4, M6a, M6b
    def ratio(a, num, den):
        nu, de = col(a, num), col(a, den)
        with np.errstate(invalid="ignore", divide="ignore"):
            return (nu.sum() / de.sum() if de.sum() else float("nan")), (W @ nu) / (W @ de)
    described = [("M2 (bits beyond shuffle, per adult-year)", "m2_mi_sum", "m2_person_years"),
                 ("M4 new tile targets", "m4_tile_new", "m4_tile_decisions"),
                 ("M4 new person targets", "m4_person_new", "m4_person_decisions"),
                 ("M4 new recipes made", "m4_make_new", "m4_make_decisions"),
                 ("M6a new in steps", "m6a_new_in_steps", "m6a_new_acts"),
                 ("M6b transfer to a new cue", "m6b_new_cue", "m6b_established")]
    L += ["## Described (no frozen prediction)", "", "| measure | " + " | ".join(NAME[a] for a in arms) +
          " | v11 − no habits [95%] | v11 − more chance [95%] |", "|---|" + "---|" * (len(arms) + 2)]
    for label, num, den in described:
        vals = {a: ratio(a, num, den) for a in arms}
        cells = " | ".join(f"{vals[a][0]:.4f}" for a in arms)
        dd = []
        for ctrl in ("h", "t"):
            if ctrl in vals:
                dd.append("{:+.4f} [{:+.4f}, {:+.4f}]".format(vals["c"][0] - vals[ctrl][0],
                                                              *pct(vals["c"][1] - vals[ctrl][1])))
            else:
                dd.append("-")
        L.append(f"| {label} | {cells} | {dd[0]} | {dd[1]} |")
    L += ["", "## Population (beside every measure)", "", "| arm | living-weeks | adult-weeks (16–49) | extinct worlds |",
          "|---|---|---|---|"]
    for a in arms:
        L.append(f"| {NAME[a]} | {int(col(a, 'living_weeks').sum()):,} | {int(col(a, 'adult_weeks').sum()):,} | "
                 f"{sum(1 for s in seeds if runs[a][s]['extinct'])} |")
    L.append("")
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
