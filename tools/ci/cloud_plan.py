"""Split a study's worlds into chunks for GitHub Actions (the `cloud-run` workflow).

    python tools/ci/cloud_plan.py <runner.py> <chunks> [smoke]   -> prints the job matrix as JSON

The runner must define ARMS and SEEDS (or DISCOVERY and HOLDOUT), YEARS, and accept `one <arm> <seed> <years> <out>`,
as every frozen study runner does. "smoke" uses the runner's SMOKE_SEEDS (the years are given to the chunk step).
"""
import importlib.util
import json
import sys
from pathlib import Path


def load(script):
    path = Path(script).resolve()
    spec = importlib.util.spec_from_file_location("runner", path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(mod)
    return mod


def items(mod, smoke=False):
    if smoke:
        seeds = tuple(mod.SMOKE_SEEDS)
    elif hasattr(mod, "SEEDS"):
        seeds = tuple(mod.SEEDS)
    else:
        seeds = tuple(mod.DISCOVERY) + tuple(mod.HOLDOUT)
    return [f"{a}:{s}" for s in seeds for a in mod.ARMS]


if __name__ == "__main__":
    mod = load(sys.argv[1])
    n = int(sys.argv[2])
    its = items(mod, len(sys.argv) > 3 and sys.argv[3] == "smoke")
    n = max(1, min(n, len(its)))
    chunks = [its[k::n] for k in range(n)]           # interleaved, so every chunk gets every arm
    print(json.dumps({"include": [{"chunk": k, "jobs": ",".join(c)} for k, c in enumerate(chunks)]}))
