"""LX1 — does parts-first teaching cost survival? (questions.md, frozen as `LX1-frozen`). Uses LM1's code and runner
unchanged (`code_lm1`, `run_lm1.py`, `LM1-frozen`); only the arms (C and L), the seeds and the output folder differ.

  python experiments/LX1_parts_first_survival/run_lx1.py zero                       # LM1's zero checks, written here
  python experiments/LX1_parts_first_survival/run_lx1.py one <arm> <seed> <years> <out>   # one world (cloud-run)
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "LM1_memory_and_parts"))
import run_lm1 as R  # noqa: E402

OUT = HERE / "output"
R.OUT = OUT                              # zero.txt is written beside LX1's worlds
YEARS = R.YEARS
SEEDS = tuple(range(7601, 8113))         # 512 new seeds, used by no study
SMOKE_SEEDS = (9961, 9962)
ARMS = {"c": R.ARMS["c"], "l": R.ARMS["l"]}

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if R.zero() else 1)
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        R.run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
