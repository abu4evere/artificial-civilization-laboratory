"""IC1 analysis, written before any data (questions.md, frozen as `IC1-frozen`; operational note 1).

  python experiments/IC1_information_channels/analyse_ic1.py            # writes results.md
  python experiments/IC1_information_channels/analyse_ic1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_ic1 import SEEDS, SHARED_MIN, WPY  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261028)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {}
    for f in sorted(glob.glob(str(OUTDIR / "o_seed_*.json"))):
        r = json.load(open(f))
        runs[r["seed"]] = r
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    present = sorted(runs) == sorted(SEEDS)
    fps = {r["code_hash"] for r in runs.values()} | {r["code_hash_after"] for r in runs.values()}
    mism = sum(sum(r["mismatch"].values()) for r in runs.values())
    ok = "All: PASS" in zero and present and len(fps) == 1 and mism == 0
    L = ["# IC1 — How does information pass between people today? Results", "",
         "Frozen as `IC1-frozen` (operational note 1). run_ic1.py, analyse_ic1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({len(runs)} of {len(SEEDS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_v8`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Wrapper counts match the law's events (mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    seeds = sorted(runs)
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])

    def col(key, src="counts"):
        return np.array([float(runs[s][src].get(key, 0)) for s in seeds])

    def ratio(num, den):
        """Pooled ratio of sums, with a world-bootstrap 95% interval."""
        point = num.sum() / den.sum() if den.sum() else float("nan")
        with np.errstate(invalid="ignore", divide="ignore"):
            reps = (W @ num) / (W @ den)
        lo, hi = np.nanpercentile(reps, [2.5, 97.5])
        return point, lo, hi

    def fmt(t, d=3):
        return f"{t[0]:.{d}f} [{t[1]:.{d}f}, {t[2]:.{d}f}]"

    pw = col("person_weeks")
    aw = col("adult_weeks")
    py, ay = pw.sum() / WPY, aw.sum() / WPY
    weeks = np.array([float(runs[s]["final_tick"]) for s in seeds])
    ext = sum(1 for s in seeds if runs[s]["extinct"])
    L += [f"Worlds: {n}; extinct {ext}. Mean living population {pw.sum() / weeks.sum():.1f}; "
          f"{py:,.0f} person-years, {ay:,.0f} adult-years.", ""]

    # Q1
    acc = col("w:accepted")
    off = col("w:offered")
    held, ref = col("ev_verified_w"), col("ev_refuted_w")
    first = ratio(col("w:acc_first_option"), acc)
    hold = ratio(held, held + ref)
    tw = {k: np.array([float(runs[s]["told_water"][k]) for s in seeds])
          for k in ("accepted", "out_of_sight", "used", "used_out_of_sight")}
    L += ["## Q1 — Water places told (primary)", "",
          f"Offered {off.sum():,.0f}; accepted {acc.sum():,.0f}.", "",
          "| measure | share [95%] |", "|---|---|",
          f"| accepted ÷ offered | {fmt(ratio(acc, off))} |",
          f"| **new** (listener knew no water of their own) | {fmt(ratio(col('w:acc_new'), acc))} |",
          f"| **first option** (no own water and no other told water) | **{fmt(first)}** |",
          f"| redundant (listener could see fresh water) | {fmt(ratio(col('w:acc_redundant'), acc))} |",
          f"| true (fresh water within 1 tile of the spot) | {fmt(ratio(col('w:acc_true'), acc))} |",
          f"| both see the told spot | {fmt(ratio(col('w:acc_both_see'), acc))} |",
          f"| the speaker saw it themselves (not relayed) | {fmt(ratio(col('w:acc_speaker_saw'), acc))} |",
          f"| **held, of those checked** ({(held + ref).sum():,.0f} checked) | **{fmt(hold)}** |",
          f"| thirst decisions whose target was told (of {col('thirst_target').sum():,.0f}) | "
          f"{fmt(ratio(col('thirst_target_told'), col('thirst_target')), 4)} |",
          f"| accepted places later chosen as a thirst target ({tw['accepted'].sum():,.0f} listener-places) | "
          f"{fmt(ratio(tw['used'], tw['accepted']), 4)} |",
          f"| the same, for places out of the listener's sight ({tw['out_of_sight'].sum():,.0f}) | "
          f"{fmt(ratio(tw['used_out_of_sight'], tw['out_of_sight']), 4)} |", ""]
    th = col("w:acc_thirst_sum").sum() / acc.sum() if acc.sum() else float("nan")
    dist = {}
    for s in seeds:
        for k, v in runs[s]["dist"].items():
            dist[k] = dist.get(k, 0) + v
    L += [f"Listener's mean thirst at the telling: {th:.3f}.", "",
          "| distance to the told spot | listener | speaker |", "|---|---|---|"]
    for band in ("sight", "5-12", "13+"):
        L.append(f"| {band} | {dist.get('listener_' + band, 0):,} | {dist.get('speaker_' + band, 0):,} |")
    b1 = first[0] >= 0.20 and hold[0] >= 0.50
    L += ["", f"**B1 (water telling does real work): {'RAISED' if b1 else 'not raised'}** "
              f"(first option {first[0]:.3f}, needs ≥ 0.20; held {hold[0]:.3f}, needs ≥ 0.50).", ""]

    # Q2
    talks = col("talks")
    sh = col("talks_shared")
    sha = col("talks_shared_adults")
    per_ay = sha.sum() / ay if ay else float("nan")
    reps_ay = (W @ sha) / (W @ aw / WPY)
    pairs = [p for s in seeds for p in runs[s]["pairs"]]
    counts = np.array([p[0] for p in pairs], float)
    in_rep = counts[counts >= SHARED_MIN].sum() / counts.sum() if counts.sum() else float("nan")
    rep_w = np.array([sum(p[0] for p in runs[s]["pairs"] if p[0] >= SHARED_MIN) for s in seeds], float)
    all_w = np.array([sum(p[0] for p in runs[s]["pairs"]) for s in seeds], float)
    rep_t = ratio(rep_w, all_w)
    srcs = np.array([p[1] for p in pairs], float)
    runs_w = np.array([p[2] for p in pairs], float)
    big = counts >= SHARED_MIN
    L += ["## Q2 — Shared attention at water", "",
          "| measure | value [95%] |", "|---|---|",
          f"| talks where both see the same fresh-water tile, of all talks ({talks.sum():,.0f}) | {fmt(ratio(sh, talks))} |",
          f"| talks where either sees fresh water | {fmt(ratio(col('talks_either_sees'), talks))} |",
          f"| **such talks between two adults, per adult-year** | **{per_ay:.2f} "
          f"[{np.percentile(reps_ay, 2.5):.2f}, {np.percentile(reps_ay, 97.5):.2f}]** |",
          f"| water places told while both see the spot (of accepted) | {fmt(ratio(col('w:acc_both_see'), acc))} |",
          f"| **share of such moments in pairs with ≥ {SHARED_MIN} of them** | **{fmt(rep_t)}** |",
          f"| mean fresh tiles both see, in such talks | {col('shared_fresh_tiles_sum').sum() / sh.sum() if sh.sum() else float('nan'):.1f} |",
          f"| mean animal groups both see, in such talks | {col('shared_herds_sum').sum() / sh.sum() if sh.sum() else float('nan'):.1f} |",
          "", f"Pairs with such moments: {len(pairs):,}; with ≥ {SHARED_MIN}: {int(big.sum()):,}.", ""]
    if len(pairs):
        L += ["| pairs | median moments | median water tiles shared | median longest run (weeks) |",
              "|---|---|---|---|",
              f"| all | {np.median(counts):.0f} | {np.median(srcs):.0f} | {np.median(runs_w):.0f} |"]
        if big.any():
            L.append(f"| ≥ {SHARED_MIN} moments | {np.median(counts[big]):.0f} | {np.median(srcs[big]):.0f} | "
                     f"{np.median(runs_w[big]):.0f} |")
        L.append("")
    b2 = per_ay >= 1.0 and in_rep >= 0.25
    L += [f"**B2 (grounding moments exist): {'RAISED' if b2 else 'not raised'}** "
          f"({per_ay:.2f} per adult-year, needs ≥ 1; {in_rep:.3f} in repeated pairs, needs ≥ 0.25).", ""]

    # Q3
    def per_k(x):
        return 1000.0 * x.sum() / py if py else float("nan")

    def held_of(k):
        v, r_ = col("ev_verified_" + k).sum(), col("ev_refuted_" + k).sum()
        return f"{v / (v + r_):.3f} of {v + r_:,.0f}" if v + r_ else "not tested"
    hows = sorted({k[len("ev_learn_thing_"):] for s in seeds for k in runs[s]["counts"] if k.startswith("ev_learn_thing_")})
    copies = col("imit_copies").sum()
    isize = sum(runs[s]["imit_size_sum"] for s in seeds) / copies if copies else float("nan")
    stories = sum(col(k) for k in ("ev_story_accepted", "ev_story_doubted", "ev_story_rejected", "ev_story_known"))
    L += ["## Q3 — The channels (per 1,000 person-years)", "",
          "| channel | received | held, of those tested |", "|---|---|---|",
          f"| water places (accepted) | {per_k(col('ev_learn_w')):.1f} | {held_of('w')} |",
          f"| game places (accepted) | {per_k(col('ev_learn_g')):.1f} | {held_of('g')} |",
          f"| beliefs about stashing (accepted) | {per_k(col('ev_learn_belief')):.1f} | {held_of('b')} |"]
    for h in hows:
        L.append(f"| recipes learned: {h} | {per_k(col('ev_learn_thing_' + h)):.1f} | |")
    L += [f"| recipe claims (m:) | | {held_of('m')} |",
          f"| marks read | {per_k(col('ev_read')):.1f} | |",
          f"| stories told (accepted {col('ev_story_accepted').sum() / stories.sum() if stories.sum() else float('nan'):.3f}) | "
          f"{per_k(stories):.1f} | |",
          f"| word about others (reputation) | {per_k(col('ev_vouched')):.1f} | |",
          f"| habit copies (of {per_k(col('imit_calls')):.1f} talks) | {per_k(col('imit_copies')):.1f} | |", "",
          f"Mean size of a habit copy (sum of changes over the whole table): {isize:.3f}. "
          "As GPT cautioned, counts are not amounts of information.", ""]
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
