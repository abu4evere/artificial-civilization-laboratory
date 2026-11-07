"""HK1 exploration (read-only, before any freeze; council round 70 asked): at every successful hunt in nature v14, the
meat taken and each party member's free carry room just before the meat is handed out. From these: the meat lost to
carry room under the live even split (as resolve_hunts does it), and the expected loss if one member, drawn by own
(0.5 + hunting skill) x tool factor, held the whole kill. Nothing in nature is changed; take_prey is wrapped to read.

  python experiments/HK1_who_holds_the_kill/explore_overflow.py <seed> <years>      # writes explore_overflow_<seed>.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "CI1_children_and_aims"))
import run_ci1 as R  # noqa: E402

seed, years = int(sys.argv[1]), int(sys.argv[2])
w = R.make(seed, "c", code="v14")          # v14 itself (CI1's zero checks: code_ci1 at 0 = code_v14)
import acl.fauna as fauna  # noqa: E402
from acl.matter import best_item, carry_capacity  # noqa: E402

rows = []
orig = fauna.take_prey


def take_prey(world, loc):
    out = orig(world, loc)
    meat = out[0]
    hunters = [world.people[i] for i in world.hunts.get(loc, ()) if world.people[i].alive]
    if meat > 0 and hunters:
        room = [max(0.0, carry_capacity(world, h) - h.edible()) for h in hunters]
        wt = [(0.5 + h.skills["hunting"]) * best_item(h, "hunt")[1] for h in hunters]
        rows.append([world.tick, round(meat, 3), len(hunters), [round(r, 3) for r in room], [round(x, 4) for x in wt]])
    return out


fauna.take_prey = take_prey
for _ in range(years * R.WPY):
    w.step()
    if not w.living():
        break

n_succ = len(rows)
meat = sum(r[1] for r in rows)
lost_even = sum(max(0.0, r[1] / r[2] - room) for r in rows for room in r[3])
lost_one = 0.0
for _, m, n, room, wt in rows:
    tw = sum(wt) or float(n)
    lost_one += sum((x / tw if sum(wt) else 1.0 / n) * max(0.0, m - rm) for x, rm in zip(wt, room))
parties = [r for r in rows if r[2] > 1]
res = {"seed": seed, "years": years, "final_tick": w.tick, "successes": n_succ, "party_successes": len(parties),
       "meat": round(meat, 2), "lost_even": round(lost_even, 3), "lost_one_expected": round(lost_one, 3),
       "share_lost_even": round(lost_even / meat, 5) if meat else None,
       "share_lost_one": round(lost_one / meat, 5) if meat else None,
       "max_take": max((r[1] for r in rows), default=0), "min_room": min((x for r in rows for x in r[3]), default=None),
       "rows": rows}
(HERE / f"explore_overflow_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
print({k: v for k, v in res.items() if k != "rows"})
