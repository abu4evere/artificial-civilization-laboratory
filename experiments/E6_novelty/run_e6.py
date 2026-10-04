"""E6: one world for 1000 years with the novelty recorder, under the baseline code or the new physics.

Usage:
  python experiments/E6_novelty/run_e6.py baseline <seed> [years]   # today's code (verified copy in code_baseline/)
  python experiments/E6_novelty/run_e6.py e6 <seed> [years]         # the new physics (code_e6/)
  python experiments/E6_novelty/run_e6.py verify <arm> <seed> [years]   # recorder is read-only: same state hash
Writes output/<arm>/seed_<n>.json and a snapshot every 100 years.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent


def setup(arm: str):
    code = HERE / ("code_baseline" if arm == "baseline" else "code_e6")
    sys.path.insert(0, str(code))
    sys.path.insert(1, str(HERE))
    import acl
    assert Path(acl.__file__).resolve().parent == (code / "acl").resolve(), acl.__file__
    return 1 if arm == "baseline" else 100


def run(arm: str, seed: int, years: int):
    scale = setup(arm)
    from acl.config import VERSIONS, WEEKS_PER_YEAR, Config
    from acl.matter import MATERIALS
    from acl.runner import save_snapshot
    from acl.historian import Historian
    from acl.world import World
    from novelty import Novelty

    out = HERE / "output" / arm
    out.mkdir(parents=True, exist_ok=True)
    w = World(Config(seed=seed))
    h = Historian()
    rec = Novelty(scale, MATERIALS)
    w.observers += [h, rec]
    t0 = time.time()
    for y in range(years):
        for _ in range(WEEKS_PER_YEAR):
            w.step()
        if (y + 1) % 100 == 0:
            save_snapshot(w, h, out / f"seed_{seed}_year{y + 1}.json.gz")
            print(f"  {arm} seed {seed}: year {y + 1}, {len(w.living())} alive, {time.time() - t0:.0f}s", flush=True)
        if not w.living():
            save_snapshot(w, h, out / f"seed_{seed}_end.json.gz")
            break
    res = rec.results(w)
    res.update({"arm": arm, "seed": seed, "years_run": w.year, "extinct": not w.living(), "versions": VERSIONS,
                "seconds": round(time.time() - t0)})
    (out / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: done, {w.year} years, LFA {res['LFA']}, {res['seconds']}s", flush=True)


def verify(arm: str, seed: int, years: int):
    scale = setup(arm)
    from acl.config import WEEKS_PER_YEAR, Config
    from acl.matter import MATERIALS
    from acl.world import World
    from novelty import Novelty

    hashes = []
    for with_rec in (False, True):
        w = World(Config(seed=seed))
        if with_rec:
            w.observers.append(Novelty(scale, MATERIALS))
        for _ in range(years * WEEKS_PER_YEAR):
            w.step()
        hashes.append(w.state_hash())
    print(f"{arm} seed {seed}, {years} years: without {hashes[0][:16]}  with {hashes[1][:16]}  ->",
          "READ-ONLY" if hashes[0] == hashes[1] else "CHANGES THE WORLD")
    return hashes[0] == hashes[1]


if __name__ == "__main__":
    if sys.argv[1] == "verify":
        ok = verify(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 20)
        sys.exit(0 if ok else 1)
    run(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 1000)
