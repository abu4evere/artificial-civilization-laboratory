"""SA1-F Part B: forager mobility and group-size numbers from Binford's (2001) hunter-gatherer data, for the sight and
range evidence notes (ratios that need no tile size). Read-only; touches no ACL code.

Data: Binford's LRB table, 339 societies, as published with the R package `binford` (Marwick):
https://raw.githubusercontent.com/benmarwick/binford/master/data-raw/LRB.csv (downloaded 16 October 2026 with the
creator's permission; kept in research_notes/papers/, which is not published). Variables (codebook, Binford 2001:117):
  grppat  1 = unrestricted mobility (the whole group moves camp to camp), 2 = restricted
  nomov   residential moves per year;  dismov  total distance moved per year, in MILES
  group1  smallest group that regularly cooperates for subsistence (dispersed-phase camp)
  group2  mean size of the group camped together at the most aggregated phase
Filter as Grove et al. (2023): grppat == 1 and nomov > 0 (and dismov > 0 for distances).

  python experiments/SA1_sensitivity/evidence_ratios.py
"""
from __future__ import annotations

import csv
import statistics
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "research_notes" / "papers" / "binford_LRB.csv"
MILE = 1.609344


def num(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return x if x == x else None   # NaN -> None


def q(xs):
    xs = sorted(xs)
    qs = statistics.quantiles(xs, n=4)
    return f"median {statistics.median(xs):.1f} (middle half {qs[0]:.1f}–{qs[2]:.1f}; n = {len(xs)})"


def main():
    rows = list(csv.DictReader(DATA.open(encoding="utf-8")))
    assert len(rows) == 339, len(rows)
    mob = [r for r in rows if num(r["grppat"]) == 1 and (num(r["nomov"]) or 0) > 0]
    dist = [r for r in mob if (num(r["dismov"]) or 0) > 0]
    nomov = [num(r["nomov"]) for r in mob]
    weeks_between = [52 / n for n in nomov]
    km_year = [num(r["dismov"]) * MILE for r in dist]
    km_move = [num(r["dismov"]) * MILE / num(r["nomov"]) for r in dist]
    km_week = [k / 52 for k in km_year]
    g1 = [num(r["group1"]) for r in mob if num(r["group1"])]
    g2 = [num(r["group2"]) for r in mob if num(r["group2"])]
    print("# Binford (2001), fully mobile groups (grppat 1, nomov > 0)\n")
    print(f"- societies: {len(mob)} of {len(rows)}; with a distance: {len(dist)}")
    print(f"- residential moves per year: {q(nomov)}")
    print(f"- weeks between camp moves (52 / moves): {q(weeks_between)}")
    print(f"- km moved per year: {q(km_year)}")
    print(f"- km per move: {q(km_move)}")
    print(f"- km of camp movement per week, averaged over the year: {q(km_week)}")
    print(f"- smallest cooperating group (group1), people: {q(g1)}")
    print(f"- aggregated camp (group2), people: {q(g2)}")
    lo = min(dist, key=lambda r: num(r["dismov"]))
    print(f"\n(lowest distance kept: {lo['name']}, {num(lo['dismov'])} miles/year; Grove et al. dropped one anomalously "
          f"low value, not named in their text, so it is reported here and left in)")


if __name__ == "__main__":
    main()
