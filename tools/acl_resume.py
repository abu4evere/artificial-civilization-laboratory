"""Restart ACL's background runs after a shutdown or sleep, only where needed. Safe to run more than once: the runners
skip worlds already saved, and nothing is started twice.

  python tools/acl_resume.py

Checks first that every saved output can be read; if any cannot, it starts nothing and says so.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments"
LK1, SA1 = EXP / "LK1_location_knowledge", EXP / "SA1_sensitivity"


def procs() -> str:
    return subprocess.run(["powershell", "-NoProfile", "-Command",
                           "Get-CimInstance Win32_Process -Filter \"name='python.exe'\" | % { $_.CommandLine }"],
                          capture_output=True, text=True, timeout=60).stdout


def start(script: str, args: list, log_dir: Path, tag: str) -> None:
    a = ",".join(f"'{x}'" for x in ["-u", script, *args])
    cmd = (f"Start-Process -FilePath '{sys.executable}' -ArgumentList {a} -WorkingDirectory '{ROOT}' -WindowStyle Hidden "
           f"-RedirectStandardOutput '{log_dir / f'run_detached_{tag}.log'}' -RedirectStandardError '{log_dir / f'run_detached_{tag}.err'}'")
    subprocess.run(["powershell", "-NoProfile", "-Command", cmd], check=True)


def unreadable(folder: Path) -> list:
    bad = []
    for f in folder.glob("*.json"):
        try:
            json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            bad.append(f.name)
    return bad


def main() -> None:
    bad = unreadable(LK1 / "output") + unreadable(SA1 / "output")
    if bad:
        print(f"STOP: unreadable output files {bad}. Started nothing. Write this in WORKLOG.md; Claude decides.")
        return
    p = procs()
    lk1_done = len(list((LK1 / "output").glob("*_seed_4*.json"))) >= 768
    sa1_done = len(list((SA1 / "output").glob("*_seed_*.json"))) >= 896
    from datetime import datetime
    tag = datetime.now().strftime("%m%d_%H%M")
    if not lk1_done and "run_lk1.py" not in p:
        start("experiments/LK1_location_knowledge/run_lk1.py", ["run"], LK1, tag)
        print("STARTED LK1 (it skips worlds already saved).")
    elif not lk1_done:
        print("OK LK1 is already running.")
    else:
        print("DONE LK1 is complete.")
    if sa1_done:
        print("DONE SA1 is complete.")
    elif "run_sa1.py" in p:
        print("OK SA1 is already running.")
    elif "after_lk1.py" in p:
        print("OK SA1's waiter is already running (SA1 starts when LK1 is done).")
    elif lk1_done:
        start("experiments/SA1_sensitivity/run_sa1.py", ["run"], SA1, tag)
        print("STARTED SA1 (it skips worlds already saved).")
    else:
        start("experiments/SA1_sensitivity/after_lk1.py", [], SA1, tag)
        print("STARTED SA1's waiter (SA1 starts when LK1 is done).")
    print("Now run: python tools/acl_status.py")


if __name__ == "__main__":
    main()
