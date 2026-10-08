"""HF3 analysis with the frozen decision rule (questions.md, `HF3-questions`). Written before any data.

Operational details written with this file, before data:
- Q1 "food received as gifts per adult-week": total gift food received by adults ÷ adult-weeks.
- Channels: G1 = share of adult-weeks with a short person within reach; G2 = share with a surplus; G3 = gifts given per
  opportunity (adult-week with both). Each as H ÷ C.
- Rescue within reach: share of starving adult-weeks with another adult holding a surplus within reach, H ÷ C.

  python experiments/HF3_gifts/analyse_hf3.py discovery   (or: holdout, or: both)
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_hf3 import DISCOVERY, HOLDOUT, OUT  # noqa: E402


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
    w(f"Replays reproduce saved runs (where saved) and code unchanged: **{'yes' if ok else 'NO'}**. Adult-weeks: "
      f"H {nh['adult_weeks']:,}, C {nc['adult_weeks']:,}. Populations: "
      + "; ".join(f"{a['seed']} H{a['pops']} C{b['pops']}" for a, b in zip(RH, RC)) + ".\n")
    q = {
        "Q1 gift food received per adult-week": (div(nh["gift_food_received_by_adults"], nh["adult_weeks"]),
                                                 div(nc["gift_food_received_by_adults"], nc["adult_weeks"])),
        "Q1 gift food given per adult-week": (div(nh["gift_food_given"], nh["adult_weeks"]),
                                              div(nc["gift_food_given"], nc["adult_weeks"])),
        "Q2 G1 meetings: share of adult-weeks with a short person within reach": (div(nh["g1_short_near"], nh["adult_weeks"]),
                                                                                  div(nc["g1_short_near"], nc["adult_weeks"])),
        "Q2 G2 surplus: share of adult-weeks holding a surplus": (div(nh["g2_surplus"], nh["adult_weeks"]),
                                                                  div(nc["g2_surplus"], nc["adult_weeks"])),
        "Q2 G3 choice: gifts given per opportunity": (div(nh["gifts_in_opportunity"], nh["opportunity"]),
                                                      div(nc["gifts_in_opportunity"], nc["opportunity"])),
        "Q2 share of adult-weeks that are opportunities": (div(nh["opportunity"], nh["adult_weeks"]),
                                                           div(nc["opportunity"], nc["adult_weeks"])),
        "Q3 starving adult-weeks with a potential giver within reach": (div(nh["starving_giver_near"], nh["starving"]),
                                                                        div(nc["starving_giver_near"], nc["starving"])),
        "Q3 starving share of adult-weeks": (div(nh["starving"], nh["adult_weeks"]), div(nc["starving"], nc["adult_weeks"])),
        "Q5 starving share, adults with a gift in the last 8 weeks": (div(nh["starving_recent_True"], nh["aw_recent_True"]),
                                                                       div(nc["starving_recent_True"], nc["aw_recent_True"])),
        "Q5 starving share, adults with no gift in the last 8 weeks": (div(nh["starving_recent_False"], nh["aw_recent_False"]),
                                                                        div(nc["starving_recent_False"], nc["aw_recent_False"])),
    }
    w("| measure | H (home base) | C (control) | H ÷ C |")
    w("|---|---|---|---|")
    for lab, (a, b) in q.items():
        w(f"| {lab} | {f(a)} | {f(b)} | {f(div(a, b)) if a is not None and b else '–'} |")
    tot = lambda n: n["gift_partner"] + n["gift_kin"] + n["gift_other"]
    sh = lambda n: " / ".join(f(div(n[f"gift_{k}"], tot(n)), 2) for k in ("partner", "kin", "other"))
    w(f"| Q4 gift food by relation (partner / kin / other) | {sh(nh)} | {sh(nc)} | – |")
    sm = lambda n: f(div(n["gift_samehome_True"], n["gift_samehome_True"] + n["gift_samehome_False"]), 2)
    w(f"| Q4 share of gift food (both with a couple home) within the same home | {sm(nh)} | {sm(nc)} | – |")
    w(f"| Q4 distance between giver's and recipient's homes (different homes) | "
      f"{f(div(nh['gift_homes_dist_sum'], nh['gift_homes_dist_n']), 2)} | {f(div(nc['gift_homes_dist_sum'], nc['gift_homes_dist_n']), 2)} | – |")
    r = lambda k: div(q[k][0], q[k][1]) if q[k][0] is not None and q[k][1] else None
    gifts = r("Q1 gift food received per adult-week")
    rescue = r("Q3 starving adult-weeks with a potential giver within reach")
    ch = {"G1 meetings": r("Q2 G1 meetings: share of adult-weeks with a short person within reach"),
          "G2 surplus": r("Q2 G2 surplus: share of adult-weeks holding a surplus"),
          "G3 choice": r("Q2 G3 choice: gifts given per opportunity")}
    explain = gifts is not None and rescue is not None and gifts <= 0.8 and rescue <= 0.8
    low = min((v, k) for k, v in ch.items() if v is not None)
    w(f"\nRule quantities: gifts received H ÷ C {f(gifts)} (≤ 0.8); rescue within reach H ÷ C {f(rescue)} (≤ 0.8) → "
      f"gifts explain the hunger **{'yes' if explain else 'no'}**. Channels H ÷ C: "
      + ", ".join(f"{k} {f(v)}" for k, v in ch.items()) + f"; lowest {low[1]} ({f(low[0])}).\n")
    return explain, low, ok


def main(which="both", out=OUT, write=True):
    L = ["# HF3 — Why gifts fell under HB1: results (generated by `analyse_hf3.py`)\n"]
    checks = (out / "checks.txt").read_text(encoding="utf-8")
    L.append(f"Observer read-only (H and C, two seeds): **{'yes' if 'CHANGES' not in checks and checks.count('READ-ONLY') >= 4 else 'NO'}**.\n")
    sets = {"discovery": [("discovery", DISCOVERY)], "holdout": [("holdout", HOLDOUT)],
            "both": [("discovery", DISCOVERY), ("holdout", HOLDOUT)]}[which]
    res = {name: section(name, seeds, out, L) for name, seeds in sets}
    if len(res) == 2:
        (ed, ld, okd), (eh, lh, okh) = res["discovery"], res["holdout"]
        L.append("## Frozen decision rule\n")
        L.append(f"Gifts explain the hunger: discovery {'yes' if ed else 'no'}, holdout {'yes' if eh else 'no'} → "
                 f"**{'supported' if ed and eh else 'not supported: gifts do not explain the hunger; the creator decides'}**.")
        if ld[1] == lh[1] and ld[0] <= 0.9 and lh[0] <= 0.9:
            L.append(f"\nChannel: **{ld[1]}** (lowest in both sets, {f(ld[0])} / {f(lh[0])}, ≤ 0.9).")
        else:
            L.append(f"\nChannel: **not identified** (lowest: discovery {ld[1]} {f(ld[0])}, holdout {lh[1]} {f(lh[0])}).")
        if not (okd and okh):
            L.append("\n**A hard stop was hit: recorded, not interpreted.**")
    text = "\n".join(L) + "\n"
    if write:
        (HERE / f"results_{which}.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "both")
