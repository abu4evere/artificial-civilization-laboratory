"""EXPLORATORY (after BD1's results; not frozen; labelled as such). Which part of bodies_stay changes survival?
Three arms, each BD1's B with one part switched off, on BD1's first 64 seeds (12001-12064), paired with BD1's own C and B.
  python run_x.py run      # writes output/<arm>_seed_<s>.json
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import run_bd1 as R  # noqa: E402

R.CODES["bd1"] = HERE / "code_bd1x"
ARMS = {"nofoul": {"bodies_stay": 1, "bd1x_no_foul": 1}, "noseen": {"bodies_stay": 1, "bd1x_no_seen": 1},
        "nomeat": {"bodies_stay": 1, "bd1x_no_meat": 1}}
R.ARMS.update(ARMS)
SEEDS = tuple(range(12001, 12065))
OUT = HERE / "output"

if __name__ == "__main__":
    if sys.argv[1] == "one":
        R.run_one(sys.argv[2], int(sys.argv[3]), 120, OUT)
    elif sys.argv[1] == "run":
        me = [sys.executable, str(Path(__file__).resolve())]
        todo = [(a, s) for s in SEEDS for a in ARMS if not (OUT / f"{a}_seed_{s}.json").exists()]
        with ThreadPoolExecutor(6) as pool:
            list(pool.map(lambda j: subprocess.call(me + ["one", j[0], str(j[1])], stdout=subprocess.DEVNULL), todo))
        print("ALL DONE", flush=True)
