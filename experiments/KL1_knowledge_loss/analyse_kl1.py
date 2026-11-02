"""KL1 analysis, written before any data (questions.md, frozen as `KL1-frozen`).

The zero checks run on GitHub while the creator is using the PC (light use); their record is `zero_cloud.log` (saved
from the cloud zero job's log), or `zero_local.log` when run locally.

  python experiments/KL1_knowledge_loss/analyse_kl1.py            # writes results.md
  python experiments/KL1_knowledge_loss/analyse_kl1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_kl1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261101)
D_LINE, R_LINE, MIN_REV = 0.5, 0.10, 30


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {}
    for f in sorted(glob.glob(str(OUTDIR / "k_seed_*.json"))):
        r = json.load(open(f))
        runs[r["seed"]] = r
    zero = ""
    for name in ("zero_cloud.log", "zero_local.log"):
        if (HERE / name).exists():
            zero = (HERE / name).read_text(encoding="utf-8", errors="replace")
            break
    R.base.setup(R.CODE)
    fp_now = R.base.fingerprint(R.CODE)
    m = re.search(r"fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    want = sorted(R.SEEDS) if not SMOKE else sorted(runs)
    present = sorted(runs) == want and len(want) > 0
    fps = {r["code_hash"] for r in runs.values()} | {r["code_hash_after"] for r in runs.values()}
    mism = sum(sum(r["mismatch"].values()) for r in runs.values())
    ok = bool(zero_ok and present and fps == {fp_now} and mism == 0)
    L = ["# KL1 — Does know-how outlive its holders? Results", "",
         "Frozen as `KL1-frozen`. run_kl1.py, analyse_kl1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks (All: PASS, same `code_v11` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(runs)} of {len(want)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_v11`'s: **{'yes' if fps == {fp_now} else 'NO'}**",
         f"- The observer's record of who knows what, and of losses and revivals, matches the world (mismatches 0): "
         f"**{'yes' if mism == 0 else f'NO ({mism})'}**",
         "", f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    seeds = sorted(runs)
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def wl(s, mk=None, j=None):
        v = runs[s]["world_losses"]
        rows = [v[k] for k in v if mk is None or k == mk]
        return sum(row[j] for row in rows) if j is not None else sum(sum(row) for row in rows)

    def rev(s, mk, path=None):
        v = runs[s]["revivals"].get(mk, {})
        return v.get(path, 0) if path is not None else sum(v.values())

    def ratio(num, den):
        num, den = np.asarray(num, float), np.asarray(den, float)
        if den.sum() == 0:
            return None, None, None
        with np.errstate(invalid="ignore", divide="ignore"):
            bs = (W @ num) / (W @ den)
        bs = bs[np.isfinite(bs)]
        return num.sum() / den.sum(), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))

    def fmt(t):
        return "n/a" if t[0] is None else f"{t[0]:.4f} [{t[1]:.4f}, {t[2]:.4f}]"
    death = [wl(s, None, 0) for s in seeds]
    allw = [wl(s) for s in seeds]
    D = ratio(death, allw)
    mk_read = [rev(s, "1", "read") for s in seeds]
    mk_all = [rev(s, "1") for s in seeds]
    Rm = ratio(mk_read, mk_all)
    loss_reading = "n/a" if D[0] is None else ("death is the main road of loss" if D[0] >= D_LINE else "forgetting is")
    if sum(mk_all) < MIN_REV or Rm[0] is None:
        mark_reading = "too few to judge"
    else:
        mark_reading = "marks revive lost know-how" if Rm[0] >= R_LINE else "marks do not (yet)"
    L += ["## Primary (frozen)", "",
          "| quantity | value [95%] | count |", "|---|---|---|",
          f"| **D**: share of world-level losses by death | **{fmt(D)}** | {int(sum(death)):,} of {int(sum(allw)):,} |",
          f"| **R_markable**: share of markable revivals through marks | **{fmt(Rm)}** | {int(sum(mk_read)):,} of "
          f"{int(sum(mk_all)):,} |", "",
          f"Readings: loss, death is the main road if D >= {D_LINE}, otherwise forgetting is; marks revive lost know-how "
          f"if R_markable >= {R_LINE}, marks do not (yet) if below, too few to judge under {MIN_REV} markable "
          "revivals.", "",
          f"**Reading (loss): {loss_reading}.**", "", f"**Reading (marks): {mark_reading}.**", ""]

    L += ["## Secondary (described, not decisive)", "",
          "### World-level losses by cause", "", "| kinds | death | forgetting | mixed |", "|---|---|---|---|"]
    for mk, name in (("1", "markable (strike)"), ("0", "other")):
        a = [sum(wl(s, mk, j) for s in seeds) for j in range(3)]
        t = sum(a)
        L.append(f"| {name} | {a[0]:,} ({a[0] / t:.3f}) | {a[1]:,} ({a[1] / t:.3f}) | {a[2]:,} ({a[2] / t:.3f}) |" if t
                 else f"| {name} | 0 | 0 | 0 |")
    L += ["", "### Revivals by path (re-invention is not preservation)", "",
          "| kinds | made | heated | read | taught with an error | copied with an error |", "|---|---|---|---|---|---|"]
    for mk, name in (("1", "markable (strike)"), ("0", "other")):
        c = Counter()
        for s in seeds:
            c.update(runs[s]["revivals"].get(mk, {}))
        L.append(f"| {name} | {c['made']:,} | {c['heated']:,} | {c['read']:,} | {c['taught_variant']:,} | "
                 f"{c['copied_variant']:,} |")
    g, ml = Counter(), Counter()
    for s in seeds:
        g.update(runs[s]["gain_paths"])
        ml.update(runs[s]["mind_losses"])
    tg, tl = sum(g.values()), sum(ml.values())
    L += ["", "### Gains of know-how by path (all kinds)", "", "| path | gains | share |", "|---|---|---|"]
    for p in R.PATHS:
        L.append(f"| {p} | {g[p]:,} | {g[p] / tg:.3f} |" if tg else f"| {p} | 0 | - |")
    L += ["", "### Losses from minds by cause", "", "| cause | losses | share |", "|---|---|---|"]
    for c in ("evicted", "forgotten", "death"):
        L.append(f"| {c} | {ml[c]:,} | {ml[c] / tl:.3f} |" if tl else f"| {c} | 0 | - |")
    ad = np.array([runs[s]["at_death"] for s in seeds]).sum(axis=0)
    life = np.concatenate([np.asarray(runs[s]["lifetimes"], float) for s in seeds]) if seeds else np.array([])
    cs = np.array([v for s in seeds for v in runs[s]["census"].values()], float)
    years = len(cs)
    L += ["", "### At a knower's death; lifetimes; knowers", "",
          f"- A dead knower's kinds that survive in someone living: {ad[0] / ad.sum():.3f} ({int(ad[0]):,} of "
          f"{int(ad.sum()):,})." if ad.sum() else "- A dead knower's kinds: none counted.",
          f"- Weeks a kind stayed known before a counted loss: median {np.median(life):.0f}, mean {life.mean():.0f} "
          f"(n {len(life):,})." if len(life) else "- Lifetimes: none counted.",
          f"- Yearly census: kinds alive per world-year {cs[:, 0].mean():.1f}; knowers per kind "
          f"{cs[:, 1].sum() / cs[:, 0].sum():.2f}; share of kinds with a single knower {cs[:, 2].sum() / cs[:, 0].sum():.3f}."
          if years and cs[:, 0].sum() else "- Census: none.",
          f"- `read` events per world-year: {sum(runs[s]['reads'] for s in seeds) / max(years, 1):.2f}.", ""]
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
