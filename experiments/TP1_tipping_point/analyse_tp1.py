"""TP1 analysis (questions.md, frozen as `TP1-frozen`). Read-only: reads saved control worlds.

  python experiments/TP1_tipping_point/analyse_tp1.py discovery   -> results_discovery.md (commit before the holdout)
  python experiments/TP1_tipping_point/analyse_tp1.py holdout     -> results_holdout.md (needs results_discovery.md)
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "NV2_nature_v2"))
sys.path.insert(0, str(EXP / "F1_baseline_fragility"))
from analyse_nv2 import died  # noqa: E402  (the extinction rule every study uses)

SETS = {"discovery": [EXP / "RT1_residence_time" / "output_rt1b", EXP / "FX2_embedded_food" / "output"],
        "holdout": [EXP / "FX3_gentler_embedded" / "output"]}
SEEDS = {"discovery": list(range(5701, 5957)) + list(range(6001, 6257)), "holdout": list(range(7301, 7557))}
YEARS = (20, 30, 40, 50, 60)
KEYS = ("women", "n", "women_single_no_mate")


def load(name):
    rows = []
    for d in SETS[name]:
        for f in sorted(d.glob("c_seed_*.json")):
            s = int(re.search(r"(\d+)", f.stem.split("_seed_")[1]).group(1))
            if s in SEEDS[name]:
                rows.append(json.loads(f.read_text(encoding="utf-8")))
    return rows


def curve(rows, key):
    c = defaultdict(lambda: [0, 0])                 # value -> [world-years, of which died out]
    for r in rows:
        d = died(r)
        for t in YEARS:
            snap = r.get("years", {}).get(str(t))
            if not snap or not snap.get("n"):
                continue
            v = int(snap.get(key, 0))
            c[v][0] += 1
            c[v][1] += d
    return dict(sorted(c.items()))


def cum(c, lo=None, hi=None):
    n = k = 0
    for v, (a, b) in c.items():
        if (lo is None or v >= lo) and (hi is None or v <= hi):
            n += a
            k += b
    return (k / n if n else None), n


def tipping(c):
    for w in sorted(c):
        below, nb = cum(c, hi=w)
        above, na = cum(c, lo=w + 3)
        if below is not None and above is not None and below >= 0.9 and above <= 0.5:
            return w, below, nb, above, na
    return None


def table(c, label):
    L = [f"| {label} | world-years | died out later |", "|---|---|---|"]
    for v, (a, b) in c.items():
        L.append(f"| {v} | {a} | {b / a:.0%} |")
    return L


def main(name):
    rows = load(name)
    n_expected = len(SEEDS[name])
    L = [f"# TP1 — tipping point: {name} results", "", "Frozen as `TP1-frozen`. analyse_tp1.py.", "",
         f"Worlds read: **{len(rows)} of {n_expected}**; died out before year 120: {sum(died(r) for r in rows)}.", ""]
    if len(rows) != n_expected:
        L.append("**Not valid: worlds missing; no outcome is shown.**")
    else:
        cw = curve(rows, "women")
        tp = tipping(cw)
        L += ["## The curve (fertile women at a check year, pooled over years 20, 30, 40, 50, 60)", ""] + \
            table(cw, "fertile women (W)") + [""]
        if name == "discovery":
            if tp:
                w, b, nb, a, na = tp
                L += [f"**Tipping point: W* = {w}.** Worlds with W ≤ {w} died out in {b:.0%} of {nb} world-years; "
                      f"worlds with W ≥ {w + 3} in {a:.0%} of {na}."]
            else:
                L += ["**No sharp threshold** (no W meets both conditions)."]
            meet = [w for w in sorted(cw) if (lambda b, a: b[0] is not None and a[0] is not None
                                              and b[0] >= 0.9 and a[0] <= 0.5)(cum(cw, hi=w), cum(cw, lo=w + 3))]
            L += ["", f"Described (not the reading): every W meeting both conditions: {meet}."]
        else:
            disc = (HERE / "results_discovery.md").read_text(encoding="utf-8")
            m = re.search(r"Tipping point: W\* = (\d+)", disc)
            if not m:
                L += ["Discovery found no sharp threshold; nothing to confirm. Holdout described only."]
            else:
                w = int(m.group(1))
                b, nb = cum(cw, hi=w)
                a, na = cum(cw, lo=w + 3)
                stands = b is not None and a is not None and b >= 0.8 and a <= 0.5
                L += [f"Discovery's W* = {w}. Holdout: W ≤ {w} died out in {b:.0%} of {nb} world-years; "
                      f"W ≥ {w + 3} in {a:.0%} of {na}. **{'Stands.' if stands else 'Not confirmed.'}**"]
        L += ["", "## Described", ""]
        for key, label in (("n", "population (all ages)"), ("women_single_no_mate", "single fertile women with no eligible man alive")):
            c = curve(rows, key)
            if key == "n":
                bins = defaultdict(lambda: [0, 0])
                for v, (a, b) in c.items():
                    lo = (v // 5) * 5
                    bins[lo][0] += a
                    bins[lo][1] += b
                L += [f"| {label} | world-years | died out later |", "|---|---|---|"] + \
                    [f"| {lo}–{lo + 4} | {a} | {b / a:.0%} |" for lo, (a, b) in sorted(bins.items())] + [""]
            else:
                L += table(c, label) + [""]
    text = "\n".join(L) + "\n"
    (HERE / f"results_{name}.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


def audit():
    """Described checks added after GPT's review (not part of the frozen reading): one row per world at each check
    year separately, and W within bands of total population (pooled world-years)."""
    def cell(k, n):
        return f"{k}/{n} ({k / n:.0%})" if n else "–"
    L = ["# TP1 — audit after GPT's review (described; not the frozen reading)", "",
         "Added after the frozen reading and the holdout were committed. analyse_tp1.py audit.", ""]
    wb = [(0, 0), (1, 1), (2, 3), (4, 6), (7, 99)]
    wl = ["0", "1", "2–3", "4–6", "7+"]
    for name in ("discovery", "holdout"):
        rows = load(name)
        L += [f"## {name.capitalize()}: one row per world, each check year separately (died out / worlds alive)", "",
              "| year | " + " | ".join(f"W {x}" for x in wl) + " |", "|---" * (len(wl) + 1) + "|"]
        for t in YEARS:
            c = [[0, 0] for _ in wb]
            for r in rows:
                s = r.get("years", {}).get(str(t))
                if not s or not s.get("n"):
                    continue
                w = int(s["women"])
                i = next(j for j, (lo, hi) in enumerate(wb) if lo <= w <= hi)
                c[i][0] += 1
                c[i][1] += died(r)
            L.append(f"| {t} | " + " | ".join(cell(k, n) for n, k in c) + " |")
        pb = [(0, 9), (10, 19), (20, 34), (35, 999)]
        pl = ["under 10", "10–19", "20–34", "35+"]
        g = {(i, j): [0, 0] for i in range(len(pb)) for j in range(len(wb))}
        for r in rows:
            d = died(r)
            for t in YEARS:
                s = r.get("years", {}).get(str(t))
                if not s or not s.get("n"):
                    continue
                i = next(a for a, (lo, hi) in enumerate(pb) if lo <= int(s["n"]) <= hi)
                j = next(a for a, (lo, hi) in enumerate(wb) if lo <= int(s["women"]) <= hi)
                g[(i, j)][0] += 1
                g[(i, j)][1] += d
        L += ["", f"## {name.capitalize()}: W within bands of total population (pooled world-years; died out / world-years)",
              "", "| population | " + " | ".join(f"W {x}" for x in wl) + " |", "|---" * (len(wl) + 1) + "|"]
        for i, lab in enumerate(pl):
            L.append(f"| {lab} | " + " | ".join(cell(g[(i, j)][1], g[(i, j)][0]) for j in range(len(wb))) + " |")
        L.append("")
    text = "\n".join(L) + "\n"
    (HERE / "results_audit.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    audit() if sys.argv[1] == "audit" else main(sys.argv[1])
