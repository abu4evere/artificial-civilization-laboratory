"""RH1 analysis in the frozen order (questions.md, `RH1-frozen`, Revision 1). Written before any data. RH1's data are
the first 120 years of M1's D80 and C20 worlds (seeds 16801-16864), recorded by RH1's observer beside M1's.

  python experiments/RH1_reproductive_histories/analyse_rh1.py            # writes results.md
  python experiments/RH1_reproductive_histories/analyse_rh1.py --smoke    # M1's smoke outputs; writes nothing

Operational definitions (written before data):
- Women counted: born in the world (birth week >= 0) by year 75, who reached 16. "Reached 45": alive at year 120 or
  died at 45 or later. Childless = no live birth recorded.
- Funnel stages (per woman, ever in her single fertile weeks): an eligible unrelated man alive; one in sight; courting
  considered by her; courting tried by either; paired; at least one fully eligible week; a birth.
- Non-exclusive reasons for a childless woman: died before 45; pool empty (an eligible man alive in fewer than half her
  single fertile weeks, and never paired); men rarely in sight (in sight in under 10% of the weeks one was alive, never
  paired); in sight but courting never tried by either (never paired); courting tried but never paired; first paired at
  35+; widowed and not re-paired before 45; paired but fewer than 26 fully eligible weeks; 26+ fully eligible weeks.
- P(0) = exp(sum of log(1 - p_t)) over her fully eligible weeks.
- Secondary single class (frozen priority): died before 45 > pool empty > never paired: men rarely in sight > never
  paired: in sight, not courted > never paired: courted, refused > paired after 35 > widowed, not re-paired > rarely
  together (< 26 eligible weeks) > eligible and unlucky.
- Shares are means over worlds (each world's share among its women), 95% bootstrap over worlds; ranked, no "main path"
  verdict.
"""
from __future__ import annotations

import json
import math
import random
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
M1 = HERE.parent / "M1_millennium_v6"
sys.path.insert(0, str(M1))
from run_m1 import OUT, RH1_ARMS, SEEDS, SMOKE_SEEDS, WPY  # noqa: E402

END = 120 * WPY


def boot(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None
    rng = random.Random(2026)
    bs = sorted(statistics.fmean(rng.choice(vals) for _ in vals) for _ in range(10000))
    return statistics.fmean(vals), bs[249], bs[9749]


def fmt(t):
    return "-" if t is None else f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"


def women_of(r, end):
    out = []
    for w in r["rh1"]["women"]:
        b = w["born"]
        if b < 0 or b > 75 * WPY:
            continue
        death = w["death"]
        if death is not None and death - b < 16 * WPY:
            continue
        w = dict(w)
        w["reached45"] = (death is None and end - b >= 45 * WPY) or (death is not None and death - b >= 45 * WPY)
        w["childless"] = not w["births"]
        out.append(w)
    return out


def age_at(w, tick):
    return (tick - w["born"]) / WPY


def reasons(w):
    rs = []
    paired = bool(w["pairs"])
    if not w["reached45"]:
        rs.append("died before 45")
    if not paired and w["single_fertile"] and w["man_alive"] < 0.5 * w["single_fertile"]:
        rs.append("pool empty")
    if not paired and w["man_alive"] and w["man_sight"] < 0.1 * w["man_alive"]:
        rs.append("never paired: men rarely in sight")
    if not paired and w["man_sight"] and not w["court_tried"] and not w["courted_by"]:
        rs.append("never paired: in sight, not courted")
    if not paired and (w["court_tried"] or w["courted_by"]):
        rs.append("never paired: courted, refused")
    if paired and w["first"].get("pair", 0) >= 35:
        rs.append("paired after 35")
    if w["losses"]:
        last = max(w["losses"])
        if age_at(w, last) < 45 and not any(t > last for t in w["pairs"]):
            rs.append("widowed, not re-paired")
    if paired and w["elig"] < 26:
        rs.append("rarely together (< 26 eligible weeks)")
    if w["elig"] >= 26:
        rs.append("eligible and unlucky (26+ eligible weeks)")
    return rs


ORDER = ["died before 45", "pool empty", "never paired: men rarely in sight", "never paired: in sight, not courted",
         "never paired: courted, refused", "paired after 35", "widowed, not re-paired",
         "rarely together (< 26 eligible weeks)", "eligible and unlucky (26+ eligible weeks)"]


def main(smoke=False):
    seeds = SMOKE_SEEDS if smoke else SEEDS
    out = M1 / "output_smoke" if smoke else OUT
    L = [f"# RH1 — why a third of women never have a child: results{' (SMOKE TEST)' if smoke else ''}", "",
         "Frozen as `RH1-frozen` (Revision 1). Data: the first 120 years of M1's D80 and C20 worlds. analyse_rh1.py "
         "(written before data).", "", "## Validity", ""]
    rows, missing = {}, []
    for a in RH1_ARMS:
        for s in seeds:
            f = out / f"{a}_seed_{s}.json"
            if f.exists():
                r = json.loads(f.read_text(encoding="utf-8"))
                if "rh1" in r:
                    rows.setdefault(a, {})[s] = r
                    continue
            missing.append(f"{a} {s}")
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- M1's zero checks (which include RH1's observer): **{'yes' if zt else 'NO'}**")
    L.append(f"- All worlds present with RH1 records: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok = zt and not missing
    L += ["", f"**{'Valid.' if ok or smoke else 'NOT VALID: no outcome is shown.'}**"]
    if not (ok or smoke):
        return finish(L, smoke)
    for a in RH1_ARMS:
        rs = rows.get(a, {})
        end = END if not smoke else max(r["final_tick"] for r in rs.values())
        per = {s: women_of(r, min(end, r["final_tick"])) for s, r in rs.items()}
        allw = [w for ws in per.values() for w in ws]
        L += ["", f"## {a.upper()} ({len(rs)} worlds; {len(allw)} women counted)", ""]
        q1 = boot([statistics.fmean(w["childless"] for w in ws if w["reached45"]) if any(w["reached45"] for w in ws)
                   else None for ws in per.values()])
        died = boot([statistics.fmean(not w["reached45"] for w in ws) if ws else None for ws in per.values()])
        unc = boot([statistics.fmean(w["childless"] and w["reached45"] for w in ws) if ws else None for ws in per.values()])
        L += ["**1. How common is childlessness?**", "",
              f"- Childless at 45, among women seen reaching 45 (mean over worlds): **{fmt(q1)}**",
              f"- Died between 16 and 45: {fmt(died)}; reached 45 childless, of all who reached 16: {fmt(unc)}", ""]
        stages = [("eligible man alive", lambda w: w["man_alive"] > 0 or bool(w["pairs"])),
                  ("one in sight", lambda w: w["man_sight"] > 0 or bool(w["pairs"])),
                  ("courting considered by her", lambda w: w["court_considered"] > 0 or bool(w["pairs"])),
                  ("courting tried by either", lambda w: w["court_tried"] > 0 or w["courted_by"] > 0 or bool(w["pairs"])),
                  ("paired", lambda w: bool(w["pairs"])),
                  ("a fully eligible week", lambda w: w["elig"] > 0),
                  ("a birth", lambda w: bool(w["births"]))]
        L += ["**2. Where does opportunity disappear?** (share of women reaching each stage; childless reached 45 vs "
              "mothers)", "", "| stage | childless at 45 | mothers |", "|---|---|---|"]
        cl = [w for w in allw if w["childless"] and w["reached45"]]
        mo = [w for w in allw if not w["childless"]]
        for name, f in stages:
            L.append(f"| {name} | {sum(1 for w in cl if f(w)) / max(len(cl), 1):.3f} | "
                     f"{sum(1 for w in mo if f(w)) / max(len(mo), 1):.3f} |")
        L += ["", "Reasons that apply to each childless woman (non-exclusive; share of childless women, pooled):", ""]
        cnt = Counter(x for w in [w for w in allw if w["childless"]] for x in reasons(w))
        nchild = sum(1 for w in allw if w["childless"])
        for k in ORDER:
            L.append(f"- {k}: {cnt[k] / max(nchild, 1):.3f}")
        pz = [math.exp(w["logq"]) for w in cl]
        L += ["", "**3. Chance or luck?** Childless women's P(0) over their fully eligible weeks: "
              f"above 0.5 (little real chance) {sum(1 for p in pz if p > 0.5) / max(len(pz), 1):.3f}; below 0.1 (had "
              f"real chances) {sum(1 for p in pz if p < 0.1) / max(len(pz), 1):.3f}; median "
              f"{statistics.median(pz) if pz else float('nan'):.3f}.", ""]
        sec = Counter()
        for w in [w for w in allw if w["childless"]]:
            r_ = reasons(w)
            sec[next((k for k in ORDER if k in r_), "none of these")] += 1
        L.append("Secondary single class (frozen priority; ranked): " +
                 "; ".join(f"{k} {v}" for k, v in sec.most_common()) + ".")
        never = [w for w in cl if not w["pairs"] and w["man_sight"] > 0]
        if never:
            sa = sum(w["she_attracted"] for w in never) / max(sum(w["man_sight"] for w in never), 1)
            ha = sum(w["he_attracted"] for w in never) / max(sum(w["man_sight"] for w in never), 1)
            beat = Counter()
            for w in never:
                beat.update(w["beaten"])
            L += ["", f"**The affection deadlock** (childless women who never paired but had an eligible man in sight; "
                  f"{len(never)} women): weeks in which she would accept at least one man in sight (attraction above "
                  f"0.55): {sa:.3f}; in which at least one such man would accept her: {ha:.3f}. When she considered "
                  f"courting but chose otherwise, she chose: " + ", ".join(f"{k} {v}" for k, v in beat.most_common(6)) + "."]
        wid = []
        for w in allw:
            for t in w["losses"]:
                if age_at(w, t) < 40:
                    wid.append(any(t < p <= t + 5 * WPY for p in w["pairs"]))
        L.append(f"\n**4. Re-pairing:** of {len(wid)} widowings before 40, re-paired within 5 years: "
                 f"{sum(wid) / max(len(wid), 1):.3f}.")
        ivs = {True: [], False: []}
        for w in allw:
            b = w["births"]
            for i in range(1, len(b)):
                ivs[bool(b[i][1])].append((b[i][0] - b[i - 1][0]) / WPY)
        L.append(f"**5. Birth intervals** (years, women with 2+ births): median "
                 f"{statistics.median(ivs[True] + ivs[False]) if ivs[True] + ivs[False] else float('nan'):.2f}; "
                 f"previous child alive {statistics.median(ivs[True]) if ivs[True] else float('nan'):.2f} "
                 f"(n {len(ivs[True])}); previous child dead "
                 f"{statistics.median(ivs[False]) if ivs[False] else float('nan'):.2f} (n {len(ivs[False])}). "
                 f"Foragers: about 2.6-4.1 (described).")
        men = [m for r in rs.values() for m in r["rh1"]["men"] if 0 <= m["born"] <= 75 * WPY
               and (m["death"] is None or m["death"] - m["born"] >= 45 * WPY)]
        if men:
            kids = sorted((m["children"] for m in men), reverse=True)
            top = sum(kids[:max(1, len(kids) // 5)]) / max(sum(kids), 1)
            fp = [m["first"].get("pair") for m in men if m["first"].get("pair") is not None]
            L.append(f"**Men** ({len(men)} reaching 45): childless {sum(1 for m in men if m['children'] == 0) / len(men):.3f}; "
                     f"median age at first pairing {statistics.median(fp) if fp else float('nan'):.1f}; "
                     f"share of births fathered by the top fifth of men {top:.3f}; widowed at least once "
                     f"{sum(1 for m in men if m['losses']) / len(men):.3f}.")
    return finish(L, smoke)


def finish(L, smoke):
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
