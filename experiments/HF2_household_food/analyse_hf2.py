"""HF2 analysis with the frozen decision rule (questions.md, `HF2-questions`). Written before any data.

  python experiments/HF2_household_food/analyse_hf2.py discovery   (or: holdout, or: both)
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_hf2 import DISCOVERY, GROUPS, HOLDOUT, OUT  # noqa: E402


def f(x, d=3):
    return "–" if x is None else f"{x:.{d}f}"


def div(a, b):
    return a / b if b else None


def pooled(arm, seeds, out):
    n = Counter()
    R = []
    for s in seeds:
        r = json.loads((out / f"{arm}_seed_{s}.json").read_text(encoding="utf-8"))
        n.update(r["n"])
        R.append(r)
    return n, R


def section(name, seeds, out, L):
    w = L.append
    nh, RH = pooled("h", seeds, out)
    nc, RC = pooled("c", seeds, out)
    ok = all(r.get("reproduces") is not False and r["code_hash"] == r["code_hash_after"] for r in RH + RC)
    w(f"## {name} (seeds {seeds[0]}–{seeds[-1]}, first 40 years)\n")
    w(f"Replays reproduce saved runs (where saved) and code unchanged: **{'yes' if ok else 'NO'}**. "
      f"Adult-weeks: H {nh['adult_weeks']:,}, C {nc['adult_weeks']:,}. Populations: "
      + "; ".join(f"{a['seed']} H{a['pops']} C{b['pops']}" for a, b in zip(RH, RC)) + ".\n")
    aw = lambda n, k: div(n[k], n["adult_weeks"])
    rows = [("Q1 food in per adult-week, total", aw(nh, "in_total"), aw(nc, "in_total"))]
    for src in ("forage", "hunt", "take", "gift", "steal"):
        rows.append((f"Q1 food in per adult-week from {src}", aw(nh, f"in_{src}"), aw(nc, f"in_{src}")))
    rows += [("Q1 meat's share of food in", div(nh["in_hunt"], nh["in_total"]), div(nc["in_hunt"], nc["in_total"])),
             ("Q2 dependants per carer-week", div(nh["dependants"], nh["carer_weeks"]), div(nc["dependants"], nc["carer_weeks"])),
             ("Q2 dependants' need ÷ carer's food in (week)", div(nh["dep_need"], nh["carer_in"]), div(nc["dep_need"], nc["carer_in"])),
             ("Q2 share of carer-weeks starving while all dependants fed", div(nh["carer_starving_deps_fed"], nh["carer_weeks"]),
              div(nc["carer_starving_deps_fed"], nc["carer_weeks"])),
             ("Q2 share of adult-weeks that are carer-weeks", div(nh["carer_weeks"], nh["adult_weeks"]),
              div(nc["carer_weeks"], nc["adult_weeks"]))]
    for g in GROUPS:
        rows.append((f"Q3 starving per 1,000 adult-weeks, {g}s", 1000 * (div(nh[f"starving_{g}"], nh[f"aw_{g}"]) or 0),
                     1000 * (div(nc[f"starving_{g}"], nc[f"aw_{g}"]) or 0)))
        rows.append((f"Q3 adult starvation deaths, {g}s", nh[f"starve_death_{g}"], nc[f"starve_death_{g}"]))
    rows += [("Q4 food given away per adult-week", aw(nh, "given"), aw(nc, "given")),
             ("Q4 given to partner / kin / others (share)", None, None),
             ("Q4 theft suffered per adult-week", aw(nh, "stolen_from"), aw(nc, "stolen_from")),
             ("Q5 hunts per person-year", div(nh["hunts"], nh["person_weeks"] / 52), div(nc["hunts"], nc["person_weeks"] / 52)),
             ("Q5 share of adult-weeks on a hunt", aw(nh, "adult_weeks_hunting"), aw(nc, "adult_weeks_hunting")),
             ("Q5 meat per hunter per hunt", div(nh["hunter_meat"], nh["hunter_hunts"]), div(nc["hunter_meat"], nc["hunter_hunts"])),
             ("Q5 distance from couple home to hunt", div(nh["hunt_dist_sum"], nh["hunt_dist_n"]), div(nc["hunt_dist_sum"], nc["hunt_dist_n"]))]
    w("| measure | H (home base) | C (control) | H ÷ C |")
    w("|---|---|---|---|")
    for lab, a, b in rows:
        if lab.startswith("Q4 given to"):
            sh = lambda n: " / ".join(f(div(n[f'given_{k}'], n['given']), 2) for k in ("partner", "kin", "other"))
            w(f"| {lab} | {sh(nh)} | {sh(nc)} | – |")
            continue
        w(f"| {lab} | {f(a)} | {f(b)} | {f(div(a, b)) if a is not None and b else '–'} |")
    # the frozen rule's quantities
    rate = lambda n, g: 1000 * (div(n[f"starving_{g}"], n[f"aw_{g}"]) or 0)
    parts = {g: (rate(nh, g) - rate(nc, g)) * nh[f"aw_{g}"] / 1000 for g in GROUPS}
    total = sum(parts.values())
    carer_share = parts["carer"] / total if total > 0 else None
    dep_ratio = div(div(nh["dependants"], nh["carer_weeks"]), div(nc["dependants"], nc["carer_weeks"]))
    hunt_ratio = div(aw(nh, "in_hunt"), aw(nc, "in_hunt"))
    total_lower = (aw(nh, "in_total") or 0) < (aw(nc, "in_total") or 0)
    w(f"\nExcess starving adult-weeks in H over C (by the frozen weighting): {total:,.0f}; share on carers "
      f"{f(carer_share)}; on partnered adults without dependants {f(div(parts['partnered'], total))}; on unpartnered "
      f"{f(div(parts['single'], total))}.\n")
    mouths = dep_ratio is not None and dep_ratio >= 1.2 and carer_share is not None and carer_share >= 2 / 3
    meat = hunt_ratio is not None and hunt_ratio <= 0.8 and total_lower
    w(f"Rule quantities: dependants per carer-week H ÷ C {f(dep_ratio)} (≥ 1.2), carers' share of the excess {f(carer_share)} "
      f"(≥ 0.667) → mouths **{'yes' if mouths else 'no'}**; food from hunting H ÷ C {f(hunt_ratio)} (≤ 0.8), total food "
      f"in lower in H {'yes' if total_lower else 'no'} → meat **{'yes' if meat else 'no'}**.\n")
    return mouths, meat, ok


def main(which="both", out=OUT, write=True):
    L = ["# HF2 — The household food balance: results (generated by `analyse_hf2.py`)\n"]
    checks = (out / "checks.txt").read_text(encoding="utf-8")
    L.append(f"Observer read-only (H and C, two seeds): **{'yes' if 'CHANGES' not in checks and checks.count('READ-ONLY') >= 4 else 'NO'}**.\n")
    sets = {"discovery": [("discovery", DISCOVERY)], "holdout": [("holdout", HOLDOUT)],
            "both": [("discovery", DISCOVERY), ("holdout", HOLDOUT)]}[which]
    res = {name: section(name, seeds, out, L) for name, seeds in sets}
    if len(res) == 2:
        (md, ed, okd), (mh, eh, okh) = res["discovery"], res["holdout"]
        mouths, meat = md and mh, ed and eh
        L.append("## Frozen decision rule\n")
        v = ("**Both** (mouths and meat)" if mouths and meat else "**Mouths**" if mouths else "**Meat**" if meat else
             "**Neither:** the hunger has yet another cause; reported as such, the creator decides")
        L.append(f"Mouths: discovery {'yes' if md else 'no'}, holdout {'yes' if mh else 'no'}. Meat: discovery "
                 f"{'yes' if ed else 'no'}, holdout {'yes' if eh else 'no'}. Verdict: {v}.")
        if not (okd and okh):
            L.append("\n**A hard stop was hit: recorded, not interpreted.**")
    text = "\n".join(L) + "\n"
    if write:
        (HERE / f"results_{which}.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "both")
