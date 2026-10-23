"""GR2 — does first-season grace hold up, and is it safe for population? (questions.md, frozen as `GR2-frozen`).
Uses GR1's code and runner unchanged (`code_g1`, `run_g1.py`, `G1-frozen` / `GR1-frozen`); only the seeds and the
output folder differ.

  python experiments/GR2_grace_confirm/run_gr2.py zero                           # GR1's zero checks, written here
  python experiments/GR2_grace_confirm/run_gr2.py one <arm> <seed> <years> <out>   # one world (cloud-run)
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "G1_first_season_grace"))
import run_g1 as R  # noqa: E402

OUT = HERE / "output"
R.OUT = OUT                              # zero.txt is written beside GR2's worlds
YEARS = R.YEARS
SEEDS = tuple(range(10001, 10513))       # 512 new seeds, used by no study
SMOKE_SEEDS = (9993, 9994)
ARMS = R.ARMS

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if R.zero() else 1)
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        R.run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
