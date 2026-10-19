"""RT1b — residence time with the walk to water counted (questions_rt1b.md; a DRAFT, not frozen). `code_rt1b` = `code_rt1`
+ `water_trip`. Prepared before freezing on GPT's direction under the creator's delegation (18 October 2026): the zero
checks and a mechanism-only pilot may run; the study may not until the creator signs the plan off.

  python experiments/RT1_residence_time/run_rt1b.py zero     # hard stops: water_trip 0 = code_rt1; without a base it does nothing; it acts; read-only; reload
  python experiments/RT1_residence_time/run_rt1b.py pilot    # throwaway seeds 9801-9804, 15 years, r4 and r4w: the water mechanism only
  python experiments/RT1_residence_time/run_rt1b.py run      # c, r4, r4w on seeds 5701-5956, 120 years (refuses until signed off)
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_rt1 as R  # noqa: E402

R.CODES["rt1b"] = HERE / "code_rt1b"
OUT = HERE / "output_rt1b"
WPY, YEARS = 52, 120
SEEDS = tuple(range(5701, 5957))
PILOT_SEEDS = (9801, 9802, 9803, 9804)
ARMS = {"c": {}, "r4": {"residence_weeks": 4}, "r4w": {"residence_weeks": 4, "water_trip": 1}}


def fingerprint():
    from run_e7 import code_hash
    return code_hash(R.CODES["rt1b"] / "acl")


class Water:
    """Read-only, after each week: of adults who ended the week's actions within sight of fresh water they could reach
    (and were then sent back to base), how many still went short of water? And of the thirsty, how many had chosen a
    destination by water (thirst_check.py's measure)?"""

    def __init__(self):
        self.c = Counter()

    def __call__(self, world, events):
        from acl import weather
        c = world.cfg
        chosen = {d.agent_id: d.chosen for d in world.week_decisions}
        went = getattr(world, "trip_end", {})
        for p in world.living():
            if p.age(world.tick) < 16 * WPY:
                continue
            g = went.get(p.id)
            if g is not None and weather.reachable_fresh(world, p, g, c.perception) is not None:
                self.c["reached_water_then_sent_back"] += 1
                self.c["of_those_still_short"] += p.thirst > 0.05
            if p.thirst <= 0.05:
                continue
            self.c["thirsty"] += 1
            _, target = chosen.get(p.id, (None, None))
            if isinstance(target, tuple) and len(target) == 2 and all(isinstance(v, int) for v in target):
                if weather.reachable_fresh(world, p, target, c.perception) is not None:
                    self.c["thirsty_but_went_to_water"] += 1


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for kw in ({}, {"residence_weeks": 4}):
        for seed, years in ((11, 5), (501, 5), (501, 20), (601, 20)):
            t = call("rt1b", seed, years, json.dumps(kw), 0) == call("rt1", seed, years, json.dumps(kw), 0)
            ok &= t
            lines.append(f"{kw or 'C'}, seed {seed}, {years} years: water_trip 0 = code_rt1: {'yes' if t else 'NO'}")
    t = call("rt1b", 501, 20, json.dumps({"water_trip": 1}), 0) == call("rt1b", 501, 20, json.dumps({}), 0)
    ok &= t
    lines.append(f"seed 501, 20 years: water_trip 1 without a base = C exactly (it does nothing): {'yes' if t else 'NO'}")
    t = call("rt1b", 501, 20, json.dumps(ARMS["r4w"]), 0) != call("rt1b", 501, 20, json.dumps(ARMS["r4"]), 0)
    ok &= t
    lines.append(f"seed 501, 20 years: r4w differs from r4 (it acts): {'yes' if t else 'NO'}")
    t = call("rt1b", 501, 20, json.dumps(ARMS["r4w"]), 1) == call("rt1b", 501, 20, json.dumps(ARMS["r4w"]), 0)
    ok &= t
    lines.append(f"r4w, seed 501, 20 years: identical with and without the observers: {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"r4w, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    R.setup("rt1b")
    lines.append(f"code_rt1b fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def hashrun(code, seed, years, kw, observe):
    R.setup(code)
    w = R.make_world(seed, kw)
    if observe:
        w.observers += list(R.observers(w)) + [Water()]
    for _ in range(years * WPY):
        w.step()
    return R.world_hash(w)


def reload_check(seed):
    R.setup("rt1b")
    from acl.world import World
    a = R.make_world(seed, ARMS["r4w"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for w in (a, b):
        for _ in range(5 * WPY):
            w.step()
    return R.world_hash(a) == R.world_hash(b) and bool(a.bases)


def pilot_one(arm):
    """Throwaway seeds; prints only the water mechanism, no survival, population or deaths."""
    R.setup("rt1b")
    tot = Counter()
    for seed in PILOT_SEEDS:
        w = R.make_world(seed, ARMS[arm])
        ch = Water()
        w.observers.append(ch)
        for _ in range(15 * WPY):
            w.step()
            if not w.living():
                break
        tot += ch.c
    still = tot["of_those_still_short"] / max(1, tot["reached_water_then_sent_back"])
    went = tot["thirsty_but_went_to_water"] / max(1, tot["thirsty"])
    print(f"{arm}: adult-weeks that ended the week's actions by reachable water and were sent back: "
          f"{tot['reached_water_then_sent_back']}; of those, still short of water: {still:.3f} | "
          f"of the thirsty, had chosen a destination by water: {went:.3f}", flush=True)


def batch():
    q = (HERE / "questions_rt1b.md").read_text(encoding="utf-8")
    if "SIGNED OFF" not in q.splitlines()[0]:
        sys.exit("ABORT: RT1b is a draft; the creator has not signed it off")
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: the zero checks have not passed (run 'zero')")
    sys.exit("ABORT: the study runner is written after sign-off")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), json.loads(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "pilot":
        for a in ("r4", "r4w"):
            pilot_one(a)
    elif cmd == "run":
        batch()
