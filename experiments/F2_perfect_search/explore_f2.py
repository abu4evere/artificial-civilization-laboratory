"""F2 — descriptive follow-ups the frozen design asked for (worlds lost under perfect finding are reported and examined),
and the worlds that die either way. Exploratory; reads F1's and F2's saved outputs only.

  python experiments/F2_perfect_search/explore_f2.py
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import analyse_f2 as A2  # noqa: E402


def main():
    P = A2.load(HERE / "output", A2.SEEDS)
    C = A2.load(A2.F1 / "output", A2.SEEDS)
    L = ["# F2 exploratory follow-ups\n"]
    for title, seeds in (("Lost under perfect finding (survived in F1)",
                          [s for s in A2.SEEDS if not C[s]["extinct"] and P[s]["extinct"]]),
                         ("Die either way", [s for s in A2.SEEDS if C[s]["extinct"] and P[s]["extinct"]])):
        L.append(f"## {title}\n")
        for s in seeds:
            for name, R in (("F1", C), ("F2", P)):
                r = R[s]
                c = Counter(d[1] for d in r["deaths"])
                kids = sum(1 for d in r["deaths"] if d[2] is not None and d[2] < 12)
                L.append(f"- seed {s} {name}: pops {r['pops']}; births {len(r['births'])}, deaths under 12 {kids}; "
                         f"died out {'year ' + str(r['E']) if r['extinct'] else 'no'}; causes "
                         + ", ".join(f"{k} {v}" for k, v in c.most_common(4)))
        L.append("")
    L.append("## Pooled rates, all worlds (F1 vs F2)\n")
    for name, R in (("F1", C), ("F2", P)):
        t = A2.A.rates(None, [(r, 0, (r["E"] + 1) if r["extinct"] else 120) for r in R.values()])
        L.append(f"- {name}: " + ", ".join(f"{k} {A2.A.fmt(t[k])}" for k in (
            "births_per_woman_year", "deaths_per_person_year", "child_deaths_per_birth", "starving_share",
            "block_no_partner", "block_apart", "cause_starvation")))
    text = "\n".join(L) + "\n"
    (HERE / "explore.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
