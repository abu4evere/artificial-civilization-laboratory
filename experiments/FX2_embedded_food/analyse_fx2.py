"""FX2 analysis in the frozen order (questions.md, `FX2-frozen`). Written and smoke-tested before any data.

  python experiments/FX2_embedded_food/analyse_fx2.py            # writes results.md
  python experiments/FX2_embedded_food/analyse_fx2.py --smoke    # throwaway smoke outputs; writes nothing

Validity (no outcome shown otherwise): zero checks pass; all 768 worlds present; one code fingerprint; manipulation
check: in E and E0, embedded food is at least 25% of adults' foraged food (pooled; the plan's years 0-10 check was met in
the mechanism run, `mech_fx2.log`; here it is read over the whole run).
Frozen reading (Holm over the three tests):
  (1) tool use, E against E0: per world, the share of adult forage-weeks with a thing of hardness >= 40 in hand; paired by
      seed over the seeds where both worlds foraged at all; Wilcoxon signed-rank; effect = mean of (E - E0) with a 95%
      bootstrap interval (10,000 resamples, random.Random(2026)). Read as: does making hard things useful change tool use?
  (2) extinction, E against C, and (3) E against E0: exact sign test, paired by seed; effect = reference's extinction
      share - E's, 95% bootstrap; yardstick +-0.117; p < 0.05 (Holm) "changes survival"; p >= 0.05 and the interval inside
      +-0.117 "no meaningful effect"; otherwise "unresolved at this sample".
Described (the creator's sign-off note): holding a hard thing is not proof of discovery, so beside (1) the share of
embedded food actually opened with a hard thing, and the share of adult forage-weeks in which one was used on it.
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "NV2_nature_v2"))
sys.path.insert(0, str(HERE.parent / "F1_baseline_fragility"))
import analyse_f1 as A  # noqa: E402
from analyse_nv2 import HALF_F2, boot, died, pooled  # noqa: E402
from run_fx2 import ARMS, OUT, SEEDS, SMOKE_SEEDS  # noqa: E402
from scipy.stats import binomtest, wilcoxon  # noqa: E402


def compare(rows, ref, a, seeds):
    d0 = [died(rows[ref][s]) for s in seeds]
    da = [died(rows[a][s]) for s in seeds]
    saved = sum(1 for x, y in zip(d0, da) if x and not y)
    lost = sum(1 for x, y in zip(d0, da) if y and not x)
    p = binomtest(saved, saved + lost).pvalue if saved + lost else 1.0
    return sum(da), saved, lost, p, boot(d0, da)


def tool_test(rows, seeds):
    pairs = [(rows["e"][s]["hard_in_hand_share"], rows["e0"][s]["hard_in_hand_share"]) for s in seeds]
    pairs = [(x, y) for x, y in pairs if x is not None and y is not None]
    d = [x - y for x, y in pairs]
    p = wilcoxon(d).pvalue if any(v != 0 for v in d) else 1.0
    rng = random.Random(2026)
    means = sorted(statistics.fmean(rng.choice(d) for _ in d) for _ in range(10000))
    return len(pairs), statistics.fmean(d), p, (means[249], means[9749]), \
        statistics.median(x for x, _ in pairs), statistics.median(y for _, y in pairs)


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, run = [0.0] * len(ps), 0.0
    for k, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - k) * ps[i]))
        adj[i] = run
    return adj


def tot(rs):
    t = {}
    for r in rs:
        for k, v in r["tools"].items():
            t[k] = t.get(k, 0) + v
    return t


def main(smoke=False):
    seeds = SMOKE_SEEDS if smoke else SEEDS
    out = HERE / "output_smoke" if smoke else OUT
    rows, missing = {}, []
    for a in ARMS:
        for s in seeds:
            f = out / f"{a}_seed_{s}.json"
            if f.exists():
                rows.setdefault(a, {})[s] = json.loads(f.read_text(encoding="utf-8"))
            else:
                missing.append(f"{a} {s}")
    L = [f"# FX2 — food that must be opened: results{' (SMOKE TEST, throwaway seeds)' if smoke else ''}", "",
         "Frozen as `FX2-frozen`. run_fx2.py, analyse_fx2.py. `embedded_share` 0.5 and `embedded_bare` 0.2 are "
         "operational assumptions, not measured from real land.", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks (share 0 = code_v2; E and E0 act; read-only; reload exact): **{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing
    if not missing:
        allr = [r for a in rows.values() for r in a.values()]
        fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
        L.append(f"- One fingerprint (`code_fx2`): **{'yes' if len(fps) == 1 else 'NO'}**")
        ok &= len(fps) == 1
        for a in ("e", "e0"):
            t = tot([rows[a][s] for s in seeds])
            sh = t.get("opened", 0) / t["food_got"] if t.get("food_got") else 0.0
            good = sh >= 0.25
            L.append(f"- Manipulation check, {a}: embedded food is **{sh:.1%}** of adults' foraged food (needed ≥ 25%): "
                     f"**{'yes' if good else 'NO'}**")
            ok &= good
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        nc = sum(died(rows["c"][s]) for s in seeds)
        n, md, pt, (lo, hi), me, me0 = tool_test(rows, seeds)
        ext = {ref: compare(rows, ref, "e", seeds) for ref in ("c", "e0")}
        adj = holm([pt, ext["c"][3], ext["e0"][3]])
        L += ["", "## Baseline (rule 14)", "", f"C died out in {nc} of {len(seeds)} worlds ({nc / len(seeds):.1%}).", "",
              "## (1) Does making hard things useful change tool use? E against E0", "",
              "| seeds compared | median share of adult forage-weeks with hardness ≥ 40 in hand, E / E0 | mean difference "
              "(E − E0) | 95% interval | p (Wilcoxon) | Holm p | reading |", "|---|---|---|---|---|---|---|"]
        lab = ("**making hard things useful changes tool use**" if adj[0] < 0.05 else "no difference shown")
        L.append(f"| {n} | {me:.3f} / {me0:.3f} | {md:+.4f} | [{lo:+.4f}, {hi:+.4f}] | {pt:.3g} | {adj[0]:.3g} | {lab} |")
        L += ["", "## (2) Survival when food is harder to reach but tools can help, E against C; "
              "(3) does the tool benefit change survival, E against E0", "",
              "| comparison | E died out | reference died out | saved / lost | p | Holm p | effect (reference − E) | "
              "95% interval | reading |", "|---|---|---|---|---|---|---|---|---|"]
        for i, ref in ((1, "c"), (2, "e0")):
            ne, sv, lo_, p, (e, lo95, hi95) = ext[ref]
            nref = sum(died(rows[ref][s]) for s in seeds)
            lab = ("**changes survival**" if adj[i] < 0.05 else
                   "**no meaningful effect**" if -HALF_F2 < lo95 and hi95 < HALF_F2 else "unresolved at this sample")
            L.append(f"| E against {ref.upper()} | {ne} | {nref} | {sv} / {lo_} | {p:.3g} | {adj[i]:.3g} | {e:+.3f} | "
                     f"[{lo95:+.3f}, {hi95:+.3f}] | {lab} |")
        L += ["", "## Beside it (described; population first, rule 18)", "",
              "Holding a hard thing is not proof that anyone found the opening mechanism; the last three columns read what "
              "was actually used on embedded food.", "",
              "| arm | median population, year 60 / 119 | births per woman-year | blocked for want of a partner | "
              "embedded share of adults' food | opened with a hard thing (any / ≥ 0.4) | forage-weeks a hard thing was "
              "used on embedded food |", "|---|---|---|---|---|---|---|"]
        for a in ARMS:
            rs = [rows[a][s] for s in seeds]
            pop = lambda i: statistics.median(r["pops"][i] if len(r["pops"]) > i else 0 for r in rs)  # noqa: E731
            rt = pooled(rs)
            t = tot(rs)
            op = t.get("opened", 0)
            sh = op / t["food_got"] if t.get("food_got") else 0.0
            hk = f"{t.get('opened_with_hard', 0) / op:.1%} / {t.get('opened_with_hard_40', 0) / op:.1%}" if op else "–"
            wk = f"{t.get('weeks_used_hard', 0) / t['adult_forage_weeks']:.1%}" if t.get("adult_forage_weeks") else "–"
            L.append(f"| {a} | {pop(5):.0f} / {pop(11):.0f} | {A.fmt(rt.get('births_per_woman_year'))} | "
                     f"{A.fmt(rt.get('block_no_partner'))} | {sh:.1%} | {hk} | {wk} |")
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
