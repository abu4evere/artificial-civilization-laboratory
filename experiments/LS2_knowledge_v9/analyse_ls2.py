"""LS2 analysis in the frozen order (questions.md, `LS2-frozen`). Written before any data.

  python experiments/LS2_where_knowledge_goes/analyse_ls1.py            # writes results.md
  python experiments/LS2_where_knowledge_goes/analyse_ls1.py --smoke    # throwaway smoke outputs; writes nothing

Intervals: world bootstrap (whole worlds resampled), 10,000 replicates, percentile 95%, generator seed 20261026.
Every bin is read over the worlds alive at its start; extinct worlds are ended, never counted as holding zero.
LP is primary; D80 is secondary and described.
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_ls2 import BIN_EDGES, D80_SEEDS, DECADE, LP_SEEDS, OUT, SMOKE_SEEDS, WPY, YEARS  # noqa: E402

B = 10_000
RNG_SEED = 20261026
NB = len(BIN_EDGES) - 1
BIN_NAMES = [f"{BIN_EDGES[i]}-{BIN_EDGES[i + 1]}" for i in range(NB)]
IN_ROUTES = ("invented", "rediscovered", "taught", "copied", "read", "other")
OUT_CH = ("pushout", "useless", "death")
ADULT = ("16-29", "30-49", "50+")
AFTER100 = [i for i in range(NB) if BIN_EDGES[i] >= 100]


def load(out, jobs):
    rows, missing = {}, []
    for arm, s in jobs:
        f = out / f"{arm}_seed_{s}.json"
        if f.exists():
            rows.setdefault(arm, []).append(json.loads(f.read_text(encoding="utf-8")))
        else:
            missing.append(f"{arm} {s}")
    return rows, missing


def idx(n):
    return np.random.default_rng(RNG_SEED).integers(0, n, size=(B, n))


def ci(x):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if not len(x):
        return "-"
    lo, hi = np.percentile(x, [2.5, 97.5])
    return f"[{lo:.3g}, {hi:.3g}]"


def ratio_boot(num, den, ix):
    """Ratio of sums over worlds, and its bootstrap replicates."""
    num, den = np.asarray(num, float), np.asarray(den, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        est = num.sum() / den.sum() if den.sum() else float("nan")
        reps = num[ix].sum(1) / den[ix].sum(1)
    return est, reps


def alive_at(r, years):
    return r["final_tick"] >= years * WPY


def binv(r, i, key):
    return r["bins"].get(str(i), {}).get(key, 0.0)


def bins_alive(rs, i):
    """Worlds alive at the bin's start that lived into it (a world ending exactly at the start has no weeks in it)."""
    return [r for r in rs if r["final_tick"] > BIN_EDGES[i] * WPY]


# --- the sections ------------------------------------------------------------------------------------------------

def section_check(L, rs):
    """M1's two co-primary measures, by M1's rules, as a check against M1 (described on v9)."""
    alive = [r for r in rs if alive_at(r, YEARS)]
    L += ["## Check against M1 (M1's rules, worlds alive at year 1,000)", ""]
    if not alive:
        L.append("No world alive at year 1,000.")
        return

    def a4(r, decs):
        acts = sum(r["decades"].get(str(d), {}).get("forage_acts", 0) for d in decs)
        owed = sum(r["decades"].get(str(d), {}).get("owed", 0) for d in decs)
        return owed / acts if acts else None

    def bret(r, lo, hi):
        ks = [k for k in r["kinds"] if k[10] > 1.0 and lo * WPY <= k[0] < hi * WPY and k[6] is not None
              and k[6] + 25 * WPY <= r["final_tick"] and k[7] is not None]
        return (sum(1 for k in ks if k[7]) / len(ks)) if ks else None, len(ks)
    for name, fe, fl in (("A4 food owed to tools per adult forage act", lambda r: a4(r, (2, 3, 4)),
                          lambda r: a4(r, range(95, 100))),
                         ("B-retained", lambda r: bret(r, 0, 50)[0], lambda r: bret(r, 900, 950)[0])):
        pairs = [(fe(r), fl(r)) for r in alive]
        pairs = [(e, l_) for e, l_ in pairs if e is not None and l_ is not None and e > 0]
        if not pairs:
            L.append(f"- {name}: no worlds with both eras.")
            continue
        e = np.array([p[0] for p in pairs])
        l_ = np.array([p[1] for p in pairs])
        ix = idx(len(pairs))
        with np.errstate(divide="ignore", invalid="ignore"):
            reps = l_[ix].mean(1) / e[ix].mean(1)
        L.append(f"- {name}: early {e.mean():.4g}, late {l_.mean():.4g}, late / early {l_.mean() / e.mean():.3f} "
                 f"{ci(reps)} ({len(pairs)} worlds). M1 (v6): A4 0.054 [0.046, 0.063]; B-retained late 0.")
    L.append("")


def section_population(L, rs, n):
    L += ["## Survivorship and population (worlds alive at each bin's start)", "",
          "| bin (years) | worlds alive | mean population | mean adults | people per 100 land tiles |",
          "|---|---|---|---|---|"]
    for i in range(NB):
        al = bins_alive(rs, i)
        decs = range(BIN_EDGES[i] // 10, max(BIN_EDGES[i] // 10 + 1, BIN_EDGES[i + 1] // 10))
        pops = [r["decades"].get(str(d), {}).get("pop") for r in al for d in decs]
        pops = [p for p in pops if p is not None]
        ads = [r["decades"].get(str(d), {}).get("adults") for r in al for d in decs]
        ads = [a for a in ads if a is not None]
        land = np.mean([r["land"] for r in al]) if al else float("nan")
        thin = " (thin)" if len(al) < 10 else ""
        L.append(f"| {BIN_NAMES[i]} | {len(al)} of {n}{thin} | {np.mean(pops) if pops else float('nan'):.1f} | "
                 f"{np.mean(ads) if ads else float('nan'):.1f} | {100 * np.mean(pops) / land if pops else float('nan'):.2f} |")
    dead = sorted(round(r["final_tick"] / WPY) for r in rs if not alive_at(r, YEARS))
    L += ["", f"Worlds that ended before year 1,000 (year): {dead or 'none'}.", ""]


def section_q1(L, rs):
    L += ["## Q1 — The ledger: copy loss and kind extinction", "",
          "Inflow by route and outflow by channel, per 1,000 person-years (worlds alive at each bin's start).", "",
          "| bin | " + " | ".join(f"in: {r_}" for r_ in IN_ROUTES) + " | " +
          " | ".join(f"out: {c}" for c in OUT_CH) + " | net | losses per held recipe-year |",
          "|---|" + "---|" * (len(IN_ROUTES) + len(OUT_CH) + 2)]
    nets = []
    for i in range(NB):
        al = bins_alive(rs, i)
        if len(al) < 10:
            L.append(f"| {BIN_NAMES[i]} | (fewer than 10 worlds: no reading) |" + " |" * (len(IN_ROUTES) + len(OUT_CH) + 1))
            nets.append(None)
            continue
        py = sum(binv(r, i, "pw") for r in al) / WPY
        held = sum(binv(r, i, "held_recipe_weeks") for r in al) / WPY
        if not py:                                     # a world ending exactly at a bin's start has no weeks in it
            nets.append(None)
            continue
        ins = [sum(binv(r, i, "in_" + x) for r in al) for x in IN_ROUTES]
        outs = [sum(binv(r, i, "out_" + x) for r in al) for x in OUT_CH]
        net = (sum(ins) - sum(outs)) / py * 1000 if py else float("nan")
        nets.append(net)
        L.append(f"| {BIN_NAMES[i]} | " + " | ".join(f"{1000 * v / py:.1f}" for v in ins) + " | " +
                 " | ".join(f"{1000 * v / py:.1f}" for v in outs) + f" | {net:+.1f} | "
                 f"{sum(outs) / held if held else float('nan'):.3f} |")
    first_neg = None
    for i, v in enumerate(nets):
        if v is not None and v < 0 and all(x is None or x < 0 for x in nets[i:]):
            first_neg = BIN_NAMES[i]
            break
    L += ["", f"- **Net flow first turns negative and stays negative:** {first_neg or 'never'}."]
    for kind, prefix, title in (("copy loss", "out_", "dominant copy-loss channel"),
                                ("kind extinction", "ext_", "dominant kind-extinction channel")):
        al = [r for r in rs if alive_at(r, 100)]
        per = np.array([[sum(binv(r, i, prefix + c) for i in AFTER100) for c in OUT_CH] for r in al], float)
        if per.size == 0 or per.sum() == 0:
            L.append(f"- **The {title} after year 100:** no events.")
            continue
        ix = idx(len(al))
        tot = per.sum()
        shares = per.sum(0) / tot
        reps = per[ix].sum(1)
        with np.errstate(divide="ignore", invalid="ignore"):
            rshare = reps / reps.sum(1, keepdims=True)
        best = int(np.argmax(shares))
        L.append(f"- **The {title} after year 100:** **{OUT_CH[best]}** ("
                 + "; ".join(f"{c} {shares[k]:.3f} {ci(rshare[:, k])}" for k, c in enumerate(OUT_CH))
                 + f"; {int(tot)} events in {len(al)} worlds).")
    L.append("")


def section_q2(L, rs):
    L += ["## Q2 — Origin, transmission, persistence (useful kinds: a factor > 1)", "",
          "| origin | era first made | useful kinds | ever held by 2+ people | still held 25 years after the maker's death (eligible) | "
          "held 2+ generations after the maker |", "|---|---|---|---|---|---|"]
    eras = (("years 0-100", 0, 100), ("years 100-1,000", 100, 1000))
    for org, flag in (("founder", 1), ("world-born", 0)):
        for en, lo, hi in eras:
            ks = [k for r in rs for k in r["kinds"] if k[10] > 1.0 and k[1] == flag and lo * WPY <= k[0] < hi * WPY]
            elig = [k for k in ks if k[7] is not None]
            if not ks:
                L.append(f"| {org} | {en} | 0 | - | - | - |")
                continue
            L.append(f"| {org} | {en} | {len(ks)} | {np.mean([k[3] >= 2 for k in ks]):.3f} | "
                     f"{(np.mean([bool(k[7]) for k in elig]) if elig else float('nan')):.3f} (of {len(elig)}) | "
                     f"{np.mean([k[4] - k[2] >= 2 for k in ks]):.3f} |")
    al = [r for r in rs]
    f = np.array([sum(binv(r, i, "useful_held_weeks_founder") for i in range(5)) for r in al], float)
    wb = np.array([sum(binv(r, i, "useful_held_weeks_worldborn") for i in range(5)) for r in al], float)
    est, reps = ratio_boot(f, f + wb, idx(len(al)))
    L += ["", f"- Founder share of useful know-how held in years 0-100 (person-recipe-weeks): {est:.3f} {ci(reps)} "
          "(descriptive).", ""]


def section_q3(L, rs):
    L += ["## Q3 — The making funnel", "",
          "Adults (16+). Feasible per adult person-week; weighed given feasible; chosen given weighed; chosen per "
          "adult person-week. Teens (12-15) after the bar.", "",
          "| bin | worlds | feasible | weighed / feasible | chosen / weighed | chosen per person-week | teens: chosen per person-week |",
          "|---|---|---|---|---|---|---|"]

    def counts(r, bins_):
        pw = sum(binv(r, i, f"pw_{a}") for i in bins_ for a in ADULT)
        fe = sum(binv(r, i, f"feasible_{a}") for i in bins_ for a in ADULT)
        we = sum(binv(r, i, f"weighed_{a}") for i in bins_ for a in ADULT)
        ch = sum(binv(r, i, f"chosen_{a}") for i in bins_ for a in ADULT)
        return pw, fe, we, ch
    for i in range(NB):
        al = bins_alive(rs, i)
        if len(al) < 10:
            continue
        pw, fe, we, ch = map(sum, zip(*[counts(r, [i]) for r in al]))
        tpw = sum(binv(r, i, "pw_12-15") for r in al)
        tch = sum(binv(r, i, "chosen_12-15") for r in al)
        L.append(f"| {BIN_NAMES[i]} | {len(al)} | {fe / pw if pw else 0:.3f} | {we / fe if fe else 0:.3f} | "
                 f"{ch / we if we else 0:.4f} | {ch / pw if pw else 0:.5f} | {tch / tpw if tpw else 0:.5f} |")
    # the frozen decomposition: years 0-10 (bins 0 and 1) to years 100-200
    late_bin = BIN_NAMES.index("100-200")
    al = [r for r in rs if alive_at(r, 100)]
    E = np.array([counts(r, [0, 1]) for r in al], float)
    Lt = np.array([counts(r, [late_bin]) for r in al], float)
    ix = idx(len(al))

    def terms(e, l_):
        pw_e, fe_e, we_e, ch_e = e
        pw_l, fe_l, we_l, ch_l = l_
        with np.errstate(divide="ignore", invalid="ignore"):
            t1 = np.log((fe_l / pw_l) / (fe_e / pw_e))
            t2 = np.log((we_l / fe_l) / (we_e / fe_e))
            t3 = np.log((ch_l / we_l) / (ch_e / we_e))
        return t1, t2, t3
    est = terms(E.sum(0), Lt.sum(0))
    reps = np.array(terms(E[ix].sum(1).T, Lt[ix].sum(1).T))
    names = ("feasible", "weighed given feasible", "chosen given weighed")
    L += ["", "**The decline decomposition (frozen): years 0-10 to years 100-200,** Δ ln(chosen per person-week) = "
          "Δ ln(feasible) + Δ ln(weighed | feasible) + Δ ln(chosen | weighed), pooled counts.", ""]
    total = sum(est)
    if not all(np.isfinite(est)):
        zero = [names[k] for k in range(3) if not np.isfinite(est[k])]
        L.append(f"- A term fell to zero: **{', '.join(zero)}** (marked \"fell to zero\").")
    else:
        with np.errstate(divide="ignore", invalid="ignore"):
            shares = [e / total for e in est]
            rshares = reps / reps.sum(0, keepdims=True)
        for k in range(3):
            L.append(f"- {names[k]}: Δ ln {est[k]:+.3f} {ci(reps[k])}; share of the decline {shares[k]:.2f} "
                     f"{ci(rshares[k])}")
        L.append(f"- Total Δ ln(chosen per person-week): {total:+.3f}. **The gate carrying the largest share: "
                 f"{names[int(np.argmax(shares))]}.**")
    # what beats making
    beat = Counter()
    for r in al:
        for i in AFTER100:
            for k_, v in r["bins"].get(str(i), {}).items():
                if k_.startswith("beaten_by_"):
                    beat[k_[10:]] += v
    tot = sum(beat.values())
    if tot:
        L.append("- When making was weighed and not chosen (after year 100), what won: " +
                 ", ".join(f"{a} {v / tot:.2f}" for a, v in beat.most_common(6)) + ".")
    L.append("")


def section_q4(L, rs):
    L += ["## Q4 — The fall in A4, exactly (A4 = s × g × k)", ""]
    al = [r for r in rs if alive_at(r, YEARS)]
    if not al:
        L += ["No world alive at year 1,000.", ""]
        return

    def parts(r, decs):
        g = lambda k: sum(r["decades"].get(str(d), {}).get(k, 0.0) for d in decs)   # noqa: E731
        return np.array([g("forage_acts"), g("tool_acts"), g("tool_got"), g("owed")])
    E = np.array([parts(r, (2, 3, 4)) for r in al])
    Lt = np.array([parts(r, range(95, 100)) for r in al])
    ix = idx(len(al))

    def split(e, l_):
        with np.errstate(divide="ignore", invalid="ignore"):
            s_ = np.log((l_[..., 1] / l_[..., 0]) / (e[..., 1] / e[..., 0]))
            g_ = np.log((l_[..., 2] / l_[..., 1]) / (e[..., 2] / e[..., 1]))
            k_ = np.log((l_[..., 3] / l_[..., 2]) / (e[..., 3] / e[..., 2]))
        return s_, g_, k_
    est = split(E.sum(0), Lt.sum(0))
    reps = split(E[ix].sum(1), Lt[ix].sum(1))
    tot = sum(est)
    se, sl = E.sum(0), Lt.sum(0)
    L += [f"Worlds alive at year 1,000: {len(al)}. Decades 2-4: s {se[1] / se[0]:.3f}, g {se[2] / se[1]:.2f}, "
          f"k {se[3] / se[2]:.3f}; decades 95-99: s {sl[1] / sl[0] if sl[0] else float('nan'):.3f}, "
          f"g {sl[2] / sl[1] if sl[1] else float('nan'):.2f}, k {sl[3] / sl[2] if sl[2] else float('nan'):.3f}.", ""]
    for name, e_, r_ in zip(("s, the share of forage acts with a tool", "g, food per tool act",
                             "k, the tool's share of that food"), est, reps):
        share = e_ / tot if np.isfinite(tot) and tot else float("nan")
        L.append(f"- {name}: Δ ln {e_:+.3f} {ci(r_)}; share of the fall {share:.2f}")
    L.append(f"- Total Δ ln A4: {tot:+.3f}.")
    o = Counter()
    for r in al:
        for d in (2, 3, 4):
            for k_ in ("tool_origin_own", "tool_origin_other", "tool_origin_unknown", "tool_made_first_20y", "tool_acts"):
                o[k_] += r["decades"].get(str(d), {}).get(k_, 0.0)
    if o["tool_acts"]:
        L.append(f"- Tools used in decades 2-4: made by the holder {o['tool_origin_own'] / o['tool_acts']:.3f}, made by "
                 f"someone else {o['tool_origin_other'] / o['tool_acts']:.3f}, unknown {o['tool_origin_unknown'] / o['tool_acts']:.3f}; "
                 f"made in the first 20 years {o['tool_made_first_20y'] / o['tool_acts']:.3f}.")
    L += ["", "| bin | forage tool lost: replaced within a year | not replaced |", "|---|---|---|"]
    for i in range(NB):
        al_ = bins_alive(rs, i)
        if len(al_) < 10:
            continue
        rp = sum(binv(r, i, "tool_replaced") for r in al_)
        nr = sum(binv(r, i, "tool_not_replaced") for r in al_)
        L.append(f"| {BIN_NAMES[i]} | {rp / (rp + nr) if rp + nr else float('nan'):.3f} | {int(nr)} of {int(rp + nr)} |")
    L.append("")


def section_q5(L, rs):
    L += ["## Q5 — Does each generation replace what it inherits?", "",
          "World-born people, by birth cohort (50-year bands). Inheritance: of the useful recipes their carers held "
          "while they were 0-16, the share they ever acquired by 30.", "",
          "| born (years) | people | inheritance rate [95%] | inherited by: taught / own making / other | useful acquired by 30 (mean) | "
          "acquired by 16: taught / copied / own (mean) | used: acquired from others and later made | onward: passed to someone younger | "
          "survival: outlived them by 25 years |",
          "|---|---|---|---|---|---|---|---|---|"]
    for lo in range(0, 1000, 50):
        hi = lo + 50
        per_world = []
        for r in rs:
            ppl = [p for p in r["people"] if not p[3] and lo * WPY <= p[1] < hi * WPY and p[12] is not None]
            per_world.append(ppl)
        n = sum(len(x) for x in per_world)
        if n == 0:
            continue
        num = np.array([sum(p[12][0] for p in x) for x in per_world], float)
        den = np.array([sum(p[12][1] for p in x) for x in per_world], float)
        est, reps = ratio_boot(num, den, idx(len(per_world)))
        allp = [p for x in per_world for p in x]
        ir = Counter()
        for p in allp:
            for k_, v in (p[12][2] or {}).items():
                ir[k_] += v
        itot = sum(ir.values()) or 1
        inh_by = (f"{ir['taught'] / itot:.2f} / {(ir['invented'] + ir['rediscovered']) / itot:.2f} / "
                  f"{(itot - ir['taught'] - ir['invented'] - ir['rediscovered']) / itot:.2f}")
        acq30u = np.mean([p[15] or 0 for p in allp])
        a16 = Counter()
        for p in allp:
            for k_, v in (p[13] or {}).items():
                a16[k_] += v
        own = a16["invented"] + a16["rediscovered"]
        used = [p[16] for p in allp if p[16]]
        onw = [p[17] for p in allp if p[17]]
        sv = [p[18] for p in allp if p[18]]
        frac = lambda xs: (sum(a for a, b in xs) / sum(b for a, b in xs)) if xs and sum(b for a, b in xs) else float("nan")  # noqa: E731
        L.append(f"| {lo}-{hi} | {n} | {est:.3f} {ci(reps)} | {inh_by} | {acq30u:.2f} | {a16['taught'] / n:.2f} / {a16['copied'] / n:.2f} / "
                 f"{own / n:.2f} | {frac(used):.3f} | {frac(onw):.3f} | {frac(sv):.3f} |")
    ks = [k for r in rs for k in r["kinds"] if k[1] == 0 and k[11] == 1 and k[10] > 1.0]
    if ks:
        L.append(f"\n- New knowledge: useful kinds invented by world-born people: {len(ks)}; held by someone of a later "
                 f"generation: {sum(1 for k in ks if k[4] > k[2])} ({np.mean([k[4] > k[2] for k in ks]):.3f}).")
    L.append("")


def section_described(L, rs):
    L += ["## Described: teaching, skill and habits", "",
          "| bin | lessons offered per person-year | taken | taken from parents / carers / kin / others | taken lessons later made | later passed on |",
          "|---|---|---|---|---|---|"]
    for i in range(NB):
        al = bins_alive(rs, i)
        if len(al) < 10:
            continue
        py = sum(binv(r, i, "pw") for r in al) / WPY
        off = sum(binv(r, i, "lesson_offered") for r in al)
        tak = sum(binv(r, i, "lesson_taken") for r in al)
        rel = [sum(binv(r, i, f"lesson_taken_{x}") for r in al) for x in ("parent", "carer", "kin", "other")]
        mk = ps = tk = 0
        for r in al:
            for x in ("parent", "carer", "kin", "other"):
                c = r["lessons"].get(f"{i}|{x}", {})
                tk += c.get("taken", 0)
                mk += c.get("made", 0)
                ps += c.get("passed", 0)
        L.append(f"| {BIN_NAMES[i]} | {off / py if py else 0:.2f} | {tak / off if off else 0:.3f} | "
                 + " / ".join(f"{int(v)}" for v in rel) + f" | {mk / tk if tk else 0:.3f} | {ps / tk if tk else 0:.3f} |")
    L += ["", "| born (years) | crafting skill at 16 | at 30 | practice weeks per person | making habit at 16 | carer's | talk partners' |",
          "|---|---|---|---|---|---|---|"]
    for lo in (0, 50, 100, 200, 400, 600, 800, 900):
        hi = {0: 50, 50: 100, 100: 200, 200: 400, 400: 600, 600: 800, 800: 900, 900: 1000}[lo]
        ppl = [p for r in rs for p in r["people"] if not p[3] and lo * WPY <= p[1] < hi * WPY]
        if not ppl:
            continue
        m = lambda j: np.mean([p[j] for p in ppl if p[j] is not None]) if any(p[j] is not None for p in ppl) else float("nan")  # noqa: E731
        L.append(f"| {lo}-{hi} | {m(5):.3f} | {m(6):.3f} | {m(11):.1f} | {m(7):.4f} | {m(9):.4f} | {m(10):.4f} |")
    L.append("")


def main(smoke=False):
    jobs = [("lp", s) for s in (SMOKE_SEEDS if smoke else LP_SEEDS)] + ([] if smoke else [("d80", s) for s in D80_SEEDS])
    out = HERE / "output_smoke" if smoke else OUT
    rows, missing = load(out, jobs)
    L = [f"# LS2 — where does knowledge go? Results{' (SMOKE TEST, throwaway seeds)' if smoke else ''}", "",
         "Frozen as `LS2-frozen`. run_ls2.py (LS1's observer), analyse_ls2.py (LS1's analysis; written before data).", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks: **{'yes' if zt else 'NO'}**")
    L.append(f"- All worlds present ({len(jobs)}): **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    allr = [r for rs in rows.values() for r in rs]
    fps = {h for r in allr for h in (r["code_hash"], r["code_hash_after"])}
    L.append(f"- One fingerprint (`code_v9`): **{'yes' if len(fps) == 1 else 'NO'}**")
    mism = Counter()
    for r in allr:
        mism.update(r["mismatch"])
    L.append(f"- Ledger balances, kind counts and holdings match in every world: **{'yes' if not mism else 'NO ' + str(dict(mism))}**")
    ok = zt and not missing and len(fps) == 1 and not mism
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**", ""]
    if not ok and not smoke:
        return finish(L, smoke)
    for arm, title in (("lp", "LP (primary)"), ("d80", "D80 (secondary, described)")):
        rs = rows.get(arm, [])
        if not rs:
            continue
        L += [f"# {title}: {len(rs)} worlds", ""]
        if arm == "lp":
            section_check(L, rs)
        section_population(L, rs, len(rs))
        section_q1(L, rs)
        section_q2(L, rs)
        section_q3(L, rs)
        section_q4(L, rs)
        section_q5(L, rs)
        section_described(L, rs)
    return finish(L, smoke)


def finish(L, smoke):
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
