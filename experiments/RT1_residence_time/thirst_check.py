"""RT1, described (not a frozen reading): are R4's extra thirst deaths people who walked to water and were sent back to
a dry base? Read-only replays (seeds 5001-5008, 30 years, arms c and r4): each week, for every adult who went short of
water (thirst > 0.05), was the destination they chose that week within sight of fresh water they could reach?

  python experiments/RT1_residence_time/thirst_check.py
"""
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_rt1 as R  # noqa: E402

R.setup("rt1")
from acl import weather  # noqa: E402


class Check:
    def __init__(self):
        self.c = Counter()

    def __call__(self, world, events):
        c = world.cfg
        chosen = {d.agent_id: d.chosen for d in world.week_decisions}
        for p in world.living():
            if p.age(world.tick) < 16 * 52:
                continue
            self.c["adult_weeks"] += 1
            if p.thirst <= 0.05:
                continue
            self.c["thirsty"] += 1
            act, target = chosen.get(p.id, (None, None))
            if isinstance(target, tuple) and len(target) == 2 and all(isinstance(v, int) for v in target):
                if weather.reachable_fresh(world, p, target, c.perception) is not None:
                    self.c["thirsty_but_went_to_water"] += 1


for arm in (sys.argv[1:] or ["c", "r4"]):
    tot = Counter()
    for seed in range(5001, 5009):
        w = R.make_world(seed, R.ARMS[arm])
        ch = Check()
        w.observers.append(ch)
        for _ in range(30 * 52):
            w.step()
            if not w.living():
                break
        tot += ch.c
    print(arm, dict(tot), "thirsty share of adult weeks %.3f" % (tot["thirsty"] / tot["adult_weeks"]),
          "| of the thirsty, chose a destination by water %.3f" % (tot["thirsty_but_went_to_water"] / max(1, tot["thirsty"])),
          flush=True)
