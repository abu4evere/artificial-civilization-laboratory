"""PF2 analysis (questions.md, frozen as `PF2-frozen`): what people do instead of courting, by arm, in both sets.

  python experiments/PF2_instead_of_courting/analyse_pf2.py     -> results.md (outcomes shown only if every check passes)
"""
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_pf2 import ARMS, CLASSES, DISCOVERY, HOLDOUT, OUT, REASONS  # noqa: E402

GROUP_ORDER = ("subsistence", "rest", "other social", "movement", "other", "court (someone else)")


def load(seeds):
    R, missing = {}, []
    for a in ARMS:
        for s in seeds:
            f = OUT / f"{a}_seed_{s}.json"
            if f.exists():
                R[(a, s)] = json.loads(f.read_text(encoding="utf-8"))
            else:
                missing.append(f.name)
    return R, missing


def main():
    out = ["# PF2 — what people do instead of courting: results", "",
           "Frozen as `PF2-frozen`. run_pf2.py, analyse_pf2.py.", "", "## Validity", ""]
    zero = OUT / "zero.txt"
    z_ok = zero.exists() and "All: PASS" in zero.read_text(encoding="utf-8")
    sets = {"discovery": load(DISCOVERY), "holdout": load(HOLDOUT)}
    present = all(not m for _R, m in sets.values())
    rs = [r for R, _m in sets.values() for r in R.values()]
    repro = bool(rs) and all(r.get("reproduces") is True for r in rs)
    fps = {r["code_hash"] for r in rs} | {r["code_hash_after"] for r in rs}
    out += [f"- Zero check (logging and observer change nothing against `code_mb1b`): **{'yes' if z_ok else 'NO'}**",
            f"- All 64 worlds present: **{'yes' if present else 'NO'}**",
            f"- Every replay equals MB1b's saved world: **{'yes' if repro else 'NO'}** "
            f"({sum(r.get('reproduces') is True for r in rs)} of {len(rs)})",
            f"- One code fingerprint (`code_pf2`): **{'yes' if len(fps) == 1 else 'NO'}**", ""]
    if not (z_ok and present and repro and len(fps) == 1):
        out.append("**Not valid: no outcome is shown.**")
        (HERE / "results.md").write_text("\n".join(out) + "\n", encoding="utf-8")
        print("\n".join(out))
        return
    out += ["**Valid.**", ""]
    wins = {}
    for name, (R, _m) in sets.items():
        out += [f"## {name.capitalize()}", "", "**Q1: was courting offered?** (share of S5 weeks)", "",
                "| arm | median alive at the end | S5 weeks | O1 offered to her | O2 offered to him only | N not offered |",
                "|---|---|---|---|---|---|"]
        agg = {}
        for arm in ARMS:
            rr = [r for (a, _s), r in R.items() if a == arm]
            cl, won, rea, sh = Counter(), Counter(), Counter(), {"O1": [], "O2": []}
            for r in rr:
                cl.update(r["classes"])
                won.update(r["won"])
                rea.update(r["reasons"])
                for k in sh:
                    sh[k] += r["shares"][k]
            n = sum(r["s5_weeks"] for r in rr)
            agg[arm] = (cl, won, rea, sh, n)
            alive = statistics.median(r["alive_end"] for r in rr)
            out.append(f"| {arm} | {alive:.0f} | {n} | " + " | ".join(f"{cl[c] / n:.1%}" for c in CLASSES) + " |")
        out += ["", "**Q2: what won instead, when courting was offered** (share of O1 + O2 weeks; courting's median share "
                "of the choice)", "", "| arm | " + " | ".join(GROUP_ORDER) + " | what wins | courting's median share (O1 / O2) |",
                "|" + "---|" * (len(GROUP_ORDER) + 3)]
        for arm in ARMS:
            cl, won, rea, sh, n = agg[arm]
            g = Counter()
            for k, v in won.items():
                g[k.split("|", 1)[1]] += v
            tot = sum(g.values())
            top = max(GROUP_ORDER, key=lambda x: g[x])
            wins[(name, arm)] = top
            m1 = statistics.median(sh["O1"]) if sh["O1"] else None
            m2 = statistics.median(sh["O2"]) if sh["O2"] else None
            out.append(f"| {arm} | " + " | ".join(f"{g[x] / tot:.1%}" if tot else "–" for x in GROUP_ORDER)
                       + f" | {top} | {m1 if m1 is None else f'{m1:.1%}'} / {m2 if m2 is None else f'{m2:.1%}'} |")
        out += ["", "**Q3: why not offered** (share of N weeks, first failed reason)", "",
                "| arm | " + " | ".join(REASONS) + " |", "|" + "---|" * (len(REASONS) + 1)]
        for arm in ARMS:
            rea = agg[arm][2]
            tot = sum(rea.values())
            out.append(f"| {arm} | " + " | ".join(f"{rea[x] / tot:.1%}" if tot else "–" for x in REASONS) + " |")
        out.append("")
    out += ["## The frozen reading: what wins", "", "| arm | discovery | holdout | reading |", "|---|---|---|---|"]
    for arm in ARMS:
        d, h = wins[("discovery", arm)], wins[("holdout", arm)]
        out.append(f"| {arm} | {d} | {h} | {'**' + d + '** (stands)' if d == h else 'no reading (sets disagree)'} |")
    (HERE / "results.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
