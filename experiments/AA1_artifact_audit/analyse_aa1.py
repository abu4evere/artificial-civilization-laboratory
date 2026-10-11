"""AA1 analysis in the frozen order (questions.md, `AA1-frozen`). Written and smoke-tested before any data.

Each shortcut's share is pooled over the worlds of a set (numerator sum ÷ denominator sum), with a 95% percentile
bootstrap over worlds (10,000 resamples, random.Random(2026)) and the absolute counts beside it. Material: share ≥ 5%
in discovery and holdout. Borderline: estimate below 5% but the interval reaches 5%.

  python experiments/AA1_artifact_audit/analyse_aa1.py discovery
  python experiments/AA1_artifact_audit/analyse_aa1.py holdout
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_aa1 import DISCOVERY, HOLDOUT  # noqa: E402

# id, label, numerator, denominator, what it touches, intended? (from the frozen intent table)
MEASURES = [
    ("A1", "corner crossings, share of all water crossings", "crossings_corner", "crossings", "crossings", "no"),
    ("A2", "wrapping-edge crossings, share of all water crossings", "crossings_wrap", "crossings", "crossings", "yes (DESIGN.md: the map wraps)"),
    ("A3", "food foraged from the dead, share of food foraged from the wild", "foraged_from_dead", "foraged_wild", "food", "unclear"),
    ("A5", "\"go to\" moves toward an out-of-sight loved one, share of all \"go to\" moves", "joins_loved_beyond_sight", "joins", "go to moves", "not stated"),
    ("A6a", "food given (decided on the receiver's exact food), share of food foraged from the wild", "gift_food", "foraged_wild", "food", "not stated"),
    ("A6b", "food stolen (decided on the victim's exact food), share of food foraged from the wild", "steal_food", "foraged_wild", "food", "not stated"),
    ("A6c", "partner-search \"go to\" moves toward someone beyond sight, share of partner-search moves", "joins_seek_beyond_sight", "joins_seek", "partner search", "not stated"),
    ("A6d", "dryness judgements resting on water beyond the person's sight, share of judgements", "dry_beyond_sight", "dry_judgements", "dryness judgements", "not stated"),
]


def share(R, num, den, idx=None):
    rs = R if idx is None else [R[i] for i in idx]
    d = sum(r.get(den, 0) for r in rs)
    return (sum(r.get(num, 0) for r in rs) / d) if d else None


def main(name, out=HERE / "output", seeds=None, write=True):
    seeds = seeds or (DISCOVERY if name == "discovery" else HOLDOUT)
    R = [json.loads((out / f"seed_{s}.json").read_text(encoding="utf-8"))["audit"] for s in seeds]
    L = [f"# AA1 — artifact audit: {name} ({len(R)} control worlds, seeds {seeds[0]}–{seeds[-1]})\n"]
    ok = "All: PASS" in (out / "zero.txt").read_text(encoding="utf-8")
    L.append(f"- Logging copy leaves the world unchanged (state hash): **{'yes' if ok else 'NO'}**")
    py = sum(r.get("person_weeks", 0) for r in R) / 52
    L.append(f"- Person-years observed: {py:,.0f}\n")
    L.append("| | shortcut | share | 95% interval | counts | intended? | reading |")
    L.append("|---|---|---|---|---|---|---|")
    for mid, label, num, den, touches, intent in MEASURES:
        s = share(R, num, den)
        if s is None:
            L.append(f"| {mid} | {label} | – | – | 0 {touches} | {intent} | not observed |")
            continue
        rng, n = random.Random(2026), len(R)
        boots = sorted(x for x in (share(R, num, den, [rng.randrange(n) for _ in range(n)]) for _ in range(10000)) if x is not None)
        lo, hi = boots[int(.025 * len(boots))], boots[int(.975 * len(boots)) - 1]
        reading = "**material**" if s >= .05 else "**borderline**" if hi >= .05 else "below 5%"
        cnt = sum(r.get(num, 0) for r in R), sum(r.get(den, 0) for r in R)
        fmt = (lambda v: f"{v:,.0f}") if touches != "food" else (lambda v: f"{v:,.0f} food units")
        L.append(f"| {mid} | {label} | **{s:.1%}** | {lo:.1%}–{hi:.1%} | {fmt(cnt[0])} of {fmt(cnt[1])} | {intent} | {reading} |")
    tot = {k: sum(r.get(k, 0) for r in R) for k in ("gifts", "thefts", "walks", "walks_wrap", "walks_corner", "joins_loved", "joins_loved_beyond_sight",
                                                   "dist_loved_beyond_sum", "dropped_food", "crossings", "crossings_boat", "crossings_corner", "crossings_wrap", "crossings_other")}
    L.append(f"\nWater crossings: {tot['crossings']:,} in all: by boat {tot['crossings_boat']:,}, corner {tot['crossings_corner']:,}, "
             f"wrapping edge {tot['crossings_wrap']:,}, other {tot['crossings_other']:,}. Walks with a corner step: {tot['walks_corner']:,} "
             f"of {tot['walks']:,}.")
    L.append(f"\nBeside them: gifts {tot['gifts'] / py:.2f} and thefts {tot['thefts'] / py:.3f} per person-year; "
             f"{tot['walks_wrap'] / max(1, tot['walks']):.1%} of all walks cross the wrapping edge; "
             f"of \"go to\" moves toward loved ones, {tot['joins_loved_beyond_sight'] / max(1, tot['joins_loved']):.0%} aim at "
             f"someone out of sight, on average {tot['dist_loved_beyond_sum'] / max(1, tot['joins_loved_beyond_sight']):.1f} tiles away; "
             f"food dropped by the dead {tot['dropped_food']:,.0f} units in all.")
    L.append("\nA shortcut that matches an intended rule is a property of ACL's world, not a flaw. A material unintended shortcut"
             " goes to the creator with the findings it could touch; nothing is fixed here.")
    text = "\n".join(L) + "\n"
    if write:
        (HERE / f"results_{name}.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main(sys.argv[1])
