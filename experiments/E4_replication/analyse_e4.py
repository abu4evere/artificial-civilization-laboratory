"""E4 analysis: apply the frozen decision rule (predictions.md) and compare E1 and E2 code. Read-only.

Worlds: seeds 101-108 (from E1/E2) and 201-216 (E4). Writes results.md.
"""
from __future__ import annotations

import json
import math
import random
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments" / "E1"))

from acl.runner import load_snapshot  # noqa: E402
from analyse_inv_extra import _bands_of, _gaps  # noqa: E402

WPY = 52
SOURCES = {("e1", "old"): ROOT / "experiments" / "E1" / "output", ("e2", "old"): ROOT / "experiments" / "E2" / "output",
           ("e1", "new"): HERE / "output" / "e1", ("e2", "new"): HERE / "output" / "e2"}


def _dir(code, seed):
    return SOURCES[(code, "old" if seed < 200 else "new")]


def measures(code, seed):
    d = _dir(code, seed)
    f = d / f"seed_{seed}.json"
    if not f.exists():
        return None
    r = json.loads(f.read_text(encoding="utf-8"))
    rows = r["rows"]
    m = {"pop100": rows[99]["population"] if len(rows) >= 100 else 0,
         "pop200": rows[199]["population"] if len(rows) >= 200 else 0,
         "extinct_by_200": r["extinct"]}
    b = de = py = 0
    for x in rows[:100]:
        b += x["births"]
        de += x["deaths"]
        py += x["population"]
    m["births_per_1000"] = 1000 * b / py if py else 0
    m["deaths_per_1000"] = 1000 * de / py if py else 0
    ev = {}
    for x in rows:
        for k, v in x["events"].items():
            ev[k] = ev.get(k, 0) + v
    yrs = max(1, r["years_run"])
    m["tests_per_year"] = sum(v for k, v in ev.items() if k.startswith(("verified", "refuted"))
                              and (k in ("verified", "refuted") or "_" in k)) / yrs
    if code == "e2":
        m["tests_per_year"] = sum(v for k, v in ev.items() if k.startswith(("verified_", "refuted_"))) / yrs
    else:
        m["tests_per_year"] = (ev.get("verified", 0) + ev.get("refuted", 0)) / yrs
    m["crossings"] = ev.get("crossed", 0)
    m["learned_from_marks"] = ev.get("learn_how_read", 0)
    carried = [x["trust"].get("rafts_carried", 0) / x["population"] for x in rows if x["population"] >= 10]
    m["raft_share"] = sum(carried) / len(carried) if carried else 0
    s = r["summary_end"]
    m["techniques"] = s["techniques"]
    m["technique_median_life"] = s["technique_life_years"]["median"]
    m["record_pairs"] = (r.get("summary_100") or {}).get("accuracy_record_pairs", []) + s.get("accuracy_record_pairs", [])
    # people: infants and fertile women in the first 100 years
    w, h = load_snapshot(d / f"seed_{seed}_end.json.gz")
    end = 100 * WPY
    iy = starved = infant_dead = 0
    fwy = births = 0
    for p in w.people.values():
        a0 = max(p.birth, 0)
        stop = min(p.death_tick if p.death_tick is not None else w.tick, end)
        bi = min(p.birth + WPY, stop)
        if bi > a0:
            iy += (bi - a0) / WPY
        if p.death_tick is not None and p.death_tick < end and p.death_tick - p.birth < WPY:
            infant_dead += 1
            starved += p.death_cause == "starvation"
        if p.sex == "F":
            f0, f1 = max(a0, p.birth + 16 * WPY), min(stop, p.birth + 45 * WPY)
            if f1 > f0:
                fwy += (f1 - f0) / WPY
        if 0 <= p.birth < end and p.mother:
            births += 1
    m["infant_years"] = iy
    m["infant_starved_per_1000"] = 1000 * starved / iy if iy else None
    m["infant_deaths_per_1000"] = 1000 * infant_dead / iy if iy else None
    m["births_per_fertile_woman_year"] = births / fwy if fwy else None
    # island mixing at year 100, and how wide the water between the founding islands is
    snap = d / f"seed_{seed}_year100.json.gz"
    if snap.exists():
        w100, _ = load_snapshot(snap)
        living = w100.living()
        groups = max(1, min(4, w100.cfg.founders // 4))
        memo = {}
        m["mixed100"] = (sum(1 for p in living if len(_bands_of(w100, p.id, memo, groups)) >= 2) / len(living)
                         if living else None)
    else:
        m["mixed100"] = None
    return m


def bootstrap_ci(diffs, n=10000, seed=12345):
    rng = random.Random(seed)
    k = len(diffs)
    means = sorted(sum(rng.choice(diffs) for _ in range(k)) / k for _ in range(n))
    return means[int(0.025 * n)], means[int(0.975 * n) - 1]


def decide(e1_vals, e2_vals, worse_is_lower: bool, e1_mean_for_shrink):
    """Apply the frozen rule. Returns (verdict, details)."""
    diffs = [(a - b) if worse_is_lower else (b - a) for a, b in zip(e1_vals, e2_vals)]
    n_worse = sum(1 for d in diffs if d > 0)
    lo, hi = bootstrap_ci(diffs)
    mean = sum(diffs) / len(diffs)
    if n_worse >= 17 and lo > 0:
        verdict = "A (a real effect)"
    elif lo <= 0 <= hi and abs(mean) < 0.10 * e1_mean_for_shrink:
        verdict = "B (noise)"
    else:
        verdict = "unresolved"
    return verdict, {"worlds": len(diffs), "worse_in_e2": n_worse, "mean_gap": mean, "ci": (lo, hi)}


def pearson(pairs):
    n = len(pairs)
    if n < 5:
        return None
    xs, ys = [p[0] for p in pairs], [p[1] for p in pairs]
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return round(sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy), 3) if sx and sy else None


def main():
    seeds = [s for s in list(range(101, 109)) + list(range(201, 217))
             if (_dir("e1", s) / f"seed_{s}.json").exists() and (_dir("e2", s) / f"seed_{s}.json").exists()]
    M = {(c, s): measures(c, s) for s in seeds for c in ("e1", "e2")}
    new = [s for s in seeds if s >= 200]
    L = ["# E4 — Replication: E1 code against E2 code · Results", ""]
    w = L.append
    w(f"Worlds: {len(seeds)} ({len(new)} new: {', '.join(map(str, new))}; plus 101–108 from E1/E2). Rules and "
      "predictions were frozen in predictions.md before the run.")
    w("")
    # --- decision rule: population
    p1 = [M[("e1", s)]["pop100"] for s in seeds]
    p2 = [M[("e2", s)]["pop100"] for s in seeds]
    verdict, d = decide(p1, p2, True, statistics.mean(p1))
    w("## The decision rule")
    w("")
    w(f"**Population at year 100.** E1 mean {statistics.mean(p1):.1f}, E2 mean {statistics.mean(p2):.1f}. E2 lower in "
      f"{d['worse_in_e2']} of {d['worlds']} worlds (rule needs ≥ 17 of 24). Mean gap {d['mean_gap']:.1f}, 95% bootstrap "
      f"interval [{d['ci'][0]:.1f}, {d['ci'][1]:.1f}]. **Verdict: {verdict}.**")
    if new:
        q1 = [M[("e1", s)]["pop100"] for s in new]
        q2 = [M[("e2", s)]["pop100"] for s in new]
        _, dn = decide(q1, q2, True, statistics.mean(q1))
        w(f"New worlds alone: E1 mean {statistics.mean(q1):.1f}, E2 mean {statistics.mean(q2):.1f}; E2 lower in "
          f"{dn['worse_in_e2']} of {dn['worlds']}; mean gap {dn['mean_gap']:.1f}, interval [{dn['ci'][0]:.1f}, {dn['ci'][1]:.1f}].")
    w("")
    both = [s for s in seeds if M[("e1", s)]["infant_starved_per_1000"] is not None
            and M[("e2", s)]["infant_starved_per_1000"] is not None]
    i1 = [M[("e1", s)]["infant_starved_per_1000"] for s in both]
    i2 = [M[("e2", s)]["infant_starved_per_1000"] for s in both]
    verdict_i, di = decide(i1, i2, False, statistics.mean(i1))
    w(f"**Infant starvation per 1000 infant-years** (worlds with infants under both codes: {len(both)}). E1 mean "
      f"{statistics.mean(i1):.1f}, E2 mean {statistics.mean(i2):.1f}. Higher in E2 in {di['worse_in_e2']} of {di['worlds']}. "
      f"Mean gap {di['mean_gap']:.1f}, interval [{di['ci'][0]:.1f}, {di['ci'][1]:.1f}]. **Verdict: {verdict_i}.** "
      "(The rule's 17-of-24 threshold is applied as written; with fewer than 24 worlds it is stricter.)")
    w("")
    # --- the other comparisons
    w("## Everything else, E1 code against E2 code (mean over worlds)")
    w("")
    w("| measure | E1 | E2 |")
    w("|---|---|---|")

    def mean_of(key, code, sel=None):
        vals = [M[(code, s)][key] for s in (sel or seeds) if M[(code, s)][key] is not None]
        return statistics.mean(vals) if vals else float("nan")
    for label, key in (("population at year 200", "pop200"), ("worlds died out by 200", "extinct_by_200"),
                       ("births per 1000 person-years (first 100 years)", "births_per_1000"),
                       ("deaths per 1000 person-years (first 100 years)", "deaths_per_1000"),
                       ("births per fertile woman-year", "births_per_fertile_woman_year"),
                       ("infant deaths, all causes, per 1000 infant-years", "infant_deaths_per_1000"),
                       ("mixed ancestry at year 100", "mixed100"),
                       ("techniques tried", "techniques"), ("median technique life (years)", "technique_median_life"),
                       ("claims tested per world-year", "tests_per_year"),
                       ("people carrying a raft (years with 10+ alive)", "raft_share"),
                       ("open-water crossings", "crossings"), ("techniques taken up from marks", "learned_from_marks")):
        if key == "extinct_by_200":
            w(f"| {label} | {sum(1 for s in seeds if M[('e1', s)][key])} | {sum(1 for s in seeds if M[('e2', s)][key])} |")
        elif key in ("mixed100", "raft_share"):
            w(f"| {label} | {100 * mean_of(key, 'e1'):.0f}% | {100 * mean_of(key, 'e2'):.0f}% |")
        else:
            w(f"| {label} | {mean_of(key, 'e1'):.2f} | {mean_of(key, 'e2'):.2f} |")
    pairs = [p for s in seeds for p in M[("e2", s)]["record_pairs"]]
    w(f"| reputation tracks accuracy (pooled r, E2 only) | – | {pearson(pairs)} |")
    w("")
    # --- predictions
    w("## Frozen predictions, scored")
    w("")
    gap_pct = 100 * (statistics.mean(p1) - statistics.mean(p2)) / statistics.mean(p1)
    w(f"1. Population lower under E2 by under 25%, rule ends unresolved or A: gap {gap_pct:.0f}%, verdict {verdict}.")
    rise = 100 * (statistics.mean(i2) - statistics.mean(i1)) / max(1e-9, statistics.mean(i1))
    w(f"2. Infant starvation higher under E2 by under 40%: {rise:+.0f}%.")
    wide = []
    for s in seeds:
        world, _ = load_snapshot(_dir("e1", s) / f"seed_{s}_end.json.gz")
        _, gap = _gaps(world)
        if M[("e1", s)]["mixed100"] is not None and M[("e2", s)]["mixed100"] is not None:
            wide.append((min(gap.values()) if gap else 99, M[("e1", s)]["mixed100"], M[("e2", s)]["mixed100"]))
    over3 = [x for x in wide if x[0] > 3]
    w(f"3. Mixing lower under E2 where islands are more than 3 tiles apart: lower in "
      f"{sum(1 for x in over3 if x[2] < x[1])} of {len(over3)} such worlds (all worlds: "
      f"{sum(1 for x in wide if x[2] < x[1])} of {len(wide)}).")
    gains = [s for s in seeds if not M[("e2", s)]["extinct_by_200"] or M[("e2", s)]["pop100"] > 0]
    w(f"4. E2's gains in every world: tests ≥ 10 per world-year in "
      f"{sum(1 for s in gains if M[('e2', s)]['tests_per_year'] >= 10)} of {len(gains)}; crossings in "
      f"{sum(1 for s in gains if M[('e2', s)]['crossings'] > 0)}; techniques from marks in "
      f"{sum(1 for s in gains if M[('e2', s)]['learned_from_marks'] > 0)}; pooled reputation r = {pearson(pairs)}.")
    t1, t2 = mean_of("techniques", "e1"), mean_of("techniques", "e2")
    l1, l2 = mean_of("technique_median_life", "e1"), mean_of("technique_median_life", "e2")
    w(f"5. Techniques tried {t1:.0f} → {t2:.0f} ({100 * (t2 - t1) / t1:+.0f}%); median life {l1:.1f} → {l2:.1f} years "
      f"({100 * (l2 - l1) / l1:+.0f}%).")
    collapse = [s for s in new if M[("e2", s)]["pop200"] < 5 and M[("e1", s)]["pop200"] >= 5]
    w(f"6. A new world collapsing under E2 but not E1: {', '.join(map(str, collapse)) or 'none'}.")
    w("")
    w("## Per world")
    w("")
    w("| seed | pop @100 E1 → E2 | pop @200 E1 → E2 | infant starvation /1000 E1 → E2 | mixed @100 E1 → E2 |")
    w("|---|---|---|---|---|")
    for s in seeds:
        a, b = M[("e1", s)], M[("e2", s)]
        fmt = lambda v: "–" if v is None else f"{v:.0f}"  # noqa: E731
        pct = lambda v: "–" if v is None else f"{100 * v:.0f}%"  # noqa: E731
        w(f"| {s} | {a['pop100']} → {b['pop100']} | {a['pop200']} → {b['pop200']} | "
          f"{fmt(a['infant_starved_per_1000'])} → {fmt(b['infant_starved_per_1000'])} | {pct(a['mixed100'])} → {pct(b['mixed100'])} |")
    (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("wrote", HERE / "results.md")


if __name__ == "__main__":
    main()
