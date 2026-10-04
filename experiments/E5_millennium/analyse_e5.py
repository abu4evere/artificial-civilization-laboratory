"""E5 analysis: apply the frozen definitions in predictions.md. Read-only. Writes results.md."""
from __future__ import annotations

import json
import statistics
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
GENES = ("curiosity", "diligence", "sociability", "kindness", "temper", "anxiety", "care", "boldness")
BARS = "▁▂▃▄▅▆▇█"


def spark(vals):
    top = max(vals) if vals else 0
    return "".join(BARS[min(7, int(v / top * 7.999))] if v else "·" for v in vals) if top else "·" * len(vals)


def longest_stretch(rows, key_of, cond):
    """Longest run of consecutive decade samples where `cond` holds for the same key. Returns (samples, key, start year)."""
    best = (0, None, None)
    current = {}
    for row in rows:
        now = {}
        for item in key_of(row):
            k, ok = item
            if ok:
                start, n = current.get(k, (row["year"], 0))
                now[k] = (start, n + 1)
                if n + 1 > best[0]:
                    best = (n + 1, k, start)
        current = now
    return best


def main():
    runs = []
    for f in sorted(OUT.glob("seed_*.json")):
        runs.append(json.loads(f.read_text(encoding="utf-8")))
    L = ["# E5 — A thousand years · Results", ""]
    w = L.append
    w(f"{len(runs)} worlds, current code, every feature frozen. Definitions and predictions were frozen in "
      "predictions.md before the run. A 'sample' is one 10-year measurement.")
    w("")
    w("## Population and populated islands over 1000 years")
    w("")
    w("```")
    for r in runs:
        rows = r["divergence"]
        pops = [x["population"] for x in rows] + [0] * (100 - len(rows))
        isl = [len(x["islands"]) for x in rows] + [0] * (100 - len(rows))
        w(f"seed {r['seed']}  people {spark(pops)}  peak {max(pops):>3}   ended: "
          + (f"died out in year {r['years_run']}" if r["extinct"] else f"{rows[-1]['population']} alive at year 1000"))
        w(f"           islands {''.join(str(min(9, v)) for v in isl)}")
    w("```")
    w("(Islands: how many islands held 5 or more people, one digit per 10 years.)")
    w("")
    dead = [r for r in runs if r["extinct"]]
    alive = [r for r in runs if not r["extinct"]]
    multi_share = {}
    for r in runs:
        rows = r["divergence"]
        multi_share[r["seed"]] = sum(1 for x in rows if len(x["islands"]) >= 2) / max(1, len(rows))
    w("## The definitions, applied")
    w("")
    w("| seed | lived | samples with 2+ populated islands | longest distinct-people stretch | longest distinct-culture stretch | longest tradition | longest rival-identity stretch |")
    w("|---|---|---|---|---|---|---|")
    results = {}
    for r in runs:
        rows = r["divergence"]

        def gene_pairs(row):
            return [((p["a"], p["b"]), p["traits_gap_over_spread"] >= 3) for p in row["pairs"]]

        def culture_pairs(row):
            out = []
            for p in row["pairs"]:
                ds = [p[k] for k in ("tech_distance", "belief_distance", "symbol_distance") if p[k] is not None]
                out.append(((p["a"], p["b"]), bool(ds) and max(ds) > 0.5))
            return out

        def traditions(row):
            return [(t, True) for t in row["traditions"]]

        def rivalry(row):
            i = row["identity"]
            ok = (i["trust_other"] is not None and i["ties_other"] >= 5 and i["trust_own"] is not None
                  and i["trust_own"] - i["trust_other"] >= 0.2)
            return [("world", ok)]
        g = longest_stretch(rows, gene_pairs, None)
        cu = longest_stretch(rows, culture_pairs, None)
        tr = longest_stretch(rows, traditions, None)
        rv = longest_stretch(rows, rivalry, None)
        # did the longest tradition outlive everyone alive when it began?
        outlived = None
        if tr[1] is not None:
            end_year = tr[2] + 10 * (tr[0] - 1)
            end_row = next((x for x in rows if x["year"] == end_year), None)
            if end_row and end_row["oldest_alive_birth"] is not None:
                outlived = end_row["oldest_alive_birth"] > (tr[2] - 10) * 52
        results[r["seed"]] = {"gene": g, "culture": cu, "tradition": tr, "outlived": outlived, "rival": rv}
        fmt = lambda s: f"{10 * s[0]} yrs" if s[0] else "none"  # noqa: E731
        trad = f"{10 * tr[0]} yrs: `{tr[1]}`" + (" (outlived its founders)" if outlived else "") if tr[0] else "none"
        w(f"| {r['seed']} | {r['years_run']} yrs | {100 * multi_share[r['seed']]:.0f}% | {fmt(g)} | {fmt(cu)} | {trad} | {fmt(rv)} |")
    w("")
    # genes over time
    gaps, spreads = [], []
    for r in runs:
        for row in r["divergence"]:
            for p in row["pairs"]:
                gaps.append((row["year"], statistics.mean(p["gene_gaps"].values())))
            for isl in row["per_island"].values():
                spreads.append((row["year"], statistics.mean(isl["spread"].values())))
    w("## Genes over time (all worlds pooled)")
    w("")
    w("| years | mean trait gap between islands | spread of a trait within an island | samples with 2+ islands |")
    w("|---|---|---|---|")
    for lo in range(0, 1000, 100):
        g_ = [v for y, v in gaps if lo < y <= lo + 100]
        s_ = [v for y, v in spreads if lo < y <= lo + 100]
        w(f"| {lo + 1}–{lo + 100} | {statistics.mean(g_):.3f} | {statistics.mean(s_):.3f} | {len(g_)} |" if g_ else
          f"| {lo + 1}–{lo + 100} | – | {statistics.mean(s_):.3f} | 0 |" if s_ else f"| {lo + 1}–{lo + 100} | – | – | 0 |")
    w("")
    # score
    w("## Frozen predictions, scored")
    w("")
    w(f"1. At least 3 of 8 die out: {len(dead)} died out ({', '.join(str(r['seed']) for r in dead) or 'none'}). "
      f"**{'confirmed' if len(dead) >= 3 else 'wrong'}**")
    shares = [multi_share[r["seed"]] for r in alive]
    ok2 = bool(alive) and sum(1 for s in shares if s < 0.25) > len(alive) / 2
    w(f"2. Surviving worlds hold 2+ populated islands less than 25% of the time: "
      f"{', '.join(f'{100 * s:.0f}%' for s in shares) or 'no survivors'}. **{'confirmed' if ok2 else 'wrong'}**")
    distinct = [s for s, v in results.items() if v["gene"][0] >= 10]
    w(f"3. No distinct people: worlds with one (100+ years): {', '.join(map(str, distinct)) or 'none'}. "
      f"**{'confirmed' if not distinct else 'wrong'}**")
    late = [v for y, v in spreads if y > 200]
    w(f"4. Within-island spread stays at the floor (0.10–0.11): mean after year 200 = "
      f"{statistics.mean(late):.3f}. **{'confirmed' if late and 0.09 <= statistics.mean(late) <= 0.12 else 'wrong'}**")
    cult = [s for s, v in results.items() if v["culture"][0] >= 10]
    w(f"5. A distinct culture (100+ years) in at least one world: {', '.join(map(str, cult)) or 'none'}. "
      f"**{'confirmed' if cult else 'wrong'}**")
    trad_ok = [s for s, v in results.items() if v["tradition"][0] >= 30 and v["outlived"]]
    surv = [r["seed"] for r in alive]
    w(f"6. A 300+ year tradition that outlived its founders in at least half the surviving worlds: "
      f"{', '.join(map(str, trad_ok)) or 'none'} of surviving {', '.join(map(str, surv)) or 'none'}. "
      f"**{'confirmed' if surv and len([s for s in trad_ok if s in surv]) >= len(surv) / 2 else 'wrong'}**")
    rival = [s for s, v in results.items() if v["rival"][0] >= 10]
    w(f"7. No rival identity: worlds with one: {', '.join(map(str, rival)) or 'none'}. "
      f"**{'confirmed' if not rival else 'wrong'}**")
    w("")
    w("## Longest-lived traditions, per world")
    w("")
    for r in runs:
        rows = r["divergence"]
        stretches = {}
        current = {}
        for row in rows:
            now = {}
            for t in row["traditions"]:
                start, n = current.get(t, (row["year"], 0))
                now[t] = (start, n + 1)
                if n + 1 > stretches.get(t, (0, 0))[0]:
                    stretches[t] = (n + 1, start)
            current = now
        top = sorted(stretches.items(), key=lambda kv: -kv[1][0])[:4]
        w(f"- seed {r['seed']}: " + "; ".join(f"`{k}` {10 * n} years from year {st}" for k, (n, st) in top))
    (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("wrote", HERE / "results.md")


if __name__ == "__main__":
    main()
