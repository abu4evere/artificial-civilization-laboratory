"""NB3-A diagnosis (after the data; labelled): replay the 10 worlds whose autopsy replay ended with a fingerprint
different from NB3's original, with NB3's own runner, unchanged and with no recorders. If these plain replays also
differ from the originals, the cause is not the recorders. If they equal the autopsy replays, the recorders are shown
read-only at full length.

Runs on long-run: gh workflow run long-run.yml -f runner=experiments/NB3A_feeding_autopsy/replay_plain.py
"""
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).parent
NB3 = HERE.parent / "NB3_feelings" / "run_nb3.py"
sys.path.insert(0, str(NB3.parent))
import run_nb3 as P  # noqa: E402

JOBS = ["fH:25805", "fH:25807", "fH:25809", "f:25801", "f:25803", "f:25806", "f:25807", "f:25810", "f:25813",
        "f:25815"]
ARMS, SEEDS, YEARS = P.ARMS, P.SEEDS, P.YEARS

if __name__ == "__main__":
    sys.argv[0] = str(NB3)
    runpy.run_path(str(NB3), run_name="__main__")
