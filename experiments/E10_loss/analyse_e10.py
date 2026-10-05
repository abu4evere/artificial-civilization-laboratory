"""E10 analysis in the binding order: validity, leak test, causal links, then deaths. Predictions scored as frozen.
Written before any E10 result was seen. Writes results.md."""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
SEEDS = (301, 302, 303, 304)
MECH = ("o2", "o3low", "o3high")
ARMS = ("arm0",) + MECH


def load(a, s):
    f = OUT / f"{a}_seed_{s}.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None


def rows(R, a, key="rows"):
    return [x for s in SEEDS for x in R[(a, s)][key]]


def fshare(rs):
    return (sum(x["forage_share"] for x in rs) / len(rs), len(rs)) if rs else (None, 0)


def f(v, d=3):
    return "–" if v is None else f"{v:.{d}f}"


def carer20(cr):
    known = [x for x in cr if x["carer_food"] is not None]
    return sum(1 for x in known if x["carer_food"] >= 20) / len(known) if known else None


def child_starv(cr):
    return sum(x["starved"] for x in cr) / len(cr) if cr else None


def main():
    R = {(a, s): load(a, s) for a in ARMS for s in SEEDS}
    zero = load("zero", 304)
    L = []
    w = L.append
    w("# E10 — The lesson of a lost child (O2) and of a death witnessed (O3) · Results\n")
    w("Arm 0 = E7 code; O2, O2+O3-low (witness 0.25), O2+O3-high (witness 0.50) = E10 code at weight 1.0. Seeds "
      "301–304, 120 years. Frozen as `E10-frozen` before any code. Order: validity, leak test, causal links, deaths.\n")
    w("## 1. Validity\n")
    v = (OUT / "verify.txt").read_text(encoding="utf-8").strip().splitlines() if (OUT / "verify.txt").exists() else []
    done = all(R.values()) and zero is not None
    checks = [("Probe read-only (both codes)", len(v) >= 2 and all("READ-ONLY" in x for x in v)),
              ("All runs finished", done),
              ("Zero-weight E10 code reproduces Arm 0 (seed 304)", done and zero["pops"] == R[("arm0", 304)]["pops"]),
              ("Arm 0 reproduces the saved E7 runs", done and all(R[("arm0", s)]["matches_saved_e7"] for s in SEEDS)),
              ("Code unchanged during runs", done and all(r["code_hash"] == r["code_hash_after"] for r in [*R.values(), zero]))]
    for n, ok in checks:
        w(f"- {n}: **{'yes' if ok else 'NO'}**")
    valid = all(ok for _, ok in checks)
    w(f"- **{'Valid' if valid else 'INVALID or incomplete'}.**\n")
    if not done:
        print("\n".join(L)); return

    w("## 2. Leak test (hard fail)\n")
    w("Autumn foraging share of adults with no lesson: never bereaved (O2), and also never a witness (O2+O3 arms); "
      "compared with the same group in Arm 0.\n")
    a0 = rows(R, "arm0")
    leak = {}
    for a in MECH:
        free = (lambda x: not x["ever_bereaved"]) if a == "o2" else (lambda x: not x["ever_bereaved"] and not x["ever_witnessed"])
        m, n = fshare([x for x in rows(R, a) if free(x)])
        b, nb = fshare([x for x in a0 if free(x)])
        leak[a] = m / b if m is not None and b else None
        w(f"- {a}: {f(m)} (n={n}) vs Arm 0 {f(b)} (n={nb}) → ratio {f(leak[a])}")
    leak_ok = all(r is not None and 0.9 <= r <= 1.1 for r in leak.values())
    w(f"\n**Leak test {'passed' if leak_ok else 'FAILED'}.**\n")

    w("## 3. Causal links\n")
    w("| arm | bereaved, first autumn after (forage share, n) | witnesses with children, first autumn after | median winter entry | child-winters with carer ≥ 20 food | adult-autumns reaching 80 | carriers made |")
    w("|---|---|---|---|---|---|---|")
    st = {}
    for a in ARMS:
        rs = rows(R, a)
        cr = rows(R, a, "child_rows")
        b = fshare([x for x in rs if x["bereaved_recent"]])
        wt = fshare([x for x in rs if x["witnessed_recent"] and x["has_children"] and not x["bereaved_recent"]])
        entry = statistics.median([x["entry"] for x in rs]) if rs else None
        c20 = carer20(cr)
        hits = sum(1 for x in rs if x["max_edible"] >= 80)
        made = sum(R[(a, s)]["carriers_made"] for s in SEEDS)
        st[a] = {"b": b[0], "w": wt[0], "c20": c20, "cs": child_starv(cr), "ncr": len(cr)}
        w(f"| {a} | {f(b[0])} (n={b[1]}) | {f(wt[0])} (n={wt[1]}) | {f(entry, 1)} | {f(100 * c20, 1) if c20 is not None else '–'}% | {hits} of {len(rs)} | {made} |")
    w("")

    w("## 4. Deaths (looked at last)\n")
    w("| arm | children's winter starvation per child-winter | child-winters | child starvation deaths, all seasons | all starvation deaths | population at 120 (seeds) |")
    w("|---|---|---|---|---|---|")
    for a in ARMS:
        cs_all = sum(v for s in SEEDS for k, v in R[(a, s)]["deaths"].items() if k.startswith("child_starvation@"))
        all_st = sum(v for s in SEEDS for k, v in R[(a, s)]["deaths"].items() if k.startswith("starvation@"))
        pops = ", ".join(str(R[(a, s)]["pops"][-1]) if R[(a, s)]["pops"] else "0" for s in SEEDS)
        w(f"| {a} | {f(100 * st[a]['cs'], 2)}% | {st[a]['ncr']} | {cs_all} | {all_st} | {pops} |")
    w("")

    w("## 5. Frozen predictions, scored\n")

    def sc(ok):
        return "**confirmed**" if ok else "**wrong**"

    def rat(x, y):
        return x / y if x is not None and y else None
    r1 = rat(st["o2"]["b"], st["arm0"]["b"])
    w(f"1. {sc(r1 is not None and r1 >= 1.3)} — bereaved carers' autumn foraging, O2 ÷ Arm 0: {f(r1, 2)} (needs ≥ 1.3).")
    r2 = rat(st["o3high"]["w"], st["arm0"]["w"])
    w(f"2. {sc(r2 is not None and r2 >= 1.2)} — witnesses with children, O2+O3-high ÷ Arm 0: {f(r2, 2)} (needs ≥ 1.2).")
    rl = rat(st["o3low"]["w"], st["arm0"]["w"])
    ok3 = rl is not None and r2 is not None and rl < r2 and st["o3low"]["c20"] is not None and st["o3low"]["c20"] < st["o3high"]["c20"]
    w(f"3. {sc(ok3)} — dose response: witness ratio low {f(rl, 2)} vs high {f(r2, 2)}; carers ≥ 20 low "
      f"{f(100 * st['o3low']['c20'], 1)}% vs high {f(100 * st['o3high']['c20'], 1)}%.")
    d4 = (st["o3high"]["c20"] - st["arm0"]["c20"]) * 100
    w(f"4. {sc(d4 >= 5)} — carers with ≥ 20 food: O2+O3-high {f(100 * st['o3high']['c20'], 1)}% vs Arm 0 "
      f"{f(100 * st['arm0']['c20'], 1)}% ({d4:+.1f} points; needs ≥ +5).")
    r5 = rat(st["o3high"]["cs"], st["arm0"]["cs"])
    w(f"5. {sc(r5 is not None and r5 <= 0.8)} — children's winter starvation, O2+O3-high ÷ Arm 0: {f(r5, 2)} (needs ≤ 0.80).")
    r6 = rat(st["o2"]["cs"], st["arm0"]["cs"])
    w(f"6. {sc(r6 is not None and 0.8 <= r6 <= 1.2)} — O2 alone, children's winter starvation ÷ Arm 0: {f(r6, 2)} (predicted within 0.8–1.2).")
    w(f"7. {sc(leak_ok)} — leak test (section 2).")
    if not valid:
        w("\n**Not valid: predictions recorded, not interpreted.**")
    elif not leak_ok:
        w("\n**The leak test failed: E10 is declared failed whatever its other results.**")
    (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
