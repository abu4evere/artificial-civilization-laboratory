"""FS1 analysis, written before any data (questions.md, frozen as `FS1-frozen`).

  python experiments/FS1_founder_start/analyse_fs1.py            # writes results.md
  python experiments/FS1_founder_start/analyse_fs1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_fs1  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
SEEDS = run_fs1.SMOKE_SEEDS if SMOKE else run_fs1.SEEDS
ARMS, WPY, AGES = run_fs1.ARMS, run_fs1.WPY, run_fs1.AGES
REPS = 10_000
RNG = np.random.default_rng(20261028)
MARGIN = 0.012            # one making act's skill gain from zero (skill_gain), fixed before data
COLLAPSE = 4              # z's extra worlds extinct by year 100 that mark its primary "survivors only"
NAME = {"t": "today", "z": "zero start", "c": "no crafting start", "x": "sham"}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {a: {} for a in ARMS}
    for f in glob.glob(str(OUTDIR / "*_seed_*.json")):
        r = json.load(open(f))
        if r["arm"] in runs:
            runs[r["arm"]][r["seed"]] = r
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    present = all(sorted(runs[a]) == sorted(SEEDS) for a in ARMS)
    fps = {r["code_hash"] for a in ARMS for r in runs[a].values()} | \
          {r["code_hash_after"] for a in ARMS for r in runs[a].values()}
    ok = "All: PASS" in zero and present and len(fps) == 1
    L = ["# FS1 — Is the erosion the founders' head start wearing off? Results"
         + (" (SMOKE TEST, throwaway seeds)" if SMOKE else ""), "",
         "Frozen as `FS1-frozen`. run_fs1.py, analyse_fs1.py (written before data).", "", "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({sum(len(v) for v in runs.values())} of {len(ARMS) * len(SEEDS)}): "
         f"**{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_fs1`): **{'yes' if len(fps) == 1 else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    seeds = sorted(SEEDS)
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])

    def col(arm, field, lo, hi):
        """Per seed: the sum of a census field over census years lo..hi-1 (a dead world adds nothing)."""
        out = []
        for s in seeds:
            r = runs[arm][s]
            i = r["census_fields"].index(field)
            out.append(float(sum(row[i] for row in r["census"] if lo <= row[0] < hi)))
        return np.array(out)

    def pooled(num, den):
        point = num.sum() / den.sum() if den.sum() else float("nan")
        with np.errstate(invalid="ignore", divide="ignore"):
            reps = (W @ num) / (W @ den)
        return point, reps

    def diff(arm, field_num, field_den, lo, hi, base="t"):
        pa, ra = pooled(col(arm, field_num, lo, hi), col(arm, field_den, lo, hi))
        pb, rb = pooled(col(base, field_num, lo, hi), col(base, field_den, lo, hi))
        d = ra - rb
        rt = ra / rb
        dlo, dhi = np.nanpercentile(d, [2.5, 97.5])
        rlo, rhi = np.nanpercentile(rt, [2.5, 97.5])
        return pa, pb, pa - pb, dlo, dhi, pa / pb if pb else float("nan"), rlo, rhi

    ext100 = {a: sum(1 for s in seeds if runs[a][s]["final_tick"] < 100 * WPY) for a in ARMS}
    ext_all = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in ARMS}
    L += [f"Paired seeds: {n}; {run_fs1.YEARS} years.", "",
          "| arm | extinct by year 100 | extinct by year 500 | mean living, years 0–100 | mean living, years "
          "300–500 |", "|---|---|---|---|---|"]
    for a in ARMS:
        L.append(f"| {a} ({NAME[a]}) | {ext100[a]} | {ext_all[a]} | {col(a, 'living', 0, 100).sum() / (n * 100):.1f} | "
                 f"{col(a, 'living', 300, 500).sum() / (n * 200):.1f} |")
    collapse = ext100["z"] - ext100["t"] >= COLLAPSE
    L += ["", f"**Collapse flag (z has ≥ {COLLAPSE} more worlds extinct by year 100 than t): "
              f"{'RAISED' if collapse else 'not raised'}** ({ext100['z']} vs {ext100['t']}).", ""]

    # Primary
    L += ["## Primary — world-born adults' (20–40) crafting skill, years 300–500", "",
          f"Margin ±{MARGIN} (one making act's skill gain from zero). Survivor-weighted: only living adults count.", "",
          "| arm | mean skill | contributing worlds | adult-years | − today [95%] | ÷ today [95%] | reading |",
          "|---|---|---|---|---|---|---|"]
    for a in ("t", "z", "c", "x"):
        N = col(a, "wb_adults_20_40", 300, 500)
        if a == "t":
            p, _ = pooled(col(a, "wb_craft_sum_20_40", 300, 500), N)
            L.append(f"| t ({NAME[a]}) | {p:.4f} | {int((N > 0).sum())} | {N.sum():,.0f} | | | |")
            continue
        pa, pb, d, dlo, dhi, rt, rlo, rhi = diff(a, "wb_craft_sum_20_40", "wb_adults_20_40", 300, 500)
        if -MARGIN < dlo and dhi < MARGIN:
            read = "converges"
        elif dlo > MARGIN:
            read = "zero start higher"
        elif dhi < -MARGIN:
            read = "zero start lower"
        else:
            read = "not shown"
        if a == "x":
            read = "(yardstick)"
        elif a == "z" and collapse:
            read += " (survivors only, after an early collapse; c is the main test)"
        L.append(f"| {a} ({NAME[a]}) | {pa:.4f} | {int((N > 0).sum())} | {N.sum():,.0f} | {d:+.4f} [{dlo:+.4f}, "
                 f"{dhi:+.4f}] | {rt:.3f} [{rlo:.3f}, {rhi:.3f}] | **{read}** |")
    L.append("")

    # Secondaries
    L += ["## Key secondaries (years 300–500; per adult-year)", "",
          "| arm | making events | − today [95%] | made things held | − today [95%] |", "|---|---|---|---|---|"]
    for a in ("t", "z", "c", "x"):
        mk = pooled(col(a, "makes", 300, 500), col(a, "adults", 300, 500))[0]
        it = pooled(col(a, "items_adults", 300, 500), col(a, "adults", 300, 500))[0]
        if a == "t":
            L.append(f"| t | {mk:.4f} | | {it:.3f} | |")
            continue
        m = diff(a, "makes", "adults", 300, 500)
        i = diff(a, "items_adults", "adults", 300, 500)
        L.append(f"| {a} | {mk:.4f} | {m[2]:+.4f} [{m[3]:+.4f}, {m[4]:+.4f}] | {it:.3f} | "
                 f"{i[2]:+.3f} [{i[3]:+.3f}, {i[4]:+.3f}] |")
    L += ["", "## The start (years 0–100), described", "",
          "| arm | world-born adults' crafting skill | all adults' crafting skill | making per adult-year | things "
          "held per adult |", "|---|---|---|---|---|"]
    for a in ("t", "z", "c", "x"):
        L.append(f"| {a} | {pooled(col(a, 'wb_craft_sum_20_40', 0, 100), col(a, 'wb_adults_20_40', 0, 100))[0]:.4f} | "
                 f"{pooled(col(a, 'adult_craft_sum', 0, 100), col(a, 'adults', 0, 100))[0]:.4f} | "
                 f"{pooled(col(a, 'makes', 0, 100), col(a, 'adults', 0, 100))[0]:.4f} | "
                 f"{pooled(col(a, 'items_adults', 0, 100), col(a, 'adults', 0, 100))[0]:.3f} |")
    L += ["", "## Skill by age (world-born, years 300–500; mean crafting skill, people counted)", "",
          "| arm | " + " | ".join(f"age {g}" for g in AGES) + " |", "|---|" + "---|" * len(AGES)]
    for a in ("t", "z", "c", "x"):
        cells = []
        for g in AGES:
            ssum = sum(runs[a][s]["skill_by_age"][str(g)][0] for s in seeds)
            cnt = sum(runs[a][s]["skill_by_age"][str(g)][1] for s in seeds)
            cells.append(f"{ssum / cnt:.4f} ({cnt:,})" if cnt else "–")
        L.append(f"| {a} | " + " | ".join(cells) + " |")
    L += ["", "## By century (all arms; world-born adults' crafting skill / mean living)", "",
          "| years | " + " | ".join(ARMS) + " |", "|---|" + "---|" * len(ARMS)]
    for lo in range(0, run_fs1.YEARS, 100):
        cells = []
        for a in ARMS:
            sk = pooled(col(a, "wb_craft_sum_20_40", lo, lo + 100), col(a, "wb_adults_20_40", lo, lo + 100))[0]
            cells.append(f"{sk:.4f} / {col(a, 'living', lo, lo + 100).sum() / (n * 100):.1f}")
        L.append(f"| {lo}–{lo + 100} | " + " | ".join(cells) + " |")
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
