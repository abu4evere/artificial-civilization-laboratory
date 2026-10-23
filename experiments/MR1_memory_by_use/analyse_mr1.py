"""MR1 analysis in the frozen order (questions.md, `MR1-frozen`). Written before any data.

  python experiments/MR1_memory_by_use/analyse_mr1.py            # writes results.md
  python experiments/MR1_memory_by_use/analyse_mr1.py --smoke    # throwaway smoke outputs; writes nothing

Validity (no outcome shown otherwise): zero checks pass; all 512 worlds present; one fingerprint (`code_mr1`).
Manipulation check (hard stop): share of new useful inventions still held by their inventor 13 weeks later, U − C,
paired Wilcoxon p < 0.05 with U higher.
Primary (transmission): CA1's link 3, U − C, paired; Wilcoxon, mean difference with a 95% bootstrap interval
(10,000, random.Random(2026)). "changes transmission" (p < 0.05), "no meaningful effect" (interval inside ±0.02),
otherwise "not shown".
Survival check (as LX1): died out = final_tick < 120 years; exact sign test on discordant pairs; effect = C − U,
bootstrap; yardstick ±0.117.
Then the frozen adoption rule, and the described measures (population first).
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_mr1 import ARMS, OUT, SEEDS, SMOKE_SEEDS  # noqa: E402
from scipy.stats import binomtest, wilcoxon  # noqa: E402

YARD, BAND = 0.117, 0.02


def boot(d):
    rng = random.Random(2026)
    m = sorted(statistics.fmean(rng.choice(d) for _ in d) for _ in range(10000))
    return statistics.fmean(d), m[249], m[9749]


def died(r):
    return int(r["final_tick"] < 120 * 52)


def paired(rows, seeds, key):
    good = [s for s in seeds if rows["c"][s][key] is not None and rows["u"][s][key] is not None]
    d = [rows["u"][s][key] - rows["c"][s][key] for s in good]
    p = wilcoxon(d).pvalue if any(x != 0 for x in d) else 1.0
    return good, d, p, boot(d) if d else (0.0, 0.0, 0.0)


def med(rows, a, seeds, key):
    v = [rows[a][s][key] for s in seeds if rows[a][s][key] is not None]
    return statistics.median(v) if v else float("nan")


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
    L = [f"# MR1 — remembering by use, not by slots: results{' (SMOKE TEST, throwaway seeds)' if smoke else ''}",
         "", "Frozen as `MR1-frozen`. run_mr1.py, analyse_mr1.py (written before data).", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks: **{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing
    if not missing:
        allr = [r for a in rows.values() for r in a.values()]
        fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
        L.append(f"- One fingerprint (`code_mr1`): **{'yes' if len(fps) == 1 else 'NO'}**")
        ok &= len(fps) == 1
        good, d, p, (e, lo, hi) = paired(rows, seeds, "useful_held13_share")
        man = p < 0.05 and e > 0
        L.append(f"- Manipulation check: useful inventions still held by the inventor 13 weeks later, C median "
                 f"{med(rows, 'c', good, 'useful_held13_share'):.3f}, U median {med(rows, 'u', good, 'useful_held13_share'):.3f}; "
                 f"U − C {e:+.3f} [{lo:+.3f}, {hi:+.3f}], Wilcoxon p {p:.3g}, {len(good)} seeds: **{'passes' if man else 'FAILS'}**")
        ok &= man
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        good, d, pw, (e2, lo2, hi2) = paired(rows, seeds, "link3")
        if pw < 0.05:
            trans = "changes transmission" + (" (U higher)" if e2 > 0 else " (U lower)")
        elif -BAND < lo2 and hi2 < BAND:
            trans = "no meaningful effect"
        else:
            trans = "not shown"
        L += ["", "## Primary: transmission (share of useful inventions ever learned by someone else, CA1's link 3)", "",
              f"Seeds with useful inventions in both arms: {len(good)} of {len(seeds)}. Medians: C "
              f"{med(rows, 'c', good, 'link3'):.3f}, U {med(rows, 'u', good, 'link3'):.3f}.", "",
              "| U − C, mean | 95% interval | Wilcoxon p | reading |", "|---|---|---|---|",
              f"| {e2:+.4f} | [{lo2:+.4f}, {hi2:+.4f}] | {pw:.3g} | **{trans}** |"]
        dc = {s: died(rows["c"][s]) for s in seeds}
        du = {s: died(rows["u"][s]) for s in seeds}
        saved = sum(1 for s in seeds if dc[s] and not du[s])
        lost = sum(1 for s in seeds if du[s] and not dc[s])
        p = binomtest(saved, saved + lost).pvalue if saved + lost else 1.0
        e, lo, hi = boot([dc[s] - du[s] for s in seeds])
        if p < 0.05:
            surv = "changes survival" + (" (U dies out less)" if e > 0 else " (U dies out more)")
        elif -YARD < lo and hi < YARD:
            surv = "no meaningful effect"
        else:
            surv = "unresolved"
        L += ["", "## Survival check (U against C, paired by seed)", "",
              f"C died out in **{sum(dc.values())} of {len(seeds)}**; U in **{sum(du.values())} of {len(seeds)}**.", "",
              "| U saved / lost (discordant pairs) | sign-test p | effect (C − U) | 95% interval | reading |",
              "|---|---|---|---|---|",
              f"| {saved} / {lost} | {p:.3g} | {e:+.3f} | [{lo:+.3f}, {hi:+.3f}] | **{surv}** |"]
        if trans != "changes transmission (U higher)":
            rule = f"**Not adopted** (transmission: {trans})."
        elif not (surv == "no meaningful effect" or "U dies out less" in surv):
            rule = f"**Not adopted** (survival: {surv})."
        else:
            rule = "**U may be proposed for adoption into nature (v4)**; the creator decides whether to accept the evidence."
        L += ["", "## The adoption rule (frozen)", "", rule, "",
              "## Beside it (described; population first, rule 18)", "",
              "| arm | median population, year 60 / 119 | died out | recipes held per person | weeks a useful invention "
              "stays with its inventor (mean) | built on by a learner | longest part chain (median) | "
              "children's useful inventions passed on |",
              "|---|---|---|---|---|---|---|---|"]
        for a in ARMS:
            rs = [rows[a][s] for s in seeds]
            pop = lambda i: statistics.median(r["pops"][i] if len(r["pops"]) > i else 0 for r in rs)  # noqa: E731
            ch, cp = sum(r["child_useful"] for r in rs), sum(r["child_useful_passed"] for r in rs)
            L.append(f"| {a} | {pop(5):.0f} / {pop(11):.0f} | {sum(died(r) for r in rs)} | "
                     f"{med(rows, a, seeds, 'recipes_per_person'):.2f} | {med(rows, a, seeds, 'useful_held_weeks_mean'):.1f} | "
                     f"{sum(r['improved_by_learner'] for r in rs)} | {med(rows, a, seeds, 'longest_chain'):.0f} | "
                     f"{cp} of {ch} |")
        L += ["", "| arm | deaths | illness | starvation | old age | thirst | other causes |", "|---|---|---|---|---|---|---|"]
        for a in ARMS:
            cz = Counter(dd[1] for s in seeds for dd in rows[a][s]["deaths"])
            tot = sum(cz.values())
            other = tot - sum(cz[k] for k in ("illness", "starvation", "old age", "thirst"))
            L.append(f"| {a} | {tot} | {cz['illness']} | {cz['starvation']} | {cz['old age']} | {cz['thirst']} | {other} |")
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
