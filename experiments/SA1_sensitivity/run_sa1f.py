"""SA1-F — the sensitive and near-the-line settings on 256 new seeds (followup_questions.md, frozen as `SA1F-frozen`).
SA1's code, arms, observers and functions, imported unchanged; only the seeds and the output folder differ.

  python experiments/SA1_sensitivity/run_sa1f.py zero    # hard stop: SA1's zero check, into output_f/
  python experiments/SA1_sensitivity/run_sa1f.py run     # 9 arms x 256 seeds (skips worlds already saved)
"""
from __future__ import annotations

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_sa1 as S  # noqa: E402

S.OUT = HERE / "output_f"
SEEDS = tuple(range(4301, 4557))
SENSITIVE = ("perception_lo", "perception_hi", "reach_hi", "mortality_hi")
NEAR = ("forage_lo", "conception_lo", "reach_lo")
ARMS = ("c",) + SENSITIVE + NEAR + ("s",)
assert len(SEEDS) == 256 and all(a in S.ARMS for a in ARMS)


def run():
    v = S.OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: zero check has not passed")
    me = [sys.executable, str(Path(__file__).resolve())]
    jobs = [(a, s) for s in SEEDS for a in ARMS if not (S.OUT / f"{a}_seed_{s}.json").exists()]
    list(ThreadPoolExecutor(4).map(lambda j: subprocess.call(me + ["one", j[0], str(j[1])]), jobs))
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if S.zero() else 1)
    elif cmd == "one":
        S.run_one(sys.argv[2], int(sys.argv[3]))
    elif cmd == "run":
        run()
    elif cmd == "smokeone":   # analysis smoke test only: 5 years, a separate folder
        S.run_one(sys.argv[2], int(sys.argv[3]), years=5, out=HERE / "output_f_smoke")
