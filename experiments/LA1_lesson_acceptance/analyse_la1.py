"""LA1 analysis, written before any data (questions.md, frozen as `LA1-frozen`; operational note 1).

  python experiments/LA1_lesson_acceptance/analyse_la1.py            # writes results.md
  python experiments/LA1_lesson_acceptance/analyse_la1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_la1 import PARTS, SEEDS  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261027)
ERAS = ["0-50", "50-100", "100-200"]
EARLY, LATE = 0, 2
if "--smoke-late" in sys.argv:
    LATE = 0


def parse(k):
    era, origin, useful, rel, age = k.split("|")
    return int(era), origin, int(useful), rel, age


def pool(worlds, sel):
    t = Counter()
    for r in worlds:
        for k, c in r["cells"].items():
            if sel(parse(k)):
                t.update(c)
    return t


def primary(p):
    return p[1] == "worldborn" and p[2] == 1


def ci(reps):
    reps = np.asarray([x for x in reps if np.isfinite(x)])
    if not len(reps):
        return "[-]"
    lo, hi = np.percentile(reps, [2.5, 97.5])
    return f"[{lo:.3g}, {hi:.3g}]"


def terms(t):
    n = t["offered"]
    a1 = n - t["g1"]
    a2 = a1 - t["g2"]
    if not n or not a1 or not a2 or not t["sum_p"]:
        return None
    return {"T1 passes G1 (not known)": a1 / n, "T2 passes G2 (not tried-and-bad)": a2 / a1,
            "T3 mean p at G3": t["sum_p"] / a2, "T4 passes G4 (can follow; p-weighted)": t["sum_pf"] / t["sum_p"]}


def decompose(worlds):
    e = pool(worlds, lambda p: primary(p) and p[0] == EARLY)
    l_ = pool(worlds, lambda p: primary(p) and p[0] == LATE)
    te, tl = terms(e), terms(l_)
    if te is None or tl is None:
        return None
    d = {k: math.log(tl[k] / te[k]) for k in te}
    d["total"] = sum(d.values())
    return d, te, tl, e, l_


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rs = [json.load(open(f)) for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json")))]
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    fps = {r["code_hash"] for r in rs} | {r["code_hash_after"] for r in rs}
    mism = sum(sum(r["mismatch"].values()) for r in rs)
    ok = "All: PASS" in zero and sorted(r["seed"] for r in rs) == sorted(SEEDS) and len(fps) == 1 and mism == 0
    L = ["# LA1 — Why are lessons refused? Results", "",
         "Frozen as `LA1-frozen` (operational note 1). run_la1.py, analyse_la1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({len(rs)} of {len(SEEDS)}): **{'yes' if sorted(r['seed'] for r in rs) == sorted(SEEDS) else 'NO'}**",
         f"- One fingerprint (`code_v7`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Credence replays exactly and every outcome matches its gate (mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**",
         "", f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    # Q1
    L += ["## Q1 — The rejection funnel (world-born useful kinds; all ages)", "",
          "| era | offered | G1 known | G2 tried-and-bad | G3 not taken up | G4 cannot follow (part shown) | taken | "
          "taken exactly as meant | taken, then pushed out of a full memory | overlapping: known / tried-and-bad / "
          "cannot follow | shown as a variant | part lessons |", "|---" * 12 + "|"]
    for e, name in enumerate(ERAS):
        t = pool(rs, lambda p: primary(p) and p[0] == e)
        n = t["offered"]
        if not n:
            continue
        L.append(f"| {name} | {n:.0f} | {t['g1'] / n:.3f} | {t['g2'] / n:.3f} | {t['g3'] / n:.3f} | {t['g4'] / n:.3f} | "
                 f"{t['taken'] / n:.4f} | {t['taken_exact'] / n:.4f} | {t['taken_pushed_out'] / max(t['taken'], 1):.3f} of taken | "
                 f"{t['known'] / n:.3f} / {t['bad_any'] / n:.3f} / {t['nofollow_any'] / n:.3f} | {t['variant'] / n:.3f} | "
                 f"{t['part_lessons']:.0f} |")
    L.append("")
    # Q2
    L += ["## Q2 — Threshold margins (lessons reaching G3)", "",
          "| era | reached G3 | mean p | p < 0.05 | p < 0.10 | p < 0.20 | mean credence | mean openness | parent lessons | "
          + " | ".join(f"credence: {k}" for k in PARTS) + " |", "|---" * (9 + len(PARTS)) + "|"]
    for e, name in enumerate(ERAS):
        t = pool(rs, lambda p: primary(p) and p[0] == e)
        n = t["reached_g3"]
        if not n:
            continue
        L.append(f"| {name} | {n:.0f} | {t['sum_p'] / n:.3f} | {t['p_lt05'] / n:.3f} | {t['p_lt10'] / n:.3f} | "
                 f"{t['p_lt20'] / n:.3f} | {t['sum_c'] / n:.3f} | {t['sum_o'] / n:.3f} | {t['parent_double'] / n:.3f} | "
                 + " | ".join(f"{t[f'cpart_{k}'] / n:+.3f}" for k in PARTS) + " |")
    L.append("")
    # Q3
    L += ["## Q3 — Acceptance and mean p by kind, relation and age", "",
          "| group | offered | taken / offered | mean p at G3 |", "|---|---|---|---|"]
    groups = [("founder kinds, useful", lambda p: p[1] == "founder" and p[2] == 1),
              ("world-born kinds, useful", lambda p: p[1] == "worldborn" and p[2] == 1),
              ("world-born kinds, not useful", lambda p: p[1] == "worldborn" and p[2] == 0)]
    for rel in ("parent", "carer", "kin", "other"):
        groups.append((f"world-born useful, teacher is {rel}", lambda p, rel=rel: primary(p) and p[3] == rel))
    for age in ("child", "teen", "adult"):
        groups.append((f"world-born useful, learner {age}", lambda p, age=age: primary(p) and p[4] == age))
    for e, name in enumerate(ERAS):
        groups.append((f"world-born useful, years {name}", lambda p, e=e: primary(p) and p[0] == e))
    for name, sel in groups:
        t = pool(rs, sel)
        if t["offered"]:
            L.append(f"| {name} | {t['offered']:.0f} | {t['taken'] / t['offered']:.4f} | "
                     f"{t['sum_p'] / max(t['reached_g3'], 1):.3f} |")
    L.append("")
    # Q4
    out = decompose(rs)
    if out:
        d, te, tl, e, l_ = out
        reps = defaultdict(list)
        for row in RNG.integers(0, len(rs), size=(REPS, len(rs))):
            o = decompose([rs[k] for k in row])
            if o:
                for k_, v in o[0].items():
                    reps[k_].append(v)
        L += ["## Q4 — Why acceptance falls after year 50 (primary; years 0-50 against 100-200; world-born useful kinds)", "",
              "Expected acceptance P(taken) = T1 × T2 × T3 × T4 (p's expectation, not the random draw).", "",
              "| term | years 0-50 | years 100-200 | Δ ln | share of the fall |", "|---|---|---|---|---|"]
        for k_ in te:
            L.append(f"| {k_} | {te[k_]:.4f} | {tl[k_]:.4f} | {d[k_]:+.3f} {ci(reps[k_])} | {(d[k_] / d['total'] if d['total'] else float('nan')):.2f} |")
        L += [f"| **P(taken), expected** | {math.prod(te.values()):.4f} | {math.prod(tl.values()):.4f} | "
              f"{d['total']:+.3f} {ci(reps['total'])} | 1.00 |", ""]
        largest = min(te, key=lambda k_: d[k_])            # the most negative Δ ln carries the largest share of a fall
        L += [f"**The term carrying the largest share of the fall: {largest}.**", ""]
        # E[p] split: E[c·o] = Shapley(E[c], E[o]) + covariance; E[c] = sum of parts
        ne, nl = e["reached_g3"], l_["reached_g3"]
        ce, cl, oe, ol = e["sum_c"] / ne, l_["sum_c"] / nl, e["sum_o"] / ne, l_["sum_o"] / nl
        pe, pl = e["sum_p"] / ne, l_["sum_p"] / nl
        sh_c = 0.5 * ((cl - ce) * oe + (cl - ce) * ol)
        sh_o = 0.5 * ((ol - oe) * ce + (ol - oe) * cl)
        cov = (pl - pe) - sh_c - sh_o
        L += [f"Mean p at G3: {pe:.4f} → {pl:.4f} (Δ {pl - pe:+.4f}) = credence part {sh_c:+.4f} + openness part "
              f"{sh_o:+.4f} + covariance {cov:+.4f}.", "",
              "Mean credence by part: " + "; ".join(
                  f"{k} {e[f'cpart_{k}'] / ne:+.3f} → {l_[f'cpart_{k}'] / nl:+.3f}" for k in PARTS)
              + f" (total {ce:.3f} → {cl:.3f}).", ""]
    # Q5
    t = pool(rs, lambda p: primary(p) and p[0] == LATE)
    if t["cf_n"]:
        a = t["cf_actual"]
        L += ["## Q5 — Counterfactual gate replay (diagnostic; years 100-200, world-born useful kinds)", "",
              f"Over the {t['cf_n']:.0f} lessons reaching G3 with an early match ({t['cf_missing']:.0f} without one), "
              f"expected lessons taken: actual {a:.1f}.", "",
              "| set back alone | expected taken | × actual |", "|---|---|---|",
              f"| (a) p to its years 0-50 mean (same relation and learner age) | {t['cf_p']:.1f} | {t['cf_p'] / a:.2f} |",
              f"| (b) credence alone | {t['cf_c']:.1f} | {t['cf_c'] / a:.2f} |",
              f"| (c) openness alone | {t['cf_o']:.1f} | {t['cf_o'] / a:.2f} |",
              f"| (d) G1 removed (all lessons in the era) | {t['exp_taken'] + t['cf_nog1_extra']:.1f} | "
              f"{(t['exp_taken'] + t['cf_nog1_extra']) / max(t['exp_taken'], 1e-9):.2f} (against {t['exp_taken']:.1f}) |",
              f"| (e) G4 removed (all lessons in the era) | {t['cf_nog4']:.1f} | {t['cf_nog4'] / max(t['exp_taken'], 1e-9):.2f} "
              f"(against {t['exp_taken']:.1f}) |", ""]
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
