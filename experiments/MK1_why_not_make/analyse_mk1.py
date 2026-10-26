"""MK1 analysis, written before any data (questions.md with draft revision 1, frozen as `MK1-frozen`; operational
note 1). Reads output/*.json, writes results.md.

  python experiments/MK1_why_not_make/analyse_mk1.py            # writes results.md
  python experiments/MK1_why_not_make/analyse_mk1.py --smoke    # throwaway smoke outputs; writes nothing
"""
from __future__ import annotations

import glob
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_mk1 import BIN_EDGES, HORIZONS, SEEDS, T, WPY  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261027)
WORTH_WEIGHT = 2.0
EARLY, LATE = (0, 1), (5,)                    # years 0-10 and 100-200 (LS1's decomposition periods)
BINS = [f"{BIN_EDGES[i]}-{BIN_EDGES[i + 1]}" for i in range(len(BIN_EDGES) - 1)]
SKILL = ["<0.1", "0.1-0.2", "0.2-0.35", "0.35-0.5", "0.5+"]


def load():
    rs = [json.load(open(f)) for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json")))]
    return rs


def parse(key):
    b, age, hb, tool, fb, sb = key.split("|")
    return int(b), age, int(hb), int(tool), int(fb), int(sb)


def idx(n):
    return RNG.integers(0, n, size=(REPS, n))


def ci(reps):
    reps = np.asarray(reps, float)
    reps = reps[np.isfinite(reps)]
    if len(reps) == 0:
        return "[-]"
    lo, hi = np.percentile(reps, [2.5, 97.5])
    return f"[{lo:.3g}, {hi:.3g}]"


def world_sums(r, select, fields):
    """Per world: sums of fields over cells passing select(parsed key)."""
    out = Counter()
    for k, c in r["cells"].items():
        if select(parse(k)):
            for f in fields:
                out[f] += c.get(f, 0.0)
    return out


def alive_at(r, year):
    return r["final_tick"] > year * WPY


FIELDS = ("pw", "feasible", "offered", "chosen", "no_offer_low", "no_offer_held", "no_offer_lowheld", "no_offer_tired",
          "sum_p", "sum_logit", "sum_uw", "sum_v", "sum_D", "sum_H", "sum_hab", "sum_th", "sum_uo", "top_make",
          "forage_acts", "forage_got")


# --- Q3: matched early/late decomposition -----------------------------------------------------------------------

def match_key(p):
    """Matched state: hunger band, tool held, food on the tile (skill is an explanation, not matched)."""
    return (p[2], p[3], p[4])


def cell_table(worlds, bins):
    """Per world, per matched state: summed fields (adults, offered weeks)."""
    tabs = []
    for r in worlds:
        t = defaultdict(Counter)
        for k, c in r["cells"].items():
            p = parse(k)
            if p[0] in bins and p[1] == "adult":
                for f in FIELDS:
                    t[match_key(p)][f] += c.get(f, 0.0)
        tabs.append(t)
    return tabs


def shapley3(a0, b0, c0, a1, b1, c1):
    """Exact Shapley split of the change in a*b*c into the three factors."""
    def f(a, b, c):
        return a * b * c
    pa = ((f(a1, b0, c0) - f(a0, b0, c0)) / 3 + (f(a1, b1, c0) - f(a0, b1, c0)) / 6
          + (f(a1, b0, c1) - f(a0, b0, c1)) / 6 + (f(a1, b1, c1) - f(a0, b1, c1)) / 3)
    pb = ((f(a0, b1, c0) - f(a0, b0, c0)) / 3 + (f(a1, b1, c0) - f(a1, b0, c0)) / 6
          + (f(a0, b1, c1) - f(a0, b0, c1)) / 6 + (f(a1, b1, c1) - f(a1, b0, c1)) / 3)
    pc = f(a1, b1, c1) - f(a0, b0, c0) - pa - pb
    return pa, pb, pc


def decompose(early_tabs, late_tabs):
    """Matched (standardised to the early offered weeks) change in mean log-odds, split exactly:
    Δ logit = (Δ worth term + Δ habit + Δ thought − Δ U_other) / T; Δ worth term = Shapley(v, D, H) + Δ covariance."""
    E, L = Counter(), Counter()
    Ec, Lc = defaultdict(Counter), defaultdict(Counter)
    for t in early_tabs:
        for s, c in t.items():
            Ec[s].update(c)
    for t in late_tabs:
        for s, c in t.items():
            Lc[s].update(c)
    states = [s for s in Ec if Ec[s]["offered"] > 0 and Lc[s]["offered"] > 0]
    wsum = sum(Ec[s]["offered"] for s in states)
    if wsum == 0:
        return None
    out = Counter()
    for s in states:
        wt = Ec[s]["offered"] / wsum
        e, l_ = Ec[s], Lc[s]
        m = {}
        for tag, c in (("e", e), ("l", l_)):
            n = c["offered"]
            m[tag] = {f: c[f] / n for f in ("sum_logit", "sum_uw", "sum_v", "sum_D", "sum_H", "sum_hab", "sum_th",
                                             "sum_uo", "sum_p")}
            m[tag]["rate"] = c["chosen"] / n
        d = {f: m["l"][f] - m["e"][f] for f in m["e"]}
        pv, pd, ph = shapley3(m["e"]["sum_v"], m["e"]["sum_D"], m["e"]["sum_H"],
                              m["l"]["sum_v"], m["l"]["sum_D"], m["l"]["sum_H"])
        pv, pd, ph = WORTH_WEIGHT * pv, WORTH_WEIGHT * pd, WORTH_WEIGHT * ph
        cov = d["sum_uw"] - (pv + pd + ph)
        out["logit"] += wt * d["sum_logit"]
        out["worth_v"] += wt * pv / T
        out["diligence"] += wt * pd / T
        out["hunger"] += wt * ph / T
        out["worth_cov"] += wt * cov / T
        out["habit"] += wt * d["sum_hab"] / T
        out["thought"] += wt * d["sum_th"] / T
        out["others"] += wt * (-d["sum_uo"]) / T
        out["p_e"] += wt * m["e"]["sum_p"]
        out["p_l"] += wt * m["l"]["sum_p"]
        out["rate_e"] += wt * m["e"]["rate"]
        out["rate_l"] += wt * m["l"]["rate"]
        out["v_e"] += wt * m["e"]["sum_v"]
        out["v_l"] += wt * m["l"]["sum_v"]
        out["uo_e"] += wt * m["e"]["sum_uo"]
        out["uo_l"] += wt * m["l"]["sum_uo"]
    out["states"] = len(states)
    out["residual"] = out["logit"] - sum(out[k] for k in ("worth_v", "diligence", "hunger", "worth_cov", "habit",
                                                          "thought", "others"))
    # raw (unmatched)
    re, rl = Counter(), Counter()
    for t in early_tabs:
        for c in t.values():
            re.update(c)
    for t in late_tabs:
        for c in t.values():
            rl.update(c)
    out["raw_rate_e"] = re["chosen"] / re["offered"] if re["offered"] else float("nan")
    out["raw_rate_l"] = rl["chosen"] / rl["offered"] if rl["offered"] else float("nan")
    out["raw_logit"] = (rl["sum_logit"] / rl["offered"] - re["sum_logit"] / re["offered"]) if re["offered"] and rl["offered"] else float("nan")
    return out


# --- sections -------------------------------------------------------------------------------------------------

def section_validity(L, rs):
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    zero_ok = "All: PASS" in zero
    seeds = sorted(r["seed"] for r in rs)
    all_present = seeds == sorted(SEEDS)
    fps = {r["code_hash"] for r in rs} | {r["code_hash_after"] for r in rs}
    mism = sum(sum(r["mismatch"].values()) for r in rs)
    L += ["## Validity", "",
          f"- Zero checks: **{'yes' if zero_ok else 'NO'}**",
          f"- All worlds present ({len(rs)} of {len(SEEDS)}): **{'yes' if all_present else 'NO'}**",
          f"- One fingerprint (`code_v7`): **{'yes' if len(fps) == 1 else 'NO'}**",
          f"- The replay matches the decision in every world (offer and worth term mismatches 0): "
          f"**{'yes' if mism == 0 else f'NO ({mism})'}**", ""]
    ok = zero_ok and all_present and len(fps) == 1 and mism == 0
    L += [f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    return ok


def section_population(L, rs):
    L += ["## Survivorship and population (worlds alive at each bin's start)", "",
          "| bin (years) | worlds alive | mean population | mean adults |", "|---|---|---|---|"]
    for i, name in enumerate(BINS):
        al = [r for r in rs if alive_at(r, BIN_EDGES[i])]
        weeks = (BIN_EDGES[i + 1] - BIN_EDGES[i]) * WPY
        pop = np.mean([r["pop"].get(f"{i}|pw", 0) / weeks for r in al]) if al else float("nan")
        ad = np.mean([r["pop"].get(f"{i}|adults", 0) / weeks for r in al]) if al else float("nan")
        L.append(f"| {name} | {len(al)} of {len(rs)} | {pop:.1f} | {ad:.1f} |")
    ended = sorted(round(r["final_tick"] / WPY) for r in rs if r["final_tick"] < BIN_EDGES[-1] * WPY)
    L += ["", f"Worlds that ended before year {BIN_EDGES[-1]} (year): {ended}.", ""]


def section_gate(L, rs):
    L += ["## The offer gate and Q1, the score gap (adults; by bin; worlds alive at each bin's start)", "",
          "Feasible per person-week; offered given feasible; why feasible but not offered (worth at most 0.05 / only "
          "things already held / both / too tired); chosen given offered; the softmax's own probability; and the mean "
          "parts of making's score when offered (worth term, habit, thought) against the others' soft maximum U_other.",
          "",
          "| bin | worlds | feasible | offered / feasible | not offered: low / held / both / tired | chosen / offered | "
          "softmax P | make scored highest | worth term | habit | thought | U_other | mean log-odds |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, name in enumerate(BINS):
        al = [r for r in rs if alive_at(r, BIN_EDGES[i])]
        s = Counter()
        for r in al:
            s.update(world_sums(r, lambda p: p[0] == i and p[1] == "adult", FIELDS))
        if not s["pw"]:
            continue
        nof = s["feasible"] - s["offered"]
        why = " / ".join(f"{s[k] / nof:.2f}" if nof else "-" for k in ("no_offer_low", "no_offer_held",
                                                                       "no_offer_lowheld", "no_offer_tired"))
        n = s["offered"] or float("nan")
        L.append(f"| {name} | {len(al)} | {s['feasible'] / s['pw']:.3f} | {s['offered'] / max(s['feasible'], 1):.3f} | "
                 f"{why} | {s['chosen'] / n:.4f} | {s['sum_p'] / n:.4f} | {s['top_make'] / n:.4f} | "
                 f"{s['sum_uw'] / n:.3f} | {s['sum_hab'] / n:.4f} | {s['sum_th'] / n:.3f} | {s['sum_uo'] / n:.3f} | "
                 f"{s['sum_logit'] / n:.2f} |")
    L += ["", "When making was offered and not chosen, what won (share):", ""]
    for i, name in enumerate(BINS):
        c = Counter()
        for r in rs:
            c.update(r["beaten"].get(str(i), {}))
        tot = sum(c.values())
        if tot:
            L.append(f"- {name}: " + ", ".join(f"{a} {n / tot:.2f}" for a, n in c.most_common(6)))
    L.append("")


def section_q2(L, rs):
    L += ["## Q2 — Skill and worth (described; skill and worth cause each other, so no cause is named)", "",
          "Adults, offered weeks, all bins. Standardised to all adults' offered weeks over bin × hunger × tool × food "
          "(direct standardisation over the states each skill band has; the share of the reference it covers is shown).", "",
          "| crafting skill | offered weeks | chosen / offered (standardised) | softmax P (std.) | v (std.) | "
          "worth term (std.) | reference weight covered |", "|---|---|---|---|---|---|---|"]
    st = defaultdict(lambda: defaultdict(Counter))       # skill band -> state -> sums
    for r in rs:
        for k, c in r["cells"].items():
            p = parse(k)
            if p[1] != "adult":
                continue
            s = (p[0], p[2], p[3], p[4])
            for f in ("offered", "chosen", "sum_p", "sum_v", "sum_uw"):
                st[p[5]][s][f] += c.get(f, 0.0)
    W = Counter()                                         # reference: all adults' offered weeks, by state
    for sb in range(len(SKILL)):
        for s_, c in st[sb].items():
            W[s_] += c["offered"]
    wtot = sum(W.values())
    for sb, name in enumerate(SKILL):
        n_all = sum(c["offered"] for c in st[sb].values())
        present = [s_ for s_, c in st[sb].items() if c["offered"] > 0]
        wsum = sum(W[s_] for s_ in present)
        if not wsum:
            L.append(f"| {name} | {n_all:.0f} | - | - | - | - | - |")
            continue
        vals = {f: sum(W[s_] / wsum * st[sb][s_][f] / st[sb][s_]["offered"] for s_ in present)
                for f in ("chosen", "sum_p", "sum_v", "sum_uw")}
        L.append(f"| {name} | {n_all:.0f} | {vals['chosen']:.4f} | {vals['sum_p']:.4f} | {vals['sum_v']:.3f} | "
                 f"{vals['sum_uw']:.3f} | {wsum / wtot:.2f} |")
    L.append("")
    # makes: the tool's quality and the worth learned after, by the maker's skill
    L += ["**Deliberate makings of forage tools (factor > 1), by the maker's skill at the time.** Worth: the maker's "
          "learned worth for that kind at the making, 13 and 52 weeks later (alive makers). 'Relative' = the worth "
          "minus the mean for the same kind at 52 weeks over all makers (so kinds are compared with themselves).", "",
          "| crafting skill | makings | forage factor (mean) | worth at making | at 13 weeks | at 52 weeks | "
          "relative at 52 weeks |", "|---|---|---|---|---|---|---|"]
    mk = [m for r in rs for m in r["makes"] if m[6] > 1.0]
    by_sig = defaultdict(list)
    for m in mk:
        if m[10] is not None:
            by_sig[m[5]].append(m[10])
    sig_mean = {s: np.mean(v) for s, v in by_sig.items()}
    for sb, name in enumerate(SKILL):
        g = [m for m in mk if (sum(m[4] >= e for e in (0.1, 0.2, 0.35, 0.5))) == sb]
        if not g:
            L.append(f"| {name} | 0 | - | - | - | - | - |")
            continue
        f = np.mean([m[6] for m in g])
        w0 = np.mean([m[8] for m in g])
        w13 = [m[9] for m in g if m[9] is not None]
        w52 = [m[10] for m in g if m[10] is not None]
        rel = [m[10] - sig_mean[m[5]] for m in g if m[10] is not None]
        L.append(f"| {name} | {len(g)} | {f:.3f} | {w0:.3f} | {np.mean(w13) if w13 else float('nan'):.3f} | "
                 f"{np.mean(w52) if w52 else float('nan'):.3f} | {np.mean(rel) if rel else float('nan'):+.3f} |")
    L.append("")


def section_q3(L, rs):
    L += ["## Q3 — Early (years 0-10) against late (years 100-200), matched", "",
          "Adults, offered weeks. Matched states: hunger band × forage tool held × food on the tile; late states "
          "weighted to the early distribution of offered weeks (states present in both). Exact split of the change in "
          "mean log-odds of choosing to make: Δ = (Δ worth term + Δ habit + Δ thought − Δ U_other) / T, the worth "
          "term split by Shapley into v, diligence and hunger, with the cell-level covariance left as its own term.",
          ""]
    al = [r for r in rs if alive_at(r, BIN_EDGES[LATE[0]])]
    for label, worlds in (("worlds alive at year 100", al), ("all worlds (late from those alive)", rs)):
        E = cell_table(worlds, EARLY)
        Lt = cell_table(worlds, LATE)
        d = decompose(E, Lt)
        if d is None:
            L.append(f"- {label}: no matched states.")
            continue
        n = len(worlds)
        reps = defaultdict(list)
        if label.startswith("worlds alive"):
            for row in idx(n):
                dd = decompose([E[k] for k in row], [Lt[k] for k in row])
                if dd is None:
                    continue
                for k_ in ("logit", "worth_v", "diligence", "hunger", "worth_cov", "habit", "thought", "others"):
                    reps[k_].append(dd[k_])
                reps["rate_ratio"].append(dd["rate_l"] / dd["rate_e"] if dd["rate_e"] else float("nan"))
        L += [f"**{label}** ({n} worlds, {d['states']:.0f} matched states):", "",
              f"- chosen given offered: raw {d['raw_rate_e']:.4f} → {d['raw_rate_l']:.4f}; matched "
              f"{d['rate_e']:.4f} → {d['rate_l']:.4f} (late / early {d['rate_l'] / d['rate_e']:.3f} "
              f"{ci(reps['rate_ratio']) if reps else ''}). Softmax P matched {d['p_e']:.4f} → {d['p_l']:.4f}.",
              f"- Δ ln(chosen given offered): raw {math.log(d['raw_rate_l'] / d['raw_rate_e']):.3f}; matched "
              f"{math.log(d['rate_l'] / d['rate_e']):.3f}. **Share of the fall that remains within matched states: "
              f"{math.log(d['rate_l'] / d['rate_e']) / math.log(d['raw_rate_l'] / d['raw_rate_e']):.2f}.**",
              f"- mean v {d['v_e']:.3f} → {d['v_l']:.3f}; U_other {d['uo_e']:.3f} → {d['uo_l']:.3f}.", "",
              "| part | Δ mean log-odds | share of the change |", "|---|---|---|"]
        tot = d["logit"]
        for k_, name in (("worth_v", "v, the learned worth"), ("diligence", "diligence"), ("hunger", "hunger"),
                         ("worth_cov", "worth term: covariance"), ("habit", "habit"), ("thought", "thought's pull"),
                         ("others", "the other options (− U_other)")):
            L.append(f"| {name} | {d[k_]:+.3f} {ci(reps[k_]) if reps else ''} | {d[k_] / tot:.2f} |")
        L += [f"| **total** | {tot:+.3f} {ci(reps['logit']) if reps else ''} | 1.00 |",
              f"", f"(Exactness check: total minus the parts = {d['residual']:.2e}.) Raw (unmatched) Δ mean "
              f"log-odds: {d['raw_logit']:+.3f}.", ""]
        largest = max(("worth_v", "diligence", "hunger", "worth_cov", "habit", "thought", "others"),
                      key=lambda k_: d[k_] * (1 if tot > 0 else -1))
        L += [f"**The part carrying the largest share of the change ({label}): {largest}.**", ""]


def section_q4(L, rs):
    L += ["## Q4 — Does making a forage tool pay? (described; an observational benefit-cost proxy, not a causal net "
          "return)", "",
          "Every forage tool (factor > 1) made deliberately, followed while its maker holds it. Benefit: the food owed "
          "to the tool (got × (1 − 1/f)) at the maker's forage acts, cumulative to each horizon; a tool that stops "
          "being followed (maker died, or no longer holds it) keeps what it had earned. Cost: one forage act's food "
          "forgone in the making week, estimated as the mean food per adult forage act in the maker's own world, bin "
          "and state (hunger × tool × food × skill).", ""]
    cellmean = {}
    for r in rs:
        for k, c in r["cells"].items():
            if c.get("forage_acts"):
                cellmean[(r["seed"], k)] = c["forage_got"] / c["forage_acts"]
    hdr = " | ".join(f"owed by {h} wk" for h in HORIZONS)
    L += [f"| bin made | tools | uses (mean) | {hdr} | lifetime owed | followed past 52 weeks | cost (one act) | "
          f"proxy at 52 weeks (owed − cost) |", "|---" * (7 + len(HORIZONS)) + "|"]
    for i, name in enumerate(BINS):
        tl = [(r["seed"], t) for r in rs for t in r["tools"] if parse(t[4])[0] == i]
        if not tl:
            continue
        owed_h = np.mean([t[7] for _, t in tl], axis=0)
        past52 = np.mean([(t[8] is None and r_end(rs, s) - t[1] > 52) or (t[8] is not None and t[8] - t[1] > 52)
                          for s, t in tl])
        cost = [cellmean.get((s, t[4])) for s, t in tl]
        cost = [x for x in cost if x is not None]
        cst = np.mean(cost) if cost else float("nan")
        L.append(f"| {name} | {len(tl)} | {np.mean([t[5] for _, t in tl]):.1f} | "
                 + " | ".join(f"{x:.1f}" for x in owed_h)
                 + f" | {np.mean([t[6] for _, t in tl]):.1f} | {past52:.2f} | {cst:.1f} | {owed_h[2] - cst:+.1f} |")
    why = Counter(t[9] for r in rs for t in r["tools"])
    L += ["", f"Why tools stopped being followed: {dict(why)}.", "",
          "| maker's skill | tools | owed by 52 weeks | proxy at 52 weeks |", "|---|---|---|---|"]
    for sb, name in enumerate(SKILL):
        tl = [(r["seed"], t) for r in rs for t in r["tools"] if parse(t[4])[5] == sb]
        if not tl:
            continue
        o52 = np.mean([t[7][2] for _, t in tl])
        cost = [cellmean.get((s, t[4])) for s, t in tl]
        cost = [x for x in cost if x is not None]
        L.append(f"| {name} | {len(tl)} | {o52:.1f} | {o52 - (np.mean(cost) if cost else float('nan')):+.1f} |")
    L.append("")


def r_end(rs, seed):
    return next(r["final_tick"] for r in rs if r["seed"] == seed)


def section_q5(L):
    L += ["## Q5 — The three hypotheses (read from the tables above; all may hold)", "",
          "- **Low-skill trap:** within matched states, choosing to make rises with skill (Q2's standardised rates); "
          "the learned worth of the same kind is lower for low-skill makers (Q2's relative worth); late makers' lower "
          "worth goes with lower skill (Q3's v part, read beside Q2).",
          "- **Opportunity cost dominates:** skilled makers also reject making (Q2's top band); the other options' "
          "soft maximum carries the fall (Q3's '− U_other' part); making pays less than one forage act within a "
          "year (Q4's proxy).",
          "- **Delayed-benefit failure:** a tool's owed food over a year exceeds the cost (Q4's proxy > 0), while "
          "learned worth and the chance of choosing to make stay low.", ""]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rs = load()
    L = ["# MK1 — Why is making not chosen? Results", "",
         "Frozen as `MK1-frozen` (with draft revision 1; operational note 1). run_mk1.py, analyse_mk1.py (written "
         "before data).", ""]
    ok = section_validity(L, rs)
    if not ok and not SMOKE:
        text = "\n".join(L) + "\n"
        (HERE / "results.md").write_text(text, encoding="utf-8")
        print(text)
        return
    section_population(L, rs)
    section_gate(L, rs)
    section_q2(L, rs)
    section_q3(L, rs)
    section_q4(L, rs)
    section_q5(L)
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
