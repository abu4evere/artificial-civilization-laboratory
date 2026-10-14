"""ID1 analysis (questions.md, frozen as `ID1-frozen`). Written and smoke-tested before any data.

  python experiments/ID1_memory_identity/analyse_id1.py discovery   # writes results_discovery.md
  python experiments/ID1_memory_identity/analyse_id1.py holdout     # writes results_holdout.md, with the agreement check
  python experiments/ID1_memory_identity/analyse_id1.py --smoke     # the throwaway smoke output (8 weeks; window 4); writes nothing

Frozen tests (operational details in questions.md):
- Behaviour = share of each of the 17 actions over a window; weeks 1-26 (swapped), 27-52 (restored). A person alive for
  fewer than 13 weeks of a window is dropped from that window. Drift = Jensen-Shannon divergence (base 2).
- Q1: arm drift vs sham drift, weeks 1-26, paired Wilcoxon (two-sided), Holm over the eight arms; "moves the person" if
  adjusted p < 0.05 and the median paired difference > 0.
- Q2: pulled = the arm's mix is closer to the donor's original mix than to the focal person's own original mix; exact
  sign test against the same indicator in the sham (paired, discordant pairs); Holm over eight.
- Q3: from "all but temperament": pulled (Q2, adjusted p < 0.05, more pulled than the sham) = "follows their parts, not
  their temperament"; else Q1 significant = "changed, but not into the donor"; else "temperament holds them".
- Q4: for each arm that moved the person, drift in weeks 27-52 vs sham drift, paired Wilcoxon, Holm over those arms;
  p >= 0.05 = "no detectable lasting change" (not proof of full return); p < 0.05 = "a lasting change".
- Hard stops: one code fingerprint; the original copy reproduces the uncopied world; the sham and every swap differ.
"""
from __future__ import annotations

import json
import math
import statistics
import sys
from pathlib import Path

from scipy.stats import binomtest, wilcoxon

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_id1 import DISCOVERY, HOLDOUT, OUT, PARTS  # noqa: E402

ACTIONS = ("rest", "forage", "hunt", "gather", "put", "take", "make", "play", "explore", "give", "care", "talk", "court",
           "steal", "attack", "flee", "join")     # acl/person.py ACTIONS (17; correction of 12 October)
ARMS = list(PARTS)


def mix(acts, a, b, min_weeks):
    xs = [x for x in acts[a:b] if x is not None]
    if len(xs) < min_weeks:
        return None
    return [xs.count(k) / len(xs) for k in ACTIONS]


def jsd(p, q):
    m = [(x + y) / 2 for x, y in zip(p, q)]
    kl = lambda u, v: sum(x * math.log2(x / y) for x, y in zip(u, v) if x > 0)  # noqa: E731
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, run = [0.0] * len(ps), 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - r) * ps[i]))
        adj[i] = run
    return adj


def wil(diffs):
    if not diffs or all(d == 0 for d in diffs):
        return 1.0
    try:
        return float(wilcoxon(diffs).pvalue)
    except ValueError:
        return 1.0


def people(rows, half, min_weeks):
    """One record per focal person: mixes per arm and window."""
    out, dropped = [], {"early": 0, "late": 0}
    for r in rows:
        if "pairs" not in r or not r["pairs"] or "original" not in r:
            continue
        for pr in r["pairs"]:
            f, d = pr["focal"], pr["donor"]
            o, s = r["original"]["acts"], r["sham"]["acts"]
            rec = {"seed": r["seed"], "focal": f, "age": pr["focal_age"], "partnered": pr["focal_partnered"],
                   "pop": r["pop_at_snapshot"], "early": {}, "late": {}}
            for win, (a, b) in (("early", (0, half)), ("late", (half, 2 * half))):
                base = {"orig": mix(o[f], a, b, min_weeks), "sham": mix(s[f], a, b, min_weeks),
                        "donor": mix(o[d], a, b, min_weeks)}
                for arm in ARMS:
                    base[arm] = mix(r["swaps"][f"{f}:{arm}"]["acts"], a, b, min_weeks)
                rec[win] = base
                if base["orig"] is None or base["sham"] is None:
                    dropped[win] += 1
            rec["alive_end"] = o[f][-1] is not None if o[f] else False
            out.append(rec)
    return out, dropped


def tests(P):
    R = {}
    q1p, q1med, q1n = [], [], []
    for arm in ARMS:
        diffs = [jsd(p["early"][arm], p["early"]["orig"]) - jsd(p["early"]["sham"], p["early"]["orig"])
                 for p in P if p["early"]["orig"] and p["early"]["sham"] and p["early"][arm]]
        q1p.append(wil(diffs))
        q1med.append(statistics.median(diffs) if diffs else None)
        q1n.append(len(diffs))
    q1a = holm(q1p)
    R["q1"] = {arm: {"n": q1n[i], "median_diff": q1med[i], "p": q1p[i], "p_holm": q1a[i],
                     "moves": q1a[i] < 0.05 and (q1med[i] or 0) > 0} for i, arm in enumerate(ARMS)}
    q2p, q2c = [], []
    for arm in ARMS:
        a_only = s_only = n = n_arm = n_sham = 0
        for p in P:
            e = p["early"]
            if not (e["orig"] and e["sham"] and e[arm] and e["donor"]):
                continue
            pa = jsd(e[arm], e["donor"]) < jsd(e[arm], e["orig"])
            ps = jsd(e["sham"], e["donor"]) < jsd(e["sham"], e["orig"])
            n += 1
            n_arm += pa
            n_sham += ps
            a_only += pa and not ps
            s_only += ps and not pa
        q2p.append(binomtest(a_only, a_only + s_only).pvalue if a_only + s_only else 1.0)
        q2c.append((n, n_arm, n_sham, a_only, s_only))
    q2a = holm(q2p)
    R["q2"] = {arm: {"n": q2c[i][0], "pulled_arm": q2c[i][1], "pulled_sham": q2c[i][2], "arm_only": q2c[i][3],
                     "sham_only": q2c[i][4], "p": q2p[i], "p_holm": q2a[i],
                     "pulled": q2a[i] < 0.05 and q2c[i][3] > q2c[i][4]} for i, arm in enumerate(ARMS)}
    abt = "all_but_temperament"
    R["q3"] = ("the person follows their parts, not their temperament" if R["q2"][abt]["pulled"]
               else "changed, but not into the donor" if R["q1"][abt]["moves"] else "temperament holds them")
    moved = [a for a in ARMS if R["q1"][a]["moves"]]
    q4p, q4m, q4n = [], [], []
    for arm in moved:
        diffs = [jsd(p["late"][arm], p["late"]["orig"]) - jsd(p["late"]["sham"], p["late"]["orig"])
                 for p in P if p["late"]["orig"] and p["late"]["sham"] and p["late"][arm]]
        q4p.append(wil(diffs))
        q4m.append(statistics.median(diffs) if diffs else None)
        q4n.append(len(diffs))
    q4a = holm(q4p) if q4p else []
    R["q4"] = {arm: {"n": q4n[i], "median_diff": q4m[i], "p": q4p[i], "p_holm": q4a[i],
                     "reading": "a lasting change" if q4a[i] < 0.05 else "no detectable lasting change"}
               for i, arm in enumerate(moved)}
    return R


def f(x, nd=3):
    return "–" if x is None else f"{x:.{nd}g}" if isinstance(x, float) else str(x)


def report(which, rows, P, dropped, R, smoke):
    L = [f"# ID1 — what makes an ACL person who they are? Results ({'SMOKE TEST, throwaway seed' if smoke else which})",
         "", "Frozen as `ID1-frozen` (correction of 12 October appended). run_id1.py, analyse_id1.py.", "", "## Validity", ""]
    fps = {r["code_hash"] for r in rows} | {r["code_hash_after"] for r in rows}
    done = [r for r in rows if "original" in r]
    rep = all(r["original_reproduces"] for r in done)
    dif = all(r["all_differ"] for r in done)
    ok = len(fps) == 1 and rep and (dif or smoke)
    L += [f"- One code fingerprint (`code_e13r`): **{'yes' if len(fps) == 1 else 'NO'}**",
          f"- The original copy reproduces the uncopied world in every world: **{'yes' if rep else 'NO'}**",
          f"- The sham and every swap differ from the original: **{'yes' if dif else 'NO'}**"
          + (" (not required in the smoke test: 4-week window)" if smoke else ""),
          f"- Worlds: {len(rows)}; skipped: {len(rows) - len(done)}"
          + "".join(f" (seed {r['seed']}: {r['skipped']})" for r in rows if "skipped" in r),
          f"- Focal people: {len(P)}; dropped (alive fewer than 13 weeks, or 2 in the smoke test): weeks 1–26 "
          f"{dropped['early']}, weeks 27–52 {dropped['late']}", "",
          f"**{'Valid.' if ok else 'NOT VALID: no outcome below may be read.'}**", "",
          "## Who (population beside every measure, rule 18)", ""]
    if P:
        L.append(f"Median population at the snapshot {statistics.median(p['pop'] for p in P):.0f}; focal people's median "
                 f"age {statistics.median(p['age'] for p in P):.1f}; partnered {sum(p['partnered'] for p in P)} of {len(P)}; "
                 f"alive at the end of the 52 weeks (original copy) {sum(p['alive_end'] for p in P)} of {len(P)}.")
    L += ["", "## Q1 — which parts move a person? (weeks 1–26; drift vs sham drift)", "",
          "| arm | people | median (arm − sham) drift | p | Holm p | moves the person |", "|---|---|---|---|---|---|"]
    for a in ARMS:
        q = R["q1"][a]
        L.append(f"| {a} | {q['n']} | {f(q['median_diff'])} | {f(q['p'])} | {f(q['p_holm'])} | {'**yes**' if q['moves'] else 'no'} |")
    L += ["", "## Q2 — pulled toward the donor? (weeks 1–26)", "",
          "| arm | people | pulled (arm) | pulled (sham) | arm only / sham only | p | Holm p | pulled |", "|---|---|---|---|---|---|---|---|"]
    for a in ARMS:
        q = R["q2"][a]
        L.append(f"| {a} | {q['n']} | {q['pulled_arm']} | {q['pulled_sham']} | {q['arm_only']} / {q['sham_only']} | "
                 f"{f(q['p'])} | {f(q['p_holm'])} | {'**yes**' if q['pulled'] else 'no'} |")
    L += ["", f"## Q3 — is temperament enough?", "", f"**{R['q3']}**", "",
          "## Q4 — does restoring bring them back? (weeks 27–52; only arms that moved the person)", ""]
    if R["q4"]:
        L += ["| arm | people | median (arm − sham) drift | p | Holm p | reading |", "|---|---|---|---|---|---|"]
        for a, q in R["q4"].items():
            L.append(f"| {a} | {q['n']} | {f(q['median_diff'])} | {f(q['p'])} | {f(q['p_holm'])} | **{q['reading']}** |")
    else:
        L.append("No arm moved the person in Q1, so Q4 has nothing to test.")
    return L


def sig(R):
    return ({a: R["q1"][a]["moves"] for a in ARMS}, {a: R["q2"][a]["pulled"] for a in ARMS}, R["q3"],
            {a: v["reading"] for a, v in R["q4"].items()})


def main(which, smoke=False):
    if smoke:
        rows = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((HERE / "output_smoke").glob("seed_*.json"))]
        half, minw = 4, 2
    else:
        seeds = DISCOVERY if which == "discovery" else HOLDOUT
        rows = [json.loads((OUT / f"seed_{s}.json").read_text(encoding="utf-8")) for s in seeds
                if (OUT / f"seed_{s}.json").exists()]
        half, minw = 26, 13
        if len(rows) < len(seeds):
            print(f"NOTE: {len(seeds) - len(rows)} worlds missing")
    P, dropped = people(rows, half, minw)
    R = tests(P)
    L = report(which, rows, P, dropped, R, smoke)
    if which == "holdout" and not smoke:
        drows = [json.loads((OUT / f"seed_{s}.json").read_text(encoding="utf-8")) for s in DISCOVERY]
        D = tests(people(drows, half, minw)[0])
        a, b = sig(D), sig(R)
        L += ["", "## Do discovery and holdout agree? (a reading stands only if they agree in direction and significance)", "",
              "| question | discovery | holdout | stands |", "|---|---|---|---|"]
        for arm in ARMS:
            L.append(f"| Q1 {arm} moves | {a[0][arm]} | {b[0][arm]} | {'yes' if a[0][arm] == b[0][arm] else 'no'} |")
        for arm in ARMS:
            L.append(f"| Q2 {arm} pulled | {a[1][arm]} | {b[1][arm]} | {'yes' if a[1][arm] == b[1][arm] else 'no'} |")
        L.append(f"| Q3 | {a[2]} | {b[2]} | {'yes' if a[2] == b[2] else 'no'} |")
        for arm in sorted(set(a[3]) | set(b[3])):
            L.append(f"| Q4 {arm} | {a[3].get(arm, '–')} | {b[3].get(arm, '–')} | "
                     f"{'yes' if a[3].get(arm) == b[3].get(arm) else 'no'} |")
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / f"results_{which}.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        main("discovery", smoke=True)
    else:
        main(sys.argv[1])
