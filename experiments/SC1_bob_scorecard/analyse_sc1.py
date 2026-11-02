"""SC1 analysis, written before any data (questions.md, frozen as `SC1-frozen`; operational notes 1 and 2).

  python experiments/SC1_bob_scorecard/analyse_sc1.py                      # writes results.md
  python experiments/SC1_bob_scorecard/analyse_sc1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_sc1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261103)
MIN = 30
DELTA = {"C3": 0.02, "C4": 0.05, "C5": 0.05, "C6": 0.05, "C7": 0.05, "C9": 0.10, "C10b": 0.05, "C12": 0.05}


def label(name, ci_lo):
    return "positive contrast detected" if ci_lo > DELTA[name] else "inconclusive"


def pct(x):
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {}
    for f in sorted(glob.glob(str(OUTDIR / "c_seed_*.json"))):
        r = json.load(open(f))
        runs[r["seed"]] = r
    zero = ""
    for name in ("zero_cloud.log", "zero_local.log"):
        if (HERE / name).exists():
            zero = (HERE / name).read_text(encoding="utf-8", errors="replace")
            break
    R.base.setup(R.CODE)
    fp_now = R.base.fingerprint(R.CODE)
    m = re.search(r"code_v11 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    seeds = sorted(runs)
    present = (len(seeds) > 0) if SMOKE else seeds == sorted(R.SEEDS)
    fps = {r["code_hash"] for r in runs.values()} | {r["code_hash_after"] for r in runs.values()}
    mism = sum(sum(r["mismatch"].values()) for r in runs.values())
    ok = bool(zero_ok and present and fps == {fp_now} and mism == 0)
    L = ["# SC1 — A scorecard of the creator's twelve capacities on live v11: results", "",
         "Frozen as `SC1-frozen` (operational notes 1 and 2). run_sc1.py, analyse_sc1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks (All: PASS, same `code_v11` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(seeds)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_v11`'s: **{'yes' if fps == {fp_now} else 'NO'}**",
         f"- Every habit update replays exactly (mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**",
         "", f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def vec(f):
        return np.array([float(f(runs[s])) for s in seeds])

    def ratio_diff(a1, b1, a2, b2):
        pt = a1.sum() / b1.sum() - a2.sum() / b2.sum()
        with np.errstate(invalid="ignore", divide="ignore"):
            rep = (W @ a1) / (W @ b1) - (W @ a2) / (W @ b2)
        return pt, *pct(rep)

    rows, notes = [], []

    # C3: calibration gain with experience, standardized over situation x action cells
    cells = sorted({k.split("|", 1)[1] for r in runs.values() for k in r["c3"]})
    ci_ = {c: j for j, c in enumerate(cells)}

    def c3mat(band, f):
        M = np.zeros((len(cells), n))
        for j, s in enumerate(seeds):
            for k, v in runs[s]["c3"].items():
                b, c = k.split("|", 1)
                if b == band:
                    M[ci_[c], j] = v[f]
        return M
    Nl, Sl, Nh, Sh = c3mat("lo", 0), c3mat("lo", 1), c3mat("hi", 0), c3mat("hi", 1)
    common = (Nl.sum(1) >= MIN) & (Nh.sum(1) >= MIN)
    wts = np.where(common, Nl.sum(1), 0.0)

    def E(N, S, valid, w):
        ww = np.where(valid, w, 0.0)
        with np.errstate(invalid="ignore", divide="ignore"):
            mean = np.where(valid, S / np.where(N > 0, N, 1), 0.0)
        return (ww * mean).sum(-1) / ww.sum(-1)
    if common.any():
        pt = float(E(Nl.sum(1), Sl.sum(1), common, wts) - E(Nh.sum(1), Sh.sum(1), common, wts))
        reps = []
        for st in range(0, REPS, 500):
            Wb = W[st:st + 500]
            nl, sl, nh, sh = Wb @ Nl.T, Wb @ Sl.T, Wb @ Nh.T, Wb @ Sh.T
            valid = common[None, :] & (nl > 0) & (nh > 0)
            reps.append(E(nl, sl, valid, wts) - E(nh, sh, valid, wts))
        lo, hi = pct(np.concatenate(reps))
        rows.append(["3 (the rule)", "C3: mean abs(q - G), k 0-19 minus k 80+, adults 16-44",
                     pt, lo, hi, "C3", f"{int(common.sum())} common cells; {int(Nl.sum()):,} + {int(Nh.sum()):,} "
                     f"updates", "the written rule works" if lo > DELTA["C3"] else "inconclusive"])
    else:
        rows.append(["3 (the rule)", "C3", None, None, None, "C3", "no common cells", "not measurable"])

    # C4: switching means after a surprise
    a_s, b_s = vec(lambda r: r["c4"].get("s", [0] * 5)[2]), vec(lambda r: r["c4"].get("s", [0] * 5)[1])
    a_c, b_c = vec(lambda r: r["c4"].get("c", [0] * 5)[2]), vec(lambda r: r["c4"].get("c", [0] * 5)[1])
    if b_s.sum() and b_c.sum():
        pt, lo, hi = ratio_diff(a_s, b_s, a_c, b_c)
        rows.append(["4", "C4: P(alternative | surprising test) - P(alternative | confirming test)", pt, lo, hi,
                     "C4", f"followed tests: surprising {int(b_s.sum()):,}, confirming {int(b_c.sum()):,}",
                     label("C4", lo)])
    else:
        rows.append(["4", "C4", None, None, None, "C4", "no followed tests", "not measurable"])

    # C5: organized production (standardized over material x season)
    strata = sorted({k.split("|", 1)[1] for r in runs.values() for k in r["c5"]})

    def c5arr(wanted, f):
        M = np.zeros((len(strata), n))
        for j, s in enumerate(seeds):
            for k, v in runs[s]["c5"].items():
                g, st = k.split("|", 1)
                if g == str(wanted):
                    M[strata.index(st), j] = v[f]
        return M
    N1, M1, N0, M0 = c5arr(1, 0), c5arr(1, 1), c5arr(0, 0), c5arr(0, 1)
    if N0.sum() < MIN:
        rows.append(["5", "C5: P(make | wanted gather) - P(make | not wanted)", None, None, None, "C5",
                     f"not-wanted gathers {int(N0.sum())} (< {MIN}); wanted {int(N1.sum()):,}",
                     "not measurable in v11 (the written want covers nearly every gather)"])
    else:
        both = (N1.sum(1) > 0) & (N0.sum(1) > 0)
        ws = np.where(both, N1.sum(1) + N0.sum(1), 0.0)

        def std(n1, m1, n0, m0, valid):
            ww = np.where(valid, ws, 0.0)
            with np.errstate(invalid="ignore", divide="ignore"):
                d = np.where(valid, m1 / np.where(n1 > 0, n1, 1) - m0 / np.where(n0 > 0, n0, 1), 0.0)
            return (ww * d).sum(-1) / ww.sum(-1)
        pt = float(std(N1.sum(1), M1.sum(1), N0.sum(1), M0.sum(1), both))
        n1, m1, n0, m0 = W @ N1.T, W @ M1.T, W @ N0.T, W @ M0.T
        lo, hi = pct(std(n1, m1, n0, m0, both[None, :] & (n1 > 0) & (n0 > 0)))
        rows.append(["5", "C5: P(make | wanted gather) - P(make | not wanted), standardized", pt, lo, hi, "C5",
                     f"gathers: wanted {int(N1.sum()):,}, not wanted {int(N0.sum()):,}",
                     "organized production detected" if lo > DELTA["C5"] else "inconclusive"])

    # C6: invention with selection by use
    kinds = {s: runs[s]["c6_kinds"] for s in seeds}
    allbf = np.array([k[0] for s in seeds for k in kinds[s]])
    nf, nn = int((allbf >= 1.10).sum()), int((allbf < 1.02).sum())
    if nf >= MIN and nn >= MIN:
        top, bot, how = (lambda b: b >= 1.10), (lambda b: b < 1.02), "best factor >= 1.10 vs < 1.02"
    elif len(allbf) >= 2 * MIN:
        q1, q2 = np.quantile(allbf, [1 / 3, 2 / 3])
        top, bot, how = (lambda b: b > q2), (lambda b: b <= q1), (f"fallback (op. note 2): top third (> {q2:.3f}) vs "
                                                                   f"bottom third (<= {q1:.3f})")
    else:
        top = None
    if top is not None:
        at, bt = vec(lambda r: sum(k[1] for k in r["c6_kinds"] if top(k[0]))), vec(lambda r: sum(1 for k in r["c6_kinds"] if top(k[0])))
        ab, bb = vec(lambda r: sum(k[1] for k in r["c6_kinds"] if bot(k[0]))), vec(lambda r: sum(1 for k in r["c6_kinds"] if bot(k[0])))
        if bt.sum() and bb.sum():
            pt, lo, hi = ratio_diff(at, bt, ab, bb)
            rows.append(["6", f"C6: P(remade in 5 years | more useful) - P(remade | less useful); {how}", pt, lo, hi,
                         "C6", f"world-new kinds {len(allbf):,} (more useful {int(bt.sum()):,}, less {int(bb.sum()):,})",
                         label("C6", lo)])
        else:
            rows.append(["6", "C6", None, None, None, "C6", "an empty class", "not measurable"])
    else:
        rows.append(["6", "C6", None, None, None, "C6", f"world-new kinds {len(allbf)}", "not measurable"])

    # C7: own against told puzzles, matched on size
    def c7(origin, b, f):
        return vec(lambda r: r["c7"].get(f"{origin}|{b}", [0, 0])[f])
    told_n = sum(c7("told", b, 0).sum() for b in ("a", "b"))
    own_n = sum(c7("own", b, 0).sum() for b in ("a", "b"))
    if told_n < MIN:
        rows.append(["7", "C7: P(acted | own puzzle) - P(acted | told), size-matched", None, None, None, "C7",
                     f"told puzzles in the bins {int(told_n)} (< {MIN}); own {int(own_n):,}",
                     "not measurable in v11 (too few told puzzles of matching size)"])
    else:
        bins = [b for b in ("a", "b") if c7("own", b, 0).sum() > 0 and c7("told", b, 0).sum() > 0]
        wb = {b: c7("own", b, 0).sum() + c7("told", b, 0).sum() for b in bins}
        tot = sum(wb.values())
        pt = sum(wb[b] / tot * (c7("own", b, 1).sum() / c7("own", b, 0).sum() - c7("told", b, 1).sum() / c7("told", b, 0).sum())
                 for b in bins)
        num, den = np.zeros(REPS), np.zeros(REPS)
        for b in bins:
            with np.errstate(invalid="ignore", divide="ignore"):
                d = (W @ c7("own", b, 1)) / (W @ c7("own", b, 0)) - (W @ c7("told", b, 1)) / (W @ c7("told", b, 0))
            okb = np.isfinite(d)
            num += np.where(okb, wb[b] * d, 0.0)
            den += np.where(okb, wb[b], 0.0)
        lo, hi = pct(num / den)
        rows.append(["7", "C7: P(acted | own puzzle) - P(acted | told), size-matched", float(pt), lo, hi, "C7",
                     f"puzzles: own {int(own_n):,}, told {int(told_n):,}", label("C7", lo)])

    # C9: told places beat chance
    chk = vec(lambda r: sum(v[0] for v in r["c9"].values()))
    ver = vec(lambda r: sum(v[1] for v in r["c9"].values()))
    ctl = vec(lambda r: sum(v[2] for v in r["c9"].values()))
    if chk.sum():
        pt, lo, hi = ratio_diff(ver, chk, ctl, chk)
        by = {k: [sum(runs[s]["c9"].get(k, [0, 0, 0])[i] for s in seeds) for i in range(3)] for k in ("w:", "g:")}
        rows.append(["9", "C9: P(told place verified) - P(random tile at the same distance passes)", pt, lo, hi, "C9",
                     f"checked {int(chk.sum()):,} (water {by['w:'][0]:,}: {by['w:'][1]:,} vs {by['w:'][2]:,}; "
                     f"game {by['g:'][0]:,}: {by['g:'][1]:,} vs {by['g:'][2]:,})", label("C9", lo)])
    else:
        rows.append(["9", "C9", None, None, None, "C9", "no checked places", "not measurable"])

    # C10b: building on others' know-how
    nest = vec(lambda r: r["c10"].get("nested", 0))
    soc = vec(lambda r: r["c10"].get("social_part", 0))
    opp = vec(lambda r: r["c10"].get("opportunity", 0))
    if nest.sum():
        pt, lo, hi = ratio_diff(soc, nest, opp, nest)
        rows.append(["10b", "C10b: P(part learned from someone) - repertoire's learned share", pt, lo, hi, "C10b",
                     f"world-new nested kinds {int(nest.sum()):,} (part learned from someone {int(soc.sum()):,})",
                     label("C10b", lo)])
    else:
        rows.append(["10b", "C10b", None, None, None, "C10b", "no nested kinds", "not measurable"])

    # C12: stable behavioural individuality (nested ridge models, leave-folds-out)
    def design(s):
        snaps = {(x[0], x[1]): x for x in runs[s]["snaps"]}
        XA, XB, Y = [], [], []
        for (pid, y), a in snaps.items():
            b = snaps.get((pid, y + 5))
            if b is None or y + 5 > 195:
                continue
            ta, tb = sum(a[5]), sum(b[5])
            sb = sum(b[6])
            if not (ta and tb and sb):
                continue
            base = list(a[4]) + [a[2], 1.0 if a[3] == "M" else 0.0] + [v / sb for v in b[6]] + list(a[7])
            XA.append(base)
            XB.append(base + [v / ta for v in a[5]])
            Y.append([v / tb for v in b[5]])
        return np.array(XA), np.array(XB), np.array(Y)
    D = {s: design(s) for s in seeds}
    folds = {s: i % 4 for i, s in enumerate(seeds)}

    def ridge_sse(which):
        sse = np.zeros(n)
        cnt = np.zeros(n)
        for f in range(4):
            tr = [s for s in seeds if folds[s] != f and len(D[s][2])]
            te = [s for s in seeds if folds[s] == f and len(D[s][2])]
            if not tr or not te:
                continue
            X = np.vstack([D[s][which] for s in tr])
            Y = np.vstack([D[s][2] for s in tr])
            mu, sd = X.mean(0), X.std(0)
            sd[sd == 0] = 1.0
            Xs = np.hstack([(X - mu) / sd, np.ones((len(X), 1))])
            P = np.eye(Xs.shape[1])
            P[-1, -1] = 0.0
            B = np.linalg.solve(Xs.T @ Xs + 1.0 * P, Xs.T @ Y)
            for s in te:
                Xt = np.hstack([(D[s][which] - mu) / sd, np.ones((len(D[s][which]), 1))])
                e = D[s][2] - Xt @ B
                j = seeds.index(s)
                sse[j] = float((e ** 2).sum())
                cnt[j] = e.size
        return sse, cnt
    if sum(len(D[s][2]) for s in seeds) >= MIN:
        sa, ca = ridge_sse(0)
        sb, _ = ridge_sse(1)
        pt = (sa.sum() - sb.sum()) / sa.sum()
        with np.errstate(invalid="ignore", divide="ignore"):
            rep = ((W @ sa) - (W @ sb)) / (W @ sa)
        lo, hi = pct(rep)
        rows.append(["12", "C12: relative cut in held-out error from adding year-t actions to Model A (with habits)",
                     float(pt), lo, hi, "C12", f"person pairs (t, t+5) {sum(len(D[s][2]) for s in seeds):,}",
                     label("C12", lo)])
    else:
        sa = sb = np.zeros(n)
        rows.append(["12", "C12", None, None, None, "C12", "too few person pairs", "not measurable"])

    # Described (given and not measurable)
    def ysum(key):
        return sum(v.get(key, 0) for r in runs.values() for v in r["yearly"].values())
    adult_years = ysum("adults")
    dec = sum(r["sums"].get("adult_decisions", 0) for r in runs.values())
    comp = sum(r["sums"].get("company_decisions", 0) for r in runs.values())
    paths = {}
    for r in runs.values():
        for k, v in r["paths"].items():
            paths[k] = paths.get(k, 0) + v
    ptot = sum(paths.values()) or 1
    fmt = lambda x: "-" if x is None else f"{x:+.4f}"  # noqa: E731
    L += ["## Measured capacities (primary contrasts)", "",
          "| capacity | contrast | value [95%] | min. effect | sample | reading |", "|---|---|---|---|---|---|"]
    for cap, name, pt, lo, hi, key, sample, read in rows:
        L.append(f"| {cap} | {name} | {fmt(pt)} [{fmt(lo)}, {fmt(hi)}] | {DELTA[key]} | {sample} | **{read}** |")
    L += ["", "A reading is \"positive contrast detected\" only when the interval's lower bound exceeds the minimum "
          "effect; otherwise \"inconclusive\" (never \"absent\"). C3 reads \"the written rule works\"; C5 reads at most "
          "\"organized production detected\".", "",
          "## Given (described)", "",
          f"- **1. Perception:** {comp / dec:.3f} of adult decisions have company within reach "
          f"({int(dec):,} decisions)." if dec else "- 1. Perception: no decisions",
          f"- **11. Motivation:** adults' mean mood {ysum('mood') / adult_years:.3f}, loneliness "
          f"{ysum('loneliness') / adult_years:.3f} ({int(adult_years):,} adult-years)." if adult_years else "- 11: -",
          "", "## Not measurable in v11 (described)", "",
          f"- **2. Memory, retrieval when relevant:** adults hold {ysum('memories') / adult_years:.1f} memories on "
          f"average; {ysum('memories_told') / max(ysum('memories'), 1):.2f} of them were told." if adult_years else "- 2: -",
          "- **3 (transfer):** one habit value per situation x action; nothing generalizes.",
          "- **8. Self-model:** nothing represents a person's own ability or uncertainty.",
          "- **10a (social cognition):** whom to trust is written. Social learning, the paths of recipe gains: " +
          ", ".join(f"{k} {v / ptot:.3f}" for k, v in sorted(paths.items(), key=lambda kv: -kv[1])) + ".", ""]
    # C10b and C12 secondaries
    impr = sum(r["c10"].get("improved", 0) for r in runs.values())
    comp10 = sum(r["c10"].get("compared", 0) for r in runs.values())
    hold = [h for r in runs.values() for h in r["holders_late_kinds"]]

    def yr(key, a, b):
        num = sum(v.get(key, 0) for r in runs.values() for y, v in r["yearly"].items() if a <= int(y) < b)
        den = sum(v.get("adults", 0) for r in runs.values() for y, v in r["yearly"].items() if a <= int(y) < b)
        return num / den if den else float("nan")
    outl = ysum("kinds_outliving_first_maker") / max(ysum("kinds_alive"), 1)
    L += ["## Secondary (described, not decisive)", "",
          f"- **C10b improvement:** {impr / comp10:.3f} of new nested kinds beat their best part on its best use "
          f"({int(comp10):,} compared)." if comp10 else "- C10b improvement: -",
          f"- **Holders per kind** first made in years 100-200: mean {np.mean(hold):.2f}, median {np.median(hold):.0f} "
          f"({len(hold):,} kinds)." if hold else "- Holders: -",
          f"- **Kinds alive that outlived their first maker:** {outl:.3f} of alive kind-years.",
          f"- **Nesting depth** (mean of adults' deepest known kind): years 100-125 {yr('depth_sum', 100, 125):.2f}, "
          f"years 175-200 {yr('depth_sum', 175, 200):.2f}."]
    # cross-situation secondary for C12
    cors, base_c = [], []
    rng2 = np.random.default_rng(20261104)
    for s in seeds:
        cr = runs[s]["cross"]
        ids = [p for p, v in cr.items() if sum(v[0]) >= 20 and sum(v[1]) >= 20]
        if len(ids) < 3:
            continue
        F = np.array([np.array(cr[p][0]) / sum(cr[p][0]) for p in ids])
        Rr = np.array([np.array(cr[p][1]) / sum(cr[p][1]) for p in ids])
        F -= F.mean(0)
        Rr -= Rr.mean(0)
        perm = rng2.permutation(len(ids))
        for i in range(len(ids)):
            a, b, c = F[i], Rr[i], Rr[perm[i]]
            if a.std() > 0 and b.std() > 0 and c.std() > 0:
                cors.append(np.corrcoef(a, b)[0, 1])
                base_c.append(np.corrcoef(a, c)[0, 1])
    if cors:
        L.append(f"- **C12 cross-situation (Gemini):** a person's own choice bias in familiar situations correlates "
                 f"{np.mean(cors):.3f} with their bias in rare ones (fewer than 5 earlier visits), against "
                 f"{np.mean(base_c):.3f} for a shuffled pairing ({len(cors):,} people).")
    L.append("")
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    (HERE / "recompute").mkdir(exist_ok=True)
    np.savez(HERE / "recompute" / "c12_sse.npz", seeds=np.array(seeds), sse_a=sa, sse_b=sb)
    print(text)


if __name__ == "__main__":
    main()
