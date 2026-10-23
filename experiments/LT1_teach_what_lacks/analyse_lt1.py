"""LT1 analysis in the frozen order (questions.md, `LT1-frozen`). Written before any data.

  python experiments/LT1_teach_what_lacks/analyse_lt1.py            # writes results.md
  python experiments/LT1_teach_what_lacks/analyse_lt1.py --smoke    # throwaway smoke outputs; writes nothing

Validity: zero checks pass; all 1,024 worlds present; one fingerprint (`code_lt1`).
Manipulation (hard stop): the share of useful lessons ending "already known" falls in T (paired Wilcoxon p < 0.05).
Primary: useful recipes learned per person-year (distinct acquisitions), T − C paired; Wilcoxon; mean difference with
a 95% bootstrap interval (10,000, random.Random(2026)). "changes learning meaningfully" if p < 0.05 and the mean rise
is at least 10% of C's mean; "no meaningful effect" if the interval lies inside ±10% of C's mean; else "not shown".
Secondary: the take rate. Safety: passing on (link 3) lower bound above −0.02; time-averaged population T / C − 1
lower bound above −0.05 safe, upper below −0.05 harmful, else inconclusive; survival as LX1.
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
from run_lt1 import ARMS, OUT, OUTCOMES, SEEDS, SMOKE_SEEDS  # noqa: E402
from scipy.stats import binomtest, wilcoxon  # noqa: E402

YARD = 0.117


def boot(d):
    rng = random.Random(2026)
    m = sorted(statistics.fmean(rng.choice(d) for _ in d) for _ in range(10000))
    return statistics.fmean(d), m[249], m[9749]


def paired(rows, seeds, key):
    good = [s for s in seeds if rows["c"][s][key] is not None and rows["t"][s][key] is not None]
    d = [rows["t"][s][key] - rows["c"][s][key] for s in good]
    p = wilcoxon(d).pvalue if any(x != 0 for x in d) else 1.0
    return good, d, p, (boot(d) if d else (0.0, 0.0, 0.0))


def mean(rows, a, seeds, key):
    v = [rows[a][s][key] for s in seeds if rows[a][s][key] is not None]
    return statistics.fmean(v) if v else float("nan")


def died(r):
    return int(r["final_tick"] < 120 * 52)


def tavg(r):
    return sum(r["pops"][i] if len(r["pops"]) > i else 0 for i in range(12)) / 12


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
    L = [f"# LT1 — teach what the learner lacks: results{' (SMOKE TEST, throwaway seeds)' if smoke else ''}", "",
         "Frozen as `LT1-frozen`. run_lt1.py, analyse_lt1.py (written before data).", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks: **{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing
    if not missing:
        allr = [r for a in rows.values() for r in a.values()]
        fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
        L.append(f"- One fingerprint (`code_lt1`): **{'yes' if len(fps) == 1 else 'NO'}**")
        ok &= len(fps) == 1
        good, d, p, (e, lo, hi) = paired(rows, seeds, "known_share")
        man = p < 0.05 and e < 0
        L.append(f"- Manipulation check: useful lessons ending \"already known\", C mean {mean(rows, 'c', good, 'known_share'):.3f}, "
                 f"T mean {mean(rows, 't', good, 'known_share'):.3f}; T − C {e:+.3f} [{lo:+.3f}, {hi:+.3f}], "
                 f"Wilcoxon p {p:.3g}: **{'passes' if man else 'FAILS'}**")
        ok &= man
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        good, d, pw, (e, lo, hi) = paired(rows, seeds, "learned_py")
        base = mean(rows, "c", good, "learned_py")
        bar = 0.10 * base
        if pw < 0.05 and e >= bar:
            learn = "changes learning meaningfully (T higher)"
        elif -bar < lo and hi < bar:
            learn = "no meaningful effect"
        else:
            learn = "not shown"
        L += ["", "## Primary: useful recipes learned per person-year", "",
              f"C's mean {base:.4f}; T's mean {mean(rows, 't', good, 'learned_py'):.4f}; the 10% bar is {bar:.4f}.", "",
              "| T − C, mean | 95% interval | as a share of C's mean | Wilcoxon p | reading |", "|---|---|---|---|---|",
              f"| {e:+.4f} | [{lo:+.4f}, {hi:+.4f}] | {e / base:+.1%} | {pw:.3g} | **{learn}** |"]
        g2, d2, p2, (e2, lo2, hi2) = paired(rows, seeds, "take_rate")
        L += ["", "## Secondary: the share of useful lessons taken", "",
              f"C {mean(rows, 'c', g2, 'take_rate'):.4f}, T {mean(rows, 't', g2, 'take_rate'):.4f}; T − C {e2:+.4f} "
              f"[{lo2:+.4f}, {hi2:+.4f}], p {p2:.3g}."]
        g3, d3, p3, (e3, lo3, hi3) = paired(rows, seeds, "link3")
        pass_ok = lo3 > -0.02
        tc = {s: tavg(rows["c"][s]) for s in seeds}
        tt = {s: tavg(rows["t"][s]) for s in seeds}
        r0 = statistics.fmean(tt.values()) / statistics.fmean(tc.values()) - 1
        rng = random.Random(2026)
        bs = []
        for _ in range(10000):
            ss = [rng.choice(seeds) for _ in seeds]
            den = sum(tc[s] for s in ss)
            bs.append(sum(tt[s] for s in ss) / den - 1 if den else 0.0)
        bs.sort()
        rlo, rhi = bs[249], bs[9749]
        pop = "safe" if rlo > -0.05 else "harmful" if rhi < -0.05 else "inconclusive"
        dc = {s: died(rows["c"][s]) for s in seeds}
        dt = {s: died(rows["t"][s]) for s in seeds}
        saved = sum(1 for s in seeds if dc[s] and not dt[s])
        lost = sum(1 for s in seeds if dt[s] and not dc[s])
        ps = binomtest(saved, saved + lost).pvalue if saved + lost else 1.0
        es, slo, shi = boot([dc[s] - dt[s] for s in seeds])
        if ps < 0.05:
            surv = "changes survival" + (" (T dies out less)" if es > 0 else " (T dies out more)")
        elif -YARD < slo and shi < YARD:
            surv = "no meaningful effect"
        else:
            surv = "unresolved"
        L += ["", "## Safety", "",
              "| check | C | T | T − C (or T / C − 1) | 95% interval | reading |", "|---|---|---|---|---|---|",
              f"| passing on (link 3) | {mean(rows, 'c', g3, 'link3'):.4f} | {mean(rows, 't', g3, 'link3'):.4f} | "
              f"{e3:+.4f} | [{lo3:+.4f}, {hi3:+.4f}] | **{'not worse' if pass_ok else 'WORSE'}** |",
              f"| time-averaged population | {statistics.fmean(tc.values()):.2f} | {statistics.fmean(tt.values()):.2f} | "
              f"{r0:+.3f} | [{rlo:+.3f}, {rhi:+.3f}] | **{pop}** |",
              f"| died out | {sum(dc.values())} | {sum(dt.values())} | {saved} saved / {lost} lost, p {ps:.3g} | "
              f"[{slo:+.3f}, {shi:+.3f}] (C − T) | **{surv}** |"]
        surv_ok = surv == "no meaningful effect" or "T dies out less" in surv
        if learn != "changes learning meaningfully (T higher)":
            rule = f"**Not adopted** (learning: {learn})."
        elif not pass_ok or pop == "harmful" or not surv_ok:
            rule = "**Not adopted** (a safety check fails)."
        elif pop == "inconclusive":
            rule = "**Stays experimental** (learning rises, but population safety is inconclusive). Not in nature."
        else:
            rule = "**Adopted into nature (v4)**, by the frozen rule."
        L += ["", "## The adoption rule (frozen)", "", rule, "", "## Beside it (described; population first)", "",
              "| arm | median population, year 60 / 120 | useful lessons offered per person-year | taken per person-year | "
              "repeat acquisitions |", "|---|---|---|---|---|"]
        for a in ARMS:
            rs = [rows[a][s] for s in seeds]
            p60 = statistics.median(r["pops"][5] if len(r["pops"]) > 5 else 0 for r in rs)
            p120 = statistics.median(r["pops"][11] if len(r["pops"]) > 11 else 0 for r in rs)
            L.append(f"| {a} | {p60:.0f} / {p120:.0f} | {mean(rows, a, seeds, 'offered_py'):.3f} | "
                     f"{mean(rows, a, seeds, 'taken_py'):.4f} | {sum(r['repeat_acq'] for r in rs)} |")
        L += ["", "How useful lessons end (pooled):", "", "| arm | " + " | ".join(OUTCOMES) + " |",
              "|---|" + "---|" * len(OUTCOMES)]
        for a in ARMS:
            tot = Counter()
            for r in rows[a].values():
                tot.update(r["lessons"])
            n = sum(tot["useful:" + o] for o in OUTCOMES)
            L.append(f"| {a} | " + " | ".join(f"{tot['useful:' + o] / n:.1%}" if n else "—" for o in OUTCOMES) + " |")
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
