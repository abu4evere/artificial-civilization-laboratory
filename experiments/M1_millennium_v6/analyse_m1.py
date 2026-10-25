"""M1 analysis in the frozen order (questions.md, `M1-frozen`, Revision 1). Written before any data.

  python experiments/M1_millennium_v6/analyse_m1.py            # writes results.md
  python experiments/M1_millennium_v6/analyse_m1.py --smoke    # throwaway smoke outputs (short runs); writes nothing

Operational definitions (written here before any data; the plan's words made concrete):
- Windows: early = the samples at years 25 and 50 (the plan's years 20-50); late = years 950, 975 and 1,000. A world's
  window value is the mean of its samples in the window.
- A4 (co-primary): food owed to tools per adult forage-week = (sum over adult forage acts of food got x (1 - 1/f),
  f = the best forage factor in hand at the moment) / number of adult forage acts, over decades 2-4 (early) and 95-99
  (late), read by a read-only wrapper around the forage action.
- B-retained (co-primary): among useful kinds (strongest factor > 1) first made in the early era (years 0-50) or the
  late era (years 900-950), whose first maker died and was followed 25 years: the share still known by someone alive
  25 years after that death.
- B first hand-over: the share of those kinds ever learned by someone other than their first maker.
- Ratios late / early per world, for worlds alive at year 1,000 (conditional view), 95% bootstrap over worlds
  (10,000 resamples of worlds; the ratio of means): builds (lower > 1.10), declines (upper < 0.90), increase below the margin (lower > 1.00, upper <= 1.10) /
  decrease below the margin (lower >= 0.90, upper < 1.00), holds (inside 0.90-1.10, including 1), unclear.
  A world whose early value is 0 is left out of the ratio and reported in a count with its late value.
- Unconditional view: worlds extinct before 1,000, with the year.
- C ladder per kind first made after year 100: (1) candidate; (2) made by 3+ people within 10 years; (3) still made 50+
  years after it appeared; (4) better: strongest factor above every kind that existed before it; (5) adopted: learned by
  someone else; (6) outlived its first maker (known 25 years after the death); (7) improved again: a later kind with it
  as a part and a higher strongest factor.
- Tradition: a recipe or belief held by 3+ living people in every 10-year sample for at least 5 samples in a row (50
  years), with a recorded passing between people, still held after all its first holders died.
- Cohort test: people reaching 30 born in years 0-50 against 900-950; per world means; ratio late / early as above.
- Trajectory class per world (point ratios; first that fits): extinct; erosion (skill ratio < 0.9 and unique recipes
  ratio < 0.9); improvement with transmission (A4 ratio > 1.1 and B-retained late > early); stable maintenance (skill
  ratio within 0.9-1.1 and B-retained late >= 0.1); stable by rediscovery (skill ratio within 0.9-1.1 and B-retained
  late < 0.1); change without improvement (anything else).
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_m1 import ARMS, OUT, SEEDS, SMOKE_SEEDS, WPY  # noqa: E402

EARLY_S, LATE_S = (25, 50), (950, 975, 1000)
EARLY_D, LATE_D = (2, 3, 4), (95, 96, 97, 98, 99)


def win(r, key, years):
    v = [s[key] for s in r["samples"] if s["year"] in years and s.get(key) is not None]
    return statistics.fmean(v) if v else None


def a4(r, decs):
    acts = sum(r["forage"].get(str(d), [0, 0, 0, 0])[0] for d in decs)
    tool = sum(r["forage"].get(str(d), [0, 0, 0, 0])[2] for d in decs)
    return tool / acts if acts else None


def bret(r, lo, hi, end):
    ks = [k for k in r["kinds"] if k[4] > 1.0 and lo * WPY <= k[0] < hi * WPY and k[2] is not None
          and k[2] + 25 * WPY <= end and k[3] is not None]
    return (sum(1 for k in ks if k[3]) / len(ks)) if ks else None, len(ks)


def bhand(r, lo, hi):
    ks = [k for k in r["kinds"] if k[4] > 1.0 and lo * WPY <= k[0] < hi * WPY]
    return (sum(1 for k in ks if k[1] > 0) / len(ks)) if ks else None


def making(r, decs):
    m = sum(r["decades"].get(str(d), {}).get("deliberate", 0) for d in decs)
    pw = sum(r["decades"].get(str(d), {}).get("person_weeks", 0) for d in decs)
    return m / (pw / (10 * WPY)) if pw else None


def cohort(r, lo, hi, idx):
    v = [c[idx] for c in r["cohort"] if lo <= c[0] < hi]
    return statistics.fmean(v) if v else None


def cohort_share(r, lo, hi):
    v = [c[2] / c[1] for c in r["cohort"] if lo <= c[0] < hi and c[1] > 0]
    return statistics.fmean(v) if v else None


def reading(lo, hi):
    if lo > 1.10:
        return "builds"
    if hi < 0.90:
        return "declines"
    if 1.00 < lo and hi <= 1.10:
        return "increase, below the meaningful margin"
    if 0.90 <= lo and hi < 1.00:
        return "decrease, below the meaningful margin"
    if 0.90 <= lo and hi <= 1.10:
        return "holds"
    return "unclear"


def ratio_test(pairs):
    """pairs: [(early, late)] per world with early > 0. Ratio of means, bootstrap over worlds."""
    if len(pairs) < 2:
        return None
    rng = random.Random(2026)
    e0 = statistics.fmean(p[0] for p in pairs)
    r0 = statistics.fmean(p[1] for p in pairs) / e0 if e0 else float("nan")
    bs = []
    n = len(pairs)
    for _ in range(10000):
        s = [pairs[rng.randrange(n)] for _ in range(n)]
        e = sum(p[0] for p in s)
        bs.append(sum(p[1] for p in s) / e if e else float("nan"))
    bs.sort()
    return r0, bs[249], bs[9749]


def ladder(r, end):
    ks = r["kinds"]
    out = [0] * 7
    order = sorted(range(len(ks)), key=lambda i: ks[i][0])
    best_before = 1.0
    earlier_best = {}
    for i in order:
        earlier_best[i] = best_before
        best_before = max(best_before, ks[i][4])
    for i, k in enumerate(ks):
        if k[0] < 100 * WPY:
            continue
        out[0] += 1
        if k[5] < 3:
            continue
        out[1] += 1
        if k[6] is None or k[6] - k[0] < 50 * WPY:
            continue
        out[2] += 1
        if not k[4] > earlier_best[i]:
            continue
        out[3] += 1
        if k[1] == 0:
            continue
        out[4] += 1
        if not k[3]:
            continue
        out[5] += 1
        if any(i in kk[8] and kk[4] > k[4] and kk[0] > k[0] for kk in ks):
            out[6] += 1
    return out


def main(smoke=False):
    seeds = SMOKE_SEEDS if smoke else SEEDS
    out = HERE / "output_smoke" if smoke else OUT
    years = 1000
    rows, missing = {}, []
    for a in ARMS:
        for s in seeds:
            f = out / f"{a}_seed_{s}.json"
            if f.exists():
                rows.setdefault(a, {})[s] = json.loads(f.read_text(encoding="utf-8"))
            else:
                missing.append(f"{a} {s}")
    if smoke and rows:
        years = max(r["final_tick"] for a in rows.values() for r in a.values()) // WPY
    L = [f"# M1 — a thousand years on nature v6: results{' (SMOKE TEST, short runs)' if smoke else ''}", "",
         "Frozen as `M1-frozen` (Revision 1). run_m1.py, analyse_m1.py (written before data).", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks: **{'yes' if zt else 'NO'}**")
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok = zt and not missing
    if not missing:
        allr = [r for a in rows.values() for r in a.values()]
        fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
        L.append(f"- One fingerprint (`code_v6`): **{'yes' if len(fps) == 1 else 'NO'}**")
        ok &= len(fps) == 1
    L += ["", f"**{'Valid.' if ok or smoke else 'NOT VALID: no outcome is shown.'}**"]
    if not (ok or smoke):
        return finish(L, smoke)
    end = years * WPY
    for a in ARMS:
        rs = rows[a]
        alive = {s: r for s, r in rs.items() if r["final_tick"] >= end}
        dead = sorted(round(r["final_tick"] / WPY) for r in rs.values() if r["final_tick"] < end)
        L += ["", f"## Arm {a.upper()}{' (primary)' if a == 'lp' else ' (secondary, described)'}", "",
              f"Worlds alive at year {years}: **{len(alive)} of {len(rs)}**; extinct at years: {dead or 'none'}.", ""]
        if not alive:
            continue
        pop_e = statistics.fmean(win(r, "population", EARLY_S) or 0 for r in alive.values())
        pop_l = statistics.fmean(win(r, "population", LATE_S) or 0 for r in alive.values())
        L.append(f"Population (worlds alive): early {pop_e:.1f}, late {pop_l:.1f}.\n")
        measures = [
            ("**A4 food owed to tools per adult forage-week (co-primary)**", lambda r: a4(r, EARLY_D), lambda r: a4(r, LATE_D)),
            ("**B-retained: useful kinds still known 25 years after the maker's death (co-primary)**",
             lambda r: bret(r, 0, 50, end)[0], lambda r: bret(r, 900, 950, end)[0]),
            ("B first hand-over share", lambda r: bhand(r, 0, 50), lambda r: bhand(r, 900, 950)),
            ("A1 best tool held (strongest factor)", lambda r: win(r, "best_item", EARLY_S), lambda r: win(r, "best_item", LATE_S)),
            ("A1 median adult's best tool", lambda r: win(r, "median_adult_best", EARLY_S), lambda r: win(r, "median_adult_best", LATE_S)),
            ("A2 uses covered", lambda r: win(r, "uses_covered", EARLY_S), lambda r: win(r, "uses_covered", LATE_S)),
            ("A3 best crafting skill", lambda r: win(r, "skill_best", EARLY_S), lambda r: win(r, "skill_best", LATE_S)),
            ("A3 mean adult crafting skill", lambda r: win(r, "skill_mean_adults", EARLY_S), lambda r: win(r, "skill_mean_adults", LATE_S)),
            ("Recipes known (unique)", lambda r: win(r, "recipes_unique", EARLY_S), lambda r: win(r, "recipes_unique", LATE_S)),
            ("Deliberate making per person-decade", lambda r: making(r, EARLY_D), lambda r: making(r, LATE_D)),
            ("Cohort at 30: useful recipes known", lambda r: cohort(r, 0, 50, 1), lambda r: cohort(r, 900, 950, 1)),
            ("Cohort at 30: share of them learned from others", lambda r: cohort_share(r, 0, 50), lambda r: cohort_share(r, 900, 950)),
            ("Cohort at 30: best tool held", lambda r: cohort(r, 0, 50, 3), lambda r: cohort(r, 900, 950, 3)),
            ("Cohort at 30: crafting skill", lambda r: cohort(r, 0, 50, 4), lambda r: cohort(r, 900, 950, 4)),
        ]
        L += ["| measure | early (mean) | late (mean) | late / early | 95% interval | reading | worlds (early = 0) |",
              "|---|---|---|---|---|---|---|"]
        for name, fe, fl in measures:
            pairs, zeros = [], 0
            for r in alive.values():
                e, l_ = fe(r), fl(r)
                if e is None or l_ is None:
                    continue
                if e == 0:
                    zeros += 1
                    continue
                pairs.append((e, l_))
            t = ratio_test(pairs)
            em = statistics.fmean(p[0] for p in pairs) if pairs else float("nan")
            lm = statistics.fmean(p[1] for p in pairs) if pairs else float("nan")
            if t:
                L.append(f"| {name} | {em:.4g} | {lm:.4g} | {t[0]:.3f} | [{t[1]:.3f}, {t[2]:.3f}] | "
                         f"**{reading(t[1], t[2])}** | {len(pairs)} ({zeros}) |")
            else:
                L.append(f"| {name} | {em:.4g} | {lm:.4g} | - | - | too few worlds | {len(pairs)} ({zeros}) |")
        lad = [0] * 7
        for r in alive.values():
            for i, v in enumerate(ladder(r, end)):
                lad[i] += v
        L += ["", "C, the ladder for kinds first made after year 100 (all alive worlds, counts): candidates "
              f"{lad[0]}; made by 3+ within 10 years {lad[1]}; still made 50+ years on {lad[2]}; better than every "
              f"earlier kind {lad[3]}; adopted {lad[4]}; outlived its maker {lad[5]}; improved again {lad[6]}."]
        tr = [t for r in alive.values() for t in r["traditions"]]
        good = [t for t in tr if t[6] >= 5 and t[4] and t[5]]
        L.append(f"Traditions (frozen definition): {len(good)} in {len(alive)} worlds "
                 f"(recipes {sum(1 for t in good if t[0] == 'r')}, beliefs {sum(1 for t in good if t[0] == 'b')}); "
                 f"of them begun after year 100: {sum(1 for t in good if t[2] is not None and t[2] >= 10)}.")
        me = statistics.fmean(statistics.fmean(r["marks_shared"][2:5] or [0]) for r in alive.values())
        ml = statistics.fmean(statistics.fmean(r["marks_shared"][95:100] or [0]) for r in alive.values())
        L.append(f"Shared marks (historian), mean per world: early {me:.1f}, late {ml:.1f} (described; not language).")
        classes = {}
        for s, r in rs.items():
            if r["final_tick"] < end:
                c = "extinction"
            else:
                sk = (win(r, "skill_mean_adults", LATE_S) or 0) / max(win(r, "skill_mean_adults", EARLY_S) or 1e-9, 1e-9)
                rc = (win(r, "recipes_unique", LATE_S) or 0) / max(win(r, "recipes_unique", EARLY_S) or 1e-9, 1e-9)
                a4e, a4l = a4(r, EARLY_D) or 0, a4(r, LATE_D) or 0
                be, bl = bret(r, 0, 50, end)[0] or 0, bret(r, 900, 950, end)[0] or 0
                if sk < 0.9 and rc < 0.9:
                    c = "erosion"
                elif a4e > 0 and a4l / a4e > 1.1 and bl > be:
                    c = "improvement with transmission"
                elif 0.9 <= sk <= 1.1 and bl >= 0.1:
                    c = "stable maintenance"
                elif 0.9 <= sk <= 1.1:
                    c = "stable by rediscovery"
                else:
                    c = "change without improvement"
            classes[c] = classes.get(c, 0) + 1
        L.append("Trajectory classes (frozen rules): " + "; ".join(f"{k} {v}" for k, v in sorted(classes.items())) + ".")
    return finish(L, smoke)


def finish(L, smoke):
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
