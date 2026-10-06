"""F1 — the exploratory leads from discovery (findings_discovery.md), checked descriptively on any set. Written before the
holdout data existed. A lead "holds" in a set if:
  L1 births stopped at least 15 years before extinction in at least two thirds of its extinct worlds;
  L2 over all single-woman-years (16-45, mid-year snapshot), at least 80% had no mate-eligible man within sight, and
     fewer than 25% had none anywhere in the world (the shortage is local, not global);
  L3 child deaths per birth in years 0-9 higher in extinct than in surviving worlds;
  L4 pairings per person-year in years 10-39 at most a third of years 0-9's, in survivors and extinct worlds alike.

  python experiments/F1_baseline_fragility/leads_check.py discovery   (or: holdout)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import analyse_f1 as A  # noqa: E402


def main(which):
    R = A.load(A.DISCOVERY if which == "discovery" else A.HOLDOUT)
    ext = [r for r in R.values() if r["extinct"]]
    sur = [r for r in R.values() if not r["extinct"]]
    L = [f"# F1 leads check: {which} ({len(ext)} of {len(R)} died out)\n"]
    gaps = [r["E"] - max((b[0] for b in r["births"]), default=-1) for r in ext]
    l1 = bool(ext) and sum(g >= 15 for g in gaps) >= 2 * len(ext) / 3
    L.append(f"- L1 years from last birth to extinction: {sorted(gaps)}: **{'holds' if l1 else 'does not hold'}**")
    ws = wn = wf = 0
    for r in R.values():
        for c in r["Y"].values():
            ws += c.get("women_single", 0)
            wn += c.get("women_single_no_mate_near", 0)
            wf += c.get("women_single_no_mate", 0)
    l2 = ws > 0 and wn / ws >= 0.80 and wf / ws < 0.25
    L.append(f"- L2 single-woman-years {ws}: none eligible within sight {wn} ({wn / max(1, ws):.0%}), none in the world "
             f"{wf} ({wf / max(1, ws):.0%}): **{'holds' if l2 else 'does not hold'}**")
    ce = A.rates(None, [(r, 0, 10) for r in ext])["child_deaths_per_birth"] if ext else None
    cs = A.rates(None, [(r, 0, 10) for r in sur])["child_deaths_per_birth"] if sur else None
    l3 = ce is not None and cs is not None and ce > cs
    L.append(f"- L3 child deaths per birth, years 0-9: extinct {A.fmt(ce)}, survivors {A.fmt(cs)}: "
             f"**{'holds' if l3 else 'does not hold'}**")
    ok4 = []
    for name, rs in (("survivors", sur), ("extinct", ext)):
        if not rs:
            continue
        a = A.rates(None, [(r, 0, 10) for r in rs])["pairs_per_person_year"]
        b = A.rates(None, [(r, 10, min(40, r["E"] + 1) if r["extinct"] else 40) for r in rs])["pairs_per_person_year"]
        ok4.append(b is not None and a and b <= a / 3)
        L.append(f"  - pairings per person-year, {name}: years 0-9 {A.fmt(a)}, years 10-39 {A.fmt(b)}")
    l4 = bool(ok4) and all(ok4)
    L.append(f"- L4 pairing collapses after the founders' decade in both: **{'holds' if l4 else 'does not hold'}**")
    text = "\n".join(L) + "\n"
    (A.HERE / f"leads_{which}.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "discovery")
