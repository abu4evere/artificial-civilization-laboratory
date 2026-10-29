"""LC1 — does curiosity slow the erosion over 1,000 years? (questions.md, frozen as `LC1-frozen`).
CU1's runner (`../CU1_curiosity/run_cu1.py`) unchanged, with 1,000 years, new seeds and its own output folder.

  python experiments/LC1_long_curiosity/run_lc1.py zero
  python experiments/LC1_long_curiosity/run_lc1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "CU1_curiosity"))
import run_cu1 as base  # noqa: E402

YEARS = 1000
SEEDS = tuple(range(20301, 20333))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9993, 9992)
ARMS = base.ARMS
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
base.OUT = HERE / "output"
base.YEARS, base.SEEDS, base.SMOKE_SEEDS, base.JOBS = YEARS, SEEDS, SMOKE_SEEDS, JOBS

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if base.zero() else 1)
    elif cmd == "fp":
        base.setup()
        print(base.fingerprint())
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        base.run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    else:
        sys.exit("use: zero | fp | one <arm> <seed> <years> <out>")
