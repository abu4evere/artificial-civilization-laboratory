"""BX1 Phase A, newborn version (the creator, 23 Nov: "we gotta see that new brain from 0 from born to grown up"):
the FIRST BABY born in the world gets the new brain (MBb) for its 'where' from birth, among old-mind people. The same world (same seed) runs twice: OLD (the agent keeps the old mind) and NEW (its 'where' is the brain's).
Logs the agent's life yearly, its weekly choices (NEW), and the time per week (for Phase B's budget).

  python run_watch.py [SEED] [YEARS]        -> output/watch_<SEED>.json and a printed summary
"""
import json
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "code_bx1"))
sys.path.insert(0, str(HERE / "code_bx1" / "acl"))

from acl.runner import new_world          # noqa: E402
from acl import mindview                  # noqa: E402
from acl.config import WEEKS_PER_YEAR     # noqa: E402

MBB = str(HERE / "mbb_seed1.npz")


def first_baby(world):
    """The first person born in the world (generation 1+), earliest birth then id. Both runs are identical until the
    brain acts, so it is the same baby in both."""
    kids = sorted((p for p in world.people.values() if p.generation >= 1), key=lambda p: (p.birth, p.id))
    return kids[0].id if kids else None


def life(world, pid):
    p = world.people.get(pid)
    if p is None:
        return None
    age = ((p.death_tick if p.death_tick is not None else world.tick) - p.birth) / WEEKS_PER_YEAR
    return {"alive": p.alive, "age": round(age, 1), "energy": round(p.energy, 1),
            "health": round(p.health), "loc": list(p.loc), "doing": p.doing, "partner": p.partner,
            "children": len(p.children), "mood": round(p.mood, 2),
            "thought": mindview.headline(world, p) if p.alive else "", "death": p.death_cause}


def run(seed, years, brain):
    world, hist = new_world(seed)
    pid, born_year = None, None
    world.bx1_log = []
    yearly, t0 = [], time.time()
    for wk in range(years * WEEKS_PER_YEAR):
        if not world.living():
            break
        world.step()
        if pid is None:
            pid = first_baby(world)
            if pid is not None:
                born_year = world.year
                if brain:
                    world.cfg.bx1_agent, world.cfg.bx1_brain = pid, MBB
        if pid is not None and wk % WEEKS_PER_YEAR == WEEKS_PER_YEAR - 1:
            yearly.append({"year": world.year, "pop": len(world.living()), "agent": life(world, pid)})
            a = world.people.get(pid)
            if a is not None and not a.alive and len(yearly) > 1 and not yearly[-2]["agent"]["alive"]:
                pass
    secs = time.time() - t0
    weeks = world.tick
    return {"agent": pid, "name": world.people[pid].name if pid else None, "born_year": born_year, "years": yearly, "choices": world.bx1_log,
            "weeks": weeks, "seconds": round(secs, 1), "sec_per_week": round(secs / max(1, weeks), 4),
            "final_pop": len(world.living())}


def summary(tag, r):
    alive_years = [y for y in r["years"] if y["agent"] and y["agent"]["alive"]]
    last = r["years"][-1]["agent"] if r["years"] else None
    print(f"--- {tag}: {r['name']} ({r['agent']}); world pop at end {r['final_pop']}; "
          f"{r['sec_per_week']} s/week ({r['seconds']} s for {r['weeks']} weeks)")
    print(f"    alive for {len(alive_years)} of {len(r['years'])} years; "
          + (f"died: {last['death']} at age {last['age']}" if last and not last["alive"] else
             f"still alive, age {last['age']}, children {last['children']}" if last else "no record"))
    if r["choices"]:
        c = Counter(x["chose"] for x in r["choices"])
        print(f"    weekly choices (brain on): {dict(c.most_common(6))}")


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42
    years = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    out = {"seed": seed, "years": years}
    for tag, brain in (("OLD", False), ("NEW", True)):
        out[tag] = run(seed, years, brain)
        summary(tag, out[tag])
    (HERE / "output").mkdir(exist_ok=True)
    (HERE / "output" / f"newborn_{seed}.json").write_text(json.dumps(out, indent=1, default=str))
    print(f"saved output/newborn_{seed}.json")


if __name__ == "__main__":
    main()
