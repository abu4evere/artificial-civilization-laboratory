"""CI1 analysis, written before any data (questions.md, frozen as `CI1-frozen`; amendment 1 before code).

  python experiments/CI1_children_and_aims/analyse_ci1.py                      # writes results.md
  python experiments/CI1_children_and_aims/analyse_ci1.py --smoke --dir <folder>
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
import run_ci1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261122)
ARMS = ("c", "g", "i", "b", "x")
NAME = {"c": "v14", "g": "LG", "i": "IN", "b": "LG+IN", "x": "sham"}
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
    m = re.search(r"code_ci1 fingerprint: ([0-9a-f]{64})", zero)
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
    L = ["# CI1: Children may make again, and a held aim that keeps the pieces (results)", "",
         "Frozen as `CI1-frozen` (amendment 1 before code). run_ci1.py, analyse_ci1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks (All: PASS, same `code_ci1` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_ci1`'s: **{'yes' if fps == {fp_now} else 'NO'}**", "",
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

    def rate(a, num, den, per):
        """(point, replicates) of sum(num) / sum(den) * per."""
        nu, de = col(a, num), col(a, den)
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

    ext = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in arms}
    LY = 1000 * WPY                                   # per 1,000 living-years (or child-years) from weeks

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

    # --- co-primary: the per-kind complete-set share
    def kinds(a):
        K = np.array([float(runs[a][s]["n_kinds"]) for s in seeds])
        C = np.array([float(runs[a][s]["n_complete"]) for s in seeds])
        with np.errstate(invalid="ignore", divide="ignore"):
            return (C.sum() / K.sum() if K.sum() else float("nan")), (W @ C) / (W @ K), int(K.sum()), int(C.sum())
    share = {a: kinds(a) for a in arms}

    L += ["## Readings (frozen; each arm alone against v14)", ""]
    readings = {}
    G = {}
    for a in ("g", "i", "b"):
        if a not in arms:
            continue
        G[a] = guards(a)
        d = share[a][0] - share["c"][0]
        lo, hi = pct(share[a][1] - share["c"][1])
        passes = lo > 0
        readings[a] = "harm" if G[a][0] else ("supported" if passes else "no harm, no effect")
        L.append(f"- **{NAME[a]}: {readings[a]}.** Guards raised: {', '.join(G[a][0]) if G[a][0] else 'none'}. "
                 f"Complete-set share {share[a][0]:.4f} against v14's {share['c'][0]:.4f}: "
                 f"{d:+.4f} [{lo:+.4f}, {hi:+.4f}].")
    if "x" in arms:
        d = share["x"][0] - share["c"][0]
        lo, hi = pct(share["x"][1] - share["c"][1])
        L.append(f"- Sham: complete-set share {d:+.4f} [{lo:+.4f}, {hi:+.4f}] against v14; guards raised: "
                 f"{', '.join(guards('x')[0]) or 'none'}.")
    L += ["", "Rule: \"supported\" if no guard is raised and the complete-set interval (arm − v14) lies wholly above 0; "
          "\"no harm, no effect\" if no guard is raised and it does not; \"harm\" if any guard is raised. A supported "
          "arm goes to a confirmatory run on new seeds before any adoption.", ""]

    L += ["## Co-primary: the share of world-new kinds whose inventor held the complete input set within 5 years", "",
          "| arm | kinds | complete | share | arm − v14 [95%] |", "|---|---|---|---|---|"]
    for a in arms:
        dd = "" if a == "c" else "{:+.4f} [{:+.4f}, {:+.4f}]".format(share[a][0] - share["c"][0],
                                                                    *pct(share[a][1] - share["c"][1]))
        L.append(f"| {NAME[a]} | {share[a][2]:,} | {share[a][3]:,} | {share[a][0]:.4f} | {dd} |")

    L += ["", "## Primary: harm guards, per arm against v14", ""]
    for a in G:
        L += [f"### {NAME[a]}", "", "| guard | arm | v14 | ratio or difference [95%] |", "|---|---|---|---|"]
        for lab, pa, pc, v, lo, hi in G[a][1]:
            L.append(f"| {lab} | {pa:,.4f} | {pc:,.4f} | {v:+.4f} [{lo:+.4f}, {hi:+.4f}] |" if "difference" in lab
                     or "extra" in lab else f"| {lab} | {pa:,.4f} | {pc:,.4f} | {v:.4f} [{lo:.4f}, {hi:.4f}] |")
        L.append("")

    # --- described
    L += ["## Described (not decisive)", ""]
    L += ["| arm | remade within 5 years | made again once complete | child inventors: kinds, complete, remade | "
          "grown inventors: kinds, complete, remade |", "|---|---|---|---|---|"]
    for a in arms:
        ks = [e for s in seeds for e in runs[a][s]["kinds"]]
        comp = [e for e in ks if e[3]]
        ch = [e for e in ks if e[2]]
        gr = [e for e in ks if not e[2]]

        def trio(xs):
            return f"{len(xs):,}, {sum(e[3] for e in xs):,}, {sum(e[4] for e in xs):,}"
        L.append(f"| {NAME[a]} | {sum(e[4] for e in ks):,} of {len(ks):,} | "
                 f"{sum(e[4] for e in comp):,} of {len(comp):,} | {trio(ch)} | {trio(gr)} |")
    L += ["", "| arm | aims formed | ended: complete / value / forgotten / held / interrupted | puts, hands, makes, play "
          "trials kept off | child makes per 1,000 child-weeks | makes per adult-year | care per 1,000 adult-weeks | food "
          "per adult (year ends) | adult-weeks at the material limit | child health | world-new kinds |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for a in arms:
        su = lambda k: sum(runs[a][s]["sums"].get(k, 0) for s in seeds)  # noqa: E731
        aw, cw = su("adult_weeks") or 1, su("child_weeks") or 1
        ends = " / ".join(f"{int(su('aim_end_' + c)):,}" for c in ("complete", "value", "forgotten", "held",
                                                                     "interrupted"))
        blocks = ", ".join(f"{int(su('aim_block_' + c)):,}" for c in ("put", "hand", "make", "play"))
        L.append(f"| {NAME[a]} | {int(su('aim_form')):,} | {ends} | {blocks} | {1000 * su('makes_child') / cw:.3f} | "
                 f"{WPY * su('makes_adult') / aw:.4f} | {1000 * su('care') / aw:.2f} | "
                 f"{su('census_food') / (su('census_adults') or 1):.1f} | {su('adult_weeks_at_limit') / aw:.4f} | "
                 f"{su('census_child_health') / (su('census_children') or 1):.1f} | "
                 f"{sum(runs[a][s]['n_kinds'] for s in seeds):,} |")
    L.append("")
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
