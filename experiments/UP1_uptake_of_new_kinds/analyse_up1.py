"""UP1 analysis, written before any data (questions.md, frozen as `UP1-frozen`).

  python experiments/UP1_uptake_of_new_kinds/analyse_up1.py                      # writes results.md
  python experiments/UP1_uptake_of_new_kinds/analyse_up1.py --smoke --dir <folder>
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
import run_up1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261104)
NAMES = ("1 holding", "2 value floor", "3 cannot make", "4a running-best skip", "4b beaten", "5 eligible, not chosen",
         "made")


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
    m = re.search(r"code_v11 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    seeds = sorted(runs)
    present = (len(seeds) > 0) if SMOKE else seeds == sorted(R.SEEDS)
    fps = {r["code_hash"] for r in runs.values()} | {r["code_hash_after"] for r in runs.values()}
    mism = sum(sum(r["mismatch"].values()) for r in runs.values())
    ok = bool(zero_ok and present and fps == {fp_now} and mism == 0)
    L = ["# UP1 — Why is a new kind never made again? Results", "",
         "Frozen as `UP1-frozen`. run_up1.py, analyse_up1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks (All: PASS, same `code_v11` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(seeds)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_v11`'s: **{'yes' if fps == {fp_now} else 'NO'}**",
         f"- The reproduced make option equals the code's at every decision (mismatches 0): "
         f"**{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def counts(cls, cx=None, early=None):
        M = np.zeros((n, 7))
        for j, s in enumerate(seeds):
            for k, v in runs[s]["steps"].items():
                c, x, e = k.split("|")
                if c == cls and (cx is None or x == cx) and (early is None or e == early):
                    M[j] += v
        return M

    def shares(M):
        tot = M.sum(1)
        pt = M.sum(0) / M.sum()
        with np.errstate(invalid="ignore", divide="ignore"):
            rep = (W @ M) / (W @ tot)[:, None]
        return pt, rep
    New, Old = counts("new"), counts("old")
    pt, rep = shares(New)
    ci = [pct(rep[:, i]) for i in range(7)]
    main_k = [i for i in range(7) if ci[i][0] > 0.50]
    reading = f"mainly blocked at step {NAMES[main_k[0]]}" if main_k else "mixed bottlenecks"
    L += ["## Primary (frozen): where new kinds stop (shares of person x kind x decisions, years 100-200)", "",
          f"New kinds: {len(set().union(*[runs[s]['per_kind'].keys() for s in seeds])):,}; "
          f"person x kind x decisions: {int(New.sum()):,} (old kinds: {int(Old.sum()):,}).", "",
          "| step | new kinds: share [95%] | old kinds: share | new - old [95%] |", "|---|---|---|---|"]
    opt, orep = shares(Old) if Old.sum() else (np.zeros(7), np.zeros((REPS, 7)))
    diffs = []
    for i in range(7):
        d = rep[:, i] - orep[:, i]
        dl, dh = pct(d)
        diffs.append((pt[i] - opt[i], dl, dh))
        L.append(f"| {NAMES[i]} | {pt[i]:.4f} [{ci[i][0]:.4f}, {ci[i][1]:.4f}] | {opt[i]:.4f} | "
                 f"{pt[i] - opt[i]:+.4f} [{dl:+.4f}, {dh:+.4f}] |")
    sig_pos = [i for i in range(7) if diffs[i][1] > 0]
    main_diff = max(sig_pos, key=lambda i: diffs[i][0]) if sig_pos else None
    L += ["", f"Rule: \"mainly blocked at step k\" if one step's share has its lower bound above 0.50; otherwise "
          f"\"mixed bottlenecks\".", "", f"**Reading: {reading}.**", "",
          f"Secondary (Gemini): the main difference from old kinds: "
          f"**{NAMES[main_diff] if main_diff is not None else 'none with an interval above 0'}**.", ""]
    # Secondary
    L += ["## Secondary (described, not decisive)", ""]
    for cx in ("simple", "nested"):
        for cls, M in (("new", counts("new", cx)), ("old", counts("old", cx))):
            if M.sum():
                s = M.sum(0) / M.sum()
                L.append(f"- {cls} kinds, {cx}: " + ", ".join(f"{NAMES[i].split(' ')[0]} {s[i]:.3f}" for i in range(7))
                         + f" ({int(M.sum()):,} decisions)")
    for e in ("early", "later"):
        M = counts("new", early=e)
        if M.sum():
            s = M.sum(0) / M.sum()
            L.append(f"- new kinds, {'first five years after invention' if e == 'early' else 'after five years'}: " +
                     ", ".join(f"{NAMES[i].split(' ')[0]} {s[i]:.3f}" for i in range(7)) + f" ({int(M.sum()):,})")
    kinds = [v for s in seeds for v in runs[s]["per_kind"].values() if sum(v)]
    if kinds:
        kw = np.mean([np.array(v) / sum(v) for v in kinds], axis=0)
        L.append("- kind-weighted (each new kind once): " + ", ".join(f"{NAMES[i].split(' ')[0]} {kw[i]:.3f}"
                                                                      for i in range(7)) + f" ({len(kinds):,} kinds)")
        ever_el = sum(1 for v in kinds if v[5] + v[6] > 0)
        ever_made = sum(1 for v in kinds if v[6] > 0)
        L.append(f"- new kinds ever eligible (step 5 or made): {ever_el:,} of {len(kinds):,}; ever made: {ever_made:,}")
    w_ = {}
    for s in seeds:
        for k, v in runs[s]["winner"].items():
            w_[k] = w_.get(k, 0) + v
    if w_:
        L.append("- at step 4, the winning make option was: " + ", ".join(f"{k} kind {v:,}" for k, v in sorted(w_.items())))
    for cls in ("new", "old"):
        e = sum(runs[s]["p5"][cls][0] for s in seeds)
        if e:
            L.append(f"- {cls} kinds as the make option: {int(e):,} decisions; mean make probability "
                     f"{sum(runs[s]['p5'][cls][1] for s in seeds) / e:.3f}")
    L.append("")
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
