"""E13R analysis in the binding order (E13R_preregistration.md §5): validity and route; the replication headline; the
source test; manipulation check, neighbours, planners, carers; children's winter starvation last (gated). Written
before any outcome arm had run. Writes results.md.

  python experiments/E13R_replication/analyse_e13r.py
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
SEEDS = tuple(range(501, 517))
ARMS = ("a", "b", "n", "p")


def load(p):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def f(v, d=3):
    return "–" if v is None else f"{v:.{d}f}"


def main():
    L = []
    w = L.append
    w("# E13R — Replicating E13 with a safeguard that can be measured · Results\n")
    w("Base world A2-full (E9 code, anticipation 1.0). Arms: A control; B any better-fed model (E13's B2); S sham; N models "
      "holding under 80; P models holding 80+. Seeds 501–516, 120 years. Frozen as `E13R-frozen` before any code.\n")

    w("## Validity and route (hard stop)\n")
    if (OUT / "STOPPED.txt").exists():
        w("**" + (OUT / "STOPPED.txt").read_text(encoding="utf-8").strip() + "**\n")
        w(((OUT / "checks.txt").read_text(encoding="utf-8") if (OUT / "checks.txt").exists() else ""))
        return finish(L)
    chk = (OUT / "checks.txt").read_text(encoding="utf-8") if (OUT / "checks.txt").exists() else ""
    R = {(a, s): load(OUT / f"{a}_seed_{s}.json") for a in ARMS for s in SEEDS}
    checks = [("V1 probe read-only (both codes)", chk.count("READ-ONLY") >= 2 and "CHANGES THE WORLD" not in chk),
              ("L2 instrumented check: only the observer's forage habit changes", "PASS" in chk.split("L2 ")[-1].split("\n")[0] if "L2 " in chk else False),
              ("L1 sham = control, V2 zero = control, V3 code unchanged (all seeds)", "L1/V2/V3: PASS" in chk),
              ("All outcome runs finished", all(R.values())),
              ("Code unchanged during outcome runs", all(r and r["code_hash"] == r["code_hash_after"] for r in R.values()))]
    for n, ok in checks:
        w(f"- {n}: **{'yes' if ok else 'NO'}**")
    valid = all(ok for _, ok in checks)
    w("\n```\n" + chk.strip() + "\n```\n")
    if not valid:
        w("**Not valid. Outcomes are not read.**")
        return finish(L)

    rows = {a: [x for s in SEEDS for x in R[(a, s)]["rows"]] for a in ARMS}
    st = {}
    for a in ARMS:
        nb = [v for s in SEEDS for v in R[(a, s)]["neighbour_forage_next"]]
        cr = [x for s in SEEDS for x in R[(a, s)]["child_rows"]]
        known = [x for x in cr if x["carer_food"] is not None]
        habit = {s: statistics.mean(R[(a, s)]["habit"]) if R[(a, s)]["habit"] else None for s in SEEDS}
        hv = [v for v in habit.values() if v is not None]
        st[a] = dict(planners=sum(1 for x in rows[a] if x["planned"]), n=len(rows[a]),
                     again=sum(R[(a, s)]["planned_again"] for s in SEEDS),
                     nb=statistics.mean(nb) if nb else None, nnb=len(nb), habit=habit,
                     habit_pooled=statistics.mean(hv) if hv else None,
                     c20=sum(1 for x in known if x["carer_food"] >= 20) / len(known) if known else None,
                     cs=sum(x["starved"] for x in cr) / len(cr) if cr else None,
                     updates=sum(R[(a, s)]["updates_total"] for s in SEEDS),
                     extinct=sum(1 for s in SEEDS if len(R[(a, s)]["pops"]) < 12 or R[(a, s)]["pops"][-1] == 0))
        st[a]["share"] = st[a]["again"] / st[a]["planners"] if st[a]["planners"] else None
    A_, B = st["a"], st["b"]

    w("## Headline: does preparation survive success? (R1)\n")
    w("| arm | planner-autumns | followed by planning the next autumn | share |")
    w("|---|---|---|---|")
    for a in ARMS:
        x = st[a]
        w(f"| {a.upper()} | {x['planners']} of {x['n']} | {x['again']} | {f(100 * x['share'], 1) if x['share'] is not None else '–'}% |")
    if B["planners"] < 20:
        r1 = None
        w(f"\n**R1 unscorable:** {B['planners']} planner-autumns in B, minimum 20.")
    else:
        r1 = B["share"] >= 0.03 and B["share"] >= 3 * (A_["share"] or 0)
        w(f"\n**R1 {'confirmed' if r1 else 'wrong'}:** B {100 * B['share']:.1f}% against A {100 * (A_['share'] or 0):.1f}% "
          f"(needs at least 3% and at least 3× A, with 20+ planner-autumns).")
    w("")

    n2 = sum(1 for s in SEEDS if B["habit"][s] is not None and A_["habit"][s] is not None and B["habit"][s] > A_["habit"][s])
    r2 = n2 >= 12
    r3v = B["planners"] / A_["planners"] if A_["planners"] else None
    r3 = r3v is not None and r3v >= 2
    d4 = 100 * (B["c20"] - A_["c20"]) if B["c20"] is not None and A_["c20"] is not None else None
    r4 = d4 is not None and d4 >= 5
    r5v = B["nb"] / A_["nb"] if B["nb"] and A_["nb"] else None
    r5 = r5v is not None and r5v >= 1.1

    w("## Source: planners, or anyone better fed?\n")
    if not (r2 and r3):
        w("**Not read:** B's effect did not replicate (R2 and R3 must both hold).\n")
        src = None
    else:
        def share(key, arm):
            d = st["b"][key] - st["a"][key]
            return (st[arm][key] - st["a"][key]) / d if d else None
        w("| measure | A | B | N | P | share kept by N | share kept by P |")
        w("|---|---|---|---|---|---|---|")
        cats = []
        for key, label, fmt in (("planners", "planner-autumns", lambda v: str(v)), ("habit_pooled", "habit value", f)):
            sn, sp = share(key, "n"), share(key, "p")
            w(f"| {label} | " + " | ".join(fmt(st[a][key]) for a in ARMS) + f" | {f(sn, 2)} | {f(sp, 2)} |")
            cats.append(("both" if sn >= 0.5 and sp >= 0.5 else "N" if sn >= 0.5 else "P" if sp >= 0.5 else "neither")
                        if sn is not None and sp is not None else None)
        reading = {"N": "a general \"forage while things are good\" habit, learned from anyone better fed, carries the effect",
                   "P": "learning from planners carries it: a preparation practice spreading",
                   "both": "either source is enough", "neither": "it takes the mix; no single source"}
        w("")
        if cats[0] == cats[1] and cats[0]:
            src = cats[0]
            w(f"**Both measures agree: {src}. Reading: {reading[src]}.**")
        else:
            src = "mixed"
            w(f"**The two measures disagree** (planner-autumns: {cats[0]}; habit value: {cats[1]}). Reported as mixed.")
        w("\nCopying updates per arm (the dose caution): " + ", ".join(f"{a.upper()} {st[a]['updates']:,}" for a in ("b", "n", "p"))
          + ". Extra planner-autumns over A per 1,000 updates: "
          + ", ".join(f"{a.upper()} {f(1000 * (st[a]['planners'] - A_['planners']) / st[a]['updates'], 2) if st[a]['updates'] else '–'}"
                      for a in ("b", "n", "p")) + ".")
        w("\nPriors: creator N 65%, both 20%, P 15%; assistant N 60%, both 25%, P 15%.\n")

    w("## The rest of the chain\n")
    w("| measure | A | B | N | P |")
    w("|---|---|---|---|---|")
    w("| habit value, seeds where higher than A | – | " + " | ".join(
        str(sum(1 for s in SEEDS if st[a]["habit"][s] is not None and A_["habit"][s] is not None and st[a]["habit"][s] > A_["habit"][s]))
        + " of 16" for a in ("b", "n", "p")) + " |")
    w("| habit value, mean over seeds | " + " | ".join(f(st[a]["habit_pooled"]) for a in ARMS) + " |")
    w("| planners' neighbours, autumn foraging the next year | " + " | ".join(f"{f(st[a]['nb'])} (n={st[a]['nnb']})" for a in ARMS) + " |")
    w("| child-winters whose carer holds 20+ | " + " | ".join(f"{100 * st[a]['c20']:.1f}%" for a in ARMS) + " |")
    w("| children's winter starvation per child-winter | " + " | ".join(f"{100 * st[a]['cs']:.2f}%" for a in ARMS) + " |")
    w("| worlds that died out | " + " | ".join(str(st[a]["extinct"]) for a in ARMS) + " |")
    w("")

    w("## Frozen predictions (Arm B against Arm A), scored\n")

    def sc(ok):
        return "**unscorable**" if ok is None else "**confirmed**" if ok else "**wrong**"
    w(f"1. {sc(r1)} — headline: repeat planning {f(100 * B['share'], 1) if B['share'] is not None else '–'}% against "
      f"{f(100 * A_['share'], 1) if A_['share'] is not None else '–'}%.")
    w(f"2. {sc(r2)} — manipulation check: habit value higher than A in {n2} of 16 seeds (needs 12).")
    w(f"3. {sc(r3)} — planner-autumns B ÷ A: {f(r3v, 2)} (needs 2).")
    w(f"4. {sc(r4)} — carers with 20+: {f(d4, 1)} points (needs +5).")
    w(f"5. {sc(r5)} — planners' neighbours' foraging B ÷ A: {f(r5v, 2)} (needs 1.1).")
    gate = r2 and r3 and r4
    r6v = B["cs"] / A_["cs"] if A_["cs"] else None
    w(f"6. {sc((r6v is not None and r6v <= 0.8) if gate else False)} — children's winter starvation B ÷ A: {f(r6v, 2)}"
      + ("" if gate else " (not interpreted: R2, R3 and R4 did not all hold)") + ".")

    w("\n## Descriptive (reported, not scored)\n")
    b_kinds = [k for s in SEEDS for k in R[("b", s)]["update_kinds"]]
    tot = sum(k[3] for k in b_kinds) or 1
    by_food = {lvl: sum(k[3] for k in b_kinds if k[0] == lvl) for lvl in range(4)}
    by_season = {se: sum(k[3] for k in b_kinds if k[1] == se) for se in range(4)}
    big = sum(k[3] for k in b_kinds if k[2])
    w("Arm B copying updates by the model's food level (0 = under half a week … 3 = 6+ weeks): "
      + ", ".join(f"{lvl}: {100 * v / tot:.0f}%" for lvl, v in by_food.items())
      + "; by season (spring, summer, autumn, winter): " + ", ".join(f"{100 * v / tot:.0f}%" for v in by_season.values())
      + f"; from models holding 80+: {100 * big / tot:.1f}%.\n")
    dose = [d for s in SEEDS for d in R[("b", s)]["dose"]]
    bins = ((0, 0), (1, 9), (10, 49), (50, 199), (200, 10 ** 9))
    w("Dose-response in B (adult samples every 10 years): " + "; ".join(
        f"{lo}–{hi if hi < 10 ** 9 else '…'} updates: habit {f(statistics.mean([h for u, h in dose if lo <= u <= hi]))} "
        f"(n={sum(1 for u, _ in dose if lo <= u <= hi)})" for lo, hi in bins if any(lo <= u <= hi for u, _ in dose)) + ".\n")
    for label, cond in (("learned from a model holding 80+ that autumn", lambda x: x["from_planner"] > 0),
                        ("did not", lambda x: x["from_planner"] == 0)):
        g = ag = 0
        for s in SEEDS:                       # ids are unique within a world only
            rs = R[("b", s)]["rows"]
            planned = {(x["pid"], x["year"]) for x in rs if x["planned"]}
            for x in rs:
                if x["planned"] and cond(x):
                    g += 1
                    ag += (x["pid"], x["year"] + 1) in planned
        w(f"- B planner-autumns whose planner {label}: {g}, followed by planning: {ag} "
          f"({f(100 * ag / g, 1) if g else '–'}%)")
    return finish(L)


def finish(L):
    (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
