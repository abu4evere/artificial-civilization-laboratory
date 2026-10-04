"""E5: one world for 1000 years under the current code, with a read-only Divergence recorder.

Usage: python experiments/E5_millennium/run_e5.py <seed> [years]
Writes output/seed_<n>.json (Lab rows, Divergence rows every 10 years) and snapshots every 100 years.
"""
from __future__ import annotations

import itertools
import json
import statistics
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))

from acl import marks  # noqa: E402
from acl.config import VERSIONS, WEEKS_PER_YEAR, Config  # noqa: E402
from acl.historian import Historian  # noqa: E402
from acl.measure import Lab  # noqa: E402
from acl.person import GENES  # noqa: E402
from acl.runner import save_snapshot  # noqa: E402
from acl.world import World  # noqa: E402

OUT = HERE / "output"


def jaccard_distance(a: set, b: set):
    if not a and not b:
        return None
    return 1.0 - len(a & b) / len(a | b)


class Divergence:
    """Every 10 years: genes, culture and identity of each populated island. Only reads."""

    def __init__(self):
        self.rows = []
        self.island = None

    def __call__(self, world, events):
        tick = world.tick - 1
        if tick % (10 * WEEKS_PER_YEAR) != 10 * WEEKS_PER_YEAR - 1:
            return
        if self.island is None:
            self.island = {xy: i for i, comp in enumerate(world.landmasses()) for xy in comp}
        living = world.living()
        groups = {}
        for p in living:
            groups.setdefault(self.island.get(p.loc, -1), []).append(p)
        peopled = {k: v for k, v in groups.items() if k != -1 and len(v) >= 5}
        row = {"year": tick // WEEKS_PER_YEAR + 1, "population": len(living),
               "islands": {str(k): len(v) for k, v in sorted(peopled.items())}}
        info = {}
        for k, v in peopled.items():
            g = {t: statistics.mean(p.genes[t] for p in v) for t in GENES}
            sd = {t: statistics.pstdev([p.genes[t] for p in v]) for t in GENES}
            tech, sym, beliefs, stories = {}, {}, {}, {}
            for p in v:
                for sig in p.recipes:
                    tech[sig] = tech.get(sig, 0) + 1
                for key, val in p.beliefs.items():
                    if val >= 0.15:
                        beliefs[key] = beliefs.get(key, 0) + 1
                for shape in p.marks:
                    for thing, mv in marks.meaning(p, shape).items():
                        if mv >= 0.3:
                            sym[f"{shape}|{thing}"] = sym.get(f"{shape}|{thing}", 0) + 1
                for m in p.memories:
                    stories[m.eid] = stories.get(m.eid, 0) + 1
            habit = [statistics.mean(p.q[i] for p in v if len(p.q) > i) for i in range(len(v[0].q))] if v[0].q else []
            info[k] = {"genes": g, "spread": sd,
                       "tech": sorted(s for s, n in tech.items() if n >= 2),
                       "beliefs": sorted(s for s, n in beliefs.items() if n >= 2),
                       "symbols": sorted(s for s, n in sym.items() if n >= 2),
                       "stories": sorted(e for e, n in stories.items() if n >= 2),
                       "habit": habit}
        row["per_island"] = {str(k): {"genes": {t: round(x, 4) for t, x in d["genes"].items()},
                                      "spread": {t: round(x, 4) for t, x in d["spread"].items()},
                                      "tech": d["tech"], "beliefs": d["beliefs"], "symbols": d["symbols"]}
                             for k, d in info.items()}
        pairs = []
        for a, b in itertools.combinations(sorted(info), 2):
            A, B = info[a], info[b]
            gaps = {t: abs(A["genes"][t] - B["genes"][t]) for t in GENES}
            spread = {t: (A["spread"][t] + B["spread"][t]) / 2 for t in GENES}
            ha, hb = A["habit"], B["habit"]
            if ha and hb:
                dot = sum(x * y for x, y in zip(ha, hb))
                na = sum(x * x for x in ha) ** 0.5
                nb = sum(y * y for y in hb) ** 0.5
                habit_d = 1.0 - dot / (na * nb) if na and nb else None
            else:
                habit_d = None
            pairs.append({"a": a, "b": b,
                          "gene_gaps": {t: round(x, 4) for t, x in gaps.items()},
                          "traits_gap_over_spread": sum(1 for t in GENES if gaps[t] > spread[t]),
                          "tech_distance": jaccard_distance(set(A["tech"]), set(B["tech"])),
                          "belief_distance": jaccard_distance(set(A["beliefs"]), set(B["beliefs"])),
                          "symbol_distance": jaccard_distance(set(A["symbols"]), set(B["symbols"])),
                          "shared_story_distance": jaccard_distance(set(A["stories"]), set(B["stories"])),
                          "habit_distance": None if habit_d is None else round(habit_d, 4)})
        row["pairs"] = pairs
        # identity: trust toward one's own island against others
        own_t, other_t, own_a, other_a = [], [], [], []
        where = {p.id: self.island.get(p.loc, -1) for p in living}
        for p in living:
            for qid, r in p.rel.items():
                if qid not in where:
                    continue
                if where[qid] == where[p.id]:
                    own_t.append(r.trust)
                    own_a.append(r.affection)
                else:
                    other_t.append(r.trust)
                    other_a.append(r.affection)
        row["identity"] = {"trust_own": statistics.mean(own_t) if own_t else None,
                           "trust_other": statistics.mean(other_t) if other_t else None,
                           "affection_own": statistics.mean(own_a) if own_a else None,
                           "affection_other": statistics.mean(other_a) if other_a else None,
                           "ties_other": len(other_t)}
        # whole-world culture, for tradition persistence across centuries
        held = {}
        for p in living:
            for sig in p.recipes:
                held["tech:" + sig] = held.get("tech:" + sig, 0) + 1
            for key, val in p.beliefs.items():
                if val >= 0.15:
                    held["belief:" + key] = held.get("belief:" + key, 0) + 1
            for shape in p.marks:
                for thing, mv in marks.meaning(p, shape).items():
                    if mv >= 0.3:
                        held[f"symbol:{shape}|{thing}"] = held.get(f"symbol:{shape}|{thing}", 0) + 1
        row["traditions"] = sorted(k for k, n in held.items() if n >= 3)
        row["oldest_alive_birth"] = min((p.birth for p in living), default=None)
        self.rows.append(row)


def main():
    seed = int(sys.argv[1])
    years = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    OUT.mkdir(parents=True, exist_ok=True)
    w = World(Config(seed=seed))
    h = Historian()
    lab = Lab(h)
    div = Divergence()
    w.observers += [h, lab, div]
    t0 = time.time()
    for y in range(years):
        for _ in range(WEEKS_PER_YEAR):
            w.step()
        if (y + 1) % 100 == 0:
            save_snapshot(w, h, OUT / f"seed_{seed}_year{y + 1}.json.gz")
            print(f"  seed {seed}: year {y + 1}, {len(w.living())} alive, {time.time() - t0:.0f}s", flush=True)
        if not w.living():
            save_snapshot(w, h, OUT / f"seed_{seed}_end.json.gz")
            break
    out = {"seed": seed, "years_run": w.year, "extinct": not w.living(), "versions": VERSIONS,
           "seconds": round(time.time() - t0), "rows": lab.years, "divergence": div.rows,
           "summary_end": lab.summary(w),
           "chronicle": [c for c in h.chronicle if c["kind"] in ("invention", "loss", "myth", "symbol", "record",
                                                                 "famine", "drought", "feud", "revenge", "era")]}
    (OUT / f"seed_{seed}.json").write_text(json.dumps(out), encoding="utf-8")
    print(f"seed {seed}: done, {w.year} years, {out['seconds']}s", flush=True)


if __name__ == "__main__":
    main()
