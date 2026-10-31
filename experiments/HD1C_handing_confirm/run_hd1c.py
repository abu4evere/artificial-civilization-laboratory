"""HD1-C — HD1's runner on new seeds (questions.md, frozen as `HD1C-frozen`). The code, arms, observer and zero checks
are HD1's (`../HD1_handing/run_hd1.py`, unchanged); only SEEDS and OUT differ.

  python experiments/HD1C_handing_confirm/run_hd1c.py zero
  python experiments/HD1C_handing_confirm/run_hd1c.py one <arm> <seed> <years> <out>
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "HD1_handing"))
import run_hd1 as base  # noqa: E402

SEEDS = tuple(range(21301, 21333))        # 32 new paired seeds, used by no study
base.SEEDS = SEEDS
base.OUT = HERE / "output"
base.JOBS = [f"{a}:{s}" for a in base.ARMS for s in SEEDS]
OUT, YEARS, ARMS, JOBS, SMOKE_SEEDS = base.OUT, base.YEARS, base.ARMS, base.JOBS, base.SMOKE_SEEDS
base.__file__ = __file__                  # zero() re-invokes this script, so hashruns use these settings

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if base.zero() else 1)
    elif cmd == "hashrun":
        print(base.hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(base.reload_check(int(sys.argv[2])))
    elif cmd == "fp":
        base.setup()
        print(base.fingerprint())
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        base.run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
