"""UV2 analysis, written before any data (questions.md, frozen as `UV2-frozen`).

  python experiments/UV2_propagation/analyse_uv2.py            # writes results.md
  python experiments/UV2_propagation/analyse_uv2.py --smoke --dir <folder> --es2 <folder> --uv1 <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_uv2 import DN_BINS, SEEDS, U_BINS  # noqa: E402
from run_uv1 import AGE_BINS, K_BINS  # noqa: E402  (run_uv2 puts UV1's folder on the path)


def arg(name, default):
    return Path(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


SMOKE = "--smoke" in sys.argv
OUTDIR = arg("--dir", HERE / "output")
ES2DIR = arg("--es2", HERE.parent / "ES2_realized_lookahead" / "output")
UV1DIR = arg("--uv1", HERE.parent / "UV1_undervaluation_by_experience" / "output")
REPS = 10_000
RNG = np.random.default_rng(20261101)
HIGH, PRIME = ("80-159", "160+"), ("16-29", "30-44")
LOW_DN = ("0-0.05", "0.05-0.1")
BAND, HALF = 0.05, 0.5
MIN_N, MIN_WORLDS = 100_000, 24
QUARTERS = (("0", "years 100-124"), ("1", "125-149"), ("2", "150-174"), ("3", "175-199"))


def load(d, arm="r"):
    runs = {}
    for f in sorted(glob.glob(str(d / f"{arm}_seed_*.json"))):
        r = json.load(open(f))
        runs[r["seed"]] = r
    return runs


def totals(r):
    return sum(v[0] for v in r["cal"].values()), sum(v[1] for v in r["cal"].values())


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs, es2, uv1 = load(OUTDIR), load(ES2DIR), load(UV1DIR)
    zl = HERE / "zero_local.log"
    zero = zl.read_text(encoding="utf-8") if zl.exists() else ""
    want = sorted(SEEDS) if not SMOKE else sorted(runs)
    present = sorted(runs) == want and len(want) > 0
    fps = {r["code_hash"] for r in runs.values()} | {r["code_hash_after"] for r in runs.values()}
    es2_fps = {r["code_hash"] for r in es2.values()}
    mism = sum(sum(r["mismatch"].values()) for r in runs.values())
    dn_bad = sum(r["dn_bad"] for r in runs.values())
    match, compared, binned = True, 0, True
    for s, r in runs.items():
        binned &= sum(v[0] for v in r["uv2"].values()) == totals(r)[0]
        e = es2.get(s)
        if e is None or e["final_tick"] != r["final_tick"]:
            match &= SMOKE
            continue
        compared += 1
        match &= e["world_hash"] == r["world_hash"] and totals(e) == totals(r)
    seeds = sorted(runs)
    n = len(seeds)

    def sums(src, field, pred):
        out = np.zeros((3, n))
        for j, s in enumerate(seeds):
            for key, v in src[s][field].items():
                if pred(key.split("|")):
                    out[0, j] += v[0]
                    out[1, j] += v[1]
                    out[2, j] += v[2]
        return out

    def prime_high(p):                    # uv2 key: kbin|agebin|dnbin|ubin|quarter|censored
        return p[0] in HIGH and p[1] in PRIME and p[5] == "0"
    all_dn = sums(runs, "uv2", prime_high)
    same_uv1 = None
    if all(s in uv1 for s in seeds):      # UV1's key: kbin|agebin|crisis|action|censored
        u = sums(uv1, "uv", lambda p: p[0] in HIGH and p[1] in PRIME and p[4] == "0")
        same_uv1 = bool(u[0].sum() > 0 and round(u[1].sum() / u[0].sum(), 4) == round(all_dn[1].sum() / all_dn[0].sum(), 4))
    ok = "All: PASS" in zero and present and len(fps) == 1 and mism == 0 and match and binned and dn_bad == 0 \
        and same_uv1 is not False
    if not SMOKE:
        ok &= fps == es2_fps and compared == len(SEEDS) and same_uv1 is True
    L = ["# UV2 — Does the habit floor come from unpractised choices further ahead? Results", "",
         "Frozen as `UV2-frozen`. run_uv2.py, analyse_uv2.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks (`zero_local.log`): **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({len(runs)} of {len(want)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, the same as ES2's (`code_es2`): **{'yes' if len(fps) == 1 and fps == es2_fps else 'NO'}**",
         f"- Every habit update replays exactly, and every completed update had its U (mismatches 0): "
         f"**{'yes' if mism == 0 else f'NO ({mism})'}**",
         f"- The replay matches ES2's r arm (world hash, pooled n and sum of abs(q - G); {compared} worlds compared): "
         f"**{'yes' if match else 'NO'}**",
         f"- Every counted update binned once: **{'yes' if binned else 'NO'}**; Dn outside [0, 1]: **{dn_bad}**",
         f"- The primary pooled over all Dn equals UV1's r B_high to 4 decimals: "
         f"**{'yes' if same_uv1 else ('not compared' if same_uv1 is None else 'NO')}**",
         "", f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def bias(x):
        tot = x[0].sum()
        if tot == 0:
            return None, None, None
        with np.errstate(invalid="ignore", divide="ignore"):
            bs = (W @ x[1]) / (W @ x[0])
        bs = bs[np.isfinite(bs)]
        return x[1].sum() / tot, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))

    def fmt(t):
        return "n/a" if t[0] is None else f"{t[0]:+.4f} [{t[1]:+.4f}, {t[2]:+.4f}]"

    low = sums(runs, "uv2", lambda p: prime_high(p) and p[2] in LOW_DN)
    bl, ba = bias(low), bias(all_dn)
    cover_n, cover_w = int(low[0].sum()), int((low[0] > 0).sum())
    if cover_n < MIN_N or cover_w < MIN_WORLDS or bl[0] is None:
        verdict = "inconclusive (coverage)"
    elif -BAND <= bl[1] and bl[2] <= BAND and abs(bl[0]) <= HALF * abs(ba[0]):
        verdict = "propagation"
    elif bl[2] < -BAND:
        verdict = "not propagation"
    else:
        verdict = "mixed"
    L += ["## Primary (frozen): signed bias B = mean(q - G), k >= 80, ages 16-44, G not closed by death", "",
          "| cell | B [95%] | n | worlds |", "|---|---|---|---|",
          f"| **Dn < 0.1** (discounted future almost all well-practised choices) | {fmt(bl)} | {cover_n:,} | "
          f"{cover_w} of {n} |",
          f"| all Dn | {fmt(ba)} | {int(all_dn[0].sum()):,} | {int((all_dn[0] > 0).sum())} of {n} |", "",
          f"Rule: propagation if the Dn < 0.1 interval lies inside [-{BAND}, +{BAND}] and abs(B) <= {HALF} x abs(B over "
          f"all Dn); not propagation if its whole interval lies below -{BAND}; else mixed; inconclusive if the cell has "
          f"under {MIN_N:,} updates or updates in under {MIN_WORLDS} worlds.", "", f"**Reading: {verdict}.**", ""]

    L += ["## Secondary (described, not decisive)", "",
          "### Dose-response: B by Dn (k >= 80, ages 16-44, not death-closed)", "",
          "| Dn | B [95%] | n | worlds |", "|---|---|---|---|"]
    for db in DN_BINS:
        x = sums(runs, "uv2", lambda p, db=db: prime_high(p) and p[2] == db)
        L.append(f"| {db} | {fmt(bias(x))} | {int(x[0].sum()):,} | {int((x[0] > 0).sum())} |")
    L += ["", "### B by Dn within each k bin (ages 16-44, not death-closed; B, with n in brackets)", "",
          "| k | " + " | ".join(DN_BINS) + " |", "|---|" + "---|" * len(DN_BINS)]
    for kb in K_BINS:
        cells = []
        for db in DN_BINS:
            x = sums(runs, "uv2", lambda p, kb=kb, db=db: p[0] == kb and p[1] in PRIME and p[5] == "0" and p[2] == db)
            t = x[0].sum()
            cells.append(f"{x[1].sum() / t:+.3f} ({int(t):,})" if t else "-")
        L.append(f"| {kb} | " + " | ".join(cells) + " |")
    L += ["", "### One-step U: B by the next decision's unpractised mass (k >= 80, ages 16-44, not death-closed)", "",
          "| U | B [95%] | n |", "|---|---|---|"]
    for ub in U_BINS:
        x = sums(runs, "uv2", lambda p, ub=ub: prime_high(p) and p[3] == ub)
        L.append(f"| {ub} | {fmt(bias(x))} | {int(x[0].sum()):,} |")
    L += ["", "### Year quarters (k >= 80, ages 16-44, not death-closed)", "",
          "| quarter | B [95%] | n | share with Dn < 0.1 |", "|---|---|---|---|"]
    for qk, name in QUARTERS:
        x = sums(runs, "uv2", lambda p, qk=qk: prime_high(p) and p[4] == qk)
        xl = sums(runs, "uv2", lambda p, qk=qk: prime_high(p) and p[4] == qk and p[2] in LOW_DN)
        t = x[0].sum()
        L.append(f"| {name} | {fmt(bias(x))} | {int(t):,} | {xl[0].sum() / t:.3f} |" if t else f"| {name} | n/a | 0 | - |")
    L += ["", "### B by Dn for each age (all k, not death-closed; B, with n in brackets)", "",
          "| age | " + " | ".join(DN_BINS) + " |", "|---|" + "---|" * len(DN_BINS)]
    for ab in AGE_BINS:
        cells = []
        for db in DN_BINS:
            x = sums(runs, "uv2", lambda p, ab=ab, db=db: p[1] == ab and p[5] == "0" and p[2] == db)
            t = x[0].sum()
            cells.append(f"{x[1].sum() / t:+.3f} ({int(t):,})" if t else "-")
        L.append(f"| {ab} | " + " | ".join(cells) + " |")
    L.append("")
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
