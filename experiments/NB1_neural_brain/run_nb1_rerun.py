"""NB1: rerun of the one phase-1 world whose cloud job hit the 340-minute limit (run 42513724775, chunk 3: c:25402 and
n:25415 finished, e:25408 did not). The same runner, code and seed, so the world is the one it would have been.

  (cloud) runner = experiments/NB1_neural_brain/run_nb1_rerun.py; it shares run_nb1's zero record through `fp`.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import run_nb1 as R  # noqa: E402

JOBS = ["e:25408"]
ARMS, YEARS = R.ARMS, R.YEARS

if __name__ == "__main__":
    if sys.argv[1] == "fp":
        R.base.setup(R.CODE)
        print(R.base.fingerprint(R.CODE))
    elif sys.argv[1] == "one":
        R.run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
