"""DG1 analysis in the frozen order (questions.md, `DG1-frozen`). Written before any data.

  python experiments/DG1_digging/analyse_dg1.py            # writes results.md
  python experiments/DG1_digging/analyse_dg1.py --smoke    # throwaway smoke outputs; writes nothing

Validity: zero checks pass; all 1,536 worlds present; one fingerprint (`code_dg1`).
Manipulation (hard stop): in D, pits are dug in at least half of the worlds.
Safety (the adoption rule), D and DW each against C: survival as LX1 (sign test, bootstrap, yardstick ±0.117);
time-averaged population X / C − 1, lower bound above −0.05 safe, upper below −0.05 harmful, else inconclusive.
Described: digs, diggers, digs by decade, food set down in pits, pits standing; starvation deaths.
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
from run_dg1 import ARMS, OUT, SEEDS, SMOKE_SEEDS  # noqa: E402
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


def safety(rows, seeds, a):
    dc = {s: died(rows["c"][s]) for s in seeds}
    dx = {s: died(rows[a][s]) for s in seeds}
    saved = sum(1 for s in seeds if dc[s] and not dx[s])
    lost = sum(1 for s in seeds if dx[s] and not dc[s])
    ps = binomtest(saved, saved + lost).pvalue if saved + lost else 1.0
    es, slo, shi = boot([dc[s] - dx[s] for s in seeds])
    if ps < 0.05:
        surv = "changes survival" + (f" ({a} dies out less)" if es > 0 else f" ({a} dies out more)")
    elif -YARD < slo and shi < YARD:
        surv = "no meaningful effect"
    else:
        surv = "unresolved"
    tc = {s: tavg(rows["c"][s]) for s in seeds}
    tx = {s: tavg(rows[a][s]) for s in seeds}
    r0 = statistics.fmean(tx.values()) / statistics.fmean(tc.values()) - 1 if statistics.fmean(tc.values()) else 0.0
    rng = random.Random(2026)
    bs = []
    for _ in range(10000):
        ss = [rng.choice(seeds) for _ in seeds]
        den = sum(tc[s] for s in ss)
        bs.append(sum(tx[s] for s in ss) / den - 1 if den else 0.0)
    bs.sort()
    rlo, rhi = bs[249], bs[9749]
    pop = "safe" if rlo > -0.05 else "harmful" if rhi < -0.05 else "inconclusive"
    row = (f"| {a} | {sum(dc.values())} / {sum(dx.values())} | {saved} / {lost} (p {ps:.3g}); C − {a} {es:+.3f} "
           f"[{slo:+.3f}, {shi:+.3f}] | **{surv}** | {r0:+.3f} [{rlo:+.3f}, {rhi:+.3f}] | **{pop}** |")
    ok = (surv == "no meaningful effect" or "dies out less" in surv) and pop == "safe"
    return row, ok


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
    L = [f"# DG1 — digging: results{' (SMOKE TEST, throwaway seeds)' if smoke else ''}", "",
         "Frozen as `DG1-frozen`. run_dg1.py, analyse_dg1.py (written before data).", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks: **{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing
    if not missing:
        allr = [r for a in rows.values() for r in a.values()]
        fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
        L.append(f"- One fingerprint (`code_dg1`): **{'yes' if len(fps) == 1 else 'NO'}**")
        ok &= len(fps) == 1
        dug = sum(1 for s in seeds if rows["d"][s]["digs"] > 0)
        man = dug >= 0.5 * len(seeds)
        L.append(f"- Manipulation check: pits dug in {dug} of {len(seeds)} D worlds: **{'passes' if man else 'FAILS'}**")
        ok &= man
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        L += ["", "## Safety (the adoption rule)", "",
              "| arm | died out C / arm | discordant (saved / lost); effect | survival | population X / C − 1 [95%] | population |",
              "|---|---|---|---|---|---|"]
        good = {}
        for a in ("d", "dw"):
            row, g = safety(rows, seeds, a)
            L.append(row)
            good[a] = g
        rule = ("**Proposed for nature (v5):** survival and population are not worse in D. The creator decides."
                if good["d"] else "**Not adopted as is:** a safety reading in D is not passed.")
        L += ["", "## The adoption rule (frozen)", "", rule, "",
              f"(The weaker setting, DW, is a sensitivity check: {'also passes' if good['dw'] else 'does not pass'}.)",
              "", "## What people did with the ground (described)", "",
              "| arm | digs | people who dug | food set down in a pit (times / food units / people) | pits at the end (deep) | starvation deaths |",
              "|---|---|---|---|---|---|"]
        for a in ARMS:
            rs = [rows[a][s] for s in seeds]
            starv = sum(1 for r in rs for dd in r["deaths"] if dd[1] == "starvation")
            if a == "c":
                L.append(f"| c | — | — | — | — | {starv} |")
                continue
            L.append(f"| {a} | {sum(r['digs'] for r in rs):,} | {sum(r['diggers'] for r in rs):,} | "
                     f"{sum(r['pit_food_puts'] for r in rs):,} / {sum(r['pit_food'] for r in rs):,.0f} / "
                     f"{sum(r['pit_food_people'] for r in rs):,} | {sum(r['pits_end'] for r in rs)} "
                     f"({sum(r['deep_pits_end'] for r in rs)}) | {starv} |")
        dec = Counter()
        for r in (rows["d"][s] for s in seeds):
            dec.update({int(k): v for k, v in r["digs_by_decade"].items()})
        L += ["", "Digs by decade (D): " + ", ".join(f"{d + 1}: {dec[d]}" for d in range(12)) + "."]
        L += ["", "## Beside it (population first)", "", "| arm | median population, year 60 / 120 | deaths |",
              "|---|---|---|"]
        for a in ARMS:
            rs = [rows[a][s] for s in seeds]
            p60 = statistics.median(r["pops"][5] if len(r["pops"]) > 5 else 0 for r in rs)
            p120 = statistics.median(r["pops"][11] if len(r["pops"]) > 11 else 0 for r in rs)
            L.append(f"| {a} | {p60:.0f} / {p120:.0f} | {sum(len(r['deaths']) for r in rs)} |")
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
