"""PD1 analysis, written before any data (questions.md, frozen as `PD1-frozen`; operational note 1).

  python experiments/PD1_population_drop/analyse_pd1.py            # writes results.md
  python experiments/PD1_population_drop/analyse_pd1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_pd1 import ARMS, BANDS, CAUSES, SEEDS  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261027)


def cnt(r, k):
    return r["counts"].get(k, 0.0)


def cen(r, field, y0=0, y1=200):
    F = r["census_fields"]
    return sum(row[F.index(field)] for row in r["census"] if y0 <= row[0] < y1)


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
    L = ["# PD1 — Why does population fall when made things persist? Results", "",
         "Frozen as `PD1-frozen` (operational note 1). run_pd1.py, analyse_pd1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)} of {len(SEEDS) * len(ARMS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_op1`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Founders + births − deaths = living at the end, in every world (mismatches 0): "
         f"**{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    seeds = sorted(set(runs["c"]) & set(runs["o"]) & set(runs["x"]))
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])

    def vec(arm, fn):
        return np.array([fn(runs[arm][s]) for s in seeds], float)

    comps = [("births", lambda r: cnt(r, "births"))] + [(f"deaths: {c}", (lambda r, c=c: -cnt(r, f"death:{c}")))
                                                         for c in CAUSES]
    ext = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in ARMS}
    L += [f"Paired seeds: {n}. Extinct by year 200: c {ext['c']}, o {ext['o']}, x {ext['x']}.", ""]
    # Q1
    L += ["## Q1 — The exact split of the gap in final population (pooled over paired worlds; extinct worlds count 0)", "",
          "Living at year 200 = founders + births − deaths, so the gap = Δbirths − Σ Δdeaths by cause.", "",
          "| component | o − c [95%] | share of the o − c gap | x − c (sham yardstick) [95%] |", "|---|---|---|---|"]
    gap_o = vec("o", lambda r: cnt(r, "living_end")) - vec("c", lambda r: cnt(r, "living_end"))
    gap_x = vec("x", lambda r: cnt(r, "living_end")) - vec("c", lambda r: cnt(r, "living_end"))
    tot_o, tot_x = gap_o.sum(), gap_x.sum()
    shares = {}
    for name, fn in comps:
        d_o = vec("o", fn) - vec("c", fn)
        d_x = vec("x", fn) - vec("c", fn)
        ro, rx = W @ d_o, W @ d_x
        lo, hi = np.percentile(ro, [2.5, 97.5])
        lx, hx = np.percentile(rx, [2.5, 97.5])
        shares[name] = d_o.sum() / tot_o if tot_o else float("nan")
        L.append(f"| {name} | {d_o.sum():+.0f} [{lo:+.0f}, {hi:+.0f}] | {shares[name]:.2f} | {d_x.sum():+.0f} [{lx:+.0f}, {hx:+.0f}] |")
    lo, hi = np.percentile(W @ gap_o, [2.5, 97.5])
    lx, hx = np.percentile(W @ gap_x, [2.5, 97.5])
    L += [f"| **total: living at year 200** | **{tot_o:+.0f} [{lo:+.0f}, {hi:+.0f}]** | 1.00 | {tot_x:+.0f} [{lx:+.0f}, {hx:+.0f}] |", ""]
    if tot_o:
        sign = np.sign(tot_o)
        largest = max(shares, key=lambda k: shares[k] if np.isfinite(shares[k]) else -9)
        L += [f"Final living: c {vec('c', lambda r: cnt(r, 'living_end')).sum():.0f}, o {vec('o', lambda r: cnt(r, 'living_end')).sum():.0f}, "
              f"x {vec('x', lambda r: cnt(r, 'living_end')).sum():.0f} (summed over {n} worlds).", "",
              f"**The component carrying the largest share of the o − c gap: {largest} (share {shares[largest]:.2f}).**", ""]
    # Q2 rates
    def rate(arm, num_fn, den_fn):
        return vec(arm, num_fn), vec(arm, den_fn)

    def ratefmt(name, num_fn, den_fn, scale=1000.0):
        out = {}
        for a in ARMS:
            nu, de = rate(a, num_fn, den_fn)
            out[a] = scale * nu.sum() / de.sum() if de.sum() else float("nan")
        no, do = rate("o", num_fn, den_fn)
        nc, dc = rate("c", num_fn, den_fn)
        nx, dx = rate("x", num_fn, den_fn)
        with np.errstate(divide="ignore", invalid="ignore"):
            ro = scale * ((W @ no) / (W @ do) - (W @ nc) / (W @ dc))
            rx = scale * ((W @ nx) / (W @ dx) - (W @ nc) / (W @ dc))
        ro, rx = ro[np.isfinite(ro)], rx[np.isfinite(rx)]
        lo, hi = np.percentile(ro, [2.5, 97.5]) if len(ro) else (np.nan, np.nan)
        lx, hx = np.percentile(rx, [2.5, 97.5]) if len(rx) else (np.nan, np.nan)
        return (f"| {name} | {out['c']:.2f} | {out['o']:.2f} | {out['x']:.2f} | {out['o'] - out['c']:+.2f} [{lo:+.2f}, {hi:+.2f}] | "
                f"{out['x'] - out['c']:+.2f} [{lx:+.2f}, {hx:+.2f}] |")
    L += ["## Q2 — Rates (per 1,000 person-years, or woman-years 16-45 for births; years 0-200)", "",
          "| rate | c | o | x | o − c [95%] | x − c [95%] |", "|---|---|---|---|---|---|"]
    py = lambda r: cen(r, "living")
    L.append(ratefmt("births per 1,000 woman-years (16-45)", lambda r: cnt(r, "births"), lambda r: cen(r, "women_16_45")))
    L.append(ratefmt("all deaths", lambda r: cnt(r, "deaths"), py))
    for c in CAUSES:
        L.append(ratefmt(f"deaths: {c}", lambda r, c=c: cnt(r, f"death:{c}"), py))
    for b in BANDS:
        L.append(ratefmt(f"all deaths, {b}s (per 1,000 {b}-years)",
                         lambda r, b=b: sum(cnt(r, f"death:{c}:{b}") for c in CAUSES), lambda r, b=b: cen(r, b)))
    L.append("")
    # Q3 fighting
    ay = lambda r: cen(r, "adult") + cen(r, "elder")
    L += ["## Q3 — Fighting", "", "| measure | c | o | x | o − c [95%] | x − c [95%] |", "|---|---|---|---|---|---|",
          ratefmt("attacks per 1,000 adult-years", lambda r: cnt(r, "attacks"), ay),
          ratefmt("killings per 1,000 adult-years", lambda r: cnt(r, "kills"), ay),
          ratefmt("share of attacks with a fighting tool in hand (×1,000)", lambda r: cnt(r, "attacks_tool"), lambda r: cnt(r, "attacks")),
          ratefmt("kill rate per attack with a tool (×1,000)", lambda r: cnt(r, "kills_tool"), lambda r: cnt(r, "attacks_tool")),
          ratefmt("kill rate per attack without a tool (×1,000)", lambda r: cnt(r, "kills") - cnt(r, "kills_tool"),
                  lambda r: cnt(r, "attacks") - cnt(r, "attacks_tool")),
          ratefmt("attackers who died (per 1,000 attacks)", lambda r: cnt(r, "attacker_died"), lambda r: cnt(r, "attacks")), ""]
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
