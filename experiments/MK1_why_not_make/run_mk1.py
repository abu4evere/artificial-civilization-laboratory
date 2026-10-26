"""MK1 — why do people who can make, and weigh making, not choose it? (questions.md with draft revision 1, frozen as
`MK1-frozen`). Read-only: live nature v7 (`code_v7`) unchanged, with a logging observer and read-only wrappers that
read state at the moment the world uses it and then call the original, unchanged:

- `thought.steer` (every option's score before and after the thought's pull, so the full softmax is known);
- the forage action (the tool in hand and the food it was owed, as LS1).

For each person-week the observer replays, read-only, the decision's own loop over recipes (`mind.decide`, the
"make" block) to tell why making was or was not offered, and splits making's score into its parts:
worth term = worth_weight × v × (0.6 + 0.4 × diligence) × (1 − 0.5 × hunger); habit = learned_weight × the habit value;
thought = the steer bonus. Two internal checks must be exact: the replayed offer equals the decision's, and the
replayed worth term equals the score the decision gave (mismatch counters, which must be 0).

  python experiments/MK1_why_not_make/run_mk1.py zero    # hard stops (writes output/zero.txt)
  python experiments/MK1_why_not_make/run_mk1.py one <arm> <seed> <years> <out>    # one world (cloud-run)
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODE = EXP / "NV7_nature_v7" / "code_v7"
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(18201, 18233))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9959, 9958)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
ARMS = {"lp": {"founders": 80, "width": 80, "height": 80}}
JOBS = [f"lp:{s}" for s in SEEDS]
BIN_EDGES = (0, 5, 10, 20, 50, 100, 200)  # years (LS1's bins up to 200)
HORIZONS = (13, 26, 52, 104)              # weeks, for a tool's cumulative benefit
T = 0.2                                   # choice_temperature (checked against the config at start)


def bin_of(tick):
    y = tick / WPY
    for i in range(len(BIN_EDGES) - 1):
        if y < BIN_EDGES[i + 1]:
            return i
    return len(BIN_EDGES) - 2


def band(x, edges):
    for i, e in enumerate(edges):
        if x < e:
            return i
    return len(edges)


HUNGER_EDGES = (0.25, 0.5, 0.75)          # hunger bands 0-3
FOOD_EDGES = (0.5, 2.0)                   # food on the person's tile, in weeks of their need: 0-2
SKILL_EDGES = (0.1, 0.2, 0.35, 0.5)       # crafting skill bands 0-4


def setup():
    sys.path.insert(0, str(CODE))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **{**V7, **kw}))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def rng_state(w):
    return hashlib.sha256(repr(w.rng.getstate()).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODE / "acl")


def forage_factor(props):
    from acl.matter import factor
    if not props or "edge" not in props:
        return 1.0
    return factor(props, "forage")


# --- the observer -----------------------------------------------------------------------------------------------

class MK1Obs:
    """Read-only. Per person-week (teens and up): the offer gate, the full softmax, making's score parts, all summed
    into matched-state cells; every deliberate making, and the forage tools it produced, followed."""

    def __init__(self, w):
        self.w = w
        c = w.cfg
        assert abs(c.choice_temperature - T) < 1e-12
        self.cells = defaultdict(lambda: defaultdict(float))   # "bin|age|hunger|tool|food|skill" -> sums
        self.beaten = defaultdict(Counter)                      # bin -> winning action when offered, not chosen
        self.week = {}                                          # pid -> this week's record (from steer)
        self.makes = []                                         # every deliberate making
        self.pending_worth = []                                 # (tick due, index into makes, pid, sig, slot)
        self.tools = {}                                         # id(item) -> record of a forage tool made
        self.mismatch = Counter()
        self.pop = defaultdict(float)                           # bin -> person-weeks (all), adults

    # -- the replay of the decision's "make" block (mind.decide), read-only --
    def replay(self, world, p, hunger):
        from acl import inquiry
        from acl.knowhow import belief
        from acl.mind import COST, MOVE_COST, _holding, _wanted_parts, can_make
        c = world.cfg
        g = p.genes
        season = world.season
        best, best_u, best_v = None, 0.05, None
        fire_here = world.tile(p.loc).fire > 0
        part_of = _wanted_parts(p)
        feasible = low = held = False
        for sig, recipe in p.recipes.items():
            if recipe["verb"] == "heat" and not fire_here:
                continue
            ok = can_make(p, recipe)
            feasible |= ok
            v = max(p.itemval.get(sig, 0.0), part_of.get(sig, 0.0))
            if recipe["verb"] == "strike":
                v = max(v, belief(p, f"{recipe['target']}/{recipe['tool']}@{season}") or 0.0)
            v = max(v, 0.5 * max(inquiry.pull(p, "m:" + sig), inquiry.pull(p, "f:" + sig)))
            if ok:
                if v <= 0.05:
                    low = True
                elif _holding(p, sig) and v == p.itemval.get(sig, 0.0):
                    held = True
            if v <= best_u or (_holding(p, sig) and v == p.itemval.get(sig, 0.0)) or not ok:
                continue
            u = c.worth_weight * v * (0.6 + 0.4 * g["diligence"]) * (1.0 - 0.5 * hunger)
            if u > best_u:
                best, best_u, best_v = sig, u, v
        tired = best is not None and p.energy < COST["make"] + MOVE_COST * 0
        return feasible, best, best_u, best_v, low, held, tired

    def on_options(self, world, p, before, after):
        from acl.matter import best_item
        from acl.mind import hunger_of
        from acl.person import A, N_ACTIONS
        tick = world.tick
        st = p.stage(tick)
        if st not in ("teen", "adult", "elder"):
            return
        c = world.cfg
        dep_need = sum(d.need(c, tick) for d in world.dependents(p.id))
        hunger = hunger_of(world, p, dep_need)
        feasible, sig, u_rep, v, low, held, tired = self.replay(world, p, hunger)
        mk_before = [o for o in before if o[1] == "make"]
        mk_after = [i for i, o in enumerate(after) if o[1] == "make"]
        offered = bool(mk_after)
        predicted = sig is not None and not tired
        if offered != predicted:
            self.mismatch["offer"] += 1
        habit = c.learned_weight * p.q[p.last_ctx * N_ACTIONS + A["make"]]
        age = p.age(tick)
        _, tool_f = best_item(p, "forage")
        tile = world.tile(p.loc)
        need = p.need(c, tick)
        key = "|".join(map(str, (bin_of(tick), "teen" if age < 16 * WPY else "adult", band(hunger, HUNGER_EDGES),
                                 int(tool_f > 1.0), band((tile.plants + tile.crop) / need, FOOD_EDGES),
                                 band(p.skills["crafting"], SKILL_EDGES))))
        rec = {"key": key, "offered": offered, "sig": sig, "v": v}
        cell = self.cells[key]
        cell["pw"] += 1
        cell["feasible"] += feasible
        if feasible and not offered:
            cell["no_offer_tired" if tired else ("no_offer_held" if held and not low else
                                                 ("no_offer_low" if low and not held else "no_offer_lowheld"))] += 1
        if offered:
            i = mk_after[0]
            u_m = after[i][0]
            uw = mk_before[0][0] - habit
            if abs(uw - u_rep) > 1e-9:
                self.mismatch["worth_term"] += 1
            th = u_m - mk_before[0][0]
            others = [o[0] for k, o in enumerate(after) if k != i]
            if others:
                top = max(others)
                u_other = top + T * math.log(sum(math.exp((x - top) / T) for x in others))
            else:
                u_other = -math.inf
            gap = u_m - u_other
            prob = 1.0 / (1.0 + math.exp(-gap / T)) if others else 1.0
            D = 0.6 + 0.4 * p.genes["diligence"]
            H = 1.0 - 0.5 * hunger
            cell["offered"] += 1
            cell["sum_p"] += prob
            cell["sum_logit"] += gap / T if others else 0.0
            cell["sum_uw"] += uw
            cell["sum_v"] += v
            cell["sum_D"] += D
            cell["sum_H"] += H
            cell["sum_hab"] += habit
            cell["sum_th"] += th
            cell["sum_uo"] += u_other if others else 0.0
            cell["top_make"] += u_m >= max(others, default=-math.inf)
            rec["skill"] = p.skills["crafting"]
        self.week[p.id] = rec

    def on_forage(self, world, p, f, got, item):
        rec = self.week.get(p.id)
        if rec is not None and p.age(world.tick) >= 16 * WPY:
            cell = self.cells[rec["key"]]
            cell["forage_acts"] += 1
            cell["forage_got"] += got
        if f > 1.0 and item is not None:
            t = self.tools.get(id(item))
            if t is not None and t["obj"] is item and t["censor"] is None:
                owed = got * (1.0 - 1.0 / f)
                age = world.tick - t["made"]
                t["uses"] += 1
                t["owed"] += owed
                for k, hz in enumerate(HORIZONS):
                    if age < hz:
                        t["owed_h"][k] += owed

    # -- the week --
    def __call__(self, world, events):
        tick = world.tick - 1
        bi = bin_of(tick)
        living = world.living()
        self.pop[f"{bi}|pw"] += len(living)
        self.pop[f"{bi}|adults"] += sum(1 for p in living if p.age(world.tick) >= 16 * WPY)
        chosen = {}
        for dcs in world.week_decisions:
            chosen[dcs.agent_id] = dcs.chosen[0] if dcs.chosen else None
        made = defaultdict(list)
        for e in events:
            if e.get("k") == "make" and e.get("thing"):
                made[e["a"]].append(e["thing"])
        for pid, rec in self.week.items():
            p = world.people.get(pid)
            if p is None:
                continue
            act = chosen.get(pid)
            cell = self.cells[rec["key"]]
            if rec["offered"]:
                if act == "make":
                    cell["chosen"] += 1
                else:
                    self.beaten[bi][act] += 1
            for sig in made.get(pid, ()):
                props = (world.knowledge.get(sig) or {}).get("props")
                ff = forage_factor(props)
                idx = len(self.makes)
                self.makes.append([tick, pid, int(p.birth < 0), round(p.age(world.tick) / WPY, 2),
                                   round(p.skills["crafting"], 4), sig, round(ff, 4),
                                   rec.get("v") if rec.get("sig") == sig else None,
                                   round(p.itemval.get(sig, 0.0), 4), None, None, rec["key"]])
                for slot, wk in ((9, 13), (10, 52)):
                    self.pending_worth.append((world.tick + wk, idx, pid, sig, slot))
                if ff > 1.0:
                    known = {id(t["obj"]) for t in self.tools.values() if t["obj"] is not None}
                    for it in p.items:
                        if it["sig"] == sig and id(it) not in known and id(it) not in self.tools:
                            self.tools[id(it)] = {"obj": it, "maker": pid, "made": world.tick, "ff": round(ff, 4),
                                                  "skill": round(p.skills["crafting"], 4), "key": rec["key"],
                                                  "uses": 0, "owed": 0.0, "owed_h": [0.0] * len(HORIZONS),
                                                  "censor": None, "why": None}
                            break
        self.week = {}
        # the worth a maker holds for what they made, 13 and 52 weeks later
        if self.pending_worth:
            keep = []
            for due, idx, pid, sig, slot in self.pending_worth:
                if due <= world.tick:
                    q = world.people.get(pid)
                    self.makes[idx][slot] = round(q.itemval.get(sig, 0.0), 4) if q is not None and q.alive else None
                else:
                    keep.append((due, idx, pid, sig, slot))
            self.pending_worth = keep
        # tools: censored when the maker no longer holds them or has died
        for t in self.tools.values():
            if t["censor"] is not None:
                continue
            q = world.people.get(t["maker"])
            if q is None or not q.alive:
                t["censor"], t["why"] = world.tick, "died"
            elif not any(it is t["obj"] for it in q.items):
                t["censor"], t["why"] = world.tick, "not held"
        for t in self.tools.values():
            if t["censor"] is not None and t["obj"] is not None:
                t["obj"] = None                         # free the reference once followed to its end

    def results(self):
        tools = [[t["maker"], t["made"], t["ff"], t["skill"], t["key"], t["uses"], round(t["owed"], 4),
                  [round(x, 4) for x in t["owed_h"]], t["censor"], t["why"]] for t in self.tools.values()]
        return {"cells": {k: dict(v) for k, v in self.cells.items()},
                "beaten": {str(k): dict(v) for k, v in self.beaten.items()},
                "makes": self.makes, "tools": tools, "pop": dict(self.pop), "mismatch": dict(self.mismatch)}


def install(w, obs):
    """The read-only wrappers. Each reads before and after and calls the original unchanged."""
    from acl import actions, thought
    orig_steer, orig_forage = thought.steer, actions._forage

    def steer(p, options):
        before = list(options)
        out = orig_steer(p, options)
        if w.people.get(p.id) is p:
            obs.on_options(w, p, before, out)
        return out

    def forage(world, p, target, eff):
        if world is w:
            from acl.matter import best_item
            i, f = best_item(p, "forage")
            item = p.items[i] if i >= 0 else None
            before = p.food + p.seeds
            orig_forage(world, p, target, eff)
            obs.on_forage(world, p, f, p.food + p.seeds - before, item)
            return
        return orig_forage(world, p, target, eff)

    thought.steer = steer
    actions._forage = forage
    if hasattr(actions, "HANDLERS"):
        actions.HANDLERS = {k: (forage if v is orig_forage else v) for k, v in actions.HANDLERS.items()}


# --- zero checks --------------------------------------------------------------------------------------------------

def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    if observe:
        obs = MK1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        extra = ":" + json.dumps({**obs.mismatch, "_offered": sum(c.get("offered", 0) for c in obs.cells.values()),
                                  "_tools": len(obs.tools)}, sort_keys=True, separators=(",", ":"))
    return world_hash(w) + ":" + rng_state(w) + extra


def reload_check(seed):
    setup()
    from acl.world import World
    a = make_world(seed, ARMS["lp"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for x in (a, b):
        for _ in range(5 * WPY):
            x.step()
    return world_hash(a) == world_hash(b)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for seed, years in ((501, 20), (601, 60)):
        a = call("hashrun", "lp", seed, years, 1)
        b = call("hashrun", "lp", seed, years, 0)
        same = a.split(":")[:2] == b.split(":")[:2]
        info = json.loads(a.split(":", 2)[2]) if a.count(":") >= 2 else {"?": 1}
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = same and not any(mism.values()) and info.get("_offered", 0) > 0 and info.get("_tools", 0) > 0
        ok &= t
        lines.append(f"arm lp, seed {seed}, {years} years: identical with and without the observer (state and random "
                     f"numbers): {'yes' if same else 'NO'}; replay mismatches (offer, worth term): {mism or 'none'}; "
                     f"offered person-weeks {info.get('_offered')}, forage tools followed {info.get('_tools')}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm lp, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_v7 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = MK1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v7", "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "world_hash": world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, mismatches {dict(obs.mismatch)}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "fp":
        setup()
        print(fingerprint())
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
