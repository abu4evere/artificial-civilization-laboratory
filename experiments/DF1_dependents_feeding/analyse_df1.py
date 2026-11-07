"""DF1 analysis (questions.md, frozen as `DF1-frozen`). Written before data.

  python experiments/DF1_dependents_feeding/analyse_df1.py [--smoke] [--dir <output>]
"""
from __future__ import annotations

import glob
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_df1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261128)
BANDS = ("16-29", "30-49", "50+")


def pct(x):
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


def finish(L):
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {}
    for f in sorted(glob.glob(str(OUTDIR / "c_seed_*.json"))):
        r = json.load(open(f))
        runs[r["seed"]] = r
    zero = (HERE / "zero_local.log").read_text(encoding="utf-8", errors="replace") if (HERE / "zero_local.log").exists() \
        else ""
    R.base.setup(R.CODE)
    fp_now = R.base.fingerprint(R.CODE)
    m = re.search(r"code_v16 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    seeds = sorted(runs) if SMOKE else sorted(R.SEEDS)
    present = SMOKE or sorted(runs) == seeds
    fps = {r["code_hash"] for r in runs.values()} | {r["code_hash_after"] for r in runs.values()}
    ok = bool(zero_ok and present and fps == {fp_now})
    L = ["# DF1: who feeds the children, and what does it cost them? (results)", "",
         "Frozen as `DF1-frozen`. run_df1.py, analyse_df1.py (written before data).", "", "## Validity", "",
         f"- Zero checks (All: PASS, `code_v16` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(runs)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_v16`'s: **{'yes' if fps == {fp_now} else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        finish(L)
        return
    seeds = [s for s in seeds if s in runs]
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def col(sex, key, band=None):
        out = []
        for s in seeds:
            t = 0.0
            for k, v in runs[s]["sums"].items():
                sx, b = k.split("|")
                if sx == sex and (band is None or b == band):
                    t += v.get(key, 0)
            out.append(t)
        return np.array(out)

    def rate(sex, num, den, per, band=None):
        nu, de = col(sex, num, band), col(sex, den, band)
        with np.errstate(invalid="ignore", divide="ignore"):
            return (nu.sum() / de.sum() * per if de.sum() else float("nan")), (W @ nu) / (W @ de) * per

    fw, fb = rate("F", "fcs", "weeks", 1000)
    mw, mb = rate("M", "fcs", "weeks", 1000)
    d, db = fw - mw, fb - mb
    lo, hi = pct(db)
    fcs_f, fcs_m = col("F", "fcs").sum(), col("M", "fcs").sum()
    share_f = fcs_f / (fcs_f + fcs_m) if fcs_f + fcs_m else float("nan")
    sb = (W @ col("F", "fcs")) / ((W @ col("F", "fcs")) + (W @ col("M", "fcs")))
    slo, shi = pct(sb)
    drives = d > 0 and lo > 0 and share_f >= 0.75
    reading = "feeding drives the gap" if drives else ("feeding does not explain it" if (lo <= 0 or mw > fw)
                                                      else "feeding contributes, below the frozen bar")
    L += ["## Primary: feeding-caused short weeks per 1,000 grown person-weeks", "",
          "A feeding-caused short week: the person held at least their own need before feeding dependents, and ended the "
          "week short (deficit > 0.05).", "",
          f"- Women: **{fw:.3f}** [{pct(fb)[0]:.3f}, {pct(fb)[1]:.3f}] ({int(fcs_f):,} of {int(col('F', 'weeks').sum()):,} "
          f"person-weeks)",
          f"- Men: **{mw:.3f}** [{pct(mb)[0]:.3f}, {pct(mb)[1]:.3f}] ({int(fcs_m):,} of {int(col('M', 'weeks').sum()):,})",
          f"- Women − men: **{d:+.3f}** [{lo:+.3f}, {hi:+.3f}]",
          f"- Women's share of all feeding-caused short weeks: **{share_f:.4f}** [{slo:.4f}, {shi:.4f}]", "",
          f"**Reading (frozen): {reading}.**", "",
          "Rule: 'feeding drives the gap' if women − men is above 0 with its lower bound above 0 and women's share is at "
          "least 0.75; 'feeding does not explain it' if the interval includes 0 or men's rate is higher.", ""]
    L += ["## By age band", "", "| band | sex | person-weeks | with dependents | dependents per week | fed out per week | "
          "short weeks per 1,000 | feeding-caused per 1,000 |", "|---|---|---|---|---|---|---|---|"]
    for b in BANDS:
        for sx in ("F", "M"):
            wk = col(sx, "weeks", b).sum()
            if not wk:
                continue
            L.append(f"| {b} | {'women' if sx == 'F' else 'men'} | {int(wk):,} | {col(sx, 'weeks_with_deps', b).sum() / wk:.3f} | "
                     f"{col(sx, 'deps', b).sum() / wk:.3f} | {col(sx, 'fed_out', b).sum() / wk:.3f} | "
                     f"{col(sx, 'short', b).sum() / wk * 1000:.2f} | {col(sx, 'fcs', b).sum() / wk * 1000:.2f} |")
    carers, gifts, en = Counter(), Counter(), Counter()
    for s in seeds:
        carers.update(runs[s]["carers"])
        gifts.update(runs[s]["gifts"])
        en.update(runs[s]["energy"])
    tc = sum(carers.values())
    L += ["", "## Who feeds", "",
          f"- Dependent-weeks by caregiver (counted body phases): " + ", ".join(
              f"{k} {v:,} ({v / tc:.3f})" for k, v in carers.most_common()) if tc else "- No dependents fed.",
          f"- Food gifts to one's own children under 12: fathers {gifts.get('M|n', 0):,} gifts ({gifts.get('M|amount', 0):,.1f} "
          f"food); mothers {gifts.get('F|n', 0):,} gifts ({gifts.get('F|amount', 0):,.1f} food).", "",
          "## The energy link (the next decision with energy below 25: in v16 forage is then offered nowhere)", "",
          "| sex | after a feeding-caused short week | after another short week | after a week not short |",
          "|---|---|---|---|"]
    for sx in ("F", "M"):
        cells = []
        for k in ("fcs", "short", "ok"):
            nn = en.get(f"{sx}|{k}|n", 0)
            cells.append(f"{en.get(f'{sx}|{k}|low', 0) / nn:.4f} ({nn:,})" if nn else "-")
        L.append(f"| {'women' if sx == 'F' else 'men'} | " + " | ".join(cells) + " |")
    L.append("")
    finish(L)


if __name__ == "__main__":
    main()
