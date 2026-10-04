"""Run Experiment 2: the same 8 seeds as E1, 200 years, after the four changes
(reputation from tested accuracy, more testing, records, floating as an affordance).

Usage: python experiments/E2/run_e2.py [seeds...]
Then:  python experiments/E2/compare_e2.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "E1"))
sys.path.insert(0, str(HERE.parent.parent))

import run_e1  # noqa: E402

run_e1.OUT = HERE / "output"

if __name__ == "__main__":
    seeds = [int(a) for a in sys.argv[1:]] or list(range(101, 109))
    for s in seeds:
        if (run_e1.OUT / f"seed_{s}.json").exists():
            print(f"seed {s}: already run")
            continue
        r = run_e1.run(s, 200)
        print(f"seed {s}: done, {r['years_run']} years, {r['seconds']}s", flush=True)
