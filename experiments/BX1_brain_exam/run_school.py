"""BX1 Phase A2, the learning brain's school (exploratory, labelled; the creator: "yes build the learning brain").

The brain (starting from Mind Lab's MBb, like genes) lives life after life in ACL: in each new world it is the FIRST
BABY, and every week it learns from
  - its own week: its value at the place it chose is pulled toward the feeling that followed there (ACL's own weekly
    feeling: reward + 2 x mood change, as the NB brains used);
  - its caregiver, while it is a child (under 16): its value at the place the caregiver chose is pulled toward the
    caregiver's feeling (learning by watching a parent).
Mind Lab's own learning rate and clip (brains3: LR 0.01, CLIP 1.0); no new numbers. What it learned carries into the
next life. School worlds use seeds 10001+ (never the watch worlds 42, 7, 101, 2026, 555).

  python run_school.py LIVES [MAX_YEARS]   -> output/school_brain.npz (after every life), output/school_log.jsonl
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "code_bx1"))
sys.path.insert(0, str(HERE / "code_bx1" / "acl"))

import numpy as np                        # noqa: E402
from acl.runner import new_world          # noqa: E402
from acl.config import WEEKS_PER_YEAR     # noqa: E402
from acl import brain_bx1 as BX           # noqa: E402

import os
KEY = "school"
OUT = HERE / "output"
FIXED = os.environ.get("BX1_FIXED")                # a fixed brain (no learning, nothing saved): the after-school test
SEED0 = int(os.environ.get("BX1_SEED0", "10001"))  # the test uses new worlds (20001+), never the school's
BASE = os.environ.get("BX1_BASELINE") == "1"      # the old mind for the same first babies (no brain, no learning)
TAG = ("baseline" if BASE else ("fixed_" + Path(FIXED).stem) if FIXED else "school") + os.environ.get("BX1_PART", "")    # a second worker: its own log
START = int(os.environ.get("BX1_START", "0"))     # a second worker starts at this life index (same seeds as one worker)


def feeling(p):
    return float(p.reward + 2.0 * (p.mood - p.mood_before))


def row_at(loc, world, target):
    c = world.cfg
    dx = ((target[0] - loc[0] + c.width // 2) % c.width) - c.width // 2
    dy = ((target[1] - loc[1] + c.height // 2) % c.height) - c.height // 2
    wx, wy = dx + BX.HALF, dy + BX.HALF
    return wy * BX.N + wx if (0 <= wx < BX.N and 0 <= wy < BX.N) else None


def first_baby(world):
    kids = sorted((p for p in world.people.values() if p.generation >= 1), key=lambda p: (p.birth, p.id))
    return kids[0].id if kids else None


def one_life(net, seed, max_years):
    world, _ = new_world(seed)
    world.bx1_log, world.bx1_choice, world.bx1_pending, world.bx1_watch = [], {}, None, set()
    pid, lessons, errs, feel = None, 0, [], []
    for _ in range(max_years * WEEKS_PER_YEAR + 2 * WEEKS_PER_YEAR):
        if not world.living():
            break
        if pid is not None:
            a = world.people[pid]
            child = a.years(world.tick) < 16
            world.bx1_watch = {pid} | ({a.caregiver} if (child and a.caregiver) else set())
        loc0 = world.people[pid].loc if pid is not None else None
        world.step()
        if pid is None:
            pid = first_baby(world)
            if pid is not None and not BASE:
                world.cfg.bx1_agent, world.cfg.bx1_brain = pid, KEY
            continue
        a = world.people[pid]
        if not a.alive:
            break
        if world.bx1_pending is not None:
            m, lev = world.bx1_pending
            loc = loc0
        else:
            m, lev, loc = BX.window(a, world), BX._levels(a), a.loc
        cells, rets = [], []
        mine = world.bx1_choice.get(pid)
        if mine and mine[0] is not None:
            r = row_at(loc, world, mine[0])
            if r is not None:
                cells.append(r)
                rets.append(feeling(a))
                feel.append(rets[-1])
        if a.caregiver and a.years(world.tick) < 16:
            cg = world.people.get(a.caregiver)
            theirs = world.bx1_choice.get(a.caregiver)
            if cg is not None and cg.alive and theirs and theirs[0] is not None:
                r = row_at(loc, world, theirs[0])
                if r is not None:
                    cells.append(r)
                    rets.append(feeling(cg))
        e = None if (BASE or FIXED) else BX.learn(net, m, lev, cells, rets)
        if e is not None:
            errs.append(e)
            lessons += len(cells)
        world.bx1_choice, world.bx1_pending = {}, None
        if a.years(world.tick) >= max_years:
            break
    a = world.people.get(pid) if pid else None
    age = None if a is None else ((a.death_tick if a.death_tick is not None else world.tick) - a.birth) / WEEKS_PER_YEAR
    return {"seed": seed, "agent": pid, "age": None if age is None else round(age, 1),
            "died": None if a is None else (a.death_cause if not a.alive else None),
            "lessons": lessons, "mse": round(float(np.mean(errs)), 4) if errs else None,
            "mean_feeling": round(float(np.mean(feel)), 4) if feel else None, "weeks": world.tick}


def main():
    lives = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    max_years = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    OUT.mkdir(exist_ok=True)
    start = OUT / "school_brain.npz"
    logf = OUT / f"{TAG}_log.jsonl"
    net = BX.load(str(HERE / FIXED) if FIXED else str(start if start.exists() else HERE / "mbb_seed1.npz"), seed=1)
    BX._BRAINS[KEY] = net
    done = sum(1 for _ in open(logf)) if logf.exists() else 0
    for i in range(START + done, START + done + lives):
        t0 = time.time()
        rec = one_life(net, SEED0 + i, max_years)
        rec.update(life=i + 1, seconds=round(time.time() - t0, 1))
        if not (BASE or FIXED):
            np.savez(start, **net.p)
        with open(logf, "a") as f:
            f.write(json.dumps(rec) + "\n")
        print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
