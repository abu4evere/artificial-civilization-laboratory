"""OD1 analysis (questions.md, frozen as `OD1-frozen`). Written before data. The gate: CI1's eight guards, each arm
against v16 (the doors, the doors without D1, and the sham as a validity check), paired world bootstrap (10,000 draws,
NumPy seed 20261130). The manipulation counts per door come first; the reading follows the creator's no-harm bar and
the pre-registered fallback order.

  python experiments/OD1_open_doors/analyse_od1.py [--smoke] [--dir <output>]
"""
from __future__ import annotations

import glob
import json
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_od1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261130)
ARMS = ("c", "o", "p", "x")
NAME = {"c": "v16", "o": "doors (D1-D5)", "p": "doors without D1", "x": "sham"}
WPY = R.WPY
LY = 1000 * WPY


def pct(x):
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


def finish(L):
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {a: {} for a in ARMS}
    for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json"))):
        r = json.load(open(f))
        if r["arm"] in runs:
            runs[r["arm"]][r["seed"]] = r
    zero = ""
    for name in ("zero_cloud.log", "zero_local.log"):
        if (HERE / name).exists():
            zero = (HERE / name).read_text(encoding="utf-8", errors="replace")
            break
    R.base.setup(R.CODE)
    fp_now = R.base.fingerprint(R.CODE)
    m = re.search(r"code_od1 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    if SMOKE:
        seeds = sorted(set.intersection(*[set(runs[a]) for a in ARMS if runs[a]]))
        present = len(seeds) > 0
    else:
        seeds = sorted(R.SEEDS)
        present = all(sorted(runs[a]) == seeds for a in ARMS)
    allr = [r for a in ARMS for r in runs[a].values()]
    fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
    bad = sum(r["parts_check"].get(k, 0) for r in allr for k in ("unexplained", "stage_E_without_event",
                                                                "stage_CD_without_all", "open_at_end"))
    ok = bool(zero_ok and present and fps == {fp_now} and bad == 0)
    L = ["# OD1: open the world's closed doors, once (results)", "",
         "Frozen as `OD1-frozen`. run_od1.py, analyse_od1.py (written before data).", "", "## Validity", "",
         f"- Zero checks (All: PASS, `code_od1` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(allr)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_od1`'s: **{'yes' if fps == {fp_now} else 'NO'}**",
         f"- MP1's part-tracking checks in every world: failures {bad}: **{'yes' if bad == 0 else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        finish(L)
        return
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def col(a, key):
        return np.array([float(runs[a][s]["sums"].get(key, 0)) for s in seeds])

    def colf(a, fn):
        return np.array([float(fn(runs[a][s])) for s in seeds])

    def od(a, key):
        return colf(a, lambda r: r["od"].get(key, 0))

    def rate(a, num, den, per=1.0):
        nu, de = col(a, num), col(a, den)
        with np.errstate(invalid="ignore", divide="ignore"):
            return (nu.sum() / de.sum() * per if de.sum() else float("nan")), (W @ nu) / (W @ de) * per

    def ratio(a, num, den, per=1.0):
        pa, ra = rate(a, num, den, per)
        pc, rc = rate("c", num, den, per)
        with np.errstate(invalid="ignore", divide="ignore"):
            return pa / pc if pc else float("nan"), ra / rc, pa, pc

    def diff(a, num, den, per=1.0):
        pa, ra = rate(a, num, den, per)
        pc, rc = rate("c", num, den, per)
        return pa - pc, ra - rc, pa, pc

    ext = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in ARMS}

    def guards(a):                         # CI1's eight, exactly as in LW1, FF4 and VW1
        out, rows = [], []
        r, rr, pa, pc = ratio(a, "death_starvation", "living_weeks", LY)
        lo, hi = pct(rr)
        rows.append(("starvation deaths per 1,000 living-years (ratio)", pa, pc, r, lo, hi))
        if r > 1.25 and lo > 1:
            out.append("starvation")
        d, dr, pa, pc = diff(a, "death_killed", "living_weeks", LY)
        lo, hi = pct(dr)
        rows.append(("killing deaths per 1,000 living-years (difference)", pa, pc, d, lo, hi))
        if d > 0.05 and lo > 0:
            out.append("killing")
        d, dr, pa, pc = diff(a, "census_health", "census_adults")
        lo, hi = pct(dr)
        rows.append(("adult health, mean (difference)", pa, pc, d, lo, hi))
        if d < -5 and hi < 0:
            out.append("adult health")
        lw_a, lw_c = col(a, "living_weeks"), col("c", "living_weeks")
        with np.errstate(invalid="ignore", divide="ignore"):
            r, rr = lw_a.sum() / lw_c.sum(), (W @ lw_a) / (W @ lw_c)
        lo, hi = pct(rr)
        rows.append(("living-weeks (ratio)", lw_a.sum(), lw_c.sum(), r, lo, hi))
        if r < 0.90 and hi < 1:
            out.append("population")
        rows.append(("extinct worlds (extra)", ext[a], ext["c"], ext[a] - ext["c"], float("nan"), float("nan")))
        if ext[a] - ext["c"] >= 3:
            out.append("extinction")
        r, rr, pa, pc = ratio(a, "child_deaths", "child_weeks", LY)
        lo, hi = pct(rr)
        rows.append(("child deaths per 1,000 child-years (ratio)", pa, pc, r, lo, hi))
        if r > 1.25 and lo > 1 and pa - pc >= 3:
            out.append("child deaths")
        r, rr, pa, pc = ratio(a, "child_death_starvation", "child_weeks", LY)
        lo, hi = pct(rr)
        rows.append(("child starvation deaths per 1,000 child-years (ratio)", pa, pc, r, lo, hi))
        if r > 1.25 and lo > 1:
            out.append("child starvation")
        r, rr, pa, pc = ratio(a, "gifts_kin_children", "adult_weeks", 1000)
        lo, hi = pct(rr)
        rows.append(("food gifts to kin's children per 1,000 adult-weeks (ratio)", pa, pc, r, lo, hi))
        if r < 0.80 and hi < 1:
            out.append("gifts to kin's children")
        return out, rows

    G = {a: guards(a) for a in ("o", "p", "x")}
    if not G["o"][0]:
        live, why = "o", "the full package (D1-D5) raises no guard"
    elif not G["p"][0]:
        live, why = "p", "the full package raises a guard and the doors without D1 raise none: D1 stays closed"
    else:
        live, why = None, "both raise a guard: nothing goes live; the world is frozen as v16"

    # the manipulation counts, per door, per 1,000 grown person-weeks (the made things per 1,000 makes for D1)
    gw = {a: od(a, "grown_weeks").sum() for a in ARMS}
    MAN = [("D1 makes with a stand-in input (per 1,000 makes)", lambda a: (od(a, "made_standin").sum(), od(a, "made_by_make").sum(), 1000)),
           ("D2 weeks above the old made-thing limit (per 1,000 grown weeks)", lambda a: (od(a, "over_items_weeks").sum(), gw[a], 1000)),
           ("D2 weeks above the old material limit (per 1,000 grown weeks)", lambda a: (od(a, "over_mats_weeks").sum(), gw[a], 1000)),
           ("D3 made binders used (per 1,000 grown weeks)", lambda a: (od(a, "made_binder_used").sum(), gw[a], 1000)),
           ("D4 made hammers used (per 1,000 grown weeks)", lambda a: (od(a, "made_hammer_used").sum(), gw[a], 1000)),
           ("D5 weeks a second thing adds warmth (per 1,000 grown weeks)", lambda a: (od(a, "layer_cold_weeks").sum(), gw[a], 1000)),
           ("D5 weeks a second thing adds carrying (per 1,000 grown weeks)", lambda a: (od(a, "layer_carry_weeks").sum(), gw[a], 1000))]

    def man_rate(a, fn):
        nu, de, per = fn(a)
        return nu / de * per if de else float("nan"), int(nu)

    barely = []
    if live is not None:                       # a door is barely exercised if all its counts are below 32 (one a world)
        most = {}
        for lab, fn in MAN:
            door = lab.split(" ")[0]
            if live == "p" and door == "D1":
                continue
            most[door] = max(most.get(door, 0), man_rate(live, fn)[1])
        barely = sorted(d for d, cnt in most.items() if cnt < 32)
    if live is None:
        reading = "harm: nothing goes live"
    elif barely:
        reading = f"no harm detected; doors barely exercised: {', '.join(barely)}"
    else:
        reading = "no harm detected under the tested conditions"

    L += ["## Manipulation counts (reported first)", "", "| door | " + " | ".join(NAME[a] for a in ARMS) + " |",
          "|---|" + "---|" * len(ARMS)]
    for lab, fn in MAN:
        cells = []
        for a in ARMS:
            v, cnt = man_rate(a, fn)
            cells.append(f"{v:.3f} ({cnt:,})" if np.isfinite(v) else f"- ({cnt:,})")
        L.append(f"| {lab} | " + " | ".join(cells) + " |")
    L += ["", "## Reading (frozen)", "",
          f"- **What goes live: {NAME[live] if live else 'nothing'}** ({why}).",
          f"- **Reading: {reading}.**",
          f"- Guards raised: doors {', '.join(G['o'][0]) or 'none'}; doors without D1 {', '.join(G['p'][0]) or 'none'}; "
          f"sham {', '.join(G['x'][0]) or 'none'} (validity check).", "",
          "Rule (the creator's bar): the doors go live if they raise no guard; if they do and the doors without D1 do "
          "not, those go live and D1 stays closed; if both do, nothing goes live. A door used fewer than 32 times in all "
          "worlds is reported as barely exercised; the doors still go live, labelled so. A pass means no detected harm "
          "under the tested conditions, not that the doors are harmless.", ""]
    for a in ("o", "p", "x"):
        L += [f"## Guards: {NAME[a]} against v16", "", f"| guard | {NAME[a]} | v16 | vs v16 [95%] |", "|---|---|---|---|"]
        for lab, pa, pc, v, lo, hi in G[a][1]:
            if "difference" in lab or "extra" in lab:
                L.append(f"| {lab} | {pa:,.4f} | {pc:,.4f} | {v:+.4f} [{lo:+.4f}, {hi:+.4f}] |")
            else:
                L.append(f"| {lab} | {pa:,.4f} | {pc:,.4f} | {v:.4f} [{lo:.4f}, {hi:.4f}] |")
        L.append("")

    # descriptives (pre-registered, not gates)
    L += ["## Descriptives (not gates)", "",
          "| arm | attacks | by a holder of a hard made thing | killings | by such a holder | made things carried, mean "
          "(sd) | max | materials carried, mean | makes per grown year |", "|---|---|---|---|---|---|---|---|---|"]
    for a in ARMS:
        g = gw[a]
        isum, isq = od(a, "items_sum").sum(), od(a, "items_sq").sum()
        mean = isum / g if g else float("nan")
        sd = (isq / g - mean ** 2) ** 0.5 if g else float("nan")
        mx = int(od(a, "items_max").max()) if len(seeds) else 0
        L.append(f"| {NAME[a]} | {int(od(a, 'attacks').sum()):,} | {int(od(a, 'attacks_by_hard_holder').sum()):,} | "
                 f"{int(od(a, 'kills').sum()):,} | {int(od(a, 'kills_by_hard_holder').sum()):,} | {mean:.3f} ({sd:.3f}) | "
                 f"{mx} | {od(a, 'mats_sum').sum() / g:.3f} | {od(a, 'made_by_make').sum() / g * WPY:.4f} |")
    L += ["", "| arm | things made with a stand-in: mean best tool factor | from the remembered inputs |", "|---|---|---|"]
    for a in ARMS:
        ns, no = od(a, "made_standin").sum(), od(a, "made_original").sum()
        fs = od(a, "factor_standin").sum() / ns if ns else float("nan")
        fo = od(a, "factor_original").sum() / no if no else float("nan")
        L.append(f"| {NAME[a]} | {fs:.4f} ({int(ns):,}) | {fo:.4f} ({int(no):,}) |")

    def stg(r, keys):
        return sum(r["stages"].get(f"stage_{k}", 0) for k in keys)
    L += ["", "| arm | new kinds needing a made part | any made part held (B+) | all held (C+) | made again (E) |",
          "|---|---|---|---|---|"]
    for a in ARMS:
        k = colf(a, lambda r: r["stages"].get("kinds", 0)).sum()
        if k:
            L.append(f"| {NAME[a]} | {int(k):,} | {colf(a, lambda r: stg(r, 'BCDE')).sum() / k:.4f} | "
                     f"{colf(a, lambda r: stg(r, 'CDE')).sum() / k:.4f} | {colf(a, lambda r: stg(r, 'E')).sum() / k:.4f} |")
        else:
            L.append(f"| {NAME[a]} | 0 | - | - | - |")
    L.append("")
    finish(L)


if __name__ == "__main__":
    main()
