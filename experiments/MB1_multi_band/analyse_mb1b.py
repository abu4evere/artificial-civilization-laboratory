"""MB1b analysis in the frozen order (questions_mb1b.md, `MB1b-frozen`). Written and smoke-tested before any data.

  python experiments/MB1_multi_band/analyse_mb1b.py            # writes results_mb1b.md
  python experiments/MB1_multi_band/analyse_mb1b.py --smoke    # throwaway smoke outputs; writes nothing

Validity (no outcome shown otherwise): zero checks pass; all 1,024 worlds present; one code fingerprint; manipulation
check (each world's founding bands are as many and as large as its arm says).
Frozen reading: extinction, b8 and b16 each against p4 paired by seed; exact sign test; effect = p4's share - arm's;
95% bootstrap (10,000, random.Random(2026)); Holm over the two; yardstick +-0.117. The sham against p4 must be quiet.
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
from run_mb1b import ARMS, OUT, SEEDS, SMOKE_SEEDS  # noqa: E402
from scipy.stats import binomtest  # noqa: E402


def compare(rows, a, seeds):
    d0 = [died(rows["p4"][s]) for s in seeds]
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


def mixing(rs):
    met = sum(r["mb1a"]["tot"].get("met", 0) for r in rs)
    exp = sum(r["mb1a"]["tot"].get("exposed", 0) for r in rs)
    return met / exp if exp else None


def cross_couples(rs):
    pc = sum(r["mb1a"]["tot"].get("pair_cross", 0) for r in rs)
    pa = sum(r["mb1a"]["tot"].get("pair", 0) for r in rs)
    return pc / pa if pa else None


def main(smoke=False):
    seeds = SMOKE_SEEDS if smoke else SEEDS
    out = HERE / "output_mb1b_smoke" if smoke else OUT
    rows, missing = {}, []
    for a in ARMS:
        for s in seeds:
            f = out / f"{a}_seed_{s}.json"
            if f.exists():
                rows.setdefault(a, {})[s] = json.loads(f.read_text(encoding="utf-8"))
            else:
                missing.append(f"{a} {s}")
    L = [f"# MB1b — same 80 people, divided differently: results{' (SMOKE TEST, throwaway seeds)' if smoke else ''}", "",
         "Frozen as `MB1b-frozen`. run_mb1b.py, analyse_mb1b.py.", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks (setting 0 = code_v2 at 20 and 80 founders; b8, b16 act; observers read-only): **{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing
    if not missing:
        allr = [r for a in rows.values() for r in a.values()]
        fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
        L.append(f"- One fingerprint (`code_mb1b`): **{'yes' if len(fps) == 1 else 'NO'}**")
        ok &= len(fps) == 1
        bad = [f"{r['arm']} {r['seed']}" for r in allr if not r["manipulation_ok"]]
        L.append(f"- Manipulation check (founding bands as many and as large as each arm says): "
                 f"**{'yes' if not bad else 'NO: ' + ', '.join(bad[:8])}**")
        ok &= not bad
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        n0 = sum(died(rows["p4"][s]) for s in seeds)
        L += ["", "## Baseline (rule 14)", "", f"P4 (4 bands of 20) died out in {n0} of {len(seeds)} worlds ({n0 / len(seeds):.1%}).",
              "", "## Extinction against P4 (the frozen reading)", "",
              "| arm | died out | saved / lost | p | Holm p | effect (P4 − arm) | 95% interval | reading |",
              "|---|---|---|---|---|---|---|---|"]
        res = {a: compare(rows, a, seeds) for a in ("b8", "b16", "sham")}
        adj = dict(zip(("b8", "b16"), holm([res["b8"][3], res["b16"][3]])))
        for a in ("b8", "b16", "sham"):
            n, sv, lo, p, (e, lo95, hi95) = res[a]
            if a == "sham":
                lab, pa = ("**caveat: the sham reached p < 0.05**" if p < 0.05 else "quiet"), p
            else:
                pa = adj[a]
                lab = ("**dividing changes survival**" if pa < 0.05 else
                       "**no meaningful effect**" if -HALF_F2 < lo95 and hi95 < HALF_F2 else "unresolved at this sample")
            L.append(f"| {a} | {n} | {sv} / {lo} | {p:.3g} | {pa:.3g} | {e:+.3f} | [{lo95:+.3f}, {hi95:+.3f}] | {lab} |")
        L += ["", "## Beside it (described; population first, rule 18)", "",
              "| arm | median population, year 60 / 119 | births per woman-year | blocked for want of a partner | "
              "between-lineage meeting per adult pair-year | couples between lineages | lineages alive at the end (median) | most bands on one island (median) | smallest gap between band centres (median) |",
              "|---|---|---|---|---|---|---|---|---|"]
        for a in ARMS:
            rs = [rows[a][s] for s in seeds]
            pop = lambda i: statistics.median(r["pops"][i] if len(r["pops"]) > i else 0 for r in rs)  # noqa: E731
            rt = pooled(rs)
            lin = statistics.median((r["mb1a"]["lineages_alive"] or [0])[-1] for r in rs)
            mbi = statistics.median(r["placement"]["max_bands_per_island"] for r in rs)
            gap = statistics.median(r["placement"]["min_centre_gap"] for r in rs if r["placement"]["min_centre_gap"] is not None)
            mx = mixing(rs)
            L.append(f"| {a} | {pop(5):.0f} / {pop(11):.0f} | {A.fmt(rt.get('births_per_woman_year'))} | "
                     f"{A.fmt(rt.get('block_no_partner'))} | {mx:.4f} | {A.fmt(cross_couples(rs))} | {lin:.0f} | {mbi:.0f} | {gap:.0f} |")
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results_mb1b.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
