"""Extra read-only analysis for the four questions after Investigations A-D.

1. Why trust is disconnected from truth.
2. Why sowing belief spreads but sowing behaviour does not.
3. Whether islands isolate populations once the crossing gap is accounted for.
4. Whether early inventions are too easy because of current property thresholds.

Nothing here runs the world forward. It uses the recorded re-runs (inv_seed_<n>.json),
the E1 snapshots, and static calculations from the physics in config.py and matter.py.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from itertools import combinations_with_replacement
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent))

from acl import matter  # noqa: E402
from acl.config import WEEKS_PER_YEAR, Config  # noqa: E402
from acl.historian import classify  # noqa: E402
from acl.runner import load_snapshot  # noqa: E402

OUT = HERE / "output"
SEASONS = ("spring", "summer", "autumn", "winter")


def _pct(a, b):
    return f"{100 * a / b:.0f}%" if b else "–"


# --- 2. sowing ----------------------------------------------------------------------------------

def best_case_yield(cfg: Config, sow_week: int, fertility: float = 0.7) -> tuple:
    """Follow one unit of seed sown in week `sow_week` of the year through the physics, with an ordinary
    year and nobody touching it. Returns (most crop standing at any time, week of the year it peaks)."""
    sown, crop, best, best_week = 0.85, 0.0, 0.0, sow_week     # 15% is lost when it is put down
    for k in range(1, 2 * WEEKS_PER_YEAR):
        week = (sow_week + k) % WEEKS_PER_YEAR
        season = week // 13
        if season in (0, 1):
            sprouted = sown * cfg.sprout_rate
            sown -= sprouted
            crop += sprouted * cfg.seed_multiplier * (0.4 + 0.6 * fertility)
        else:
            sown *= 1.0 - cfg.seed_loss
        if season == 3:
            crop *= 1.0 - cfg.crop_rot
        if crop > best:
            best, best_week = crop, week
    return round(best, 2), best_week


def sowing(runs, L):
    w = L.append
    cfg = Config()
    w("### Sowing: what the physics allows, against what happened")
    w("")
    w("One unit of seed sown in an ordinary year on ground of fertility 0.7, never touched, never harvested early. "
      "Most crop standing at any one time (each unit of seed eaten instead is worth 1 food):")
    w("")
    w("| sown in | most crop | when it peaks |")
    w("|---|---|---|")
    for s, name in enumerate(SEASONS):
        y, wk = best_case_yield(cfg, s * 13 + 6)
        w(f"| mid-{name} | {y} | week {wk} ({SEASONS[wk // 13]}) |")
    w("")
    # actual yield by the season of sowing: harvests on that spot in the following 60 weeks
    by_season = defaultdict(lambda: [0.0, 0.0, 0.0])        # seeds sown, crop harvested, harvested by the sower
    sowers_per_year = Counter()
    for r in runs:
        harvests = defaultdict(list)
        for tick, who, x, y, crop, sowers in r["harvests"]:
            harvests[(x, y)].append((tick, who, crop))
        claimed = set()
        for tick, who, x, y, amount, season, belief in sorted(r["sowings"]):
            rec = by_season[season]
            rec[0] += amount
            sowers_per_year[(r["seed"], tick // WEEKS_PER_YEAR)] += 1
            for i, (t2, who2, crop) in enumerate(harvests[(x, y)]):
                if tick <= t2 <= tick + 60 and (x, y, i) not in claimed:
                    claimed.add((x, y, i))
                    rec[1] += crop
                    if who2 == who:
                        rec[2] += crop
    w("What really came back, per unit of seed sown (all harvests on that spot within 60 weeks):")
    w("")
    w("| sown in | seeds sown | crop harvested per seed | of which by the sower |")
    w("|---|---|---|---|")
    for s, name in enumerate(SEASONS):
        sown, crop, own = by_season[s]
        w(f"| {name} | {sown:.0f} | {crop / sown if sown else 0:.2f} | {own / sown if sown else 0:.2f} |")
    w("")
    # believers vs sowers: patterns say who holds the belief; sowings say who acts
    w("Who believes, who has only been told, and who sows (yearly averages over all living years of all seeds):")
    w("")
    w("| seed | believe in sowing (tested, ≥0.15) | told only (hearsay) | people who sowed that year | ratio believers : sowers |")
    w("|---|---|---|---|---|")
    for r in runs:
        bel, hs, sow, yrs = 0, 0, 0, 0
        sowers_by_year = defaultdict(set)
        for tick, who, *_ in r["sowings"]:
            sowers_by_year[tick // WEEKS_PER_YEAR].add(who)
        for i, y in enumerate(r["patterns"]):
            bel_keys = [v[0] for k, v in y.items() if k.startswith("belief:seeds@")]
            hs_keys = [v[0] for k, v in y.items() if k.startswith("hearsay:seeds@")]
            bel += max(bel_keys, default=0)
            hs += max(hs_keys, default=0)
            sow += len(sowers_by_year.get(i, ()))
            yrs += 1
        w(f"| {r['seed']} | {bel / yrs:.1f} | {hs / yrs:.1f} | {sow / yrs:.1f} | "
          f"{(bel / sow) if sow else float('inf'):.1f} : 1 |")
    w("")


# --- 3. islands ----------------------------------------------------------------------------------

def _gaps(world):
    comps = world.landmasses()
    c = world.cfg
    gap = {}
    for i in range(len(comps)):
        for j in range(i + 1, len(comps)):
            best = 99
            for (x1, y1) in comps[i]:
                for (x2, y2) in comps[j]:
                    dx = min(abs(x1 - x2), c.width - abs(x1 - x2))
                    dy = min(abs(y1 - y2), c.height - abs(y1 - y2))
                    best = min(best, max(dx, dy))
            gap[(i, j)] = gap[(j, i)] = best
    return comps, gap


def _bands_of(world, pid, memo, groups):
    """The founding bands someone descends from."""
    if pid in memo:
        return memo[pid]
    p = world.people[pid]
    if p.generation == 0:
        out = frozenset([(int(pid[1:]) - 1) % groups])
    else:
        out = frozenset()
        for par in (p.mother, p.father):
            if par and par in world.people:
                out = out | _bands_of(world, par, memo, groups)
    memo[pid] = out
    return out


def islands(runs, L):
    w = L.append
    w("### Islands: crossings that needed something that floats, and whose children mixed")
    w("")
    w("| seed | islands with people at the start | water between them (tiles) | crossings over water wider than a jump (needed a raft) | first such crossing (year) | crossings over a jump-wide channel | descend from 2+ founding bands @100 | @200 |")
    w("|---|---|---|---|---|---|---|---|")
    for r in runs:
        world = r["_w"]
        c = world.cfg
        comps, gap = _gaps(world)
        island = {loc: i for i, comp in enumerate(comps) for loc in comp}
        groups = max(1, min(4, c.founders // 4))
        founders = [p for p in world.people.values() if p.generation == 0]
        # where each founding band started: the island of the founders' first recorded crossing origin is unknown,
        # so use the island the band's founders were most often on in the first year of the recorded crossings;
        # simpler and exact: re-create the starting world (deterministic) and read their places.
        from acl.world import World
        start = World(Config(seed=r["seed"]))
        band_island = {}
        for p in start.people.values():
            band_island.setdefault((int(p.id[1:]) - 1) % groups, Counter())[island.get(p.loc)] += 1
        start_islands = sorted({cnt.most_common(1)[0][0] for cnt in band_island.values()})
        widths = sorted({gap[(a, b)] for a in start_islands for b in start_islands if a < b})
        wide = [cr for cr in r["crossings"] if gap.get((cr[2], cr[3]), 99) > c.reach]
        hop = [cr for cr in r["crossings"] if gap.get((cr[2], cr[3]), 99) <= c.reach]
        mixed = []
        for tag in ("year100", "end"):
            path = OUT / f"seed_{r['seed']}_{tag}.json.gz"
            if not path.exists():
                mixed.append("–")
                continue
            wd, _ = load_snapshot(path) if tag == "year100" else (world, None)
            memo = {}
            living = wd.living()
            if not living:
                mixed.append("–")
                continue
            m = sum(1 for p in living if len(_bands_of(wd, p.id, memo, groups)) >= 2)
            mixed.append(_pct(m, len(living)))
        w(f"| {r['seed']} | {len(start_islands)} | {', '.join(str(x) for x in widths) or '–'} | {len(wide)} | "
          f"{wide[0][0] // WEEKS_PER_YEAR if wide else '–'} | {len(hop)} | {mixed[0]} | {mixed[1]} |")
    w("")
    w("Do people keep the rafts they make? (Floating is never what a thing is judged by; people carry their three "
      "most valued things.)")
    w("")
    w("| seed | year | living | know how to make something that floats 0.65+ | carry one | its worth to them (mean) |")
    w("|---|---|---|---|---|---|")
    for r in runs:
        for tag in ("year100", "end"):
            path = OUT / f"seed_{r['seed']}_{tag}.json.gz"
            if not path.exists():
                continue
            wd = r["_w"] if tag == "end" else load_snapshot(path)[0]
            living = wd.living()
            if not living:
                continue
            floats = {sig for sig, rec in wd.knowledge.items()
                      if rec.get("props") and rec["props"].get("float", 0.0) >= 0.65}
            know = [p for p in living if floats & set(p.recipes)]
            carry = [p for p in living if any(it.get("float", 0.0) >= 0.65 for it in p.items)]
            worth = [p.itemval.get(sig, 0.0) for p in know for sig in floats & set(p.recipes)]
            w(f"| {r['seed']} | {wd.year} | {len(living)} | {len(know)} | {len(carry)} | "
              f"{sum(worth) / len(worth) if worth else 0:.2f} |")
    w("")


# --- 4. inventions ----------------------------------------------------------------------------------

def thresholds(L):
    w = L.append
    w("### Early inventions and the property thresholds")
    w("")
    one = []
    for a, b in combinations_with_replacement(matter.MATERIALS, 2):
        for binder in matter.FLEXIBLE:
            one.append(((a, b, binder), matter.bind(matter.raw_props(a), matter.raw_props(b), binder)))
    w("Two kinds of threshold are involved, and only one changes what people can do:")
    w("")
    w("- **Physics (changes lives):** something floating 0.65 or more lets a person stand on water "
      "(`world.passable`). Tools help in proportion to their properties (`matter.factor`), with no threshold.")
    w("- **Names (changes nothing):** the historian calls a thing a raft at float 0.65, a carrier at contain 0.6, "
      "a wrap at warm 0.6, a club at hard 0.6 with reach 0.55, a blade at edge 0.55. These only decide what we "
      "call things and when \"the first …\" is written. People never see them.")
    w("")
    w("One-step ties of raw materials, and how they sit against those thresholds:")
    w("")
    w("| tie | float | contain | warm | hard, reach | named |")
    w("|---|---|---|---|---|---|")
    for (a, b, binder), it in one:
        cls = classify(it)
        if it["float"] >= 0.5 or it["contain"] >= 0.5 or it["warm"] >= 0.5 or cls:
            w(f"| {a} + {b} with {binder} | {it['float']} | {it['contain']} | {it['warm']} | {it['hard']}, {it['reach']} | "
              f"{', '.join(cls) or '–'} |")
    w("")
    base_float = max(matter.RAW[m][5] for m in matter.MATERIALS)
    w(f"Raw materials alone: the most buoyant (wood) floats {base_float}, below the 0.65 needed. Tying any two "
      "buoyant things adds half the smaller one's float, so wood + wood is the first and simplest thing that "
      "crosses water. Fiber tied to fiber gets +0.1 containment for each flexible part, which is why three "
      "fibers already hold things like a basket.")
    w("")
    w("What-if, on paper only (no run): how many one-step ties would cross water, or be named, if the thresholds were higher:")
    w("")
    w("| float needed to cross water | one-step ties that would cross |")
    w("|---|---|")
    for t in (0.65, 0.7, 0.75, 0.8, 0.9):
        w(f"| {t} | {sum(1 for _, it in one if it['float'] >= t)} |")
    w("")


def main():
    runs = []
    for f in sorted(OUT.glob("inv_seed_*.json")):
        r = json.loads(f.read_text(encoding="utf-8"))
        r["_w"], r["_h"] = load_snapshot(OUT / f"seed_{r['seed']}_end.json.gz")
        runs.append(r)
    L = ["## Extra analysis for the four questions", ""]
    sowing(runs, L)
    islands(runs, L)
    thresholds(L)
    text = (HERE / "investigations.md").read_text(encoding="utf-8") if (HERE / "investigations.md").exists() else ""
    marker = "## Extra analysis for the four questions"
    if marker in text:
        text = text[:text.index(marker)]
    (HERE / "investigations.md").write_text(text + "\n".join(L) + "\n", encoding="utf-8")
    print("appended to", HERE / "investigations.md")


if __name__ == "__main__":
    main()
