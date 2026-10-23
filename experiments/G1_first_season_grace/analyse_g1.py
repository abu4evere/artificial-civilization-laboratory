"""G1 analysis in the frozen order (questions.md, `G1-frozen`). Written before any data.

  python experiments/G1_first_season_grace/analyse_g1.py            # writes results.md
  python experiments/G1_first_season_grace/analyse_g1.py --smoke    # throwaway smoke outputs; writes nothing

Validity (no outcome shown otherwise): zero checks pass; all 512 worlds present; one fingerprint (`code_g1`).
Manipulation check (hard stop): share of new useful inventions still held by their inventor 13 weeks later, G − C,
paired Wilcoxon p < 0.05 with G higher.
Primary (transmission): CA1's link 3, G − C, paired; Wilcoxon, mean difference with a 95% bootstrap interval
(10,000, random.Random(2026)). "changes transmission" (p < 0.05), "no meaningful effect" (interval inside ±0.02),
otherwise "not shown".
Survival check (as LX1): died out = final_tick < 120 years; exact sign test on discordant pairs; effect = C − G,
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
from run_g1 import ARMS, OUT, SEEDS, SMOKE_SEEDS  # noqa: E402
from scipy.stats import binomtest, wilcoxon  # noqa: E402

YARD, BAND = 0.117, 0.02


def boot(d):
    rng = random.Random(2026)
    m = sorted(statistics.fmean(rng.choice(d) for _ in d) for _ in range(10000))
    return statistics.fmean(d), m[249], m[9749]


def died(r):
    return int(r["final_tick"] < 120 * 52)


def paired(rows, seeds, key):
    good = [s for s in seeds if rows["c"][s][key] is not None and rows["g"][s][key] is not None]
    d = [rows["g"][s][key] - rows["c"][s][key] for s in good]
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
    L = [f"# G1 — a first season of grace: results{' (SMOKE TEST, throwaway seeds)' if smoke else ''}",
         "", "Frozen as `G1-frozen`. run_g1.py, analyse_g1.py (written before data).", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks: **{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing
    if not missing:
        allr = [r for a in rows.values() for r in a.values()]
        fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
        L.append(f"- One fingerprint (`code_g1`): **{'yes' if len(fps) == 1 else 'NO'}**")
        ok &= len(fps) == 1
        good, d, p, (e, lo, hi) = paired(rows, seeds, "useful_held13_share")
        man = p < 0.05 and e > 0
        L.append(f"- Manipulation check: useful inventions still held by the inventor 13 weeks later, C median "
                 f"{med(rows, 'c', good, 'useful_held13_share'):.3f}, G median {med(rows, 'g', good, 'useful_held13_share'):.3f}; "
                 f"G − C {e:+.3f} [{lo:+.3f}, {hi:+.3f}], Wilcoxon p {p:.3g}, {len(good)} seeds: **{'passes' if man else 'FAILS'}**")
        ok &= man
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        good, d, pw, (e2, lo2, hi2) = paired(rows, seeds, "link3")
        if pw < 0.05:
            trans = "changes transmission" + (" (G higher)" if e2 > 0 else " (G lower)")
        elif -BAND < lo2 and hi2 < BAND:
            trans = "no meaningful effect"
        else:
            trans = "not shown"
        L += ["", "## Primary: transmission (share of useful inventions ever learned by someone else, CA1's link 3)", "",
              f"Seeds with useful inventions in both arms: {len(good)} of {len(seeds)}. Medians: C "
              f"{med(rows, 'c', good, 'link3'):.3f}, G {med(rows, 'g', good, 'link3'):.3f}.", "",
              "| G − C, mean | 95% interval | Wilcoxon p | reading |", "|---|---|---|---|",
              f"| {e2:+.4f} | [{lo2:+.4f}, {hi2:+.4f}] | {pw:.3g} | **{trans}** |"]
        dc = {s: died(rows["c"][s]) for s in seeds}
        dg = {s: died(rows["g"][s]) for s in seeds}
        saved = sum(1 for s in seeds if dc[s] and not dg[s])
        lost = sum(1 for s in seeds if dg[s] and not dc[s])
        p = binomtest(saved, saved + lost).pvalue if saved + lost else 1.0
        e, lo, hi = boot([dc[s] - dg[s] for s in seeds])
        if p < 0.05:
            surv = "changes survival" + (" (G dies out less)" if e > 0 else " (G dies out more)")
        elif -YARD < lo and hi < YARD:
            surv = "no meaningful effect"
        else:
            surv = "unresolved"
        L += ["", "## Survival check (G against C, paired by seed)", "",
              f"C died out in **{sum(dc.values())} of {len(seeds)}**; G in **{sum(dg.values())} of {len(seeds)}**.", "",
              "| G saved / lost (discordant pairs) | sign-test p | effect (C − G) | 95% interval | reading |",
              "|---|---|---|---|---|",
              f"| {saved} / {lost} | {p:.3g} | {e:+.3f} | [{lo:+.3f}, {hi:+.3f}] | **{surv}** |"]
        if trans != "changes transmission (G higher)":
            rule = f"**Not adopted** (transmission: {trans})."
        elif not (surv == "no meaningful effect" or "G dies out less" in surv):
            rule = f"**Not adopted** (survival: {surv})."
        else:
            rule = "**G may be proposed for adoption into nature (v4)**; the creator decides whether to accept the evidence."
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
        L += ["", "### After GPT's review: the cost, the fallback, and the pathway (described)", "",
              "Full-memory drops, summed over worlds (per 100 person-years in brackets). In C every drop is v3's.",
              "In G: \"displaced\" = grace protected a new recipe and an older one went instead; \"same\" = the one v3 "
              "would drop was already older; \"fallback\" = every held recipe was new, so v3's rule applied.", "",
              "| arm | drops | displaced | same | fallback | dropped while valued > 0.15 | displaced while valued > 0.15 | "
              "displaced that were useful kinds |", "|---|---|---|---|---|---|---|---|"]
        for a in ARMS:
            rs = [rows[a][s] for s in seeds]
            py = sum(r["person_years"] for r in rs)
            dk = Counter()
            for r in rs:
                dk.update(r["drops"])
            n = sum(dk.values())
            f = lambda x: f"{x:,} ({100 * x / py:.1f})"  # noqa: E731
            L.append(f"| {a} | {f(n)} | {f(dk['displaced'])} | {f(dk['same'])} | {f(dk['fallback'])} | "
                     f"{f(sum(r['drops_teachable'] for r in rs))} | {f(sum(r['displaced_teachable'] for r in rs))} | "
                     f"{f(sum(r['displaced_useful'] for r in rs))} |")
        L += ["", "The pathway for useful inventions (summed over worlds; each step counted on its own, not nested):", "",
              "| arm | useful inventions | held at 13 weeks | made again by the inventor | valued > 0.15 by the inventor | "
              "offered in a lesson | learned by someone else |", "|---|---|---|---|---|---|---|"]
        for a in ARMS:
            rs = [rows[a][s] for s in seeds]
            n = sum(r["path_n"] for r in rs)
            pc = lambda k: f"{sum(r['path'][k] for r in rs):,} ({100 * sum(r['path'][k] for r in rs) / n:.1f}%)"  # noqa: E731
            L.append(f"| {a} | {n:,} | {pc('held13')} | {pc('used_again')} | {pc('valued')} | {pc('offered')} | "
                     f"{pc('learned')} |")
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
