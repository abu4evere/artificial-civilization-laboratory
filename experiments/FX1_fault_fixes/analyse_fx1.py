"""FX1 analysis, written before any data (questions.md, frozen as `FX1-frozen`).

  python experiments/FX1_fault_fixes/analyse_fx1.py                      # writes results.md
  python experiments/FX1_fault_fixes/analyse_fx1.py --smoke --dir <folder>
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
import run_fx1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261107)
ARMS = ("c", "f", "f1", "f23", "x")
NAME = {"c": "v11", "f": "f", "f1": "f1", "f23": "f23", "x": "sham"}
WPY = R.WPY


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
    m = re.search(r"code_fx1 fingerprint: ([0-9a-f]{64})", zero)
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
    L = ["# FX1: Fixing three faults in nature v11 (results)", "",
         "Frozen as `FX1-frozen`. run_fx1.py, analyse_fx1.py (written before data).", "", "## Validity", "",
         f"- Zero checks (All: PASS, same `code_fx1` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_fx1`'s: **{'yes' if fps == {fp_now} else 'NO'}**", "",
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

    # --- Decision (frozen): harm only, f against v11
    pop = ratio_of("f", "c", "living_weeks")
    g = (["population"] if pop[0] < 0.90 and pop[2] < 1.0 else []) + (["extinctions"] if ext["f"] - ext["c"] >= 3 else [])
    reading = "harm: investigate" if g else "no harm"
    L += ["## Decision (frozen): a check for harm only, f against v11", "",
          "| contrast | living-weeks ratio [95%] | extinct worlds (arm, v11) |", "|---|---|---|"]
    for a in ("f", "f1", "f23", "x"):
        if a in arms:
            r = ratio_of(a, "c", "living_weeks")
            L.append(f"| {NAME[a]} / v11 | {r[0]:.4f} [{r[1]:.4f}, {r[2]:.4f}] | {ext[a]}, {ext['c']} |")
    L += ["", "Guards (f against v11): population if the ratio is below 0.90 with its upper bound below 1; extinctions if "
          "f has 3 or more extinct worlds beyond v11's.", "",
          f"**Reading: {reading}.**" + (f" **Guard raised: {', '.join(g)}.**" if g else " No guard raised."), ""]

    # --- Flags (frozen): described measures, f against v11, ratio outside [0.8, 1.25] with the interval wholly outside 1
    measures = [("makes per adult-year", "adult_makes", "adult_weeks"),
                ("kinds invented per adult-year", None, "adult_weeks"),
                ("made things held per adult", "census_items", "census_adults"),
                ("things on the ground at year 200", "ground_end", None),
                ("adult-weeks", "adult_weeks", None)]
    L += ["## Flags for investigation (f against v11; frozen rule: ratio outside [0.8, 1.25] with its 95% interval "
          "wholly outside 1)", "", "| measure | f / v11 [95%] | sham / v11 [95%] | flag |", "|---|---|---|---|"]
    flags = []
    for label, num, den in measures:
        if num is None:            # kinds: from the per-world count n_kinds
            for a in arms:
                for s in seeds:
                    runs[a][s]["sums"]["_kinds"] = runs[a][s]["n_kinds"]
            num = "_kinds"
        rf, rx = ratio_of("f", "c", num, den), ratio_of("x", "c", num, den)
        flag = (rf[0] < 0.8 or rf[0] > 1.25) and (rf[1] > 1 or rf[2] < 1)
        if flag:
            flags.append(label)
        L.append(f"| {label} | {rf[0]:.4f} [{rf[1]:.4f}, {rf[2]:.4f}] | {rx[0]:.4f} [{rx[1]:.4f}, {rx[2]:.4f}] | "
                 f"{'**FLAG**' if flag else 'no'} |")
    L += ["", f"**Flags: {', '.join(flags) if flags else 'none'}.**", ""]

    # --- Described
    L += ["## Described (not decisive)", "",
          "| arm | adult decisions with a make option | rules differ | offer is the newest recipe | v11 rule's offer is "
          "the newest | fixed rule's offer is the newest | heir's things "
          "deleted | heir's things dropped | from a body, dropped | makes per adult-year | kinds per 100 adult-years | "
          "lineage R (kinds, remade) | made things per adult | on the ground at year 200 (mean per world) |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for a in arms:
        su = lambda k: sum(runs[a][s]["sums"].get(k, 0) for s in seeds)  # noqa: E731
        off = su("offers") or 1
        ay = su("adult_weeks") / WPY or 1
        nk = sum(runs[a][s]["n_kinds"] for s in seeds)
        nr = sum(runs[a][s]["n_remade"] for s in seeds)
        L.append(f"| {NAME[a]} | {int(su('offers')):,} | {su('offers_differ') / off:.4f} | "
                 f"{su('offers_newest') / off:.4f} | {su('old_rule_newest') / off:.4f} | "
                 f"{su('new_rule_newest') / off:.4f} | {int(su('heir_deleted')):,} | {int(su('heir_dropped')):,} | "
                 f"{int(su('body_dropped')):,} | {su('adult_makes') / ay:.4f} | {100 * nk / ay:.3f} | "
                 f"{(nr / nk if nk else float('nan')):.4f} ({nk:,}, {nr:,}) | "
                 f"{su('census_items') / (su('census_adults') or 1):.3f} | {su('ground_end') / n:.1f} |")
    L.append("")
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
