"""F1 — the exploratory numbers in findings_discovery.md ("The mechanism"), reproducible (rule 16). These were first read
with one-off snippets after the frozen analysis; this script makes them traceable. Exploratory, not confirmatory.

  python experiments/F1_baseline_fragility/explore_f1.py discovery   (or: holdout)
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import analyse_f1 as A  # noqa: E402


def mates(rs, y0, y1):
    ws = wn = wf = 0
    pops = []
    for r in rs:
        for y in range(y0, y1):
            c = r["Y"].get(y, {})
            ws += c.get("women_single", 0)
            wn += c.get("women_single_no_mate_near", 0)
            wf += c.get("women_single_no_mate", 0)
            if c.get("n"):
                pops.append(c["n"])
    return ws, wn, wf, sorted(pops)[len(pops) // 2] if pops else None


def main(which):
    R = A.load(A.DISCOVERY if which == "discovery" else A.HOLDOUT)
    ext = [r for r in R.values() if r["extinct"]]
    sur = [r for r in R.values() if not r["extinct"]]
    L = [f"# F1 exploratory numbers: {which}\n"]
    L.append("## Early rates (years 0-9 and 10-19)\n")
    for lab, y0, y1 in (("years 0-9", 0, 10), ("years 10-19", 10, 20)):
        for g, rs in (("survivors", sur), ("extinct", ext)):
            t = A.rates(None, [(r, y0, y1) for r in rs])
            L.append(f"- {lab}, {g}: " + ", ".join(f"{k} {A.fmt(t[k])}" for k in (
                "births_per_woman_year", "deaths_per_person_year", "child_deaths_per_birth", "starving_share",
                "block_no_partner", "pairs_per_person_year")))
    L.append("\n## Single women 16-45 without a mate-eligible man (mid-year snapshots)\n")
    for lab, rs, y0, y1 in (("survivors, years 0-39", sur, 0, 40), ("survivors, years 40-119", sur, 40, 120),
                            ("extinct, whole life", ext, 0, 120)):
        ws, wn, wf, mp = mates(rs, y0, y1)
        if ws:
            L.append(f"- {lab}: {ws} single-woman-years; none within sight {wn} ({wn / ws:.0%}); none in the world "
                     f"{wf} ({wf / ws:.0%}); median population {mp}")
    L.append("\n## Extinct worlds: before and after the last birth B\n")
    for r in sorted(ext, key=lambda r: r["E"]):
        B = max((b[0] for b in r["births"]), default=-1)
        a = mates([r], max(0, B - 10), B + 1)
        b = mates([r], B + 1, r["E"] + 1)
        nw = sum(r["Y"].get(y, {}).get("women", 0) for y in range(B + 1, r["E"] + 1))
        L.append(f"- seed {r['seed']}: B {B}, E {r['E']}; decade before B: single-woman-years {a[0]}, none within sight "
                 f"{a[1]}, none in world {a[2]}; after B: woman-years {nw}, single {b[0]}, none within sight {b[1]}, "
                 f"none in world {b[2]}")
    L.append("\n## Deaths under 12, by cause\n")
    for g, rs in (("survivors", sur), ("extinct", ext)):
        c = Counter(d[1] for r in rs for d in r["deaths"] if d[2] is not None and d[2] < 12)
        L.append(f"- {g}: births {sum(len(r['births']) for r in rs)}, child deaths {sum(c.values())}: "
                 + ", ".join(f"{k} {v}" for k, v in c.most_common()))
    text = "\n".join(L) + "\n"
    (A.HERE / f"explore_{which}.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "discovery")
