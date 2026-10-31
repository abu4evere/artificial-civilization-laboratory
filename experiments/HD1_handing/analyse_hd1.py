"""HD1 analysis, written before any data (questions.md, frozen as `HD1-frozen`; operational note 1).

  python experiments/HD1_handing/analyse_hd1.py            # writes results.md
  python experiments/HD1_handing/analyse_hd1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_hd1 import ARMS, SEEDS, WPY  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261031)
NAME = {"c": "v10", "h": "h (handing)", "x": "sham"}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {a: {} for a in ARMS}
    for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json"))):
        r = json.load(open(f))
        runs[r["arm"]][r["seed"]] = r
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    present = all(sorted(runs[a]) == sorted(SEEDS) for a in ARMS)
    fps = {r["code_hash"] for a in ARMS for r in runs[a].values()} | \
          {r["code_hash_after"] for a in ARMS for r in runs[a].values()}
    mism = sum(sum(r["mismatch"].values()) for a in ARMS for r in runs[a].values())
    ok = "All: PASS" in zero and present and len(fps) == 1 and mism == 0
    L = ["# HD1 — Can a person hand a made thing to another? Results", "",
         "Frozen as `HD1-frozen` (operational note 1). run_hd1.py, analyse_hd1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)} of {len(SEEDS) * len(ARMS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_hd1`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Forage replay and conservation (mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    seeds = sorted(set(runs["c"]) & set(runs["h"]) & set(runs["x"]))
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])

    def col(a, k):
        return np.array([float(runs[a][s]["sums"].get(k, 0.0)) for s in seeds])

    def cens(a, i, y0=100, y1=200):
        return np.array([float(sum(c[i] for c in runs[a][s]["census"] if y0 <= c[0] < y1)) for s in seeds])

    def ratio(num, den):
        point = num.sum() / den.sum() if den.sum() else float("nan")
        with np.errstate(invalid="ignore", divide="ignore"):
            reps = (W @ num) / (W @ den)
        return point, reps

    def diff(a, b, num, den):
        """(pooled num/den in arm a) - (in arm b), paired world bootstrap."""
        pa, ra = ratio(col(a, num) if isinstance(num, str) else num[a], col(a, den) if isinstance(den, str) else den[a])
        pb, rb = ratio(col(b, num) if isinstance(num, str) else num[b], col(b, den) if isinstance(den, str) else den[b])
        lo, hi = np.nanpercentile(ra - rb, [2.5, 97.5])
        return pa - pb, lo, hi, pa, pb

    def rat(a, b, num, den):
        pa, ra = ratio(num[a], den[a])
        pb, rb = ratio(num[b], den[b])
        with np.errstate(invalid="ignore", divide="ignore"):
            lo, hi = np.nanpercentile(ra / rb, [2.5, 97.5])
        return pa / pb if pb else float("nan"), lo, hi, pa, pb

    ext = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in ARMS}
    L += [f"Paired seeds: {n}. Extinct: v10 {ext['c']}, h {ext['h']}, sham {ext['x']}.", ""]

    # primary: realized share of adults' foraged food added by tools
    R = {a: (col(a, "with") - col(a, "without")) for a in ARMS}
    Wf = {a: col(a, "with") for a in ARMS}
    dh = diff("h", "c", R, Wf)
    dx = diff("x", "c", R, Wf)
    L += ["## Primary — food added by tools (share of adults' foraged food, years 100-200)", "",
          "| arm | R |", "|---|---|"]
    for a in ARMS:
        L.append(f"| {NAME[a]} | {ratio(R[a], Wf[a])[0]:.4f} |")
    L += ["", f"**h - v10: {dh[0]:+.4f} [{dh[1]:+.4f}, {dh[2]:+.4f}]**; sham - v10: {dx[0]:+.4f} [{dx[1]:+.4f}, {dx[2]:+.4f}].", ""]

    # mechanism
    ay = {a: col(a, "adult_weeks") / WPY for a in ARMS}
    hands = {a: col(a, "hands") for a in ARMS}
    L += ["## Mechanism (years 100-200)", "", "| measure | v10 | h | sham |", "|---|---|---|---|"]

    def row(label, num, den, d=3):
        L.append(f"| {label} | " + " | ".join(f"{ratio(num[a], den[a])[0]:.{d}f}" for a in ARMS) + " |")
    row("handings per adult-year", hands, ay)
    row("share of adult forage weeks with a tool in hand", {a: col(a, "tool_weeks") for a in ARMS},
        {a: col(a, "forage_weeks") for a in ARMS})
    row("food gifts per adult-year", {a: col(a, "food_gifts") for a in ARMS}, ay, 2)
    row("recipients' forage weeks with a tool (within a year of receiving)",
        {a: col(a, "recipient_tool_weeks") for a in ARMS}, {a: col(a, "recipient_forage_weeks") for a in ARMS})
    rev = col("h", "reversals").sum() / hands["h"].sum() if hands["h"].sum() else float("nan")
    L += ["", f"Reversals in h (handed back to the giver within 4 weeks): {rev:.4f} of {hands['h'].sum():,.0f} handings.", ""]

    # flags
    pop = {a: col(a, "living_weeks") for a in ARMS}
    span = {a: np.full(n, 100.0 * WPY) for a in ARMS}
    fpa = {a: col(a, "with") for a in ARMS}
    aw = {a: col(a, "adult_weeks") for a in ARMS}
    rec = {a: cens(a, 4) for a in ARMS}
    adu = {a: cens(a, 2) for a in ARMS}
    gifts = {a: col(a, "food_gifts") for a in ARMS}
    cd = {a: col(a, "child_deaths") * 1000.0 for a in ARMS}
    cy = {a: col(a, "child_weeks") / WPY for a in ARMS}
    flags = {}
    L += ["## No-harm flags (h against v10; sham against v10 beside it)", "",
          "| flag | h ÷ v10 (or −) [95%] | sham ÷ v10 (or −) | raised |", "|---|---|---|---|"]
    for name, num, den, cut in (("population (mean living)", pop, span, 0.90), ("food per adult", fpa, aw, 0.90),
                                ("recipes held per adult", rec, adu, 0.90), ("food gifts per adult-year", gifts, ay, 0.95)):
        rh, rx = rat("h", "c", num, den), rat("x", "c", num, den)
        raised = rh[0] < cut and rh[2] < 1.0
        flags[name] = raised
        L.append(f"| {name} (< {cut} with upper < 1) | {rh[0]:.3f} [{rh[1]:.3f}, {rh[2]:.3f}] | {rx[0]:.3f} | "
                 f"{'**RAISED**' if raised else 'no'} |")
    ch, cx = diff("h", "c", cd, cy), diff("x", "c", cd, cy)
    flags["child deaths"] = ch[0] > 0 and ch[1] > 0
    L.append(f"| child deaths per 1,000 child-years (h − v10 > 0, lower > 0) | {ch[0]:+.2f} [{ch[1]:+.2f}, {ch[2]:+.2f}] | "
             f"{cx[0]:+.2f} | {'**RAISED**' if flags['child deaths'] else 'no'} |")
    flags["extinctions"] = ext["h"] - ext["c"] >= 3
    L.append(f"| extinctions (h − v10 ≥ 3) | {ext['h'] - ext['c']:+d} | {ext['x'] - ext['c']:+d} | "
             f"{'**RAISED**' if flags['extinctions'] else 'no'} |")
    flags["ping-pong"] = rev == rev and rev > 0.10
    L.append(f"| ping-pong (reversals > 10% of handings) | {rev:.4f} | | {'**RAISED**' if flags['ping-pong'] else 'no'} |")
    L.append("")

    supported = dh[0] > 0 and dh[1] > 0 and dh[0] > dx[0] and not any(flags.values())
    hpy = ratio(hands["h"], ay["h"])[0]
    L += ["## The frozen decision", "",
          f"- h - v10 {dh[0]:+.4f} [{dh[1]:+.4f}, {dh[2]:+.4f}] (> 0 with lower > 0); sham - v10 {dx[0]:+.4f} "
          f"(h must exceed it); flags raised: {', '.join(k for k, v in flags.items() if v) or 'none'}.",
          f"- Handings per adult-year in h: {hpy:.2f}" + (" (rare: < 0.1; a null would point to choice, not to access "
                                                         "being irrelevant)" if hpy < 0.1 else "") + ".", "",
          f"**{'SUPPORTED' if supported else 'NOT SUPPORTED'}.** (A test in a copy; adoption only by the safe path in "
          "CLAUDE.md, with a confirmatory run.)", ""]
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
