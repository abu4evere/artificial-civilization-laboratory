"""PB1b analysis, written before any study data (questions.md, frozen as `PB1b-frozen`).

  python experiments/PB1b_episodic_predictor/analyse_pb1b.py                      # writes results.md
  python experiments/PB1b_episodic_predictor/analyse_pb1b.py --smoke --dir <folder>
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
import run_pb1b as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261113)
OUTPUTS = ("food gained", "net food", "health", "energy", "materials", "things held", "distance", "new kind",
           "affection")
NAME = {"B": "B (table)", "E": "E-own", "Eo": "E-obs", "E5": "E-obs-0.5", "L5": "L-obs-0.5", "Ek5": "E-own k=5", "Ek15": "E-own k=15"}


def pct(x):
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {}
    for f in sorted(glob.glob(str(OUTDIR / "c_seed_*.json"))):
        r = json.load(open(f))
        runs[r["seed"]] = r
    zero = ""
    for name in ("zero_cloud.log", "zero_local.log"):
        if (HERE / name).exists():
            zero = (HERE / name).read_text(encoding="utf-8", errors="replace")
            break
    R.base.setup(R.CODE)
    fp_now = R.base.fingerprint(R.CODE)
    m = re.search(r"code_v13 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    seeds = sorted(runs) if SMOKE else sorted(R.SEEDS)
    present = bool(seeds) and all(s in runs for s in seeds)
    fps = {runs[s]["code_hash"] for s in runs} | {runs[s]["code_hash_after"] for s in runs}
    ok = bool(zero_ok and present and fps == {fp_now})
    L = ["# PB1b: A shadow brain with episodic memory (results)", "",
         "Frozen as `PB1b-frozen`. run_pb1b.py, analyse_pb1b.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks (All: PASS, same `code_v13` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(runs)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_v13`'s: **{'yes' if fps == {fp_now} else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    seeds = [s for s in seeds if s in runs]
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def sse(v, case):              # per world, summed over the 9 outputs
        return np.array([sum(runs[s]["sse"][v][case]) for s in seeds])

    def skill(v, case):
        a, b = sse(v, case), sse("B", case)
        with np.errstate(invalid="ignore", divide="ignore"):
            pt = 1.0 - a.sum() / b.sum() if b.sum() else float("nan")
            rep = 1.0 - (W @ a) / (W @ b)
        return pt, *pct(rep)

    def cnt(case):
        return sum(runs[s]["counts"].get(case, 0) for s in seeds)

    # --- The gate (frozen; round 60): E-own against B
    def gate(v):
        u, f = skill(v, "u_pair"), skill(v, "fam")
        return u, f, (u[1] > 0), (f[1] >= -0.02)
    u, f, ok_u, ok_f = gate("E")
    reading = ("GO to PB2 with an episodic memory" if ok_u and ok_f else
               "memory without generalisation" if ok_f else "not yet")
    L += ["## The gate (frozen): E-own against the table B", "",
          "| part | cases | skill of E-own [95%] | holds |", "|---|---|---|---|",
          f"| 1. unfamiliar (situation, action), common actions | {cnt('u_pair'):,} | {u[0]:+.4f} [{u[1]:+.4f}, {u[2]:+.4f}] | "
          f"{'yes' if ok_u else 'no'} (interval wholly above 0) |",
          f"| 2. familiar (lived before) | {cnt('fam'):,} | {f[0]:+.4f} [{f[1]:+.4f}, {f[2]:+.4f}] | "
          f"{'yes' if ok_f else 'no'} (lower end >= -0.02) |", "",
          f"**Reading: {reading}.**", ""]
    uo, fo, ok_uo, ok_fo = gate("Eo")
    L += ["## E-obs (described; preferred for PB2 if it passes the gate and beats E-own on unfamiliar cases)", "",
          f"- unfamiliar: {uo[0]:+.4f} [{uo[1]:+.4f}, {uo[2]:+.4f}]; familiar: {fo[0]:+.4f} [{fo[1]:+.4f}, {fo[2]:+.4f}]; "
          f"passes the gate: **{'yes' if ok_uo and ok_fo else 'no'}**", ""]
    cases = ("u_pair", "fam", "u_prop", "all", "rare", "u_place", "w0", "w1", "w2", "w3")
    label = {"u_pair": "unfamiliar pairs (gate part 1)", "fam": "familiar (gate part 2)",
             "u_prop": "unfamiliar property combinations", "all": "all own weeks",
             "rare": "rare actions", "u_place": "unfamiliar destination", "w0": "first 100 weeks lived",
             "w1": "100-500 weeks", "w2": "500-1,000 weeks", "w3": "over 1,000 weeks"}
    L += ["## Every variant against B (described; no multiplicity claim)", "",
          "| cases | weeks | " + " | ".join(NAME[v] for v in R.VARIANTS if v != "B") + " |",
          "|---|---|" + "---|" * (len(R.VARIANTS) - 1)]
    for c in cases:
        cells = []
        for v in R.VARIANTS:
            if v == "B":
                continue
            s = skill(v, c)
            cells.append(f"{s[0]:+.3f} [{s[1]:+.3f}, {s[2]:+.3f}]")
        L.append(f"| {label[c]} | {cnt(c):,} | " + " | ".join(cells) + " |")

    def diff(v1, v2, case="u_pair"):
        a1, a2 = sse(v1, case), sse(v2, case)
        b = sse("B", case)
        with np.errstate(invalid="ignore", divide="ignore"):
            pt = (a2.sum() - a1.sum()) / b.sum()
            rep = ((W @ a2) - (W @ a1)) / (W @ b)
        return pt, *pct(rep)
    dd = diff("Eo", "E")
    L += ["", f"- E-obs over E-own on unfamiliar pairs (skill difference): {dd[0]:+.4f} [{dd[1]:+.4f}, {dd[2]:+.4f}] → "
          f"**{'observation is preferred for PB2' if (dd[1] > 0 and ok_uo and ok_fo) else 'own memory only'}**.",
          "- Nearest-memory distance on unfamiliar weeks (median of per-world medians): "
          f"{np.median([runs[s]['nearest_quartiles'][1] for s in seeds]):.3f}.", ""]
    # by output
    L += ["## By output: E-own and E-obs against B, all own weeks (described)", "",
          "| output | E-own | E-obs | B's mean squared standardised error (headroom) |", "|---|---|---|---|"]
    for k, o in enumerate(OUTPUTS):
        def sk(v):
            a = sum(runs[s]["sse"][v]["all"][k] for s in seeds)
            b = sum(runs[s]["sse"]["B"]["all"][k] for s in seeds)
            return 1 - a / b if b else float("nan")
        bmse = sum(runs[s]["sse"]["B"]["all"][k] for s in seeds) / max(1, cnt("all"))
        L.append(f"| {o} | {sk('E'):+.3f} | {sk('Eo'):+.3f} | {bmse:.3f} |")
    su = lambda key: sum(runs[s]["sums"].get(key, 0) for s in seeds)  # noqa: E731
    L += ["", "## Population and sample (beside every measure)", "",
          f"Followed adults {su('followed_people'):,}; their own prequential weeks {su('own_weeks'):,}; observed examples "
          f"{su('observed'):,}; living-weeks {su('living_weeks'):,}; extinct worlds "
          f"{sum(1 for s in seeds if runs[s]['extinct'])}.", ""]
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
