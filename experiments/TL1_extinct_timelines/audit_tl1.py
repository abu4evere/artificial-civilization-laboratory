"""TL1 audit (added after the frozen reading, 22 October 2026; described, not a reading).

Q3's search for a first K-year birth gap runs to the end of the run, so a surviving world whose last K years have no
births counts as "survived after a hiatus" with no time left to recover. This shows Q3 with gaps that end by year 100.

  python experiments/TL1_extinct_timelines/audit_tl1.py   -> results_audit.md
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import analyse_tl1 as A  # noqa: E402

L = ["# TL1 — audit of Q3 (described; added after the frozen reading)", "",
     "| set | K | gaps (all) | survived | survived with no later birth | gaps ending by year 100 | survived | later birth |",
     "|---|---|---|---|---|---|---|---|"]
for name in ("discovery", "holdout"):
    ws = A.load_worlds(name)
    for k in (5, 10, 15):
        tot = surv = surv_none = c = cs = cb = 0
        for r in ws:
            by = set(b[0] for b in r.get("births", []))
            my = r["final_tick"] // 52
            end = None
            for y in range(my - k + 1):
                if not any((y + o) in by for o in range(k)) and r.get("years", {}).get(str(y), {}).get("women", 0) > 0:
                    end = y + k - 1
                    break
            if end is None:
                continue
            s = not A.is_extinct(r)
            later = any(b > end for b in by)
            tot += 1
            surv += s
            surv_none += s and not later
            if end <= 100:
                c += 1
                cs += s
                cb += later
        L.append(f"| {name} | {k} | {tot} | {surv} ({surv / tot:.1%}) | {surv_none} | {c} | {cs} ({cs / c:.1%}) | "
                 f"{cb} ({cb / c:.1%}) |")
text = "\n".join(L) + "\n"
(HERE / "results_audit.md").write_text(text, encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
print(text)
