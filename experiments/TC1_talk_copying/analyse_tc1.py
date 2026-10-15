"""TC1 analysis (questions.md, frozen as `TC1-frozen`). Written and smoke-tested before any data.

  python experiments/TC1_talk_copying/analyse_tc1.py discovery   # writes results_discovery.md
  python experiments/TC1_talk_copying/analyse_tc1.py holdout     # writes results_holdout.md, with the agreement check
  python experiments/TC1_talk_copying/analyse_tc1.py --smoke     # throwaway smoke output (10 years); writes nothing

Frozen reading (decision rules), primary 1 = per world, mean over children reaching 20 of (r with parents at birth − r
with an unrelated adult), paired by seed against W:
- "the copying rule makes people alike": N's median at least twice W's, paired Wilcoxon p < 0.05;
- "the world makes them alike": the ratio N ÷ W (medians) within 0.75–1.25 with its whole 95% bootstrap interval;
- otherwise "unresolved at this sample".
A reading stands only if discovery and holdout agree. S is described against both, on both primaries (primary 2 = own
experience's weighted share). Extinction: exact sign test against W. No outcome is shown if the run is not valid.
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from pathlib import Path

from scipy.stats import binomtest, wilcoxon

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "BL0_habit_use"))
sys.path.insert(0, str(HERE))
from analyse_bl0 import per_world  # noqa: E402
from run_tc1 import ARMS, OUT, R  # noqa: E402

NAMES = {"w": "W (whole table, today)", "s": "S (speaker's situation)", "n": "N (no copying)", "sham": "sham"}


def p1(r):
    xs = [d[1] - d[2] for d in r["desc"] if d[0] == 20 and d[1] is not None and d[2] is not None]
    return statistics.mean(xs) if xs else None


def boot_ratio(ws, ns, k=10_000):
    pairs = [(a, b) for a, b in zip(ws, ns) if a is not None and b is not None]
    if not pairs:
        return None, None, None
    rng = random.Random(2026)
    def ratio(ps):
        mw = statistics.median(a for a, _ in ps)
        return statistics.median(b for _, b in ps) / mw if mw else None
    bs = sorted(x for x in (ratio(rng.choices(pairs, k=len(pairs))) for _ in range(k)) if x is not None)
    return ratio(pairs), bs[int(0.025 * len(bs))], bs[int(0.975 * len(bs)) - 1]


def wil(a, b):
    d = [y - x for x, y in zip(a, b) if x is not None and y is not None and y != x]
    if not d:
        return 1.0
    try:
        return float(wilcoxon(d).pvalue)
    except ValueError:
        return 1.0


def load(seeds, out=OUT):
    rows, missing = {}, []
    for a in ARMS:
        for s in seeds:
            f = out / f"{a}_seed_{s}.json"
            if f.exists():
                rows.setdefault(a, {})[s] = json.loads(f.read_text(encoding="utf-8"))
            else:
                missing.append(f"{a} {s}")
    return rows, missing


def reading(rows, seeds):
    W = [p1(rows["w"][s]) for s in seeds]
    N = [p1(rows["n"][s]) for s in seeds]
    ws, ns = [x for x in W if x is not None], [x for x in N if x is not None]
    if not ws or not ns:                       # no child reached 20 (only in a short smoke test)
        return "unresolved at this sample", None, None, 1.0, (None, None, None)
    mw, mn = statistics.median(ws), statistics.median(ns)
    p = wil(W, N)
    ratio = boot_ratio(W, N)
    if mw and mn >= 2 * mw and p < 0.05:
        lab = "the copying rule makes people alike"
    elif ratio[1] is not None and 0.75 <= ratio[1] and ratio[2] <= 1.25:
        lab = "the world makes them alike"
    else:
        lab = "unresolved at this sample"
    return lab, mw, mn, p, ratio


def f(x, nd=3):
    return "–" if x is None else f"{x:.{nd}f}"


def main(which, smoke=False):
    seeds = (9601,) if smoke else (R.DISCOVERY if which == "discovery" else R.HOLDOUT)
    if smoke:
        rows, missing = load(seeds, HERE / "output_smoke")
    else:
        rows, missing = load(seeds)
    L = [f"# TC1 — talk copying: results ({'SMOKE TEST, throwaway seed' if smoke else which})", "",
         "Frozen as `TC1-frozen`. run_tc1.py, analyse_tc1.py.", "", "## Validity", ""]
    ok = True
    if not smoke:
        z = OUT / "zero.txt"
        zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
        L.append(f"- Zero check (defaults = control = code_bl0; S and N differ; parts add up): **{'yes' if zt else 'NO'}**")
        ok &= zt
        L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
        ok &= not missing
        rep = all(r.get("reproduces_bl0") for r in rows.get("w", {}).values())
        L.append(f"- W reproduces BL0 exactly on every world: **{'yes' if rep else 'NO'}**")
        ok &= rep
    allr = [r for a in rows.values() for r in a.values()]
    fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
    err = max(r["max_split_error"] for r in allr)
    dif = all(rows[a][s]["world_hash"] != rows["w"][s]["world_hash"] for a in ("s", "n") for s in seeds
              if s in rows.get(a, {}) and s in rows.get("w", {}))
    L += [f"- One fingerprint (`code_tc1`): **{'yes' if len(fps) == 1 else 'NO'}**",
          f"- Parts add up in every arm (largest error {err:.2g}): **{'yes' if err <= 1e-9 else 'NO'}**",
          f"- S and N differ from W in every world: **{'yes' if dif else 'NO'}**"]
    ok &= len(fps) == 1 and err <= 1e-9 and dif
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        P = {a: {s: per_world(rows[a][s]) for s in seeds} for a in ARMS}
        surv = {a: sum(1 for s in seeds if rows[a][s]["final_tick"] >= 120 * 52) for a in ARMS}
        L += ["", "## Population and survival (rules 14 and 18)", "",
              "| arm | survived 120 years | median population, year 120 |", "|---|---|---|"]
        for a in ARMS:
            pops = [rows[a][s]["pops"][11] if len(rows[a][s]["pops"]) > 11 else 0 for s in seeds]
            L.append(f"| {NAMES[a]} | {surv[a]} of {len(seeds)} | {statistics.median(pops):.0f} |")
        L += ["", "## The measures (medians across worlds; paired against W)", "",
              "| arm | sameness: parents − unrelated r at 20 | own experience share | copied share | choice effect | p vs W (sameness) | p vs W (own share) |",
              "|---|---|---|---|---|---|---|"]
        W1 = [p1(rows["w"][s]) for s in seeds]
        WE = [P["w"][s]["w_E"] for s in seeds]
        for a in ARMS:
            A1 = [p1(rows[a][s]) for s in seeds]
            AE = [P[a][s]["w_E"] for s in seeds]
            AT = [P[a][s]["w_T"] for s in seeds]
            CE = [P[a][s]["ce_adult"] for s in seeds]
            med = lambda xs: statistics.median([x for x in xs if x is not None]) if any(x is not None for x in xs) else None  # noqa: E731
            L.append(f"| {NAMES[a]} | {f(med(A1))} | {f(med(AE))} | {f(med(AT))} | {f(med(CE))} | "
                     f"{'–' if a == 'w' else f(wil(W1, A1), 4)} | {'–' if a == 'w' else f(wil(WE, AE), 4)} |")
        lab, mw, mn, p, ratio = reading(rows, seeds)
        L += ["", "## The frozen reading", "",
              f"N against W, sameness: W {f(mw)}, N {f(mn)}; ratio N ÷ W {f(ratio[0])} [{f(ratio[1])}, {f(ratio[2])}]; "
              f"paired Wilcoxon p = {p:.3g}.", "", f"**{lab}**", "",
              "## Extinction against W (exact sign test, rule 14)", "", "| arm | died out | saved / lost | p |", "|---|---|---|---|"]
        dw = {s: rows["w"][s]["final_tick"] < 120 * 52 for s in seeds}
        for a in ("s", "n", "sham"):
            da = {s: rows[a][s]["final_tick"] < 120 * 52 for s in seeds}
            saved = sum(1 for s in seeds if dw[s] and not da[s])
            lost = sum(1 for s in seeds if da[s] and not dw[s])
            pp = binomtest(saved, saved + lost).pvalue if saved + lost else 1.0
            L.append(f"| {NAMES[a]} | {sum(da.values())} (W {sum(dw.values())}) | {saved} / {lost} | {pp:.3g} |")
        if which == "holdout" and not smoke:
            drows, dmiss = load(R.DISCOVERY)
            if not dmiss:
                dl = reading(drows, R.DISCOVERY)[0]
                L += ["", "## Do discovery and holdout agree?", "", f"Discovery: **{dl}**. Holdout: **{lab}**. "
                      + (f"**Stands: {lab}.**" if dl == lab else "**No reading** (they disagree).")]
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / f"results_{which}.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        main("discovery", smoke=True)
    else:
        main(sys.argv[1])
