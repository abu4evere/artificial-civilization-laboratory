"""CA3 analysis in the frozen order (questions.md, `CA3-frozen`). Written before any data.

  python experiments/CA3_opportunity/analyse_ca3.py          # writes results.md

Validity (no outcome shown otherwise): zero check passes; all 32 worlds present; every replay ends in CA1's saved state;
one fingerprint. Question 1: among useful never-passed inventions that stopped at G1, availability-limited (held under
13 weeks) against opportunity-limited; the reading is the larger, only if the same in discovery and holdout, else "both".
Questions 2 and 3 described, discovery and holdout apart.
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_ca3 import DISCOVERY, HOLDOUT, OUT  # noqa: E402


def fmt(x, pct=False):
    if x is None:
        return "–"
    return f"{x:.0%}" if pct else f"{x:.0f}"


def section(name, rows, L):
    g1 = sum(r["g1_stopped"] for r in rows)
    av = sum(r["availability"] for r in rows)
    op = sum(r["opportunity"] for r in rows)
    how = Counter()
    for r in rows:
        how.update(r["lost_how"])
    ct = sum(r["composite_talks"] for r in rows)
    cf = sum(r["composite_followable"] for r in rows)
    L += [f"## {name.capitalize()} ({len(rows)} worlds)", "",
          f"**Question 1.** Useful inventions never passed on that stopped at G1 (never in a teaching talk): **{g1}**. "
          f"Availability-limited (held under 13 weeks): **{av}** ({av / g1:.0%}); opportunity-limited: **{op}** "
          f"({op / g1:.0%})." if g1 else "No inventions stopped at G1.", "",
          "How the first knower lost it (or not): " + ", ".join(f"{k} {v} ({v / max(1, g1):.0%})" for k, v in how.most_common()) + ".", "",
          f"**Question 2.** Teaching talks in which an inventor held a useful never-passed composite: {ct:,}; the learner "
          f"knew every made part in **{cf:,}** ({cf / ct:.1%})." if ct else "**Question 2.** No such talks.", "",
          "**Question 3.** Passed on against never passed on (medians over inventions, pooled):", "",
          "| | inventions | weeks held | teaching talks while held | different learners met | inventor a child (under 16) | ever valued enough to offer |",
          "|---|---|---|---|---|---|---|"]
    for g in ("passed on", "never passed on"):
        gs = [r["groups"][g] for r in rows if r["groups"][g]["n"]]
        n = sum(x["n"] for x in gs)
        w = lambda k: (sum(x[k] * x["n"] for x in gs if x[k] is not None) / n) if n else None  # noqa: E731
        L.append(f"| {g} | {n} | {fmt(w('hold_weeks_median'))} | {fmt(w('talks_median'))} | {fmt(w('learners_median'))} | "
                 f"{fmt(w('inventor_child_share'), True)} | {fmt(w('valued_share'), True)} |")
    L += ["", "(Per-world medians, averaged weighted by inventions.)", ""]
    pops = lambda d: statistics.median(r["pops"][d] if len(r["pops"]) > d else 0 for r in rows)  # noqa: E731
    L += ["Living people (median), decades 1–12: " + ", ".join(f"{pops(d):.0f}" for d in range(12)) + ".", ""]
    return "availability" if av > op else "opportunity" if op > av else "tie"


def main():
    rows, missing = {}, []
    for name, seeds in (("discovery", DISCOVERY), ("holdout", HOLDOUT)):
        for s in seeds:
            f = OUT / f"seed_{s}.json"
            if f.exists():
                rows.setdefault(name, []).append(json.loads(f.read_text(encoding="utf-8")))
            else:
                missing.append(str(s))
    L = ["# CA3 — opportunity or availability: results", "", "Frozen as `CA3-frozen`. run_ca3.py, analyse_ca3.py. "
         "Read-only: a logging copy of nature v2, shown to change nothing.", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero check (logging copy = code_v2): **{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing
    allr = [r for v in rows.values() for r in v]
    same = bool(allr) and all(r["same_as_ca1"] for r in allr)
    L.append(f"- Every replay ends in CA1's saved state: **{'yes' if same else 'NO'}**")
    ok &= same
    fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
    L.append(f"- One fingerprint (`code_ca3`): **{'yes' if len(fps) == 1 else 'NO'}**")
    ok &= len(fps) == 1
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**", ""]
    if ok:
        r1 = {name: section(name, rows[name], L) for name in ("discovery", "holdout")}
        L += ["## The frozen reading", ""]
        if r1["discovery"] == r1["holdout"] and r1["discovery"] != "tie":
            L.append(f"**{r1['discovery'].capitalize()}**: the larger share of inventions that never reached a teaching "
                     "talk, in both discovery and holdout.")
        else:
            L.append(f"**Both**: {r1['discovery']} was larger in discovery, {r1['holdout']} in holdout.")
    text = "\n".join(L) + "\n"
    (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main()
