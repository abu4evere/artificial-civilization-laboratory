"""LK1 analysis in the frozen order (questions.md, `LK1-frozen`). Written and smoke-tested on the pilot's outputs before
any main-run data.

Operational details (written before data):
- Extinct, as every study: the world does not reach year 120 with someone alive (12 decade marks, the last above 0).
- Primary: M against C, paired by seed; exact two-sided sign test on worlds that differ; effect = C's extinction share
  minus M's (positive = fewer extinctions without current-location knowledge); 95% percentile bootstrap over seeds,
  10,000 resamples, random.Random(2026); half of F2's effect = (1 − F2's ÷ F1's extinctions on F1's 64 seeds) ÷ 2 ×
  C's extinction share. Reading as frozen.
- Secondary, per world, then paired Wilcoxon signed-rank (scipy, two-sided, zero differences dropped), M against C:
  pairings per eligible single-year; median weeks from becoming an eligible single to pairing; share of partner-weeks
  and of mother–child-weeks (child under 16) spent beyond sight; median length of a spell apart; births per woman-year
  (F1's definition); A6c (share of partner-search go-to moves aimed beyond sight). Pooled values per arm beside them.
- Manipulation, in the main run itself: M's go-to moves toward an out-of-sight loved one's current tile must total 0.

  python experiments/LK1_location_knowledge/analyse_lk1.py            # main run (writes results.md)
  python experiments/LK1_location_knowledge/analyse_lk1.py --smoke    # pilot outputs, arms C and M only
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "F1_baseline_fragility"))
sys.path.insert(0, str(EXP / "MC1L_moving_camp_large"))
import analyse_f1 as A  # noqa: E402
from analyse_mc1l import F1_SEEDS, ext_file, load, sign_test  # noqa: E402

SEEDS = tuple(range(4001, 4257))
NAMES = {"c": "C (current location)", "m": "M (last seen)", "s": "S sham"}


def boot(d):
    rng = random.Random(2026)
    b = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(10000))
    return b[249], b[9749]


def per_world(r):
    a, b = r["audit"], r["bonds"]
    n = b["n"]
    end = (r["E"] + 1) if r["extinct"] else 120
    rate = A.rates(None, [(r, 0, end)])
    med = lambda xs: statistics.median(xs) if xs else None  # noqa: E731
    div = lambda x, y: x / y if y else None  # noqa: E731
    return {
        "pairings_per_single_year": div(n.get("pairings", 0), n.get("single_weeks", 0) / 52),
        "weeks_to_pairing": med(b["wait"]),
        "partner_apart_share": div(n.get("partner_weeks_apart", 0), n.get("partner_weeks", 0)),
        "mother_child_apart_share": div(n.get("mother_child_weeks_apart", 0), n.get("mother_child_weeks", 0)),
        "partner_spell": med(b["spells"]["partner"]),
        "mother_child_spell": med(b["spells"]["mother_child"]),
        "births_per_woman_year": rate.get("births_per_woman_year"),
        "a6c_share": div(a.get("joins_seek_beyond_sight", 0), a.get("joins_seek", 0)),
    }


def pooled(R):
    n, ab, wait, sp = Counter(), Counter(), [], {"partner": [], "mother_child": []}
    for r in R.values():
        n.update(r["bonds"]["n"])
        ab.update({k: v for k, v in r["audit"].items() if isinstance(v, (int, float))})
        wait += r["bonds"]["wait"]
        for k in sp:
            sp[k] += r["bonds"]["spells"][k]
    end = lambda r: (r["E"] + 1) if r["extinct"] else 120  # noqa: E731
    rate = A.rates(None, [(r, 0, end(r)) for r in R.values()])
    div = lambda x, y: x / y if y else float("nan")  # noqa: E731
    med = lambda xs: statistics.median(xs) if xs else float("nan")  # noqa: E731
    return {
        "pairings_per_single_year": div(n["pairings"], n["single_weeks"] / 52),
        "weeks_to_pairing": med(wait),
        "partner_apart_share": div(n["partner_weeks_apart"], n["partner_weeks"]),
        "mother_child_apart_share": div(n["mother_child_weeks_apart"], n["mother_child_weeks"]),
        "partner_spell": med(sp["partner"]),
        "mother_child_spell": med(sp["mother_child"]),
        "births_per_woman_year": rate.get("births_per_woman_year", float("nan")),
        "a6c_share": div(ab["joins_seek_beyond_sight"], ab["joins_seek"]),
        "_a5_beyond": ab["joins_loved_beyond_sight"], "_mem": ab["joins_loved_mem"], "_joins": ab["joins"],
    }


LABELS = {"pairings_per_single_year": "pairings per eligible single-year",
          "weeks_to_pairing": "median weeks from eligible single to pairing",
          "partner_apart_share": "share of partner-weeks spent beyond sight",
          "mother_child_apart_share": "share of mother–child-weeks (child under 16) beyond sight",
          "partner_spell": "median spell apart, partners (weeks)",
          "mother_child_spell": "median spell apart, mother and child (weeks)",
          "births_per_woman_year": "births per woman-year",
          "a6c_share": "A6c: partner-search moves aimed beyond sight"}


def main(out=HERE / "output", seeds=SEEDS, arms=("c", "m", "s"), write=True, f1_ref=True):
    D = {a: load(out, seeds, a) for a in arms}
    L = []
    w = L.append
    w("# LK1 — Location knowledge: results\n")
    w(f"Frozen as `LK1-frozen`. {len(seeds)} seeds ({seeds[0]}–{seeds[-1]}), 20 founders, 40 × 40, 120 years; arms: "
      + ", ".join(NAMES[a] for a in arms) + ". `code_lk1`.\n")
    z = (out / "zero.txt")
    zero_ok = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    hashes = {r["code_hash"] for R in D.values() for r in R.values()} | {r["code_hash_after"] for R in D.values()
                                                                         for r in R.values()}
    P = {a: pooled(D[a]) for a in arms}
    manip = P["m"]["_a5_beyond"] == 0 and P["m"]["_mem"] > 0 if "m" in P else False
    w("## Validity\n")
    w(f"- Zero checks: **{'yes' if zero_ok else 'no'}**")
    w(f"- Code unchanged in every world (one fingerprint): **{'yes' if len(hashes) == 1 else 'no'}**")
    w(f"- Manipulation in the main run (M: {P['m']['_a5_beyond']} moves toward an out-of-sight loved one's current "
      f"tile, must be 0; {P['m']['_mem']} toward remembered tiles): **{'yes' if manip else 'no'}**")
    valid = zero_ok and len(hashes) == 1 and manip
    w(f"\n**{'Valid.' if valid else 'NOT VALID: no outcome is read.'}**\n")
    ext = {a: sum(r["extinct"] for r in D[a].values()) for a in arms}
    w("## Baseline (rule 14)\n")
    w(f"C died out in {ext['c']} of {len(seeds)} worlds ({ext['c'] / len(seeds):.1%}).\n")
    w("## Outcomes (population beside every measure, rule 18)\n")
    w("| | " + " | ".join(NAMES[a] for a in arms) + " |")
    w("|---|" + "---|" * len(arms))
    w("| **worlds died out** | " + " | ".join(f"**{ext[a]}**" for a in arms) + " |")
    w("| median population, year 119 | " + " | ".join(
        f"{statistics.median(r['Y'].get(119, {}).get('n', 0) for r in D[a].values()):.0f}" for a in arms) + " |")
    w("| A5: share of go-to moves toward an out-of-sight loved one's current tile | " + " | ".join(
        f"{P[a]['_a5_beyond'] / P[a]['_joins']:.3f}" if P[a]["_joins"] else "–" for a in arms) + " |")
    w("| go-to moves toward a remembered tile | " + " | ".join(str(P[a]["_mem"]) for a in arms) + " |")
    for k, lab in LABELS.items():
        w(f"| {lab} | " + " | ".join(f"{P[a][k]:.3f}" for a in arms) + " |")
    if f1_ref:
        f1 = sum(ext_file(EXP / "F1_baseline_fragility" / "output" / f"seed_{s}.json") for s in F1_SEEDS)
        f2 = sum(ext_file(EXP / "F2_perfect_search" / "output" / f"seed_{s}.json") for s in F1_SEEDS)
        rel = 1 - f2 / f1
    else:
        rel = 0.68
    w("\n## The primary question: does knowing where absent loved ones are change survival? (M against C)\n")
    C, M = D["c"], D["m"]
    saved = sum(1 for s in seeds if C[s]["extinct"] and not M[s]["extinct"])
    lost = sum(1 for s in seeds if not C[s]["extinct"] and M[s]["extinct"])
    p = sign_test(saved, lost)
    d = [int(C[s]["extinct"]) - int(M[s]["extinct"]) for s in seeds]
    eff, (lo, hi) = sum(d) / len(d), boot(d)
    half = rel / 2 * ext["c"] / len(seeds)
    if p < 0.05 and eff > 0:
        v = "**fewer extinctions without current-location knowledge**: knowing where loved ones are *harms* survival (unexpected; examined read-only)"
    elif p < 0.05 and eff < 0:
        v = "**current-location knowledge holds worlds together**; its size is the effect estimate"
    elif max(abs(lo), abs(hi)) < half:
        v = "**no meaningful effect on survival** (the interval excludes half of F2's effect)"
    else:
        v = "**unresolved** at this sample"
    w(f"Died out: M {ext['m']} vs C {ext['c']}; saved / lost {saved} / {lost}; exact sign test **p = {p:.3g}**. "
      f"Effect (C − M extinction share) {eff:+.3f}, 95% interval [{lo:+.3f}, {hi:+.3f}]; half of F2's effect "
      f"{half:.3f}.\n")
    w(f"Frozen rule: {v}." if valid else "Frozen rule: not read (the run is not valid).")
    if "s" in D:
        S = D["s"]
        ss = sum(1 for s in seeds if C[s]["extinct"] and not S[s]["extinct"])
        sl = sum(1 for s in seeds if not C[s]["extinct"] and S[s]["extinct"])
        sp = sign_test(ss, sl)
        ds = [int(C[s]["extinct"]) - int(S[s]["extinct"]) for s in seeds]
        slo, shi = boot(ds)
        w(f"\nSham against C: died out {ext['s']} vs {ext['c']}; {ss} / {sl}; p = {sp:.3g}; effect "
          f"{sum(ds) / len(ds):+.3f} [{slo:+.3f}, {shi:+.3f}]"
          + (" — **caveat (frozen): the sham reached p < 0.05.**" if sp < 0.05 else "."))
    w("\n## Secondary measures, per world (M against C; paired Wilcoxon; described, not thresholded)\n")
    w("| measure | C median | M median | paired Wilcoxon p | worlds with both |")
    w("|---|---|---|---|---|")
    from scipy.stats import wilcoxon
    for k, lab in LABELS.items():
        pairs = [(per_world(C[s])[k], per_world(M[s])[k]) for s in seeds]
        pairs = [(x, y) for x, y in pairs if x is not None and y is not None]
        diffs = [y - x for x, y in pairs if y != x]
        try:
            pw = wilcoxon(diffs).pvalue if len(diffs) > 0 else 1.0
        except ValueError:
            pw = 1.0
        cm = statistics.median(x for x, _ in pairs) if pairs else float("nan")
        mm = statistics.median(y for _, y in pairs) if pairs else float("nan")
        w(f"| {lab} | {cm:.3f} | {mm:.3f} | {pw:.3g} | {len(pairs)} |")
    text = "\n".join(L) + "\n"
    if write:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        po = HERE / "output_pilot"
        main(out=po, seeds=tuple(range(9201, 9205)), arms=("c", "m"), write=False)
    else:
        main()
