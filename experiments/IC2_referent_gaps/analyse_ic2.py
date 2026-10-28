"""IC2 analysis, written before any data (questions.md, frozen as `IC2-frozen`).

  python experiments/IC2_referent_gaps/analyse_ic2.py            # writes results.md
  python experiments/IC2_referent_gaps/analyse_ic2.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_ic2 import REFS, SEEDS, WPY  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261028)
SHARED_MIN = 5          # IC1's B2 rule: a pair "repeats" with at least 5 moments
WORKABLE_SHARED, WORKABLE_REP, WORKABLE_GAPS = 1.0, 0.25, 1.0


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
    L = ["# IC2 — Where is there a real information gap: water, game or danger? Results"
         + (" (SMOKE TEST, throwaway seeds)" if SMOKE else ""), "",
         "Frozen as `IC2-frozen`. run_ic2.py, analyse_ic2.py (written before data).", "",
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

    def ratio(num, den, scale=1.0):
        """Pooled ratio of sums (times scale), with a world-bootstrap 95% interval."""
        point = scale * num.sum() / den.sum() if den.sum() else float("nan")
        with np.errstate(invalid="ignore", divide="ignore"):
            reps = scale * (W @ num) / (W @ den)
        lo, hi = np.nanpercentile(reps, [2.5, 97.5]) if np.isfinite(reps).any() else (float("nan"),) * 2
        return point, lo, hi

    def fmt(t, d=3):
        return f"{t[0]:.{d}f} [{t[1]:.{d}f}, {t[2]:.{d}f}]"

    pw, aw = col("person_weeks"), col("adult_weeks")
    py, ay = pw / WPY, aw / WPY
    weeks = np.array([float(runs[s]["final_tick"]) for s in seeds])
    ext = sum(1 for s in seeds if runs[s]["extinct"])
    L += [f"Worlds: {n}; extinct {ext}. Mean living population {pw.sum() / weeks.sum():.1f}; "
          f"{py.sum():,.0f} person-years, {ay.sum():,.0f} adult-years.", ""]

    def pair_cols(r):
        rep = np.array([float(sum(k * m for k, m in runs[s]["pair_hist"][r] if k >= SHARED_MIN)) for s in seeds])
        all_ = np.array([float(sum(k * m for k, m in runs[s]["pair_hist"][r])) for s in seeds])
        return rep, all_

    # Q1-Q3 table
    L += ["## Q1–Q3 — Shared attention, gaps and decision-relevant gaps, by referent", "",
          "| referent | shared moments (both adults) per adult-year | share in pairs with ≥ 5 | clutter (instances both "
          "see) | gaps per adult-year | **decision-relevant gaps per adult-year** | relevant ÷ gaps |",
          "|---|---|---|---|---|---|---|"]
    summary = {}
    for r in REFS:
        sh = ratio(col(f"{r}_shared_adults"), ay)
        rep, all_ = pair_cols(r)
        rp = ratio(rep, all_)
        clutter = col(f"{r}_shared_clutter").sum() / max(1.0, col(f"{r}_shared").sum())
        gp = ratio(col(f"{r}_gap"), ay)
        rel = ratio(col(f"{r}_relevant"), ay)
        share = ratio(col(f"{r}_relevant"), col(f"{r}_gap"))
        summary[r] = (sh[0], rp[0], rel[0])
        L.append(f"| {r} | {fmt(sh, 2)} | {fmt(rp)} | {clutter:.1f} | {fmt(gp, 2)} | **{fmt(rel, 3)}** | "
                 f"{fmt(share)} |")
    L += ["", "Counts summed over all worlds:", "",
          "| referent | shared talks (all ages) | gaps | decision-relevant gaps |", "|---|---|---|---|"]
    for r in REFS:
        L.append(f"| {r} | {col(f'{r}_shared').sum():,.0f} | {col(f'{r}_gap').sum():,.0f} | "
                 f"{col(f'{r}_relevant').sum():,.0f} |")
    ages = ["0-4", "5-8", "9-12"]
    g_ages = [col(f"game_gap_age_{a}").sum() for a in ages]
    tot = sum(g_ages) or 1.0
    L += ["", "Game gaps by the age of the freshest sighting: " +
          ", ".join(f"{a} weeks {v / tot:.3f}" for a, v in zip(ages, g_ages)) + ".", ""]

    # The frozen ranking
    workable = [r for r in REFS if summary[r][0] >= WORKABLE_SHARED and summary[r][1] >= WORKABLE_REP
                and summary[r][2] >= WORKABLE_GAPS]
    L += ["## The frozen ranking (a screen, not a law of language)", ""]
    for r in REFS:
        sh, rp, rel = summary[r]
        L.append(f"- **{r}:** shared {sh:.2f} per adult-year (needs ≥ {WORKABLE_SHARED:g}), repeated pairs {rp:.3f} "
                 f"(needs ≥ {WORKABLE_REP:g}), decision-relevant gaps {rel:.3f} per adult-year (needs ≥ "
                 f"{WORKABLE_GAPS:g}): **{'workable' if r in workable else 'not workable'}**")
    if workable:
        best = max(workable, key=lambda r: summary[r][2])
        L += ["", f"**Proposed first referent: {best}.**" + (
            " A game-signal study must carry a flag on hunting and food, because today's game telling does real work."
            if best == "game" else "")]
    else:
        L += ["", "**No referent is workable:** ACL today has no referent where a learned signal could both be grounded "
              "and be useful. The next question is the creator's (which law change would create a real need, judged "
              "against human evidence, not tuned)."]
    L.append("")

    # Q4 today's game channel
    tg = {k: np.array([float(runs[s]["told_game"][k]) for s in seeds]) for k in
          ("accepted", "out_of_sight", "used", "used_out_of_sight")}
    acc_n = col("g_accepted")
    L += ["## Q4 — Today's game channel (described)", "",
          f"- Accepted game places: {acc_n.sum():,.0f} of {col('g_offered').sum():,.0f} offered; "
          f"{fmt(ratio(acc_n, py, 1000.0), 1)} per 1,000 person-years.",
          f"- Listener-places later chosen as a destination: {fmt(ratio(tg['used'], tg['accepted']))} of "
          f"{tg['accepted'].sum():,.0f}; for spots out of sight at the telling: "
          f"{fmt(ratio(tg['used_out_of_sight'], tg['out_of_sight']))} of {tg['out_of_sight'].sum():,.0f}.",
          f"- Chosen options going to a told game place: {fmt(ratio(col('chose_told_game'), col('chosen')), 4)} "
          f"({col('chose_told_game').sum():,.0f} of {col('chosen').sum():,.0f}); an upper bound.",
          f"- Of those, reached the target tile: {fmt(ratio(col('chose_told_game_reached'), col('chose_told_game')))}; "
          f"then saw a game group: {fmt(ratio(col('chose_told_game_sees_game'), col('chose_told_game')))}."]
    bands = ["0-4", "5-8", "9-12", "older", "relayed"]
    a_b = [col(f"g_acc_age_{b}").sum() for b in bands]
    tb = sum(a_b) or 1.0
    L += ["- Accepted game places by the age of the speaker's own sighting: " +
          ", ".join(f"{b} {v / tb:.3f}" for b, v in zip(bands, a_b)) + ".", ""]

    # Q5 danger
    L += ["## Q5 — Danger outcomes (described)", "",
          f"- Maulings: {col('maulings').sum():,.0f}; {fmt(ratio(col('maulings'), py, 1000.0), 2)} per 1,000 "
          f"person-years.",
          f"- Maulings in which the victim had been the listener in a danger gap about the same group in the 4 weeks "
          f"before: {fmt(ratio(col('maulings_after_gap'), col('maulings')))}.",
          f"- Decision-relevant danger gaps followed by a near miss (within 2 tiles of that group within 2 weeks): "
          f"{fmt(ratio(col('danger_near_miss'), col('danger_relevant')))} of {col('danger_relevant').sum():,.0f}.", ""]

    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
