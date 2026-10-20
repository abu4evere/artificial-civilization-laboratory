"""LM1 analysis in the frozen order (proposal.md, `LM1-frozen`). Written and smoke-tested before any data.

  python experiments/LM1_memory_and_parts/analyse_lm1.py            # writes results.md
  python experiments/LM1_memory_and_parts/analyse_lm1.py --smoke    # throwaway smoke outputs; writes nothing

Validity (no outcome shown otherwise): zero checks pass; all 1,024 worlds present; one fingerprint; manipulation checks (M as amended by Amendment 1)
(M: among tie drops in M and ML, composites' share within 0.05 of their share of tied recipes, pooled; L: part lessons
in every L and ML world that lived 10 years, and some taken).
Primary: per world, link-3 proportion; M, L, ML each against C, paired: Wilcoxon signed-rank; mean paired difference,
95% bootstrap (10,000, random.Random(2026)); Holm over the three; "changes transmission" if Holm p < 0.05; "no meaningful
effect" if p >= 0.05 and the interval inside +-0.02; else "not shown". Interaction (ML - L) - (M - C): own Wilcoxon and
bootstrap; "interaction shown" if p < 0.05 and the interval excludes 0, else "not shown".
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_lm1 import ARMS, OUT, SEEDS, SMOKE_SEEDS  # noqa: E402
from scipy.stats import wilcoxon  # noqa: E402


def boot(d):
    rng = random.Random(2026)
    m = sorted(statistics.fmean(rng.choice(d) for _ in d) for _ in range(10000))
    return statistics.fmean(d), m[249], m[9749]


def test(d):
    p = wilcoxon(d).pvalue if any(x != 0 for x in d) else 1.0
    return (p, *boot(d))


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, run = [0.0] * len(ps), 0.0
    for k, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - k) * ps[i]))
        adj[i] = run
    return adj


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
    L = [f"# LM1 — memory or parts: results{' (SMOKE TEST, throwaway seeds)' if smoke else ''}", "",
         "Frozen as `LM1-frozen`. run_lm1.py, analyse_lm1.py.", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks: **{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing
    if not missing:
        allr = [r for a in rows.values() for r in a.values()]
        fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
        L.append(f"- One fingerprint (`code_lm1`): **{'yes' if len(fps) == 1 else 'NO'}**")
        ok &= len(fps) == 1
        mt = [r for a in ("m", "ml") for r in rows[a].values() if r["ties"]]
        n = sum(r["ties"] for r in mt)
        dc = sum(r["tie_drop_composite"] * r["ties"] for r in mt) / n if n else None
        tc = sum(r["tie_composite_share"] * r["ties"] for r in mt) / n if n else None
        old = sum(r["tie_drop_oldest"] * r["ties"] for r in mt) / n if n else None
        ct = [r for r in rows["c"].values() if r["ties"]]          # Amendment 1: oldest dropped, composites less than C
        cn = sum(r["ties"] for r in ct)
        cdc = sum(r["tie_drop_composite"] * r["ties"] for r in ct) / cn if cn else None
        t = old is not None and old >= 0.99 and dc is not None and cdc is not None and dc < cdc
        L.append(f"- Manipulation check, M (Amendment 1): longest-held dropped in {old:.1%} of ties (needed at least "
                 f"99%); composites {dc:.1%} of tie drops against {cdc:.1%} in C (needed lower): "
                 f"**{'yes' if t else 'NO'}**. Reported, not a stop: composites {dc:.1%} of tie drops against "
                 f"{tc:.1%} of tied recipes")
        ok &= t
        lt = [r for a in ("l", "ml") for r in rows[a].values() if r["final_tick"] >= 10 * 52]
        every = all(r["part_lessons"] > 0 for r in lt)
        some = sum(r["part_taken"] for r in lt) > 0
        L.append(f"- Manipulation check, L: part lessons in every L/ML world living 10 years: **{'yes' if every else 'NO'}**; "
                 f"some taken ({sum(r['part_taken'] for r in lt)} of {sum(r['part_lessons'] for r in lt)}): "
                 f"**{'yes' if some else 'NO'}**")
        ok &= every and some
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        val = {a: {s: rows[a][s]["link3"] for s in seeds} for a in ARMS}
        good = [s for s in seeds if all(val[a][s] is not None for a in ARMS)]
        res = {a: test([val[a][s] - val["c"][s] for s in good]) for a in ("m", "l", "ml")}
        adj = dict(zip(("m", "l", "ml"), holm([res[a][0] for a in ("m", "l", "ml")])))
        L += ["", "## Primary: share of useful inventions passed on (CA1's link 3)", "",
              f"Worlds with useful inventions in every arm: {len(good)} of {len(seeds)}. C's median: "
              f"{statistics.median(val['c'][s] for s in good):.3f}.", "",
              "| arm vs C | mean difference | 95% interval | p | Holm p | reading |", "|---|---|---|---|---|---|"]
        for a in ("m", "l", "ml"):
            p, e, lo, hi = res[a]
            lab = ("**changes transmission**" if adj[a] < 0.05 else
                   "**no meaningful effect**" if -0.02 < lo and hi < 0.02 else "not shown")
            L.append(f"| {a.upper()} | {e:+.4f} | [{lo:+.4f}, {hi:+.4f}] | {p:.3g} | {adj[a]:.3g} | {lab} |")
        d = [(val["ml"][s] - val["l"][s]) - (val["m"][s] - val["c"][s]) for s in good]
        p, e, lo, hi = test(d)
        lab = "**interaction shown**" if p < 0.05 and (lo > 0 or hi < 0) else "interaction not shown"
        L += ["", f"**Interaction (ML − L) − (M − C):** {e:+.4f} [{lo:+.4f}, {hi:+.4f}], p = {p:.3g}: {lab}.", "",
              "## Beside it (described; identical definitions in every arm; population first, rule 18)", "",
              "| arm | median population, year 60 / 119 | died out | useful kinds created (median) | passed on (median) | "
              "made by a learner | improved by a learner | improvement passed on |", "|---|---|---|---|---|---|---|---|"]
        for a in ARMS:
            rs = [rows[a][s] for s in seeds]
            pop = lambda i: statistics.median(r["pops"][i] if len(r["pops"]) > i else 0 for r in rs)  # noqa: E731
            died = sum(1 for r in rs if r["final_tick"] < 120 * 52)
            L.append(f"| {a} | {pop(5):.0f} / {pop(11):.0f} | {died} | {statistics.median(r['useful'] for r in rs):.0f} | "
                     f"{statistics.median(r['passed'] for r in rs):.0f} | {sum(r['made_by_learner'] for r in rs)} | "
                     f"{sum(r['improved_by_learner'] for r in rs)} | {sum(r['improved_passed'] for r in rs)} |")
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
