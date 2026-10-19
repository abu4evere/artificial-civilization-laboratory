"""RT1b analysis in the frozen order (questions_rt1b.md, `RT1b-frozen`). Written and smoke-tested before any data.

  python experiments/RT1_residence_time/analyse_rt1b.py            # writes results_rt1b.md
  python experiments/RT1_residence_time/analyse_rt1b.py --smoke    # throwaway smoke outputs; writes nothing

Validity (no outcome shown otherwise): zero checks pass; all 768 worlds present; one code fingerprint; manipulation
checks: R4's and R4w's adults change the tile they sleep on in 15-35% of weeks (pooled); of R4w's thirsty adult-weeks,
under 5% followed a chosen trip to water (pooled).
Frozen reading, extinction (not reaching year 120 with someone alive): (1) R4w against C, (2) R4w against R4, each paired
by seed: exact sign test; effect = reference's extinction share - R4w's, 95% bootstrap (10,000 resamples,
random.Random(2026)); Holm over the two; yardstick +-0.117: p < 0.05 (Holm) "changes survival"; p >= 0.05 and the
interval inside +-0.117 "no meaningful effect"; otherwise "unresolved at this sample".
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "NV2_nature_v2"))
sys.path.insert(0, str(HERE.parent / "F1_baseline_fragility"))
import analyse_f1 as A  # noqa: E402
from analyse_nv2 import HALF_F2, boot, died, pooled  # noqa: E402
from analyse_rt1 import meeting, moves  # noqa: E402
from run_rt1b import ARMS, OUT, SEEDS, SMOKE_SEEDS  # noqa: E402
from scipy.stats import binomtest  # noqa: E402


def compare(rows, ref, a, seeds):
    d0 = [died(rows[ref][s]) for s in seeds]
    da = [died(rows[a][s]) for s in seeds]
    saved = sum(1 for x, y in zip(d0, da) if x and not y)
    lost = sum(1 for x, y in zip(d0, da) if y and not x)
    p = binomtest(saved, saved + lost).pvalue if saved + lost else 1.0
    return sum(da), saved, lost, p, boot(d0, da)


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, run = [0.0] * len(ps), 0.0
    for k, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - k) * ps[i]))
        adj[i] = run
    return adj


def water(rs):
    t = {}
    for r in rs:
        for k, v in r["water"].items():
            t[k] = t.get(k, 0) + v
    went = t.get("thirsty_but_went_to_water", 0) / t["thirsty"] if t.get("thirsty") else 0.0
    still = (t.get("of_those_still_short", 0) / t["reached_water_then_sent_back"]
             if t.get("reached_water_then_sent_back") else None)
    return went, still, t.get("reached_water_then_sent_back", 0)


def deaths(rs, cause, upto, stages=None):
    return sum(1 for r in rs for d in r["deaths"]
               if d[0] < upto and d[1] == cause and (stages is None or d[3] in stages))


def main(smoke=False):
    seeds = SMOKE_SEEDS if smoke else SEEDS
    out = HERE / "output_rt1b_smoke" if smoke else OUT
    rows, missing = {}, []
    for a in ARMS:
        for s in seeds:
            f = out / f"{a}_seed_{s}.json"
            if f.exists():
                rows.setdefault(a, {})[s] = json.loads(f.read_text(encoding="utf-8"))
            else:
                missing.append(f"{a} {s}")
    L = [f"# RT1b — residence time with the walk to water counted: results{' (SMOKE TEST, throwaway seeds)' if smoke else ''}",
         "", "Frozen as `RT1b-frozen`. run_rt1b.py, analyse_rt1b.py.", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks (off = code_rt1; without a base it does nothing; it acts; read-only; reload exact): "
             f"**{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing
    if not missing:
        allr = [r for a in rows.values() for r in a.values()]
        fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
        L.append(f"- One fingerprint (`code_rt1b`): **{'yes' if len(fps) == 1 else 'NO'}**")
        ok &= len(fps) == 1
        for a in ("r4", "r4w"):
            ch = moves([rows[a][s] for s in seeds])[0]
            t = ch is not None and 0.15 <= ch <= 0.35
            L.append(f"- Manipulation check, {a}: adults change the tile they sleep on in **{ch:.1%}** of weeks "
                     f"(needed 15–35%): **{'yes' if t else 'NO'}**")
            ok &= t
        went, _, _ = water([rows["r4w"][s] for s in seeds])
        t = went < 0.05
        L.append(f"- Manipulation check, the fix: of R4w's thirsty adult-weeks, **{went:.1%}** followed a chosen trip to "
                 f"water (needed under 5%): **{'yes' if t else 'NO'}**")
        ok &= t
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        nc = sum(died(rows["c"][s]) for s in seeds)
        L += ["", "## Baseline (rule 14)", "", f"C died out in {nc} of {len(seeds)} worlds ({nc / len(seeds):.1%}).", "",
              "## Extinction (the frozen reading)", "",
              "| comparison | R4w died out | reference died out | saved / lost | p | Holm p | effect (reference − R4w) | "
              "95% interval | reading |",
              "|---|---|---|---|---|---|---|---|---|"]
        res = {ref: compare(rows, ref, "r4w", seeds) for ref in ("c", "r4")}
        adj = dict(zip(("c", "r4"), holm([res["c"][3], res["r4"][3]])))
        for ref in ("c", "r4"):
            n, sv, lo, p, (e, lo95, hi95) = res[ref]
            nref = sum(died(rows[ref][s]) for s in seeds)
            lab = ("**changes survival**" if adj[ref] < 0.05 else
                   "**no meaningful effect**" if -HALF_F2 < lo95 and hi95 < HALF_F2 else "unresolved at this sample")
            L.append(f"| R4w against {ref.upper()} | {n} | {nref} | {sv} / {lo} | {p:.3g} | {adj[ref]:.3g} | {e:+.3f} | "
                     f"[{lo95:+.3f}, {hi95:+.3f}] | {lab} |")
        L += ["", "## Beside it (described; population first, rule 18)", "",
              "| arm | median population, year 60 / 119 | births per woman-year | blocked for want of a partner | "
              "between-lineage meeting | thirst deaths, years 0–39 / 0–119 | adult starvation deaths, years 0–39 | "
              "weeks changing tile | thirsty after a chosen trip to water | sent back from water and still short |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for a in ARMS:
            rs = [rows[a][s] for s in seeds]
            pop = lambda i: statistics.median(r["pops"][i] if len(r["pops"]) > i else 0 for r in rs)  # noqa: E731
            rt = pooled(rs)
            ch = moves(rs)[0]
            went, still, nb = water(rs)
            st = f"{still:.3f} (of {nb})" if still is not None else "–"
            L.append(f"| {a} | {pop(5):.0f} / {pop(11):.0f} | {A.fmt(rt.get('births_per_woman_year'))} | "
                     f"{A.fmt(rt.get('block_no_partner'))} | {meeting(rs):.4f} | {deaths(rs, 'thirst', 40)} / "
                     f"{deaths(rs, 'thirst', 120)} | {deaths(rs, 'starvation', 40, ('adult', 'elder'))} | {ch:.1%} | "
                     f"{went:.1%} | {st} |")
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results_rt1b.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
