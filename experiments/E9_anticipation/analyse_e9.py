"""E9 analysis, in the binding order of E9_preregistration.md §7: validity, then the causal links (autumn food,
winter entry, carrying limit, carriers), and only then deaths and population. Predictions scored as frozen.
Written before any E9 result was seen. Writes results.md."""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
SEEDS = (301, 302, 303, 304)
ARMS = ("arm0", "a2low", "a2full")


def load(arm, s):
    f = OUT / f"{arm}_seed_{s}.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None


def share(rows, cond):
    r = [x for x in rows if cond(x)]
    return (sum(x["forage_share"] for x in r) / len(r), len(r)) if r else (None, 0)


def med(v):
    return statistics.median(v) if v else None


def f(v, d=2):
    return "–" if v is None else f"{v:.{d}f}"


def main():
    R = {(a, s): load(a, s) for a in ARMS for s in SEEDS}
    zero = load("zero", 304)
    L = []
    w = L.append
    w("# E9 — Anticipation (A2) · Results\n")
    w("Arm 0 = E7 code; A2-low and A2-full = E7 code + A2 at weight 0.375 and 1.0. Seeds 301–304, 120 years. "
      "Pre-registration frozen as `E9-frozen` before any code. Analysis order fixed by the creator: validity, causal "
      "links, then survival.\n")

    w("## 1. Validity\n")
    v = (OUT / "verify.txt").read_text(encoding="utf-8").strip().splitlines() if (OUT / "verify.txt").exists() else []
    ok_ro = len(v) >= 2 and all("READ-ONLY" in x for x in v)
    done = all(R.values()) and zero is not None
    ok_zero = done and zero["pops"] == R[("arm0", 304)]["pops"]
    ok_rep = done and all(R[("arm0", s)]["matches_saved_e7"] for s in SEEDS)
    ok_code = done and all(r["code_hash"] == r["code_hash_after"] for r in [*R.values(), zero])
    for name, ok in (("Probe read-only (both codes)", ok_ro), ("All runs finished", done),
                     ("Zero-weight A2 code reproduces Arm 0 (seed 304, every 10 years)", ok_zero),
                     ("Arm 0 reproduces the saved E7 runs", ok_rep), ("Code unchanged during runs", ok_code)):
        w(f"- {name}: **{'yes' if ok else 'NO'}**")
    valid = ok_ro and done and ok_zero and ok_rep and ok_code
    w(f"- **{'Valid' if valid else 'INVALID or incomplete'}.**\n")
    if not done:
        print("\n".join(L)); return

    w("## 2. Leak test (hard fail)\n")
    w("Autumn foraging share of adults who have never gone short in any winter.\n")
    w("| seed | arm 0 | A2-low | A2-full |")
    w("|---|---|---|---|")
    pooled = {}
    for a in ARMS:
        rows = [x for s in SEEDS for x in R[(a, s)]["rows"]]
        pooled[a] = share(rows, lambda x: not x["ever_short_winter"])
    for s in SEEDS:
        cells = [share(R[(a, s)]["rows"], lambda x: not x["ever_short_winter"]) for a in ARMS]
        w(f"| {s} | " + " | ".join(f"{f(c[0], 3)} (n={c[1]})" for c in cells) + " |")
    w(f"| pooled | " + " | ".join(f"{f(pooled[a][0], 3)} (n={pooled[a][1]})" for a in ARMS) + " |")
    leak_ok = all(pooled[a][0] and 0.9 <= pooled[a][0] / pooled["arm0"][0] <= 1.1 for a in ("a2low", "a2full"))
    w(f"\n**Leak test {'passed' if leak_ok else 'FAILED'}** (A2 arms within ±10% of Arm 0, pooled).\n")

    w("## 3. Causal links\n")
    w("| seed | arm | autumn foraging, short last winter | median winter entry | adult-autumns reaching 80 | carriers made | carrier worth @120 |")
    w("|---|---|---|---|---|---|---|")
    stats = {}
    for s in SEEDS:
        for a in ARMS:
            r = R[(a, s)]
            sh, n = share(r["rows"], lambda x: x["short_prev_winter"])
            entry = med([x["winter_entry"] for x in r["rows"]])
            hit = sum(1 for x in r["rows"] if x["max_edible"] >= 80)
            made = sum(r["carriers_made"].values())
            cw = (next((x for x in r["samples"] if x["year"] == 120), {}) or {}).get("carrier_worth_mean")
            stats[(a, s)] = {"short_share": sh, "entry": entry, "hits": hit, "rows": len(r["rows"]), "made": made}
            w(f"| {s} | {a} | {f(sh, 3)} (n={n}) | {f(entry, 1)} | {hit} of {len(r['rows'])} | {made} | {f(cw, 3)} |")
    w("")

    w("## 4. Survival (looked at last)\n")
    w("| seed | arm | winter starvation deaths | all starvation deaths | infant deaths | pop @60 / 90 / 120 | plants left at end of autumn (mean) |")
    w("|---|---|---|---|---|---|---|")
    for s in SEEDS:
        for a in ARMS:
            r = R[(a, s)]
            d = r["deaths"]
            ws = d.get("starvation@3", 0)
            alls = sum(v for k, v in d.items() if k.startswith("starvation@"))
            pops = " / ".join(str(r["pops"][i]) if len(r["pops"]) > i else "–" for i in (5, 8, 11))
            pl = statistics.mean(r["end_autumn_plants"]) if r["end_autumn_plants"] else None
            w(f"| {s} | {a} | {ws} | {alls} | {d.get('infant', 0)} | {pops} | {f(pl, 0)} |")
    w("")

    w("## 5. Frozen predictions, scored\n")

    def sc(ok):
        return "**confirmed**" if ok else "**wrong**"

    def ratio(a, s, k="short_share"):
        x, y = stats[(a, s)][k], stats[("arm0", s)][k]
        return x / y if x is not None and y else None
    r_full = {s: ratio("a2full", s) for s in SEEDS}
    r_low = {s: ratio("a2low", s) for s in SEEDS}
    n1 = sum(1 for s in SEEDS if r_full[s] and r_full[s] >= 1.3)
    w(f"1. {sc(n1 >= 3)} (manipulation check) — A2-full autumn foraging of adults short last winter, ÷ Arm 0: "
      + ", ".join(f"{s}: {f(r_full[s])}" for s in SEEDS) + f" ({n1} of 4 ≥ 1.3).")
    n2 = sum(1 for s in SEEDS if r_low[s] is not None and r_full[s] is not None and r_low[s] < r_full[s])
    w(f"2. {sc(n2 >= 3)} — dose response (A2-low rise smaller than A2-full) in {n2} of 4 seeds: "
      + ", ".join(f"{s}: {f(r_low[s])} vs {f(r_full[s])}" for s in SEEDS) + ".")
    n3 = sum(1 for s in SEEDS if stats[("a2full", s)]["entry"] is not None and stats[("arm0", s)]["entry"]
             and stats[("a2full", s)]["entry"] >= 2 * stats[("arm0", s)]["entry"])
    w(f"3. {sc(n3 >= 3)} — A2-full median winter entry ≥ 2× Arm 0 in {n3} of 4 seeds: "
      + ", ".join(f"{s}: {f(stats[('a2full', s)]['entry'], 1)} vs {f(stats[('arm0', s)]['entry'], 1)}" for s in SEEDS) + ".")
    ws0 = sum(R[("arm0", s)]["deaths"].get("starvation@3", 0) for s in SEEDS)
    wsf = sum(R[("a2full", s)]["deaths"].get("starvation@3", 0) for s in SEEDS)
    w(f"4. {sc(ws0 > 0 and wsf <= 0.8 * ws0)} — winter starvation deaths, A2-full {wsf} vs Arm 0 {ws0} (needs ≤ 80%).")
    hits = sum(stats[("a2full", s)]["hits"] for s in SEEDS)
    rows = sum(stats[("a2full", s)]["rows"] for s in SEEDS)
    w(f"5. {sc(rows and hits / rows >= 0.01)} — A2-full adult-autumns reaching 80 food in hand: {hits} of {rows} "
      f"({100 * hits / rows:.2f}%; needs ≥ 1%).")
    w(f"6. {sc(leak_ok)} — leak test (section 2).")
    if not ok_rep or not valid:
        w("\n**The experiment is not valid; predictions are recorded but not interpreted.**")
    elif not leak_ok:
        w("\n**The leak test failed: E9 is declared failed, whatever its other results (pre-registration §4a).**")
    (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
