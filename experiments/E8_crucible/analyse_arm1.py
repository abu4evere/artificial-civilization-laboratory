"""Score E8 Arms 0 and 1 against amendment_1.md A7/A9, exactly as frozen. Read-only. Writes results_arm1.md.
Written before any Arm 1 result was seen."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
SEEDS = (301, 302, 303, 304)


def load(arm, s):
    f = HERE / "output" / f"{arm}_seed_{s}.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None


def at(r, year):
    return next((x for x in r["samples"] if x["year"] == year), None) if r else None


def rate(r, lo_dec, hi_dec):
    d = [r["decades"].get(str(k)) for k in range(lo_dec, hi_dec)]
    makes = sum(x.get("deliberate", 0) for x in d if x)
    pdec = sum(x.get("person_weeks", 0) for x in d if x) / 520
    return makes / pdec if pdec else 0.0


def traditions(r):
    sets = [set(x["held_by_3"]) for x in r["samples"] if 30 <= x["year"] <= 120]
    return len(set.intersection(*sets)) if len(sets) >= 10 else 0


def f2(v):
    return "–" if v is None else (f"{v:.2f}" if isinstance(v, float) else str(v))


def main():
    a0 = {s: load("arm0", s) for s in SEEDS}
    a1 = {s: load("arm1", s) for s in SEEDS}
    L = []
    w = L.append
    w("# E8 — Arms 0 and 1 · Results\n")
    w("Arm 0 = E7 code; Arm 1 = E7 code + rule R2 (practise what has proved its worth). Seeds 301–304, 120 years. "
      "Predictions frozen in amendment_1.md A9 (tag `E8-arm1-frozen`) before any code was written.\n")
    w("## Validity\n")
    v = (HERE / "output" / "verify.txt").read_text(encoding="utf-8").strip().splitlines() if (HERE / "output" / "verify.txt").exists() else []
    ok_ro = len(v) >= 2 and all("READ-ONLY" in x for x in v)
    done = all(a0.values()) and all(a1.values())
    ok_rep = done and all(r["matches_saved_e7"] for r in a0.values())
    ok_code = done and all(r["code_hash"] == r["code_hash_after"] for r in [*a0.values(), *a1.values()])
    w(f"- Probe read-only, both codes: **{'yes' if ok_ro else 'NO'}**")
    w(f"- All 8 runs finished: **{'yes' if done else 'NO'}**")
    w(f"- Arm 0 reproduces the saved E7 runs: **{'yes' if ok_rep else 'NO'}**")
    w(f"- Code unchanged during the runs: **{'yes' if ok_code else 'NO'}**")
    w(f"- **{'Valid' if ok_ro and done and ok_rep and ok_code else 'INVALID or incomplete'}.**\n")
    if not done:
        print("\n".join(L)); return

    w("## Arm 0 against Arm 1, seed by seed\n")
    w("| seed | deliberate/person-decade yrs 50–120 | later-born skill @120 (mean / best) | recipes @120 | composite share @120 | traditions 30–120 | pop @60 / 90 / 120 | food/person @120 | starved |")
    w("|---|---|---|---|---|---|---|---|---|")
    for s in SEEDS:
        for arm, r in (("0", a0[s]), ("1", a1[s])):
            e = at(r, 120)
            pops = " / ".join(f2((at(r, y) or {}).get("population")) for y in (60, 90, 120))
            w(f"| {s} arm {arm} | {rate(r, 5, 12):.2f} | {f2(e and e['later_skill_mean'])} / {f2(e and e['later_skill_best'])} | "
              f"{f2(e and e['recipes_unique'])} | {f2(e and e['composite_share'])} | {traditions(r)} | {pops} | "
              f"{f2(e and e['food_per_person'])} | {r['deaths'].get('starvation', 0)} |")
    w("")
    w("## Frozen predictions (A9), scored\n")

    def sc(ok):
        return "**confirmed**" if ok else "**wrong**"

    p1 = [(s, rate(a1[s], 5, 12), rate(a0[s], 5, 12)) for s in SEEDS]
    ok1 = all(x1 >= 3 * x0 for _, x1, x0 in p1)
    w(f"1. {sc(ok1)} (manipulation check) — deliberate makes per person-decade, years 50–120, arm 1 vs arm 0: "
      + "; ".join(f"{s}: {x1:.2f} vs {x0:.2f}" for s, x1, x0 in p1) + ".")

    def count(pred):
        return sum(1 for s in SEEDS if pred(s))

    def m(r, k):
        e = at(r, 120)
        return e and e.get(k)
    n2 = count(lambda s: m(a1[s], "later_skill_mean") is not None and m(a0[s], "later_skill_mean")
               and m(a1[s], "later_skill_mean") >= 2 * m(a0[s], "later_skill_mean"))
    n3 = count(lambda s: m(a1[s], "recipes_unique") and m(a0[s], "recipes_unique") and m(a1[s], "recipes_unique") >= 1.3 * m(a0[s], "recipes_unique"))
    n4 = count(lambda s: m(a1[s], "composite_share") is not None and m(a0[s], "composite_share") is not None
               and m(a1[s], "composite_share") >= m(a0[s], "composite_share") - 0.02)
    n5 = count(lambda s: traditions(a1[s]) >= traditions(a0[s]))
    alive = sum(1 for s in SEEDS if (at(a1[s], 120) or {}).get("population"))
    n6pop = count(lambda s: m(a1[s], "population") and m(a0[s], "population") and m(a1[s], "population") >= 0.8 * m(a0[s], "population"))
    st0 = sum(a0[s]["deaths"].get("starvation", 0) for s in SEEDS)
    st1 = sum(a1[s]["deaths"].get("starvation", 0) for s in SEEDS)
    note = "" if ok1 else " (not interpreted: the manipulation check failed)"
    w(f"2. {sc(n2 >= 3)} — later-born adult skill at 120 ≥ 2× arm 0 in {n2} of 4 seeds{note}.")
    w(f"3. {sc(n3 >= 3)} — recipes held at 120 ≥ 1.3× arm 0 in {n3} of 4 seeds{note}.")
    w(f"4. {sc(n4 >= 3)} — composite share not lower (±2 points) in {n4} of 4 seeds{note}.")
    w(f"5. {sc(n5 >= 3)} — traditions at least as many in {n5} of 4 seeds{note}.")
    ok6 = alive == 4 and n6pop >= 3 and st1 <= 1.3 * st0
    w(f"6. {sc(ok6)} — arm 1 worlds alive at 120: {alive} of 4; population ≥ 80% of arm 0 in {n6pop} of 4; "
      f"starvation deaths {st1} vs {st0}{note}.")
    (HERE / "results_arm1.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
