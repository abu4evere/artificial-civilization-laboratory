"""E7.6 analysis: tables for Q1–Q5 and the frozen predictions in predictions.md, scored as written.
Read-only. Written before any E7.6 result was seen. Writes results.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
ARMS = ("baseline", "e7")
SEEDS = list(range(301, 309))
YEARS = (25, 50, 100, 200, 300, 500, 700, 1000)


def load():
    runs = {}
    for arm in ARMS:
        for s in SEEDS:
            f = HERE / "output" / arm / f"seed_{s}.json"
            if f.exists():
                runs[(arm, s)] = json.loads(f.read_text(encoding="utf-8"))
    return runs


def at(run, year):
    return next((x for x in run["samples"] if x["year"] == year), None)


def per_person_decade(run, d):
    c = run["decades"].get(str(d))
    if not c or not c.get("person_weeks"):
        return None
    person_decades = c["person_weeks"] / 520
    return c.get("deliberate", 0) / person_decades, c.get("play_made", 0) / person_decades


def rank(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2
        i = j + 1
    return r


def spearman(a, b):
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if len(pairs) < 4:
        return None, len(pairs)
    ra, rb = rank([p[0] for p in pairs]), rank([p[1] for p in pairs])
    n = len(pairs)
    ma, mb = sum(ra) / n, sum(rb) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    va = sum((x - ma) ** 2 for x in ra) ** 0.5
    vb = sum((y - mb) ** 2 for y in rb) ** 0.5
    return (round(cov / (va * vb), 2) if va and vb else None), n


def fmt(v):
    return "–" if v is None else (f"{v:.2f}" if isinstance(v, float) else str(v))


def main():
    runs = load()
    L = []
    w = L.append
    w("# E7.6 — Expertise retention audit · Results\n")
    w("Read-only replays of the 16 E7 worlds (seeds 301–308; `baseline` = E6 code, `e7` = E7 code). "
      "Predictions were frozen in predictions.md (tag `E7.6-frozen`) before any run.\n")

    # validity
    w("## Validity\n")
    verify = (HERE / "output" / "verify.txt").read_text(encoding="utf-8").strip().splitlines() \
        if (HERE / "output" / "verify.txt").exists() else []
    ok_ro = len(verify) >= 2 and all("READ-ONLY" in v for v in verify)
    ok_rep = bool(runs) and all(r["replay_matches_saved"] for r in runs.values())
    ok_code = bool(runs) and all(r["code_hash"] == r["code_hash_after"] for r in runs.values())
    w(f"- Probe read-only (both codes, 20 years): **{'yes' if ok_ro else 'NO'}**")
    w(f"- Every replay matches its saved run: **{'yes' if ok_rep else 'NO'}** "
      f"({sum(r['replay_matches_saved'] for r in runs.values())} of {len(runs)})")
    w(f"- Code unchanged during the runs: **{'yes' if ok_code else 'NO'}**")
    w(f"- Worlds replayed: {len(runs)} of 16")
    w(f"- **The audit is {'valid' if ok_ro and ok_rep and ok_code and len(runs) == 16 else 'INVALID or incomplete'}.**\n")

    # Q1
    w("## Q1 — Does crafting skill decay?\n")
    w("Best living crafter / mean of top 10 / mean of everyone alive, at each year (– = world already gone).\n")
    w("| arm | seed | " + " | ".join(f"yr {y}" for y in YEARS) + " |")
    w("|---|---|" + "---|" * len(YEARS))
    for (arm, s), r in sorted(runs.items()):
        cells = []
        for y in YEARS:
            x = at(r, y)
            cells.append(f"{x['skill_best']:.2f} / {x['skill_top10']:.2f} / {x['skill_mean']:.2f}" if x and x["skill_best"] is not None else "–")
        w(f"| {arm} | {s} | " + " | ".join(cells) + " |")
    w("")

    # Q2
    w("## Q2 — Do recipes survive?\n")
    w("Unique recipes held by the living / mean holders per recipe.\n")
    w("| arm | seed | peak unique (year) | " + " | ".join(f"yr {y}" for y in YEARS) + " |")
    w("|---|---|---|" + "---|" * len(YEARS))
    for (arm, s), r in sorted(runs.items()):
        peak = max(r["samples"], key=lambda x: x["recipes_unique"]) if r["samples"] else None
        cells = [f"{x['recipes_unique']} / {x['recipes_mean_holders']}" if (x := at(r, y)) else "–" for y in YEARS]
        w(f"| {arm} | {s} | {peak['recipes_unique']} ({peak['year']}) | " + " | ".join(cells) + " |" if peak else f"| {arm} | {s} | – |")
    w("")

    # Q3
    w("## Q3 — Do people stop making things?\n")
    w("Per person per decade: deliberate makes (from a recipe) / things made in play. Pooled mean over worlds alive in that decade.\n")
    w("| decade | baseline deliberate | baseline play | e7 deliberate | e7 play | worlds alive (b / e7) |")
    w("|---|---|---|---|---|---|")
    for d in (0, 1, 2, 4, 9, 14, 19, 29, 49, 69, 99):
        row = [f"{d * 10}–{d * 10 + 10}"]
        alive = []
        for arm in ARMS:
            vals = [v for (a, s), r in runs.items() if a == arm and (v := per_person_decade(r, d))]
            row += [fmt(sum(v[0] for v in vals) / len(vals)) if vals else "–", fmt(sum(v[1] for v in vals) / len(vals)) if vals else "–"]
            alive.append(str(len(vals)))
        w("| " + " | ".join(row) + f" | {' / '.join(alive)} |")
    w("")

    # Q4
    w("## Q4 — Do watertight vessels exist at all?\n")
    w("| arm | seed | made, total | made per century | samples with anyone carrying one | most carried at once |")
    w("|---|---|---|---|---|---|")
    for (arm, s), r in sorted(runs.items()):
        made = sum(c.get("watertight_made", 0) for c in r["decades"].values())
        cent = made / max(1, r["years_run"] / 100)
        with_one = sum(1 for x in r["samples"] if x["people_with_watertight"] > 0)
        most = max((x["watertight_carried"] for x in r["samples"]), default=0)
        w(f"| {arm} | {s} | {made} | {cent:.1f} | {with_one} of {len(r['samples'])} | {most} |")
    w("")

    # Q5
    w("## Q5 — Expertise against population\n")
    rows = []
    for (arm, s), r in sorted(runs.items()):
        pops = [x["population"] for x in r["samples"]] or [0]
        delib = sum(c.get("deliberate", 0) for c in r["decades"].values())
        pdec = sum(c.get("person_weeks", 0) for c in r["decades"].values()) / 520
        best = [x["skill_best"] for x in r["samples"] if x["skill_best"] is not None]
        b500 = (at(r, 500) or {}).get("skill_best")
        rows.append({"arm": arm, "seed": s, "peak": max(pops), "mean": round(sum(pops) / len(pops), 1),
                     "LFA": r["LFA"], "best_ever": max(best) if best else None, "best_500": b500,
                     "best_end": best[-1] if best else None,
                     "delib_rate": round(delib / pdec, 2) if pdec else None, "years": r["years_run"]})
    w("| arm | seed | lived | peak pop | mean pop | LFA | best skill ever | best @500 | best at end | deliberate / person-decade |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for x in rows:
        w(f"| {x['arm']} | {x['seed']} | {x['years']} | {x['peak']} | {x['mean']} | {fmt(x['LFA'])} | {fmt(x['best_ever'])} | "
          f"{fmt(x['best_500'])} | {fmt(x['best_end'])} | {fmt(x['delib_rate'])} |")
    w("")
    long = [x for x in rows if x["years"] >= 500]
    for label, key, subset in (("mean population vs best skill at year 500", "best_500", long),
                               ("mean population vs deliberate makes per person-decade", "delib_rate", rows),
                               ("mean population vs LFA", "LFA", rows)):
        rho, n = spearman([x["mean"] for x in subset], [x[key] for x in subset])
        w(f"- Spearman ρ, {label}: **{fmt(rho)}** (n = {n})")
    w("\nWith n ≤ 16, and 8 of those pairs sharing seeds, these correlations are descriptive, not tests.\n")

    # predictions
    w("## Frozen predictions, scored\n")

    def score(ok):
        return "**confirmed**" if ok else "**wrong**"

    long3 = [r for r in runs.values() if r["years_run"] >= 300]
    p1 = [(r["arm"], r["seed"], at(r, 50), at(r, 300)) for r in long3]
    ok1 = bool(p1) and all(a and b and b["skill_best"] < a["skill_best"] and b["skill_mean"] < 0.15 for _, _, a, b in p1)
    w(f"1. {score(ok1)} — worlds lived 300+ years: " + "; ".join(
        f"{arm} {s}: best {a['skill_best']:.2f} → {b['skill_best']:.2f}, mean at 300 {b['skill_mean']:.2f}"
        for arm, s, a, b in p1 if a and b) + ".")

    def rates(r, lo, hi):
        vals = [v[0] for d in range(lo, hi) if (v := per_person_decade(r, d))]
        return vals
    ok2 = True
    det = []
    for r in runs.values():
        after = rates(r, 10, 100)
        early = rates(r, 0, 5)
        if after:
            mx = max(after)
            ok2 &= mx < 1 and (sum(after) / len(after)) < (sum(early) / len(early) if early else 1e9)
            det.append(f"{r['arm']} {r['seed']}: max after yr 100 {mx:.2f}, mean {sum(after)/len(after):.2f} vs first 50 yrs {sum(early)/len(early):.2f}")
    w(f"2. {score(ok2 and bool(det))} — " + "; ".join(det) + ".")

    p3 = []
    for r in runs.values():
        if r["years_run"] >= 500 and r["samples"]:
            peak = max(x["recipes_unique"] for x in r["samples"])
            y500 = at(r, 500)["recipes_unique"]
            p3.append((r["arm"], r["seed"], peak, y500))
    ok3 = bool(p3) and all(y <= p / 2 for _, _, p, y in p3)
    w(f"3. {score(ok3)} — peak → year 500 unique recipes: " + "; ".join(f"{a} {s}: {p} → {y}" for a, s, p, y in p3) + ".")

    made_c = [sum(c.get("watertight_made", 0) for c in r["decades"].values()) / max(1, r["years_run"] / 100) for r in runs.values()]
    samples_all = [x for r in runs.values() for x in r["samples"]]
    none_share = sum(1 for x in samples_all if x["people_with_watertight"] == 0) / max(1, len(samples_all))
    ok4 = (sum(made_c) / len(made_c) < 5) and none_share >= 0.5 if made_c else False
    w(f"4. {score(ok4)} — mean watertight things made per world per century {sum(made_c)/len(made_c):.1f}; "
      f"samples with nobody carrying one: {100 * none_share:.0f}%.")

    r_skill, n1 = spearman([x["mean"] for x in long], [x["best_500"] for x in long])
    r_delib, n2 = spearman([x["mean"] for x in rows], [x["delib_rate"] for x in rows])
    ok5 = all(v is not None and 0.3 < v < 0.7 for v in (r_skill, r_delib))
    w(f"5. {score(ok5)} — ρ(population, best skill at 500) = {fmt(r_skill)} (n={n1}); ρ(population, deliberate rate) = {fmt(r_delib)} (n={n2}).")

    comp = []
    for y in (100, 300, 500):
        for key in ("skill_mean",):
            b = [at(r, y)[key] for (a, s), r in runs.items() if a == "baseline" and at(r, y)]
            e = [at(r, y)[key] for (a, s), r in runs.items() if a == "e7" and at(r, y)]
            if b and e:
                comp.append((y, sum(b) / len(b), sum(e) / len(e)))
    db = [x["delib_rate"] for x in rows if x["arm"] == "baseline" and x["delib_rate"] is not None]
    de = [x["delib_rate"] for x in rows if x["arm"] == "e7" and x["delib_rate"] is not None]
    ok6 = all(e <= b * 1.1 for _, b, e in comp) and (sum(de) / len(de) <= 1.1 * sum(db) / len(db))
    w(f"6. {score(ok6)} — mean skill baseline vs e7: " + "; ".join(f"yr {y}: {b:.2f} vs {e:.2f}" for y, b, e in comp)
      + f"; deliberate per person-decade {sum(db)/len(db):.2f} vs {sum(de)/len(de):.2f}. "
      "Reading: 'no higher' allows up to 10% above the baseline.")

    (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
