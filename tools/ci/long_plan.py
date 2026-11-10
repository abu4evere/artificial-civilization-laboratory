"""Plan one stage of the `long-run` workflow: every world of the study that has no finished result yet.

    python tools/ci/long_plan.py <runner.py> <results_dir>   -> prints {"matrix": ..., "todo": N, "total": M}

Worlds are listed as the `cloud-run` planner lists them (cloud_plan.items); one world per job.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cloud_plan import items, load  # noqa: E402

mod = load(sys.argv[1])
done_dir = Path(sys.argv[2])
its = items(mod)
done = {p.name for p in done_dir.glob("*_seed_*.json")} if done_dir.exists() else set()
todo = [x.split(":") for x in its if f"{x.split(':')[0]}_seed_{x.split(':')[1]}.json" not in done]
matrix = {"include": [{"arm": a, "seed": s} for a, s in todo]} if todo else {"include": [{"arm": "none", "seed": "0"}]}
print(json.dumps({"matrix": matrix, "todo": len(todo), "total": len(its)}))
