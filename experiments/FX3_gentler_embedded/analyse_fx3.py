"""FX3 analysis in the frozen order (questions.md, `FX3-frozen`, Revision 2). Written and smoke-tested before any data.

  python experiments/FX3_gentler_embedded/analyse_fx3.py            # writes results.md
  python experiments/FX3_gentler_embedded/analyse_fx3.py --smoke    # throwaway smoke outputs; writes nothing

Validity (no outcome shown otherwise): zero checks pass; all 1,280 worlds present; one code fingerprint (`code_fx2`).
Primary 1, survival (always read): S25 against S25-0 and B50 against B50-0, paired by seed; exact sign test; effect =
tool-free arm's extinction share - tool arm's, 95% bootstrap (10,000 resamples, random.Random(2026)); Holm over the two.
p < 0.05 "changes survival", with a size label: "beyond the yardstick" if the estimate is outside +-0.117, else
"within the yardstick"; p >= 0.05 and the interval inside +-0.117 "no meaningful effect"; otherwise "unresolved".
Primary 2, tool use: share of adult forage-weeks with a hard thing (hardness >= 40) in hand, tool arm against its
tool-free arm, Wilcoxon signed-rank, 95% bootstrap of the mean difference; Holm over the two; "limited" (described, not
tested) if fewer than 64 seeds give forage-weeks in both arms.
Described: each arm against C; population; births; partner blocking; embedded share of food; opened with a hard thing;
forage-weeks a hard thing was used on embedded food (carrying and using reported apart).
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
sys.path.insert(0, str(HERE.parent / "FX2_embedded_food"))
import analyse_f1 as A  # noqa: E402
from analyse_nv2 import HALF_F2, boot, died, pooled  # noqa: E402
from analyse_fx2 import holm, tot  # noqa: E402
from run_fx3 import ARMS, OUT, PAIRS, SEEDS, SMOKE_SEEDS  # noqa: E402
from scipy.stats import binomtest, wilcoxon  # noqa: E402

MIN_SEEDS = 64


def compare(rows, ref, a, seeds):
    d0 = [died(rows[ref][s]) for s in seeds]
    da = [died(rows[a][s]) for s in seeds]
    saved = sum(1 for x, y in zip(d0, da) if x and not y)
    lost = sum(1 for x, y in zip(d0, da) if y and not x)
    p = binomtest(saved, saved + lost).pvalue if saved + lost else 1.0
    return sum(da), sum(d0), saved, lost, p, boot(d0, da)


def tool_test(rows, a, b, seeds):
    pairs = [(rows[a][s]["hard_in_hand_share"], rows[b][s]["hard_in_hand_share"]) for s in seeds]
    pairs = [(x, y) for x, y in pairs if x is not None and y is not None]
    if not pairs:
        return 0, None, 1.0, (None, None), None, None
    d = [x - y for x, y in pairs]
    p = wilcoxon(d).pvalue if any(v != 0 for v in d) else 1.0
    rng = random.Random(2026)
    means = sorted(statistics.fmean(rng.choice(d) for _ in d) for _ in range(10000))
    return len(pairs), statistics.fmean(d), p, (means[249], means[9749]), \
        statistics.median(x for x, _ in pairs), statistics.median(y for _, y in pairs)


def survival_label(p_adj, e, lo, hi):
    if p_adj < 0.05:
        size = "beyond the yardstick" if abs(e) > HALF_F2 else "within the yardstick"
        return f"**changes survival** ({size})"
    if -HALF_F2 < lo and hi < HALF_F2:
        return "**no meaningful effect**"
    return "unresolved"


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
    L = [f"# FX3 — food that must be opened, at gentler settings: results{' (SMOKE TEST)' if smoke else ''}", "",
         "Frozen as `FX3-frozen` (Revision 2). run_fx3.py, analyse_fx3.py; code `code_fx2` unchanged. Settings are "
         "operational.", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks (share 0 = code_v2; every arm acts; the tool route acts; read-only; reload exact): "
             f"**{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + str(len(missing))}**")
    ok &= not missing
    if not missing:
        allr = [r for a in rows.values() for r in a.values()]
        fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
        L.append(f"- One fingerprint (`code_fx2`): **{'yes' if len(fps) == 1 else 'NO'}**")
        ok &= len(fps) == 1
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        nc = sum(died(rows["c"][s]) for s in seeds)
        surv = {a: compare(rows, b, a, seeds) for a, b in PAIRS}
        sadj = dict(zip([a for a, _ in PAIRS], holm([surv[a][4] for a, _ in PAIRS])))
        L += ["", "## Baseline (rule 14)", "", f"C died out in {nc} of {len(seeds)} worlds ({nc / len(seeds):.1%}).", "",
              "## Primary 1: does the tool route change survival? (always read)", "",
              "| comparison | tool arm died out | tool-free arm died out | saved / lost | p | Holm p | effect (tool-free − "
              "tool) | 95% interval | reading |", "|---|---|---|---|---|---|---|---|---|"]
        for a, b in PAIRS:
            na, nb, sv, ls, p, (e, lo, hi) = surv[a]
            L.append(f"| {a.upper()} against {b.upper()} | {na} | {nb} | {sv} / {ls} | {p:.3g} | {sadj[a]:.3g} | {e:+.3f} | "
                     f"[{lo:+.3f}, {hi:+.3f}] | {survival_label(sadj[a], e, lo, hi)} |")
        tools = {a: tool_test(rows, a, b, seeds) for a, b in PAIRS}
        tadj = dict(zip([a for a, _ in PAIRS], holm([tools[a][2] for a, _ in PAIRS])))
        L += ["", "## Primary 2: does the tool route change tool use? (carrying a hard thing)", "",
              "| comparison | seeds compared | median share of adult forage-weeks with hardness ≥ 40 in hand, tool / "
              "tool-free | mean difference | 95% interval | p | Holm p | reading |", "|---|---|---|---|---|---|---|---|"]
        for a, b in PAIRS:
            n, md, p, (lo, hi), m1, m0 = tools[a]
            if n < MIN_SEEDS:
                L.append(f"| {a.upper()} against {b.upper()} | {n} | {m1} / {m0} | {md} | – | – | – | **limited** "
                         f"(fewer than {MIN_SEEDS} seeds; described only) |")
                continue
            lab = "**the tool route changes tool use**" if tadj[a] < 0.05 else "no difference shown"
            L.append(f"| {a.upper()} against {b.upper()} | {n} | {m1:.3f} / {m0:.3f} | {md:+.4f} | [{lo:+.4f}, {hi:+.4f}] | "
                     f"{p:.3g} | {tadj[a]:.3g} | {lab} |")
        L += ["", "## Each arm against C (described)", "", "| arm | died out | against C: saved / lost | effect (C − arm) | "
              "95% interval |", "|---|---|---|---|---|"]
        for a in ARMS:
            if a == "c":
                continue
            na, _nc, sv, ls, _p, (e, lo, hi) = compare(rows, "c", a, seeds)
            L.append(f"| {a} | {na} | {sv} / {ls} | {e:+.3f} | [{lo:+.3f}, {hi:+.3f}] |")
        L += ["", "## Beside it (described; population first)", "",
              "Carrying a hard thing is not using it; the last two columns read what was actually used on embedded food.",
              "", "| arm | median population, year 60 / 119 | births per woman-year | blocked for want of a partner | "
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
