"""CL1 analysis, written before any data (questions.md, frozen as `CL1-frozen`; operational note 1).

  python experiments/CL1_calibration_ledger/analyse_cl1.py            # writes results.md
  python experiments/CL1_calibration_ledger/analyse_cl1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_cl1 import ROUTES, SEEDS, SUMS  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261027)
ERAS = ["0-50", "50-100", "100-200"]
COMMON = ("forage", "give", "talk", "gather")
SHOW = ("make", "forage", "give", "talk", "gather")
J = {k: i for i, k in enumerate(SUMS)}
TERMS = ["C_td - G"] + [f"C_{r}" for r in ROUTES[1:]]


def pooled(r, era, acts):
    out = np.zeros(len(SUMS))
    for a in acts:
        out += np.array(r["cells"].get(f"{era}|{a}", [0.0] * len(SUMS)))
    return out


def split(s):
    n = s[..., J["n"]]
    with np.errstate(divide="ignore", invalid="ignore"):
        t = {"C_td - G": (s[..., J["C_td"]] - s[..., J["G"]]) / n}
        for r in ROUTES[1:]:
            t[f"C_{r}"] = s[..., J[f"C_{r}"]] / n
        t["q - G"] = (s[..., J["q"]] - s[..., J["G"]]) / n
        t["q"] = s[..., J["q"]] / n
        t["G"] = s[..., J["G"]] / n
        t["C_td"] = s[..., J["C_td"]] / n
        t["gap"] = s[..., J["gap"]] / s[..., J["gap_n"]]
    return t


def ci(x):
    x = np.asarray(x)
    x = x[np.isfinite(x)]
    if not len(x):
        return "[-]"
    lo, hi = np.percentile(x, [2.5, 97.5])
    return f"[{lo:+.3f}, {hi:+.3f}]"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rs = [json.load(open(f)) for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json")))]
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    fps = {r["code_hash"] for r in rs} | {r["code_hash_after"] for r in rs}
    mism = sum(sum(r["mismatch"].values()) for r in rs)
    seeds_ok = sorted(r["seed"] for r in rs) == sorted(SEEDS)
    ok = "All: PASS" in zero and seeds_ok and len(fps) == 1 and mism == 0
    L = ["# CL1 — Which route carries the miscalibration? Results", "",
         "Frozen as `CL1-frozen` (operational note 1). run_cl1.py, analyse_cl1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({len(rs)} of {len(SEEDS)}): **{'yes' if seeds_ok else 'NO'}**",
         f"- One fingerprint (`code_v7`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- TD replay exact and the ledger adds up at every update and decade (mismatches 0): "
         f"**{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    W = np.stack([np.bincount(row, minlength=len(rs)) for row in RNG.integers(0, len(rs), size=(REPS, len(rs)))])
    for title, acts, q in (("Q1 — The common actions pooled (forage, give, talk, gather)", COMMON, "Q1"),
                           ("Q2 — Make", ("make",), "Q2")):
        per = np.stack([pooled(r, 2, acts) for r in rs])
        if not per[:, J["n"]].sum():
            continue
        pt = split(per.sum(0))
        bs = split(W @ per)
        L += [f"## {title}: q − G split by route (adults, years 100-200; {per[:, J['n']].sum():.0f} updates)", "",
              f"q {pt['q']:.3f} − G {pt['G']:.3f} = **{pt['q - G']:+.3f}** {ci(bs['q - G'])}, exactly:", "",
              "| term | value [95%] | share of q − G |", "|---|---|---|"]
        for t in TERMS:
            L.append(f"| {t} | {pt[t]:+.4f} {ci(bs[t])} | {pt[t] / pt['q - G']:.2f} |")
        L += [f"| (check: sum) | {sum(pt[t] for t in TERMS):+.4f} | 1.00 |", "",
              f"Own-experience value C_td {pt['C_td']:.3f} against G {pt['G']:.3f}; the max gap {pt['gap']:.3f}.", ""]
        if q == "Q1":
            largest = max(TERMS, key=lambda t: pt[t])
            L += [f"**The term carrying the largest share of the over-valuation: {largest} "
                  f"({pt[largest]:+.3f}, share {pt[largest] / pt['q - G']:.2f}).**", ""]
    # Q3
    L += ["## Q3 — By era and action (adults)", "",
          "| era | action | updates | q | G | q − G | " + " | ".join(TERMS) + " | max gap |", "|---" * (7 + len(TERMS)) + "|"]
    for e, name in enumerate(ERAS):
        for a in SHOW + ("(common pooled)",):
            acts = COMMON if a == "(common pooled)" else (a,)
            s = sum((pooled(r, e, acts) for r in rs), np.zeros(len(SUMS)))
            if not s[J["n"]]:
                continue
            t = split(s)
            L.append(f"| {name} | {a} | {s[J['n']]:.0f} | {t['q']:.3f} | {t['G']:.3f} | {t['q - G']:+.3f} | "
                     + " | ".join(f"{t[x]:+.3f}" for x in TERMS) + f" | {t['gap']:.3f} |")
    L.append("")
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
