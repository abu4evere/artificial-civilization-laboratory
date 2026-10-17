"""RT1 analysis in the frozen order (questions.md, `RT1-frozen`, `RT1-amend1`). Written and smoke-tested before any data.

  python experiments/RT1_residence_time/analyse_rt1.py            # writes results.md
  python experiments/RT1_residence_time/analyse_rt1.py --smoke    # throwaway smoke outputs; writes nothing

Validity (no outcome shown otherwise): zero checks pass; all 768 worlds present; one code fingerprint; the manipulation
check: R4's adults change the tile they sleep on in 15-35% of weeks (pooled), and R4's distance a month (pooled mean) is
within +-25% of C's.
Frozen reading, extinction (not reaching year 120 with someone alive), R4 against C paired by seed: exact sign test on
worlds that differ; effect = C's extinction share - R4's, 95% bootstrap (10,000 resamples, random.Random(2026));
yardstick +-0.117: p < 0.05 "residence time changes survival"; p >= 0.05 and the interval inside +-0.117 "no meaningful
effect on survival"; otherwise "unresolved at this sample". The sham against C must be quiet.
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
from run_rt1 import ARMS, OUT, SEEDS, SMOKE_SEEDS  # noqa: E402
from scipy.stats import binomtest  # noqa: E402


def compare(rows, a, seeds):
    dc = [died(rows["c"][s]) for s in seeds]
    da = [died(rows[a][s]) for s in seeds]
    saved = sum(1 for x, y in zip(dc, da) if x and not y)
    lost = sum(1 for x, y in zip(dc, da) if y and not x)
    p = binomtest(saved, saved + lost).pvalue if saved + lost else 1.0
    return sum(da), saved, lost, p, boot(dc, da)


def moves(rs):
    t = {k: sum(r["moves"][k] for r in rs) for k in rs[0]["moves"]}
    return (t["changed"] / t["pairs"] if t["pairs"] else None,
            t["month_sum"] / t["month_n"] if t["month_n"] else None,
            t["hunt_success_part"] / (t["adult_weeks"] / 52) if t["adult_weeks"] else None)


def meeting(rs):
    met = sum(r["mb1a"]["tot"].get("met", 0) for r in rs)
    exp = sum(r["mb1a"]["tot"].get("exposed", 0) for r in rs)
    return met / exp if exp else None


def adult_starvation(rs, upto=40):
    return sum(1 for r in rs for d in r["deaths"] if d[0] < upto and d[1] == "starvation" and d[3] in ("adult", "elder"))


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
    L = [f"# RT1 — residence time: results{' (SMOKE TEST, throwaway seeds)' if smoke else ''}", "",
         "Frozen as `RT1-frozen`, Amendment 1 `RT1-amend1`. run_rt1.py, analyse_rt1.py.", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks (off = code_v2; observers read-only; R4 acts; save and reload exact): **{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing
    if not missing:
        allr = [r for a in rows.values() for r in a.values()]
        fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
        L.append(f"- One fingerprint (`code_rt1`): **{'yes' if len(fps) == 1 else 'NO'}**")
        ok &= len(fps) == 1
        mc, mr = moves([rows["c"][s] for s in seeds]), moves([rows["r4"][s] for s in seeds])
        share_ok = mr[0] is not None and 0.15 <= mr[0] <= 0.35
        dist_ok = mr[1] is not None and mc[1] and 0.75 <= mr[1] / mc[1] <= 1.25
        L.append(f"- Manipulation check: R4's adults change the tile they sleep on in **{mr[0]:.1%}** of weeks (C {mc[0]:.1%}; "
                 f"needed 15–35%): **{'yes' if share_ok else 'NO'}**; distance a month **{mr[1]:.2f}** tiles against C's "
                 f"{mc[1]:.2f} (ratio {mr[1] / mc[1]:.2f}; needed 0.75–1.25): **{'yes' if dist_ok else 'NO'}**")
        ok &= share_ok and dist_ok
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        nc = sum(died(rows["c"][s]) for s in seeds)
        L += ["", "## Baseline (rule 14)", "", f"C died out in {nc} of {len(seeds)} worlds ({nc / len(seeds):.1%}).", "",
              "## Extinction against C (the frozen reading)", "",
              "| arm | died out | saved / lost | p | effect (C − arm) | 95% interval |", "|---|---|---|---|---|---|"]
        res = {}
        for a in ("r4", "sham"):
            n, sv, lo, p, (e, lo95, hi95) = compare(rows, a, seeds)
            res[a] = (p, lo95, hi95)
            L.append(f"| {a} | {n} | {sv} / {lo} | {p:.3g} | {e:+.3f} | [{lo95:+.3f}, {hi95:+.3f}] |")
        p, lo95, hi95 = res["r4"]
        lab = ("residence time changes survival" if p < 0.05 else
               "no meaningful effect on survival" if -HALF_F2 < lo95 and hi95 < HALF_F2 else "unresolved at this sample")
        L += ["", f"**Frozen rule: {lab}.**" + (" (Caveat: the sham reached p < 0.05.)" if res["sham"][0] < 0.05 else "")]
        L += ["", "## Beside it (described; population first, rule 18)", "",
              "| arm | median population, year 60 / 119 | births per woman-year | decisions blocked for want of a partner | "
              "between-lineage meeting per adult pair-year | adult starvation deaths, years 0–39 | successful hunts per adult-year | "
              "weeks changing tile | distance a month |",
              "|---|---|---|---|---|---|---|---|---|"]
        for a in ARMS:
            rs = [rows[a][s] for s in seeds]
            pop = lambda i: statistics.median(r["pops"][i] if len(r["pops"]) > i else 0 for r in rs)  # noqa: E731
            rt = pooled(rs)
            ch, mo, hu = moves(rs)
            L.append(f"| {a} | {pop(5):.0f} / {pop(11):.0f} | {A.fmt(rt.get('births_per_woman_year'))} | "
                     f"{A.fmt(rt.get('block_no_partner'))} | {meeting(rs):.4f} | {adult_starvation(rs)} | {hu:.3f} | "
                     f"{ch:.1%} | {mo:.2f} |")
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
