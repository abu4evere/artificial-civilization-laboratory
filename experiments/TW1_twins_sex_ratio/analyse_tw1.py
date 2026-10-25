"""TW1 analysis in the frozen order (questions.md, `TW1-frozen`). Written before any data.

  python experiments/TW1_twins_sex_ratio/analyse_tw1.py            # writes results.md
  python experiments/TW1_twins_sex_ratio/analyse_tw1.py --smoke    # throwaway smoke outputs; writes nothing

Validity: zero checks pass; all 512 worlds present; one fingerprint (`code_tw1`).
Manipulation (hard stops; pooled over arm T, per delivery; exact binomial tests, a check fails if p < 0.001, i.e. the
target lies outside the 99.9% interval): twin deliveries against 0.014; identical-twin deliveries against 0.004; boys
among independent sex draws (singletons, both fraternal twins, one per identical pair) against 105/205. In arm C: no
twins at all. Independence from mother's age, previous births and population: described only (shown by code and unit
tests).
Adoption rule: if valid and the manipulation checks pass, both settings are proposed for nature (v7); everything else
is described, never used to accept or refuse.
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_tw1 import ARMS, OUT, SEEDS, SMOKE_SEEDS  # noqa: E402
from scipy.stats import binomtest  # noqa: E402


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
    L = [f"# TW1 — twins and the sex ratio at birth: results{' (SMOKE TEST, throwaway seeds)' if smoke else ''}", "",
         "Frozen as `TW1-frozen`. run_tw1.py, analyse_tw1.py (written before data).", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks: **{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing
    if missing:
        L += ["", "**NOT VALID: no outcome is shown.**"]
        return finish(L, smoke)
    allr = [r for a in rows.values() for r in a.values()]
    fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
    L.append(f"- One fingerprint (`code_tw1`): **{'yes' if len(fps) == 1 else 'NO'}**")
    ok &= len(fps) == 1
    T = [d for s in seeds for d in rows["t"][s]["deliveries"]]
    C = [d for s in seeds for d in rows["c"][s]["deliveries"]]
    D = len(T)
    tw = sum(1 for d in T if d[4] != "single")
    mz = sum(1 for d in T if d[4] == "identical")
    sexes = []
    for d in T:
        sexes += d[5][:1] if d[4] == "identical" else d[5]
    boys = sum(1 for x in sexes if x == "M")
    p_tw = binomtest(tw, D, 0.014).pvalue if D else 0.0
    p_mz = binomtest(mz, D, 0.004).pvalue if D else 0.0
    p_sx = binomtest(boys, len(sexes), 105 / 205).pvalue if sexes else 0.0
    c_tw = sum(1 for d in C if d[4] != "single")
    man = p_tw >= 0.001 and p_mz >= 0.001 and p_sx >= 0.001 and c_tw == 0
    L += ["", "## Manipulation check (pooled over arm T, per delivery)", "",
          "| check | observed | target | exact p | passes |", "|---|---|---|---|---|",
          f"| twin deliveries | {tw} of {D:,} ({1000 * tw / max(D, 1):.1f} per 1,000) | 14 per 1,000 | {p_tw:.3g} | {'yes' if p_tw >= 0.001 else 'NO'} |",
          f"| identical-twin deliveries | {mz} of {D:,} ({1000 * mz / max(D, 1):.1f} per 1,000) | 4 per 1,000 | {p_mz:.3g} | {'yes' if p_mz >= 0.001 else 'NO'} |",
          f"| boys per 100 girls (independent draws) | {boys} of {len(sexes):,} ({100 * boys / max(len(sexes) - boys, 1):.1f}) | 105 | {p_sx:.3g} | {'yes' if p_sx >= 0.001 else 'NO'} |",
          f"| twin deliveries in arm C | {c_tw} | 0 | | {'yes' if c_tw == 0 else 'NO'} |",
          "", f"- Manipulation check: **{'passes' if man else 'FAILS'}**"]
    ok &= man
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if not ok:
        return finish(L, smoke)
    L += ["", "## The adoption rule (frozen)", "",
          "**Both settings (twins at a fixed random chance; boys 105 to girls 100) are proposed for nature (v7).** "
          "What they do below is reported, not used to accept or refuse. The creator decides."]
    L += ["", "## Described: independence (shown by code; here only described)", "",
          "| group | deliveries | twin deliveries per 1,000 |", "|---|---|---|"]
    groups = [("mother under 25", lambda d: d[1] < 25), ("mother 25-35", lambda d: 25 <= d[1] < 35),
              ("mother 35+", lambda d: d[1] >= 35), ("first delivery", lambda d: d[2] == 0),
              ("1-2 before", lambda d: 1 <= d[2] <= 2), ("3+ before", lambda d: d[2] >= 3)]
    pops = sorted(d[3] for d in T)
    t1, t2 = pops[len(pops) // 3], pops[2 * len(pops) // 3]
    groups += [("population low third", lambda d: d[3] < t1), ("middle third", lambda d: t1 <= d[3] < t2),
               ("high third", lambda d: d[3] >= t2)]
    for name, f in groups:
        g = [d for d in T if f(d)]
        L.append(f"| {name} | {len(g):,} | {1000 * sum(1 for d in g if d[4] != 'single') / max(len(g), 1):.1f} |")
    L += ["", "## Described: survival of twins and singletons in arm T (pooled; full follow-up only)", "",
          "| born as | to age 1 | to age 5 | to age 15 |", "|---|---|---|---|"]
    for kind in ("single", "fraternal", "identical"):
        cells = []
        for a in ("1", "5", "15"):
            s_ = sum(rows["t"][s]["survival"][kind][a][0] for s in seeds)
            n_ = sum(rows["t"][s]["survival"][kind][a][1] for s in seeds)
            cells.append(f"{s_ / n_:.3f} (of {n_:,})" if n_ else "-")
        L.append(f"| {kind} | " + " | ".join(cells) + " |")
    tm = [m for s in seeds for m in rows["t"][s]["twin_mothers"]]
    L.append(f"\nMothers of twins who died within a year of the delivery: {sum(m['died_within_year'] for m in tm)} "
             f"of {len(tm)}. Identical pairs in which both reached 16: "
             f"{sum(rows['t'][s]['identical_pairs_both_16'] for s in seeds)}.")
    L += ["", "## Described: population, survival, sex ratio (population first)", "",
          "| arm | time-averaged population | median pop. yr 60 / 120 | died out | deliveries | boys per 100 girls reaching 16 / 30 / 50 |",
          "|---|---|---|---|---|---|"]
    for a in ARMS:
        rs = [rows[a][s] for s in seeds]
        ta = statistics.fmean(tavg(r) for r in rs)
        p60 = statistics.median(r["pops"][5] if len(r["pops"]) > 5 else 0 for r in rs)
        p120 = statistics.median(r["pops"][11] if len(r["pops"]) > 11 else 0 for r in rs)
        died = sum(1 for r in rs if r["final_tick"] < 120 * 52)
        dl = sum(len(r["deliveries"]) for r in rs)
        ratios = []
        for age in ("16", "30", "50"):
            m = sum(r["reached_by_sex"][age]["M"] for r in rs)
            f = sum(r["reached_by_sex"][age]["F"] for r in rs)
            ratios.append(f"{100 * m / max(f, 1):.0f}")
        L.append(f"| {a} | {ta:.2f} | {p60:.0f} / {p120:.0f} | {died} | {dl:,} | {' / '.join(ratios)} |")
    L += ["", "| arm | deaths | starvation | illness | old age | thirst | killed | childbirth |", "|---|---|---|---|---|---|---|---|"]
    for a in ARMS:
        ds = [d for s in seeds for d in rows[a][s]["deaths"]]
        cnt = lambda k: sum(1 for d in ds if d[1] == k)  # noqa: E731
        L.append(f"| {a} | {len(ds):,} | {cnt('starvation'):,} | {cnt('illness'):,} | {cnt('old age'):,} | "
                 f"{cnt('thirst'):,} | {cnt('killed'):,} | {cnt('childbirth'):,} |")
    return finish(L, smoke)


def finish(L, smoke):
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
