"""SA1-F analysis in the frozen order (followup_questions.md, `SA1F-frozen`). Written and smoke-tested before any data.

- Each arm against C, paired by seed: exact sign test; effect = C's extinction share minus the arm's; 95% bootstrap
  (10,000 resamples, random.Random(2026)); Holm over the seven. Yardstick: half of F2's effect on F1's seeds (0.117,
  recomputed from F1's and F2's saved files exactly as SA1 does; not re-estimated on the new seeds).
- Readings: sensitive (p < 0.05, |effect| > yardstick); moves survival (p < 0.05, |effect| <= yardstick); no meaningful
  effect (p >= 0.05, interval inside +-yardstick); otherwise no sign at this sample.
- Two tables: the four sensitive settings, then the three near the line. Beside each: SA1's 64-world effect and interval;
  "agrees" if SA1's point effect lies inside the new interval.
- No outcome is shown if the run is not valid.

  python experiments/SA1_sensitivity/analyse_sa1f.py            # main run (writes results_f.md)
  python experiments/SA1_sensitivity/analyse_sa1f.py --smoke    # smoke outputs only
"""
from __future__ import annotations

import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.stdout.reconfigure(encoding="utf-8")
import analyse_sa1 as A1  # noqa: E402
from analyse_sa1 import A, EXP, boot, ext_file, holm, load, sign_test, tool_share, world_tool_share  # noqa: E402
from analyse_mc1l import F1_SEEDS  # noqa: E402

SENSITIVE = [("perception", "perception_lo", "2"), ("perception", "perception_hi", "8"), ("reach", "reach_hi", "6"),
             ("mortality_base", "mortality_hi", "3.0e-5")]
NEAR = [("forage_base", "forage_lo", "6"), ("conception_chance", "conception_lo", "0.02"), ("reach", "reach_lo", "2")]
SEEDS = tuple(range(4301, 4557))


def compare(C, X, seeds):
    saved = sum(1 for s in seeds if C[s]["extinct"] and not X[s]["extinct"])
    lost = sum(1 for s in seeds if not C[s]["extinct"] and X[s]["extinct"])
    d = [int(C[s]["extinct"]) - int(X[s]["extinct"]) for s in seeds]
    return saved, lost, sign_test(saved, lost), sum(d) / len(d), *boot(d)


def main(out=HERE / "output_f", seeds=SEEDS, rows=None, base_out=HERE / "output", write=True):
    rows = rows or SENSITIVE + NEAR
    arms = ["c"] + [a for _, a, _ in rows] + ["s"]
    D = {a: load(out, seeds, a) for a in arms}
    L = []
    w = L.append
    w("# SA1-F — The sensitive and near-the-line settings on 256 new seeds: results\n")
    w(f"Frozen as `SA1F-frozen`. Control code (sham in `code_p2`); seeds {seeds[0]}–{seeds[-1]} ({len(seeds)}); 120 years.\n")
    z = out / "zero.txt"
    zero_ok = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    hashes = {}
    for R in D.values():
        for r in R.values():
            hashes.setdefault(r.get("code", "code_e13r"), set()).update({r["code_hash"], r["code_hash_after"]})
    ok_hash = all(len(v) == 1 for v in hashes.values())
    valid = zero_ok and ok_hash
    w("## Validity\n")
    w(f"- Zero check (observers leave the world unchanged; code_p2 with every setting off = the control code): **{'yes' if zero_ok else 'no'}**")
    w(f"- All {len(arms)} × {len(seeds)} worlds present: **yes**")
    w(f"- Code unchanged in every world (one fingerprint per code copy): **{'yes' if ok_hash else 'no'}**")
    w(f"\n**{'Valid.' if valid else 'NOT VALID: no outcome is shown.'}**\n")
    if not valid:
        text = "\n".join(L) + "\n"
        if write:
            (HERE / "results_f.md").write_text(text, encoding="utf-8")
        print(text)
        return
    n = len(seeds)
    ext = {a: sum(r["extinct"] for r in D[a].values()) for a in arms}
    f1 = sum(ext_file(EXP / "F1_baseline_fragility" / "output" / f"seed_{s}.json") for s in F1_SEEDS)
    f2 = sum(ext_file(EXP / "F2_perfect_search" / "output" / f"seed_{s}.json") for s in F1_SEEDS)
    half = (1 - f2 / f1) / 2 * f1 / len(F1_SEEDS)
    w("## Baseline (rule 14)\n")
    w(f"C died out in {ext['c']} of {n} worlds ({ext['c'] / n:.1%}). Yardstick (half of F2's effect on F1's seeds): **{half:.3f}**.\n")
    C = D["c"]
    res = [(name, arm, val, *compare(C, D[arm], seeds)) for name, arm, val in rows]
    adj = holm([r[5] for r in res])
    base = {}
    if base_out is not None:
        B = {a: load(base_out, F1_SEEDS, a) for a in ["c"] + [a for _, a, _ in rows]}
        base = {a: compare(B["c"], B[a], F1_SEEDS) for _, a, _ in rows}
    sham = compare(C, D["s"], seeds)
    for title, group in (("The four sensitive settings", SENSITIVE), ("The three near the line", NEAR)):
        sel = [(r, pa) for r, pa in zip(res, adj) if (r[0], r[1], r[2]) in group]
        if not sel:
            continue
        w(f"## {title} (the frozen reading)\n")
        w(f"| setting | value | died out (C: {ext['c']}) | saved / lost | p | Holm p | effect (C − arm) | 95% interval | reading | SA1 (64 worlds) | against SA1 |")
        w("|---|---|---|---|---|---|---|---|---|---|---|")
        for (name, arm, val, sv, ls, p, eff, lo, hi), pa in sel:
            if p < 0.05 and abs(eff) > half:
                r = "**sensitive**"
            elif p < 0.05:
                r = "moves survival"
            elif -half < lo and hi < half:
                r = "**no meaningful effect**"
            else:
                r = "no sign at this sample"
            if p < 0.05 and pa >= 0.05:
                r += " (does not survive Holm)"
            if arm in base:
                b = base[arm]
                bt = f"{b[3]:+.3f} [{b[4]:+.3f}, {b[5]:+.3f}]"
                ag = "agrees" if lo <= b[3] <= hi else "**differs**"
            else:
                bt, ag = "—", "—"
            w(f"| `{name}` | {val} | {ext[arm]} | {sv} / {ls} | {p:.3g} | {pa:.3g} | {eff:+.3f} | [{lo:+.3f}, {hi:+.3f}] | {r} | {bt} | {ag} |")
        w("")
    ss, sl, sp, se, sa, sb = sham
    w(f"Sham against C: died out {ext['s']} vs {ext['c']}; {ss} / {sl}; p = {sp:.3g}; effect {se:+.3f} [{sa:+.3f}, {sb:+.3f}]"
      + (" — **caveat (frozen): the sham reached p < 0.05; every reading carries it.**" if sp < 0.05 else " (quiet)."))
    w("\n## Beside them (population first, rule 18)\n")
    w("| arm | median population, year 119 | births per woman-year | decisions blocked for want of a partner | tools' share of foraged food (E8.2, upper bound) |")
    w("|---|---|---|---|---|")
    from scipy.stats import wilcoxon
    for a in arms:
        R = D[a]
        end = lambda r: (r["E"] + 1) if r["extinct"] else 120  # noqa: E731
        rate = A.rates(None, [(r, 0, end(r)) for r in R.values()])
        pop = statistics.median(r["Y"].get(119, {}).get("n", 0) for r in R.values())
        extra = ""
        if a != "c":
            diffs = [y - x for x, y in ((world_tool_share(C[s]), world_tool_share(R[s])) for s in seeds)
                     if x is not None and y is not None and y != x]
            try:
                extra = f" (Wilcoxon p {wilcoxon(diffs).pvalue:.3g})" if diffs else ""
            except ValueError:
                extra = ""
        w(f"| {a} | {pop:.0f} | {A.fmt(rate.get('births_per_woman_year'))} | {A.fmt(rate.get('block_no_partner'))} | "
          f"{tool_share(R):.3f}{extra} |")
    text = "\n".join(L) + "\n"
    if write:
        (HERE / "results_f.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        main(out=HERE / "output_f_smoke", seeds=(9701, 9702),
             rows=[("perception", "perception_lo", "2"), ("forage_base", "forage_lo", "6")], base_out=HERE / "output",
             write=False)
    else:
        main()
