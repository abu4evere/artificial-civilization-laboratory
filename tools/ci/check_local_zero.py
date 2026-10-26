"""Check a study's committed local zero record, so the `cloud-run` workflow can skip re-running the zero checks
(input skip_zero=local).

    python tools/ci/check_local_zero.py <runner.py>

Passes only if `zero_local.log` beside the runner says "All: PASS" and the code fingerprint it records equals the
fingerprint of the code the cloud is about to run (`<runner> fp`). Anything else fails, and the workflow stops.
"""
import re
import subprocess
import sys
from pathlib import Path

runner = Path(sys.argv[1])
log = runner.parent / "zero_local.log"
if not log.exists():
    sys.exit(f"no local zero record: {log}")
text = log.read_text(encoding="utf-8", errors="replace")
if "All: PASS" not in text:
    sys.exit(f"the local zero record does not say 'All: PASS':\n{text}")
m = re.search(r"fingerprint: ([0-9a-f]{64})", text)
if not m:
    sys.exit("the local zero record has no code fingerprint")
fp = subprocess.run([sys.executable, str(runner), "fp"], capture_output=True, text=True).stdout.split()
if not fp or fp[-1] != m.group(1):
    sys.exit(f"fingerprint mismatch: local record {m.group(1)}, code here {fp[-1] if fp else '?'}")
print(f"local zero record accepted: All: PASS, fingerprint {m.group(1)} matches the code here")
