"""LU1 analysis in the frozen order (questions.md, `LU1-frozen`). Written before any data. Read-only; described.

  python experiments/LU1_lesson_uptake/analyse_lu1.py            # writes results.md
  python experiments/LU1_lesson_uptake/analyse_lu1.py --smoke    # throwaway smoke outputs; writes nothing
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_lu1 import OUT, OUTCOMES, SEEDS, SMOKE_SEEDS  # noqa: E402

FAILS = [o for o in OUTCOMES if o != "taken"]
SPLIT = ("taken", "not_open", "known", "cannot_follow", "part_shown", "own_bad")


def pct(a, b):
    return f"{a / b:.1%}" if b else "—"


def main(smoke=False):
    seeds = SMOKE_SEEDS if smoke else SEEDS
    out = HERE / "output_smoke" if smoke else OUT
    rows = {s: json.loads((out / f"c_seed_{s}.json").read_text(encoding="utf-8")) for s in seeds
            if (out / f"c_seed_{s}.json").exists()}
    missing = [s for s in seeds if s not in rows]
    L = [f"# LU1 — why are offered lessons not taken up? results{' (SMOKE TEST)' if smoke else ''}", "",
         "Frozen as `LU1-frozen`. run_lu1.py, analyse_lu1.py (written before data). Read-only; described.", "",
         "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    fps = {r["code_hash"] for r in rows.values()} | {r["code_hash_after"] for r in rows.values()}
    ok = zt and not missing and len(fps) == 1
    L += [f"- Zero checks: **{'yes' if zt else 'NO'}**",
          f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + str(missing[:8])}**",
          f"- One fingerprint (`code_lu1`): **{'yes' if len(fps) == 1 else 'NO'}**", "",
          f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        tot = Counter()
        for r in rows.values():
            tot.update(r["lessons"])
        n = sum(tot["useful:" + o] for o in OUTCOMES)
        nf = sum(tot["useful:" + o] for o in FAILS)
        L += ["", "## 1. How lessons about useful inventions end", "",
              f"{n:,} lessons about useful inventions in {len(rows)} worlds ({nf:,} not taken).", "",
              "| outcome | lessons | share of all | share of those not taken | median share per world |",
              "|---|---|---|---|---|"]
        for o in OUTCOMES:
            per = []
            for r in rows.values():
                s = sum(r["lessons"].get("useful:" + x, 0) for x in OUTCOMES)
                if s:
                    per.append(r["lessons"].get("useful:" + o, 0) / s)
            of_failed = "" if o == "taken" else pct(tot["useful:" + o], nf)
            L.append(f"| {o} | {tot['useful:' + o]:,} | {pct(tot['useful:' + o], n)} | {of_failed} | "
                     f"{statistics.median(per) if per else 0:.1%} |")
        main_o = max(FAILS, key=lambda o: tot["useful:" + o])
        share = tot["useful:" + main_o] / nf if nf else 0
        reading = (f"the main reason useful lessons fail is **{main_o}** ({share:.0%} of those not taken)."
                   if share >= 0.40 else "no single main reason.")
        L += ["", "**Reading (frozen rule):** " + reading]
        L += ["", "## 2. By teacher and learner (useful inventions)", "",
              "| group | lessons | " + " | ".join(SPLIT) + " |", "|---|---|" + "---|" * len(SPLIT)]
        for g, label in (("parent", "teacher is a parent"), ("other_teacher", "teacher is not a parent"),
                         ("inventor", "teacher is the inventor"), ("not_inventor", "teacher is not the inventor"),
                         ("child", "learner under 16"), ("adult", "learner 16 or over")):
            m = sum(tot[f"useful:{g}:{o}"] for o in OUTCOMES)
            if m:
                L.append(f"| {label} | {m:,} | " + " | ".join(pct(tot[f"useful:{g}:{o}"], m) for o in SPLIT) + " |")
        lo = Counter()
        for r in rows.values():
            lo.update(r["not_open"])
        k = tot["useful:not_open"]
        L += ["", "## 3. Lessons not taken because the chance failed (useful inventions)", ""]
        if k:
            L += [f"Mean credence in the teacher {lo['useful:cred_sum'] / k:.2f}; mean openness "
                  f"{lo['useful:open_sum'] / k:.2f}.", "", "| chance of taking it | lessons | share |", "|---|---|---|"]
            for b in range(10):
                L.append(f"| {b / 10:.1f}–{(b + 1) / 10:.1f} | {lo[f'useful:chance_bin{b}']:,} | "
                         f"{pct(lo[f'useful:chance_bin{b}'], k)} |")
        tk = tot["useful:taken"]
        L += ["", "## 4. After a useful lesson is taken", "",
              (f"{tot['useful:taken_made_later']:,} of {tk:,} ({pct(tot['useful:taken_made_later'], tk)}) learners "
               f"later made the thing.") if tk else "No useful lessons were taken."]
        p60 = statistics.median(r["pops"][5] if len(r["pops"]) > 5 else 0 for r in rows.values())
        p120 = statistics.median(r["pops"][11] if len(r["pops"]) > 11 else 0 for r in rows.values())
        died = sum(r["final_tick"] < 120 * 52 for r in rows.values())
        L += ["", "## Beside it (population first)", "",
              f"Median population at year 60 / 120: {p60:.0f} / {p120:.0f}; died out: {died} of {len(rows)}."]
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
