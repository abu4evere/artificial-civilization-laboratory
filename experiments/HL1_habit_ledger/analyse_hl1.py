"""HL1 analysis, written before any data (questions.md, frozen as `HL1-frozen`).

  python experiments/HL1_habit_ledger/analyse_hl1.py            # writes results.md
  python experiments/HL1_habit_ledger/analyse_hl1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_hl1 import BIN_EDGES, ROUTES, SEEDS, WPY  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261027)
BINS = [f"{BIN_EDGES[i]}-{BIN_EDGES[i + 1]}" for i in range(len(BIN_EDGES) - 1)]
EARLY, LATE = (0, 1), (5,)
if "--smoke-late" in sys.argv:
    LATE = (2,)
FAMS = ("forage", "give", "talk", "gather", "put", "join", "rest", "make")
N_CTX = 32


def ci(reps):
    reps = np.asarray([x for x in reps if np.isfinite(x)])
    if not len(reps):
        return "[-]"
    lo, hi = np.percentile(reps, [2.5, 97.5])
    return f"[{lo:.3g}, {hi:.3g}]"


def pooled(worlds, bins):
    out = defaultdict(Counter)
    for r in worlds:
        for k, c in r["cells"].items():
            b, hb, tool, fb = map(int, k.split("|"))
            if b in bins:
                out[(hb, tool, fb)].update(c)
    return out


def split(worlds):
    E, L = pooled(worlds, EARLY), pooled(worlds, LATE)
    states = [s for s in E if E[s]["offered"] > 0 and L[s]["offered"] > 0]
    wsum = sum(E[s]["offered"] for s in states)
    if not wsum:
        return None
    d = Counter()
    for s in states:
        w = E[s]["offered"] / wsum
        ne, nl = E[s]["offered"], L[s]["offered"]
        for k_ in ["hab_total"] + [f"hab_{r}" for r in ROUTES] + [f"make_{r}" for r in ROUTES]:
            d[k_ + "_e"] += w * E[s][k_] / ne
            d[k_ + "_l"] += w * L[s][k_] / nl
    d["states"] = len(states)
    for k_ in ["hab_total"] + [f"hab_{r}" for r in ROUTES] + [f"make_{r}" for r in ROUTES]:
        d[k_] = d[k_ + "_l"] - d[k_ + "_e"]
    d["residual"] = d["hab_total"] - sum(d[f"hab_{r}"] for r in ROUTES)
    return d


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rs = [json.load(open(f)) for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json")))]
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    fps = {r["code_hash"] for r in rs} | {r["code_hash_after"] for r in rs}
    mism = sum(sum(r["mismatch"].values()) for r in rs)
    ok = "All: PASS" in zero and sorted(r["seed"] for r in rs) == sorted(SEEDS) and len(fps) == 1 and mism == 0
    L = ["# HL1 — Where do the habits come from? Results", "",
         "Frozen as `HL1-frozen`. run_hl1.py, analyse_hl1.py (written before data).", "", "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({len(rs)} of {len(SEEDS)}): **{'yes' if sorted(r['seed'] for r in rs) == sorted(SEEDS) else 'NO'}**",
         f"- One fingerprint (`code_v7`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- The ledger closes, every TD update replays exactly, the Q1 split adds up (mismatches 0): "
         f"**{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    # Q1
    al = [r for r in rs if r["final_tick"] > BIN_EDGES[LATE[0]] * WPY]
    d = split(al)
    if d:
        reps = defaultdict(list)
        for row in RNG.integers(0, len(al), size=(REPS, len(al))):
            dd = split([al[k] for k in row])
            if dd is None:
                continue
            reps["hab_total"].append(dd["hab_total"])
            for r in ROUTES:
                reps[r].append(dd[f"hab_{r}"])
        L += ["## Q1 — Which route carries CO1's habit rise (primary)", "",
              f"Adults, weeks in which make was offered; early = years 0-10, late = years 100-200; worlds alive at year "
              f"{BIN_EDGES[LATE[0]]} ({len(al)}); {d['states']} matched states (hunger × tool × food), late weighted to "
              f"the early offered weeks.", "",
              f"- The habit part of the competing pull (Σ s_a·h_a): {d['hab_total_e']:.3f} → {d['hab_total_l']:.3f}; "
              f"**Δ = {d['hab_total']:+.3f} {ci(reps['hab_total'])}**.", "",
              "| route | early | late | Δ | share of the rise |", "|---|---|---|---|---|"]
        for r in ROUTES:
            L.append(f"| {r} | {d[f'hab_{r}_e']:.4f} | {d[f'hab_{r}_l']:.4f} | {d[f'hab_{r}']:+.4f} {ci(reps[r])} | "
                     f"{d[f'hab_{r}'] / d['hab_total']:.2f} |")
        L += [f"", f"(Exactness check: Δ minus the routes = {d['residual']:.2e}.)", ""]
        largest = max(ROUTES, key=lambda r: d[f"hab_{r}"] * np.sign(d["hab_total"]))
        L += [f"**The route carrying the largest share of the rise: {largest}.**", "",
              "Making's own habit term (0.6 × its habit value), by route: " + ", ".join(
                  f"{r} {d[f'make_{r}_e']:.5f} → {d[f'make_{r}_l']:.5f}" for r in ROUTES) + ".", ""]
    # Q2
    L += ["## Q2 — Raw flows: total change in habit values by route (summed over situations and people)", ""]
    tot = {i: Counter() for i in range(len(BINS))}
    for r in rs:
        for b, c in r["flows"].items():
            tot[int(b)].update(c)
    L += ["| bin | " + " | ".join(f"{f}: td / talk / carer / paid" for f in FAMS[:5]) + " | copying events | carer events |",
          "|---" * (3 + 5) + "|"]
    for i, name in enumerate(BINS):
        t = tot[i]
        cells = [f"{t[f'td_d:{f}']:.0f} / {t[f'talk_d:{f}']:.0f} / {t[f'carer_d:{f}']:.0f} / {t[f'paid_d:{f}']:.0f}"
                 for f in FAMS[:5]]
        L.append(f"| {name} | " + " | ".join(cells) + f" | {t['talk_n']:.0f} | {t['carer_n']:.0f} |")
    L.append("")
    # Q3
    L += ["## Q3 — Rich-get-richer (adults)", "",
          "| bin | action | chosen per adult-week | TD updates per adult-week | mean reward r | mean future | mean TD target | "
          "mean habit value |", "|---|---|---|---|---|---|---|---|"]
    for i, name in enumerate(BINS):
        t = tot[i]
        pw = t["adult_pw"] or float("nan")
        for f in ("forage", "give", "talk", "gather", "make"):
            n = t[f"atd_n:{f}"]
            mr = t[f"atd_r:{f}"] / n if n else float("nan")
            mf = t[f"atd_f:{f}"] / n if n else float("nan")
            mq = t[f"meanq:{f}"] / t["meanq_n"] if t["meanq_n"] else float("nan")
            L.append(f"| {name} | {f} | {t[f'chosen:{f}'] / pw:.4f} | {n / pw:.4f} | {mr:.3f} | {mf:.3f} | "
                     f"{mr + 0.8 * mf:.3f} | {mq:.4f} |")
    # rank association across worlds × families
    xs, ys = [], []
    for r in rs:
        e, l_ = Counter(), Counter()
        for b, c in r["flows"].items():
            (e if int(b) in (0, 1, 2) else l_ if int(b) == 5 else Counter()).update(c)
        if not e["adult_pw"] or not l_["meanq_n"] or not e["meanq_n"]:
            continue
        for f in FAMS:
            xs.append(e[f"chosen:{f}"] / e["adult_pw"])
            ys.append(l_[f"meanq:{f}"] / l_["meanq_n"] - e[f"meanq:{f}"] / e["meanq_n"])
    if len(xs) > 3:
        rx, ry = np.argsort(np.argsort(xs)), np.argsort(np.argsort(ys))
        L += ["", f"Rank association, across worlds × {len(FAMS)} families, of how often an action was chosen in years "
              f"0-20 with the growth of its mean habit value to years 100-200: **{np.corrcoef(rx, ry)[0, 1]:.2f}** "
              f"({len(xs)} pairs; described)."]
    all_t = Counter()
    for t in tot.values():
        all_t.update(t)
    L += ["", f"**The negative test (making, all bins):** change in its habit by own TD {all_t['td_d:make']:+.2f} "
          f"({all_t['td_n:make']:.0f} updates); by copying in talk {all_t['talk_d:make']:+.2f}; by carer "
          f"{all_t['carer_d:make']:+.2f}. Forage: TD {all_t['td_d:forage']:+.2f} ({all_t['td_n:forage']:.0f} updates); "
          f"talk {all_t['talk_d:forage']:+.2f}; carer {all_t['carer_d:forage']:+.2f}.", ""]
    # Q4
    L += ["## Q4 — Social amplification (copying in talk)", "",
          f"Copying events: {all_t['talk_n']:.0f}; for respect {all_t['talk_for_respect']:.0f}, for seeming happier "
          f"{all_t['talk_for_mood']:.0f}.", "",
          "| action | mean model − learner habit gap per copying event (per situation) | total change copied |",
          "|---|---|---|"]
    for f in FAMS:
        n = all_t["talk_n"]
        L.append(f"| {f} | {all_t[f'talk_gap:{f}'] / (n * N_CTX) if n else float('nan'):+.4f} | {all_t[f'talk_d:{f}']:+.1f} |")
    L.append("")
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
