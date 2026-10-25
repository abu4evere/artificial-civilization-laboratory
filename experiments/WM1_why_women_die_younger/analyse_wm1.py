"""WM1 analysis in the frozen order (questions.md, `WM1-frozen`). Written before any data.

  python experiments/WM1_why_women_die_younger/analyse_wm1.py            # writes results.md
  python experiments/WM1_why_women_die_younger/analyse_wm1.py --smoke    # throwaway smoke outputs; writes nothing

Rates are deaths per 1,000 person-years (person-weeks / 52) of world-born people, by sex and 5-year band (16-19 ..
50-54). Age-standardised with fixed equal weights over those 8 bands; a band with no person-weeks for either sex is
dropped for both (counted). G = standardised female minus male rate; R = female / male standardised rate.
Intervals: world bootstrap, 10,000 replicates, percentile 95%; Part B paired by seed (all arms resampled together).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_wm1 import ARMS, OUT, SEEDS, SMOKE_SEEDS, WPY, YEARS  # noqa: E402

BANDS = ["16-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54"]
WIDTH = [4, 5, 5, 5, 5, 5, 5, 5]                       # years in each band (to age 55)
SURV_BANDS = 7                                         # 16-19 .. 45-49: survival from 16 to 50
CAUSES = ["childbirth", "starvation", "illness", "thirst", "killed", "old age"]
LOADS_F = ["pregnant", "after delivery", "carer", "unloaded"]
LOADS_M = ["carer", "unloaded"]
B = 10_000
DESIGN = ["c20", "p", "b", "k", "pb", "pk", "bk", "pbk"]
EFFECTS = ["p", "b", "k", "pb", "pk", "bk", "pbk"]


def load(out, seeds):
    rows, missing = {}, []
    for a in ARMS:
        for s in seeds:
            f = out / f"{a}_seed_{s}.json"
            if f.exists():
                rows.setdefault(a, []).append(json.loads(f.read_text(encoding="utf-8")))
            else:
                missing.append(f"{a} {s}")
    return rows, missing


def mats(rs, ind="all", val="all", group="world"):
    """Per world: person-weeks [w, sex, band] and deaths [w, sex, band, cause] (+ 'other' last)."""
    n = len(rs)
    pw = np.zeros((n, 2, 8))
    d = np.zeros((n, 2, 8, len(CAUSES) + 1))
    for i, r in enumerate(rs):
        for si, sx in enumerate("FM"):
            for bi, b in enumerate(BANDS):
                c = r["cells"].get(f"{group}|{sx}|{b}|{ind}|{val}")
                if not c:
                    continue
                pw[i, si, bi] = c[0]
                for cause, k in c[4].items():
                    d[i, si, bi, CAUSES.index(cause) if cause in CAUSES else len(CAUSES)] += k
    return pw, d


def rates(pw, d):
    """pw [..., 2, 8], d [..., 2, 8] -> per-band rates per 1,000 person-years, NaN where no person-weeks."""
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(pw > 0, d / pw * WPY * 1000, np.nan)


def std(pw, d):
    """Equal-weight standardised F and M rates, G, R over bands with person-weeks for both sexes."""
    r = rates(pw, d)
    ok = ~np.isnan(r[..., 0, :]) & ~np.isnan(r[..., 1, :])
    rf = np.where(ok, r[..., 0, :], 0).sum(-1) / np.maximum(ok.sum(-1), 1)
    rm = np.where(ok, r[..., 1, :], 0).sum(-1) / np.maximum(ok.sum(-1), 1)
    with np.errstate(divide="ignore", invalid="ignore"):
        return rf, rm, rf - rm, rf / rm, (ok.sum(-1) < 8)


def boot_idx(n, seed=20261025):
    return np.random.default_rng(seed).integers(0, n, size=(B, n))


def ci(x):
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    if not len(x):
        return "-"
    lo, hi = np.percentile(x, [2.5, 97.5])
    return f"[{lo:.2f}, {hi:.2f}]"


def lohi(x):
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    return np.percentile(x, [2.5, 97.5])


def survival(pw, d):
    """Life table from band hazards: S(16 -> 50) per sex, [..., 2]."""
    with np.errstate(divide="ignore", invalid="ignore"):
        h = np.where(pw > 0, d / pw, 0.0)[..., :SURV_BANDS]
    w = np.array(WIDTH[:SURV_BANDS]) * WPY
    return np.prod((1 - h) ** w, axis=-1)


def pop_line(rs):
    ta = np.mean([np.mean((r["pops"] + [0] * YEARS)[:YEARS]) for r in rs])
    died = sum(1 for r in rs if r["final_tick"] < YEARS * WPY)
    py = sum(c[0] for r in rs for k, c in r["cells"].items() if k.startswith("world|") and k.endswith("|all|all")) / WPY
    return ta, died, py


def main(smoke=False):
    seeds = SMOKE_SEEDS if smoke else SEEDS
    out = HERE / "output_smoke" if smoke else OUT
    rows, missing = load(out, seeds)
    L = [f"# WM1 — why do women die younger than men? Results{' (SMOKE TEST, throwaway seeds)' if smoke else ''}", "",
         "Frozen as `WM1-frozen`. run_wm1.py, analyse_wm1.py (written before data). Rates: deaths per 1,000 "
         "person-years of world-born people; age-standardised with equal weights over 16-19 .. 50-54.", "",
         "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks: **{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present ({len(ARMS) * len(seeds)}): **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing
    if missing:
        L += ["", "**NOT VALID: no outcome is shown.**"]
        return finish(L, smoke)
    fp_ok = True
    for code in ("v7", "wm1"):
        fps = {h for a, rs in rows.items() if ARMS[a]["code"] == code for r in rs for h in (r["code_hash"], r["code_hash_after"])}
        L.append(f"- One fingerprint for `code_{code}`: **{'yes' if len(fps) == 1 else 'NO'}** ({', '.join(f[:12] for f in fps)})")
        fp_ok &= len(fps) == 1
    ok &= fp_ok
    seeds_ok = all([r["seed"] for r in rows[a]] == list(seeds) for a in ARMS)
    L.append(f"- Seeds paired across arms: **{'yes' if seeds_ok else 'NO'}**")
    ok &= seeds_ok
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if not ok and not smoke:                           # a smoke test goes on, to exercise the code
        return finish(L, smoke)
    n = len(seeds)
    idx = boot_idx(n)

    # ---------------- Q1
    L += ["", "## Q1 — The gap (primary)", "",
          "| setting | time-avg pop. | died out | world-born adult person-years | women: std rate | men: std rate | "
          "G (F − M) [95%] | R (F / M) [95%] | survival 16→50 women | men |", "|---|---|---|---|---|---|---|---|---|---|"]
    for a in ("c20", "d80"):
        rs = rows[a]
        pw, d = mats(rs)
        dt = d.sum(-1)
        rf, rm, g, r_, drop = std(pw.sum(0), dt.sum(0))
        bp, bd = pw[idx].sum(1), dt[idx].sum(1)
        brf, brm, bg, br, bdrop = std(bp, bd)
        s = survival(pw.sum(0), dt.sum(0))
        bs = survival(bp, bd)
        ta, died, py = pop_line(rs)
        L.append(f"| {a.upper()} | {ta:.1f} | {died} of {n} | {py:,.0f} | {rf:.1f} {ci(brf)} | {rm:.1f} {ci(brm)} | "
                 f"**{g:.1f}** {ci(bg)} | **{r_:.2f}** {ci(br)} | {s[0]:.3f} {ci(bs[:, 0])} | {s[1]:.3f} {ci(bs[:, 1])} |")
        if bdrop.any() or drop:
            L.append(f"\n({a.upper()}: a band was dropped in the estimate: {bool(drop)}; in {int(bdrop.sum())} of {B} replicates.)")
    L += ["", "Band rates (per 1,000 person-years; deaths / person-years):", "",
          "| setting | sex | " + " | ".join(BANDS) + " |", "|---|---|" + "---|" * 8]
    for a in ("c20", "d80"):
        pw, d = mats(rows[a])
        P, D = pw.sum(0), d.sum(-1).sum(0)
        rr = rates(P, D)
        for si, sx in enumerate("FM"):
            L.append(f"| {a.upper()} | {sx} | " + " | ".join(
                f"{rr[si, b]:.1f} ({D[si, b]:.0f}/{P[si, b] / WPY:,.0f})" if P[si, b] else "-" for b in range(8)) + " |")
    L += ["", "Survival 16 → 50 by birth cohort (world-born):", "", "| setting | cohort | women | men |", "|---|---|---|---|"]
    for a in ("c20", "d80"):
        for coh in ("born <40", "born 40-69"):
            pw, d = mats(rows[a], "cohort", coh)
            dt = d.sum(-1)
            s = survival(pw.sum(0), dt.sum(0))
            bs = survival(pw[idx].sum(1), dt[idx].sum(1))
            L.append(f"| {a.upper()} | {coh} | {s[0]:.3f} {ci(bs[:, 0])} | {s[1]:.3f} {ci(bs[:, 1])} |")

    # ---------------- Q2
    L += ["", "## Q2 — Loads and their aftermath (primary, descriptive: associations, not causes)", "",
          "Standardised rates per sex over the bands with person-weeks in that sex (equal weights; bands used shown). "
          "\"Within 10%\" (R in [0.9, 1.1]) is a descriptive tolerance only.", ""]
    inds = [("load", LOADS_F), ("preg", ["no", "trim1", "trim2", "trim3"]),
            ("since", ["never", "0-12", "13-52", "53-104", ">104"]),
            ("preg_deps", ["neither", "preg only", "deps only", "preg+deps"]), ("deps", ["0", "1", "2", "3+"]),
            ("fed_share", ["0", "<25%", "25-50%", ">50%"]), ("deficit13", ["0", "0-0.1", "0.1-0.3", ">0.3"]),
            ("sick_now", ["no", "yes"]), ("sick_year", ["0", "1-4", "5+"]), ("health", ["<40", "40-70", "70-90", ">=90"])]
    for a in ("c20", "d80"):
        L += [f"### {a.upper()}", "", "| indicator | value | women: person-years | women: std rate [95%] (bands) | "
              "men: person-years | men: std rate [95%] (bands) |", "|---|---|---|---|---|---|"]
        for ind, vals in inds:
            for v in vals:
                pw, d = mats(rows[a], ind, v)
                dt = d.sum(-1)
                cells = []
                for si in (0, 1):
                    P, D = pw.sum(0)[si], dt.sum(0)[si]
                    if P.sum() == 0:
                        cells += ["0", "-"]
                        continue
                    r = rates(P, D)
                    okb = ~np.isnan(r)
                    est = np.nanmean(r)
                    bP, bD = pw[idx].sum(1)[:, si], dt[idx].sum(1)[:, si]
                    br = rates(bP, bD)
                    with np.errstate(all="ignore"):
                        nb = (~np.isnan(br)).sum(-1)
                        bm = np.where(nb > 0, np.nansum(br, axis=-1) / np.maximum(nb, 1), np.nan)
                    cells += [f"{P.sum() / WPY:,.0f}", f"{est:.1f} {ci(bm)} ({int(okb.sum())})"]
                L.append(f"| {ind} | {v} | " + " | ".join(cells) + " |")
        L.append("")

    # ---------------- Q3
    L += ["## Q3 — Cause and state (primary, descriptive; signed contributions to G)", "",
          "G split exactly: each row is the standardised female-minus-male rate of that cause (or of deaths in that "
          "state at death, over all person-weeks). Rows sum to G. Negative = an offset.", ""]
    for a in ("c20", "d80"):
        pw, d = mats(rows[a])
        P = pw.sum(0)
        bP = pw[idx].sum(1)
        ok_b = (P[0] > 0) & (P[1] > 0)
        g_total = None
        L += [f"### {a.upper()}", "", "| part | contribution to G [95%] | share of G |", "|---|---|---|"]
        parts = [(c, d[..., k]) for k, c in enumerate(CAUSES + ["other"])]
        lp = {}
        for st in LOADS_F:
            pwl, dl = mats(rows[a], "load", st)
            lp[st] = dl.sum(-1)
        contrib = []
        for name, dd in parts:
            r = rates(P, dd.sum(0))
            c = np.mean(np.where(ok_b, r[0] - r[1], 0)[ok_b]) if ok_b.any() else np.nan
            br = rates(bP, dd[idx].sum(1))
            bc = np.nanmean(br[:, 0, :] - br[:, 1, :], axis=-1)
            contrib.append((f"cause: {name}", c, bc))
        for st in LOADS_F:
            r = rates(P, lp[st].sum(0))
            c = np.mean((r[0] - r[1])[ok_b])
            br = rates(bP, lp[st][idx].sum(1))
            bc = np.nanmean(br[:, 0, :] - br[:, 1, :], axis=-1)
            contrib.append((f"state at death: {st}", c, bc))
        g_total = sum(c for nm, c, _ in contrib if nm.startswith("cause"))
        for nm, c, bc in contrib:
            L.append(f"| {nm} | {c:.2f} {ci(bc)} | {100 * c / g_total:.0f}% |" if g_total else f"| {nm} | {c:.2f} {ci(bc)} | - |")
        L.append(f"\nG = {g_total:.2f} (sum of the causes).\n")

    # ---------------- Q4 / Q5
    L += ["## Q4 — The diagnostic arms (primary, causal diagnostic; C20; paired by seed)", "",
          "Δ = G(arm) − G(C20, v7). Negative = the female disadvantage shrinks. Main effects and interactions from the "
          "2 × 2 × 2 design (contrast / 4). Verdict for a main effect: **reduces the gap** if its interval lies below 0; "
          "otherwise **does not** if its interval lies above −1; otherwise **unclear** (operational note 1).", "",
          "| arm | time-avg pop. | died out | women std rate | men std rate | G [95%] | Δ vs C20 [95%] | child survival to 5 | "
          "deliveries per woman reaching 45 |", "|---|---|---|---|---|---|---|---|---|"]
    G, BG = {}, {}
    for a in DESIGN:
        rs = rows[a]
        pw, d = mats(rs)
        dt = d.sum(-1)
        rf, rm, g, _, _ = std(pw.sum(0), dt.sum(0))
        brf, brm, bg, _, _ = std(pw[idx].sum(1), dt[idx].sum(1))
        G[a], BG[a] = g, bg
    for a in DESIGN:
        rs = rows[a]
        pw, d = mats(rs)
        dt = d.sum(-1)
        rf, rm, g, _, _ = std(pw.sum(0), dt.sum(0))
        brf, brm, _, _, _ = std(pw[idx].sum(1), dt[idx].sum(1))
        ta, died, py = pop_line(rs)
        c5 = sum(r["child5"][0] for r in rs) / max(1, sum(r["child5"][1] for r in rs))
        dw = sum(r["deliveries_women45"] for r in rs) / max(1, sum(r["women45"] for r in rs))
        delta = "-" if a == "c20" else f"{G[a] - G['c20']:.2f} {ci(BG[a] - BG['c20'])}"
        L.append(f"| {a.upper() if a != 'c20' else 'C20 (v7)'} | {ta:.1f} | {died} | {rf:.1f} {ci(brf)} | {rm:.1f} {ci(brm)} | "
                 f"{g:.2f} {ci(BG[a])} | {delta} | {c5:.3f} | {dw:.2f} (of {sum(r['women45'] for r in rs)}) |")
    L += ["", "| effect | estimate [95%] | verdict (main effects only) |", "|---|---|---|"]

    def coded(a, f):
        return 1 if f in a and a != "c20" else -1
    for eff in EFFECTS:
        coef = {a: np.prod([coded(a, f) for f in eff]) for a in DESIGN}
        est = sum(coef[a] * G[a] for a in DESIGN) / 4
        best = sum(coef[a] * BG[a] for a in DESIGN) / 4
        lo, hi = lohi(best)
        verdict = ""
        if len(eff) == 1:
            verdict = "reduces the gap" if hi < 0 else "does not" if lo > -1 else "unclear"
        L.append(f"| {eff.upper()} | {est:.2f} {ci(best)} | {verdict} |")
    share = G["pbk"] / G["c20"] if G["c20"] else np.nan
    with np.errstate(divide="ignore", invalid="ignore"):
        bshare = BG["pbk"] / BG["c20"]
    lo, _ = lohi(BG["pbk"])
    L += ["", "## Q5 — All three removed (P0 + B0 + K0)", "",
          f"- G with all three removed: {G['pbk']:.2f} {ci(BG['pbk'])}; the share of G that remains: {share:.2f} {ci(bshare)}.",
          f"- G stays clearly above 0 (interval above 0): **{'yes: the gap has another source' if lo > 0 else 'no'}**."]

    # ---------------- described
    L += ["", "## Described only", ""]
    L += ["| setting / arm | women's share of carer-weeks | food given to dependants per adult week, women / men | "
          "hunting share of weeks, women / men | attacks made per 1,000 weeks, women / men | injuries per 1,000 weeks, women / men | "
          "tiles moved per week, women / men |", "|---|---|---|---|---|---|---|"]
    for a in ARMS:
        rs = rows[a]
        cw = {s: sum(r["carer_weeks"][s] for r in rs) for s in "FM"}

        def ex(s, what):
            return sum(r["expo"].get(f"{s}|world|{what}", 0) for r in rs)
        fed = {}
        for s in "FM":
            P = sum(c[0] for r in rs for k, c in r["cells"].items() if k.startswith(f"world|{s}|") and k.endswith("|all|all"))
            F = sum(c[3] for r in rs for k, c in r["cells"].items() if k.startswith(f"world|{s}|") and k.endswith("|all|all"))
            fed[s] = F / P if P else 0
        wk = {s: max(1, ex(s, "weeks")) for s in "FM"}
        L.append(f"| {a} | {cw['F'] / max(1, cw['F'] + cw['M']):.2f} | {fed['F']:.2f} / {fed['M']:.2f} | "
                 f"{ex('F', 'hunt_weeks') / wk['F']:.3f} / {ex('M', 'hunt_weeks') / wk['M']:.3f} | "
                 f"{1000 * (ex('F', 'attack') + ex('F', 'kill')) / wk['F']:.2f} / {1000 * (ex('M', 'attack') + ex('M', 'kill')) / wk['M']:.2f} | "
                 f"{1000 * ex('F', 'injured') / wk['F']:.2f} / {1000 * ex('M', 'injured') / wk['M']:.2f} | "
                 f"{ex('F', 'travel') / wk['F']:.2f} / {ex('M', 'travel') / wk['M']:.2f} |")
    L += ["", "Food given to adults (by giver's relation), per recipient state, C20:", "",
          "| recipient | state | partner | kin | other |", "|---|---|---|---|---|"]
    rs = rows["c20"]
    for s in "FM":
        for st in (LOADS_F if s == "F" else LOADS_M):
            vals = [sum(r["prov"].get(f"{s}|{st}|{rel}", 0.0) for r in rs) for rel in ("partner", "kin", "other")]
            L.append(f"| {s} | {st} | " + " | ".join(f"{v:,.0f}" for v in vals) + " |")
    L += ["", "Deaths of world-born adults 16-54 in C20: partner alive / near at death; last 13 weeks:", "",
          "| sex | deaths | partner alive | partner within 2 tiles | mean food given out | mean food received | mean deficit |",
          "|---|---|---|---|---|---|---|"]
    for s in "FM":
        ds = [x for r in rs for x in r["deaths"] if x["group"] == "world" and x["sex"] == s and 16 <= x["age"] < 55]
        if ds:
            L.append(f"| {s} | {len(ds)} | {np.mean([x['partner_alive'] for x in ds]):.2f} | "
                     f"{np.mean([x['partner_near'] for x in ds]):.2f} | {np.mean([x['fed13'] for x in ds]):.1f} | "
                     f"{np.mean([x['recv13'] for x in ds]):.1f} | {np.mean([x['def13'] for x in ds]):.3f} |")
    L += ["", "Founders (C20 and D80):", "", "| setting | women std rate | men std rate | G |", "|---|---|---|---|"]
    for a in ("c20", "d80"):
        pw, d = mats(rows[a], group="founder")
        rf, rm, g, _, _ = std(pw.sum(0), d.sum(-1).sum(0))
        L.append(f"| {a.upper()} | {rf:.1f} | {rm:.1f} | {g:.1f} |")
    return finish(L, smoke)


def finish(L, smoke):
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
