"""MB1a analysis (questions.md, Stage A, frozen as `MB1a-frozen`). Written and smoke-tested before any data.

  python experiments/MB1_multi_band/analyse_mb1a.py discovery    # writes results_mb1a_discovery.md
  python experiments/MB1_multi_band/analyse_mb1a.py holdout      # writes results_mb1a_holdout.md, with the agreement check
  python experiments/MB1_multi_band/analyse_mb1a.py --smoke      # the throwaway smoke output only; writes nothing

Frozen reading, per arm: the median across worlds of the between-lineage meeting rate per adult pair-year;
>= 0.05 "bands meet like forager bands"; < 0.005 "bands are effectively closed"; otherwise "rarely". A reading stands only
if discovery and holdout agree. Worlds with no adult pair of different lineages in any year are reported separately.
Everything else is described, not thresholded. Population is reported beside every measure (rule 18).
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_mb1a import ARMS, OUT, SEEDS  # noqa: E402

NAMES = {"c": "C (20 founders, 40 × 40)", "p": "P (80 founders, 40 × 40)", "lp": "LP (80 founders, 80 × 80)"}
HI, LO = 0.05, 0.005


def reading(x):
    if x is None:
        return "no between-lineage pairs"
    return "bands meet like forager bands" if x >= HI else "bands are effectively closed" if x < LO else "rarely"


def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def f(x, nd=4):
    return "–" if x is None else f"{x:.{nd}f}"


def rate(t, num, den):
    return t.get(num, 0) / t[den] if t.get(den) else None


def load(which, out=OUT, seeds=None):
    seeds = seeds or SEEDS[which]
    rows, missing = {}, []
    for arm, ss in seeds.items():
        for s in ss:
            p = out / f"{arm}_seed_{s}.json"
            if p.exists():
                rows.setdefault(arm, []).append(json.loads(p.read_text(encoding="utf-8")))
            else:
                missing.append(f"{arm} {s}")
    return rows, missing


def block_rates(r, a, b):
    """Meeting rate over years a..b-1 of one world, or None if no pair was exposed then."""
    ex = sum(y[1] for y in r["per_year"] if a <= y[0] < b)
    return sum(y[2] for y in r["per_year"] if a <= y[0] < b) / ex if ex else None


def arm_summary(rs):
    worlds = []
    for r in rs:
        t = r["tot"]
        worlds.append({"meet": rate(t, "met", "exposed"), "inter": rate(t, "interacted", "exposed"),
                       "meet_ss": rate(t, "met_ss", "exposed_ss"), "inter_ss": rate(t, "interacted_ss", "exposed_ss"),
                       "pairs": t.get("pair", 0), "pairs_cross": t.get("pair_cross", 0),
                       "learned": t.get("learn_taught", 0) + t.get("learn_copied", 0), "learned_cross": t.get("learn_cross", 0),
                       "survived": r["final_tick"] >= 120 * 52, "pops": r["pops"], "lineages": r["lineages_alive"],
                       "blocks": [block_rates(r, a, a + 30) for a in (0, 30, 60, 90)]})
    exposed = [w for w in worlds if w["meet"] is not None]
    S = {"n": len(worlds), "n_exposed": len(exposed), "n_closed_by_loss": len(worlds) - len(exposed),
         "meet": med(w["meet"] for w in exposed), "inter": med(w["inter"] for w in exposed),
         "meet_ss": med(w["meet_ss"] for w in exposed), "inter_ss": med(w["inter_ss"] for w in exposed),
         "pairs": sum(w["pairs"] for w in worlds), "pairs_cross": sum(w["pairs_cross"] for w in worlds),
         "worlds_cross_couple": sum(1 for w in worlds if w["pairs_cross"] > 0),
         "learned": sum(w["learned"] for w in worlds), "learned_cross": sum(w["learned_cross"] for w in worlds),
         "survived": sum(w["survived"] for w in worlds),
         "blocks": [med(w["blocks"][i] for w in worlds) for i in range(4)],
         "pop_decades": [med(w["pops"][i] if i < len(w["pops"]) else 0 for w in worlds) for i in range(12)],
         "lin_decades": [med(w["lineages"][i] if i < len(w["lineages"]) else 0 for w in worlds) for i in range(12)]}
    return S


def validity(rows, missing, which, smoke):
    L, ok = [], True
    if not smoke:
        z = OUT / "zero.txt"
        zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
        L.append(f"- Observer leaves the world unchanged (zero check): **{'yes' if zt else 'NO'}**")
        ok &= zt
        L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
        ok &= not missing
    for arm, rs in rows.items():
        fps = {r["code_hash"] for r in rs} | {r["code_hash_after"] for r in rs}
        same = len(fps) == 1
        L.append(f"- {arm}: one code fingerprint (`{ARMS[arm][0]}`): **{'yes' if same else 'NO'}**")
        ok &= same
        if not smoke:
            ref = all(r.get("saved_code_hash") == r["code_hash"] for r in rs)
            rep = all(r.get("reproduces") for r in rs)
            rep_h = sum(1 for r in rs if r.get("reproduces_hash"))
            L.append(f"- {arm}: same code as the saved worlds: **{'yes' if ref else 'NO'}**; every replay reproduces its "
                     f"saved decade populations (frozen check): **{'yes' if rep else 'NO'}**; final state hash also equal: "
                     f"{rep_h} of {len(rs)}")
            ok &= ref and rep
        unk = sum(r["unknown_lineage"] for r in rs)
        L.append(f"- {arm}: people of unknown lineage (left out of every pair): {unk}")
    L.append("")
    L.append(f"**{'Valid.' if ok else 'NOT VALID: no outcome below may be read.'}**")
    return L, ok


def table(S, which):
    w = []
    arms = [a for a in ("c", "p", "lp") if a in S]
    w.append("| | " + " | ".join(NAMES[a] for a in arms) + " |")
    w.append("|---|" + "---|" * len(arms))

    def row(label, fn):
        w.append(f"| {label} | " + " | ".join(fn(S[a]) for a in arms) + " |")

    row("worlds (survived 120 years)", lambda s: f"{s['n']} ({s['survived']})")
    row("median population, years 10 / 60 / 120", lambda s: " / ".join(f(s['pop_decades'][i], 0) for i in (0, 5, 11)))
    row("median lineages alive, years 10 / 60 / 120", lambda s: " / ".join(f(s['lin_decades'][i], 0) for i in (0, 5, 11)))
    row("worlds with no between-lineage adult pair in any year", lambda s: str(s["n_closed_by_loss"]))
    row("**meeting: median rate per adult pair-year (frozen measure)**", lambda s: f"**{f(s['meet'])}**")
    row("**reading**", lambda s: f"**{reading(s['meet'])}**")
    row("same-sex pairs only (Hill et al.'s sample; described)", lambda s: f(s["meet_ss"]))
    row("interacting (chose to talk, give or court): median per pair-year", lambda s: f(s["inter"]))
    row("interacting, same-sex pairs", lambda s: f(s["inter_ss"]))
    row("meeting by period, years 0–29 / 30–59 / 60–89 / 90–119", lambda s: " / ".join(f(x) for x in s["blocks"]))
    row("couples formed: between lineages / all", lambda s: f"{s['pairs_cross']} / {s['pairs']}"
        + (f" ({s['pairs_cross'] / s['pairs']:.1%})" if s["pairs"] else ""))
    row("worlds with at least one between-lineage couple", lambda s: f"{s['worlds_cross_couple']} of {s['n']}")
    row("recipes learned from a person of another lineage / all learned from people", lambda s:
        f"{s['learned_cross']} / {s['learned']}" + (f" ({s['learned_cross'] / s['learned']:.1%})" if s["learned"] else ""))
    return w


def main(which, smoke=False):
    if smoke:
        rows, missing = load(which, out=HERE / "output_mb1a_smoke", seeds={"c": (9301,)})
    else:
        rows, missing = load(which)
    L = [f"# MB1a — do ACL's bands meet? Results ({'SMOKE TEST, throwaway seed' if smoke else which})", "",
         "Frozen as `MB1a-frozen` (Stage A; correction of 12 October appended). Read-only replays; run_mb1a.py, "
         "analyse_mb1a.py.", "", "## Validity", ""]
    v, ok = validity(rows, missing, which, smoke)
    L += v
    S = {a: arm_summary(rs) for a, rs in rows.items()}
    L += ["", "## Measures (population beside every measure, rule 18)", ""] + table(S, which)
    L += ["", f"Thresholds (operational cut-offs informed by Hill et al. 2014, not biological boundaries): ≥ {HI} meet like "
          f"forager bands; < {LO} effectively closed; otherwise rarely. \"Within sight\" is an upper bound on contact "
          "(correction of 12 October)."]
    if which == "holdout" and not smoke:
        drows, dmiss = load("discovery")
        D = {a: arm_summary(rs) for a, rs in drows.items()}
        L += ["", "## Do discovery and holdout agree? (the frozen condition for a reading to stand)", "",
              "| arm | discovery | holdout | stands |", "|---|---|---|---|"]
        for a in ("c", "p", "lp"):
            if a in S and a in D:
                rd, rh = reading(D[a]["meet"]), reading(S[a]["meet"])
                L.append(f"| {NAMES[a]} | {rd} ({f(D[a]['meet'])}) | {rh} ({f(S[a]['meet'])}) | "
                         f"{'**yes: ' + rh + '**' if rd == rh else 'no: no reading'} |")
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / f"results_mb1a_{which}.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        main("discovery", smoke=True)
    else:
        main(sys.argv[1])
