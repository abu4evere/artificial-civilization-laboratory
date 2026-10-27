"""MO1 analysis, written before any data (questions.md, frozen as `MO1-frozen`; operational note 1).

  python experiments/MO1_memory_order/analyse_mo1.py            # writes results.md
  python experiments/MO1_memory_order/analyse_mo1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_mo1 import ARMS, SEEDS  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261027)


def load():
    out = {a: {} for a in ARMS}
    for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json"))):
        r = json.load(open(f))
        out[r["arm"]][r["seed"]] = r
    return out


def cnt(r, k):
    return r["counts"].get(k, 0.0)


def census(r, y0, y1, num, den):
    F = r["census_fields"]
    i, j = F.index(num), F.index(den)
    rows = [row for row in r["census"] if y0 <= row[0] < y1]
    return sum(row[i] for row in rows), sum(row[j] for row in rows)


def measures(r):
    """Per-world numerators and denominators."""
    u, a = census(r, 50, 200, "useful_adults", "adults")
    mk, a2 = census(r, 0, 200, "makes", "adults")
    pop, n = census(r, 150, 200, "living", "year")
    last = r["census"][-1] if r["census"] else [0] * 7
    return {
        "M": (cnt(r, "over_survived"), cnt(r, "over")),
        "P1": (cnt(r, "held_52"), cnt(r, "checked")),
        "P1_taught": (cnt(r, "held_52_taught"), cnt(r, "checked_taught")),
        "P1_copied": (cnt(r, "held_52_copied"), cnt(r, "checked_copied")),
        "P2": (u, a),
        "P3": (cnt(r, "bad_52"), cnt(r, "checked")),
        "made_52": (cnt(r, "made_52"), cnt(r, "checked")),
        "displaced_val": (cnt(r, "displaced_val_sum"), cnt(r, "displaced")),
        "displaced_useful": (cnt(r, "displaced_useful"), cnt(r, "displaced")),
        "displaced_made_52": (cnt(r, "displaced_made_52"), cnt(r, "displaced")),
        "relearned": (cnt(r, "relearned"), cnt(r, "learned_taught") + cnt(r, "learned_copied")),
        "makes_per_adult_year": (mk, a2),
        "pop_150_200": (pop, len([row for row in r["census"] if 150 <= row[0] < 200]) or 1),
        "wb_kinds_alive_end": (last[6] if r["census"] and r["census"][-1][0] >= 199 else 0.0, 1.0),
    }


def ratio(ms, seeds, key):
    num = sum(ms[s][key][0] for s in seeds)
    den = sum(ms[s][key][1] for s in seeds)
    return num / den if den else float("nan")


def paired(msa, msb, seeds, key):
    """Pooled ratio a - b over paired seeds, with a paired world bootstrap."""
    seeds = list(seeds)
    na = np.array([msa[s][key][0] for s in seeds], float)
    da = np.array([msa[s][key][1] for s in seeds], float)
    nb = np.array([msb[s][key][0] for s in seeds], float)
    db = np.array([msb[s][key][1] for s in seeds], float)
    W = np.stack([np.bincount(row, minlength=len(seeds)) for row in RNG.integers(0, len(seeds), size=(REPS, len(seeds)))])
    with np.errstate(divide="ignore", invalid="ignore"):
        d = (W @ na) / (W @ da) - (W @ nb) / (W @ db)
    d = d[np.isfinite(d)]
    point = na.sum() / da.sum() - nb.sum() / db.sum()
    lo, hi = np.percentile(d, [2.5, 97.5]) if len(d) else (float("nan"), float("nan"))
    return point, lo, hi


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = load()
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    present = all(sorted(runs[a]) == sorted(SEEDS) for a in ARMS)
    fps = {r["code_hash"] for a in ARMS for r in runs[a].values()} | \
          {r["code_hash_after"] for a in ARMS for r in runs[a].values()}
    mism = sum(sum(r["mismatch"].values()) for a in ARMS for r in runs[a].values())
    ok = "All: PASS" in zero and present and len(fps) == 1 and mism == 0
    L = ["# MO1 — The memory order. Results", "",
         "Frozen as `MO1-frozen` (operational note 1). run_mo1.py, analyse_mo1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)} of {len(SEEDS) * len(ARMS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_mo1`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Every predicted deletion matches the code's (mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    seeds = sorted(set(runs["c"]) & set(runs["o"]) & set(runs["s"]))
    ms = {a: {s: measures(runs[a][s]) for s in seeds} for a in ARMS}
    ext = {a: sum(runs[a][s]["extinct"] for s in seeds) for a in ARMS}
    L += [f"Paired seeds: {len(seeds)}. Worlds extinct by year 200: c {ext['c']}, o {ext['o']}, s {ext['s']}.", ""]
    rows = [("M", "M: new recipe survives a learning-caused overflow"),
            ("P1", "P1: taken recipes still held 52 weeks later"),
            ("P1_taught", "  P1, taught"), ("P1_copied", "  P1, copied by watching"),
            ("P2", "P2: useful recipes held per adult (years 50-200)"),
            ("P3", "P3: taken recipes found bad within 52 weeks"),
            ("made_52", "taken recipes made within 52 weeks"),
            ("displaced_val", "value of the recipe deleted instead (when the new one survives)"),
            ("displaced_useful", "deleted instead: a useful kind"),
            ("displaced_made_52", "deleted instead: made by its holder in the past 52 weeks"),
            ("relearned", "evicted recipes relearned, per learned recipe"),
            ("makes_per_adult_year", "making events per adult-year"),
            ("pop_150_200", "mean living population, years 150-200"),
            ("wb_kinds_alive_end", "world-born kinds held by anyone alive at year 200 (mean per world)")]
    L += ["## The measures (pooled over paired worlds; 95% paired world bootstrap, 10,000 replicates)", "",
          "| measure | c | o | s | o − c [95%] | s − c [95%] (sham yardstick) |", "|---|---|---|---|---|---|"]
    res = {}
    for key, name in rows:
        vc, vo, vs = (ratio(ms[a], seeds, key) for a in ("c", "o", "s"))
        d = paired(ms["o"], ms["c"], seeds, key)
        ds = paired(ms["s"], ms["c"], seeds, key)
        res[key] = (vc, vo, vs, d)
        L.append(f"| {name} | {vc:.4g} | {vo:.4g} | {vs:.4g} | {d[0]:+.4g} [{d[1]:+.4g}, {d[2]:+.4g}] | "
                 f"{ds[0]:+.4g} [{ds[1]:+.4g}, {ds[2]:+.4g}] |")
    L.append("")
    vc, vo, _, _ = res["M"]
    m_ok = vo >= 0.90 and vc <= 0.40
    p1 = res["P1"][3]
    p1_ok = p1[1] > 0
    p2c = res["P2"][0]
    p2 = res["P2"][3]
    p2_ok = p2[1] > -0.05 * p2c
    p3 = res["P3"][3]
    p3_ok = p3[2] < 0.02
    L += ["## The frozen decision rule", "",
          f"- **M (manipulation):** o {vo:.3f} ≥ 0.90 and c {vc:.3f} ≤ 0.40: **{'passes' if m_ok else 'FAILS'}**",
          f"- **P1 (retention):** o − c {p1[0]:+.4f} [{p1[1]:+.4f}, {p1[2]:+.4f}], lower bound above 0: "
          f"**{'supports' if p1_ok else 'does not support'}**",
          f"- **P2 (knowledge kept):** o − c {p2[0]:+.4f} [{p2[1]:+.4f}, {p2[2]:+.4f}], lower bound above "
          f"−5% of c ({-0.05 * p2c:+.4f}): **{'no harm' if p2_ok else 'HARM'}**",
          f"- **P3 (reliability):** o − c {p3[0]:+.4f} [{p3[1]:+.4f}, {p3[2]:+.4f}], upper bound below +0.02: "
          f"**{'no harm' if p3_ok else 'HARM'}**", "",
          f"**{'The change is supported' if (m_ok and p1_ok and p2_ok and p3_ok) else 'The change is not supported'} "
          f"by the frozen rule.** Adoption as nature v8 is left to the creator.", ""]
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
