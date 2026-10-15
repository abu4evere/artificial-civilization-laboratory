"""NV2 analysis: v2 against v1 (questions.md, frozen as `NV2-frozen`). Written and smoke-tested before any data.

  python experiments/NV2_nature_v2/analyse_nv2.py            # writes results.md
  python experiments/NV2_nature_v2/analyse_nv2.py --smoke    # throwaway smoke output (10 years); writes nothing

Frozen reading, extinction (not reaching year 120 with someone alive), v2 against v1 paired by seed, exact sign test on
worlds that differ; effect = v1's extinction share − v2's, 95% bootstrap interval (10,000 resamples, random.Random(2026));
yardstick ±0.117 (half of F2's effect):
- p < 0.05: "v2 changes survival"; p ≥ 0.05 and the interval inside ±0.117: "no meaningful effect on survival";
  otherwise "unresolved at this sample". The sham against v1 must be quiet. No outcome is shown if the run is not valid.
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from pathlib import Path

from scipy.stats import binomtest, wilcoxon

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "F1_baseline_fragility"))
import analyse_f1 as A  # noqa: E402
from run_nv2 import ARMS, OUT, SEEDS  # noqa: E402

HALF_F2 = 0.117


def died(r):
    return r["final_tick"] < 120 * 52


def boot(dv1, dv2, k=10_000):
    rng = random.Random(2026)
    idx = list(range(len(dv1)))
    est = (sum(dv1) - sum(dv2)) / len(dv1)
    bs = []
    for _ in range(k):
        s = rng.choices(idx, k=len(idx))
        bs.append((sum(dv1[i] for i in s) - sum(dv2[i] for i in s)) / len(s))
    bs.sort()
    return est, bs[int(0.025 * k)], bs[int(0.975 * k) - 1]


def compare(rows, a, seeds):
    d1 = [died(rows["v1"][s]) for s in seeds]
    da = [died(rows[a][s]) for s in seeds]
    saved = sum(1 for x, y in zip(d1, da) if x and not y)
    lost = sum(1 for x, y in zip(d1, da) if y and not x)
    p = binomtest(saved, saved + lost).pvalue if saved + lost else 1.0
    return sum(da), saved, lost, p, boot(d1, da)


def pooled(rs):
    """F1's own pooled rates (births per woman-year, decisions blocked), over each world's 120 years, as SA1 reports them."""
    return A.rates(None, [({"Y": {int(k): v for k, v in r["years"].items()}, "deaths": r["deaths"], "births": r["births"]},
                           0, 120) for r in rs])


def main(smoke=False):
    seeds = (9701,) if smoke else SEEDS
    out = HERE / "output_smoke" if smoke else OUT
    rows, missing = {}, []
    for a in ARMS:
        for s in seeds:
            f = out / f"{a}_seed_{s}.json"
            if f.exists():
                rows.setdefault(a, {})[s] = json.loads(f.read_text(encoding="utf-8"))
            else:
                missing.append(f"{a} {s}")
    L = [f"# NV2 — nature v2 against v1: results{' (SMOKE TEST, throwaway seed)' if smoke else ''}", "",
         "Frozen as `NV2-frozen`. run_nv2.py, analyse_nv2.py.", "", "## Validity", ""]
    ok = True
    if not smoke:
        z = OUT / "zero.txt"
        zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
        L.append(f"- Zero checks (all off = control; each change acts; knowledge copy changes no behaviour; probe read-only): "
                 f"**{'yes' if zt else 'NO'}**")
        ok &= zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing
    allr = [r for a in rows.values() for r in a.values()]
    fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
    L.append(f"- One fingerprint (`code_v2`): **{'yes' if len(fps) == 1 else 'NO'}**")
    ok &= len(fps) == 1
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        n1 = sum(died(rows["v1"][s]) for s in seeds)
        L += ["", "## Baseline (rule 14)", "", f"v1 died out in {n1} of {len(seeds)} worlds ({n1 / len(seeds):.1%}).", "",
              "## Extinction against v1 (the frozen reading)", "",
              "| arm | died out | saved / lost | p | effect (v1 − arm) | 95% interval |", "|---|---|---|---|---|---|"]
        res = {}
        for a in ("v2", "sham"):
            n, sv, lo, p, (e, lo95, hi95) = compare(rows, a, seeds)
            res[a] = (p, lo95, hi95)
            L.append(f"| {a} | {n} | {sv} / {lo} | {p:.3g} | {e:+.3f} | [{lo95:+.3f}, {hi95:+.3f}] |")
        p, lo95, hi95 = res["v2"]
        lab = ("v2 changes survival" if p < 0.05 else
               "no meaningful effect on survival" if -HALF_F2 < lo95 and hi95 < HALF_F2 else "unresolved at this sample")
        L += ["", f"**Frozen rule: {lab}.**" + (" (Caveat: the sham reached p < 0.05.)" if res["sham"][0] < 0.05 else "")]
        L += ["", "## Beside it (described; population first, rule 18)", "",
              "| arm | median population, year 60 / 119 | births per woman-year (pooled) | decisions blocked for want of a partner (pooled) |",
              "|---|---|---|---|"]
        for a in ARMS:
            rs = [rows[a][s] for s in seeds]
            pop = lambda i: statistics.median(r["pops"][i] if len(r["pops"]) > i else 0 for r in rs)  # noqa: E731
            rt = pooled(rs)
            L.append(f"| {a} | {pop(5):.0f} / {pop(11):.0f} | {A.fmt(rt.get('births_per_woman_year'))} | "
                     f"{A.fmt(rt.get('block_no_partner'))} |")
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
