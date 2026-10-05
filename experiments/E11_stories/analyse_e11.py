"""E11 analysis in the creator's binding chain order (E11_preregistration.md §6), predictions scored as frozen.
Written before any E11 result was seen. Writes results.md."""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
E10 = HERE.parent / "E10_loss" / "output"
SEEDS = (301, 302, 303, 304)
ARMS = ("arm0", "s1low", "s1high")


def load(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def f(v, d=3):
    return "–" if v is None else f"{v:.{d}f}"


def fshare(rs):
    return (sum(x["forage_share"] for x in rs) / len(rs), len(rs)) if rs else (None, 0)


def main():
    R = {(a, s): load(OUT / f"{a}_seed_{s}.json") for a in ARMS for s in SEEDS}
    zero = load(OUT / "zero_seed_304.json")
    e10o2 = load(E10 / "o2_seed_304.json")
    L = []
    w = L.append
    w("# E11 — Stories that carry a hard season (S1) · Results\n")
    w("Arm 0 = E7 code; S1-low and S1-high = E11 code (O2 on, story 0.25 / 0.50). Seeds 301–304, 120 years. Frozen "
      "as `E11-frozen` before any code. Read in the creator's chain order; deaths last.\n")
    w("## Validity\n")
    v = (OUT / "verify.txt").read_text(encoding="utf-8").strip().splitlines() if (OUT / "verify.txt").exists() else []
    done = all(R.values()) and zero is not None
    checks = [("Probe read-only (both codes)", len(v) >= 2 and all("READ-ONLY" in x for x in v)),
              ("All runs finished", done),
              ("Zero-story E11 code reproduces E10's O2 arm (seed 304)", done and e10o2 is not None and zero["pops"] == e10o2["pops"]),
              ("Arm 0 reproduces the saved E7 runs", done and all(R[("arm0", s)]["matches_saved_e7"] for s in SEEDS)),
              ("Code unchanged during runs", done and all(r["code_hash"] == r["code_hash_after"] for r in [*R.values(), zero]))]
    for n, ok in checks:
        w(f"- {n}: **{'yes' if ok else 'NO'}**")
    valid = all(ok for _, ok in checks)
    w(f"- **{'Valid' if valid else 'INVALID or incomplete'}.**\n")
    if not done:
        print("\n".join(L)); return

    rows = {a: [x for s in SEEDS for x in R[(a, s)]["rows"]] for a in ARMS}
    w("## Leak test (hard fail)\n")
    free = lambda x: not x["ever_bereaved"] and not x["ever_heard"]
    b0 = fshare([x for x in rows["arm0"] if free(x)])
    leak = {}
    for a in ("s1low", "s1high"):
        m = fshare([x for x in rows[a] if free(x)])
        leak[a] = m[0] / b0[0] if m[0] is not None and b0[0] else None
        w(f"- {a}: {f(m[0])} (n={m[1]}) vs Arm 0 {f(b0[0])} (n={b0[1]}) → {f(leak[a])}")
    leak_ok = all(x is not None and 0.9 <= x <= 1.1 for x in leak.values())
    w(f"\n**Leak test {'passed' if leak_ok else 'FAILED'}.** (Few adults never hear such a story, so this group is small.)\n")

    w("## The chain, in order\n")
    w("| step | measure | Arm 0 | S1-low | S1-high |")
    w("|---|---|---|---|---|")
    st = {}
    for a in ARMS:
        cs = [R[(a, s)]["story_counts"] for s in SEEDS]
        hd = sum(v for s in SEEDS for k, v in R[(a, s)]["deaths"].items() if k.startswith("starvation@"))
        told = sum(c.get("told", 0) for c in cs)
        heard = sum(c.get("heard", 0) for c in cs)
        lis = fshare([x for x in rows[a] if x["heard_recent"] and not x["ever_bereaved"]])
        planned = sum(1 for x in rows[a] if x["planned"])
        again = sum(R[(a, s)]["planned_again"] for s in SEEDS)
        cr = [x for s in SEEDS for x in R[(a, s)]["child_rows"]]
        known = [x for x in cr if x["carer_food"] is not None]
        c20 = sum(1 for x in known if x["carer_food"] >= 20) / len(known) if known else None
        cstarv = sum(x["starved"] for x in cr) / len(cr) if cr else None
        st[a] = dict(hd=hd, told=told, heard=heard, lis=lis[0], nlis=lis[1], planned=planned, n=len(rows[a]),
                     again=again, c20=c20, cs=cstarv, entry=statistics.median([x["entry"] for x in rows[a]]),
                     carriers=sum(R[(a, s)]["carriers_made"] for s in SEEDS))
    lines = [("1", "starvation deaths", "hd", "{}"), ("2", "tellings of hunger-death stories", "told", "{}"),
             ("3", "hearings accepted or recognised", "heard", "{}"),
             ("4", "autumn foraging, heard a hunger story in the past year, never bereaved", "lis", "{:.3f}"),
             ("5", "adult-autumns holding 80+ (planners)", "planned", "{}"),
             ("6", "planner-autumns followed by planning the next autumn", "again", "{}")]
    for step, name, key, fmt in lines:
        w(f"| {step} | {name} | " + " | ".join(fmt.format(st[a][key]) if st[a][key] is not None else "–" for a in ARMS) + " |")
    w(f"| – | median food entering winter | " + " | ".join(f"{st[a]['entry']:.1f}" for a in ARMS) + " |")
    w(f"| – | carriers made | " + " | ".join(str(st[a]['carriers']) for a in ARMS) + " |")
    w(f"| 7 | child-winters whose carer holds 20+ | " + " | ".join(f"{100 * st[a]['c20']:.1f}%" for a in ARMS) + " |")
    w(f"| 7 | children's winter starvation per child-winter | " + " | ".join(f"{100 * st[a]['cs']:.2f}%" for a in ARMS) + " |")
    w("")

    w("## Frozen predictions, scored\n")

    def sc(ok):
        return "**confirmed**" if ok else "**wrong**"
    r1 = st["s1high"]["lis"] / st["arm0"]["lis"] if st["s1high"]["lis"] and st["arm0"]["lis"] else None
    w(f"1. {sc(r1 is not None and r1 >= 1.2)} — listeners' autumn foraging, S1-high ÷ Arm 0: {f(r1, 2)} (needs ≥ 1.2).")
    p2 = st["s1high"]["planned"] / st["s1high"]["n"]
    w(f"2. {sc(p2 >= 0.01)} — S1-high planners: {st['s1high']['planned']} of {st['s1high']['n']} ({100 * p2:.2f}%; needs ≥ 1%).")
    p3 = st["s1high"]["again"] / st["s1high"]["planned"] if st["s1high"]["planned"] else 0
    w(f"3. {sc(st['s1high']['planned'] >= 20 and p3 >= 0.10)} — headline: planner-autumns followed by planning again, "
      f"S1-high: {st['s1high']['again']} of {st['s1high']['planned']} ({100 * p3:.1f}%; needs ≥ 10% with ≥ 20 planners; E9.3: 1 of 113).")
    rl = st["s1low"]["lis"] / st["arm0"]["lis"] if st["s1low"]["lis"] and st["arm0"]["lis"] else None
    ok4 = rl is not None and r1 is not None and rl < r1 and st["s1low"]["planned"] / st["s1low"]["n"] < p2
    w(f"4. {sc(ok4)} — dose response: listeners low {f(rl, 2)} vs high {f(r1, 2)}; planners low "
      f"{100 * st['s1low']['planned'] / st['s1low']['n']:.2f}% vs high {100 * p2:.2f}%.")
    d5 = 100 * (st["s1high"]["c20"] - st["arm0"]["c20"])
    w(f"5. {sc(d5 >= 5)} — carers with 20+: {d5:+.1f} points (needs ≥ +5).")
    r6 = st["s1high"]["cs"] / st["arm0"]["cs"] if st["arm0"]["cs"] else None
    gate = (r1 is not None and r1 >= 1.2) and p2 >= 0.01 and d5 >= 5
    w(f"6. {sc(gate and r6 is not None and r6 <= 0.8)} — children's winter starvation S1-high ÷ Arm 0: {f(r6, 2)}"
      + ("" if gate else " (not interpreted: predictions 1, 2 and 5 did not all hold, so the chain does not reach step 7)") + ".")
    w(f"7. {sc(leak_ok)} — leak test.")
    if not valid:
        w("\n**Not valid: predictions recorded, not interpreted.**")
    elif not leak_ok:
        w("\n**The leak test failed: E11 is declared failed whatever its other results.**")
    (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
