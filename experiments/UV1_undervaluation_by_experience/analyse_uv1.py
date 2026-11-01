"""UV1 analysis, written before any data (questions.md, frozen as `UV1-frozen`).

  python experiments/UV1_undervaluation_by_experience/analyse_uv1.py            # writes results.md
  python experiments/UV1_undervaluation_by_experience/analyse_uv1.py --smoke --dir <folder> [--es2 <folder>]
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_uv1 import AGE_BINS, ARMS, K_BINS, SEEDS  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
ES2DIR = Path(sys.argv[sys.argv.index("--es2") + 1]) if "--es2" in sys.argv else \
    HERE.parent / "ES2_realized_lookahead" / "output"
REPS = 10_000
RNG = np.random.default_rng(20261101)
NAME = {"c": "v11", "r": "r (realized look-ahead)"}
LOW, HIGH = ("0-9", "10-19"), ("80-159", "160+")
PRIME = ("16-29", "30-44")
BAND, HALF = 0.05, 0.5
MIN_N, MIN_WORLDS = 100_000, 24


def load(d):
    runs = {a: {} for a in ARMS}
    for f in sorted(glob.glob(str(d / "*_seed_*.json"))):
        r = json.load(open(f))
        if r["arm"] in runs:
            runs[r["arm"]][r["seed"]] = r
    return runs


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs, es2 = load(OUTDIR), load(ES2DIR)
    zl = HERE / "zero_local.log"
    zero = zl.read_text(encoding="utf-8") if zl.exists() else ""
    want = sorted(SEEDS) if not SMOKE else sorted(set(runs["c"]) | set(runs["r"]))
    present = all(sorted(runs[a]) == want for a in ARMS) and len(want) > 0
    fps = {r["code_hash"] for a in ARMS for r in runs[a].values()} | \
          {r["code_hash_after"] for a in ARMS for r in runs[a].values()}
    es2_fps = {r["code_hash"] for a in ARMS for r in es2[a].values()}
    mism = sum(sum(r["mismatch"].values()) for a in ARMS for r in runs[a].values())

    def totals(r):
        return sum(v[0] for v in r["cal"].values()), sum(v[1] for v in r["cal"].values())
    match, compared, binned = True, 0, True
    for a in ARMS:
        for s, r in runs[a].items():
            n_uv = sum(v[0] for v in r["uv"].values())
            binned &= n_uv == totals(r)[0]
            e = es2[a].get(s)
            if e is None or e["final_tick"] != r["final_tick"]:
                match &= SMOKE                       # a smoke world may have no ES2 twin of the same length
                continue
            compared += 1
            match &= e["world_hash"] == r["world_hash"] and totals(e) == totals(r)
    ok = "All: PASS" in zero and present and len(fps) == 1 and mism == 0 and match and binned
    if not SMOKE:
        ok &= fps == es2_fps and compared == len(ARMS) * len(SEEDS)
    L = ["# UV1 — Does habit under-valuation fade with experience? Results", "",
         "Frozen as `UV1-frozen`. run_uv1.py, analyse_uv1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks (`zero_local.log`): **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)} of {len(want) * len(ARMS)}): "
         f"**{'yes' if present else 'NO'}**",
         f"- One fingerprint, the same as ES2's (`code_es2`): **{'yes' if len(fps) == 1 and fps == es2_fps else 'NO'}**",
         f"- Every habit update replays exactly (mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**",
         f"- The replay matches ES2 (world hash, pooled n and sum of abs(q - G); {compared} worlds compared): "
         f"**{'yes' if match else 'NO'}**",
         f"- Every counted update binned once: **{'yes' if binned else 'NO'}**",
         "", f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    seeds = sorted(set(runs["c"]) & set(runs["r"]))
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def sums(a, k=None, age=None, crisis=None, act=None, cens="0"):
        """Per-seed arrays of n, sum (q - G), sum |q - G| over the uv cells that match."""
        out = np.zeros((3, n))
        for j, s in enumerate(seeds):
            for key, v in runs[a][s]["uv"].items():
                kb, ab, cr, ac, ce = key.split("|")
                if (k is None or kb in k) and (age is None or ab in age) and (crisis is None or cr == crisis) \
                        and (act is None or ac == act) and (cens is None or ce == cens):
                    out[0, j] += v[0]
                    out[1, j] += v[1]
                    out[2, j] += v[2]
        return out

    def bias(x):
        """Pooled signed bias and its 95% world-bootstrap interval."""
        tot = x[0].sum()
        if tot == 0:
            return None, None, None
        b = W @ x[0]
        with np.errstate(invalid="ignore", divide="ignore"):
            bs = (W @ x[1]) / b
        bs = bs[np.isfinite(bs)]
        return x[1].sum() / tot, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))

    def fmt(t):
        return "n/a" if t[0] is None else f"{t[0]:+.4f} [{t[1]:+.4f}, {t[2]:+.4f}]"

    def reading(a):
        lo, hi = sums(a, k=LOW, age=PRIME), sums(a, k=HIGH, age=PRIME)
        bl, bh = bias(lo), bias(hi)
        cover_n, cover_w = int(hi[0].sum()), int((hi[0] > 0).sum())
        if cover_n < MIN_N or cover_w < MIN_WORLDS or bl[0] is None or bh[0] is None:
            verdict = "inconclusive (coverage)"
        elif -BAND <= bh[1] and bh[2] <= BAND and abs(bh[0]) <= HALF * abs(bl[0]):
            verdict = "start lag"
        elif (bl[0] < 0 and bh[2] < -BAND) or (bl[0] > 0 and bh[1] > BAND):
            verdict = "persistent bias"
        else:
            verdict = "mixed"
        return bl, bh, int(lo[0].sum()), cover_n, cover_w, verdict

    L += ["## Primary (frozen): signed bias B = mean(q - G), ages 16-44, G not closed by death", "",
          "| arm | B_low (k 0-19) [95%] | n low | B_high (k 80+) [95%] | n high | worlds with high-k updates | reading |",
          "|---|---|---|---|---|---|---|"]
    rd = {}
    for a in ("r", "c"):
        bl, bh, nl, nh, wh, v = rd[a] = reading(a)
        L.append(f"| {NAME[a]} | {fmt(bl)} | {nl:,} | {fmt(bh)} | {nh:,} | {wh} of {n} | **{v}**"
                 f"{'' if a == 'r' else ' (described)'} |")
    L += ["", f"Rule (for r): start lag if B_high's interval lies inside [-{BAND}, +{BAND}] and abs(B_high) <= "
              f"{HALF} x abs(B_low); persistent bias if the whole interval lies beyond {BAND} on B_low's side; else "
              f"mixed; inconclusive if the high-k cell has under {MIN_N:,} updates or updates in under {MIN_WORLDS} "
              "worlds.", "", f"**Reading (r): {rd['r'][5]}.** v11, described: {rd['c'][5]}.", ""]

    L += ["## Secondary (described, not decisive)", "",
          "### B by k bin (ages 16-44, not death-closed)", "",
          "| k | v11 B [95%] | v11 n | r B [95%] | r n | people (v11 / r, all ages, summed over worlds) |",
          "|---|---|---|---|---|---|"]
    for kb in K_BINS:
        xc, xr = sums("c", k=(kb,), age=PRIME), sums("r", k=(kb,), age=PRIME)
        pc = sum(runs["c"][s]["people_by_k"].get(kb, 0) for s in seeds)
        pr = sum(runs["r"][s]["people_by_k"].get(kb, 0) for s in seeds)
        L.append(f"| {kb} | {fmt(bias(xc))} | {int(xc[0].sum()):,} | {fmt(bias(xr))} | {int(xr[0].sum()):,} | "
                 f"{pc:,} / {pr:,} |")
    L += ["", "### B by age (all k, not death-closed)", "",
          "| age | v11 B [95%] | v11 n | r B [95%] | r n |", "|---|---|---|---|---|"]
    for ab in AGE_BINS:
        xc, xr = sums("c", age=(ab,)), sums("r", age=(ab,))
        L.append(f"| {ab} | {fmt(bias(xc))} | {int(xc[0].sum()):,} | {fmt(bias(xr))} | {int(xr[0].sum()):,} |")
    L += ["", "### r: B by k within each age (not death-closed; B, with n in brackets)", "",
          "| age | " + " | ".join(K_BINS) + " |", "|---|" + "---|" * len(K_BINS)]
    for ab in AGE_BINS:
        cells = []
        for kb in K_BINS:
            x = sums("r", k=(kb,), age=(ab,))
            t = x[0].sum()
            cells.append(f"{x[1].sum() / t:+.3f} ({int(t):,})" if t else "-")
        L.append(f"| {ab} | " + " | ".join(cells) + " |")
    L += ["", "### Crisis slices (weak or under half a week of food, with company; ages 16-44, not death-closed)", "",
          "| action | k | v11 B [95%] | v11 n | r B [95%] | r n |", "|---|---|---|---|---|---|"]
    for act in ("rest", "talk"):
        for name, kk in (("0-19", LOW), ("80+", HIGH)):
            xc, xr = sums("c", k=kk, age=PRIME, crisis="1", act=act), sums("r", k=kk, age=PRIME, crisis="1", act=act)
            L.append(f"| {act} | {name} | {fmt(bias(xc))} | {int(xc[0].sum()):,} | {fmt(bias(xr))} | "
                     f"{int(xr[0].sum()):,} |")
    L += ["", "### Death-closed share (all counted updates)", "", "| arm | death-closed | all | share |",
          "|---|---|---|---|"]
    for a in ("c", "r"):
        d, t = sums(a, cens="1")[0].sum(), sums(a, cens=None)[0].sum()
        L.append(f"| {NAME[a]} | {int(d):,} | {int(t):,} | {d / t:.4f} |" if t else f"| {NAME[a]} | 0 | 0 | - |")
    L.append("")
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
