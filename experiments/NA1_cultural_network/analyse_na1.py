"""NA1 analysis, written before any data (questions.md, frozen as `NA1-frozen`; operational note 1).

  python experiments/NA1_cultural_network/analyse_na1.py            # writes results.md
  python experiments/NA1_cultural_network/analyse_na1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_na1 import ERAS, SEEDS, WPY  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261027)
ERA_NAMES = ["0-50", "50-100", "100-200"]
# kind row: 0 first, 1 founder, 2 era, 3 inventor death, 4 factor, 5 knowers ever, 6-9 inventor cop/talk/off/took,
# 10-13 any cop/talk/off/took, 14 made, 15 passed, 16 took a variant
INV = {"co-present": 6, "talked": 7, "offered": 8, "took": 9}
ANY = {"co-present": 10, "talked": 11, "offered": 12, "took": 13, "made": 14, "passed": 15}
STEPS = list(ANY)


def ci(reps):
    reps = np.asarray([x for x in reps if np.isfinite(x)])
    if not len(reps):
        return "[-]"
    lo, hi = np.percentile(reps, [2.5, 97.5])
    return f"[{lo:.3g}, {hi:.3g}]"


def wb(r, era=None):
    return [k for k in r["kinds"] if k[1] == 0 and k[0] >= 0 and (era is None or k[2] == era)]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rs = [json.load(open(f)) for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json")))]
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    fps = {r["code_hash"] for r in rs} | {r["code_hash_after"] for r in rs}
    mism = sum(sum(r["mismatch"].values()) for r in rs)
    ok = "All: PASS" in zero and sorted(r["seed"] for r in rs) == sorted(SEEDS) and len(fps) == 1 and mism == 0
    L = ["# NA1 — Who actually gets a chance to learn? Results", "",
         "Frozen as `NA1-frozen` (operational note 1). run_na1.py, analyse_na1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({len(rs)} of {len(SEEDS)}): **{'yes' if sorted(r['seed'] for r in rs) == sorted(SEEDS) else 'NO'}**",
         f"- One fingerprint (`code_v7`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Internal checks (non-knowers only; took only in a lesson; each stage within the one before): "
         f"**{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    L += ["## Population and people within reach (aged 4+; worlds alive in the era)", "",
          "| era (years) | worlds | mean population | people within reach (mean) |", "|---|---|---|---|"]
    edges = (0,) + ERAS
    for e, name in enumerate(ERA_NAMES):
        al = [r for r in rs if r["final_tick"] > edges[e] * WPY]
        wk = (edges[e + 1] - edges[e]) * WPY
        pw = sum(r["pop"].get(f"{e}|pw", 0) for r in al)
        L.append(f"| {name} | {len(al)} | {np.mean([r['pop'].get(f'{e}|pw', 0) / wk for r in al]) if al else float('nan'):.1f} | "
                 f"{sum(r['pop'].get(f'{e}|near', 0) for r in al) / max(pw, 1):.2f} |")
    L.append("")
    # Q1
    L += ["## Q1 — The effective network, per useful world-born kind", "",
          "Distinct non-knowers (aged 4+) reaching each stage: with the inventor (while alive) and with any knower (the "
          "kind's whole life). Mean / median / share of kinds with none.", "",
          "| era | kinds | " + " | ".join(f"inventor: {s}" for s in INV) + " | " + " | ".join(f"any: {s}" for s in ANY)
          + " | any: took a variant |", "|---" * (3 + len(INV) + len(ANY)) + "|"]
    for e, name in enumerate(ERA_NAMES):
        ks = np.array([k for r in rs for k in wb(r, e)], float)
        if not len(ks):
            continue
        cell = lambda j: f"{ks[:, j].mean():.2f} / {np.median(ks[:, j]):.0f} / {np.mean(ks[:, j] == 0):.2f}"  # noqa: E731
        L.append(f"| {name} | {len(ks)} | " + " | ".join(cell(j) for j in INV.values()) + " | "
                 + " | ".join(cell(j) for j in ANY.values()) + f" | {cell(16)} |")
    fk = np.array([k for r in rs for k in r["kinds"] if k[1] == 1], float)
    if len(fk):
        L += ["", "Founders' kinds (described): " + ", ".join(f"any {s} {fk[:, j].mean():.2f}" for s, j in ANY.items())
              + f" ({len(fk)} kinds)."]
    L.append("")
    # Q2
    L += ["## Q2 — The funnel (primary): pooled over world-born useful kinds, any knower, whole life", ""]
    for e, name in [(None, "all eras")] + list(enumerate(ERA_NAMES)):
        per_world = np.array([[sum(k[j] for k in wb(r, e)) for j in ANY.values()] for r in rs], float)
        tot = per_world.sum(0)
        L += [f"**{name}**: " + ", ".join(f"{s} {int(t)}" for s, t in zip(STEPS, tot)) + ".", "",
              "| step | rate | ln rate |", "|---|---|---|"]
        lns = []
        ix = RNG.integers(0, len(rs), size=(REPS if e is None else 0, len(rs)))
        for i in range(1, len(STEPS)):
            rate = tot[i] / tot[i - 1] if tot[i - 1] else float("nan")
            ln = math.log(rate) if rate and rate > 0 else (-math.inf if rate == 0 else float("nan"))
            lns.append(ln)
            extra = ""
            if e is None and len(ix):
                num, den = per_world[ix, i].sum(1), per_world[ix, i - 1].sum(1)
                with np.errstate(divide="ignore", invalid="ignore"):
                    extra = " " + ci(num / den)
            L.append(f"| {STEPS[i - 1]} → {STEPS[i]} | {rate:.4f}{extra} | "
                     f"{'fell to zero' if ln == -math.inf else f'{ln:.3f}'} |")
        finite = [(x, i) for i, x in enumerate(lns) if np.isfinite(x) or x == -math.inf]
        if finite:
            x, i = min(finite)
            L += ["", f"**The step with the largest loss ({name}): {STEPS[i]} → {STEPS[i + 1]}"
                  + (" (fell to zero)" if x == -math.inf else "") + ".**", ""]
    # Q3
    allk = [k for r in rs for k in wb(r)]
    rat = [x for r in rs for x in r["ratchet"]]
    done = [x for x in rat if x[7] is not None]
    L += ["## Q3 — The ratchet ledger (A → B → C, B improving a kind learned socially)", "",
          f"- World-born useful kinds: {len(allk)}. Improvements by a social learner (B): {len(rat)} "
          f"({1000 * len(rat) / max(len(allk), 1):.2f} per 1,000 kinds). **Completed A→B→C chains: {len(done)} "
          f"({1000 * len(done) / max(len(allk), 1):.2f} per 1,000 kinds).**"]
    for e, name in enumerate(ERA_NAMES):
        re_ = [x for x in rat if edges[e] * WPY <= x[0] < edges[e + 1] * WPY]
        de = [x for x in re_ if x[7] is not None]
        L.append(f"- {name}: improvements {len(re_)}, completed {len(de)}")
    if rat:
        L.append(f"- Factor gained by the improvement (mean): {np.mean([x[6] - x[5] for x in rat]):+.3f}.")
    L.append("")
    # Q4
    L += ["## Q4 — Network against population (described; worlds × eras)", "",
          "| era | worlds | mean population | mean reach (any co-present per kind) | mean took per kind |", "|---|---|---|---|---|"]
    xs, ys = [], []
    for e, name in enumerate(ERA_NAMES):
        rows = []
        for r in rs:
            ks = wb(r, e)
            if not ks:
                continue
            wk = (edges[e + 1] - edges[e]) * WPY
            pop = r["pop"].get(f"{e}|pw", 0) / wk
            rows.append((pop, np.mean([k[10] for k in ks]), np.mean([k[13] for k in ks])))
            xs.append(pop)
            ys.append(np.mean([k[10] for k in ks]))
        if rows:
            a = np.array(rows)
            L.append(f"| {name} | {len(rows)} | {a[:, 0].mean():.1f} | {a[:, 1].mean():.2f} | {a[:, 2].mean():.3f} |")
    if len(xs) > 3:
        rx, ry = np.argsort(np.argsort(xs)), np.argsort(np.argsort(ys))
        L += ["", f"Rank correlation of population with a kind's mean reach, across world-eras: {np.corrcoef(rx, ry)[0, 1]:.2f} "
              f"({len(xs)} world-eras; described)."]
    L.append("")
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
