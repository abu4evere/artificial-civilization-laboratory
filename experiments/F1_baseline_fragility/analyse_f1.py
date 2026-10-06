"""F1 analysis, in the order of questions.md (frozen as `F1-questions`). Written before any discovery data was read.

Decisions made in writing this file (before data), where questions.md left room:
- A world "dies out" if it has no one alive at year 120. E = the year (0-based) of its last living week.
- Q1 windows for extinct worlds are counted back from E: [E-30, E-20), [E-20, E-10), [E-10, E]. Survivors are
  pooled over their whole run and over years 0-39.
- Q2 "mate shortage" before the last birth: in more than half of the years [B-10, B) at least one unpartnered woman
  16-45 had no mate-eligible man anywhere in the world (mid-year snapshot).
- Q4 AUC = P(future-extinct world's value > survivor's value), ties count a half; "separation" = max(AUC, 1 - AUC),
  the direction reported. The sex ratio enters as imbalance |log(men / women)|. Past-decade indicators use years
  [t-10, t). Worlds dying at least 20 years after t are "future-extinct"; worlds dying sooner are left out.
- Q5 signatures, binary per world, read over the first 30 years for every world alive at year 30 (worlds that die
  before 30 are described separately):
    G1 population at year 30 below the 20 founders;   G2 adult sex imbalance at year 30 (men ÷ women outside 0.67-1.5);
    G3 most unpartnered women 16-45 at year 30 have no mate-eligible man in the world;
    G4 starving share of person-weeks, years 0-29, above the median of all worlds alive at 30;
    G5 births per woman-year, years 0-29, below that median;
    G6 most people alone at year 30 (groups ÷ population > 0.5);
    G7 at most 3 women 16-45 at year 30.

  python experiments/F1_baseline_fragility/analyse_f1.py discovery   (or: holdout)
"""
from __future__ import annotations

import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_f1 import DISCOVERY, HOLDOUT, OUT  # noqa: E402

WPY = 52
CAUSES = ("starvation", "thirst", "cold", "neglect", "illness", "old age", "childbirth", "killed", "mauled")
BLOCKS = ("pregnant", "no_partner", "partner_dead", "apart", "low_health", "starving", "partner_child", "nursing",
          "eligible")


def load(seeds):
    R = {}
    for s in seeds:
        r = json.loads((OUT / f"seed_{s}.json").read_text(encoding="utf-8"))
        r["Y"] = {int(k): v for k, v in r["years"].items()}
        r["extinct"] = not (len(r["pops"]) == 12 and r["pops"][-1] > 0)
        r["E"] = (r["final_tick"] - 1) // WPY if r["extinct"] else None
        R[s] = r
    return R


def ysum(r, key, y0, y1):
    return sum(r["Y"].get(y, {}).get(key, 0.0) for y in range(y0, y1))


def rates(rs, windows):
    """Pooled rates over a list of (world, y0, y1)."""
    agg = Counter()
    for r, y0, y1 in windows:
        for y in range(y0, y1):
            for k, v in r["Y"].get(y, {}).items():
                if isinstance(v, (int, float)) and (k.startswith(("d_", "r_")) or k in (
                        "births", "deaths", "person_weeks", "woman_weeks", "starving_weeks", "no_carer_weeks", "pairs")):
                    agg[k] += v
        agg["child_deaths"] += sum(1 for d in r["deaths"] if y0 <= d[0] < y1 and d[2] is not None and d[2] < 12)
        agg["births_w"] += sum(1 for b in r["births"] if y0 <= b[0] < y1)
    py = agg["person_weeks"] / WPY
    wy = agg["woman_weeks"] / WPY
    out = {"person_years": py, "woman_years": wy,
           "births_per_woman_year": agg["births"] / wy if wy else None,
           "deaths_per_person_year": agg["deaths"] / py if py else None,
           "births_per_person_year": agg["births"] / py if py else None,
           "starving_share": agg["starving_weeks"] / agg["person_weeks"] if agg["person_weeks"] else None,
           "child_deaths_per_birth": agg["child_deaths"] / agg["births_w"] if agg["births_w"] else None,
           "no_carer_share": agg["no_carer_weeks"] / agg["person_weeks"] if agg["person_weeks"] else None,
           "pairs_per_person_year": agg["pairs"] / py if py else None}
    for c in CAUSES:
        out["cause_" + c] = agg["d_" + c] / agg["deaths"] if agg["deaths"] else None
    for b in BLOCKS:
        out["block_" + b] = agg["r_" + b] / agg["woman_weeks"] if agg["woman_weeks"] else None
    return out


def fmt(x, d=3):
    return "–" if x is None else f"{x:.{d}f}"


def auc(pos, neg):
    if not pos or not neg:
        return None
    s = 0.0
    for a in pos:
        for b in neg:
            s += 1.0 if a > b else 0.5 if a == b else 0.0
    return s / (len(pos) * len(neg))


def indicators(r, t):
    Y, c = r["Y"], r["Y"].get(t, {})
    wy = ysum(r, "woman_weeks", t - 10, t) / WPY
    pw = ysum(r, "person_weeks", t - 10, t)
    au = [Y[y]["autumn_tile"] for y in range(t - 10, t) if y in Y and "autumn_tile" in Y[y]]
    m, f = c.get("adult_men", 0), c.get("adult_women", 0)
    return {"population": c.get("n", 0),
            "women 16-45": c.get("women", 0),
            "adult sex imbalance, abs log(m/f)": abs(math.log((m + 0.5) / (f + 0.5))),
            "births per woman-year, past decade": ysum(r, "births", t - 10, t) / wy if wy else 0.0,
            "starving share, past decade": ysum(r, "starving_weeks", t - 10, t) / pw if pw else 0.0,
            "autumn food per land tile, past decade": statistics.mean(au) if au else 0.0,
            "share of women 16-45 unpartnered": c.get("women_single", 0) / c["women"] if c.get("women") else 1.0,
            "share of single women with no mate in world": (c.get("women_single_no_mate", 0) / c["women_single"]
                                                            if c.get("women_single") else 0.0),
            "groups": c.get("groups", 0)}


def main(which):
    seeds = DISCOVERY if which == "discovery" else HOLDOUT
    R = load(seeds)
    L = []
    w = L.append
    ext = [r for r in R.values() if r["extinct"]]
    sur = [r for r in R.values() if not r["extinct"]]
    w(f"# F1 — Baseline fragility: {which} results (generated by `analyse_f1.py {which}`)\n")
    w("## Validity\n")
    rep = [r["seed"] for r in R.values() if "reproduces" in r and not r["reproduces"]]
    code = all(r["code_hash"] == r["code_hash_after"] for r in R.values())
    checks = (OUT / "checks.txt").read_text(encoding="utf-8").strip()
    w(f"- Observer read-only: **{'yes' if 'CHANGES' not in checks and checks.count('READ-ONLY') >= 2 else 'NO'}**")
    if which == "discovery":
        w(f"- Replays reproduce saved populations: **{'yes, all ' + str(len(R)) if not rep else 'NO: ' + str(rep)}**")
    w(f"- Code unchanged during runs: **{'yes' if code else 'NO'}**\n")
    valid = not rep and code and "CHANGES" not in checks

    w(f"## Worlds\n\n{len(ext)} of {len(R)} died out. Year of extinction: "
      + ", ".join(f"{r['seed']}: {r['E']}" for r in sorted(ext, key=lambda r: r["E"])) + ".")
    w("Peak population, extinct worlds (median): "
      f"{statistics.median(max(v.get('n', 0) for v in r['Y'].values()) for r in ext) if ext else '–'}; "
      f"survivors: {statistics.median(max(v.get('n', 0) for v in r['Y'].values()) for r in sur) if sur else '–'}.\n")

    # ---------------- Q1 and Q3
    w("## Q1 / Q3. Births against deaths, and what kills\n")
    cols = [("survivors, whole run", [(r, 0, 120) for r in sur]),
            ("survivors, years 0-39", [(r, 0, 40) for r in sur]),
            ("extinct, whole life", [(r, 0, r["E"] + 1) for r in ext]),
            ("extinct, E-30 to E-20", [(r, max(0, r["E"] - 30), max(0, r["E"] - 20)) for r in ext]),
            ("extinct, E-20 to E-10", [(r, max(0, r["E"] - 20), max(0, r["E"] - 10)) for r in ext]),
            ("extinct, last 10 years", [(r, max(0, r["E"] - 10), r["E"] + 1) for r in ext])]
    T = [(name, rates(None, win)) for name, win in cols]
    w("| measure | " + " | ".join(n for n, _ in T) + " |")
    w("|---|" + "---|" * len(T))
    keys = (["person_years", "births_per_woman_year", "births_per_person_year", "deaths_per_person_year",
             "starving_share", "child_deaths_per_birth", "no_carer_share", "pairs_per_person_year"]
            + ["cause_" + c for c in CAUSES] + ["block_" + b for b in BLOCKS])
    for k in keys:
        w(f"| {k} | " + " | ".join(fmt(t[k], 0 if k == "person_years" else 3) for _, t in T) + " |")
    w("\n(cause_*: share of deaths; block_*: share of woman-weeks (16-45) in each state, the first failing condition in "
      "the code's order.)\n")

    # ages
    w("Mean age of the living and share over 50 (mid-year), extinct worlds in their last 10 years vs survivors:")
    def agestats(win):
        a = [r["Y"][y]["mean_age"] for r, y0, y1 in win for y in range(y0, y1) if y in r["Y"] and "mean_age" in r["Y"][y]]
        o = [(r["Y"][y].get("n_elder_M", 0) + r["Y"][y].get("n_elder_F", 0)) / r["Y"][y]["n"]
             for r, y0, y1 in win for y in range(y0, y1) if y in r["Y"] and r["Y"][y].get("n")]
        return fmt(statistics.mean(a), 1) if a else "–", fmt(statistics.mean(o)) if o else "–"
    for name, win in cols:
        a, o = agestats(win)
        w(f"- {name}: mean age {a}, share over 50 {o}")
    w("")

    # ---------------- Q2
    w("## Q2. Paths to extinction (frozen classification)\n")
    w("| seed | E | last birth B | E − B | last woman 16-45 F | bad-weather deaths, last 10 y | path | main block before B | mate shortage before B |")
    w("|---|---|---|---|---|---|---|---|---|")
    paths = Counter()
    for r in sorted(ext, key=lambda r: r["E"]):
        E = r["E"]
        B = max((b[0] for b in r["births"]), default=-1)
        Fy = max((y for y, v in r["Y"].items() if v.get("woman_weeks", 0) > 0), default=-1)
        last = [d for d in r["deaths"] if d[0] >= E - 10]
        bad = sum(1 for d in last if d[1] in ("starvation", "thirst", "cold"))
        if last and bad / len(last) > 0.5:
            path = "crash"
        elif E - B >= 15:
            path = "reproductive failure, then ageing out"
        else:
            path = "attrition"
        paths[path] += 1
        blk = Counter()
        for y in range(max(0, B - 10), B + 1):
            for b in BLOCKS:
                if b != "pregnant":
                    blk[b] += r["Y"].get(y, {}).get("r_" + b, 0)
        main_b = blk.most_common(1)[0][0] if sum(blk.values()) else "–"
        yrs = [y for y in range(max(0, B - 10), B) if y in r["Y"]]
        short = sum(1 for y in yrs if r["Y"][y].get("women_single_no_mate", 0) >= 1)
        w(f"| {r['seed']} | {E} | {B} | {E - B} | {Fy} | {bad} of {len(last)} | {path} | {main_b} | "
          f"{short} of {len(yrs)} years{' (shortage)' if yrs and short > len(yrs) / 2 else ''} |")
    w("\nPaths: " + "; ".join(f"{k}: {v}" for k, v in paths.most_common()) + ".\n")

    # ---------------- Q4
    w("## Q4. Early warning (pre-stated indicators; AUC, direction: higher value = future-extinct)\n")
    for t in (20, 30, 40):
        fut = [r for r in ext if r["E"] >= t + 20]
        alive_s = sur
        w(f"**Year {t}:** {len(fut)} future-extinct worlds (die at {t + 20} or later) vs {len(alive_s)} survivors.\n")
        if not fut:
            continue
        w("| indicator | median, future-extinct | median, survivors | AUC | separation |")
        w("|---|---|---|---|---|")
        for k in indicators(fut[0], t):
            a = [indicators(r, t)[k] for r in fut]
            b = [indicators(r, t)[k] for r in alive_s]
            u = auc(a, b)
            w(f"| {k} | {fmt(statistics.median(a))} | {fmt(statistics.median(b))} | {fmt(u, 2)} | "
              f"{fmt(max(u, 1 - u), 2)}{' ←' if max(u, 1 - u) >= 0.80 else ''} |")
        w("")

    # ---------------- Q5
    w("## Q5. Signatures over the first 30 years (worlds alive at year 30)\n")
    at30 = [r for r in R.values() if r["Y"].get(30, {}).get("n", 0) > 0]
    early = [r for r in ext if r not in at30]
    w(f"{len(early)} extinct worlds died before year 30 (described in Q2); {sum(r['extinct'] for r in at30)} extinct and "
      f"{sum(not r['extinct'] for r in at30)} surviving worlds were alive at 30.\n")

    def sw(r):
        pw = ysum(r, "person_weeks", 0, 30)
        return ysum(r, "starving_weeks", 0, 30) / pw if pw else 0.0

    def bw(r):
        wy = ysum(r, "woman_weeks", 0, 30) / WPY
        return ysum(r, "births", 0, 30) / wy if wy else 0.0
    med_s = statistics.median(sw(r) for r in at30) if at30 else 0
    med_b = statistics.median(bw(r) for r in at30) if at30 else 0

    def sig(r):
        c = r["Y"][30]
        m, f = c.get("adult_men", 0), c.get("adult_women", 0)
        ratio = m / f if f else float("inf")
        return {"G1 population at 30 below 20": c["n"] < 20,
                "G2 adult sex imbalance at 30": not (0.67 <= ratio <= 1.5),
                "G3 most single women have no mate in world": c.get("women_single", 0) > 0 and c.get("women_single_no_mate", 0) > c["women_single"] / 2,
                "G4 starving share 0-29 above median": sw(r) > med_s,
                "G5 births per woman-year 0-29 below median": bw(r) < med_b,
                "G6 most people alone at 30": c.get("groups", 0) / c["n"] > 0.5,
                "G7 at most 3 women 16-45 at 30": c.get("women", 0) <= 3}
    e30 = [r for r in at30 if r["extinct"]]
    s30 = [r for r in at30 if not r["extinct"]]
    w("| signature | extinct worlds with it | survivors with it | shared? (≥ 2/3 extinct, ≤ 1/3 survivors) |")
    w("|---|---|---|---|")
    if e30 and s30:
        for k in sig(e30[0]):
            ne = sum(sig(r)[k] for r in e30)
            ns = sum(sig(r)[k] for r in s30)
            ok = ne >= 2 * len(e30) / 3 and ns <= len(s30) / 3
            w(f"| {k} | {ne} of {len(e30)} | {ns} of {len(s30)} | {'**yes**' if ok else 'no'} |")
    if not valid:
        w("\n**Not valid: recorded, not interpreted.**")
    text = "\n".join(L) + "\n"
    (HERE / f"results_{which}.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "discovery")
