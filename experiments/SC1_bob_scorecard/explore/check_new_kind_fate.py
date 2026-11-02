"""SC1 follow-up, exploratory (not part of any frozen plan): what happens to a kind invented after year 100?
Replays world 22001 (live v11, read-only wrappers only) to year 130 and follows every world-new kind made in play
from year 100: is it dropped from the inventor's recipes at once (the 12-recipe cap evicts the least valued, and a new
kind starts at value 0), is the made thing ever used (judge_item), does its value ever pass 0.05 (the make choice's
floor), and how long does the inventor keep it.

  python experiments/SC1_bob_scorecard/explore/check_new_kind_fate.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.setup("v11")
from acl import knowhow  # noqa: E402

w = base.make_world(22001, base.LP)
START, END = 100 * 52, 130 * 52
track = {}             # (pid, sig) -> dict
o_rem, o_judge = knowhow.remember_recipe, knowhow.judge_item


def remember_recipe(world, p, sig, recipe, how, source=None, props=None, meant=None):
    new_world = sig not in world.knowledge
    before = len(p.recipes)
    others = [world_v for s, world_v in p.itemval.items() if s in p.recipes]
    out = o_rem(world, p, sig, recipe, how, source, props, meant)
    if new_world and how == "made" and START <= world.tick < END:
        track[(p.id, sig)] = {"t": world.tick, "n_before": before, "kept": sig in p.recipes,
                              "min_other": min(others) if others else None, "used": 0, "vmax": 0.0, "lost": None}
    return out


def judge_item(world, p, sig, felt):
    out = o_judge(world, p, sig, felt)
    e = track.get((p.id, sig))
    if e is not None:
        e["used"] += 1
    return out


knowhow.remember_recipe, knowhow.judge_item = remember_recipe, judge_item


def obs(world, events):
    for (pid, sig), e in track.items():
        if e["lost"] is not None or not e["kept"]:
            continue
        p = world.people.get(pid)
        if p is None or not p.alive:
            e["lost"] = ["death", world.tick - e["t"]]
        elif sig not in p.recipes:
            e["lost"] = ["dropped", world.tick - e["t"]]
        else:
            e["vmax"] = max(e["vmax"], p.itemval.get(sig, 0.0))


w.observers.append(obs)
for _ in range(END):
    w.step()
E = list(track.values())
kept = [e for e in E if e["kept"]]
out = {"new_kinds": len(E),
       "dropped_at_once": sum(1 for e in E if not e["kept"]),
       "inventor_had_12_before": sum(1 for e in E if e["n_before"] >= 12),
       "kept": len(kept),
       "kept_ever_used": sum(1 for e in kept if e["used"] > 0),
       "kept_value_ever_above_0.05": sum(1 for e in kept if e["vmax"] > 0.05),
       "kept_lost_by_drop": sum(1 for e in kept if e["lost"] and e["lost"][0] == "dropped"),
       "kept_lost_by_death": sum(1 for e in kept if e["lost"] and e["lost"][0] == "death"),
       "kept_still_held_at_130": sum(1 for e in kept if e["lost"] is None),
       "median_weeks_held_if_dropped": sorted(e["lost"][1] for e in kept if e["lost"] and e["lost"][0] == "dropped")[
           len([e for e in kept if e["lost"] and e["lost"][0] == "dropped"]) // 2] if any(
           e["lost"] and e["lost"][0] == "dropped" for e in kept) else None}
(HERE / "check_new_kind_fate.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out))
