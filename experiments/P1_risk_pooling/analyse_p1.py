"""P1 tables (questions.md), written before the P1 data existed. Writes findings_tables.md.

  python experiments/P1_risk_pooling/analyse_p1.py
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
SEEDS = tuple(range(501, 517))
BANDS = ("under 0.5", "0.5-2", "2+")


def pct(a, b, d=1):
    return f"{100 * a / b:.{d}f}%" if b else "–"


def main():
    D = {(a, s): json.loads((OUT / f"{a}_seed_{s}.json").read_text(encoding="utf-8")) for a in "ab" for s in SEEDS}
    L = []
    w = L.append
    w("# P1 — Risk pooling or spreading scarcity: tables\n")
    v = (OUT / "verify.txt").read_text(encoding="utf-8").strip().replace("\n", "; ")
    rep = all(r["replay_matches"] for r in D.values())
    w(f"Probe check: {v}. Replays match the saved E13R runs in all 32: **{'yes' if rep else 'NO'}**.\n")

    for a in "ab":
        rows = [r for s in SEEDS for r in D[(a, s)]["rows"]]
        w(f"## Q1. Does family food protect, beyond one's own? (Arm {a.upper()}, everyone alive at the start of winter)\n")
        w("Each cell: went short during winter / died of starvation in winter (person-winters).\n")
        w("| own food (weeks) ↓ · family food per head (weeks) → | " + " | ".join(BANDS) + " |")
        w("|---|---|---|---|")
        for ob in BANDS:
            cells = []
            for fb in BANDS:
                g = [r for r in rows if r["own"] == ob and r["fam"] == fb]
                cells.append(f"{pct(sum(r['short'] for r in g), len(g))} / {pct(sum(r['died'] for r in g), len(g), 2)} (n={len(g):,})")
            w(f"| {ob} | " + " | ".join(cells) + " |")
        alone = [r for r in rows if r["kin"] == 0]
        w(f"\nPeople with no close kin alive: {len(alone):,} ({pct(len(alone), len(rows))}); went short "
          f"{pct(sum(r['short'] for r in alone), len(alone))}, died {pct(sum(r['died'] for r in alone), len(alone), 2)}.\n")

    w("## Q2. Do people starve amid plenty? (winter starvation deaths)\n")
    w("| | A | B |")
    w("|---|---|---|")
    dd = {a: [d for s in SEEDS for d in D[(a, s)]["deaths"]] for a in "ab"}
    w("| deaths | " + " | ".join(f"{len(dd[a]):,}" for a in "ab") + " |")
    w("| median age | " + " | ".join(f"{statistics.median([d['age'] for d in dd[a]]):.1f}" if dd[a] else "–" for a in "ab") + " |")
    w("| with no close kin alive | " + " | ".join(pct(sum(1 for d in dd[a] if d['kin'] == 0), len(dd[a])) for a in "ab") + " |")
    w("| close kin held nothing (under 1 in total) | " + " | ".join(pct(sum(1 for d in dd[a] if d['kin'] and d['kin_food'] < 1), len(dd[a])) for a in "ab") + " |")
    w("| median food held by close kin, in total | " + " | ".join(f"{statistics.median([d['kin_food'] for d in dd[a]]):.1f}" if dd[a] else "–" for a in "ab") + " |")
    w("| a close kin within sight held two weeks or more | " + " | ".join(pct(sum(1 for d in dd[a] if d['kin_rich_near']), len(dd[a])) for a in "ab") + " |")
    w("| had received a gift in the four weeks before | " + " | ".join(pct(sum(1 for d in dd[a] if d['gift_4w']), len(dd[a])) for a in "ab") + " |")

    w("\n## Q3. Does help reach the hungry in time? (adults going short in a winter week)\n")
    w("| own food band | arm | short-weeks | received a gift in the next two weeks | died within 4 weeks: with a gift | without |")
    w("|---|---|---|---|---|---|")
    for b in BANDS:
        for a in "ab":
            sr = [x for s in SEEDS for x in D[(a, s)]["short_rows"] if x[0] == b]
            got = [x for x in sr if x[1]]
            no = [x for x in sr if not x[1]]
            w(f"| {b} | {a.upper()} | {len(sr):,} | {pct(len(got), len(sr))} | {pct(sum(x[2] for x in got), len(got), 2)} | "
              f"{pct(sum(x[2] for x in no), len(no), 2)} |")

    w("\n## Q4. What does giving cost the giver? (adult winter-weeks; went short within the next 4 weeks)\n")
    w("| own food band | arm | weeks they gave | short after giving | weeks they did not give | short after not giving |")
    w("|---|---|---|---|---|---|")
    for b in BANDS:
        for a in "ab":
            gr = [x for s in SEEDS for x in D[(a, s)]["give_rows"] if x[0] == b]
            gv = [x for x in gr if x[1]]
            ng = [x for x in gr if not x[1]]
            w(f"| {b} | {a.upper()} | {len(gv):,} | {pct(sum(x[2] for x in gv), len(gv))} | {len(ng):,} | "
              f"{pct(sum(x[2] for x in ng), len(ng))} |")

    w("\n## Q5. More sharing, better winters? (B against A, per world)\n")
    for label, f in (("share of person-winters going short", lambda r: sum(x["short"] for x in r["rows"]) / len(r["rows"]) if r["rows"] else None),
                     ("winter starvation deaths per person-winter", lambda r: sum(x["died"] for x in r["rows"]) / len(r["rows"]) if r["rows"] else None)):
        up = down = 0
        for s in SEEDS:
            x, y = f(D[("a", s)]), f(D[("b", s)])
            if x is None or y is None:
                continue
            up += y > x
            down += y < x
        pooled = {a: [r for s in SEEDS for r in D[(a, s)]["rows"]] for a in "ab"}
        key = "short" if "short" in label else "died"
        w(f"- {label}: A {pct(sum(r[key] for r in pooled['a']), len(pooled['a']), 2)}, B {pct(sum(r[key] for r in pooled['b']), len(pooled['b']), 2)}; "
          f"B higher in {up} worlds, lower in {down}.")

    (HERE / "findings_tables.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
