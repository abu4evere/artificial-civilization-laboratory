"""CT1 analysis in the frozen order (questions.md, `CT1-frozen`). Written and committed before any data.

  python experiments/CT1_courting_nature/analyse_ct1.py            # writes results.md
  python experiments/CT1_courting_nature/analyse_ct1.py --smoke    # throwaway smoke outputs; writes nothing

Validity (no outcome shown otherwise): zero checks pass; all 1,024 worlds present; one fingerprint (`code_ct1`);
manipulation checks: K1 and K12 (Amendment 1), K1 acts: at least one acceptance v3 would have refused; K2 and K12, courting attempts per single adult-year rise against C (paired Wilcoxon, p < 0.05, mean > 0).
Primary: died out (final_tick < 120 years); each arm against C paired by seed: exact sign test, Holm over the three;
effect = C's share - the arm's, 95% bootstrap (10,000, random.Random(2026)); yardstick 0.117.
Then mechanism outcomes, harm outcomes, the interaction, and the frozen adoption rule.
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_ct1 import ARMS, FAM_BINS, LONELY_BINS, OUT, SEEDS, SMOKE_SEEDS  # noqa: E402
from scipy.stats import binomtest, wilcoxon  # noqa: E402

YARD = 0.117
WPY = 52
CANDS = ("k1", "k2", "k12")


def boot(d):
    rng = random.Random(2026)
    m = sorted(statistics.fmean(rng.choice(d) for _ in d) for _ in range(10000))
    return statistics.fmean(d), m[249], m[9749]


def wil(d):
    return wilcoxon(d).pvalue if any(x != 0 for x in d) else 1.0


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, run = [0.0] * len(ps), 0.0
    for k, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - k) * ps[i]))
        adj[i] = run
    return adj


def died(r):
    return int(r["final_tick"] < 120 * WPY)


def ysum(r, key):
    return sum(v.get(key, 0) for v in r["years"].values())


def per_world(r):
    c = r["courting"]
    ww = ysum(r, "woman_weeks")
    births = len(r["births"])
    inf = sum(1 for d in r["deaths"] if d[3] == "infant")
    return {
        "no_aff_accepted": c.get("accepted_no_aff", 0),
        "attempts_per_single_year": c.get("attempts", 0) / (c["single_adult_weeks"] / WPY) if c.get("single_adult_weeks") else 0.0,
        "births_per_woman_year": births / (ww / WPY) if ww else 0.0,
        "single_share": ysum(r, "r_no_partner") / ww if ww else 0.0,
        "pairs": c.get("pairs", 0),
        "infant_deaths_per_birth": inf / births if births else None,
        "adult_starvation": sum(1 for d in r["deaths"] if d[1] == "starvation" and d[3] == "adult"),
        "young_or_older_father_share": ((c.get("births_mother_under_18", 0) + c.get("births_father_15_older", 0))
                                        / c["births"]) if c.get("births") else None,
    }


def paired(rows, a, key, seeds):
    d = [rows[a][s]["m"][key] - rows["c"][s]["m"][key] for s in seeds
         if rows[a][s]["m"][key] is not None and rows["c"][s]["m"][key] is not None]
    return d


def main(smoke=False):
    seeds = SMOKE_SEEDS if smoke else SEEDS
    out = HERE / "output_smoke" if smoke else OUT
    rows, missing = {}, []
    for a in ARMS:
        for s in seeds:
            f = out / f"{a}_seed_{s}.json"
            if f.exists():
                r = json.loads(f.read_text(encoding="utf-8"))
                r["m"] = per_world(r)
                rows.setdefault(a, {})[s] = r
            else:
                missing.append(f"{a} {s}")
    L = [f"# CT1 — courting as nature: results{' (SMOKE TEST, throwaway seeds)' if smoke else ''}", "",
         "Frozen as `CT1-frozen`. run_ct1.py, analyse_ct1.py. Nature v3.", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks: **{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing
    manip = {}
    if not missing:
        allr = [r for a in rows.values() for r in a.values()]
        fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
        L.append(f"- One fingerprint (`code_ct1`): **{'yes' if len(fps) == 1 else 'NO'}**")
        ok &= len(fps) == 1
        for a in ("k1", "k12"):                     # Amendment 1: K1 acts (an acceptance v3 would have refused)
            fl = sum(rows[a][s]["courting"].get("accepted_flipped", 0) for s in seeds)
            att = sum(rows[a][s]["courting"].get("attempts", 0) for s in seeds)
            wf = sum(1 for s in seeds if rows[a][s]["courting"].get("accepted_flipped", 0))
            t = fl >= 1
            manip[(a, "flipped")] = t
            L.append(f"- Manipulation check (Amendment 1), {a.upper()}: K1 acts, acceptances v3 would have refused: {fl} "
                     f"({100 * fl / att if att else 0:.2f} per 100 attempts; in {wf} of {len(seeds)} worlds): "
                     f"**{'yes' if t else 'NO'}**")
            ok &= t
        for a, key, label in (("k2", "attempts_per_single_year", "K2: courting attempts per single adult-year"),
                              ("k12", "attempts_per_single_year", "K12: courting attempts per single adult-year")):
            d = paired(rows, a, key, seeds)
            p, (e, lo, hi) = wil(d), boot(d)
            t = p < 0.05 and e > 0
            manip[(a, key)] = t
            L.append(f"- Manipulation check, {label} rise against C: mean difference {e:+.3f} [{lo:+.3f}, {hi:+.3f}], "
                     f"p = {p:.3g}: **{'yes' if t else 'NO'}**")
            ok &= t
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        dc = {s: died(rows["c"][s]) for s in seeds}
        res = {}
        for a in CANDS:
            da = {s: died(rows[a][s]) for s in seeds}
            saved = sum(1 for s in seeds if dc[s] and not da[s])
            lost = sum(1 for s in seeds if da[s] and not dc[s])
            p = binomtest(saved, saved + lost).pvalue if saved + lost else 1.0
            res[a] = [sum(da.values()), saved, lost, p, *boot([dc[s] - da[s] for s in seeds])]
        adj = dict(zip(CANDS, holm([res[a][3] for a in CANDS])))
        reading = {}
        L += ["", "## Primary: survival (each arm against C, paired by seed)", "",
              f"C died out in **{sum(dc.values())} of {len(seeds)}**.", "",
              "| arm | died out | saved / lost | p | Holm p | effect (C − arm) | 95% interval | reading |",
              "|---|---|---|---|---|---|---|---|"]
        for a in CANDS:
            n, sv, ls, p, e, lo, hi = res[a]
            if adj[a] < 0.05:
                rd = ("changes survival (" + ("fewer" if e > 0 else "more") + " die out, "
                      + ("beyond" if abs(e) > YARD else "within") + " the yardstick)")
            elif -YARD < lo and hi < YARD:
                rd = "no meaningful effect"
            else:
                rd = "unresolved"
            reading[a] = rd
            L.append(f"| {a.upper()} | {n} | {sv} / {ls} | {p:.3g} | {adj[a]:.3g} | {e:+.3f} | [{lo:+.3f}, {hi:+.3f}] | "
                     f"**{rd}** |")
        L += ["", "## Mechanism outcomes (paired differences against C; mean [95% interval])", "",
              "| arm | births per woman-year | share of fertile woman-weeks single | couples formed |", "|---|---|---|---|"]
        mech = {}
        for a in CANDS:
            cells = []
            for key in ("births_per_woman_year", "single_share", "pairs"):
                e, lo, hi = boot(paired(rows, a, key, seeds))
                mech[(a, key)] = e
                cells.append(f"{e:+.4f} [{lo:+.4f}, {hi:+.4f}]")
            L.append(f"| {a.upper()} | " + " | ".join(cells) + " |")
        cm = {k: statistics.fmean(rows["c"][s]["m"][k] for s in seeds) for k in ("births_per_woman_year", "single_share", "pairs")}
        L.append(f"| C (mean level) | {cm['births_per_woman_year']:.4f} | {cm['single_share']:.4f} | {cm['pairs']:.1f} |")
        L += ["", "## Harm outcomes (C's level; each arm's absolute and relative change, paired 95% interval, Wilcoxon p)", ""]
        harm = {}
        for key, label, serious in (("infant_deaths_per_birth", "infant deaths per birth", True),
                                    ("adult_starvation", "adult deaths by starvation (per world)", True),
                                    ("young_or_older_father_share", "births to a mother under 18 or a father 15+ years older", False)):
            cv = [rows["c"][s]["m"][key] for s in seeds if rows["c"][s]["m"][key] is not None]
            base = statistics.fmean(cv) if cv else 0.0
            L += [f"**{label}** (C: {base:.4f})" + (" — serious harm measure" if serious else ""), "",
                  "| arm | change | relative | 95% interval | p |", "|---|---|---|---|---|"]
            for a in CANDS:
                d = paired(rows, a, key, seeds)
                e, lo, hi = boot(d)
                p = wil(d)
                harm[(a, key)] = serious and p < 0.05 and e > 0
                L.append(f"| {a.upper()} | {e:+.4f} | {(e / base if base else 0):+.1%} | [{lo:+.4f}, {hi:+.4f}] | {p:.3g} |")
            L.append("")
        L.append("**Couples that split:** 0 in every arm by construction (couples part only at death; operational note).")
        L += ["", "## Mechanism, described (pooled over worlds)", "",
              "Acceptance share of courting attempts on someone not yet a partner, by the courted one's familiarity with "
              "the suitor:", "", "| arm | " + " | ".join(f"fam < {e:g}" for e in FAM_BINS) + " |",
              "|---" * (len(FAM_BINS) + 1) + "|"]
        for a in ARMS:
            t = Counter()
            for s in seeds:
                t.update(rows[a][s]["courting"])
            L.append(f"| {a.upper()} | " + " | ".join(
                f"{t[f'acc_fam{i}']}/{t[f'att_fam{i}']}" for i in range(len(FAM_BINS))) + " |")
        L += ["", "Courting attempts per single adult-year, by the suitor's loneliness:", "",
              "| arm | " + " | ".join(f"lonely < {e:g}" for e in LONELY_BINS) + " | suitor knows them well (fam ≥ 0.35) |",
              "|---" * (len(LONELY_BINS) + 2) + "|"]
        for a in ARMS:
            t = Counter()
            for s in seeds:
                t.update(rows[a][s]["courting"])
            cells = [f"{t[f'att_lonely{i}'] / (t[f'single_weeks_lonely{i}'] / WPY):.2f}" if t[f"single_weeks_lonely{i}"]
                     else "–" for i in range(len(LONELY_BINS))]
            known = f"{t['att_known'] / t['attempts']:.1%}" if t["attempts"] else "–"
            L.append(f"| {a.upper()} | " + " | ".join(cells) + f" | {known} |")
        L.append("")
        L.append("Whether the change acts mostly on people who would otherwise rarely pair is not measurable from this "
                 "log (it records attempts, not who would have paired without the change); not described.")
        d = [(died(rows["k12"][s]) - died(rows["k2"][s])) - (died(rows["k1"][s]) - dc[s]) for s in seeds]
        e, lo, hi = boot(d)
        L += ["", f"**Interaction on dying out (K12 − K2) − (K1 − C):** {e:+.3f} [{lo:+.3f}, {hi:+.3f}] (described).", "",
              "## The adoption rule (frozen)", ""]
        qual = {}
        for a in ("k1", "k2"):
            m_ok = all(v for (arm, _), v in manip.items() if arm == a)
            surv_ok = reading[a] == "no meaningful effect" or reading[a].startswith("changes survival (fewer")
            harm_ok = not any(harm[(a, k)] for k in ("infant_deaths_per_birth", "adult_starvation"))
            qual[a] = m_ok and surv_ok and harm_ok
            why = [] if qual[a] else (["manipulation check failed"] * (not m_ok)
                                      + [f"survival: {reading[a]}"] * (not surv_ok)
                                      + ["a serious harm rose"] * (not harm_ok))
            L.append(f"- **{a.upper()}: {'may be proposed for adoption (the creator decides on its evidence)' if qual[a] else 'not adopted (' + '; '.join(why) + ')'}**.")
        if qual["k1"] and qual["k2"]:
            k12_ok = (reading["k12"] == "no meaningful effect" or reading["k12"].startswith("changes survival (fewer")) \
                and not any(harm[("k12", k)] for k in ("infant_deaths_per_birth", "adult_starvation"))
            L.append(f"- **K12: {'may be proposed (both qualify alone)' if k12_ok else 'not proposed'}**.")
        else:
            L.append("- **K12: not proposed** (K1 and K2 do not both qualify alone).")
        L.append("- Births and couples are the mechanism's evidence, shown above; no p-value on them is a condition.")
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
