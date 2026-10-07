"""HB1 — why a shared home raised extinction (exploratory, read-only from saved outputs; after the frozen analysis).
Compares control (F1), HB1 and sham on: pairing, births per partnered woman, mates within sight, spread, starvation by
period, deaths by stage and cause.

  python experiments/HB1_home_base/explore_hb1.py      -> explore.md
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(HERE))
import analyse_hb1 as H  # noqa: E402

A = H.A


def agg(R, y0, y1, keys):
    n = Counter()
    for r in R.values():
        for y in range(y0, y1):
            v = r["Y"].get(y, {})
            n.update({k: v.get(k, 0) for k in keys})
    return n


def main():
    C = H.load(EXP / "F1_baseline_fragility" / "output", H.SEEDS)
    X = H.load(HERE / "output", H.SEEDS, "h_")
    S = H.load(HERE / "output", H.SEEDS, "s_")
    L = ["# HB1 exploratory follow-up (read-only; after the frozen analysis)\n"]
    w = L.append
    keys = ("person_weeks", "woman_weeks", "births", "pairs", "starving_weeks", "r_no_partner", "r_partner_dead",
            "r_pregnant", "r_apart", "r_nursing", "r_eligible", "r_low_health", "r_starving", "women_single",
            "women_single_no_mate", "women_single_no_mate_near", "deaths")
    for y0, y1 in ((0, 10), (10, 40), (40, 120)):
        w(f"## Years {y0}–{y1 - 1}\n")
        w("| measure | C | H | S |")
        w("|---|---|---|---|")
        rows = {}
        for name, R in (("C", C), ("H", X), ("S", S)):
            n = agg(R, y0, y1, keys)
            py, wy = n["person_weeks"] / 52, n["woman_weeks"] / 52
            partnered = n["woman_weeks"] - n["r_no_partner"] - n["r_partner_dead"]
            rows[name] = {
                "pairings per person-year": n["pairs"] / py if py else None,
                "births per woman-year": n["births"] / wy if wy else None,
                "births per partnered woman-year": n["births"] / (partnered / 52) if partnered else None,
                "share of woman-weeks without a partner": n["r_no_partner"] / n["woman_weeks"] if n["woman_weeks"] else None,
                "partnered, not pregnant: share eligible to conceive": (n["r_eligible"] / (partnered - n["r_pregnant"])
                                                                         if partnered - n["r_pregnant"] else None),
                "partnered, not pregnant: share nursing": (n["r_nursing"] / (partnered - n["r_pregnant"])
                                                           if partnered - n["r_pregnant"] else None),
                "single women with no eligible man within sight": (n["women_single_no_mate_near"] / n["women_single"]
                                                                   if n["women_single"] else None),
                "single women with no eligible man anywhere": (n["women_single_no_mate"] / n["women_single"]
                                                               if n["women_single"] else None),
                "starving share of person-weeks": n["starving_weeks"] / n["person_weeks"] if n["person_weeks"] else None,
                "deaths per person-year": n["deaths"] / py if py else None,
                "person-years": py,
            }
        for k in rows["C"]:
            w(f"| {k} | " + " | ".join(A.fmt(rows[a][k], 0 if k == "person-years" else 3) for a in ("C", "H", "S")) + " |")
        w("")
    w("## Spread at year 20 (median over worlds alive)\n")
    w("| measure | C | H | S |")
    w("|---|---|---|---|")
    for k in ("groups", "nearest_adult", "n"):
        vals = []
        for R in (C, X, S):
            xs = sorted(r["Y"][20][k] for r in R.values() if r["Y"].get(20, {}).get("n") and r["Y"][20].get(k) is not None)
            vals.append(A.fmt(xs[len(xs) // 2], 2) if xs else "–")
        w(f"| {k} | " + " | ".join(vals) + " |")
    w("\n## Deaths by stage and cause, years 0–39\n")
    for name, R in (("C", C), ("H", X), ("S", S)):
        c = Counter((d[3], d[1]) for r in R.values() for d in r["deaths"] if d[0] < 40)
        st = Counter(d[3] for r in R.values() for d in r["deaths"] if d[0] < 40)
        w(f"- {name}: by stage " + ", ".join(f"{k} {v}" for k, v in st.most_common()) + "; top causes "
          + ", ".join(f"{k[0]}/{k[1]} {v}" for k, v in c.most_common(6)))
    text = "\n".join(L) + "\n"
    (HERE / "explore.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
