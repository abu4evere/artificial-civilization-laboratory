"""CI1-C — CI1's runner on new seeds, arms v14 / LG / sham (questions.md, frozen as `CI1C-frozen`). The code, set-up,
guards and observer are CI1's (`../CI1_children_and_aims/run_ci1.py`, unchanged), with one read-only addition: for each
world-new kind, whether a person other than its inventor made it within 5 years. The zero checks are CI1's (all four
arms, so code_ci1 is checked whole), run through this script so the observer checked is the one used.

  python experiments/CI1C_children_confirm/run_ci1c.py zero
  python experiments/CI1C_children_confirm/run_ci1c.py one <arm> <seed> <years> <out>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "CI1_children_and_aims"))
import run_ci1 as base  # noqa: E402

SEEDS = tuple(range(24101, 24133))        # 32 new paired seeds, used by no study
ARMS = {a: base.ARMS[a] for a in ("c", "g", "x")}    # IN set aside (round 69); base.ARMS stays whole for the zero checks
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
base.SEEDS, base.JOBS, base.OUT = SEEDS, JOBS, HERE / "output"
OUT, YEARS, SMOKE_SEEDS, WPY, CODE = base.OUT, base.YEARS, base.SMOKE_SEEDS, base.WPY, base.CODE
base.__file__ = __file__                  # zero() re-invokes this script, so hashruns use these settings


class CI1CObs(base.CI1Obs):
    """CI1's observer, plus: for each world-new kind, whether someone other than its inventor made it within 5 years
    (the weeks after the first, as CI1 counts remaking)."""

    def __init__(self, w):
        super().__init__(w)
        self.others = {}

    def __call__(self, world, events):
        tick = world.tick - 1
        for ev in events:
            if ev["k"] != "make" or ev.get("thing") is None:
                continue
            kd = self.kinds.get(ev["thing"])
            if kd is not None and ev.get("a") != kd[1] and kd[0] < tick <= kd[0] + base.WIN:
                self.others[ev["thing"]] = 1
        super().__call__(world, events)

    def results(self):
        r = super().results()
        r["made_by_others"] = [self.others.get(sig, 0) for sig in self.kinds]
        r["n_others"] = sum(r["made_by_others"])
        return r


base.CI1Obs = CI1CObs                     # run_one and hashrun build their observer from this name

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if base.zero() else 1)
    elif cmd == "hashrun":
        print(base.hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        ok, n = base.reload_check(int(sys.argv[2]))
        print(ok, n)
    elif cmd == "unit":
        ok, st = base.unit_check(int(sys.argv[2]))
        print(ok, json.dumps(st, sort_keys=True, separators=(",", ":")))
    elif cmd == "fp":
        base.base.setup(CODE)
        print(base.base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        base.run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: every year counted; never study data
        assert sys.argv[2] in ARMS
        base.LATE[0], base.LATE[1] = 0, int(sys.argv[4]) * WPY
        base.run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
