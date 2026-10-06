"""V1 tables (questions.md), written before the V1 data existed. Writes findings_tables.md.

  python experiments/V1_bad_years/analyse_v1.py
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
SEEDS = tuple(range(501, 517))


def corr(a, b):
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if len(pairs) < 3:
        return None
    xs, ys = zip(*pairs)
    mx, my = statistics.mean(xs), statistics.mean(ys)
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx <= 0 or vy <= 0:
        return None
    return sum((x - mx) * (y - my) for x, y in pairs) / (vx * vy) ** 0.5


def f2(x):
    return "–" if x is None else f"{x:.2f}"


def med(xs, d=3):
    xs = [x for x in xs if x is not None]
    return f"{statistics.median(xs):.{d}f}" if xs else "–"


def quarters(rows, key, reverse=False):
    """The worst and best quarter of a world's years by `key` (higher = worse unless reverse)."""
    good = [r for r in rows if r.get(key) is not None]
    if len(good) < 8:
        return [], []
    srt = sorted(good, key=lambda r: r[key], reverse=not reverse)
    k = len(srt) // 4
    return srt[:k], srt[-k:]


def main():
    D = {s: json.loads((OUT / f"seed_{s}.json").read_text(encoding="utf-8")) for s in SEEDS}
    L = []
    w = L.append
    w("# V1 — What do ACL's existing bad years do? Tables\n")
    v = (OUT / "verify.txt").read_text(encoding="utf-8").strip()
    rep = all(r["replay_matches"] for r in D.values())
    w(f"Probe check: {v}. Replays match the saved E13R runs in all 16: **{'yes' if rep else 'NO'}**.\n")

    # complete years only (the world alive through the year, with its measures taken)
    Y = {s: [r for r in D[s]["years"] if r["winter_tile"] is not None and r["pop_start"] > 0 and r["year"] >= 1] for s in SEEDS}
    for s in SEEDS:
        for r in Y[s]:
            r["deaths_pp"] = (r["adult_starved_winter"] + r["child_starved_winter"]) / r["pop_start"]
            r["short_share"] = r["short_weeks"] / r["adult_winter_weeks"] if r["adult_winter_weeks"] else None

    w("## Q1. How variable are ACL's years?\n")
    cv_a, cv_w = [], []
    for s in SEEDS:
        a = [r["autumn_tile"] for r in Y[s] if r["autumn_tile"]]
        b = [r["winter_tile"] for r in Y[s] if r["winter_tile"]]
        if len(a) > 5:
            cv_a.append(statistics.pstdev(a) / statistics.mean(a))
        if len(b) > 5:
            cv_w.append(statistics.pstdev(b) / statistics.mean(b))
    w(f"Coefficient of variation of plant food per land tile from year to year, per world: mid-autumn median {med(cv_a)}, "
      f"mid-winter median {med(cv_w)}. (Real grassland production: about 0.37, Shi et al. 2014, N4 evidence.)")
    allr = [r for s in SEEDS for r in Y[s]]
    w(f"\nCorrelation over all world-years, winter food per tile with: the year's growing weather "
      f"{f2(corr([r['weather'] for r in allr], [r['winter_tile'] for r in allr]))}; winter hardness "
      f"{f2(corr([r['hard'] for r in allr], [r['winter_tile'] for r in allr]))}; wetness "
      f"{f2(corr([r['wet'] for r in allr], [r['winter_tile'] for r in allr]))}.")

    w("\n## Q2. Are bad winters deadly?\n")
    dshare = []
    for s in SEEDS:
        worst, best = quarters(Y[s], "deaths_pp")
        tot = sum(r["adult_starved_winter"] + r["child_starved_winter"] for r in Y[s])
        if tot:
            dshare.append(sum(r["adult_starved_winter"] + r["child_starved_winter"] for r in worst) / tot)
    w(f"Share of a world's winter starvation deaths that fall in its worst quarter of winters (by deaths per person): "
      f"median {med(dshare, 2)} (a quarter would be even).")
    w(f"\nCorrelation over all world-years, winter starvation deaths per person with: winter food per tile "
      f"{f2(corr([r['winter_tile'] for r in allr], [r['deaths_pp'] for r in allr]))}; winter hardness "
      f"{f2(corr([r['hard'] for r in allr], [r['deaths_pp'] for r in allr]))}; growing weather "
      f"{f2(corr([r['weather'] for r in allr], [r['deaths_pp'] for r in allr]))}; adults' share of winter-weeks short "
      f"{f2(corr([r['short_share'] for r in allr], [r['deaths_pp'] for r in allr]))}.")
    poor, rich = [], []
    for s in SEEDS:
        lo, hi = quarters(Y[s], "winter_tile", reverse=True)        # lo: least winter food per tile
        poor += lo
        rich += hi
    w(f"\nWinters with the least food per tile (each world's poorest quarter) against the most: deaths per 1,000 people "
      f"{1000 * statistics.mean([r['deaths_pp'] for r in poor]):.2f} against {1000 * statistics.mean([r['deaths_pp'] for r in rich]):.2f}; "
      f"adults' share of winter-weeks short {med([r['short_share'] for r in poor])} against {med([r['short_share'] for r in rich])}.")

    w("\n## Q3. Does density absorb bad years?\n")
    nxt = {s: {r["year"]: r for r in Y[s]} for s in SEEDS}
    after_bad, after_mild = [], []
    for s in SEEDS:
        worst, best = quarters(Y[s], "deaths_pp")
        for grp, acc in ((worst, after_bad), (best, after_mild)):
            for r in grp:
                n1 = nxt[s].get(r["year"] + 1)
                n3 = nxt[s].get(r["year"] + 3)
                if n1 and n3:
                    acc.append((n1["pop_start"] / r["pop_start"], n3["pop_start"] / r["pop_start"]))
    w(f"Population a year later ÷ this year: after the worst quarter of winters {med([x[0] for x in after_bad])}, after the "
      f"mildest {med([x[0] for x in after_mild])}; three years later {med([x[1] for x in after_bad])} against "
      f"{med([x[1] for x in after_mild])}.")

    w("\n## Q4. Do people respond, the next autumn?\n")
    w("| next year, after a winter that was | planners per adult | median stock ÷ winter need | carers with food stashed | seed sown per person | expectation of going short in winter |")
    w("|---|---|---|---|---|---|")
    for label, key, rev in (("among the worst quarter (deaths)", "deaths_pp", False), ("among the mildest quarter (deaths)", "deaths_pp", False),
                            ("among the poorest quarter (food per tile)", "winter_tile", True), ("among the richest quarter (food per tile)", "winter_tile", True)):
        rows = []
        for s in SEEDS:
            worst, best = quarters(Y[s], key, reverse=rev)
            grp = worst if "worst" in label or "poorest" in label else best
            for r in grp:
                n1 = nxt[s].get(r["year"] + 1)
                if n1:
                    rows.append(n1)
        if not rows:
            continue
        pl = statistics.mean(r["planners"] / r["adults_autumn"] for r in rows if r["adults_autumn"])
        cs = sum(r["carers_stash"][0] for r in rows) / max(1, sum(r["carers_stash"][1] for r in rows))
        sw = statistics.mean(r["seed_sown"] / r["pop_start"] for r in rows)
        w(f"| {label} | {pl:.3f} | {med([r['stock_need'] for r in rows])} | {100 * cs:.1f}% | {sw:.2f} | {med([r['expect_short_winter'] for r in rows])} |")

    w("\n## Q5. Do bad years cluster?\n")
    rs = []
    for s in SEEDS:
        a = [r["winter_tile"] for r in Y[s]]
        if len(a) > 5:
            c = corr(a[:-1], a[1:])
            if c is not None:
                rs.append(c)
    w(f"Correlation of a world's winter food per tile with the next year's: median {med(rs, 2)} over {len(rs)} worlds.")

    (HERE / "findings_tables.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
