"""NB2-A analysis (questions.md, NB2A-frozen). Written before the autopsy's data. Descriptive.

  python experiments/NB2A_autopsy/analyse_nb2a.py [--dir <output>]
"""
from __future__ import annotations

import glob
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
OUT = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
ARMS = ("c", "s", "n")
SEEDS = tuple(range(25601, 25617))
VIOLENT = ("killed", "violence")


def main():
    runs = {a: {} for a in ARMS}
    for f in sorted(glob.glob(str(OUT / "*_seed_*.json"))):
        r = json.load(open(f))
        runs[r["arm"]][r["seed"]] = r
    present = all(sorted(runs[a]) == list(SEEDS) for a in ARMS)
    same = all(r["same_as_nb2"] for a in ARMS for r in runs[a].values())
    # Correction 1 (appended after the data, 11 November 2026; questions.md): with --exact-only, the replays that do not
    # end with NB2's fingerprint are left out and named; with --all, every replay is kept. See questions.md.
    dropped = [f"{a}:{s}" for a in ARMS for s, r in runs[a].items() if not r["same_as_nb2"]]
    if "--exact-only" in sys.argv or "--all" in sys.argv:
        if "--exact-only" in sys.argv:
            runs = {a: {s: r for s, r in runs[a].items() if r["same_as_nb2"]} for a in ARMS}
        same = True
    mode = "exact-only" if "--exact-only" in sys.argv else ("all" if "--all" in sys.argv else "frozen")
    L = ["# NB2-A: why did NB2's people die out? (autopsy results)", "",
         f"Mode: **{mode}** (correction 1 in questions.md). Replays not ending with NB2's fingerprint: {dropped}", "",
         f"- All 48 replays present: **{'yes' if present else 'NO'}**; worlds used: {sum(len(v) for v in runs.values())}",
         f"- Every replay ends exactly as NB2's world did (read-only recorders): **{'yes' if same else 'NO'}**", ""]
    if not (present and same):
        L.append("**NOT VALID: nothing is concluded.**")
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    # deaths by cause and age, whole lives
    L += ["## Deaths by cause (all worlds, whole lives; share of deaths in the age group)", ""]
    shares = {}
    for grp in ("16+", "12_15", "u12"):
        L += [f"**Age {grp}:**", "", "| cause | " + " | ".join(ARMS) + " |", "|---|" + "---|" * len(ARMS)]
        tot = {a: Counter() for a in ARMS}
        for a in ARMS:
            for r in runs[a].values():
                for dec in r["decades"].values():
                    for k, v in dec.items():
                        if k.startswith("death:") and k.endswith(":" + grp):
                            tot[a][k.split(":")[1]] += v
        causes = sorted(set().union(*[set(t) for t in tot.values()]))
        for cause in causes:
            L.append(f"| {cause} | " + " | ".join(
                f"{tot[a][cause] / max(1, sum(tot[a].values())):.3f} ({tot[a][cause]})" for a in ARMS) + " |")
        L.append(f"| all deaths | " + " | ".join(str(sum(tot[a].values())) for a in ARMS) + " |")
        L.append("")
        shares[grp] = tot
    # the two frozen readings, for people 12 and over
    def share12(a, causes):
        t = shares["16+"][a] + shares["12_15"][a]
        return sum(t[c] for c in causes) / max(1, sum(t.values()))
    viol = {a: share12(a, VIOLENT) for a in ARMS}
    starv = {a: share12(a, ("starvation",)) for a in ARMS}
    vio_drives = viol["n"] >= 0.25 and viol["n"] > 5 * viol["c"]
    sta_drives = starv["n"] >= 0.25 and starv["n"] > 5 * starv["c"]
    L += ["## Readings (frozen; people 12 and over)", "",
          f"- Violent deaths' share: " + ", ".join(f"{a} {viol[a]:.3f}" for a in ARMS)
          + f". **Violence drives the collapse: {'yes' if vio_drives else 'no'}.**",
          f"- Starvation's share: " + ", ".join(f"{a} {starv[a]:.3f}" for a in ARMS)
          + f". **Starvation drives it: {'yes' if sta_drives else 'no'}.**", "",
          "Rule: a cause drives the collapse if it is at least a quarter of all deaths of people 12 and over in n and "
          "more than 5 times its share in c.", ""]
    # attacks
    L += ["## The attacks", "", "| | " + " | ".join(ARMS) + " |", "|---|" + "---|" * len(ARMS)]
    rows = {a: [x for r in runs[a].values() for x in r["attacks"]] for a in ARMS}

    def frac(a, f):
        xs = rows[a]
        return f"{sum(1 for x in xs if f(x)) / len(xs):.3f}" if xs else "-"
    L.append("| attacks (all worlds) | " + " | ".join(str(len(rows[a])) for a in ARMS) + " |")
    for lab, f in (("chosen (not retaliation)", lambda x: x["source"] == "chosen"),
                   ("the old brain would never have offered it (grudge <= 0.15)", lambda x: not x["old_brain_offers"]),
                   ("against kin", lambda x: x["kin"] > 0), ("against one's partner", lambda x: x["partner"]),
                   ("by a child under 12", lambda x: x["a_age"] == "u12"), ("by a teen 12-15", lambda x: x["a_age"] == "12_15"),
                   ("against a child under 12", lambda x: x["b_age"] == "u12"),
                   ("the target was killed", lambda x: x["killed_target"]),
                   ("the attacker was killed", lambda x: x["killed_attacker"]),
                   ("the attacker was hungry (hunger > 0.5)", lambda x: x["hunger"] > 0.5)):
        L.append(f"| {lab} | " + " | ".join(frac(a, f) for a in ARMS) + " |")
    # starvation
    L += ["", "## Deaths by starvation", "", "| | " + " | ".join(ARMS) + " |", "|---|" + "---|" * len(ARMS)]
    st = {a: [x for r in runs[a].values() for x in r["starved"]] for a in ARMS}

    def sfrac(a, f):
        xs = st[a]
        return f"{sum(1 for x in xs if f(x)) / len(xs):.3f}" if xs else "-"
    L.append("| deaths by starvation | " + " | ".join(str(len(st[a])) for a in ARMS) + " |")
    for lab, f in (("a child under 12", lambda x: x["age"] == "u12"),
                   ("kin within reach had more than twice their need", lambda x: x["kin_with_surplus_near"]),
                   ("held no food", lambda x: x["food_held"] == 0),
                   ("foraged in under 2 of the last 8 weeks",
                    lambda x: x["forage_share_8w"] is not None and x["forage_share_8w"] < 0.25)):
        L.append(f"| {lab} | " + " | ".join(sfrac(a, f) for a in ARMS) + " |")
    # children's and teens' choices, first 100 years
    L += ["", "## What children (3-11) and teens (12-15) chose in the first 100 years (share of weeks)", ""]
    for grp in ("3_11", "12_15"):
        tot = {a: Counter() for a in ARMS}
        for a in ARMS:
            for r in runs[a].values():
                for k, v in r["kid_acts"].items():
                    dec, g = k.split(":")
                    if g == grp and int(dec) < 10:
                        for act, n in v.items():
                            tot[a][act] += n
        acts = sorted(set().union(*[set(t) for t in tot.values()]))
        L += [f"**{grp}:**", "", "| action | " + " | ".join(ARMS) + " |", "|---|" + "---|" * len(ARMS)]
        for act in acts:
            L.append(f"| {act} | " + " | ".join(f"{tot[a][act] / max(1, sum(tot[a].values())):.3f}" for a in ARMS) + " |")
        L.append("")
    (HERE / ("results_all48.md" if mode == "all" else "results.md")).write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
