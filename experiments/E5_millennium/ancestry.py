"""E5 follow-up (read-only): which founding bands do the living descend from? Reads saved snapshots only."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))

from acl.config import Config  # noqa: E402
from acl.runner import load_snapshot  # noqa: E402
from acl.world import World  # noqa: E402

OUT = HERE / "output"


def main():
    res = {}
    for seed in (301, 302, 303, 304, 306, 308):
        start = World(Config(seed=seed))
        island = {xy: i for i, comp in enumerate(start.landmasses()) for xy in comp}
        bands = sorted({island[p.loc] for p in start.people.values()})
        band_of = {p.id: bands.index(island[p.loc]) for p in start.people.values()}
        res[seed] = {"founding_bands": len(bands), "founders_per_band": [sum(1 for b in band_of.values() if b == k) for k in range(len(bands))]}
        for year in (100, 500, 1000):
            f = OUT / f"seed_{seed}_year{year}.json.gz"
            if not f.exists():
                continue
            w, _ = load_snapshot(f)
            memo = {}

            def anc(pid):
                if pid in memo:
                    return memo[pid]
                p = w.people[pid]
                if p.generation == 0 or not p.mother or not p.father:
                    v = [0.0] * len(bands)
                    if pid in band_of:
                        v[band_of[pid]] = 1.0
                else:
                    a, b = anc(p.mother), anc(p.father)
                    v = [(x + y) / 2 for x, y in zip(a, b)]
                memo[pid] = v
                return v
            living = w.living()
            now_island = {xy: i for i, comp in enumerate(w.landmasses()) for xy in comp}
            by_place = {}
            for p in living:
                by_place.setdefault(now_island.get(p.loc, -1), []).append(anc(p.id))
            res[seed][year] = {str(k): {"n": len(v), "ancestry": [round(sum(x[i] for x in v) / len(v), 2) for i in range(len(bands))],
                                        "mixed": sum(1 for x in v if max(x) < 0.95)} for k, v in sorted(by_place.items())}
    (OUT / "ancestry.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    for s, d in res.items():
        print(s, d)


if __name__ == "__main__":
    main()
