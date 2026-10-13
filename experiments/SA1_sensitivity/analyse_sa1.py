"""SA1 analysis in the frozen order (questions.md, `SA1-frozen`). Written and smoke-tested before any main-run data.

Operational details (written before data):
- Extinct, as every study: the world does not reach year 120 with someone alive (12 decade marks, the last above 0).
- Each sweep arm against C (the control re-run), paired by seed; exact two-sided sign test on worlds that differ;
  effect = C's extinction share minus the arm's (positive = fewer extinctions in the arm); 95% percentile bootstrap,
  10,000 resamples, random.Random(2026); Holm adjustment over the 12 sweep comparisons.
- Reading (decision rules): sensitive = p < 0.05 and |effect| > 0.117 (half of F2's effect on F1's seeds, recomputed
  here); moves survival = p < 0.05 and |effect| <= 0.117; otherwise "no sign at this sample" (never "robust").
- Secondary, pooled per arm: median population at year 119; births per woman-year and decisions blocked for want of a
  partner (F1's rates); tools' share of foraged food (E8.2's upper bound), with the paired Wilcoxon p against C.

  python experiments/SA1_sensitivity/analyse_sa1.py            # main run (writes results.md)
  python experiments/SA1_sensitivity/analyse_sa1.py --smoke    # smoke outputs only
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "F1_baseline_fragility"))
sys.path.insert(0, str(EXP / "MC1L_moving_camp_large"))
import analyse_f1 as A  # noqa: E402
from analyse_mc1l import F1_SEEDS, ext_file, load, sign_test  # noqa: E402

SWEEP = [("conception_chance", "conception_lo", "conception_hi", "0.02", "0.08"),
         ("perception", "perception_lo", "perception_hi", "2", "8"),
         ("reach", "reach_lo", "reach_hi", "2", "6"),
         ("camp_radius", "camp_lo", "camp_hi", "1", "4"),
         ("mortality_base", "mortality_lo", "mortality_hi", "0.75e-5", "3.0e-5"),
         ("forage_base", "forage_lo", "forage_hi", "6", "24")]


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, run = [0.0] * len(ps), 0.0
    for k, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - k) * ps[i]))
        adj[i] = run
    return adj


def boot(d):
    rng = random.Random(2026)
    b = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(10000))
    return b[249], b[9749]


def tool_share(R):
    got = sum(r["e82"]["forage"].get("food_foraged", 0.0) for r in R.values())
    ub = sum(r["e82"]["forage"].get("food_from_tools_ub", 0.0) for r in R.values())
    return ub / got if got else float("nan")


def world_tool_share(r):
    f = r["e82"]["forage"]
    return f.get("food_from_tools_ub", 0.0) / f["food_foraged"] if f.get("food_foraged") else None


def main(out=HERE / "output", seeds=F1_SEEDS, arms=None, write=True):
    arms = arms or ["c"] + [a for row in SWEEP for a in row[1:3]] + ["s"]
    D = {a: load(out, seeds, a) for a in arms}
    L = []
    w = L.append
    w("# SA1 — Sensitivity audit: results\n")
    w(f"Frozen as `SA1-frozen`. Control code; F1's {len(seeds)} seeds; 120 years; one setting changed per arm.\n")
    z = out / "zero.txt"
    cc = out / "control_check.txt"
    zero_ok = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    ctrl_ok = cc.exists() and "All: PASS" in cc.read_text(encoding="utf-8")
    hashes, ok_hash = {}, True     # one fingerprint per code copy (the sham runs in code_p2), unchanged in every world
    for R in D.values():
        for r in R.values():
            hashes.setdefault(r.get("code", "code_e13r"), set()).update({r["code_hash"], r["code_hash_after"]})
    ok_hash = all(len(v) == 1 for v in hashes.values())
    valid = zero_ok and ctrl_ok and ok_hash
    w("## Validity\n")
    w(f"- Zero check (observers leave the world unchanged): **{'yes' if zero_ok else 'no'}**")
    w(f"- Control re-run reproduces F1's saved populations on every seed: **{'yes' if ctrl_ok else 'no'}**")
    w(f"- Code unchanged in every world (one fingerprint per code copy): **{'yes' if ok_hash else 'no'}**")
    w(f"\n**{'Valid.' if valid else 'NOT VALID: no reading is made.'}**\n")
    ext = {a: sum(r["extinct"] for r in D[a].values()) for a in arms}
    n = len(seeds)
    f1 = sum(ext_file(EXP / "F1_baseline_fragility" / "output" / f"seed_{s}.json") for s in F1_SEEDS)
    f2 = sum(ext_file(EXP / "F2_perfect_search" / "output" / f"seed_{s}.json") for s in F1_SEEDS)
    half = (1 - f2 / f1) / 2 * f1 / len(F1_SEEDS)
    w("## Baseline (rule 14)\n")
    w(f"C (control re-run) died out in {ext['c']} of {n} worlds ({ext['c'] / n:.1%}). Half of F2's effect: **{half:.3f}**.\n")
    rows, ps = [], []
    C = D["c"]
    for name, lo, hi, vlo, vhi in SWEEP:
        for arm, val in ((lo, vlo), (hi, vhi)):
            if arm not in D:
                continue
            X = D[arm]
            saved = sum(1 for s in seeds if C[s]["extinct"] and not X[s]["extinct"])
            lost = sum(1 for s in seeds if not C[s]["extinct"] and X[s]["extinct"])
            d = [int(C[s]["extinct"]) - int(X[s]["extinct"]) for s in seeds]
            p = sign_test(saved, lost)
            rows.append((name, val, arm, saved, lost, p, sum(d) / n, *boot(d)))
            ps.append(p)
    adj = holm(ps) if ps else []
    w("## Extinction, each setting against the control (the frozen reading)\n")
    w(f"| setting | value | died out (C: {ext['c']}) | saved / lost | p | Holm p | effect (C − arm) | 95% interval | reading |")
    w("|---|---|---|---|---|---|---|---|---|")
    for (name, val, arm, sv, ls, p, eff, lo_, hi_), pa in zip(rows, adj):
        if not valid:
            r = "not read"
        elif p < 0.05 and abs(eff) > half:
            r = "**sensitive**"
        elif p < 0.05:
            r = "moves survival"
        else:
            r = "no sign at this sample"
        if valid and p < 0.05 and pa >= 0.05:
            r += " (does not survive Holm)"
        w(f"| `{name}` | {val} | {ext[arm]} | {sv} / {ls} | {p:.3g} | {pa:.3g} | {eff:+.3f} | [{lo_:+.3f}, {hi_:+.3f}] | {r} |")
    if "s" in D:
        S = D["s"]
        ss = sum(1 for s in seeds if C[s]["extinct"] and not S[s]["extinct"])
        sl = sum(1 for s in seeds if not C[s]["extinct"] and S[s]["extinct"])
        sp = sign_test(ss, sl)
        ds = [int(C[s]["extinct"]) - int(S[s]["extinct"]) for s in seeds]
        a_, b_ = boot(ds)
        w(f"\nSham against C: died out {ext['s']} vs {ext['c']}; {ss} / {sl}; p = {sp:.3g}; effect {sum(ds) / n:+.3f} "
          f"[{a_:+.3f}, {b_:+.3f}]" + (" — **caveat (frozen): the sham reached p < 0.05.**" if sp < 0.05 else "."))
    w("\n## Beside them (population first, rule 18)\n")
    w("| arm | median population, year 119 | births per woman-year | decisions blocked for want of a partner | tools' share of foraged food (E8.2, upper bound) |")
    w("|---|---|---|---|---|")
    from scipy.stats import wilcoxon
    for a in arms:
        R = D[a]
        end = lambda r: (r["E"] + 1) if r["extinct"] else 120  # noqa: E731
        rate = A.rates(None, [(r, 0, end(r)) for r in R.values()])
        pop = statistics.median(r["Y"].get(119, {}).get("n", 0) for r in R.values())
        ts = tool_share(R)
        extra = ""
        if a != "c":
            pairs = [(world_tool_share(C[s]), world_tool_share(R[s])) for s in seeds]
            diffs = [y - x for x, y in pairs if x is not None and y is not None and y != x]
            try:
                extra = f" (Wilcoxon p {wilcoxon(diffs).pvalue:.3g})" if diffs else ""
            except ValueError:
                extra = ""
        w(f"| {a} | {pop:.0f} | {A.fmt(rate.get('births_per_woman_year'))} | {A.fmt(rate.get('block_no_partner'))} | "
          f"{ts:.3f}{extra} |")
    text = "\n".join(L) + "\n"
    if write:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        main(out=HERE / "output_smoke", seeds=(501, 502), arms=["c", "forage_lo", "s"], write=False)
    else:
        main()
