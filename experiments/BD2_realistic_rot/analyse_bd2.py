"""BD2 analysis in the frozen order (questions.md, `BD2-frozen`). Written before any data.

  python experiments/BD2_realistic_rot/analyse_bd2.py            # writes results.md
  python experiments/BD2_realistic_rot/analyse_bd2.py --smoke    # throwaway smoke outputs; writes nothing

Validity: zero checks pass; all 1,536 worlds present; one fingerprint (`code_bd2`).
Manipulation (hard stop): in R, bodies become bones in under half of C's median weeks, and foul person-weeks per
person-year are under half of C's.
Primary (GPT): time-averaged population. (1) R / C - 1 with a 95% bootstrap over paired seeds: "no meaningful effect"
inside +-0.05; "R lower" if the upper bound is below -0.05; "R higher" if the lower bound is above +0.05; else "not
shown". (2) Does bodies' gain hold with realistic rot? R / N - 1 (N: no bodies): "the gain holds" if the lower bound is
above 0; "no gain" if the interval lies inside +-0.05; else "not shown". C / N - 1 is described (BD1 again, on v5).
Survival (major secondary): sign test, bootstrap, yardstick +-0.117, for R against C and R against N.
Then the frozen adoption rule.
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_bd2 import ARMS, OUT, SEEDS, SMOKE_SEEDS  # noqa: E402
from scipy.stats import binomtest  # noqa: E402

YARD = 0.117


def boot(d):
    rng = random.Random(2026)
    m = sorted(statistics.fmean(rng.choice(d) for _ in d) for _ in range(10000))
    return statistics.fmean(d), m[249], m[9749]


def died(r):
    return int(r["final_tick"] < 120 * 52)


def tavg(r):
    return sum(r["pops"][i] if len(r["pops"]) > i else 0 for i in range(12)) / 12


def ratio(rows, seeds, a, b):
    ta = {s: tavg(rows[a][s]) for s in seeds}
    tb = {s: tavg(rows[b][s]) for s in seeds}
    r0 = statistics.fmean(ta.values()) / statistics.fmean(tb.values()) - 1 if statistics.fmean(tb.values()) else 0.0
    rng = random.Random(2026)
    bs = []
    for _ in range(10000):
        ss = [rng.choice(seeds) for _ in seeds]
        den = sum(tb[s] for s in ss)
        bs.append(sum(ta[s] for s in ss) / den - 1 if den else 0.0)
    bs.sort()
    return statistics.fmean(ta.values()), statistics.fmean(tb.values()), r0, bs[249], bs[9749]


def surv(rows, seeds, a, b):
    da = {s: died(rows[a][s]) for s in seeds}
    db = {s: died(rows[b][s]) for s in seeds}
    saved = sum(1 for s in seeds if db[s] and not da[s])
    lost = sum(1 for s in seeds if da[s] and not db[s])
    ps = binomtest(saved, saved + lost).pvalue if saved + lost else 1.0
    e, lo, hi = boot([db[s] - da[s] for s in seeds])
    if ps < 0.05:
        r = f"changes survival ({a} dies out {'less' if e > 0 else 'more'})"
    elif -YARD < lo and hi < YARD:
        r = "no meaningful effect"
    else:
        r = "unresolved"
    return sum(da.values()), sum(db.values()), saved, lost, ps, e, lo, hi, r


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
    L = [f"# BD2 — bodies with realistic rot: results{' (SMOKE TEST, throwaway seeds)' if smoke else ''}", "",
         "Frozen as `BD2-frozen`. run_bd2.py, analyse_bd2.py (written before data).", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks: **{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing
    if not missing:
        allr = [r for a in rows.values() for r in a.values()]
        fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
        L.append(f"- One fingerprint (`code_bd2`): **{'yes' if len(fps) == 1 else 'NO'}**")
        ok &= len(fps) == 1
        wc = [x for s in seeds for x in rows["c"][s]["weeks_to_bones"]]
        wr = [x for s in seeds for x in rows["r"][s]["weeks_to_bones"]]
        mc = statistics.median(wc) if wc else 0
        mr = statistics.median(wr) if wr else 0
        fc = sum(rows["c"][s]["foul_weeks"] for s in seeds) / max(1, sum(rows["c"][s]["person_years"] for s in seeds))
        fr = sum(rows["r"][s]["foul_weeks"] for s in seeds) / max(1, sum(rows["r"][s]["person_years"] for s in seeds))
        man = mr < 0.5 * mc and fr < 0.5 * fc
        L.append(f"- Manipulation check: median weeks to bones C {mc:.0f}, R {mr:.0f}; foul weeks per person-year C "
                 f"{fc:.2f}, R {fr:.2f}: **{'passes' if man else 'FAILS'}**")
        ok &= man
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        mr_, mc_, r1, lo1, hi1 = ratio(rows, seeds, "r", "c")
        read1 = ("no meaningful effect" if -0.05 < lo1 and hi1 < 0.05 else "R lower" if hi1 < -0.05
                 else "R higher" if lo1 > 0.05 else "not shown")
        _, mn_, r2, lo2, hi2 = ratio(rows, seeds, "r", "n")
        read2 = "the gain holds" if lo2 > 0 else "no gain" if -0.05 < lo2 and hi2 < 0.05 else "not shown"
        _, _, r3, lo3, hi3 = ratio(rows, seeds, "c", "n")
        L += ["", "## Primary: time-averaged population (GPT's choice)", "",
              f"Means: C (v5, bodies rot as stored food) **{mc_:.2f}**, R (realistic rot) **{mr_:.2f}**, N (no bodies) "
              f"**{mn_:.2f}**.", "",
              "| comparison | ratio - 1 | 95% interval | reading |", "|---|---|---|---|",
              f"| (1) R against C: what realistic rot does | {r1:+.3f} | [{lo1:+.3f}, {hi1:+.3f}] | **{read1}** |",
              f"| (2) R against N: does bodies' gain hold? | {r2:+.3f} | [{lo2:+.3f}, {hi2:+.3f}] | **{read2}** |",
              f"| C against N (described: BD1 again, on v5) | {r3:+.3f} | [{lo3:+.3f}, {hi3:+.3f}] | |"]
        L += ["", "## Survival (major secondary)", "",
              "| comparison | died out (arm / other) | saved / lost, p | effect | reading |", "|---|---|---|---|---|"]
        for a, b in (("r", "c"), ("r", "n"), ("c", "n")):
            da, db, sv, ls, ps, e, lo, hi, rd = surv(rows, seeds, a, b)
            L.append(f"| {a} against {b} | {da} / {db} | {sv} / {ls}, p {ps:.3g} | {e:+.3f} [{lo:+.3f}, {hi:+.3f}] | **{rd}** |")
        L += ["", "## The adoption rule (frozen)", "",
              "**Realistic rot is proposed for nature (v6)**: the manipulation check passed, and it is the truer physics. "
              "What it does to population and survival is reported above and is not used to accept or refuse it, so "
              "the rule never tunes nature toward an outcome. The creator decides."]
        L += ["", "## What happened to the bodies (described)", "",
              "| arm | bodies | median weeks to bones | foul person-weeks | meals from bodies | from rotten | by kin | seen | tools to kin |",
              "|---|---|---|---|---|---|---|---|---|"]
        for a in ("c", "r"):
            rs = [rows[a][s] for s in seeds]
            w = [x for r in rs for x in r["weeks_to_bones"]]
            L.append(f"| {a} | {sum(r['bodies'] for r in rs):,} | {statistics.median(w) if w else float('nan'):.0f} | "
                     f"{sum(r['foul_weeks'] for r in rs):,} | {sum(r['ate_n'] for r in rs):,} | "
                     f"{sum(r['ate_rotten'] for r in rs):,} | {sum(r['ate_kin'] for r in rs):,} | "
                     f"{sum(r['seen'] for r in rs):,} | {sum(r['tools'] for r in rs):,} |")
        L += ["", "## Beside it (population first)", "", "| arm | median population, year 60 / 120 | deaths | starvation |",
              "|---|---|---|---|"]
        for a in ARMS:
            rs = [rows[a][s] for s in seeds]
            p60 = statistics.median(r["pops"][5] if len(r["pops"]) > 5 else 0 for r in rs)
            p120 = statistics.median(r["pops"][11] if len(r["pops"]) > 11 else 0 for r in rs)
            st = sum(1 for r in rs for dd in r["deaths"] if dd[1] == "starvation")
            L.append(f"| {a} | {p60:.0f} / {p120:.0f} | {sum(len(r['deaths']) for r in rs)} | {st} |")
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
