"""FF3 analysis, written before any data (questions.md, frozen as `FF3-frozen`).

  python experiments/FF3_name_ties/analyse_ff3.py                      # writes results.md
  python experiments/FF3_name_ties/analyse_ff3.py --smoke --dir <folder>
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
import run_ff3 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261121)
ARMS = ("c", "f", "x")
NAME = {"c": "v13", "f": "f", "x": "sham"}
WPY = R.WPY
MEMS = ("recipes", "marks", "records", "puzzles")


def pct(x):
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


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
    m = re.search(r"code_ff3 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    if SMOKE:
        seeds = sorted(set.intersection(*[set(runs[a]) for a in ARMS if runs[a]]))
        present = len(seeds) > 0
    else:
        seeds = sorted(R.SEEDS)
        present = all(sorted(runs[a]) == seeds for a in ARMS)
    allr = [r for a in ARMS for r in runs[a].values()]
    fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
    ok = bool(zero_ok and present and fps == {fp_now})
    L = ["# FF3: Memory ties settled by name, a fault fix in nature v13 (results)", "",
         "Frozen as `FF3-frozen`. run_ff3.py, analyse_ff3.py (written before data). Years 100–200.", "", "## Validity", "",
         f"- Zero checks (All: PASS, same `code_ff3` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_ff3`'s: **{'yes' if fps == {fp_now} else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    arms = [a for a in ARMS if all(s in runs[a] for s in seeds)]
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def col(a, key):
        return np.array([float(runs[a][s]["sums"].get(key, 0)) for s in seeds])

    def ratio_of(a, b, num, den=None):
        """(arm a's pooled num/den) / (arm b's), with a paired bootstrap interval; den None = plain sums."""
        na, nb = col(a, num), col(b, num)
        if den is None:
            da, db = np.ones(n), np.ones(n)
        else:
            da, db = col(a, den), col(b, den)
        with np.errstate(invalid="ignore", divide="ignore"):
            pt = (na.sum() / da.sum()) / (nb.sum() / db.sum()) if den else na.sum() / nb.sum()
            rep = ((W @ na) / (W @ da)) / ((W @ nb) / (W @ db)) if den else (W @ na) / (W @ nb)
        return float(pt), *pct(rep)

    ext = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in arms}

    # --- Decision (frozen): harm only, f against v13
    pop = ratio_of("f", "c", "living_weeks")
    g = (["population"] if pop[0] < 0.90 and pop[2] < 1.0 else []) + (["extinctions"] if ext["f"] - ext["c"] >= 3 else [])
    reading = "harm: investigate" if g else "no harm"
    L += ["## Decision (frozen): a check for harm only, f against v13", "",
          "| contrast | living-weeks ratio [95%] | extinct worlds (arm, v13) |", "|---|---|---|"]
    for a in ("f", "x"):
        if a in arms:
            r = ratio_of(a, "c", "living_weeks")
            L.append(f"| {NAME[a]} / v13 | {r[0]:.4f} [{r[1]:.4f}, {r[2]:.4f}] | {ext[a]}, {ext['c']} |")
    L += ["", "Guards (f against v13): population if the ratio is below 0.90 with its upper bound below 1; extinctions if "
          "f has 3 or more extinct worlds beyond v13's.", "",
          f"**Reading: {reading}.**" + (f" **Guard raised: {', '.join(g)}.**" if g else " No guard raised."), ""]

    # --- Flags (frozen): described measures, f against v13, ratio outside [0.8, 1.25] with the interval wholly outside 1
    measures = []
    for mname in MEMS:
        measures += [(f"{mname}: evictions per adult-week", f"{mname}_evict", "adult_weeks"),
                     (f"{mname}: evictions with a tie, per eviction", f"{mname}_tie", f"{mname}_evict")]
    measures += [("recipes: the newest dropped, per eviction", "recipes_newest_dropped", "recipes_evict"),
                 ("world-new kinds", "new_kinds", None),
                 ("kinds made again by their inventor within 5 years", "remade_kinds", None),
                 ("makes per adult-week", "adult_makes", "adult_weeks"),
                 ("adult-weeks", "adult_weeks", None)]
    L += ["## Flags for investigation (f against v13; frozen rule: ratio outside [0.8, 1.25] with its 95% interval "
          "wholly outside 1)", "", "| measure | f / v13 [95%] | sham / v13 [95%] | flag |", "|---|---|---|---|"]
    flags = []
    for label, num, den in measures:
        rf = ratio_of("f", "c", num, den)
        rx = ratio_of("x", "c", num, den) if "x" in arms else (float("nan"),) * 3
        flag = bool(np.isfinite(rf[0]) and (rf[0] < 0.8 or rf[0] > 1.25) and (rf[1] > 1 or rf[2] < 1))
        if flag:
            flags.append(label)
        L.append(f"| {label} | {rf[0]:.4f} [{rf[1]:.4f}, {rf[2]:.4f}] | {rx[0]:.4f} [{rx[1]:.4f}, {rx[2]:.4f}] | "
                 f"{'**FLAG**' if flag else 'no'} |")
    L += ["", f"**Flags: {', '.join(flags) if flags else 'none'}.**", ""]

    # --- Described, per arm
    L += ["## Described (not decisive), per arm", "",
          "| arm | living-weeks | adult-weeks | recipes: evictions, ties, newest dropped, kept at birth | marks: evictions, "
          "ties | records: evictions, ties | puzzles: evictions, ties | draws | world-new kinds, remade | makes per "
          "adult-year |", "|---|---|---|---|---|---|---|---|---|---|"]
    for a in arms:
        su = lambda k: sum(runs[a][s]["sums"].get(k, 0) for s in seeds)  # noqa: E731
        aw = su("adult_weeks") or 1
        re_ = su("recipes_evict")
        kept = 1 - su("recipes_newest_dropped") / re_ if re_ else float("nan")
        draws = sum(su(f"{mn}_draws") for mn in MEMS)
        L.append(f"| {NAME[a]} | {int(su('living_weeks')):,} | {int(su('adult_weeks')):,} | {int(re_):,}, "
                 f"{int(su('recipes_tie')):,}, {int(su('recipes_newest_dropped')):,}, {kept:.3f} | "
                 f"{int(su('marks_evict')):,}, {int(su('marks_tie')):,} | {int(su('records_evict')):,}, "
                 f"{int(su('records_tie')):,} | {int(su('puzzles_evict')):,}, {int(su('puzzles_tie')):,} | {int(draws):,} | "
                 f"{int(su('new_kinds')):,}, {int(su('remade_kinds')):,} | {WPY * su('adult_makes') / aw:.4f} |")
    L.append("")
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
