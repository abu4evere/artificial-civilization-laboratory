"""Run Experiment 1 (Long histories): many seeds, up to 200 years each, features frozen.

Usage:
    python experiments/E1/run_e1.py --years 200 --seeds 101 102 103
    python experiments/E1/run_e1.py --analyse          # write summary.md from what has run

Each seed writes output/seed_<n>.json: one row of measurements per year (see
acl/measure.py), a summary at year 100 and at the end, and the chronicle.
Snapshots at year 100 and 200 go next to it. All of it is deterministic for a
given seed and code version.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent))

from acl.config import VERSIONS, WEEKS_PER_YEAR, Config  # noqa: E402
from acl.historian import Historian  # noqa: E402
from acl.measure import Lab  # noqa: E402
from acl.runner import save_snapshot  # noqa: E402
from acl.world import World  # noqa: E402

OUT = HERE / "output"


def run(seed: int, years: int) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    w = World(Config(seed=seed))
    h = Historian()
    lab = Lab(h)
    w.observers += [h, lab]
    t0 = time.time()
    at_100 = None
    for y in range(years):
        for _ in range(WEEKS_PER_YEAR):
            w.step()
        if not w.living():
            break
        if y + 1 == 100:
            at_100 = lab.summary(w)
            save_snapshot(w, h, OUT / f"seed_{seed}_year100.json.gz")
        if (y + 1) % 25 == 0:
            print(f"  seed {seed}: year {y + 1}, {len(w.living())} alive, {time.time() - t0:.0f}s", flush=True)
    save_snapshot(w, h, OUT / f"seed_{seed}_end.json.gz")
    out = {"seed": seed, "years_run": w.year, "extinct": not w.living(), "versions": VERSIONS,
           "seconds": round(time.time() - t0), "rows": lab.years, "summary_100": at_100,
           "summary_end": lab.summary(w),
           "chronicle": [c for c in h.chronicle if c["kind"] in
                         ("invention", "first", "myth", "symbol", "famine", "drought", "feud", "revenge", "era")]}
    (OUT / f"seed_{seed}.json").write_text(json.dumps(out), encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", type=int, default=200)
    ap.add_argument("--seeds", type=int, nargs="*", default=[101, 102, 103, 104, 105, 106])
    ap.add_argument("--analyse", action="store_true")
    a = ap.parse_args()
    if not a.analyse:
        for s in a.seeds:
            if (OUT / f"seed_{s}.json").exists():
                print(f"seed {s}: already run")
                continue
            r = run(s, a.years)
            print(f"seed {s}: done, {r['years_run']} years, {r['seconds']}s", flush=True)
    from analyse_e1 import write_summary
    write_summary(OUT, HERE / "summary.md")


if __name__ == "__main__":
    main()
