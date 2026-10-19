"""CA2 analysis in the frozen order (questions.md, `CA2-frozen`). Written before any data.

  python experiments/CA2_teaching_gates/analyse_ca2.py           # writes results.md
  python experiments/CA2_teaching_gates/analyse_ca2.py --pilot   # reads output_pilot/ (throwaway), writes nothing

Validity (no outcome shown otherwise): zero check passes; all 32 worlds present; every replay's final state hash equals
CA1's saved one; one fingerprint. Unmatched log records are counted and shown.
Gates, per useful invention never passed on: entering gate g = inventions that passed gates 1..g-1; passing = those that
passed g; pass rate = passing / entering. Reading: (b) the gate where the most stopped, (a) the gate with the lowest pass
rate; "one bottleneck: gate X" only if (b) is X in both sets and (a) is X in both; if (b) agrees but (a) does not, "most
stopped at X; lowest pass rate elsewhere"; if (b) differs, "no single bottleneck".
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_ca2 import DISCOVERY, GATES, HOLDOUT, OUT  # noqa: E402

END = "taken, but changed in the showing"


def gate_table(rows, L):
    lv = Counter()
    for r in rows:
        lv.update({int(k): v for k, v in r["levels"].items()})
    n = sum(lv.values())
    stopped = Counter()
    for r in rows:
        stopped.update(r["stopped"])
    L += ["| gate | entering | passing | pass rate | stopped here for good |", "|---|---|---|---|---|"]
    rates = {}
    for g in range(7):
        entering = sum(v for k, v in lv.items() if k >= g)
        passing = sum(v for k, v in lv.items() if k >= g + 1)
        rate = passing / entering if entering else None
        rates[GATES[g]] = rate
        L.append(f"| {GATES[g]} | {entering} | {passing} | {rate:.3f} | {stopped.get(GATES[g], 0)} |" if rate is not None
                 else f"| {GATES[g]} | 0 | 0 | – | 0 |")
    L += ["", f"Useful inventions never passed on: **{n}**. Of them, {stopped.get(END, 0)} were shown and taken, but the "
          "learner took away a different kind (counted by CA1 as a new kind).", ""]
    most = max(GATES, key=lambda g: stopped.get(g, 0))
    lowest = min((g for g in GATES if rates[g] is not None), key=lambda g: rates[g])
    return most, lowest


def described(rows, L):
    for name, key in (("Watching, for the same inventions (outcomes)", "watch"),
                      ("Kept a year (G8), learners of useful inventions", "kept"),
                      ("Who built on what (CA1's link-5 pairs)", "who_built")):
        c = Counter()
        for r in rows:
            c.update(r[key])
        tot = sum(c.values())
        L.append(f"- **{name}:** " + (", ".join(f"{k} {v} ({v / tot:.0%})" for k, v in c.most_common()) if tot else "none")
                 + ".")
    pops = lambda d: statistics.median(r["pops"][d] if len(r["pops"]) > d else 0 for r in rows)  # noqa: E731
    L += [f"- **Living people** (median), decades 1–12: " + ", ".join(f"{pops(d):.0f}" for d in range(12)) + ".",
          f"- Log records: {sum(r['log_records'] for r in rows):,}; unmatched: {sum(r['unmatched'] for r in rows)}.", ""]


def main(pilot=False):
    out = HERE / "output_pilot" if pilot else OUT
    sets = {"discovery": DISCOVERY, "holdout": HOLDOUT}
    rows, missing = {}, []
    for name, seeds in sets.items():
        for s in seeds:
            f = out / f"seed_{s}.json"
            if f.exists():
                rows.setdefault(name, []).append(json.loads(f.read_text(encoding="utf-8")))
            else:
                missing.append(str(s))
    L = ["# CA2 — why teaching passes on so little: results" + (" (PILOT, throwaway)" if pilot else ""), "",
         "Frozen as `CA2-frozen`. run_ca2.py, analyse_ca2.py. Read-only: a logging copy of nature v2, shown to change "
         "nothing.", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero check (logging copy = code_v2): **{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing or pilot
    allr = [r for v in rows.values() for r in v]
    same = all(r["same_as_ca1"] for r in allr)
    L.append(f"- Every replay ends in CA1's saved state: **{'yes' if same else 'NO'}**")
    ok &= same or pilot
    fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
    L.append(f"- One fingerprint (`code_ca2`): **{'yes' if len(fps) == 1 else 'NO'}**")
    ok &= len(fps) == 1
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**", ""]
    if ok:
        res = {}
        for name in ("discovery", "holdout"):
            if name in rows:
                L += [f"## {name.capitalize()} ({len(rows[name])} worlds)", ""]
                res[name] = gate_table(rows[name], L)
                described(rows[name], L)
        L += ["## The frozen reading", ""]
        (bd, ad), (bh, ah) = res.get("discovery", (None, None)), res.get("holdout", (None, None))
        if bd is not None and bd == bh and ad == bd and ah == bd:
            L.append(f"**One bottleneck: {bd}**: the most stopped there, and its pass rate was the lowest, in both sets.")
        elif bd is not None and bd == bh:
            L.append(f"**Most stopped at {bd}** in both sets; **the lowest pass rate was elsewhere** ({ad} in discovery, "
                     f"{ah} in holdout).")
        else:
            L.append(f"**No single bottleneck:** the most stopped at {bd} in discovery and {bh} in holdout.")
    text = "\n".join(L) + "\n"
    if not pilot:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(pilot="--pilot" in sys.argv)
