"""BD1 analysis in the frozen order (questions.md, `BD1-frozen`). Written before any data.

  python experiments/BD1_bodies_stay/analyse_bd1.py            # writes results.md
  python experiments/BD1_bodies_stay/analyse_bd1.py --smoke    # throwaway smoke outputs; writes nothing

Validity: zero checks pass; all 1,024 worlds present; one fingerprint (`code_bd1`).
Manipulation (hard stop): in B, every world in which someone died has a body; bodies turn to bones; the living meet
rotten bodies (some "foul" weeks) in at least half of the worlds with a body.
Safety (the adoption rule): survival as LX1 (sign test, bootstrap, yardstick ±0.117); time-averaged population B / C − 1,
lower bound above −0.05 safe, upper bound below −0.05 harmful, else inconclusive (as GR2).
Then described: the fate of bodies; eating from bodies (how often, kin, rotten, hunger, by decade and generation);
foul weeks; deaths of the dead's knowledge by sight; tools recovered; deaths by cause.
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
from run_bd1 import ARMS, OUT, SEEDS, SMOKE_SEEDS  # noqa: E402
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
    L = [f"# BD1 — bodies stay: results{' (SMOKE TEST, throwaway seeds)' if smoke else ''}", "",
         "Frozen as `BD1-frozen`. run_bd1.py, analyse_bd1.py (written before data).", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks: **{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing
    if not missing:
        allr = [r for a in rows.values() for r in a.values()]
        fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
        L.append(f"- One fingerprint (`code_bd1`): **{'yes' if len(fps) == 1 else 'NO'}**")
        ok &= len(fps) == 1
        b = rows["b"]
        with_deaths = [s for s in seeds if b[s]["deaths"]]
        every = all(b[s]["bodies"] > 0 for s in with_deaths)
        bones = sum(b[s]["bones"] for s in seeds) > 0
        with_body = [s for s in seeds if b[s]["bodies"] > 0]
        foul = sum(1 for s in with_body if b[s]["foul_weeks"] > 0)
        man = every and bones and foul >= 0.5 * len(with_body)
        L.append(f"- Manipulation check: a body in every B world with a death ({'yes' if every else 'NO'}); bodies turn "
                 f"to bones ({'yes' if bones else 'NO'}); rotten bodies met in {foul} of {len(with_body)} worlds with a "
                 f"body: **{'passes' if man else 'FAILS'}**")
        ok &= man
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        dc = {s: died(rows["c"][s]) for s in seeds}
        db = {s: died(rows["b"][s]) for s in seeds}
        saved = sum(1 for s in seeds if dc[s] and not db[s])
        lost = sum(1 for s in seeds if db[s] and not dc[s])
        ps = binomtest(saved, saved + lost).pvalue if saved + lost else 1.0
        es, slo, shi = boot([dc[s] - db[s] for s in seeds])
        if ps < 0.05:
            surv = "changes survival" + (" (B dies out less)" if es > 0 else " (B dies out more)")
        elif -YARD < slo and shi < YARD:
            surv = "no meaningful effect"
        else:
            surv = "unresolved"
        tc = {s: tavg(rows["c"][s]) for s in seeds}
        tb = {s: tavg(rows["b"][s]) for s in seeds}
        r0 = statistics.fmean(tb.values()) / statistics.fmean(tc.values()) - 1
        rng = random.Random(2026)
        bs = []
        for _ in range(10000):
            ss = [rng.choice(seeds) for _ in seeds]
            den = sum(tc[s] for s in ss)
            bs.append(sum(tb[s] for s in ss) / den - 1 if den else 0.0)
        bs.sort()
        rlo, rhi = bs[249], bs[9749]
        pop = "safe" if rlo > -0.05 else "harmful" if rhi < -0.05 else "inconclusive"
        L += ["", "## Safety (the adoption rule)", "",
              "| check | C | B | effect | 95% interval | reading |", "|---|---|---|---|---|---|",
              f"| died out | {sum(dc.values())} of {len(seeds)} | {sum(db.values())} of {len(seeds)} | "
              f"{saved} saved / {lost} lost (p {ps:.3g}); C − B {es:+.3f} | [{slo:+.3f}, {shi:+.3f}] | **{surv}** |",
              f"| time-averaged population | {statistics.fmean(tc.values()):.2f} | {statistics.fmean(tb.values()):.2f} | "
              f"B / C − 1 {r0:+.3f} | [{rlo:+.3f}, {rhi:+.3f}] | **{pop}** |"]
        good = (surv == "no meaningful effect" or "B dies out less" in surv) and pop == "safe"
        rule = ("**Proposed for nature (v4):** survival and population are not worse. The creator decides."
                if good else "**Not adopted as is:** a safety reading is not passed; the cause is to be looked for.")
        L += ["", "## The adoption rule (frozen)", "", rule]
        b = [rows["b"][s] for s in seeds]
        nb = sum(r["bodies"] for r in b)
        wtb = [x for r in b for x in r["weeks_to_bones"]]
        ate = sum(r["ate_n"] for r in b)
        hung = [x for r in b for x in r["ate_hunger"]]
        L += ["", "## What happened to the bodies (B; described)", "",
              f"- Bodies: **{nb:,}** in {len(seeds)} worlds; turned to bones: {sum(r['bones'] for r in b):,}; median weeks "
              f"to bones {statistics.median(wtb) if wtb else float('nan'):.0f}.",
              f"- Meat in bodies {sum(r['body_meat'] for r in b):,.0f} food units; food taken from bodies "
              f"{sum(r['ate_food'] for r in b):,.1f}.",
              f"- **Eating from bodies:** {ate:,} times, from {sum(r['ate_bodies'] for r in b):,} bodies, by "
              f"{sum(r['ate_people'] for r in b):,} people, in {sum(1 for r in b if r['ate_n'])} of {len(seeds)} worlds. "
              f"Of these, by kin of the dead: {sum(r['ate_kin'] for r in b):,}; from a rotten body: "
              f"{sum(r['ate_rotten'] for r in b):,}; the eater's hunger, median {statistics.median(hung) if hung else float('nan'):.2f}.",
              f"- Person-weeks next to a rotten body (\"foul\"): {sum(r['foul_weeks'] for r in b):,}.",
              f"- People who learned of a death from the sight of the body: {sum(r['seen'] for r in b):,}.",
              f"- Tools taken from a body by a partner or child: {sum(r['tools'] for r in b):,}.", "",
              "Eating from bodies by decade (all B worlds):", "",
              "| decade | " + " | ".join(str(d + 1) for d in range(12)) + " |", "|---|" + "---|" * 12]
        dec = Counter()
        gen = Counter()
        for r in b:
            dec.update({int(k): v for k, v in r["ate_by_decade"].items()})
            gen.update({int(k): v for k, v in r["ate_by_gen"].items()})
        L.append("| times | " + " | ".join(str(dec[d]) for d in range(12)) + " |")
        L += ["", "By the eater's generation: " + ", ".join(f"{g}{'+' if g == 5 else ''}: {gen[g]}" for g in range(6)) + "."]
        L += ["", "## Beside it (population first)", "",
              "| arm | median population, year 60 / 120 | deaths | illness | starvation | old age | thirst | animals | other |",
              "|---|---|---|---|---|---|---|---|---|"]
        for a in ARMS:
            rs = [rows[a][s] for s in seeds]
            p60 = statistics.median(r["pops"][5] if len(r["pops"]) > 5 else 0 for r in rs)
            p120 = statistics.median(r["pops"][11] if len(r["pops"]) > 11 else 0 for r in rs)
            cz = Counter(dd[1] for r in rs for dd in r["deaths"])
            tot = sum(cz.values())
            animals = sum(v for k, v in cz.items() if k in ("wolf", "bear", "animal", "hunting"))
            other = tot - sum(cz[k] for k in ("illness", "starvation", "old age", "thirst")) - animals
            L.append(f"| {a} | {p60:.0f} / {p120:.0f} | {tot} | {cz['illness']} | {cz['starvation']} | {cz['old age']} | "
                     f"{cz['thirst']} | {animals} | {other} |")
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
