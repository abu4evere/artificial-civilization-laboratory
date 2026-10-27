"""PT1 analysis, written before any data (questions.md, frozen as `PT1-frozen`; operational note 1).

  python experiments/PT1_parts_teaching/analyse_pt1.py            # writes results.md
  python experiments/PT1_parts_teaching/analyse_pt1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_pt1 import SEEDS  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261027)
ERAS = ["0-50", "50-100", "100-200"]
CLS = ("none", "wrong", "deep", "reach")
STEPS = [("pt", "part shown and taken"), ("pk", "part kept (not pushed out)"), ("pm", "part made"),
         ("ah", "every missing part held"), ("wt", "whole taken again"), ("wm", "whole made")]


def ci(reps):
    reps = np.asarray([x for x in reps if np.isfinite(x)])
    if not len(reps):
        return "[-]"
    lo, hi = np.percentile(reps, [2.5, 97.5])
    return f"[{lo:.3g}, {hi:.3g}]"


W = None


def weights(n):
    """World-bootstrap weights: how often each world is drawn, in each of REPS replicates (drawn once)."""
    global W
    if W is None:
        W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])
    return W


def ratio_boot(num, den):
    """Bootstrap of sum(num) / sum(den) over worlds; num and den are per-world arrays."""
    w = weights(len(num))
    with np.errstate(divide="ignore", invalid="ignore"):
        return (w @ np.asarray(num, float)) / (w @ np.asarray(den, float))


def fail_cells(r, era=None, primary=True):
    """Failure cells (era|origin|useful|cls), filtered."""
    t = {c: Counter() for c in CLS}
    for k, v in r["cells"].items():
        parts = k.split("|")
        if parts[0] in ("mem", "pop"):
            continue
        e, origin, useful, cls = int(parts[0]), parts[1], int(parts[2]), parts[3]
        if primary and not (origin == "worldborn" and useful == 1):
            continue
        if era is not None and e != era:
            continue
        t[cls].update(v)
    return t


def cls_shares(rs, era=None):
    tot = {c: 0.0 for c in CLS}
    for r in rs:
        t = fail_cells(r, era)
        for c in CLS:
            tot[c] += t[c]["fail"]
    n = sum(tot.values())
    return {c: (tot[c] / n if n else 0.0) for c in CLS}, n


def chains(r, primary=True):
    F = r["chain_fields"]
    idx = {f: i + 2 for i, f in enumerate(F)}
    out = []
    for c in r["chains"]:
        if primary and not (c[idx["origin"]] == "worldborn" and c[idx["useful"]] == 1):
            continue
        out.append({f: c[idx[f]] for f in F})
    return out


def funnel(rs):
    """Reachable chains (ever reachable): cumulative counts at each step, in order; censoring at each stop."""
    reached = [0] * (len(STEPS) + 1)
    died = [0] * len(STEPS)
    times = [[] for _ in STEPS]
    for r in rs:
        for ch in chains(r):
            if not ch["ever_reach"]:
                continue
            reached[0] += 1
            for i, (s, _) in enumerate(STEPS):
                if ch[s] is None:
                    if ch["end"] is not None:
                        died[i] += 1
                    break
                reached[i + 1] += 1
                times[i].append(ch[s] - ch["t0"])
    return reached, died, times


def mem_cells(rs, kind=None, primary=False):
    t = Counter()
    for r in rs:
        for k, v in r["cells"].items():
            parts = k.split("|")
            if parts[0] != "mem":
                continue
            _, e, origin, useful, which = parts
            if kind and which != kind:
                continue
            if primary and not (origin == "worldborn" and useful == "1"):
                continue
            t.update(v)
    return t


def pop(rs, era):
    s = n = 0.0
    for r in rs:
        c = r["cells"].get(f"pop|{era}", {})
        s += c.get("sum_pop", 0.0)
        n += c.get("years", 0.0)
    return s / n if n else float("nan")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rs = [json.load(open(f)) for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json")))]
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    fps = {r["code_hash"] for r in rs} | {r["code_hash_after"] for r in rs}
    mism = sum(sum(r["mismatch"].values()) for r in rs)
    seeds_ok = sorted(r["seed"] for r in rs) == sorted(SEEDS)
    ok = "All: PASS" in zero and seeds_ok and len(fps) == 1 and mism == 0
    L = ["# PT1 — Does parts-first teaching work? Results", "",
         "Frozen as `PT1-frozen` (operational note 1). run_pt1.py, analyse_pt1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({len(rs)} of {len(SEEDS)}): **{'yes' if seeds_ok else 'NO'}**",
         f"- One fingerprint (`code_v7`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Gate outcomes, part selection and eviction replay match the code (mismatches 0): "
         f"**{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    L += ["Mean population (living, sampled yearly): " + "; ".join(
        f"years {name}: {pop(rs, e):.1f}" for e, name in enumerate(ERAS)) + f" ({len(rs)} worlds).", ""]
    # Q1 shares
    L += ["## Q1 — Is the parts-first route reachable? (primary; G4 failures of world-born useful kinds)", "",
          "| era | G4 failures | (a) none: teacher knows no made part | (b) wrong: part shown already held | "
          "(c) deep: part shown needs a missing part | (d) reachable |", "|---|---|---|---|---|---|"]
    for e, name in [(None, "all")] + list(enumerate(ERAS)):
        sh, n = cls_shares(rs, e)
        if n:
            L.append(f"| {name} | {n:.0f} | " + " | ".join(f"{sh[c]:.3f}" for c in CLS) + " |")
    L.append("")
    per = [cls_shares([r])[1] for r in rs]
    reps = {c: ratio_boot([cls_shares([r])[0][c] * cls_shares([r])[1] if cls_shares([r])[1] else 0.0 for r in rs], per)
            for c in CLS}
    L += ["World bootstrap 95% (all eras): " + "; ".join(f"{c} {ci(reps[c])}" for c in CLS) + ".", ""]
    sh, n = cls_shares(rs)
    L += [f"**Share of G4 failures that parts-first can reach at all: {sh['reach']:.3f} {ci(reps['reach'])}.**", ""]
    # Q1 funnel
    reached, died, times = funnel(rs)
    if reached[0]:
        L += ["### The completion funnel (chains: one learner and one whole kind, ever reachable; followed until death "
              "or the run's end)", "",
              "| step | chains reaching it | conditional on the step before [95%] | stopped here by death | "
              "median weeks from the first G4 failure |", "|---|---|---|---|---|",
              f"| reachable G4 failure (start) | {reached[0]} | - | - | - |"]
        conds = []
        for i, (s, name) in enumerate(STEPS):
            c = reached[i + 1] / reached[i] if reached[i] else float("nan")
            conds.append(c)
            rp = ratio_boot([funnel([r])[0][i + 1] for r in rs], [funnel([r])[0][i] for r in rs])
            med = f"{np.median(times[i]):.0f}" if times[i] else "-"
            L.append(f"| {name} | {reached[i + 1]} | {c:.3f} {ci(rp)} | {died[i]} | {med} |")
        worst = min(range(len(STEPS)), key=lambda i: conds[i] if np.isfinite(conds[i]) else 9)
        L += ["", f"**The step with the largest loss among reachable chains: {STEPS[worst][1]} "
                  f"(conditional {conds[worst]:.3f}).**", ""]
        allc = [ch for r in rs for ch in chains(r)]
        L += [f"All world-born useful chains (any class): {len(allc)}; whole later held by any route "
              f"{sum(ch['wh'] is not None for ch in allc) / len(allc):.3f}; whole made "
              f"{sum(ch['wm'] is not None for ch in allc) / len(allc):.3f}.", ""]
    # Q2
    L += ["## Q2 — The selection rule (world-born useful)", "",
          "| era | G4 failures | wrong-part rate | teacher knew a missing part but showed another | "
          "teacher knows any missing part | mean p, whole lesson | reachable: part lesson G1 / G2 / G3 / G4 / taken "
          "| reachable: mean p, part lesson | reachable: part kept / taken |", "|---" * 9 + "|"]
    for e, name in [(None, "all")] + list(enumerate(ERAS)):
        tot = Counter()
        rch = Counter()
        for r in rs:
            t = fail_cells(r, e)
            for c in CLS:
                tot.update(t[c])
            rch.update(t["reach"])
        if not tot["fail"]:
            continue
        nr = sum(rch[f"pl_{g}"] for g in ("g1", "g2", "g3", "g4", "taken"))
        gates = " / ".join(f"{rch[f'pl_{g}'] / nr:.3f}" if nr else "-" for g in ("g1", "g2", "g3", "g4", "taken"))
        L.append(f"| {name} | {tot['fail']:.0f} | {tot_cls(rs, e, 'wrong') / tot['fail']:.3f} | "
                 f"{tot['teacher_knew_missing_other'] / tot['fail']:.3f} | {tot['teacher_knows_a_missing'] / tot['fail']:.3f} | "
                 f"{tot['whole_sum_p'] / tot['fail']:.3f} | {gates} | "
                 f"{rch['pl_sum_p'] / max(rch['pl_reached_g3'], 1):.3f} | "
                 f"{rch['pl_kept'] / max(rch['pl_taken'], 1):.3f} |")
    L.append("")
    # Q3
    L += ["## Q3 — Memory: lesson-added recipes that overflow the 12-recipe memory", "",
          "| lessons | kinds | overflows | evicted is the new lesson | mean evicted value | tied at the lowest value | "
          "evicted is composite / composite share held | replay (lesson value set first): new lesson survives | "
          "of evicted new lessons, would survive | mean lesson value / mean value evicted in replay | relearned | "
          "mean weeks to relearn |", "|---" * 12 + "|"]
    for kind in ("whole", "part"):
        for prim, lab in ((False, "all kinds"), (True, "world-born useful")):
            t = mem_cells(rs, kind, prim)
            n = t["n"]
            if not n:
                continue
            L.append(f"| {kind} | {lab} | {n:.0f} | {t['evict_new'] / n:.3f} | {t['sum_evicted_val'] / n:.4f} | "
                     f"{t['tied'] / n:.3f} | {t['evicted_composite'] / n:.3f} / {t['held_composite'] / n:.3f} | "
                     f"{t['replay_survive'] / n:.3f} | {t['replay_survive_if_evicted'] / max(t['evict_new'], 1):.3f} | "
                     f"{t['sum_lesson_val'] / n:.3f} / {t['sum_replay_evicted_val'] / n:.4f} | "
                     f"{t['relearned'] / n:.3f} | {t['sum_relearn_weeks'] / max(t['relearned'], 1):.0f} |")
    mw = [mem_cells([r], "whole") for r in rs]
    rp = ratio_boot([m["evict_new"] for m in mw], [m["n"] for m in mw])
    rp2 = ratio_boot([m["replay_survive"] for m in mw], [m["n"] for m in mw])
    L += ["", f"Whole lessons, all kinds, world bootstrap 95%: evicted is the new lesson {ci(rp)}; survives in the replay "
              f"{ci(rp2)}.", ""]
    # Q4
    L += ["## Q4 — Depth (G4 failures of world-born useful kinds)", "",
          "| era | G4 failures | levels needed: 1 | 2 | 3 or more | mean missing parts (direct) | "
          "mean missing parts (all levels) | needs two or more levels |", "|---" * 8 + "|"]
    for e, name in [(None, "all")] + list(enumerate(ERAS)):
        tot = Counter()
        for r in rs:
            for c, v in fail_cells(r, e).items():
                tot.update(v)
        n = tot["fail"]
        if not n:
            continue
        L.append(f"| {name} | {n:.0f} | {tot['depth_1'] / n:.3f} | {tot['depth_2'] / n:.3f} | {tot['depth_3'] / n:.3f} | "
                 f"{tot['nmiss_direct'] / n:.2f} | {tot['nmiss_all'] / n:.2f} | "
                 f"{(tot['depth_2'] + tot['depth_3']) / n:.3f} |")
    L.append("")
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


def tot_cls(rs, e, cls):
    return sum(fail_cells(r, e)[cls]["fail"] for r in rs)


if __name__ == "__main__":
    main()
