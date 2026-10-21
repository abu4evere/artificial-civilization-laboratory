"""Write stub copies of a study's saved worlds (final state hash only) so a replay study can check itself on GitHub.

    python tools/ci/saved_stubs.py <hashes.json> <dir>

<hashes.json> maps a saved world's file name to its final state hash (committed beside the study, e.g.
experiments/MB1_multi_band/saved_world_hashes.json). Existing files are never overwritten.
"""
import json
import sys
from pathlib import Path

hashes = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
n = 0
for name, h in hashes.items():
    f = out / name
    if not f.exists():
        f.write_text(json.dumps({"world_hash": h}), encoding="utf-8")
        n += 1
print(f"wrote {n} stubs into {out}")
