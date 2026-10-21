"""Fetch a `cloud-run` workflow's results into a study's output folder.

    python tools/ci/fetch_cloud.py <run-id> <out_dir> [--replace]

Downloads the run's `results` artifact (gh CLI) and copies each world's file into <out_dir>. A file that already exists
is left alone unless --replace; a world already run on this computer is compared instead (its final state hash must be
equal), which doubles as a check that GitHub's machines replay ACL exactly.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GH = r"C:\Users\User\gh\bin\gh.exe"
REPO = "abu4evere/artificial-civilization-laboratory"

run_id, out = sys.argv[1], Path(sys.argv[2])
replace = "--replace" in sys.argv
out.mkdir(parents=True, exist_ok=True)
tmp = Path(tempfile.mkdtemp())
subprocess.run([GH, "run", "download", run_id, "--repo", REPO, "--name", "results", "--dir", str(tmp)], check=True)
new = same = differ = 0
for f in sorted(tmp.glob("*.json")):
    dst = out / f.name
    if dst.exists() and not replace:
        a = json.loads(f.read_text(encoding="utf-8")).get("world_hash")
        b = json.loads(dst.read_text(encoding="utf-8")).get("world_hash")
        if a == b:
            same += 1
        else:
            differ += 1
            print("DIFFERS from the local run:", f.name)
        continue
    shutil.copy2(f, dst)
    new += 1
print(f"copied {new}; already here and identical {same}; already here and different {differ}")
sys.exit(1 if differ else 0)
