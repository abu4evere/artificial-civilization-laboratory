"""One command that says how ACL's background runs are doing, in plain words. Reads only; changes nothing.

  python tools/acl_status.py

Made for the fallback helper (docs/HELPER_RUNBOOK.md): every line starts with OK, WAIT, DONE or PROBLEM.
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments"
RUNS = [  # name, output folder, file pattern, how many, the process that runs it
    ("LK1", EXP / "LK1_location_knowledge" / "output", "*_seed_4*.json", 768, "run_lk1.py"),
    ("SA1", EXP / "SA1_sensitivity" / "output", "*_seed_*.json", 896, "run_sa1.py"),
]


def processes() -> str:
    try:
        out = subprocess.run(["powershell", "-NoProfile", "-Command",
                              "Get-CimInstance Win32_Process -Filter \"name='python.exe'\" | % { $_.CommandLine }"],
                             capture_output=True, text=True, timeout=60).stdout
    except Exception:
        out = ""
    return out


def broken(folder: Path, pattern: str) -> list:
    bad = []
    for f in folder.glob(pattern):
        try:
            json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            bad.append(f.name)
    return bad


def main() -> None:
    print(f"ACL status at {datetime.now():%Y-%m-%d %H:%M}")
    procs = processes()
    for name, folder, pattern, total, script in RUNS:
        files = sorted(folder.glob(pattern), key=lambda f: f.stat().st_mtime) if folder.exists() else []
        n = len(files)
        running = script in procs
        bad = broken(folder, pattern) if folder.exists() else []
        if bad:
            print(f"PROBLEM {name}: {len(bad)} unreadable output file(s): {', '.join(bad[:5])}. Do not delete them. Write this in WORKLOG.md and stop.")
            continue
        if n >= total:
            print(f"DONE    {name}: all {total} worlds saved.")
            continue
        recent = [f for f in files if (datetime.now().timestamp() - f.stat().st_mtime) < 1200]
        rate = len(recent) / 20 if recent else 0.0   # worlds a minute over the last 20 minutes
        left = total - n
        eta = f"about {left / rate / 60:.1f} hours left at {rate:.1f} worlds a minute" if rate else "no world saved in the last 20 minutes"
        if running:
            print(f"OK      {name}: {n} of {total} worlds saved, running; {eta}.")
        elif name == "SA1" and "after_lk1.py" in procs:
            print(f"WAIT    SA1: waiting for LK1 to finish (its waiter is running); {n} of {total} saved.")
        else:
            print(f"PROBLEM {name}: {n} of {total} saved and NOT running. Follow 'Runs stopped' in docs/HELPER_RUNBOOK.md.")
    logs = [("LK1", f) for f in (EXP / "LK1_location_knowledge").glob("run_detached*.err")] +            [("SA1", f) for f in (EXP / "SA1_sensitivity").glob("run_detached*.err")]
    for name, log in logs:
        if log.exists():
            text = log.read_text(encoding="utf-8", errors="replace").strip()
            if "Traceback" in text or "Error" in text or "ABORT" in text or "HARD STOP" in text:
                print(f"PROBLEM {name}: its error log has an error. Copy the last 20 lines of {log.relative_to(ROOT)} into WORKLOG.md and stop.")
    waiter = EXP / "SA1_sensitivity" / "after_lk1.log"
    if waiter.exists():
        last = waiter.read_text(encoding="utf-8").strip().splitlines()[-1:]
        print(f"INFO    SA1 waiter log: {last[0] if last else '(empty)'}")


if __name__ == "__main__":
    main()
