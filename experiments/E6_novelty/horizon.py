"""E6.6 (watch-only): the effective reward horizon of agents, in today's code (code_baseline, = the live world).

Replays a world from week 1 with probes that only read, and records every time an outcome changed what a person
had learned, with the delay back to the act it credited:
- beliefs about leaving things in places (sowing, stashing, heaping): every credit, the weeks since that thing was
  left at that spot, and which experience gave the credit (returning to see the spot, food kept or gone, a warm
  place in the cold);
- made things: weeks from making a thing to first using it, and whether the maker made it again;
- habits: each person's weekly reward, to set the size of a delayed reward against the noise of ordinary weeks.
Then: did a credited act get repeated? (a belief that moved, followed by the same act in the next year)

Usage: python experiments/E6_novelty/horizon.py <seed> [years]   -> output/horizon_<seed>.json
"""
from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "code_baseline"))

from acl import biology, knowhow  # noqa: E402
from acl.config import WEEKS_PER_YEAR, Config  # noqa: E402
from acl.world import World  # noqa: E402

seed = int(sys.argv[1])
years = int(sys.argv[2]) if len(sys.argv) > 2 else 150
W = {"credits": [], "puts": [], "makes": {}, "uses": {}}
RW = [0, 0.0, 0.0]         # count, sum, sum of squares of weekly habit rewards
CHANNEL = [None]


def w_credit(world, p, key, change):
    spots = [pl[0] for pl in p.placements if pl[3] == key and (pl[1], pl[2]) == tuple(p.loc)]
    delay = world.tick - max(spots) if spots else None
    W["credits"].append([world.tick, p.id, key, round(change, 4), delay, CHANNEL[0]])
    return R_CREDIT(world, p, key, change)


def w_look_around(world, p):
    CHANNEL[0] = "returned to the spot"
    try:
        return R_LOOK(world, p)
    finally:
        CHANNEL[0] = None


def w_associate(world, p, loc, surprise, weight=1.0):
    caller = sys._getframe(1).f_code.co_name
    CHANNEL[0] = {"_take": "food left there (kept or gone)", "body_phase": "warm or cold there"}.get(caller, caller)
    try:
        return R_ASSOC(world, p, loc, surprise, weight)
    finally:
        CHANNEL[0] = None


def w_judge(world, p, sig, felt):
    u = W["uses"].setdefault(f"{p.id}|{sig}", [world.tick, 0])
    u[1] += 1
    return R_JUDGE(world, p, sig, felt)


def w_learn(world, p):
    r = p.reward + 2.0 * (p.mood - p.mood_before)
    RW[0] += 1
    RW[1] += r
    RW[2] += r * r
    return R_LEARN(world, p)


def watch(world, events):
    for e in events:
        if e["k"] == "put" and e.get("a"):
            W["puts"].append([e["t"], e["a"], f"{e['thing']}@{(e['t'] % WEEKS_PER_YEAR) // 13}"])
        elif e["k"] in ("make", "play") and e.get("thing") and e.get("a"):
            W["makes"].setdefault(f"{e['a']}|{e['thing']}", []).append(e["t"])


R_CREDIT, R_LOOK, R_ASSOC = knowhow._credit, knowhow.look_around, knowhow.associate
R_JUDGE, R_LEARN = knowhow.judge_item, biology._learn
knowhow._credit, knowhow.look_around, knowhow.associate = w_credit, w_look_around, w_associate
knowhow.judge_item, biology._learn = w_judge, w_learn


def main():
    w = World(Config(seed=seed))
    w.observers.append(watch)
    same = None
    for y in range(years):
        for _ in range(WEEKS_PER_YEAR):
            w.step()
        if y + 1 == 100:
            saved = json.loads(gzip.open(HERE / "output" / "baseline" / f"seed_{seed}_year100.json.gz").read())["world"]
            same = json.dumps(json.loads(json.dumps(w.to_dict())), sort_keys=True) == json.dumps(saved, sort_keys=True)
        if not w.living():
            break
    mean = RW[1] / RW[0]
    out = {"seed": seed, "years": years, "replay_matches_year100": same,
           "reward_sd": (RW[2] / RW[0] - mean * mean) ** 0.5, "reward_mean": mean, "n_rewards": RW[0], **W}
    (HERE / "output" / f"horizon_{seed}.json").write_text(json.dumps(out), encoding="utf-8")
    print(seed, "credits", len(W["credits"]), "puts", len(W["puts"]), "makes", len(W["makes"]),
          "uses", len(W["uses"]), "replay ok", same)


if __name__ == "__main__":
    main()
