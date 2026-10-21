"""LX1 analysis in the frozen order (questions.md, `LX1-frozen`).

  python experiments/LX1_parts_first_survival/analyse_lx1.py            # writes results.md
  python experiments/LX1_parts_first_survival/analyse_lx1.py --smoke    # throwaway smoke outputs; writes nothing

Validity (no outcome shown otherwise): zero checks pass; all 1,024 worlds present; one fingerprint (`code_lm1`);
part lessons in every L world that lived 10 years, and some taken.
Primary (survival): died out = final_tick < 120 years (as LM1); L against C paired by seed: exact sign test on the
discordant pairs; effect = C's share − L's share, 95% bootstrap (10,000, random.Random(2026)); yardstick ±0.117.
Secondary (replication): link 3, L − C, Wilcoxon, bootstrap of the mean difference.
Then the frozen adoption rule.
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
from run_lx1 import ARMS, OUT, SEEDS, SMOKE_SEEDS  # noqa: E402
from scipy.stats import binomtest, wilcoxon  # noqa: E402

YARD = 0.117


def boot(d):
    rng = random.Random(2026)
    m = sorted(statistics.fmean(rng.choice(d) for _ in d) for _ in range(10000))
    return statistics.fmean(d), m[249], m[9749]


def died(r):
    return int(r["final_tick"] < 120 * 52)


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
    L = [f"# LX1 — does parts-first teaching cost survival? results{' (SMOKE TEST, throwaway seeds)' if smoke else ''}",
         "", "Frozen as `LX1-frozen`. run_lx1.py, analyse_lx1.py.", "", "## Validity", ""]
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
        lt = [r for r in rows["l"].values() if r["final_tick"] >= 10 * 52]
        every = all(r["part_lessons"] > 0 for r in lt)
        some = sum(r["part_taken"] for r in lt) > 0
        L.append(f"- Manipulation check, L: part lessons in every L world living 10 years: **{'yes' if every else 'NO'}**; "
                 f"some taken ({sum(r['part_taken'] for r in lt)} of {sum(r['part_lessons'] for r in lt)}): "
                 f"**{'yes' if some else 'NO'}**")
        ok &= every and some
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        dc = {s: died(rows["c"][s]) for s in seeds}
        dl = {s: died(rows["l"][s]) for s in seeds}
        saved = sum(1 for s in seeds if dc[s] and not dl[s])
        lost = sum(1 for s in seeds if dl[s] and not dc[s])
        p = binomtest(saved, saved + lost).pvalue if saved + lost else 1.0
        e, lo, hi = boot([dc[s] - dl[s] for s in seeds])
        if p < 0.05:
            surv = "changes survival" + (" (L dies out less" if e > 0 else " (L dies out more") + \
                   (", beyond the yardstick)" if abs(e) > YARD else ", within the yardstick)")
        elif -YARD < lo and hi < YARD:
            surv = "no meaningful effect"
        else:
            surv = "unresolved"
        L += ["", "## Primary: survival (L against C, paired by seed)", "",
              f"C died out in **{sum(dc.values())} of {len(seeds)}**; L in **{sum(dl.values())} of {len(seeds)}**.", "",
              "| L saved / lost (discordant pairs) | sign-test p | effect (C − L) | 95% interval | reading |",
              "|---|---|---|---|---|",
              f"| {saved} / {lost} | {p:.3g} | {e:+.3f} | [{lo:+.3f}, {hi:+.3f}] | **{surv}** |"]
        good = [s for s in seeds if rows["c"][s]["link3"] is not None and rows["l"][s]["link3"] is not None]
        d = [rows["l"][s]["link3"] - rows["c"][s]["link3"] for s in good]
        pw = wilcoxon(d).pvalue if any(x != 0 for x in d) else 1.0
        e2, lo2, hi2 = boot(d)
        repl = pw < 0.05 and e2 > 0
        L += ["", "## Secondary: replication of LM1 (share of useful inventions passed on, CA1's link 3)", "",
              f"Seeds with useful inventions in both arms: {len(good)} of {len(seeds)}. C's median: "
              f"{statistics.median(rows['c'][s]['link3'] for s in good):.3f}.", "",
              "| L − C, mean | 95% interval | Wilcoxon p | replication |", "|---|---|---|---|",
              f"| {e2:+.4f} | [{lo2:+.4f}, {hi2:+.4f}] | {pw:.3g} | **{'holds' if repl else 'fails'}** |"]
        if surv == "unresolved":
            rule = "**Do not adopt now** (survival unresolved); the creator decides whether to run more seeds."
        elif "L dies out more" in surv:
            rule = "**Do not adopt** (L dies out more)."
        elif not repl:
            rule = "**Do not adopt** (the replication fails)."
        else:
            rule = "**Adopt L1 into nature (v3)**, by the frozen rule."
        L += ["", "## The adoption rule (frozen)", "", rule, "",
              "## Beside it (described; population first, rule 18)", "",
              "| arm | median population, year 60 / 119 | died out | deaths | illness | starvation | old age | thirst | other causes |",
              "|---|---|---|---|---|---|---|---|---|"]
        for a in ARMS:
            rs = [rows[a][s] for s in seeds]
            pop = lambda i: statistics.median(r["pops"][i] if len(r["pops"]) > i else 0 for r in rs)  # noqa: E731
            cz = Counter(dd[1] for r in rs for dd in r["deaths"])
            tot = sum(cz.values())
            other = tot - sum(cz[k] for k in ("illness", "starvation", "old age", "thirst"))
            L.append(f"| {a} | {pop(5):.0f} / {pop(11):.0f} | {sum(died(r) for r in rs)} | {tot} | "
                     f"{cz['illness']} | {cz['starvation']} | {cz['old age']} | {cz['thirst']} | {other} |")
        L += ["", "Births and partner blocking are not recorded by `code_lm1` (no new code was allowed), so they are "
              "not described."]
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
