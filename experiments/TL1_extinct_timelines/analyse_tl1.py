"""TL1 analysis: extinct-world timelines (questions.md, frozen as `TL1-frozen`).

  python experiments/TL1_extinct_timelines/analyse_tl1.py discovery   -> results_discovery.md (commit before holdout)
  python experiments/TL1_extinct_timelines/analyse_tl1.py holdout     -> results_holdout.md (needs results_discovery.md)
"""
from __future__ import annotations

import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent

SETS = {
    "discovery": [
        EXP / "RT1_residence_time" / "output_rt1b",
        EXP / "FX2_embedded_food" / "output",
    ],
    "holdout": [
        EXP / "FX3_gentler_embedded" / "output",
    ],
}
SEEDS = {
    "discovery": list(range(5701, 5957)) + list(range(6001, 6257)),
    "holdout": list(range(7301, 7557)),
}

CAUSES = [
    "old age",
    "starvation",
    "illness",
    "thirst",
    "neglect",
    "childbirth",
    "killed",
    "cold",
]


def load_worlds(set_name: str) -> list[dict]:
    rows = []
    for d in SETS[set_name]:
        for f in sorted(d.glob("c_seed_*.json")):
            m = re.search(r"(\d+)", f.stem.split("_seed_")[1])
            if not m:
                continue
            s = int(m.group(1))
            if s in SEEDS[set_name]:
                rows.append(json.loads(f.read_text(encoding="utf-8")))
    return rows


def is_extinct(r: dict) -> bool:
    return r["final_tick"] < 120 * 52


def analyse_q1(extinct_worlds: list[dict]) -> dict:
    deltas = []
    for r in extinct_worlds:
        t_ext = r["final_tick"] // 52
        t_last_birth = r["births"][-1][0] if r.get("births") else 0
        deltas.append(t_ext - t_last_birth)

    n = len(deltas)
    med = statistics.median(deltas) if deltas else 0
    mean_val = statistics.mean(deltas) if deltas else 0
    ge_20_count = sum(1 for d in deltas if d >= 20)
    ge_20_share = ge_20_count / n if n else 0.0
    lt_10_count = sum(1 for d in deltas if d < 10)
    lt_10_share = lt_10_count / n if n else 0.0

    if med >= 30 and ge_20_share >= 0.80:
        reading = "Ageing out"
    elif med < 10 or lt_10_share >= 0.50:
        reading = "Acute collapse"
    else:
        reading = "Mixed"

    return {
        "n": n,
        "deltas": deltas,
        "median": med,
        "mean": mean_val,
        "ge_20_count": ge_20_count,
        "ge_20_share": ge_20_share,
        "lt_10_count": lt_10_count,
        "lt_10_share": lt_10_share,
        "reading": reading,
    }


def analyse_q2(extinct_worlds: list[dict]) -> dict:
    qualifying = []
    shares = []

    for r in extinct_worlds:
        t_last_birth = r["births"][-1][0] if r.get("births") else 0
        snap = r.get("years", {}).get(str(t_last_birth), {})
        w_single = snap.get("women_single", 0)
        w_no_mate = snap.get("women_single_no_mate", 0)

        if w_single > 0:
            share = (w_single - w_no_mate) / w_single
            qualifying.append(r["seed"])
            shares.append(share)

    n_qual = len(shares)
    mean_share = statistics.mean(shares) if shares else 0.0
    med_share = statistics.median(shares) if shares else 0.0

    # Distribution breakdown: share == 0, 0 < share < 1, share == 1
    zero_c = sum(1 for s in shares if s == 0.0)
    partial_c = sum(1 for s in shares if 0.0 < s < 1.0)
    full_c = sum(1 for s in shares if s == 1.0)

    if mean_share >= 0.50:
        reading = "failure to pair"
    elif mean_share < 0.20:
        reading = "empty mate pool"
    else:
        reading = "mixed"

    return {
        "n_extinct": len(extinct_worlds),
        "n_qualifying": n_qual,
        "mean_share": mean_share,
        "median_share": med_share,
        "zero_count": zero_c,
        "partial_count": partial_c,
        "full_count": full_c,
        "shares": shares,
        "reading": reading,
    }


def analyse_q3(all_worlds: list[dict], k_values=(5, 10, 15)) -> dict:
    results = {}
    n_worlds = len(all_worlds)

    for k in k_values:
        experienced_worlds = []
        recovered_birth = []
        survived_120 = []

        for r in all_worlds:
            # Check if world ever had fertile women
            ever_women = any(r.get("years", {}).get(str(y), {}).get("women", 0) > 0 for y in range(r["final_tick"] // 52 + 1))
            if not ever_women:
                continue

            birth_years = set(b[0] for b in r.get("births", []))
            max_y = r["final_tick"] // 52

            # Find FIRST episode of K consecutive years with zero births where women > 0 at start
            first_hiatus_end = None
            for y in range(max_y - k + 1):
                if not any((y + offset) in birth_years for offset in range(k)):
                    if r.get("years", {}).get(str(y), {}).get("women", 0) > 0:
                        first_hiatus_end = y + k - 1
                        break

            if first_hiatus_end is not None:
                experienced_worlds.append(r["seed"])
                has_later_birth = any(by > first_hiatus_end for by in birth_years)
                recovered_birth.append(has_later_birth)
                survived_120.append(not is_extinct(r))

        n_exp = len(experienced_worlds)
        birth_rec_c = sum(1 for b in recovered_birth if b)
        surv_rec_c = sum(1 for s in survived_120 if s)

        birth_rec_rate = birth_rec_c / n_exp if n_exp else 0.0
        surv_rec_rate = surv_rec_c / n_exp if n_exp else 0.0

        results[k] = {
            "n_exp": n_exp,
            "birth_recovered_count": birth_rec_c,
            "birth_recovery_rate": birth_rec_rate,
            "surv_recovered_count": surv_rec_c,
            "surv_recovery_rate": surv_rec_rate,
        }

    # Reading on k=10 survival
    r10 = results[10]["surv_recovery_rate"]
    if r10 < 0.05:
        reading = "empirical point of no return"
    elif r10 >= 0.20:
        reading = "recoverable"
    else:
        reading = "rarely recovered"

    return {
        "n_total": n_worlds,
        "by_k": results,
        "reading": reading,
    }


def analyse_q4(extinct_worlds: list[dict]) -> dict:
    final_deaths = Counter()
    total_deaths = 0

    for r in extinct_worlds:
        t_ext = r["final_tick"] // 52
        for d in r.get("deaths", []):
            d_yr = d[0]
            cause = d[1]
            if d_yr >= t_ext - 9:
                final_deaths[cause] += 1
                total_deaths += 1

    shares = {}
    for c in CAUSES:
        count = final_deaths.get(c, 0)
        shares[c] = (count, count / total_deaths if total_deaths else 0.0)

    old_age_share = shares["old age"][1]
    if old_age_share >= 0.40:
        reading = "natural attrition following reproductive failure"
    else:
        reading = "not confirmed"

    return {
        "total_deaths": total_deaths,
        "shares": shares,
        "reading": reading,
    }


def run(set_name: str):
    print(f"Loading {set_name} worlds...")
    worlds = load_worlds(set_name)
    print(f"Loaded {len(worlds)} worlds.")

    extinct = [w for w in worlds if is_extinct(w)]
    surviving = [w for w in worlds if not is_extinct(w)]
    print(f"Extinct: {len(extinct)}, Surviving: {len(surviving)}")

    q1 = analyse_q1(extinct)
    q2 = analyse_q2(extinct)
    q3 = analyse_q3(worlds)
    q4 = analyse_q4(extinct)

    # Format report
    out_lines = [
        f"# TL1 Results — {set_name.capitalize()} Set",
        "",
        f"**Sample:** {len(worlds)} control worlds ({len(extinct)} extinct, {len(surviving)} surviving to year 120).",
        "",
        "---",
        "",
        "## Q1. The Reproductive Gap (ΔT = T_extinct − T_last_birth)",
        "",
        f"- **Median ΔT:** {q1['median']:.1f} years (mean {q1['mean']:.1f} years)",
        f"- **ΔT ≥ 20 years:** {q1['ge_20_share']*100:.1f}% ({q1['ge_20_count']} / {q1['n']} extinct worlds)",
        f"- **ΔT < 10 years:** {q1['lt_10_share']*100:.1f}% ({q1['lt_10_count']} / {q1['n']} extinct worlds)",
        f"- **Frozen Reading:** **{q1['reading']}**",
        "",
        "---",
        "",
        "## Q2. Mate Availability at Last Birth (t = T_last_birth)",
        "",
        f"- **Qualifying extinct worlds (`women_single > 0` at t = T_last_birth):** {q2['n_qualifying']} / {q2['n_extinct']} ({q2['n_qualifying']/q2['n_extinct']*100:.1f}%)",
        f"- **Mean eligible share:** {q2['mean_share']*100:.1f}% (median {q2['median_share']*100:.1f}%)",
        "- **Distribution across qualifying worlds:**",
        f"  - Share = 100% (all single women had eligible men): {q2['full_count']} / {q2['n_qualifying']} ({q2['full_count']/q2['n_qualifying']*100:.1f}%)",
        f"  - 0% < Share < 100%: {q2['partial_count']} / {q2['n_qualifying']} ({q2['partial_count']/q2['n_qualifying']*100:.1f}%)",
        f"  - Share = 0% (mate pool exhausted): {q2['zero_count']} / {q2['n_qualifying']} ({q2['zero_count']/q2['n_qualifying']*100:.1f}%)",
        f"- **Frozen Reading:** **{q2['reading']}**",
        "",
        "---",
        "",
        "## Q3. Point of No Return: First Episode of K-Year Birth Hiatus",
        "",
        "| K (years) | Experienced Hiatus (n / N) | Subsequent Birth (n / N) | Survival to Year 120 (n / N) |",
        "|---|---|---|---|",
    ]

    for k in (5, 10, 15):
        bk = q3["by_k"][k]
        out_lines.append(
            f"| {k} | {bk['n_exp']} / {q3['n_total']} ({bk['n_exp']/q3['n_total']*100:.1f}%) | "
            f"{bk['birth_recovery_rate']*100:.1f}% ({bk['birth_recovered_count']} / {bk['n_exp']}) | "
            f"{bk['surv_recovery_rate']*100:.1f}% ({bk['surv_recovered_count']} / {bk['n_exp']}) |"
        )

    out_lines.extend([
        "",
        f"- **Frozen Reading (K = 10 survival):** **{q3['reading']}**",
        "",
        "---",
        "",
        "## Q4. Causes of Final Deaths (Last 10 Years Before Extinction)",
        "",
        f"- **Total deaths in final decade across all {len(extinct)} extinct worlds:** {q4['total_deaths']}",
        "",
        "| Cause | Death Count | Share of Final Deaths |",
        "|---|---|---|",
    ])

    for c in CAUSES:
        cnt, shr = q4["shares"][c]
        out_lines.append(f"| `{c}` | {cnt} | {shr*100:.1f}% |")

    out_lines.extend([
        "",
        f"- **Frozen Reading:** **{q4['reading']}**",
        "",
    ])

    out_path = HERE / f"results_{set_name}.md"
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"Results written to {out_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("discovery", "holdout"):
        print("Usage: python analyse_tl1.py [discovery|holdout]")
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "holdout":
        disc_file = HERE / "results_discovery.md"
        if not disc_file.exists():
            print("ERROR: results_discovery.md must exist and be committed before running holdout!")
            sys.exit(1)

    run(mode)
