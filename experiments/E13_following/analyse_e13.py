"""E13 analysis in the binding order (E13_preregistration.md §6): validity, leak test, repeat planning (headline),
manipulation check, neighbours, planners, carers, then children's deaths (gated). Written before any result. Writes results.md."""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
E9 = HERE.parent / "E9_anticipation" / "output"
SEEDS = (301, 302, 303, 304)
ARMS = ("a", "b", "c")


def load(p):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def f(v, d=3):
    return "–" if v is None else f"{v:.{d}f}"


def main():
    R = {(a, s): load(OUT / f"{a}_seed_{s}.json") for a in ARMS for s in SEEDS}
    zero = load(OUT / "zero_seed_304.json")
    L = []
    w = L.append
    w("# E13 — Following those who visibly do well (B2) · Results\n")
    w("Base world A2-full (E9 code, anticipation 1.0). Arm A control; Arm B follows the best-fed visible adult; Arm C the "
      "same among adults whose children all live. Seeds 301–304, 120 years. Frozen as `E13-frozen` before any code.\n")
    w("## Validity\n")
    v = (OUT / "verify.txt").read_text(encoding="utf-8").strip().splitlines() if (OUT / "verify.txt").exists() else []
    done = all(R.values()) and zero is not None
    checks = [("Probe read-only (both codes)", len(v) >= 2 and all("READ-ONLY" in x for x in v)),
              ("All runs finished", done),
              ("Zero check: E13 code with B2 off reproduces E9 A2-full (seed 304)", done and zero["matches_e9_a2full"]),
              ("Arm A reproduces E9 A2-full (all seeds)", done and all(R[("a", s)]["matches_e9_a2full"] for s in SEEDS)),
              ("Code unchanged during runs", done and all(r["code_hash"] == r["code_hash_after"] for r in [*R.values(), zero]))]
    for n, ok in checks:
        w(f"- {n}: **{'yes' if ok else 'NO'}**")
    valid = all(ok for _, ok in checks)
    w(f"- **{'Valid' if valid else 'INVALID or incomplete'}.**\n")
    if not done:
        print("\n".join(L)); return

    rows = {a: [x for s in SEEDS for x in R[(a, s)]["rows"]] for a in ARMS}

    def share(rs):
        return (sum(x["forage_share"] for x in rs) / len(rs), len(rs)) if rs else (None, 0)

    w("## Leak test (hard fail)\n")
    base = share([x for x in rows["a"] if not x["ever_observed"]])
    leak = {}
    for a in ("b", "c"):
        m = share([x for x in rows[a] if not x["ever_observed"]])
        leak[a] = m[0] / base[0] if m[0] is not None and base[0] else None
        w(f"- Arm {a.upper()}: {f(m[0])} (n={m[1]}) vs Arm A {f(base[0])} (n={base[1]}) → {f(leak[a])}")
    leak_ok = all(x is not None and 0.9 <= x <= 1.1 for x in leak.values())
    w(f"\n**Leak test {'passed' if leak_ok else 'FAILED'}.** (Most adults see a better-fed neighbour forage at some point, so this group is small.)\n")

    st = {}
    for a in ARMS:
        planners = sum(1 for x in rows[a] if x["planned"])
        again = sum(R[(a, s)]["planned_again"] for s in SEEDS)
        nb = [v for s in SEEDS for v in R[(a, s)]["neighbour_forage_next"]]
        habit = {s: statistics.mean(R[(a, s)]["habit"]) if R[(a, s)]["habit"] else None for s in SEEDS}
        cr = [x for s in SEEDS for x in R[(a, s)]["child_rows"]]
        known = [x for x in cr if x["carer_food"] is not None]
        st[a] = dict(planners=planners, n=len(rows[a]), again=again, nb=statistics.mean(nb) if nb else None, nnb=len(nb),
                     habit=habit, c20=sum(1 for x in known if x["carer_food"] >= 20) / len(known) if known else None,
                     cs=sum(x["starved"] for x in cr) / len(cr) if cr else None)

    w("## Headline: does preparation survive success?\n")
    w("| arm | planner-autumns | followed by planning the next autumn | share |")
    w("|---|---|---|---|")
    for a in ARMS:
        x = st[a]
        w(f"| {a.upper()} | {x['planners']} of {x['n']} | {x['again']} | {f(100 * x['again'] / x['planners'], 1) if x['planners'] else '–'}% |")
    w("")
    w("## The rest of the chain\n")
    w("| measure | A | B | C |")
    w("|---|---|---|---|")
    w("| habit value, autumn foraging while stocked (mean of 10-year samples; seeds 301/302/303/304) | "
      + " | ".join(" / ".join(f(st[a]["habit"][s]) for s in SEEDS) for a in ARMS) + " |")
    w("| planners' neighbours, autumn foraging the next year | " + " | ".join(f"{f(st[a]['nb'])} (n={st[a]['nnb']})" for a in ARMS) + " |")
    w("| planner-autumns | " + " | ".join(str(st[a]["planners"]) for a in ARMS) + " |")
    w("| child-winters whose carer holds 20+ | " + " | ".join(f"{100 * st[a]['c20']:.1f}%" for a in ARMS) + " |")
    w("| children's winter starvation per child-winter | " + " | ".join(f"{100 * st[a]['cs']:.2f}%" for a in ARMS) + " |")
    w("")

    w("## Frozen predictions (Arm B), scored\n")

    def sc(ok):
        return "**confirmed**" if ok else "**wrong**"
    b, a0 = st["b"], st["a"]
    p1 = b["again"] / b["planners"] if b["planners"] else 0
    w(f"1. {sc(b['planners'] >= 20 and p1 >= 0.10)} — headline: {b['again']} of {b['planners']} planner-autumns followed by planning "
      f"({100 * p1:.1f}%; needs ≥ 10% with ≥ 20; Arm A {a0['again']} of {a0['planners']}).")
    n2 = sum(1 for s in SEEDS if b["habit"][s] is not None and a0["habit"][s] is not None and b["habit"][s] > a0["habit"][s])
    w(f"2. {sc(n2 >= 3)} — manipulation check: habit value higher than Arm A in {n2} of 4 seeds.")
    r3 = b["nb"] / a0["nb"] if b["nb"] and a0["nb"] else None
    w(f"3. {sc(r3 is not None and r3 >= 1.1)} — planners' neighbours' foraging, B ÷ A: {f(r3, 2)} (needs ≥ 1.1).")
    r4 = b["planners"] / a0["planners"] if a0["planners"] else None
    w(f"4. {sc(r4 is not None and r4 >= 2)} — planner-autumns, B ÷ A: {f(r4, 2)} (needs ≥ 2).")
    d5 = 100 * (b["c20"] - a0["c20"])
    w(f"5. {sc(d5 >= 5)} — carers with 20+: {d5:+.1f} points (needs ≥ +5).")
    r6 = b["cs"] / a0["cs"] if a0["cs"] else None
    gate = n2 >= 3 and r4 is not None and r4 >= 2 and d5 >= 5
    w(f"6. {sc(gate and r6 is not None and r6 <= 0.8)} — children's winter starvation, B ÷ A: {f(r6, 2)}"
      + ("" if gate else " (not interpreted: predictions 2, 4 and 5 did not all hold)") + ".")
    w(f"7. {sc(leak_ok)} — leak test.")
    w("\nArm C against Arm B is reported above, with no directional prediction.")
    if not valid:
        w("\n**Not valid: predictions recorded, not interpreted.**")
    elif not leak_ok:
        w("\n**The leak test failed: E13 is declared failed whatever its other results.**")
    (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
