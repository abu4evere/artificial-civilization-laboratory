"""LA1 — why are lessons refused? (questions.md, frozen as `LA1-frozen`). Read-only: live nature v7 (`code_v7`) unchanged,
with one read-only wrapper on `information.hear_how` that reads every condition before the decision (including the
random draw, read from a copy of the generator's state, never consuming it) and calls the original unchanged.

  python experiments/LA1_lesson_acceptance/run_la1.py zero
  python experiments/LA1_lesson_acceptance/run_la1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import hashlib
import json
import random
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODE = EXP / "NV7_nature_v7" / "code_v7"
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(18701, 18733))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9949, 9948)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
ARMS = {"lp": {"founders": 80, "width": 80, "height": 80}}
JOBS = [f"lp:{s}" for s in SEEDS]
USES = ("forage", "hunt", "wood", "stone", "fiber", "fight", "carry", "cold")
ERAS = (50, 100, 200)
PARTS = ("base", "child", "health", "evidence", "overthink", "clamp")


def era_of(tick):
    y = tick / WPY
    for i, e in enumerate(ERAS):
        if y < e:
            return i
    return len(ERAS) - 1


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


def maxf(props):
    from acl.matter import factor
    if not props or "edge" not in props:
        return 1.0
    return max(factor(props, u) for u in USES)


def relation(world, teacher, learner):
    if teacher.id in (learner.mother, learner.father):
        return "parent"
    if learner.caregiver == teacher.id:
        return "carer"
    if world.kinship(teacher, learner) > 0:
        return "kin"
    return "other"


def age_band(weeks):
    y = weeks / WPY
    return "child" if y < 12 else ("teen" if y < 16 else "adult")


class LA1Obs:
    def __init__(self, w):
        self.w = w
        self.useful_cache = {}
        self.cells = defaultdict(lambda: defaultdict(float))     # "era|origin|useful|rel|age" -> sums
        self.early = defaultdict(lambda: [0.0, 0.0, 0.0, 0])     # (rel, age) -> sums of p, c, o, n (years 0-50)
        self.mismatch = Counter()
        self.depth = 0
        self.founder_kinds = set()                          # kinds first made by a founder (operational note 1)
        for p in w.living():
            self.founder_kinds.update(p.recipes)

    def useful(self, sig):
        if sig not in self.useful_cache:
            props = (self.w.knowledge.get(sig) or {}).get("props")
            if props is None:
                return False
            self.useful_cache[sig] = maxf(props) > 1.0
        return self.useful_cache[sig]

    def before(self, world, learner, teacher, meant, recipe, parent, part_lesson):
        from acl import thought
        from acl.config import CHILD_END
        from acl.information import _openness, _sig_of, credence, record
        from acl.knowhow import can_follow
        from acl.util import clamp
        sig = _sig_of(recipe)
        known = sig in learner.recipes
        holds = any(it["sig"] == meant for it in teacher.items)
        ev = 0.15 if holds else 0.0
        c = credence(world, learner, teacher, evidence=ev)
        r = learner.rel.get(teacher.id)
        trust = r.trust if r else 0.0
        respect = r.respect if r else 0.0
        goodwill = 0.35 + 0.45 * max(trust, 0.0) - 0.6 * max(-trust, 0.0) + 0.2 * respect
        est, n = record(learner, teacher.id)
        wgt = n / (n + 3.0)
        base = (1.0 - wgt) * goodwill + wgt * (0.05 + 0.95 * est)
        tick = world.tick
        child = 0.2 if (learner.age(tick) < CHILD_END and teacher.age(tick) >= CHILD_END) else 0.0
        health = 0.25 * (teacher.health / 100.0 - 0.7) - (0.1 if teacher.starving else 0.0)
        s = base + child + health + ev
        m = s * 0.6 if thought.state(learner) == "overthinking" else s
        c2 = clamp(m)
        if abs(c2 - c) > 1e-12:
            self.mismatch["credence_replay"] += 1
        o = _openness(learner, parent)
        own = learner.itemval.get(sig)
        bad = own is not None and own < -0.1 and ("m:" + sig) not in learner.heard
        follow = can_follow(learner, recipe)
        g = random.Random()
        g.setstate(world.rng.getstate())
        draw = g.random()
        return {"sig": sig, "known": known, "bad": bad, "follow": follow, "c": c, "o": o, "p": c * o, "draw": draw,
                "parts": {"base": base, "child": child, "health": health, "evidence": ev, "overthink": m - s,
                          "clamp": c2 - m}, "variant": sig != meant, "part_lesson": part_lesson}

    def after(self, world, learner, teacher, meant, info, before_set, result):
        tick = world.tick
        era = era_of(tick)
        origin = "founder" if meant in self.founder_kinds else "worldborn"
        usef = int(self.useful(meant))
        rel = relation(world, teacher, learner)
        age = age_band(learner.age(tick))
        key = f"{era}|{origin}|{usef}|{rel}|{age}"
        cell = self.cells[key]
        if info["part_lesson"]:
            cell["part_lessons"] += 1
            return
        cell["offered"] += 1
        cell["known"] += info["known"]
        cell["bad_any"] += info["bad"]
        cell["nofollow_any"] += not info["follow"]
        cell["variant"] += info["variant"]
        took_new = info["sig"] in learner.recipes and info["sig"] not in before_set
        # the gate actually reached, in the code's order
        if info["known"]:
            gate = "g1"
        elif info["bad"]:
            gate = "g2"
        elif info["draw"] >= info["p"]:
            gate = "g3"
        elif not info["follow"]:
            gate = "g4"
        else:
            gate = "taken"
        cell[gate] += 1
        if gate == "taken":
            cell["taken_exact"] += not info["variant"]
            cell["taken_pushed_out"] += not took_new        # operational note 1: memory full, pushed out at once
        if gate != "g4" and (gate == "taken") != bool(result):  # at G4 the code returns the part lesson's result
            self.mismatch["outcome"] += 1
        if gate in ("g3", "g4", "taken"):                  # reached G3: expectation terms
            p = info["p"]
            cell["reached_g3"] += 1
            cell["sum_p"] += p
            cell["sum_c"] += info["c"]
            cell["sum_o"] += info["o"]
            cell["sum_co"] += info["c"] * info["o"]
            cell["sum_pf"] += p * info["follow"]
            cell["p_lt05"] += p < 0.05
            cell["p_lt10"] += p < 0.10
            cell["p_lt20"] += p < 0.20
            for k, v in info["parts"].items():
                cell[f"cpart_{k}"] += v
            cell["parent_double"] += rel == "parent"
            if era == 0:
                e = self.early[(rel, age)]
                e[0] += p
                e[1] += info["c"]
                e[2] += info["o"]
                e[3] += 1
            elif era == 2:
                e = self.early.get((rel, age))
                if e and e[3]:
                    ep, ec, eo = e[0] / e[3], e[1] / e[3], e[2] / e[3]
                    cell["cf_p"] += ep * info["follow"]
                    cell["cf_c"] += ec * info["o"] * info["follow"]
                    cell["cf_o"] += info["c"] * eo * info["follow"]
                    cell["cf_n"] += 1
                    cell["cf_actual"] += p * info["follow"]
                else:
                    cell["cf_missing"] += 1
            cell["cf_nog4"] += p                            # (e) G4 removed: expectation with follow = 1
        if gate == "g1":
            cell["cf_nog1_extra"] += (0 if info["bad"] else info["p"] * info["follow"])   # (d) G1 removed
        cell["exp_taken"] += (0 if gate in ("g1", "g2") else info["p"] * info["follow"])

    def __call__(self, world, events):
        pass

    def results(self):
        return {"cells": {k: dict(v) for k, v in self.cells.items()}, "mismatch": dict(self.mismatch)}


def install(w, obs):
    from acl import information, knowhow
    orig = information.hear_how
    orig_rem = knowhow.remember_recipe

    def remember_recipe(world, p, sig, recipe, how, source=None, props=None, meant=None):
        if world is w and how in ("made", "heated") and sig not in world.knowledge and p.birth < 0:
            obs.founder_kinds.add(sig)
        return orig_rem(world, p, sig, recipe, how, source, props, meant)

    knowhow.remember_recipe = remember_recipe

    def hear_how(world, learner, teacher, meant, recipe, claim, parent, part_lesson=False):
        if world is not w:
            return orig(world, learner, teacher, meant, recipe, claim, parent, part_lesson)
        info = obs.before(world, learner, teacher, meant, recipe, parent, part_lesson)
        before_set = set(learner.recipes)
        out = orig(world, learner, teacher, meant, recipe, claim, parent, part_lesson)
        obs.after(world, learner, teacher, meant, info, before_set, out)
        return out

    information.hear_how = hear_how


def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = LA1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        res = obs.results()
        off = sum(c.get("offered", 0) for c in res["cells"].values())
        tk = sum(c.get("taken", 0) for c in res["cells"].values())
        extra = ":" + json.dumps({**res["mismatch"], "_offered": off, "_taken": tk}, sort_keys=True,
                                 separators=(",", ":"))
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
        t = same and not any(mism.values()) and info.get("_offered", 0) > 0 and info.get("_taken", 0) > 0
        ok &= t
        lines.append(f"arm lp, seed {seed}, {years} years: identical with and without the observer (state and random "
                     f"numbers): {'yes' if same else 'NO'}; credence-replay and outcome mismatches: {mism or 'none'}; "
                     f"lessons offered {info.get('_offered')}, taken {info.get('_taken')}")
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
    obs = LA1Obs(w)
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
    print(f"{arm} seed {seed}: done, tick {w.tick}, mismatches {res['mismatch']}", flush=True)


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
