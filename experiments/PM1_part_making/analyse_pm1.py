"""PM1 analysis (questions.md, frozen as `PM1-frozen`). Written before data.

  python experiments/PM1_part_making/analyse_pm1.py [--smoke] [--dir <output>]
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
import run_pm1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261127)
STAGES = ("P0a", "P0b", "P1", "P2", "P3", "P4", "P5", "P6", "P7")
LABEL = {"P0a": "the part's recipe known by no one living", "P0b": "the part's recipe unknown to the knower (others know it)",
         "P1": "known, never the inputs in hand", "P2": "inputs in hand, never valued enough",
         "P3": "eligible, never the make option offered", "P4": "offered, never chosen", "P5": "chosen, never made",
         "P6": "made, never all parts held at once", "P7": "all parts held at once"}


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
    chk = Counter()
    for r in runs.values():
        chk.update(r["check"])
    bad = chk["make_mismatch"] + chk["made_without_event"] + chk["p7_without_all"]
    ok = bool(zero_ok and present and fps == {fp_now} and bad == 0)
    L = ["# PM1: why are the parts of new kinds never made again? (results)", "",
         "Frozen as `PM1-frozen`. run_pm1.py, analyse_pm1.py (written before data).", "", "## Validity", "",
         f"- Zero checks (All: PASS, `code_v16` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(runs)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_v16`'s: **{'yes' if fps == {fp_now} else 'NO'}**",
         f"- In every world: decisions looked at {chk['looks'] + chk['looks_no_block']:,}; make option predicted wrongly "
         f"{chk['make_mismatch']}; event checks failed {chk['made_without_event'] + chk['p7_without_all']}: "
         f"**{'yes' if bad == 0 else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        finish(L)
        return
    seeds = [s for s in seeds if s in runs]
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def col(key):
        return np.array([float(runs[s]["stages"].get(key, 0)) for s in seeds])

    kinds = col("kinds")
    res = {}
    L += [f"## Primary: the furthest part-making stage ({int(kinds.sum()):,} new kinds with made parts)", "",
          "| stage | | kinds | share [95%] |", "|---|---|---|---|"]
    for st in STAGES:
        c = col(f"stage_{st}")
        v = c.sum() / kinds.sum() if kinds.sum() else float("nan")
        with np.errstate(invalid="ignore", divide="ignore"):
            lo, hi = pct((W @ c) / (W @ kinds))
        res[st] = (v, lo, hi)
        L.append(f"| {st} | {LABEL[st]} | {int(c.sum()):,} | {v:.4f} [{lo:.4f}, {hi:.4f}] |")
    order = sorted([s for s in STAGES if s != "P7"], key=lambda s: -res[s][0])
    top, nxt = order[0], order[1]
    clear = res[top][1] > res[nxt][2]
    L += ["", f"**Reading (frozen): most kinds stop at {top} ({LABEL[top]}), {'clear' if clear else 'shared'}** "
          f"({top} {res[top][0]:.4f} [{res[top][1]:.4f}, {res[top][2]:.4f}] against the next, {nxt}, "
          f"{res[nxt][0]:.4f} [{res[nxt][1]:.4f}, {res[nxt][2]:.4f}]).", "",
          "Rule: the largest share among P0-P6 (P0a and P0b counted apart); 'clear' if its lower bound is above the next "
          "largest's upper bound.", ""]
    L += ["## By depth", "", "| depth | kinds | " + " | ".join(STAGES) + " |", "|---|---|" + "---|" * len(STAGES)]
    for d in (1, 2, 3):
        cnt = {st: col(f"depth{d}_{st}").sum() for st in STAGES}
        tot = sum(cnt.values())
        L.append(f"| {d}{'+' if d == 3 else ''} | {int(tot):,} | " + " | ".join(
            f"{cnt[st] / tot:.3f}" if tot else "-" for st in STAGES) + " |")
    v1, v0 = col("valued1").sum(), col("valued0").sum()
    L += ["", "## The whole's value (was the kind itself ever valued by its inventor in the 5 years?)", "",
          f"- Valued: {int(v1):,}; never valued: {int(v0):,} (share never valued {v0 / (v0 + v1):.4f})." if v0 + v1
          else "- No kinds.", "", "| | " + " | ".join(STAGES) + " |", "|---|" + "---|" * len(STAGES)]
    for vv in (1, 0):
        cnt = {st: col(f"valued{vv}_{st}").sum() for st in STAGES}
        tot = sum(cnt.values())
        L.append(f"| {'valued' if vv else 'never valued'} ({int(tot):,}) | " + " | ".join(
            f"{cnt[st] / tot:.3f}" if tot else "-" for st in STAGES) + " |")
    p3, slot, inst = Counter(), Counter(), Counter()
    for s in seeds:
        p3.update(runs[s]["p3_reasons"])
        slot.update(runs[s]["slot"])
        inst.update(runs[s]["instead"])
    t3, ts, ti = sum(p3.values()), sum(slot.values()), sum(inst.values())
    L += ["", "## Within P3: why making the part was not the option offered (looks, in P3 kinds)", "",
          ("- " + ", ".join(f"{k} {v:,} ({v / t3:.3f})" for k, v in p3.most_common())) if t3 else "- none",
          "", "## When another recipe won the make slot, it was (looks, all kinds)", "",
          ("- " + ", ".join(f"{k} {v:,} ({v / ts:.3f})" for k, v in slot.most_common())) if ts else "- none",
          "", "## When making the part was offered but not chosen, the choice was (looks)", "",
          ("- " + ", ".join(f"{k} {v:,} ({v / ti:.3f})" for k, v in inst.most_common(12))) if ti else "- none", ""]
    finish(L)


if __name__ == "__main__":
    main()
