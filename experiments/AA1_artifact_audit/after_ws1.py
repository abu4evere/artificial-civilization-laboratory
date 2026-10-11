"""Wait for WS1's main run to finish (all 1,280 outputs saved and no WS1 worker still running), then start AA1's
discovery run. Reads only file counts; changes nothing in WS1.

  python experiments/AA1_artifact_audit/after_ws1.py      (started detached, so it survives the session ending)
"""
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WS1_OUT = ROOT / "experiments" / "S1_world_size" / "output"
LOG = Path(__file__).with_name("after_ws1.log")


def done():
    return sum(1 for _ in WS1_OUT.glob("*_seed_*.json")) >= 1280


def say(msg):
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M} {msg}\n")


say("waiting for WS1 (1,280 worlds)")
while not done():
    time.sleep(600)
time.sleep(120)   # let the last WS1 process finish writing and exit
say("WS1 complete; starting AA1 discovery (seeds 501-516)")
r = subprocess.call([sys.executable, "-u", str(ROOT / "experiments" / "AA1_artifact_audit" / "run_aa1.py"), "discovery"], cwd=str(ROOT))
say(f"AA1 discovery finished (exit {r}); the discovery reading is written next, before the holdout")
