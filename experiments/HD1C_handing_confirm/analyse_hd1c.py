"""HD1-C analysis: HD1's frozen analysis (`../HD1_handing/analyse_hd1.py`, unchanged) on this study's seeds and output.

  python experiments/HD1C_handing_confirm/analyse_hd1c.py      # writes results.md here
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_hd1c  # noqa: E402,F401  (sets HD1's runner to these seeds)
sys.path.insert(0, str(HERE.parent / "HD1_handing"))
import analyse_hd1 as base  # noqa: E402

base.SEEDS = run_hd1c.SEEDS
base.HERE = HERE
base.OUTDIR = HERE / "output"
base.main()
