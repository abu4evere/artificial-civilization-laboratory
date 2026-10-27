"""VC1 analysis, written before any data (questions.md, frozen as `VC1-frozen`; operational note 1).

  python experiments/VC1_value_calibration/analyse_vc1.py            # writes results.md
  python experiments/VC1_value_calibration/analyse_vc1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_vc1 import SEEDS, SUMS  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261027)
ERAS = ["0-50", "50-100", "100-200"]
COMMON = ("forage", "give", "talk", "gather")
SHOW = ("make",) + COMMON
J = {k: i for i, k in enumerate(SUMS)}


def cell(r, key):
    return np.array(r["cells"].get(key, [0.0] * len(SUMS)), float)


def pooled(r, era, acts):
    return sum((cell(r, f"{era}|{a}") for a in acts), np.zeros(len(SUMS)))


def weights(n):
    return np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])


def ci(x):
    x = np.asarray(x)
    x = x[np.isfinite(x)]
    if not len(x):
        return "[-]"
    lo, hi = np.percentile(x, [2.5, 97.5])
    return f"[{lo:+.3f}, {hi:+.3f}]"


def stats(s):
    n = s[J["n"]]
    if not n:
        return None
    q, G = s[J["q"]] / n, s[J["G"]] / n
    vq = s[J["qq"]] / n - q * q
    vG = s[J["GG"]] / n - G * G
    cov = s[J["qG"]] / n - q * G
    gap = s[J["gap"]] / s[J["gap_n"]] if s[J["gap_n"]] else float("nan")
    return {"n": n, "q": q, "G": G, "bias": q - G, "gap": gap,
            "slope": cov / vq if vq > 0 else float("nan"),
            "corr": cov / np.sqrt(vq * vG) if vq > 0 and vG > 0 else float("nan"),
            "cens": s[J["cens"]] / n, "link": s[J["gap_n"]] / s[J["link_n"]] if s[J["link_n"]] else float("nan"),
            "r": s[J["r"]] / n, "y": s[J["y"]] / n}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rs = [json.load(open(f)) for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json")))]
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    fps = {r["code_hash"] for r in rs} | {r["code_hash_after"] for r in rs}
    mism = sum(sum(r["mismatch"].values()) for r in rs)
    seeds_ok = sorted(r["seed"] for r in rs) == sorted(SEEDS)
    ok = "All: PASS" in zero and seeds_ok and len(fps) == 1 and mism == 0
    L = ["# VC1 — Are habits calibrated? Results", "",
         "Frozen as `VC1-frozen` (operational note 1). run_vc1.py, analyse_vc1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({len(rs)} of {len(SEEDS)}): **{'yes' if seeds_ok else 'NO'}**",
         f"- One fingerprint (`code_v7`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Every TD update replays exactly (mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    acts = rs[0]["actions"]
    W = weights(len(rs))
    # Q1, Q2, Q4 table
    L += ["## Q1, Q2, Q4 — Calibration by action (adults; q before the update against the realised discounted return G)",
          "", "| era | action | updates | mean q | mean G | bias q − G | max gap 0.8·(max q[s′] − q[s′, a_next]) | "
          "gap / bias | slope of G on q | corr | censored by death | next-week link |", "|---" * 12 + "|"]
    for e, name in enumerate(ERAS):
        for a in SHOW + ("(common pooled)", "(all actions)"):
            group = COMMON if a == "(common pooled)" else (acts if a == "(all actions)" else (a,))
            s = sum((pooled(r, e, group) for r in rs), np.zeros(len(SUMS)))
            st = stats(s)
            if st is None:
                continue
            share = st["gap"] / st["bias"] if st["bias"] else float("nan")
            L.append(f"| {name} | {a} | {st['n']:.0f} | {st['q']:.3f} | {st['G']:.3f} | {st['bias']:+.3f} | "
                     f"{st['gap']:.3f} | {share:.2f} | {st['slope']:.2f} | {st['corr']:.2f} | {st['cens']:.3f} | "
                     f"{st['link']:.3f} |")
    L.append("")
    # named: make's bias against the common actions', years 100-200, with intervals
    late = 2
    per_make = np.stack([pooled(r, late, ("make",)) for r in rs])
    per_com = np.stack([pooled(r, late, COMMON) for r in rs])

    def bias_of(m):
        return (m[:, J["q"]] - m[:, J["G"]]) / m[:, J["n"]]

    with np.errstate(divide="ignore", invalid="ignore"):
        bm = bias_of(W @ per_make)
        bc = bias_of(W @ per_com)
        gm = (W @ per_make)[:, J["gap"]] / (W @ per_make)[:, J["gap_n"]]
        gc = (W @ per_com)[:, J["gap"]] / (W @ per_com)[:, J["gap_n"]]
    sm, sc = stats(per_make.sum(0)), stats(per_com.sum(0))
    if sm and sc:
        L += ["## Named (years 100-200)", "",
              f"- Make: bias q − G {sm['bias']:+.3f} {ci(bm)} (n = {sm['n']:.0f} updates); max gap {sm['gap']:.3f} {ci(gm)}.",
              f"- Common actions (forage, give, talk, gather): bias {sc['bias']:+.3f} {ci(bc)} (n = {sc['n']:.0f}); "
              f"max gap {sc['gap']:.3f} {ci(gc)}.",
              f"- **Make's bias minus the common actions' bias: {sm['bias'] - sc['bias']:+.3f} {ci(bm - bc)}.**",
              f"- Make: q {'below' if sm['bias'] < 0 else 'above'} G; common actions: q "
              f"{'above' if sc['bias'] > 0 else 'below'} G.", ""]
    # Q3: make's realised G against other actions in the same situation, weighted by make's updates per situation
    L += ["## Q3 — Does making pay more? Realised G of make minus other actions in the same situation "
          "(weighted by make's updates per situation)", "", "| era | situations with make | make updates | "
          "G(make) − G(others), within situation [95%] |", "|---|---|---|---|"]
    for e, name in enumerate(ERAS):
        mk = np.zeros((len(rs), 32, 2))
        ot = np.zeros((len(rs), 32, 2))
        for wi, r in enumerate(rs):
            for ctx in range(32):
                c = cell(r, f"{e}|{ctx}|make")
                mk[wi, ctx] = (c[J["n"]], c[J["G"]])
                for a in acts:
                    if a != "make":
                        c2 = cell(r, f"{e}|{ctx}|{a}")
                        ot[wi, ctx] += (c2[J["n"]], c2[J["G"]])

        def q3(wts):
            m = np.tensordot(wts, mk, axes=(1, 0))      # reps x ctx x 2
            o = np.tensordot(wts, ot, axes=(1, 0))
            with np.errstate(divide="ignore", invalid="ignore"):
                d = m[..., 1] / m[..., 0] - o[..., 1] / o[..., 0]
            w = np.where(np.isfinite(d), m[..., 0], 0.0)
            d = np.where(np.isfinite(d), d, 0.0)
            return (w * d).sum(-1) / w.sum(-1)
        point = q3(np.ones((1, len(rs))))[0]
        nctx = int(((mk[:, :, 0].sum(0) > 0) & (ot[:, :, 0].sum(0) > 0)).sum())
        reps = np.concatenate([q3(W[k:k + 1000]) for k in range(0, REPS, 1000)])
        L.append(f"| {name} | {nctx} | {mk[:, :, 0].sum():.0f} | {point:+.3f} {ci(reps)} |")
    L.append("")
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
