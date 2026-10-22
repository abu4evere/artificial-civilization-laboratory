"""AP1 analysis (questions.md, frozen as `AP1-frozen`). Written and committed before any data. Described only.

  python experiments/AP1_why_apart/analyse_ap1.py   -> results.md
"""
import json
import random
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
CT1 = HERE.parent / "CT1_courting_nature" / "output"
SEEDS = range(8201, 8329)
ARMS = ("c", "k1")
REASONS = ("both_subsistence", "one_moving", "one_caring", "one_resting", "other")
ACTS = ("subsistence", "moving", "care", "social", "rest", "other")
EDGES = ("1", "2", "3–4", "5–8", "9–13", "14–26", "27–52", "53–104", "105+")


def boot(d):
    rng = random.Random(2026)
    m = sorted(statistics.fmean(rng.choice(d) for _ in d) for _ in range(10000))
    return statistics.fmean(d), m[249], m[9749]


def main():
    rows, missing = {a: {} for a in ARMS}, []
    for a in ARMS:
        for s in SEEDS:
            f = OUT / f"{a}_seed_{s}.json"
            if f.exists():
                rows[a][s] = json.loads(f.read_text(encoding="utf-8"))
            else:
                missing.append(f"{a} {s}")
    L = ["# AP1 — why are couples apart? Results (described)", "",
         "Frozen as `AP1-frozen`. run_ap1.py, analyse_ap1.py. CT1's C and K1 worlds (seeds 8201–8328) replayed exactly "
         "with a read-only observer; nature v3.", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero check (observer changes nothing): **{'yes' if zt else 'NO'}**")
    ok = zt and not missing
    L.append(f"- All 256 worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:6])}**")
    if not missing:
        rep = sum(1 for a in ARMS for r in rows[a].values() if r.get("reproduces") is True)
        L.append(f"- Every replay equals CT1's saved world: **{'yes' if rep == 256 else 'NO'}** ({rep} of 256)")
        ok &= rep == 256
        mism = 0
        for a in ARMS:
            for s, r in rows[a].items():
                saved = json.loads((CT1 / f"{a}_seed_{s}.json").read_text(encoding="utf-8"))
                f1 = sum(y.get("r_apart", 0) for y in saved["years"].values())
                mism += int(round(f1)) != r["apart"].get("apart_weeks", 0)
        L.append(f"- Audit: observer's apart weeks equal CT1's F1 `apart` count in every world: "
                 f"**{'yes' if mism == 0 else f'NO ({mism} worlds differ)'}**")
        ok &= mism == 0
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        tot = {a: {} for a in ARMS}
        for a in ARMS:
            for r in rows[a].values():
                for k, v in r["apart"].items():
                    tot[a][k] = tot[a].get(k, 0) + v
        L += ["", "## Q1: what couples are doing when apart (pair reason, share of apart couple-weeks)", "",
              "| reason | C (weeks) | K1 (weeks) | K1 − C per world, mean | 95% interval |", "|---|---|---|---|---|"]
        share = {}
        for rsn in REASONS:
            cells = []
            for a in ARMS:
                n, d = tot[a].get(f"reason_{rsn}", 0), tot[a]["apart_weeks"]
                share[(a, rsn)] = n / d
                cells.append(f"{n / d:.1%} ({n:,})")
            ok_s = [s for s in SEEDS if rows["c"][s]["apart"].get("apart_weeks", 0) and rows["k1"][s]["apart"].get("apart_weeks", 0)]
            dd = [rows["k1"][s]["apart"].get(f"reason_{rsn}", 0) / rows["k1"][s]["apart"]["apart_weeks"]
                  - rows["c"][s]["apart"].get(f"reason_{rsn}", 0) / rows["c"][s]["apart"]["apart_weeks"] for s in ok_s]
            e, lo, hi = boot(dd)
            L.append(f"| {rsn.replace('_', ' ')} | {cells[0]} | {cells[1]} | {e:+.4f} | [{lo:+.4f}, {hi:+.4f}] |")
        for a in ARMS:
            L.append(f"\n{a.upper()}: partnered fertile woman-weeks {tot[a]['partnered_weeks']:,}; apart "
                     f"{tot[a]['apart_weeks']:,} ({tot[a]['apart_weeks'] / tot[a]['partnered_weeks']:.1%}); mean distance "
                     f"when apart {tot[a]['apart_dist_sum'] / tot[a]['apart_weeks']:.1f} tiles.")
        L += ["", "Each partner's action when apart (C):", "", "| action class | her | him |", "|---|---|---|"]
        for ac in ACTS:
            L.append(f"| {ac} | {tot['c'].get('her_' + ac, 0) / tot['c']['apart_weeks']:.1%} | "
                     f"{tot['c'].get('him_' + ac, 0) / tot['c']['apart_weeks']:.1%} |")
        L += ["", "## Q2: who moves apart (weeks a together couple becomes apart)", "", "| | her | him | both |",
              "|---|---|---|---|"]
        for a in ARMS:
            sp = [tot[a].get(f"split_{w}", 0) for w in ("her", "him", "both")]
            n = sum(sp) or 1
            L.append(f"| {a.upper()} ({sum(sp):,}) | {sp[0] / n:.1%} | {sp[1] / n:.1%} | {sp[2] / n:.1%} |")
        L += ["", "## Q3: how long separations last", "", "| spell length (weeks) | " + " | ".join(EDGES) + " |",
              "|---" * (len(EDGES) + 1) + "|"]
        for a in ARMS:
            n = tot[a].get("spells", 1)
            L.append(f"| {a.upper()} | " + " | ".join(f"{tot[a].get(f'spell_len_b{i}', 0) / n:.1%}" for i in range(len(EDGES)))
                     + " |")
        for a in ARMS:
            L.append(f"\n{a.upper()}: {tot[a].get('spells', 0):,} spells, mean {tot[a]['spell_weeks'] / tot[a]['spells']:.1f} "
                     f"weeks; ended in reunion {tot[a].get('spells_reunited', 0) / tot[a]['spells']:.1%}.")
        L += ["", "## Q4: hunger (described, not a cause)", ""]
        for a in ARMS:
            L.append(f"- {a.upper()}: either partner starving in {tot[a]['apart_starving'] / tot[a]['apart_weeks']:.1%} of "
                     f"apart weeks against {tot[a]['together_starving'] / tot[a]['together_weeks']:.1%} of together weeks.")
        other = share[("c", "other")]
        L += ["", "## Stopping rule and the prior (frozen)", ""]
        L.append(f"- \"Other\" share (C): {other:.1%}: "
                 + ("**over a third: the causes cannot be told apart from this record; move to another bottleneck.**"
                    if other > 1 / 3 else "under a third, so the record does tell the causes apart."))
        bs = share[("c", "both_subsistence")]
        second = sorted(REASONS[1:], key=lambda x: -share[("c", x)])[0]
        L.append(f"- Prior \"most apart weeks (over half) are both subsistence; one moving away is second\": both "
                 f"subsistence {bs:.1%}, second is {second.replace('_', ' ')}: "
                 f"**{'right' if bs > 0.5 and second == 'one_moving' else ('partly right' if bs > 0.5 else 'wrong')}**.")
    text = "\n".join(L) + "\n"
    (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main()
