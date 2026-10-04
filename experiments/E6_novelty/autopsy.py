"""E6.5 autopsy (watch-only): where does the discovery chain break?

Opportunity -> Interaction -> Transformation -> Observation -> Reuse -> Tradition

Replays an E6 world from its first week with probes that only read:
- at every decision: was there an opportunity (at a fire holding clay, food or anything to heat; holding something
  watertight at fresh water), was a heat/fill option among the person's top choices, and what did they choose?
- every time anything is held in a fire: what, by whom, and what came of it;
- the life of one traced thing (the rare event in that world): who made it, how it felt in use, puzzles, making
  it again, teaching, and how it was lost.
The replay is checked against the saved snapshot at year 100 (identical world state).

Usage: python experiments/E6_novelty/autopsy.py <seed> <traced sig> [years]   -> output/autopsy_<seed>.json
"""
from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "code_e6"))

from acl import actions, knowhow, matter, mind, weather  # noqa: E402
from acl.config import WEEKS_PER_YEAR, Config  # noqa: E402
from acl.world import World  # noqa: E402

seed, traced = int(sys.argv[1]), sys.argv[2]
years = int(sys.argv[3]) if len(sys.argv) > 3 else 100
W = None
opp = Counter()            # opportunity kind -> adult-weeks
took = Counter()           # opportunity kind -> weeks the matching step was taken
chose = {}                 # opportunity kind -> Counter of what was chosen instead
in_mind = Counter()        # opportunity kind -> weeks the step was among their top four options
ranks = {}                 # opportunity kind -> scores (step score, chosen score) when it was considered
heated = []                # every hold-in-fire: [tick, person, part, outcome]
trace = {"events": [], "uses": [], "weekly": []}


def adult(p, tick):
    return p.age(tick) >= 16 * WEEKS_PER_YEAR


def watched_decide(world, p):
    tick = world.tick
    tile = world.tile(p.loc)
    kinds = []
    if adult(p, tick) and tile.fire > 0:
        kinds.append("at a fire")
        if p.mats.get("clay", 0.0) >= 1.0:
            kinds.append("at a fire holding clay")
            if p.damp.get("clay", 0) <= matter.DRY:
                kinds.append("at a fire holding dry clay")
        shaped = [it for it in p.items if it["plastic"] >= 50]
        if shaped:
            kinds.append("at a fire holding a shaped clay thing")
            if any(it.get("wet", 0) <= matter.DRY for it in shaped):
                kinds.append("at a fire holding a DRY shaped clay thing")
        if p.food - min(p.kept, p.food) >= 2.0:
            kinds.append("at a fire with raw food")
    if adult(p, tick) and matter.best_holder(p, "water") >= 0:
        kinds.append("holding a watertight thing")
        if weather.reachable_fresh(world, p, p.loc, world.cfg.water_reach) is not None:
            kinds.append("holding a watertight thing at fresh water")
    option = REAL_DECIDE(world, p)
    for k in kinds:
        opp[k] += 1
        step = "fill" if "watertight" in k else "heat"
        taken = option[0] == step or (step == "heat" and "clay" in k and option[0] in ("play", "make"))
        took[k] += taken
        chose.setdefault(k, Counter())[option[0]] += 1
        for c in p.considered:
            if c[0] == step:
                in_mind[k] += 1
                best = max(cc[2] for cc in p.considered)
                ranks.setdefault(k, []).append([c[2], best])
                break
    if p.id == trace.get("maker") or any(it["sig"] == traced for it in p.items):
        if tick % 4 == 0:
            trace["weekly"].append({"t": tick, "who": p.id, "loc": list(p.loc), "chose": option[0],
                                    "itemval": round(p.itemval.get(traced, 0.0), 3),
                                    "knows": traced in p.recipes,
                                    "holds": any(it["sig"] == traced for it in p.items),
                                    "puzzles": [k for k in p.puzzles if traced in k],
                                    "considered": p.considered[:4]})
    return option


def watched_hold(world, p, part):
    out = REAL_HOLD(world, p, part)
    if out is not None:
        what = out["sig"]
    elif world.tile(p.loc).fire > 0:
        what = "burned, cracked or only dried"
    else:
        what = "no fire"
    heated.append([world.tick, p.id, part, what])
    return out


def watched_judge(world, p, sig, felt):
    if sig == traced:
        trace["uses"].append([world.tick, p.id, round(felt, 3), round(p.itemval.get(sig, 0.0), 3)])
    return REAL_JUDGE(world, p, sig, felt)


def watch_events(world, events):
    for e in events:
        if e.get("thing") == traced or e.get("with") == traced:
            trace["events"].append({k: v for k, v in e.items() if k in ("t", "k", "a", "b", "how", "thing", "with",
                                                                          "substance", "meant")})
            if e["k"] in ("play", "make") and "maker" not in trace:
                trace["maker"] = e["a"]
        if e["k"] == "death" and e.get("a") == trace.get("maker"):
            trace["maker_died"] = [e["t"], e.get("cause")]
        if e["k"] == "knowledge_lost" and e.get("thing") == traced:
            trace["lost"] = e["t"]


REAL_DECIDE, REAL_HOLD, REAL_JUDGE = mind.decide, actions._hold_in_fire, knowhow.judge_item
mind.decide, actions._hold_in_fire, knowhow.judge_item = watched_decide, watched_hold, watched_judge


def main():
    w = World(Config(seed=seed))
    w.observers.append(watch_events)
    same = None
    for y in range(years):
        for _ in range(WEEKS_PER_YEAR):
            w.step()
        if y + 1 == 100:
            saved = json.loads(gzip.open(HERE / "output" / "e6" / f"seed_{seed}_year100.json.gz").read())["world"]
            same = json.dumps(json.loads(json.dumps(w.to_dict())), sort_keys=True) == json.dumps(saved, sort_keys=True)
        if not w.living():
            break
    maker = w.people.get(trace.get("maker")) if trace.get("maker") else None
    out = {"seed": seed, "traced": traced, "years": years, "replay_matches_year100": same,
           "opportunities": {k: {"adult_weeks": opp[k], "step_among_top_choices": in_mind[k], "step_taken": took[k],
                                 "chosen_instead": dict(chose.get(k, Counter()).most_common(6)),
                                 "scores_when_considered": ranks.get(k, [])[:20]} for k in opp},
           "held_in_fire": heated,
           "maker": None if maker is None else {
               "id": maker.id, "name": maker.name, "genes": {g: round(v, 2) for g, v in maker.genes.items()},
               "born_tick": maker.birth, "died": trace.get("maker_died")},
           "trace": trace}
    (HERE / "output" / f"autopsy_{seed}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k not in ("trace", "held_in_fire")}, indent=1)[:6000])
    print("held in fire:", heated[:20])
    print("traced events:", trace["events"][:20])
    print("uses:", trace["uses"][:20])


if __name__ == "__main__":
    main()
