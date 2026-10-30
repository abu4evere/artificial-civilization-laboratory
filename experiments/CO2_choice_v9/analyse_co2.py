"""CO2 analysis, written before any data (questions.md, frozen as `CO2-frozen`): CO1's analysis with names changed,
plus Q5 (the curiosity split of making's deficit; adults, as CO1's primary).

  python experiments/CO2_choice_v9/analyse_co2.py            # writes results.md
  python experiments/CO2_choice_v9/analyse_co2.py --smoke --dir <folder> [--smoke-late]
"""
from __future__ import annotations

import glob
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_co2 import SEEDS  # noqa: E402
from run_co1 import BIN_EDGES, SWAPS, T, WPY  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261027)
BINS = [f"{BIN_EDGES[i]}-{BIN_EDGES[i + 1]}" for i in range(len(BIN_EDGES) - 1)]
EARLY, LATE = (0, 1), (5,)
if "--smoke-late" in sys.argv:
    LATE = (2,)
PARTS = ("habit", "multiplicity", "per-entry score", "spread")


def parse(k):
    b, age, hb, tool, fb = k.split("|")
    return int(b), age, int(hb), int(tool), int(fb)


def families(rs):
    return sorted({k.split(":")[0] for r in rs for c in r["cells"].values() for k in c if ":" in k})


def alive_at(r, year):
    return r["final_tick"] > year * WPY


def ci(reps):
    reps = np.asarray([x for x in reps if np.isfinite(x)])
    if not len(reps):
        return "[-]"
    lo, hi = np.percentile(reps, [2.5, 97.5])
    return f"[{lo:.3g}, {hi:.3g}]"


def pooled(worlds, bins):
    """Matched state (hunger, tool, food) -> summed adult cell counters."""
    out = defaultdict(Counter)
    for r in worlds:
        for k, c in r["cells"].items():
            p = parse(k)
            if p[0] in bins and p[1] == "adult":
                out[(p[2], p[3], p[4])].update(c)
    return out


def split(worlds, fams):
    E, L = pooled(worlds, EARLY), pooled(worlds, LATE)
    states = [s for s in E if E[s]["offered"] > 0 and L[s]["offered"] > 0]
    wsum = sum(E[s]["offered"] for s in states)
    if not wsum:
        return None
    d = Counter()
    for s in states:
        w = E[s]["offered"] / wsum
        e, l_ = E[s], L[s]
        ne, nl = e["offered"], l_["offered"]
        d["u_other_e"] += w * e["u_other"] / ne
        d["u_other_l"] += w * l_["u_other"] / nl
        d["spread"] += w * (l_["spread"] / nl - e["spread"] / ne)
        d["logit_e"] += w * e["logit"] / ne
        d["logit_l"] += w * l_["logit"] / nl
        d["grouped_e"] += w * e["logit_grouped"] / ne
        d["grouped_l"] += w * l_["logit_grouped"] / nl
        if l_["swapped"]:
            for sw in SWAPS:
                d[f"swap_{sw}"] += w * l_[f"logit_swap_{sw}"] / l_["swapped"]
        for a in fams:
            for key, part in (("sh", "habit"), ("sn", "multiplicity"), ("sm", "per-entry score")):
                x = w * (l_[f"{a}:{key}"] / nl - e[f"{a}:{key}"] / ne)
                d[part] += x
                d[f"{a}|{part}"] += x
    d["spread_part"] = d["spread"]
    d["states"] = len(states)
    d["delta"] = d["u_other_l"] - d["u_other_e"]
    d["residual"] = d["delta"] - (d["habit"] + d["multiplicity"] + d["per-entry score"] + d["spread"])
    return d


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rs = [json.load(open(f)) for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json")))]
    fams = families(rs)
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    fps = {r["code_hash"] for r in rs} | {r["code_hash_after"] for r in rs}
    mism = sum(sum(r["mismatch"].values()) for r in rs)
    ok = "All: PASS" in zero and sorted(r["seed"] for r in rs) == sorted(SEEDS) and len(fps) == 1 and mism == 0
    L = ["# CO2 — What makes the other options beat making under nature v9? Results", "",
         "Frozen as `CO2-frozen`. run_co2.py (CO1's runner on code_v9 + the curiosity split), analyse_co2.py "
         "(CO1's analysis + Q5; written before data).", "", "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({len(rs)} of {len(SEEDS)}): **{'yes' if sorted(r['seed'] for r in rs) == sorted(SEEDS) else 'NO'}**",
         f"- One fingerprint (`code_v9`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- The identity holds in every logged week (family and identity mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**",
         "", f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    # population and people near
    L += ["## Population and people within reach (adults, offered weeks; worlds alive at each bin's start)", "",
          "| bin | worlds | offered weeks | people within reach (mean) | U_other (mean) | chosen / offered |",
          "|---|---|---|---|---|---|"]
    for i, name in enumerate(BINS):
        al = [r for r in rs if alive_at(r, BIN_EDGES[i])]
        t = Counter()
        for r in al:
            for k, c in r["cells"].items():
                p = parse(k)
                if p[0] == i and p[1] == "adult":
                    t.update(c)
        if t["offered"]:
            n = t["offered"]
            L.append(f"| {name} | {len(al)} | {n:.0f} | {t['near'] / n:.2f} | {t['u_other'] / n:.3f} | "
                     f"{t['chosen'] / n:.4f} |")
    L.append("")
    # Q1
    L += ["## Q1 — Which families? (adults, offered weeks, all worlds alive at each bin's start)", "",
          "Share of the competing weight s_a (mean over offered weeks); entries n_a, habit h_a and per-entry score M_a "
          "are means over the weeks the family is present.", ""]
    tot = {}
    for i in range(len(BINS)):
        t = Counter()
        for r in rs:
            for k, c in r["cells"].items():
                p = parse(k)
                if p[0] == i and p[1] == "adult":
                    t.update(c)
        tot[i] = t
    main_f = sorted(fams, key=lambda a: -sum(tot[i][f"{a}:s"] for i in tot))[:10]
    L += ["| family | " + " | ".join(f"s {b}" for b in BINS) + " | n early → late | h early → late | M early → late |",
          "|---" * (4 + len(BINS)) + "|"]
    for a in main_f:
        row = []
        for i in range(len(BINS)):
            n = tot[i]["offered"]
            row.append(f"{tot[i][f'{a}:s'] / n:.3f}" if n else "-")
        e = tot[0] + tot[1]
        l_ = tot[5]

        def m(t, key):
            return t[f"{a}:{key}"] / t[f"{a}:present"] if t[f"{a}:present"] else float("nan")
        L.append(f"| {a} | " + " | ".join(row) + f" | {m(e, 'n'):.2f} → {m(l_, 'n'):.2f} | {m(e, 'h'):.3f} → "
                 f"{m(l_, 'h'):.3f} | {m(e, 'm'):.3f} → {m(l_, 'm'):.3f} |")
    L.append("")
    # Q2
    al = [r for r in rs if alive_at(r, BIN_EDGES[LATE[0]])]
    d = split(al, fams)
    if d is None:
        L += ["## Q2 — no matched states.", ""]
    else:
        reps = defaultdict(list)
        ix = RNG.integers(0, len(al), size=(REPS, len(al)))
        for row in ix:
            dd = split([al[k] for k in row], fams)
            if dd is None:
                continue
            for k_ in ("delta", "habit", "multiplicity", "per-entry score", "spread"):
                reps[k_].append(dd[k_])
        L += ["## Q2 — The exact split of the rise in U_other (primary)", "",
              f"Adults, offered weeks; early = years 0-10, late = years 100-200; worlds alive at year 100 ({len(al)}); "
              f"{d['states']:.0f} matched states (hunger × tool × food), late weighted to the early offered weeks.", "",
              f"- U_other: {d['u_other_e']:.3f} → {d['u_other_l']:.3f}; **Δ = {d['delta']:+.3f} {ci(reps['delta'])}**.",
              "", "| part | Δ | share of the rise |", "|---|---|---|"]
        for part in PARTS:
            key = part if part != "spread" else "spread"
            L.append(f"| {part} | {d[key]:+.3f} {ci(reps[key])} | {d[key] / d['delta']:.2f} |")
        L += [f"| **total** | {d['delta']:+.3f} | 1.00 |", "",
              f"(Exactness check: Δ minus the parts = {d['residual']:.2e}.)", ""]
        largest = max(PARTS, key=lambda p_: d[p_ if p_ != "spread" else "spread"] * np.sign(d["delta"]))
        L += [f"**The part carrying the largest share of the rise: {largest}.**", "",
              "By family (habit + multiplicity + per-entry score), largest contributions:", "",
              "| family | habit | multiplicity | per-entry score | total |", "|---|---|---|---|---|"]
        fam_tot = {a: sum(d[f"{a}|{p_}"] for p_ in PARTS[:3]) for a in fams}
        for a in sorted(fams, key=lambda a: -abs(fam_tot[a]))[:8]:
            L.append(f"| {a} | {d[f'{a}|habit']:+.3f} | {d[f'{a}|multiplicity']:+.3f} | {d[f'{a}|per-entry score']:+.3f} | "
                     f"{fam_tot[a]:+.3f} |")
        L.append("")
        # Q3
        fall = d["logit_e"] - d["logit_l"]
        L += ["## Q3 — Counterfactual swaps (diagnostic; within each world, its own early means; late = years 100-200)", "",
              f"Mean log-odds of choosing make (matched): early {d['logit_e']:.2f}, late {d['logit_l']:.2f} (fall "
              f"{fall:.2f}).", "", "| late, with this part set back to its early value | mean log-odds | share of the fall undone |",
              "|---|---|---|"]
        for sw, name in (("n", "(i) entries"), ("h", "(ii) habits"), ("m", "(iii) per-entry scores"), ("all", "(iv) all three")):
            v = d[f"swap_{sw}"]
            L.append(f"| {name} | {v:.2f} | {(v - d['logit_l']) / fall:.2f} |")
        L += ["", f"(v) Grouped (every family one entry): early {d['grouped_e']:.2f}, late {d['grouped_l']:.2f}; actual "
              f"early {d['logit_e']:.2f}, late {d['logit_l']:.2f}. The swaps interact; their shares need not add up.", ""]
    # Q4
    L += ["## Q4 — Described", "", "Habit h_a (mean when present), by bin, for the main families:", "",
          "| family | " + " | ".join(BINS) + " |", "|---" * (1 + len(BINS)) + "|"]
    for a in main_f[:6]:
        L.append(f"| {a} | " + " | ".join(f"{tot[i][f'{a}:h'] / tot[i][f'{a}:present']:.3f}" if tot[i][f"{a}:present"] else "-"
                                       for i in range(len(BINS))) + " |")
    L += ["", "Forage per-entry score M by hunger band, early and late:", ""]
    for hb in range(4):
        e = Counter()
        l_ = Counter()
        for r in rs:
            for k, c in r["cells"].items():
                p = parse(k)
                if p[1] == "adult" and p[2] == hb:
                    (e if p[0] in EARLY else l_ if p[0] in LATE else Counter()).update(c)
        f = lambda t: t["forage:m"] / t["forage:present"] if t["forage:present"] else float("nan")  # noqa: E731
        L.append(f"- hunger band {hb}: {f(e):.3f} → {f(l_):.3f}")
    L.append("")
    # Q5 (CO2's addition): which part carries making's deficit; adults, late offered weeks
    rng5 = np.random.default_rng(20261101)
    keys = ("q5_gap", "q5_habit", "q5_curiosity", "q5_mult", "q5_built")
    per = []
    for r in rs:
        t5 = Counter()
        for k, c in r["cells"].items():
            p = parse(k)
            if p[0] in LATE and p[1] == "adult":
                t5.update({x: c.get(x, 0.0) for x in keys + ("q5_n", "c_m", "c_other", "h_m")})
        per.append(t5)
    G = np.array([[t[x] for x in keys] for t in per], float)
    n5 = sum(t["q5_n"] for t in per)
    L += ["## Q5 — Which part carries making's deficit under v9 (primary for v9)", "",
          f"Adults, weeks with making offered, years 100-200 ({int(n5):,} person-weeks in {len(rs)} worlds). The gap "
          "U_other - U_m splits exactly into habit, curiosity, multiplicity and spread, and the built-in and thought "
          "pull. World bootstrap, 10,000 replicates, generator seed 20261101.", ""]
    if n5 and G[:, 0].sum():
        idx = rng5.integers(0, len(per), size=(REPS, len(per)))
        tot5 = G.sum(0)
        reps5 = G[idx].sum(1)
        with np.errstate(divide="ignore", invalid="ignore"):
            share = tot5[1:] / tot5[0]
            rshare = reps5[:, 1:] / reps5[:, :1]
        names = ("habit", "curiosity", "multiplicity and spread", "built-in and thought pull")
        L += ["| part | mean per week | share of the gap [95%] |", "|---|---|---|",
              f"| the gap U_other - U_m | {tot5[0] / n5:.4f} | 1 |"]
        lo_hi = {}
        for j, nm in enumerate(names):
            ok_ = rshare[:, j][np.isfinite(rshare[:, j])]
            lo, hi = np.percentile(ok_, [2.5, 97.5])
            lo_hi[nm] = (share[j], lo, hi)
            L.append(f"| {nm} | {tot5[j + 1] / n5:+.4f} | {share[j]:+.3f} [{lo:+.3f}, {hi:+.3f}] |")
        cm = sum(t["c_m"] for t in per) / n5
        co = sum(t["c_other"] for t in per) / n5
        hm = sum(t["h_m"] for t in per) / n5
        L += ["", f"Making's own score: habit {hm:.4f}, curiosity {cm:.4f}; the competitors' weighted curiosity "
                  f"{co:.4f}.", ""]
        if lo_hi["habit"][1] > 0.5:
            read = "habit carries it"
        elif lo_hi["built-in and thought pull"][1] > 0.5:
            read = "built-in pull carries it"
        else:
            read = "mixed"
        against = lo_hi["curiosity"][2] < 0
        L += [f"**Reading: {read}.**" + (" **Curiosity works against the gap (it favours making).**" if against
                                         else ""), ""]
    else:
        L += ["No late offered weeks.", ""]
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
