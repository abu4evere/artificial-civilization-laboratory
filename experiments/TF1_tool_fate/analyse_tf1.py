"""TF1 analysis, written before any data (questions.md, frozen as `TF1-frozen`; operational note 1).

  python experiments/TF1_tool_fate/analyse_tf1.py            # writes results.md
  python experiments/TF1_tool_fate/analyse_tf1.py --smoke --dir <folder>    # throwaway; writes nothing
"""
from __future__ import annotations

import glob
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_tf1 import BIN_EDGES, SEEDS, WPY  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261027)
BINS = [f"{BIN_EDGES[i]}-{BIN_EDGES[i + 1]}" for i in range(len(BIN_EDGES) - 1)]
FATES = ("worn_out", "deleted_at_limit", "used_in_making", "lost_at_death", "lost_with_body", "unknown")


def bin_of(tick):
    y = tick / WPY
    for i in range(len(BIN_EDGES) - 1):
        if y < BIN_EDGES[i + 1]:
            return i
    return len(BIN_EDGES) - 2


def ci(reps):
    reps = np.asarray(reps, float)
    reps = reps[np.isfinite(reps)]
    if len(reps) == 0:
        return "[-]"
    lo, hi = np.percentile(reps, [2.5, 97.5])
    return f"[{lo:.3g}, {hi:.3g}]"


def boot_ratio(num, den):
    num, den = np.asarray(num, float), np.asarray(den, float)
    est = num.sum() / den.sum() if den.sum() else float("nan")
    ix = RNG.integers(0, len(num), size=(REPS, len(num)))
    with np.errstate(invalid="ignore", divide="ignore"):
        reps = num[ix].sum(1) / den[ix].sum(1)
    return est, reps


def alive_at(r, year):
    return r["final_tick"] > year * WPY


def death_route(t):
    """What happened to a forage tool at its first holder's death: inherited / taken from the body / lost with the
    body / still with the body / lost at death; None if no holder of it died."""
    moves = t[7]
    if "inherited" in moves:
        return "inherited"
    if "left_with_body" in moves:
        i = moves.index("left_with_body")
        if "taken_from_body" in moves[i:]:
            return "taken_from_body"
        return "lost_with_body" if t[3] == "lost_with_body" else "with_body_at_end"
    if t[3] == "lost_at_death":
        return "lost_at_death"
    return None


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rs = [json.load(open(f)) for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json")))]
    L = ["# TF1 — Where do made things go? Results", "",
         "Frozen as `TF1-frozen` (operational note 1). run_tf1.py, analyse_tf1.py (written before data).", ""]
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    unk = sum(b.get("end_all_unknown", 0) for r in rs for b in r["bins"].values())
    ends = sum(r["ended"] for r in rs)
    fps = {r["code_hash"] for r in rs} | {r["code_hash_after"] for r in rs}
    ledger = sum(sum(r["mismatch"].values()) for r in rs)
    ok = ("All: PASS" in zero) and sorted(r["seed"] for r in rs) == sorted(SEEDS) and len(fps) == 1 and ledger == 0
    L += ["## Validity", "",
          f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
          f"- All worlds present ({len(rs)} of {len(SEEDS)}): **{'yes' if sorted(r['seed'] for r in rs) == sorted(SEEDS) else 'NO'}**",
          f"- One fingerprint (`code_v7`): **{'yes' if len(fps) == 1 else 'NO'}**",
          f"- The ledger balances in every world (appeared = ended + still in the world): **{'yes' if ledger == 0 else 'NO'}**",
          f"- Unknown fates: {unk} of {ends} ends ({unk / max(ends, 1):.4f}); under 1%: "
          f"**{'yes' if unk < 0.01 * max(ends, 1) else 'NO: readings marked unreliable'}**", "",
          f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    # population
    L += ["## Population (worlds alive at each bin's start)", "", "| bin | worlds | mean population |", "|---|---|---|"]
    for i, name in enumerate(BINS):
        al = [r for r in rs if alive_at(r, BIN_EDGES[i])]
        wk = (BIN_EDGES[i + 1] - BIN_EDGES[i]) * WPY
        L.append(f"| {name} | {len(al)} of {len(rs)} | "
                 f"{np.mean([r['bins'].get(str(i), {}).get('pw', 0) / wk for r in al]) if al else float('nan'):.1f} |")
    L += ["", f"Worlds that ended before year {BIN_EDGES[-1]}: "
          f"{sorted(round(r['final_tick'] / WPY) for r in rs if r['final_tick'] < BIN_EDGES[-1] * WPY)}.", ""]

    # Q1
    L += ["## Q1 — How do forage tools end? (forage factor > 1; by the bin in which they ended)", "",
          "| bin | ends | " + " | ".join(FATES) + " | life (weeks, mean) | uses left at end (mean) |",
          "|---" * (4 + len(FATES)) + "|"]
    for i, name in enumerate(BINS):
        ts = [t for r in rs for t in r["tools"] if t[3] != "still_held" and bin_of(t[4]) == i]
        if not ts:
            continue
        c = Counter(t[3] for t in ts)
        L.append(f"| {name} | {len(ts)} | " + " | ".join(f"{c[f] / len(ts):.3f}" for f in FATES)
                 + f" | {np.mean([t[4] - t[0] for t in ts]):.1f} | {np.mean([t[5] for t in ts]):.1f} |")
    allts = [t for r in rs for t in r["tools"] if t[3] != "still_held"]
    L += ["", "All bins pooled, with world-bootstrap intervals:", ""]
    for f in FATES:
        num = [sum(1 for t in r["tools"] if t[3] == f) for r in rs]
        den = [sum(1 for t in r["tools"] if t[3] != "still_held") for r in rs]
        est, reps = boot_ratio(num, den)
        L.append(f"- {f}: {est:.3f} {ci(reps)}")
    still = sum(1 for r in rs for t in r["tools"] if t[3] == "still_held")
    L += [f"- (forage tools still held at the end: {still}; ended: {len(allts)})", ""]
    # uses destroyed
    pw = sum(b.get("pw", 0) for r in rs for b in r["bins"].values())
    L += ["**Forage-tool uses left at the end, by fate** (uses destroyed), per 1,000 person-years:", ""]
    for f in FATES:
        u = sum(t[5] for t in allts if t[3] == f)
        L.append(f"- {f}: {u / (pw / WPY) * 1000:.1f}")
    L.append("")

    # Q2
    dels = [t for r in rs for t in r["tools"] if t[3] == "deleted_at_limit"]
    all_del = sum(b.get("end_all_deleted_at_limit", 0) for r in rs for b in r["bins"].values())
    num = [sum(1 for t in r["tools"] if t[3] == "deleted_at_limit") for r in rs]
    den = [sum(b.get("end_all_deleted_at_limit", 0) for b in r["bins"].values()) for r in rs]
    est, reps = boot_ratio(num, den)
    L += ["## Q2 — The carry limit", "",
          f"- Made things deleted at the carry limit: {all_del}. **Share that were working forage tools: {est:.3f} "
          f"{ci(reps)}.**"]
    if dels:
        ex = [t[8] for t in dels if t[8]]
        L += [f"- Their uses left (mean): {np.mean([t[5] for t in dels]):.1f}; their forage factor (mean) "
              f"{np.mean([t[2] for t in dels]):.3f}.",
              f"- Better forage tool than the worst thing kept: {np.mean([e[1] for e in ex]):.3f}.",
              f"- Holder had a child under 16 in their care: {np.mean([e[2] for e in ex]):.3f}; anyone within reach: "
              f"{np.mean([e[3] for e in ex]):.3f}; a child under 16 within reach: {np.mean([e[4] for e in ex]):.3f}."]
    ud = sum(t[5] for t in dels)
    uw = sum(t[5] for t in allts if t[3] == "worn_out")
    L += [f"- Forage-tool uses destroyed by the carry limit: {ud}; left at wearing out: {uw}.", ""]
    tb = Counter()
    for r in rs:
        for b_ in r["bins"].values():
            tb.update(b_)
    L += ["**Gone within the week they were made** (operational note 2; never in the weekly census):", ""]
    for k_ in ("play", "make"):
        n_ = tb[f"made_{k_}"]
        if n_:
            L.append(f"- made in {k_}: {n_:.0f}; gone the same week {tb[f'made_{k_}_gone_same_week'] / n_:.3f}; of those, "
                     f"a kind with worth 0: {tb[f'made_{k_}_gone_worth0'] / max(tb[f'made_{k_}_gone_same_week'], 1):.3f}")
    L.append("")

    # Q3
    dr = [death_route(t) for r in rs for t in r["tools"]]
    dr = [x for x in dr if x]
    c = Counter(dr)
    num = [sum(1 for t in r["tools"] if death_route(t) == "inherited") for r in rs]
    den = [sum(1 for t in r["tools"] if death_route(t)) for r in rs]
    est, reps = boot_ratio(num, den)
    L += ["## Q3 — Forage tools at their holder's death", "",
          f"Forage tools whose holder died: {len(dr)}. " + ", ".join(f"{k} {v / len(dr):.3f}" for k, v in c.most_common())
          + "." if dr else "No forage tool's holder died.",
          f"", f"**Inherited: {est:.3f} {ci(reps)}.**", "",
          "| bin | forage-tool uses lost at death or with the body, per 1,000 person-years |", "|---|---|"]
    for i, name in enumerate(BINS):
        u = sum(t[5] for r in rs for t in r["tools"] if t[3] in ("lost_at_death", "lost_with_body") and bin_of(t[4]) == i)
        p_ = sum(r["bins"].get(str(i), {}).get("pw", 0) for r in rs)
        if p_:
            L.append(f"| {name} | {u / (p_ / WPY) * 1000:.1f} |")
    L.append("")

    # Q4
    L += ["## Q4 — Children and tools", "",
          "| bin | children (6-15) holding a forage tool | no tool while their carer holds 1+ | no tool while carer holds 2+ "
          "| adults holding a forage tool |", "|---|---|---|---|---|"]
    for i, name in enumerate(BINS):
        b = Counter()
        for r in rs:
            b.update(r["bins"].get(str(i), {}))
        if not b["pw"]:
            continue
        f = lambda a, d: f"{b[a] / b[d]:.3f}" if b[d] else "-"   # noqa: E731
        L.append(f"| {name} | {f('child_tool_w', 'child_w')} | {f('child_carer1_none_w', 'child_carer1_w')} "
                 f"({b['child_carer1_w']:.0f} wk) | {f('child_carer2_none_w', 'child_carer2_w')} | "
                 f"{f('adult_tool_w', 'adult_w')} |")
    num = [sum(b.get("child_carer1_none_w", 0) for b in r["bins"].values()) for r in rs]
    den = [sum(b.get("child_carer1_w", 0) for b in r["bins"].values()) for r in rs]
    est, reps = boot_ratio(num, den)
    L += ["", f"**Child-weeks with no forage tool while the carer holds one, all bins: {est:.3f} {ci(reps)}.**", ""]
    ft = [f for r in rs for f in r["first_tool"] if f[2] >= 0]
    if ft:
        c = Counter(f[1] for f in ft)
        L += [f"First forage tool (world-born, {len(ft)} people): median age {np.median([f[0] for f in ft]) / WPY:.1f} "
              f"years; before 16: {np.mean([f[0] < 16 * WPY for f in ft]):.3f}; how: "
              + ", ".join(f"{k} {v / len(ft):.3f}" for k, v in c.most_common()) + ".", ""]

    # Q5
    L += ["## Q5 — Replacement within a year, by route", "",
          "| bin | lost their last forage tool | replaced within a year | made | inherited | taken from a body | other |",
          "|---|---|---|---|---|---|---|"]
    for i, name in enumerate(BINS):
        b = Counter()
        for r in rs:
            b.update(r["bins"].get(str(i), {}))
        rep = {k[9:]: v for k, v in b.items() if k.startswith("replaced_")}
        n = sum(rep.values()) + b["not_replaced"]
        if not n:
            continue
        tot = sum(rep.values()) or 1
        other = tot - rep.get("made", 0) - rep.get("inherited", 0) - rep.get("taken_from_body", 0)
        L.append(f"| {name} | {n:.0f} | {sum(rep.values()) / n:.3f} | {rep.get('made', 0) / tot:.3f} | "
                 f"{rep.get('inherited', 0) / tot:.3f} | {rep.get('taken_from_body', 0) / tot:.3f} | {other / tot:.3f} |")
    L.append("")
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
