"""BL0 analysis (questions.md, frozen as `BL0-frozen`, with Amendment 1). Written and smoke-tested before any data.

  python experiments/BL0_habit_use/analyse_bl0.py discovery   # writes results_discovery.md
  python experiments/BL0_habit_use/analyse_bl0.py holdout     # writes results_holdout.md, with the agreement check
  python experiments/BL0_habit_use/analyse_bl0.py --smoke     # the throwaway smoke output (15 years); writes nothing

Per world, then the median across worlds with a bootstrap interval (10,000 resamples, random.Random(2026)).
Decision rules (signed off as decision rules, not scientific truths): Q1, the mean choice effect over adult decisions:
>= 0.10 "habits steer", < 0.02 "habits barely steer", otherwise "habits steer a little". Q2, among adults, own
experience's share of the habit term (of I + C + E + T): >= 50% "mostly learned", < 25% "mostly inherited or absorbed"
(C and T count as absorbed), otherwise "mixed". A label is read only where discovery and holdout agree. Values near a
line are reported as close to it, with their interval. Population beside every measure (rule 18).
"""
from __future__ import annotations

import json
import math
import random
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_bl0 import AGES, DISCOVERY, HI, HOLDOUT, LO, NB, OUT  # noqa: E402

ACTIONS = ("rest", "forage", "hunt", "gather", "put", "take", "make", "play", "explore", "give", "care", "talk", "court",
           "steal", "attack", "flee", "join")
ADULT_BANDS = (3, 4, 5)


def boot(xs, k=10_000):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None, None, None
    rng = random.Random(2026)
    ms = sorted(statistics.median(rng.choices(xs, k=len(xs))) for _ in range(k))
    return statistics.median(xs), ms[int(0.025 * k)], ms[int(0.975 * k) - 1]


def q1_label(x):
    return "habits steer" if x >= 0.10 else "habits barely steer" if x < 0.02 else "habits steer a little"


def q2_label(x):
    return "mostly learned" if x >= 0.50 else "mostly inherited or absorbed" if x < 0.25 else "mixed"


def hist_median(h):
    n = sum(h)
    if not n:
        return None
    run = 0
    for b, c in enumerate(h):
        run += c
        if run >= n / 2:      # bin b >= 1 covers log10 values from (b - 1) to b steps above LO; report its middle
            return 0.0 if b == 0 else 10 ** (math.log10(LO) + (b - 0.5) / (NB - 1) * (math.log10(HI) - math.log10(LO)))
    return None


def per_world(r):
    n, s = r["n"], r["sum"]
    dec = sum(n.get(f"dec_{b}", 0) for b in ADULT_BANDS)
    ce = sum(s.get(f"ce_{b}", 0.0) for b in ADULT_BANDS)
    W = {"seed": r["seed"], "survived": r["final_tick"] >= 120 * 52, "pops": r["pops"],
         "ce_adult": ce / dec if dec else None,
         "top_adult": sum(n.get(f"top_{b}", 0) for b in ADULT_BANDS) / dec if dec else None,
         "ce_band": [s.get(f"ce_{b}", 0.0) / n[f"dec_{b}"] if n.get(f"dec_{b}") else None for b in range(len(AGES))],
         "top_band": [n.get(f"top_{b}", 0) / n[f"dec_{b}"] if n.get(f"dec_{b}") else None for b in range(len(AGES))]}
    wt = s.get("w_total", 0.0)
    for x in "ICET":
        W["w_" + x] = s.get("w_" + x, 0.0) / wt if wt else None
        W["u_" + x] = s.get("u_" + x, 0.0) / n["dec_adult_parts"] if n.get("dec_adult_parts") else None
    W["stale_ce"] = s.get("stale_ce", 0.0) / n["stale_decisions"] if n.get("stale_decisions") else None
    W["stale_value"] = s.get("stale_abs_value", 0.0) / n["stale_options"] if n.get("stale_options") else None
    lin = [x[7] for x in r["snap"] if x[1] in ADULT_BANDS and x[7] is not None]
    W["lineage"] = statistics.mean(lin) if lin else None
    W["snap"] = r["snap"]
    W["desc"] = r["desc"]
    return W


def fmt(x, nd=3):
    return "–" if x is None else f"{x:.{nd}f}"


def ci(t, nd=3):
    m, a, b = t
    return "–" if m is None else f"{m:.{nd}f} [{a:.{nd}f}, {b:.{nd}f}]"


def summarise(rows):
    W = [per_world(r) for r in rows]
    S = {"W": W, "q1": boot([w["ce_adult"] for w in W]), "top": boot([w["top_adult"] for w in W]),
         "q2E": boot([w["w_E"] for w in W])}
    for x in "ICET":
        S["w_" + x] = boot([w["w_" + x] for w in W])
        S["u_" + x] = boot([w["u_" + x] for w in W])
    return S


def report(which, rows, smoke):
    L = [f"# BL0 — does ACL's brain meaningfully learn? Results ({'SMOKE TEST, throwaway seed' if smoke else which})", "",
         "Frozen as `BL0-frozen`, with Amendment 1 (`BL0-amend1`, part T). run_bl0.py, analyse_bl0.py.", "", "## Validity", ""]
    ok = True
    if not smoke:
        z = OUT / "zero.txt"
        zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
        L.append(f"- Logging copy reproduces the control world; parts add up (zero check): **{'yes' if zt else 'NO'}**")
        ok &= zt
    fps = {r["code_hash"] for r in rows} | {r["code_hash_after"] for r in rows}
    err = max(r["max_split_error"] for r in rows)
    nz = sum(r["n"].get("first_seen_nonzero", 0) for r in rows)
    L += [f"- One code fingerprint (`code_bl0`): **{'yes' if len(fps) == 1 else 'NO'}**",
          f"- I + C + E + T = habit, and the origin split = habit, every person every week: largest error {err:.2g} "
          f"(**{'yes' if err <= 1e-9 else 'NO'}**, ≤ 1e-9)",
          f"- People first seen with habits the observer had not followed: {nz} (must be 0)",
          f"- Worlds: {len(rows)}; deepest generation: {max(r['max_generation'] for r in rows)}"]
    ok &= len(fps) == 1 and err <= 1e-9 and nz == 0
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome below may be read.'}**", ""]
    S = summarise(rows)
    W = S["W"]
    pops = [[w["pops"][i] if i < len(w["pops"]) else 0 for w in W] for i in range(12)]
    L += ["## Population and survival (rules 14 and 18)", "",
          f"Survived 120 years: {sum(w['survived'] for w in W)} of {len(W)}. Median population at years 10 / 30 / 60 / 90 / 120: "
          + " / ".join(fmt(statistics.median(pops[i]), 0) if pops[i] else "–" for i in (0, 2, 5, 8, 11)) + ".", "",
          "## Q1 — habits' effect on scores and on choices", "",
          f"**Choice effect, mean over adult decisions** (probability the choice would differ without the learned term), "
          f"median across worlds [95% interval]: **{ci(S['q1'])}** → decision rule: **{q1_label(S['q1'][0]) if S['q1'][0] is not None else '–'}**", "",
          f"Adult decisions whose top-scoring option changes without the learned term: {ci(S['top'])}", "",
          "| age | choice effect (median of world means) | top option changes |", "|---|---|---|"]
    for b, (a, z) in enumerate(AGES):
        L.append(f"| {f'{a}–{z - 1}' if z < 200 else f'{a}+'} | {fmt(boot([w['ce_band'][b] for w in W])[0])} | "
                 f"{fmt(boot([w['top_band'][b] for w in W])[0])} |")
    hl = [[sum(r["hist"]["L"][a][k] for r in rows) for k in range(NB)] for a in range(len(ACTIONS))]
    hi = [[sum(r["hist"]["inst"][a][k] for r in rows) for k in range(NB)] for a in range(len(ACTIONS))]
    L += ["", "Score effect per action (all decisions, all worlds pooled; medians approximate to one histogram bin):", "",
          "| action | median abs learned | median abs instinct | ratio |", "|---|---|---|---|"]
    for a, name in enumerate(ACTIONS):
        ml, mi = hist_median(hl[a]), hist_median(hi[a])
        L.append(f"| {name} | {fmt(ml, 4)} | {fmt(mi, 4)} | {fmt(ml / mi if ml is not None and mi else None, 3)} |")
    L += ["", "## Q2 — where the habit term comes from (adults)", "",
          "| part | share of the choice effect (weighted) | share of the habit term (unweighted) |", "|---|---|---|"]
    for x, name in zip("ICET", ("inherited (I)", "caregiver (C)", "own experience (E)", "copied in talk (T)")):
        L.append(f"| {name} | {ci(S['w_' + x])} | {ci(S['u_' + x])} |")
    L += ["", f"Own experience's share → decision rule: **{q2_label(S['q2E'][0]) if S['q2E'][0] is not None else '–'}**", "",
          "By age (yearly snapshots, all worlds pooled): values with |E| ≥ 0.05 (of 544), and each part's share:", "",
          "| age | people-years | values with own experience | I | C | E | T |", "|---|---|---|---|---|---|---|"]
    for b, (a, z) in enumerate(AGES):
        xs = [x for w in W for x in w["snap"] if x[1] == b and x[3] is not None]
        if xs:
            L.append(f"| {f'{a}–{z - 1}' if z < 200 else f'{a}+'} | {len(xs)} | {statistics.median(x[2] for x in xs):.0f} | "
                     + " | ".join(f"{statistics.mean(x[3 + j] for x in xs):.3f}" for j in range(4)) + " |")
    L += ["", "## Q3 — persistence", "",
          f"Later life: when a situation comes back with habits not used for 52+ weeks, their mean abs value "
          f"{ci(boot([w['stale_value'] for w in W]))}; the choice effect of those habits alone {ci(boot([w['stale_ce'] for w in W]))}.", "",
          "Descendants (all children pooled; correlation over the 544 values with parents' habits at birth, and with an "
          "unrelated adult's; described, not thresholded):", "",
          "| age | children | parents r (mean) | unrelated adult r (mean) | parents − unrelated [95% interval] | I share | E share |",
          "|---|---|---|---|---|---|---|"]
    for age in (12, 20, 40):
        xs = [d for w in W for d in w["desc"] if d[0] == age and d[1] is not None and d[2] is not None]
        if xs:
            diffs = [d[1] - d[2] for d in xs]
            rng = random.Random(2026)
            bs = sorted(statistics.mean(rng.choices(diffs, k=len(diffs))) for _ in range(10_000))
            L.append(f"| {age} | {len(xs)} | {statistics.mean(d[1] for d in xs):.3f} | {statistics.mean(d[2] for d in xs):.3f} | "
                     f"{statistics.mean(diffs):.3f} [{bs[250]:.3f}, {bs[9749]:.3f}] | "
                     f"{statistics.mean(d[3] for d in xs if d[3] is not None):.3f} | {statistics.mean(d[4] for d in xs if d[4] is not None):.3f} |")
        else:
            L.append(f"| {age} | 0 | – | – | – | – | – |")
    L += ["", f"Lineage: adults' share of the habit term that traces to the experience of people two or more generations "
          f"above them: {ci(boot([w['lineage'] for w in W]))}", "", "## Q4 — reach and staleness", ""]
    ctx = [sum(r["ctx_count"].get(str(k), r["ctx_count"].get(k, 0)) for r in rows) for k in range(32)]
    tot = sum(ctx)
    py = tot / 52 if tot else 0
    L.append("Situations recurring per person-year (32 situations; all worlds pooled): "
             + ", ".join(f"{c / py:.1f}" for c in ctx) + "." if py else "No decisions.")
    st = {}
    for r in rows:
        for k, v in r["staleness_weeks"].items():
            st[int(k)] = st.get(int(k), 0) + v
    if st:
        n = sum(st.values())
        run, med = 0, None
        for k in sorted(st):
            run += st[k]
            if run >= n / 2:
                med = k
                break
        L.append(f"Weeks since the chosen habit value last changed, when used: median {med} (capped at 520).")
    if which == "holdout" and not smoke:
        D = summarise([json.loads((OUT / f"seed_{s}.json").read_text(encoding="utf-8")) for s in DISCOVERY])
        a1, b1 = q1_label(D["q1"][0]), q1_label(S["q1"][0])
        a2, b2 = q2_label(D["q2E"][0]), q2_label(S["q2E"][0])
        L += ["", "## Do discovery and holdout agree? (a label is read only where they agree)", "",
              "| rule | discovery | holdout | stands |", "|---|---|---|---|",
              f"| Q1 | {a1} ({ci(D['q1'])}) | {b1} ({ci(S['q1'])}) | {'**yes: ' + b1 + '**' if a1 == b1 else 'no'} |",
              f"| Q2 | {a2} ({ci(D['q2E'])}) | {b2} ({ci(S['q2E'])}) | {'**yes: ' + b2 + '**' if a2 == b2 else 'no'} |"]
    return L


def main(which, smoke=False):
    if smoke:
        rows = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((HERE / "output_smoke").glob("seed_*.json"))]
    else:
        seeds = DISCOVERY if which == "discovery" else HOLDOUT
        rows = [json.loads((OUT / f"seed_{s}.json").read_text(encoding="utf-8")) for s in seeds
                if (OUT / f"seed_{s}.json").exists()]
        if len(rows) < len(seeds):
            print(f"NOTE: {len(seeds) - len(rows)} worlds missing")
    text = "\n".join(report(which, rows, smoke)) + "\n"
    if not smoke:
        (HERE / f"results_{which}.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        main("discovery", smoke=True)
    else:
        main(sys.argv[1])
