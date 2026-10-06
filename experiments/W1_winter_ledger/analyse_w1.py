"""W1 tables (questions.md), written before the W1 data existed. Writes findings_tables.md.

  python experiments/W1_winter_ledger/analyse_w1.py
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
SEEDS = tuple(range(501, 517))
SEASONS = ("spring", "summer", "autumn", "winter")


def weeks(stock, need, rate):
    w = 0
    while w < 60:
        stock = stock * (1 - rate) - need
        if stock < 0:
            return w + max(0.0, (stock + need) / need)
        w += 1
    return w


def med(xs, d=1):
    xs = [x for x in xs if x is not None]
    return f"{statistics.median(xs):.{d}f}" if xs else "–"


def pct(a, b, d=1):
    return f"{100 * a / b:.{d}f}%" if b else "–"


def main():
    D = {(a, s): json.loads((OUT / f"{a}_seed_{s}.json").read_text(encoding="utf-8")) for a in "ab" for s in SEEDS}
    L = []
    w = L.append
    w("# W1 — The winter ledger: tables\n")
    v = (OUT / "verify.txt").read_text(encoding="utf-8").strip()
    rep = all(r["replay_matches"] for r in D.values())
    w(f"Exactness:\n```\n{v}\n```\nReplays match the saved E13R runs in all 32: **{'yes' if rep else 'NO'}**.\n")

    def F(a, s, key):
        return sum(D[(a, x)]["flows"].get(str(s), {}).get(key, 0.0) for x in SEEDS)

    def agree(f):
        up = down = 0
        for x in SEEDS:
            p, q = f("a", x), f("b", x)
            if p is None or q is None:
                continue
            up += q > p
            down += q < p
        return f"B higher in {up}, lower in {down}"

    w("## Q1. The arithmetic ceiling (rules only)\n")
    w("| stored as | one adult, carrying 100 | carer + 2 children (15 a week), carrying 100 |")
    w("|---|---|---|")
    for label, rate in (("loose food", 0.04), ("fired or smoked food", 0.01), ("seeds", 0.005)):
        w(f"| {label} | {weeks(100, 7, rate):.1f} weeks | {weeks(100, 15, rate):.1f} weeks |")
    w("\nWinter is 13 weeks: an adult needs 91, a carer with two children 195, with three 247.\n")

    w("## Q2. The winter ledger (all worlds, all winters)\n")
    w("| flow in winter | A | B |")
    w("|---|---|---|")
    keys = [("eaten", "eaten"), ("need", "needed (full rations)"), ("gathered_forage", "gathered by foraging"),
            ("gathered_hunt", "gathered by hunting"), ("rot_body", "rotted on people"), ("rot_stash", "rotted in stashes"),
            ("put_stash", "put into stashes"), ("taken_own", "taken back from own stash"),
            ("taken_other", "taken from others' stashes"), ("given", "given to others"), ("stolen", "stolen"),
            ("fed_dependents", "fed to dependents"), ("inherited", "inherited"), ("put_ground", "sown or left on the ground")]
    for k, label in keys:
        w(f"| {label} | {F('a', 3, k):,.0f} | {F('b', 3, k):,.0f} |")
    for a in "ab":
        held = sum(x["held"] + x["stash"] for s in SEEDS for x in D[(a, s)]["winters"])
        eaten = F(a, 3, "eaten")
        gathered = F(a, 3, "gathered_forage") + F(a, 3, "gathered_hunt")
        w(f"\n**{a.upper()}:** food held at the start of winters (people and stashes) {held:,.0f}; eaten in winter "
          f"{eaten:,.0f}; gathered in winter {gathered:,.0f}. Gathered ÷ eaten {gathered / eaten:.2f}; held at start ÷ "
          f"eaten {held / eaten:.2f}; eaten ÷ needed {eaten / F(a, 3, 'need'):.3f}.")
    w("\n" + "Winter gathered ÷ eaten, per seed: " + agree(
        lambda a, x: (D[(a, x)]["flows"].get("3", {}).get("gathered_forage", 0) / D[(a, x)]["flows"]["3"]["eaten"])
        if D[(a, x)]["flows"].get("3", {}).get("eaten") else None) + ".")

    w("\n### By season (A)\n")
    w("| season | gathered | eaten | gathered ÷ eaten | rotted on people | put into stashes |")
    w("|---|---|---|---|---|---|")
    for i, name in enumerate(SEASONS):
        g = F("a", i, "gathered_forage") + F("a", i, "gathered_hunt")
        e = F("a", i, "eaten")
        w(f"| {name} | {g:,.0f} | {e:,.0f} | {g / e:.2f} | {F('a', i, 'rot_body'):,.0f} | {F('a', i, 'put_stash'):,.0f} |")

    w("\n## Q3. Households at the start of winter\n")
    w("| | A | B |")
    w("|---|---|---|")
    H = {a: [h for s in SEEDS for h in D[(a, s)]["households"]] for a in "ab"}
    w(f"| carer-winters | {len(H['a'])} | {len(H['b'])} |")
    w("| median stock (carer, dependents, own stashes) | " + " | ".join(med([h["stock"] for h in H[a]]) for a in "ab") + " |")
    w("| median winter need | " + " | ".join(med([h["need"] for h in H[a]]) for a in "ab") + " |")
    w("| median stock ÷ need | " + " | ".join(med([h["stock"] / h["need"] for h in H[a]], 2) for a in "ab") + " |")
    for lo, hi, label in ((0, 0.1, "under a tenth"), (0.1, 0.25, "a tenth to a quarter"), (0.25, 0.5, "a quarter to a half"),
                          (0.5, 1.0, "a half to all"), (1.0, 1e9, "all or more")):
        w(f"| stock covers {label} of winter need | " + " | ".join(
            pct(sum(1 for h in H[a] if lo <= h["stock"] / h["need"] < hi), len(H[a])) for a in "ab") + " |")
    w("| winter need above what the carer can carry | " + " | ".join(
        pct(sum(1 for h in H[a] if h["need"] > h["carry"]), len(H[a])) for a in "ab") + " |")
    w("| any food in the carer's own stashes | " + " | ".join(
        pct(sum(1 for h in H[a] if h["own_stash"] > 0), len(H[a])) for a in "ab") + " |")

    w("\n## Q4. Rot and seeds\n")
    w("| | A | B |")
    w("|---|---|---|")
    for a_label, key in (("rotted on people in winter", "rot_body"), ("rotted in stashes in winter", "rot_stash")):
        w(f"| {a_label} ÷ eaten in winter | " + " | ".join(f"{F(a, 3, key) / F(a, 3, 'eaten'):.3f}" for a in "ab") + " |")
    w("| rotted on people, whole year ÷ gathered, whole year | " + " | ".join(
        f"{sum(F(a, i, 'rot_body') for i in range(4)) / sum(F(a, i, 'gathered_forage') + F(a, i, 'gathered_hunt') for i in range(4)):.3f}"
        for a in "ab") + " |")
    w("| seeds ÷ all food held, start of winter | " + " | ".join(
        f"{sum(x['seeds'] for s in SEEDS for x in D[(a, s)]['winters']) / sum(x['held'] for s in SEEDS for x in D[(a, s)]['winters']):.3f}"
        for a in "ab") + " |")

    w("\n## Q5. Stashes\n")
    w("| | A | B |")
    w("|---|---|---|")
    w("| put into stashes in autumn | " + " | ".join(f"{F(a, 2, 'put_stash'):,.0f}" for a in "ab") + " |")
    w("| in stashes at the start of winter, mean per winter per world | " + " | ".join(
        f"{statistics.mean([x['stash'] for s in SEEDS for x in D[(a, s)]['winters']]):.1f}" for a in "ab") + " |")
    w("| food held by people at the start of winter, mean per winter per world | " + " | ".join(
        f"{statistics.mean([x['held'] for s in SEEDS for x in D[(a, s)]['winters']]):.1f}" for a in "ab") + " |")
    w("| taken back in winter by owners | " + " | ".join(f"{F(a, 3, 'taken_own'):,.0f}" for a in "ab") + " |")
    w("| taken in winter by others | " + " | ".join(f"{F(a, 3, 'taken_other'):,.0f}" for a in "ab") + " |")
    w("| rotted in stashes in winter | " + " | ".join(f"{F(a, 3, 'rot_stash'):,.0f}" for a in "ab") + " |")

    w("\n## Q6. Who runs out, and when\n")
    w("| food at the start of winter | A: went short | A: median first week | B: went short | B: median first week |")
    w("|---|---|---|---|---|")
    R = {a: [r for s in SEEDS for r in D[(a, s)]["runs_out"]] for a in "ab"}
    for lo, hi, label in ((0, 5, "under 5"), (5, 20, "5–20"), (20, 50, "20–50"), (50, 1e9, "50+")):
        cells = []
        for a in "ab":
            g = [r for r in R[a] if lo <= r[0] < hi]
            cells += [pct(sum(1 for r in g if r[1] is not None), len(g)) + f" (n={len(g)})", med([r[1] for r in g])]
        w(f"| {label} | " + " | ".join(cells) + " |")
    for role, flag in (("carers", True), ("adults without dependents", False)):
        cells = []
        for a in "ab":
            g = [r for r in R[a] if r[2] is flag]
            cells.append(pct(sum(1 for r in g if r[1] is not None), len(g)))
        w(f"\nWent short at some point in winter, {role}: A {cells[0]}, B {cells[1]}.")

    (HERE / "findings_tables.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
