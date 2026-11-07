"""HK1 exploration (read-only, before any freeze): every hunt in nature v14 by party size, attempts and successes, from
the world's own "hunt" events (party = the ids on one tile that week). Asked after explore_overflow.py found no party
successes in 3 worlds x 100 years.

  python experiments/HK1_who_holds_the_kill/explore_parties.py <seed> <years>      # writes explore_parties_<seed>.json
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "CI1_children_and_aims"))
import run_ci1 as R  # noqa: E402

seed, years = int(sys.argv[1]), int(sys.argv[2])
w = R.make(seed, "c", code="v14")
att, succ, adults_weeks = Counter(), Counter(), 0


def obs(world, events):
    global adults_weeks
    for ev in events:
        if ev["k"] == "hunt":
            n = len(ev.get("party") or [ev.get("a")])
            att[n] += 1
            succ[n] += int(bool(ev.get("success")))
    adults_weeks += sum(1 for p in world.living() if p.age(world.tick) >= 12 * R.WPY)


w.observers.append(obs)
for _ in range(years * R.WPY):
    w.step()
    if not w.living():
        break
res = {"seed": seed, "years": years, "final_tick": w.tick, "attempts_by_party_size": dict(sorted(att.items())),
       "successes_by_party_size": dict(sorted(succ.items())), "grown_weeks": adults_weeks,
       "hunts_per_grown_year": round(R.WPY * sum(att.values()) / adults_weeks, 5) if adults_weeks else None}
(HERE / f"explore_parties_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
print(res)
