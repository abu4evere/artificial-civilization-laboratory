"""CP1 — Courtship-to-pairing pipeline audit (questions.md, frozen as `CP1-frozen`).

Read-only on saved v2 control worlds from RT1b (seeds 5701-5956), FX2 (6001-6256) and FX3 (7301-7556).
Decomposes every fertile woman-week into the six gates G1-G6 and reports extinct vs surviving.

  python experiments/CP1_courtship_pipeline/analyse_cp1.py discovery   -> results_discovery.md (commit before holdout)
  python experiments/CP1_courtship_pipeline/analyse_cp1.py holdout     -> results_holdout.md (needs results_discovery.md)
"""
from __future__ import annotations

import json
import re
import statistics
import sys
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

MIN_WW = 100  # worlds with fewer fertile woman-weeks total are excluded from averages


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


def world_shares(r: dict) -> dict:
    """One row per world: pooled sums over all years, then the gate shares.
    G1-G3 split 'single fertile woman-years' using the snapshot counts; G4-G6 use weekly sums."""

    ww = 0.0            # fertile woman-weeks (all)
    r_no_partner = 0.0  # fertile woman-weeks with no partner
    r_apart = 0.0       # fertile woman-weeks partner-alive but apart
    r_pregnant = 0.0
    r_nursing = 0.0
    r_starving = 0.0
    r_eligible = 0.0

    ws_total = 0        # single fertile women-year snapshots pooled
    ws_no_mate = 0      # of those, no eligible man anywhere
    ws_no_mate_near = 0 # of those, no eligible man within perception (superset of no_mate)

    births = 0

    for y in r.get("years", {}).values():
        ww += y.get("woman_weeks", 0)
        r_no_partner += y.get("r_no_partner", 0)
        r_apart += y.get("r_apart", 0)
        r_pregnant += y.get("r_pregnant", 0)
        r_nursing += y.get("r_nursing", 0)
        r_starving += y.get("r_starving", 0)
        r_eligible += y.get("r_eligible", 0)

        ws_total += y.get("women_single", 0)
        ws_no_mate += y.get("women_single_no_mate", 0)
        ws_no_mate_near += y.get("women_single_no_mate_near", 0)

        births += y.get("births", 0)

    # Share of single fertile woman-YEARS at each sub-gate (G1, G2, G3)
    # G1: no eligible man alive anywhere
    # G2: eligible man alive but none within perception (= no_mate_near minus no_mate)
    # G3: eligible man within perception, still single
    # Each is a share of total fertile woman-WEEKS, so the three gates sum to r_no_partner / ww
    if ws_total > 0 and ww > 0:
        single_fraction = r_no_partner / ww  # share of woman-weeks spent single
        g1 = (ws_no_mate / ws_total) * single_fraction
        g2 = ((ws_no_mate_near - ws_no_mate) / ws_total) * single_fraction
        g3 = ((ws_total - ws_no_mate_near) / ws_total) * single_fraction
    else:
        g1 = g2 = g3 = 0.0

    # Partnered-with-living-partner weeks (lower bound: ww - r_no_partner;
    # on these saved worlds r_partner_dead is not stored, so some weeks that
    # had a partner-dead state fall into the residual below).
    partnered = max(0.0, ww - r_no_partner)

    # G4: co-residence failure, as share of all woman-weeks
    g4 = r_apart / ww if ww > 0 else 0.0

    # G5: physiological blockers (starving + nursing), as share of all woman-weeks
    g5 = (r_starving + r_nursing) / ww if ww > 0 else 0.0

    # G6a: eligible-this-week (all gates passed), share of all woman-weeks
    # G6b: pregnant (an outcome of a prior eligible week), share of all woman-weeks
    g6_eligible = r_eligible / ww if ww > 0 else 0.0
    g6_pregnant = r_pregnant / ww if ww > 0 else 0.0

    # Residual (r_partner_dead + r_low_health + r_partner_child, not stored on these worlds)
    accounted = r_no_partner + r_apart + r_pregnant + r_nursing + r_starving + r_eligible
    residual = max(0.0, ww - accounted) / ww if ww > 0 else 0.0

    # Births per partnered fertile woman-year
    partnered_wy = partnered / 52.0
    births_per_pwy = (births / partnered_wy) if partnered_wy > 0 else 0.0
    # Births per fertile woman-year (all)
    births_per_wy = (births / (ww / 52.0)) if ww > 0 else 0.0

    return {
        "seed": r.get("seed"),
        "extinct": is_extinct(r),
        "ww": ww,
        "r_no_partner_share": (r_no_partner / ww) if ww > 0 else 0.0,
        "g1": g1,
        "g2": g2,
        "g3": g3,
        "g4": g4,
        "g5": g5,
        "g6_eligible": g6_eligible,
        "g6_pregnant": g6_pregnant,
        "residual": residual,
        "births_per_pwy": births_per_pwy,
        "births_per_wy": births_per_wy,
    }


def cohort_summary(rows: list[dict], label: str) -> dict:
    """Per-world means (equal weight per world), restricted to worlds with >= MIN_WW woman-weeks."""
    kept = [r for r in rows if r["ww"] >= MIN_WW]
    excluded = len(rows) - len(kept)

    def mean(key):
        xs = [r[key] for r in kept]
        return statistics.mean(xs) if xs else 0.0

    def median(key):
        xs = [r[key] for r in kept]
        return statistics.median(xs) if xs else 0.0

    return {
        "label": label,
        "n_worlds": len(rows),
        "n_included": len(kept),
        "n_excluded_low_ww": excluded,
        "mean_ww": statistics.mean([r["ww"] for r in kept]) if kept else 0.0,
        "g1": mean("g1"),
        "g2": mean("g2"),
        "g3": mean("g3"),
        "g4": mean("g4"),
        "g5": mean("g5"),
        "g6_eligible": mean("g6_eligible"),
        "g6_pregnant": mean("g6_pregnant"),
        "residual": mean("residual"),
        "r_no_partner_share": mean("r_no_partner_share"),
        "births_per_pwy": mean("births_per_pwy"),
        "births_per_pwy_median": median("births_per_pwy"),
        "births_per_wy": mean("births_per_wy"),
    }


def pick_bottleneck(ext: dict, surv: dict) -> dict:
    """Among G1-G4, the gate with the largest absolute excess (extinct - surviving)."""
    gates = ["g1", "g2", "g3", "g4"]
    excesses = {g: ext[g] - surv[g] for g in gates}
    best = max(gates, key=lambda g: excesses[g])
    return {"gate": best, "excesses": excesses, "excess": excesses[best]}


def run(set_name: str):
    print(f"Loading {set_name} worlds...")
    worlds = load_worlds(set_name)
    print(f"Loaded {len(worlds)} worlds.")

    rows = [world_shares(w) for w in worlds]
    extinct = [r for r in rows if r["extinct"]]
    surviving = [r for r in rows if not r["extinct"]]
    print(f"Extinct: {len(extinct)}, Surviving: {len(surviving)}")

    s_ext = cohort_summary(extinct, "extinct")
    s_surv = cohort_summary(surviving, "surviving")
    s_all = cohort_summary(rows, "all")

    verdict = pick_bottleneck(s_ext, s_surv)

    # Reading rule, discovery vs holdout
    if set_name == "discovery":
        gates_sorted = sorted(verdict["excesses"].items(), key=lambda kv: -kv[1])
        top, second = gates_sorted[0], gates_sorted[1]
        if verdict["excess"] >= 0.05 and top[1] > second[1]:
            reading = f"**Bottleneck in extinct worlds: {verdict['gate'].upper()}** (excess {verdict['excess']*100:+.1f} pp; next: {second[0].upper()} {second[1]*100:+.1f} pp)"
        else:
            reading = f"**Mixed** (top gate {verdict['gate'].upper()} excess {verdict['excess']*100:+.1f} pp; threshold 5.0 pp not met OR tied with next)"
    else:
        # Holdout vs discovery check happens in findings.md, not here
        reading = f"Top excess gate in extinct: {verdict['gate'].upper()} ({verdict['excess']*100:+.1f} pp). Confirmation against discovery done in findings.md."

    out_lines = [
        f"# CP1 Results — {set_name.capitalize()} Set",
        "",
        f"**Sample:** {len(worlds)} control worlds "
        f"({len(extinct)} extinct, {len(surviving)} surviving to year 120). "
        f"Worlds with < {MIN_WW} fertile woman-weeks total are excluded from averages "
        f"(extinct: {s_ext['n_excluded_low_ww']}, surviving: {s_surv['n_excluded_low_ww']}, all: {s_all['n_excluded_low_ww']}).",
        "",
        "---",
        "",
        "## Pipeline gates: per-world mean share of fertile woman-weeks",
        "",
        "Shares are **per-world means** (equal weight per world). G1+G2+G3 sum to the share of woman-weeks spent single "
        "(partnerless). G4 is partner-alive-but-apart. G5 is physiological blockers (starving + nursing). "
        "G6-eligible counts weeks where every gate is passed; G6-pregnant counts weeks already carrying.",
        "",
        "| Gate | Name | Extinct | Surviving | Excess (ext − surv) |",
        "|---|---|---:|---:|---:|",
        f"| G1 | Mate pool: no eligible man alive anywhere | {s_ext['g1']*100:.2f}% | {s_surv['g1']*100:.2f}% | {(s_ext['g1']-s_surv['g1'])*100:+.2f} pp |",
        f"| G2 | Encounter: man alive but not within sight | {s_ext['g2']*100:.2f}% | {s_surv['g2']*100:.2f}% | {(s_ext['g2']-s_surv['g2'])*100:+.2f} pp |",
        f"| G3 | Courtship + acceptance: man within sight, still single | {s_ext['g3']*100:.2f}% | {s_surv['g3']*100:.2f}% | {(s_ext['g3']-s_surv['g3'])*100:+.2f} pp |",
        f"| G4 | Co-residence: partnered, apart from partner | {s_ext['g4']*100:.2f}% | {s_surv['g4']*100:.2f}% | {(s_ext['g4']-s_surv['g4'])*100:+.2f} pp |",
        f"| G5 | Physiological blockers (starving + nursing) | {s_ext['g5']*100:.2f}% | {s_surv['g5']*100:.2f}% | {(s_ext['g5']-s_surv['g5'])*100:+.2f} pp |",
        f"| G6-eligible | All gates passed, could conceive | {s_ext['g6_eligible']*100:.2f}% | {s_surv['g6_eligible']*100:.2f}% | {(s_ext['g6_eligible']-s_surv['g6_eligible'])*100:+.2f} pp |",
        f"| G6-pregnant | Already pregnant | {s_ext['g6_pregnant']*100:.2f}% | {s_surv['g6_pregnant']*100:.2f}% | {(s_ext['g6_pregnant']-s_surv['g6_pregnant'])*100:+.2f} pp |",
        f"| residual | r_partner_dead + r_low_health + r_partner_child (not stored) | {s_ext['residual']*100:.2f}% | {s_surv['residual']*100:.2f}% | {(s_ext['residual']-s_surv['residual'])*100:+.2f} pp |",
        "",
        f"**Total share of woman-weeks spent single (partnerless):** extinct {s_ext['r_no_partner_share']*100:.1f}%, surviving {s_surv['r_no_partner_share']*100:.1f}%.",
        f"**Mean fertile woman-weeks per world (included):** extinct {s_ext['mean_ww']:.0f}, surviving {s_surv['mean_ww']:.0f}.",
        "",
        "---",
        "",
        "## Births per partnered fertile woman-year",
        "",
        f"- **Extinct:** mean {s_ext['births_per_pwy']:.3f}, median {s_ext['births_per_pwy_median']:.3f}",
        f"- **Surviving:** mean {s_surv['births_per_pwy']:.3f}, median {s_surv['births_per_pwy_median']:.3f}",
        f"- **Overall (per fertile woman-year, not just partnered):** extinct {s_ext['births_per_wy']:.3f}, surviving {s_surv['births_per_wy']:.3f}",
        "",
        "---",
        "",
        "## Frozen reading",
        "",
        reading,
        "",
        "Full ranking of (extinct − surviving) excesses among G1–G4:",
        "",
    ]
    for g, e in sorted(verdict["excesses"].items(), key=lambda kv: -kv[1]):
        out_lines.append(f"- **{g.upper()}:** {e*100:+.2f} pp")
    out_lines.append("")

    out_path = HERE / f"results_{set_name}.md"
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"Results written to {out_path}")
    print(f"\nTop G1-G4 excesses (ext - surv):")
    for g, e in sorted(verdict["excesses"].items(), key=lambda kv: -kv[1]):
        print(f"  {g.upper()}: {e*100:+.2f} pp")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("discovery", "holdout"):
        print("Usage: python analyse_cp1.py [discovery|holdout]")
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "holdout":
        disc_file = HERE / "results_discovery.md"
        if not disc_file.exists():
            print("ERROR: results_discovery.md must exist and be committed before running holdout!")
            sys.exit(1)

    run(mode)
