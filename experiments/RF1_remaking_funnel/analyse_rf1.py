"""RF1 analysis (questions.md, frozen as `RF1-frozen`); written before any data.

Per kind with at least one wanting week, the farthest stage reached in 5 years: 1 cannot obtain, 2 not offered,
3 out-competed, 4 started but never complete, 5 complete (all inputs in hand at a week's end while the recipe was
known). Shares pooled over worlds; a world bootstrap of 10,000 replicates, NumPy seed 20261120. Reading: "inability
dominates" if stages 1+2 > 0.5 with the lower bound above 0.5; "pursuit fails" if stages 3+4 > 0.5 with the lower
bound above 0.5; otherwise "mixed".

  python experiments/RF1_remaking_funnel/analyse_rf1.py                      # writes results.md
  python experiments/RF1_remaking_funnel/analyse_rf1.py --smoke --dir <folder>
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
import run_rf1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261120)
F = {k: i for i, k in enumerate(R.KIND_FIELDS)}
NAMES = {1: "cannot obtain", 2: "not offered", 3: "out-competed", 4: "started, never complete", 5: "complete"}


def pct(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


def stage(k):
    if k[F["ww"]] == 0:
        return 0
    if k[F["full"]]:
        return 5
    if k[F["cho"]]:
        return 4
    if k[F["off"]]:
        return 3
    if k[F["obt"]]:
        return 2
    return 1


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {}
    for f in sorted(glob.glob(str(OUTDIR / "c_seed_*.json"))):
        r = json.load(open(f))
        runs[r["seed"]] = r
    zero = ""
    for name in ("zero_cloud.log", "zero_local.log"):
        if (HERE / name).exists():
            zero = (HERE / name).read_text(encoding="utf-8", errors="replace")
            break
    R.base.setup(R.CODE)
    fp_now = R.base.fingerprint(R.CODE)
    m = re.search(r"code_v13 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    seeds = sorted(runs) if SMOKE else sorted(R.SEEDS)
    present = len(seeds) > 0 if SMOKE else sorted(runs) == seeds
    fps = {r["code_hash"] for r in runs.values()} | {r["code_hash_after"] for r in runs.values()}
    unit_wrong = sum(r["unit2"][0] for r in runs.values())
    ok = bool(zero_ok and present and fps == {fp_now})
    L = ["# RF1: why do the inputs never come together? (results)", "",
         "Frozen as `RF1-frozen`. run_rf1.py, analyse_rf1.py (written before data). Read-only on v13; kinds first made "
         "in years 130–165, followed 5 years.", "", "## Validity", "",
         f"- Zero checks (All: PASS, same `code_v13` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(runs)} of {len(R.SEEDS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_v13`'s: **{'yes' if fps == {fp_now} else 'NO'}**",
         f"- In the runs too, missing inputs empty exactly when can_make: wrong {unit_wrong:,} of "
         f"{sum(r['unit2'][1] for r in runs.values()):,}", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)
    K = [runs[s]["rf1"] if s in runs else [] for s in seeds]
    st = [[stage(k) for k in ks] for ks in K]
    den = np.array([sum(1 for s in ss if s > 0) for ss in st], float)

    def share(stages):
        nu = np.array([sum(1 for s in ss if s in stages) for ss in st], float)
        with np.errstate(invalid="ignore", divide="ignore"):
            return nu.sum() / den.sum(), (W @ nu) / (W @ den), int(nu.sum())

    L += ["## Primary: the funnel (kinds with at least one wanting week)", "",
          f"Kinds tracked {sum(len(ks) for ks in K):,}; with a wanting week {int(den.sum()):,}; with none "
          f"{sum(1 for ss in st for s in ss if s == 0):,}.", "",
          "| stage | share | 95% | kinds |", "|---|---|---|---|"]
    for s in range(1, 6):
        p, reps, cnt = share({s})
        L.append(f"| {s}. {NAMES[s]} | {p:.3f} | [{pct(reps)[0]:.3f}, {pct(reps)[1]:.3f}] | {cnt:,} |")
    pi, ri, _ = share({1, 2})
    pp, rp, _ = share({3, 4})
    li, hi_i = pct(ri)
    lp, hi_p = pct(rp)
    L += ["", f"- Inability (1 + 2): **{pi:.3f} [{li:.3f}, {hi_i:.3f}]**",
          f"- Pursuit fails (3 + 4): **{pp:.3f} [{lp:.3f}, {hi_p:.3f}]**", ""]
    if pi > 0.5 and li > 0.5:
        reading, follow = "inability dominates", "the option generation and the inputs' availability, read in the code (a possible fault), not an intention law"
    elif pp > 0.5 and lp > 0.5:
        reading, follow = "pursuit fails", "the council on an intention law (a held aim toward a state one's own experience valued)"
    else:
        reading, follow = "mixed", "the council, with the shares"
    L += [f"**Reading: {reading}.**", "", f"**What follows (decided before data): {follow}.**", ""]

    # --- described
    T = {k: sum(r["tally"][k] for r in runs.values()) for k in ("ww", "raw", "raw_ungatherable", "part", "wet", "fill",
                                                                 "fire_away", "at_limit")}
    ins: dict = {}
    for r in runs.values():
        for a, v in r["tally"]["instead"].items():
            ins[a] = ins.get(a, 0) + v
    tot_ins = sum(ins.values())
    allk = [k for ks in K for k in ks]
    s4 = [k for k in allk if stage(k) == 4]
    s5 = [k for k in allk if stage(k) == 5]
    ww = sorted(k[F["ww"]] for k in allk if k[F["ww"]] > 0)
    ww_t = max(1, T["ww"])
    L += ["## Described", "",
          f"- Wanting weeks {T['ww']:,}; per kind with any, median {ww[len(ww) // 2] if ww else 'nan'}",
          f"- Missing inputs per wanting week (counts): raw {T['raw']:,} (of them bone or hide, not gatherable from "
          f"the ground: {T['raw_ungatherable']:,}); part {T['part']:,}; wet {T['wet']:,}; fill {T['fill']:,}",
          f"- A heat recipe away from a fire: {T['fire_away']:,} wanting weeks",
          f"- At the carry limit: {T['at_limit']:,} wanting weeks ({T['at_limit'] / ww_t:.3f})",
          "- Chosen instead (wanting weeks with a choice not toward a missing input): " +
          ", ".join(f"{a} {v / max(1, tot_ins):.3f}" for a, v in sorted(ins.items(), key=lambda x: -x[1])[:8]) +
          f" (of {tot_ins:,})",
          f"- Stage 4: {len(s4):,} kinds; a completed gather of a missing input {sum(k[F['comp']] for k in s4):,}; "
          f"a gathered input later lower before the set was complete {sum(k[F['lost']] for k in s4):,}",
          f"- Stage 5: {len(s5):,} kinds; make offered {sum(k[F['make_offered']] for k in s5):,}; remade "
          f"{sum(k[F['remade']] for k in s5):,}", ""]
    # amendment 1: why the kinds with no wanting week had none (the reason seen most in the inventor's decision weeks)
    why: dict = {}
    for k in allk:
        if k[F["ww"]] > 0:
            continue
        counts = [k[len(R.KIND_FIELDS) + j] for j in range(len(R.NOT))]
        key = R.NOT[int(np.argmax(counts))] if sum(counts) else "no decision week (inventor dead)"
        why[key] = why.get(key, 0) + 1
    names = {"young": "inventor not grown", "gone": "recipe forgotten", "low": "valued at or below 0.05",
             "held": "still holding a fresh one"}
    L += ["- Amendment 1, kinds with no wanting week, by the reason most often seen: " +
          ", ".join(f"{names.get(a, a)} {v:,}" for a, v in sorted(why.items(), key=lambda x: -x[1])), ""]
    L += ["## Population", "", f"- Worlds {len(seeds)}; extinct {sum(1 for s in seeds if s in runs and runs[s]['extinct'])}",
          ""]
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
