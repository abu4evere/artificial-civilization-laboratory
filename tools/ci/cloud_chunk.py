"""Run one chunk of a study's worlds (a step of the `cloud-run` workflow).

    python tools/ci/cloud_chunk.py <runner.py> <years> <out_dir> <arm:seed,arm:seed,...> [workers]

Each world is run by the runner itself (`one <arm> <seed> <years> <out>`), exactly as on the creator's computer; this
script only hands out the work and stops with an error if any world fails.
"""
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

script, years, out, jobs = sys.argv[1], sys.argv[2], Path(sys.argv[3]), sys.argv[4]
workers = int(sys.argv[5]) if len(sys.argv) > 5 else (os.cpu_count() or 2)
out.mkdir(parents=True, exist_ok=True)
todo = [j.split(":") for j in jobs.split(",") if j]


def one(job):
    arm, seed = job
    return subprocess.call([sys.executable, script, "one", arm, seed, years, str(out.resolve())])


with ThreadPoolExecutor(workers) as pool:
    codes = list(pool.map(one, todo))
bad = [f"{a}:{s}" for (a, s), c in zip(todo, codes) if c]
missing = [f"{a}:{s}" for a, s in todo if not (out / f"{a}_seed_{s}.json").exists()]
print(f"chunk done: {len(todo)} worlds, failed {bad}, missing {missing}", flush=True)
sys.exit(1 if bad or missing else 0)
