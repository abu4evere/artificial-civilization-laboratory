"""Wait for LK1's main run to finish (all 768 outputs saved), then start SA1's main run. Reads only file counts;
changes nothing in LK1.

  python experiments/SA1_sensitivity/after_lk1.py      (started detached, so it survives the session ending)
"""
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LK1_OUT = ROOT / "experiments" / "LK1_location_knowledge" / "output"
LOG = Path(__file__).with_name("after_lk1.log")


def done():
    return sum(1 for _ in LK1_OUT.glob("*_seed_4*.json")) >= 768


def say(msg):
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M} {msg}\n")


say("waiting for LK1 (768 worlds)")
while not done():
    time.sleep(600)
time.sleep(120)   # let the last LK1 process finish writing and exit
say("LK1 complete; starting SA1 (control re-run first)")
r = subprocess.call([sys.executable, "-u", str(ROOT / "experiments" / "SA1_sensitivity" / "run_sa1.py"), "run"], cwd=str(ROOT))
say(f"SA1 run finished (exit {r})")
