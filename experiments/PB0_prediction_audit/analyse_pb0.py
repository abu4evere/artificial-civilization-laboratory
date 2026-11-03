"""PB0 analysis, written before any data (questions.md, frozen as `PB0-frozen`).

  python experiments/PB0_prediction_audit/analyse_pb0.py                      # writes results.md
  python experiments/PB0_prediction_audit/analyse_pb0.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_pb0 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261111)
SEL, HOLD = (0, 1), (2, 3)               # replays used to pick the winner, and the held-out replays
FOODS = ("starving or weak", "under 2 weeks", "2-6 weeks", "6+ weeks")
SEASONS = ("spring", "summer", "autumn", "winter")
KIND = {"make": "make", "hunt": "hunt", "gather": "gather", "forage": "food", "take": "food"}


def pct(x):
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


def total(mark):
    return mark[0] + mark[1]              # reward + mood parts


def outcomes(d, h):
    """{option index: list over replays of [reward, mood, alive, food, health] at horizon h} (studied options only)."""
    out = {}
    for k, v in d["outcomes"].items():
        reps = [rp.get(str(h)) for rp in v["replays"]]
        if all(m is not None for m in reps):
            out[int(k)] = reps
    return out


def held_out(d, h, base_k=None):
    """(gain on held-out replays, winner, base option, held-out values) for one decision at horizon h; None if the base
    option was not studied. The winner has the best mean over the selection replays; ties go to the higher score."""
    oc = outcomes(d, h)
    base_k = d["top"] if base_k is None else base_k
    if base_k not in oc:
        return None
    score = {k: d["options"][k][0] for k in oc}
    win = max(oc, key=lambda k: (np.mean([total(oc[k][i]) for i in SEL]), score[k], -k))
    hv = {k: [oc[k][i] for i in HOLD] for k in (win, base_k)}
    gain = np.mean([total(m) for m in hv[win]]) - np.mean([total(m) for m in hv[base_k]])
    return float(gain), win, base_k, hv


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {}
    for f in sorted(glob.glob(str(OUTDIR / "c_seed_*.json"))):
        r = json.load(open(f))
        runs[r["seed"]] = r
    zero = ""
    for name in ("zero_cloud.log", "zero_local.log"):
        if (HERE / name).exists():
            zero = (HERE / name).read_text(encoding="utf-8", errors="replace")
            break
    R.base.setup(R.CODE)
    fp_now = R.base.fingerprint(R.CODE)
    m = re.search(r"code_v12 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    seeds = sorted(runs) if SMOKE else sorted(R.SEEDS)
    present = bool(seeds) and all(s in runs for s in seeds)
    fps = {runs[s]["code_hash"] for s in runs} | {runs[s]["code_hash_after"] for s in runs}
    ok = bool(zero_ok and present and fps == {fp_now})
    L = ["# PB0: Would knowing what happens next change people's choices? (results)", "",
         "Frozen as `PB0-frozen`. run_pb0.py, analyse_pb0.py (written before data).", "", "## Validity", "",
         f"- Zero checks (All: PASS, same `code_v12` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(runs)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_v12`'s: **{'yes' if fps == {fp_now} else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    seeds = [s for s in seeds if s in runs]
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)
    decs = {s: [d for d in runs[s]["decisions"] if not d.get("skipped")] for s in seeds}
    skipped = sum(1 for s in seeds for d in runs[s]["decisions"] if d.get("skipped"))

    # --- Primary (frozen): held-out gain G at H = 4 over the top-scored option; A = mean |top's held-out outcome|
    g_sum, a_sum, cnt = np.zeros(n), np.zeros(n), np.zeros(n)
    noise, regret, parts, ends, kinds = [], [], np.zeros(2), Counter(), Counter()
    by_food, by_season = defaultdict(list), defaultdict(list)
    for j, s in enumerate(seeds):
        for d in decs[s]:
            x = held_out(d, R.H_MAIN)
            if x is None:
                continue
            gain, win, top, hv = x
            g_sum[j] += gain
            a_sum[j] += abs(np.mean([total(m) for m in hv[top]]))
            cnt[j] += 1
            sd = abs(total(hv[top][0]) - total(hv[top][1])) / np.sqrt(2)
            noise.append(sd)
            regret.append(gain)
            parts += [np.mean([m[0] for m in hv[win]]) - np.mean([m[0] for m in hv[top]]),
                      np.mean([m[1] for m in hv[win]]) - np.mean([m[1] for m in hv[top]])]
            for lab, kk in (("winner", win), ("top", top)):
                ends[lab + "_alive"] += np.mean([m[2] for m in hv[kk]])
                ends[lab + "_food"] += np.mean([m[3] for m in hv[kk]])
                ends[lab + "_health"] += np.mean([m[4] for m in hv[kk]])
            ends["n"] += 1
            kinds["same" if win == top else KIND.get(d["options"][win][1], "other")] += 1
            by_food[FOODS[d["ctx"] // 8]].append(gain)
            by_season[SEASONS[d["season"] % 4]].append(gain)
    with np.errstate(invalid="ignore", divide="ignore"):
        G = g_sum.sum() / cnt.sum()
        A = a_sum.sum() / cnt.sum()
        Gb = (W @ g_sum) / (W @ cnt)
    lo, hi = pct(Gb)
    go = bool(lo > 0 and G >= 0.05 * A)
    L += ["## Primary (frozen): held-out gain of foresight at 4 weeks", "",
          "| decisions studied | G (held-out gain over the top-scored option) [95%] | A (mean abs. outcome of the top option) "
          "| G / A | reading |", "|---|---|---|---|---|",
          f"| {int(cnt.sum()):,} (skipped {skipped}) | {G:+.4f} [{lo:+.4f}, {hi:+.4f}] | {A:.4f} | "
          f"{(G / A if A else float('nan')):.3f} | **{'GO' if go else 'NO-GO'}** |", "",
          "Rule: GO to PB1 if G's 95% interval lies wholly above 0 and G >= 0.05 x A; otherwise NO-GO.", ""]

    # --- Described
    noise_m = float(np.mean(noise)) if noise else float("nan")
    S = float(np.mean([g > noise_m for g in regret])) if regret else float("nan")
    c = max(ends["n"], 1)
    L += ["## Described (no decision drawn)", "",
          f"- **S, regret share:** {S:.4f} of decisions have a held-out gain above the mean noise SD ({noise_m:.4f}).",
          f"- **The gain's parts** (mean per decision): from reward {parts[0] / c:+.4f}, from mood {parts[1] / c:+.4f}.",
          f"- **At 4 weeks, winner against top** (held-out means): alive {ends['winner_alive'] / c:.4f} against "
          f"{ends['top_alive'] / c:.4f}; food {ends['winner_food'] / c:.3f} against {ends['top_food'] / c:.3f}; health "
          f"{ends['winner_health'] / c:.2f} against {ends['top_health'] / c:.2f}.",
          "- **The winner's kind:** " + ", ".join(f"{k} {v}" for k, v in sorted(kinds.items(), key=lambda x: -x[1])) + "."]
    # H = 1 (in sample: one run per option) and the long sample
    g1 = []
    for s in seeds:
        for d in decs[s]:
            r1 = {int(k): v["r1"] for k, v in d.get("outcomes", {}).items() if v["r1"] is not None}
            if d["top"] in r1:
                best = max(r1, key=lambda k: (r1[k][0] + r1[k][1], d["options"][k][0]))
                g1.append(sum(r1[best]) - sum(r1[d["top"]]))
    L.append(f"- **H = 1** (in sample, one run per option): mean gain {np.mean(g1) if g1 else float('nan'):+.4f} over "
             f"{len(g1)} decisions.")
    for h in R.H_LONG:
        gl = [x[0] for s in seeds for d in decs[s] if d.get("long") for x in [held_out(d, h)] if x is not None]
        L.append(f"- **H = {h}** (long sample, held out): mean gain {np.mean(gl) if gl else float('nan'):+.4f} over "
                 f"{len(gl)} decisions.")
    # all-options sample: the full-menu winner outside the top 6
    out6 = tot = 0
    for s in seeds:
        for d in decs[s]:
            if not d.get("all"):
                continue
            oc = outcomes(d, R.H_MAIN)
            if not oc:
                continue
            order = sorted(range(len(d["options"])), key=lambda k: (-d["options"][k][0], k))
            win = max(oc, key=lambda k: (np.mean([total(oc[k][i]) for i in SEL]), d["options"][k][0], -k))
            tot += 1
            out6 += win not in order[:R.K]
    L.append(f"- **All-options sample:** the full-menu winner lies outside the top {R.K} in {out6} of {tot} decisions.")
    gp = [x[0] for s in seeds for d in decs[s] if d.get("picked") is not None
          for x in [held_out(d, R.H_MAIN, base_k=d["picked"])] if x is not None]
    L.append(f"- **Against the softmax's actual pick:** held-out gain {np.mean(gp) if gp else float('nan'):+.4f} over "
             f"{len(gp)} decisions.")
    L += ["", "| food band | decisions | mean held-out gain |", "|---|---|---|"]
    for k in FOODS:
        if by_food[k]:
            L.append(f"| {k} | {len(by_food[k])} | {np.mean(by_food[k]):+.4f} |")
    L += ["", "| season | decisions | mean held-out gain |", "|---|---|---|"]
    for k in SEASONS:
        if by_season[k]:
            L.append(f"| {k} | {len(by_season[k])} | {np.mean(by_season[k]):+.4f} |")
    lw = sum(runs[s]["sums"].get("living_weeks", 0) for s in seeds)
    aw = sum(runs[s]["sums"].get("adult_weeks", 0) for s in seeds)
    L += ["", "## Population (beside the measure)", "",
          f"Living-weeks {lw:,} and adult-weeks {aw:,} in the sampling window; extinct worlds "
          f"{sum(1 for s in seeds if runs[s]['extinct'])}.", ""]
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
