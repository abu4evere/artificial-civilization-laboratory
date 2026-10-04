"""E6.6 analysis: the reward horizon, from output/horizon_<seed>.json. Read-only. Writes horizon.md."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
WPY = 52
BINS = [(0, 1, "0–1 weeks"), (2, 4, "2–4 weeks"), (5, 12, "5–12 weeks"), (13, 26, "13–26 weeks"), (27, 52, "27–52 weeks")]
LR, DISCOUNT = 0.05, 0.8          # config.learning_rate, config.discount (today's code)


def bin_of(d):
    for lo, hi, name in BINS:
        if lo <= d <= hi:
            return name
    return "over 52 weeks"


def main():
    runs = [json.loads(f.read_text(encoding="utf-8")) for f in sorted((HERE / "output").glob("horizon_*.json"))]
    L = ["# E6.6: The reward horizon · how far back can people learn?", ""]
    w = L.append
    w(f"Watch-only replays of today's code (the live world's code), seeds "
      f"{', '.join(str(r['seed']) for r in runs)}, {runs[0]['years']} years each. "
      f"Replays matched the saved worlds at year 100: {', '.join(str(r['replay_matches_year100']) for r in runs)}.")
    w("")

    # --- 1. habits ------------------------------------------------------------------------------
    sd = sum(r["reward_sd"] for r in runs) / len(runs)
    w("## 1. Habits (what kind of action goes well in a situation)")
    w("")
    w(f"Each week's habit update counts next week's prospects at {DISCOUNT}, so a reward k weeks after an act counts "
      f"{DISCOUNT}^k. The act's own reward is mixed with every week in between, whose rewards vary with a standard "
      f"deviation of **{sd:.2f}** (measured).")
    w("")
    w("| delay | weight of the reward | a reward of 1.0 stands out from one ordinary week's noise? |")
    w("|---|---|---|")
    for k in (1, 2, 5, 10, 20, 52):
        wt = DISCOUNT ** k
        w(f"| {k} week{'s' if k > 1 else ''} | {wt:.3f} | {'yes' if wt > sd else 'no'} |")
    w("")
    w("And habits are kept per situation (32 of them: food in hand, company, season), not per act. What they carry "
      "is how good a situation tends to be, not which earlier act made it so.")
    w("")

    # --- 2. placements -------------------------------------------------------------------------
    credits = [c for r in runs for c in r["credits"]]
    w("## 2. Leaving things in places (sowing, stashing, heaping): credit by delay")
    w("")
    w(f"{len(credits)} times an outcome moved a belief about something left somewhere. The delay is the weeks since "
      "that thing was last left at that spot.")
    w("")
    by = defaultdict(lambda: [0, 0])
    chan = Counter()
    for t, pid, key, ch, d, c in credits:
        if d is None:
            continue
        by[bin_of(d)][0 if ch > 0 else 1] += 1
        chan[(c, bin_of(d))] += 1
    w("| delay | credits up | credits down |")
    w("|---|---|---|")
    for _, _, name in BINS:
        w(f"| {name} | {by[name][0]} | {by[name][1]} |")
    w("")
    w("Which experience gave the credit:")
    w("")
    w("| experience | " + " | ".join(n for _, _, n in BINS) + " |")
    w("|---|" + "---|" * len(BINS))
    for c in sorted({k[0] for k in chan}, key=str):
        w(f"| {c} | " + " | ".join(str(chan[(c, n)]) for _, _, n in BINS) + " |")
    w("")

    # did they repeat what was credited?
    puts = defaultdict(list)
    makes_by = defaultdict(list)
    for r in runs:
        for t, pid, key in r["puts"]:
            puts[(r["seed"], pid, key)].append(t)
        for k, ticks in r["makes"].items():
            pid, sig = k.split("|", 1)
            makes_by[(r["seed"], pid, sig)] = ticks
    rep = defaultdict(lambda: [0, 0, 0, 0])     # bin -> [up n, up repeated, down n, down repeated]
    for r in runs:
        for t, pid, key, ch, d, c in r["credits"]:
            if d is None:
                continue
            thing, season = key.rsplit("@", 1)
            if "/" in thing:
                later = [x for x in makes_by.get((r["seed"], pid, thing), []) if t < x <= t + WPY
                         and (x % WPY) // 13 == int(season)]
            else:
                later = [x for x in puts.get((r["seed"], pid, key), []) if t < x <= t + WPY]
            row = rep[bin_of(d)]
            if ch > 0:
                row[0] += 1
                row[1] += bool(later)
            else:
                row[2] += 1
                row[3] += bool(later)
    w("**Did they do it again within a year?** Learning means a credit up is followed by the act more often than a "
      "credit down.")
    w("")
    w("| delay | after a credit up | after a credit down | difference |")
    w("|---|---|---|---|")
    for _, _, name in BINS:
        a, b, c_, d_ = rep[name]
        if a + c_ == 0:
            continue
        pu = b / a if a else None
        pd = d_ / c_ if c_ else None
        diff = f"{100 * (pu - pd):+.0f} points" if pu is not None and pd is not None else "–"
        w(f"| {name} | {'–' if pu is None else f'{100 * pu:.0f}% of {a}'} | {'–' if pd is None else f'{100 * pd:.0f}% of {c_}'} | {diff} |")
    w("")

    # --- 3. made things -------------------------------------------------------------------------
    w("## 3. Made things: from making to first use")
    w("")
    delays = Counter()
    again = defaultdict(lambda: [0, 0])
    never = [0, 0]
    for r in runs:
        uses = r["uses"]
        for k, ticks in r["makes"].items():
            m0 = ticks[0]
            more = any(x > m0 + 2 for x in ticks[1:])
            u = uses.get(k)
            if u is None or u[0] < m0:
                if u is None:
                    never[0] += 1
                    never[1] += more
                continue
            b = bin_of(u[0] - m0)
            delays[b] += 1
            again[b][0] += 1
            again[b][1] += more
    w("| first use after making | things | made again later |")
    w("|---|---|---|")
    for _, _, name in BINS + [(0, 0, "over 52 weeks")]:
        if again[name][0]:
            w(f"| {name} | {again[name][0]} | {100 * again[name][1] / again[name][0]:.0f}% |")
    if never[0]:
        w(f"| never used | {never[0]} | {100 * never[1] / never[0]:.0f}% |")
    w("")
    w("A made thing's worth attaches to the thing, and grows each time it is used, for as long as it is held. So "
      "making is the one act whose payoff can come any time later and still count, as long as the thing is in hand.")
    (HERE / "horizon.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
