"""G1 tables (questions.md), written before the G1 data existed. Writes findings_tables.md.

  python experiments/G1_who_receives/analyse_g1.py
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
SEEDS = tuple(range(501, 517))
SEASONS = ("spring", "summer", "autumn", "winter")
ORDER = {
    "tie": ["partner", "own child, young", "own child, teen", "own child, adult", "own child, elder", "parent", "sibling",
            "other kin", "friend", "acquaintance", "stranger"],
    "stage": ["infant, in giver's care", "infant, in another's care", "infant, no carer", "child, in giver's care",
              "child, in another's care", "child, no carer", "teen", "adult", "elder"],
    "hunger": ["under 0.5 weeks", "0.5–1", "1–2", "2–4", "4+ weeks"],
    "status": ["bottom quarter", "second quarter", "third quarter", "top quarter"],
    "repay": ["paying back", "not paying back"],
}
TITLES = {"tie": "Q1. To whom? (the recipient's tie to the giver)", "stage": "Q2. To which ages?",
          "hunger": "Q3. To the hungry? (recipient's food before the gift, in weeks of their own need)",
          "status": "Q4. To the high-status? (adult recipients, by the respect others hold for them)",
          "repay": "Q5b. How much is repayment?"}


def pct(a, b, d=1):
    return f"{100 * a / b:.{d}f}%" if b else "–"


def main():
    D = {s: json.loads((OUT / f"seed_{s}.json").read_text(encoding="utf-8")) for s in SEEDS}
    L = []
    w = L.append
    w("# G1 — Who receives the food: tables\n")
    v = (OUT / "verify.txt").read_text(encoding="utf-8").strip()
    rep = all(r["replay_matches"] for r in D.values())
    w(f"Probe check: {v}. Replays match the saved E13R runs in all 16: **{'yes' if rep else 'NO'}**.\n")

    def total(dim, key):
        g = f = 0.0
        for x in SEEDS:
            row = D[x]["by"].get(dim, {}).get(key)
            if row:
                g += row[0]
                f += row[1]
        return g, f

    def seeds_with(dim, key, share_min):
        """Worlds in which this label's share of food is at least share_min."""
        n = 0
        for x in SEEDS:
            rows = {k: v for k, v in D[x]["by"].get(dim, {}).items() if k.startswith("all|")}
            tot = sum(v[1] for v in rows.values())
            if tot and rows.get(key, [0, 0])[1] / tot >= share_min:
                n += 1
        return n

    for dim in ("tie", "stage", "hunger", "status", "repay"):
        w(f"## {TITLES[dim]}\n")
        w("| | gifts | food | share of food | " + " | ".join(SEASONS) + " |")
        w("|---|---|---|---|" + "---|" * 4)
        tot_food = sum(total(dim, f"all|{lab}")[1] for lab in ORDER[dim])
        season_tot = [sum(total(dim, f"{i}|{lab}")[1] for lab in ORDER[dim]) for i in range(4)]
        for lab in ORDER[dim]:
            g, f = total(dim, f"all|{lab}")
            if not g:
                continue
            w(f"| {lab} | {g:,.0f} | {f:,.0f} | {pct(f, tot_food)} | "
              + " | ".join(pct(total(dim, f"{i}|{lab}")[1], season_tot[i]) for i in range(4)) + " |")
        w("")

    w("## Q5. To the same few?\n")
    rec = sorted((a for x in SEEDS for a in D[x]["received"]), reverse=True)
    per_world = []
    for x in SEEDS:
        r = D[x]["received"]
        if r:
            k = max(1, len(r) // 10)
            per_world.append(sum(r[:k]) / sum(r))
    w(f"Recipients over the whole run: {len(rec):,}. Share of all food received that went to the top 10% of recipients, "
      f"per world: median {100 * statistics.median(per_world):.0f}% (range {100 * min(per_world):.0f}–{100 * max(per_world):.0f}%).")
    gy = [g for x in SEEDS for g in D[x]["giver_years"] if g[0] > 0]
    w(f"\nGivers in a year: {len(gy):,}. Share of a giver's yearly giving that went to their single main recipient: "
      f"median {100 * statistics.median([t / a for a, t in gy]):.0f}%; all to one person in "
      f"{pct(sum(1 for a, t in gy if t >= a - 1e-9), len(gy))} of giver-years.")
    rp = [n for x in SEEDS for n in D[x]["recipients_per_giver_year"]]
    w(f"\nDifferent recipients per giver per year: median {statistics.median(rp):.0f}, mean {statistics.mean(rp):.1f}.")

    w("\n## Seed agreement for the largest categories\n")
    for dim in ("tie", "stage"):
        shares = defaultdict(float)
        for lab in ORDER[dim]:
            shares[lab] = total(dim, f"all|{lab}")[1]
        tot = sum(shares.values())
        for lab, f in sorted(shares.items(), key=lambda kv: -kv[1])[:4]:
            w(f"- {dim}, {lab}: {pct(f, tot)} pooled; at least a fifth of all food in {seeds_with(dim, 'all|' + lab, 0.2)} of 16 worlds.")

    (HERE / "findings_tables.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
