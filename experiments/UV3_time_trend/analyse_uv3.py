"""UV3 analysis, written before any data (questions.md, frozen as `UV3-frozen`).

  python experiments/UV3_time_trend/analyse_uv3.py            # writes results.md
  python experiments/UV3_time_trend/analyse_uv3.py --smoke --dir <folder> --es2 <folder> --uv2 <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_uv3 import HIGH, PRIME, SEEDS  # noqa: E402


def arg(name, default):
    return Path(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


SMOKE = "--smoke" in sys.argv
OUTDIR = arg("--dir", HERE / "output")
ES2DIR = arg("--es2", HERE.parent / "ES2_realized_lookahead" / "output")
UV2DIR = arg("--uv2", HERE.parent / "UV2_propagation" / "output")
REPS, BATCH = 10_000, 500
RNG = np.random.default_rng(20261101)
BAND, MIN_CELL, MIN_COVER = 0.05, 100, 0.80
Q1, Q4 = "0", "3"
QNAME = {"0": "years 100-124", "1": "125-149", "2": "150-174", "3": "175-199"}


def load(d):
    runs = {}
    for f in sorted(glob.glob(str(d / "r_seed_*.json"))):
        r = json.load(open(f))
        runs[r["seed"]] = r
    return runs


def totals(r):
    return sum(v[0] for v in r["cal"].values()), sum(v[1] for v in r["cal"].values())


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs, es2, uv2 = load(OUTDIR), load(ES2DIR), load(UV2DIR)
    zl = HERE / "zero_local.log"
    zero = zl.read_text(encoding="utf-8") if zl.exists() else ""
    want = sorted(SEEDS) if not SMOKE else sorted(runs)
    present = sorted(runs) == want and len(want) > 0
    fps = {r["code_hash"] for r in runs.values()} | {r["code_hash_after"] for r in runs.values()}
    es2_fps = {r["code_hash"] for r in es2.values()}
    mism = sum(sum(r["mismatch"].values()) for r in runs.values())
    match, compared, tabled = True, 0, True
    for s, r in runs.items():
        tabled &= sum(v[0] for v in r["dec"].values()) == totals(r)[0]
        e = es2.get(s)
        if e is None or e["final_tick"] != r["final_tick"]:
            match &= SMOKE
            continue
        compared += 1
        match &= e["world_hash"] == r["world_hash"] and totals(e) == totals(r)
    seeds = sorted(runs)
    n = len(seeds)

    # The primary population: k >= 80, ages 16-44, not death-closed. Per world: cell -> quarter -> [n, sum q, sum G].
    cells = defaultdict(lambda: np.zeros((4, 3, n)))
    for j, s in enumerate(seeds):
        for key, v in runs[s]["prim"].items():
            qt, ab, ctx, act, ce = key.split("|")
            if ce == "0" and qt in QNAME:
                cells[(ab, ctx, act)][int(qt), :, j] += v

    def quarter_b(qt):
        nn = sum(c[int(qt), 0].sum() for c in cells.values())
        return (sum(c[int(qt), 1].sum() for c in cells.values()) - sum(c[int(qt), 2].sum() for c in cells.values())) / nn \
            if nn else None
    same_uv2 = None
    if all(s in uv2 for s in seeds):
        same_uv2 = True
        for qt in QNAME:
            nn = sg = 0.0
            for s in seeds:
                for key, v in uv2[s]["uv2"].items():
                    kb, ab, _, _, q2, ce = key.split("|")
                    if kb in HIGH and ab in PRIME and ce == "0" and q2 == qt:
                        nn += v[0]
                        sg += v[1]
            b3 = quarter_b(qt)
            if nn == 0 and b3 is None and SMOKE:      # a short smoke world has no updates in the later quarters
                continue
            same_uv2 &= bool(nn > 0 and b3 is not None and round(sg / nn, 4) == round(b3, 4))
    ok = "All: PASS" in zero and present and len(fps) == 1 and mism == 0 and match and tabled and same_uv2 is not False
    if not SMOKE:
        ok = bool(ok and fps == es2_fps and compared == len(SEEDS) and same_uv2 is True)
    L = ["# UV3 — Is the shrinking habit gap rising returns or climbing values? Results", "",
         "Frozen as `UV3-frozen`. run_uv3.py, analyse_uv3.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks (`zero_local.log`): **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({len(runs)} of {len(want)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, the same as ES2's (`code_es2`): **{'yes' if len(fps) == 1 and fps == es2_fps else 'NO'}**",
         f"- Every habit update replays exactly (mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**",
         f"- The replay matches ES2's r arm (world hash, pooled n and sum of abs(q - G); {compared} worlds compared): "
         f"**{'yes' if match else 'NO'}**",
         f"- Every counted update in the decade table once: **{'yes' if tabled else 'NO'}**",
         f"- The primary population's B by quarter equals UV2's to 4 decimals: "
         f"**{'yes' if same_uv2 else ('not compared' if same_uv2 is None else 'NO')}**",
         "", f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return

    keys = sorted(cells)
    A = np.stack([cells[k] for k in keys])                     # cells x quarter x (n, q, G) x worlds
    pooled = A.sum(axis=3)                                     # cells x quarter x 3
    common = (pooled[:, 0, 0] >= MIN_CELL) & (pooled[:, 3, 0] >= MIN_CELL)
    cover = {qt: float(pooled[common, int(qt), 0].sum() / pooled[:, int(qt), 0].sum()) if pooled[:, int(qt), 0].sum()
             else 0.0 for qt in (Q1, Q4)}
    C = A[common]
    w = C[:, 0, 0].sum(axis=1) + C[:, 3, 0].sum(axis=1)
    w = w / w.sum() if w.sum() else w

    def delta(field, nq1, fq1, nq4, fq4):
        """Standardized change (Q4 - Q1) of a cell mean, with fixed weights; cells empty in either quarter are dropped
        and the remaining weights renormalized."""
        with np.errstate(invalid="ignore", divide="ignore"):
            d = fq4 / nq4 - fq1 / nq1
        m = (nq1 > 0) & (nq4 > 0)
        ww = np.where(m, w, 0.0)
        return (np.where(m, d, 0.0) * ww).sum(axis=-1) / ww.sum(axis=-1)

    def point_and_ci(field):
        j = 1 if field == "q" else 2
        pt = float(delta(field, C[:, 0, 0].sum(1), C[:, 0, j].sum(1), C[:, 3, 0].sum(1), C[:, 3, j].sum(1)))
        reps = []
        for start in range(0, REPS, BATCH):
            Wb = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(BATCH, n))]).astype(float)
            reps.append(delta(field, Wb @ C[:, 0, 0].T, Wb @ C[:, 0, j].T, Wb @ C[:, 3, 0].T, Wb @ C[:, 3, j].T))
        reps = np.concatenate(reps)
        reps = reps[np.isfinite(reps)]
        return pt, float(np.percentile(reps, 2.5)), float(np.percentile(reps, 97.5))

    dG = point_and_ci("G") if common.any() else (None, None, None)
    dq = point_and_ci("q") if common.any() else (None, None, None)
    if min(cover.values()) < MIN_COVER or dG[0] is None:
        verdict = "inconclusive (coverage)"
    elif dG[1] > BAND:
        verdict = "returns rising"
    elif -BAND <= dG[1] and dG[2] <= BAND:
        verdict = "returns stable"
    elif dG[2] < -BAND:
        verdict = "returns falling"
    else:
        verdict = "mixed"

    def fmt(t):
        return "n/a" if t[0] is None else f"{t[0]:+.4f} [{t[1]:+.4f}, {t[2]:+.4f}]"
    L += ["## Primary (frozen): the standardized change in realized return, years 175-199 minus 100-124", "",
          "Population: k >= 80, ages 16-44, G not closed by death. Cells: age bin x situation x action, common support "
          f"(at least {MIN_CELL} updates in both quarters), fixed count weights.", "",
          "| quantity | value [95%] |", "|---|---|",
          f"| **Delta G** | **{fmt(dG)}** |",
          f"| Delta q (secondary) | {fmt(dq)} |",
          f"| Delta B = Delta q - Delta G (standardized) | {dq[0] - dG[0]:+.4f} |" if dG[0] is not None else "| Delta B | n/a |",
          f"| common-support cells | {int(common.sum())} of {len(keys)} |",
          f"| coverage: years 100-124 / 175-199 | {cover[Q1]:.3f} / {cover[Q4]:.3f} |", "",
          f"Rule: inconclusive if coverage < {MIN_COVER} in either quarter; returns rising if Delta G's interval lies "
          f"wholly above +{BAND}; stable if inside [-{BAND}, +{BAND}]; falling if wholly below -{BAND}; else mixed.", "",
          f"**Reading: {verdict}.**", ""]

    L += ["## Secondary (described, not decisive)", "",
          "### The primary population by quarter (not standardized)", "",
          "| quarter | n | mean q | mean G | B |", "|---|---|---|---|---|"]
    for qt in QNAME:
        nn = sum(c[int(qt), 0].sum() for c in cells.values())
        sq = sum(c[int(qt), 1].sum() for c in cells.values())
        sgv = sum(c[int(qt), 2].sum() for c in cells.values())
        L.append(f"| {QNAME[qt]} | {int(nn):,} | {sq / nn:+.4f} | {sgv / nn:+.4f} | {(sq - sgv) / nn:+.4f} |" if nn
                 else f"| {QNAME[qt]} | 0 | - | - | - |")
    dec = defaultdict(lambda: np.zeros(3))
    for s in seeds:
        for key, v in runs[s]["dec"].items():
            d, kb, ab, bd, ce = key.split("|")
            if kb in HIGH and ab in PRIME and ce == "0":
                dec[(int(d), int(bd))] += v
    L += ["", "### Per decade (k >= 80, ages 16-44, not death-closed)", "",
          "| decade | n | mean q | mean G | B |", "|---|---|---|---|---|"]
    for d in sorted({k[0] for k in dec}):
        t = sum((v for k, v in dec.items() if k[0] == d), np.zeros(3))
        L.append(f"| {d * 10}s | {int(t[0]):,} | {t[1] / t[0]:+.4f} | {t[2] / t[0]:+.4f} | {(t[1] - t[2]) / t[0]:+.4f} |")
    L += ["", "### B by birth decade within each decade (same population; B, with n in brackets)", ""]
    bds = sorted({k[1] for k in dec})
    L += ["| decade | " + " | ".join(f"born {b * 10}s" for b in bds) + " |", "|---|" + "---|" * len(bds)]
    for d in sorted({k[0] for k in dec}):
        row = []
        for b in bds:
            v = dec.get((d, b))
            row.append(f"{(v[1] - v[2]) / v[0]:+.3f} ({int(v[0]):,})" if v is not None and v[0] else "-")
        L.append(f"| {d * 10}s | " + " | ".join(row) + " |")
    nb = defaultdict(lambda: np.zeros(2))
    for s in seeds:
        for bd, v in runs[s]["newborn"].items():
            nb[int(bd)] += v
    L += ["", "### Newborns' mean starting habit value by birth decade (all years)", "",
          "| born | births | mean starting value |", "|---|---|---|"]
    for bd in sorted(nb):
        L.append(f"| {bd * 10}s | {int(nb[bd][0]):,} | {nb[bd][1] / nb[bd][0]:+.4f} |")
    L += ["", "### Tools' share of adults' foraged food by quarter", "", "| quarter | share |", "|---|---|"]
    for qt in QNAME:
        fw = sum(runs[s]["tools"].get(qt, [0.0, 0.0])[0] for s in seeds)
        fo = sum(runs[s]["tools"].get(qt, [0.0, 0.0])[1] for s in seeds)
        L.append(f"| {QNAME[qt]} | {(fw - fo) / fw:.4f} |" if fw else f"| {QNAME[qt]} | - |")
    L.append("")
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
