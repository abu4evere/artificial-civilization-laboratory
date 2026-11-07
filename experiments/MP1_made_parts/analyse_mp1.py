"""MP1 analysis (questions.md, frozen as `MP1-frozen`). Written before data.

  python experiments/MP1_made_parts/analyse_mp1.py [--smoke] [--dir <output>]
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
import run_mp1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261125)
STAGES = "ABCDE"
LABEL = {"A": "no knower holds any of its made parts", "B": "some parts held, never all at once",
         "C": "all made parts held, but cannot make it", "D": "could make it, never made again",
         "E": "made again"}


def pct(x):
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


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
    m = re.search(r"code_v15 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    seeds = sorted(runs) if SMOKE else sorted(R.SEEDS)
    present = SMOKE or sorted(runs) == seeds
    fps = {r["code_hash"] for r in runs.values()} | {r["code_hash_after"] for r in runs.values()}
    chk = Counter()
    for r in runs.values():
        chk.update(r["check"])
    bad = chk["unexplained"] + chk["stage_E_without_event"] + chk["stage_CD_without_all"] + chk["open_at_end"]
    ok = bool(zero_ok and present and fps == {fp_now} and bad == 0)
    L = ["# MP1: where do the made parts of new kinds go? (results)", "",
         "Frozen as `MP1-frozen`. run_mp1.py, analyse_mp1.py (written before data).", "", "## Validity", "",
         f"- Zero checks (All: PASS, `code_v15` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(runs)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_v15`'s: **{'yes' if fps == {fp_now} else 'NO'}**",
         f"- In every world: tracked parts {chk['tracked']:,}; gone unexplained {chk['unexplained']}; stage checks "
         f"failed {chk['stage_E_without_event'] + chk['stage_CD_without_all']}: **{'yes' if bad == 0 else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        finish(L)
        return
    seeds = [s for s in seeds if s in runs]
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def col(fn):
        return np.array([float(fn(runs[s])) for s in seeds])

    def share(num, den):
        nu, de = col(num), col(den)
        with np.errstate(invalid="ignore", divide="ignore"):
            return (nu.sum() / de.sum() if de.sum() else float("nan")), (W @ nu) / (W @ de)

    kinds = col(lambda r: r["stages"].get("kinds", 0)).sum()
    res = {}
    L += [f"## Primary: how far each followed kind gets ({int(kinds):,} new kinds with made parts, years 100-190)", "",
          "| stage | | kinds | share [95%] |", "|---|---|---|---|"]
    for st in STAGES:
        v, b = share(lambda r, st=st: r["stages"].get(f"stage_{st}", 0), lambda r: r["stages"].get("kinds", 0))
        lo, hi = pct(b)
        res[st] = (v, lo, hi)
        cnt = int(col(lambda r, st=st: r["stages"].get(f"stage_{st}", 0)).sum())
        L.append(f"| {st} | {LABEL[st]} | {cnt:,} | {v:.4f} [{lo:.4f}, {hi:.4f}] |")
    order = sorted("ABCD", key=lambda s: -res[s][0])
    top, nxt = order[0], order[1]
    clear = res[top][1] > res[nxt][2]
    L += ["", f"**Reading (frozen): most kinds stop at {top} ({LABEL[top]}), {'clear' if clear else 'shared'}** "
          f"({top} {res[top][0]:.4f} [{res[top][1]:.4f}, {res[top][2]:.4f}] against the next, {nxt}, "
          f"{res[nxt][0]:.4f} [{res[nxt][1]:.4f}, {res[nxt][2]:.4f}]).", "",
          "Rule: the largest share among A-D; 'clear' if its lower bound is above the next largest's upper bound.", ""]

    L += ["## By depth (the longest chain of made parts)", "", "| depth | kinds | A | B | C | D | E |", "|---|---|---|---|---|---|---|"]
    for d in (1, 2, 3):
        cnts = {st: int(col(lambda r, st=st, d=d: r["stages"].get(f"depth{d}_stage_{st}", 0)).sum()) for st in STAGES}
        tot = sum(cnts.values())
        L.append(f"| {d}{'+' if d == 3 else ''} | {tot:,} | " + " | ".join(
            f"{cnts[st] / tot:.3f}" if tot else "-" for st in STAGES) + " |")
    L += ["", "## The inventor alone", "", "| stage | share |", "|---|---|"]
    for st in STAGES:
        v, b = share(lambda r, st=st: r["stages"].get(f"inv_stage_{st}", 0), lambda r: r["stages"].get("kinds", 0))
        lo, hi = pct(b)
        L.append(f"| {st} | {v:.4f} [{lo:.4f}, {hi:.4f}] |")

    fates = Counter()
    sub = Counter()
    lim = Counter()
    for s in seeds:
        fates.update(runs[s]["fates"])
        sub.update(runs[s]["sub"])
        lim.update(runs[s]["limit"])
    tot = sum(fates.values())
    L += ["", f"## Secondary: the first fate of each tracked part ({tot:,} parts)", "", "| fate | parts | share [95%] |",
          "|---|---|---|"]
    for k, v in fates.most_common():
        sv, b = share(lambda r, k=k: r["fates"].get(k, 0), lambda r: sum(r["fates"].values()))
        lo, hi = pct(b)
        L.append(f"| {k} | {v:,} | {sv:.4f} [{lo:.4f}, {hi:.4f}] |")
    nd = fates.get("dropped at the carry limit", 0)
    L += ["", f"After a drop at the carry limit ({nd:,}): " + "; ".join(
        f"{k} {v:,} ({v / nd:.3f})" for k, v in sub.items() if k.startswith("picked") or k.startswith("dropped"))
        if nd else "No drops at the carry limit.",
        f"Left with a body and later taken: {sub.get('taken from the body', 0):,}.", "",
        "## Described", "",
        f"- Knower-weeks at the 3-thing carry limit: {lim['knower_weeks_at_limit']:,} of {lim['knower_weeks']:,} "
        f"({lim['knower_weeks_at_limit'] / lim['knower_weeks']:.4f})." if lim["knower_weeks"] else "- No knower-weeks.",
        (f"- Drops of tracked parts by the carry-limit step: {lim['drops_tracked']:,} ({lim['drops_new_at_once']:,} of "
         f"them the part just made, dropped at once); the dropped part was its holder's "
         f"least valued thing in {lim['drops_least_valued']:,}; valued 0 by its holder in {lim['drops_valued_zero']:,}.")
        if lim["drops_tracked"] else "- No drops of tracked parts by the carry-limit step.",
        f"- New kinds made by a non-inventor within 5 years: {int(col(lambda r: r['stages'].get('made_other', 0)).sum()):,} "
        f"of {int(kinds):,}.", ""]
    finish(L)


def finish(L):
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
