"""E4: run one world under one code. Usage: python run_e4.py <e1|e2> <seed> [years]

Same observers and outputs as E1/E2 (historian + Lab; snapshots at year 100 and the end).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
CODE, SEED = sys.argv[1], int(sys.argv[2])
YEARS = int(sys.argv[3]) if len(sys.argv) > 3 else 200
sys.path.insert(0, str(ROOT / "experiments" / "E3_births" / "code_e1") if CODE == "e1" else str(ROOT))

from acl.config import VERSIONS, WEEKS_PER_YEAR, Config  # noqa: E402
from acl.historian import Historian  # noqa: E402
from acl.measure import Lab  # noqa: E402
from acl.runner import save_snapshot  # noqa: E402
from acl.world import World  # noqa: E402

OUT = HERE / "output" / CODE


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    w = World(Config(seed=SEED))
    h = Historian()
    lab = Lab(h)
    w.observers += [h, lab]
    t0 = time.time()
    at_100 = None
    for y in range(YEARS):
        for _ in range(WEEKS_PER_YEAR):
            w.step()
        if not w.living():
            break
        if y + 1 == 100:
            at_100 = lab.summary(w)
            save_snapshot(w, h, OUT / f"seed_{SEED}_year100.json.gz")
    save_snapshot(w, h, OUT / f"seed_{SEED}_end.json.gz")
    out = {"seed": SEED, "code": CODE, "years_run": w.year, "extinct": not w.living(), "versions": VERSIONS,
           "seconds": round(time.time() - t0), "rows": lab.years, "summary_100": at_100, "summary_end": lab.summary(w)}
    (OUT / f"seed_{SEED}.json").write_text(json.dumps(out), encoding="utf-8")
    print(f"{CODE} seed {SEED}: {w.year} years, {out['seconds']}s", flush=True)


if __name__ == "__main__":
    main()
