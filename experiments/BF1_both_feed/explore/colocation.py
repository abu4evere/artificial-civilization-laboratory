"""A side look before any plan for law B (not data; council round 79 asked for it): in v16 worlds, how often is a young
child's living father on the child's tile at the week's body phase, and does he hold food beyond his own needs then?
Read-only: wraps biology.body_phase and counts before calling it. Exploration seeds 26901-26902, used by no study.

  python experiments/BF1_both_feed/explore/colocation.py <seed> <years> <out.json>
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent.parent
sys.path.insert(0, str(EXP / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.CODES["v16"] = EXP / "NV16_nature_v16" / "code_v16"
base.setup("v16")
from acl import biology  # noqa: E402
from acl.config import CHILD_END, WEEKS_PER_YEAR  # noqa: E402
from acl.world import distance  # noqa: E402

seed, years, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
FROM = max(0, years - 30) * WEEKS_PER_YEAR          # count the last 30 years
n = Counter()
orig = biology.body_phase


def counted(world):
    if world.tick >= FROM:
        c = world.cfg
        for ch in world.living():
            if ch.age(world.tick) >= CHILD_END or not ch.caregiver:
                continue
            n["child_weeks"] += 1
            if ch.caregiver != ch.mother:
                n["carer_not_mother"] += 1
                continue
            n["carer_mother"] += 1
            f = world.people.get(ch.father) if ch.father else None
            if f is None or not f.alive:
                n["father_dead_or_none"] += 1
                continue
            d = distance(f.loc, ch.loc, c.width, c.height)
            n["father_d0" if d == 0 else "father_d1" if d == 1 else "father_d2plus"] += 1
            mother = world.people[ch.mother]
            if mother.partner == f.id:
                n["father_is_mothers_partner"] += 1
                if d == 0:
                    n["partner_father_d0"] += 1
            if d == 0:
                own = f.need(c, world.tick) + sum(x.need(c, world.tick) for x in world.dependents(f.id))
                if f.edible() > own:
                    n["father_d0_with_surplus"] += 1
                if ch.need(c, world.tick) - ch.edible() > 0 and mother.edible() < mother.need(c, world.tick) + ch.need(c, world.tick):
                    n["father_d0_mother_short"] += 1
    orig(world)


biology.body_phase = counted
w = base.make_world(seed, dict(base.LP))
for _ in range(years * WEEKS_PER_YEAR):
    w.step()
Path(out).write_text(json.dumps({"seed": seed, "years": years, "counted_from_year": FROM // WEEKS_PER_YEAR,
                                 "living_at_end": sum(1 for _ in w.living()), **dict(n)}, indent=1))
print(seed, dict(n))
