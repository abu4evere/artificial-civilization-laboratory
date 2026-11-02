"""UP1 — why is a new kind never made again? (questions.md, frozen as `UP1-frozen`). Read-only on `code_v11`.
At every adult decision, the observer reproduces the make choice of `mind.decide` for every kind the person knows and
records the first blocking step: 1 holding (as the code skips), 2 value floor, 3 cannot make, 4a skipped by the running
best, 4b beaten, 5 eligible but not chosen, or made. It checks that its reproduced make option equals the one the code
offered (mismatch 0). New kinds: world-new kinds made in play in years 100-195; old kinds: first made before year 100.

  python experiments/UP1_uptake_of_new_kinds/run_up1.py zero
  python experiments/UP1_uptake_of_new_kinds/run_up1.py one c <seed> <years> <out>
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

CODE = "v11"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(22101, 22133))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9929, 9928)
ARMS = {"c": dict(base.LP)}
JOBS = [f"c:{s}" for s in SEEDS]
OUT = HERE / "output"
ADULT = 16 * WPY
LATE = [100 * WPY, 200 * WPY]
STEPS = ("1", "2", "3", "4a", "4b", "5", "made")


class UP1Obs:
    def __init__(self, w):
        self.w = w
        self.mismatch = Counter()
        self.played = set()                                    # world-new kinds made in play
        self.steps = defaultdict(lambda: [0] * 7)              # "new|old" + "|nested|simple" + "|early|later"
        self.per_kind = defaultdict(lambda: [0] * 7)           # new kinds: sig -> step counts
        self.p5 = {"new": [0, 0.0], "old": [0, 0.0]}           # eligible decisions, sum of make probability
        self.winner = Counter()                                # step 4 for new kinds: the winner is "new"/"old"/"other"
        self.pending = {}
        self.s = Counter()

    def cls(self, world, sig):
        rec = world.knowledge.get(sig)
        if rec is None:
            return None
        t = rec["first_tick"]
        if t < LATE[0]:
            return "old"
        if sig in self.played and t <= LATE[1] - 5 * WPY:
            return "new"
        return None

    @staticmethod
    def nested(recipe):
        from acl.matter import MATERIALS
        if recipe.get("verb") == "bind":
            return any(x not in MATERIALS for x in recipe["parts"])
        return recipe.get("verb") == "heat" and recipe["part"] not in MATERIALS

    def classify(self, world, p, steered):
        """Reproduce the make block of `mind.decide` (same order, same conditions) and record each kind's step."""
        from acl import inquiry
        from acl.knowhow import belief
        from acl.mind import COST, _holding, _wanted_parts, can_make, hunger_of
        c = world.cfg
        tick = world.tick
        offered = [o for o in steered if o[1] == "make"]
        off_t = offered[0][2] if offered else None
        st = p.stage(tick)
        if st not in ("teen", "adult", "elder"):
            if off_t is not None:
                self.mismatch["make_offered_to_child"] += 1
            return
        deps = world.dependents(p.id)
        hunger = hunger_of(world, p, sum(d.need(c, tick) for d in deps))
        fire_here = world.tile(p.loc).fire > 0
        part_of = _wanted_parts(p)
        g = p.genes
        best, best_u = None, 0.05
        info = []
        for sig, recipe in p.recipes.items():
            heat_blocked = recipe["verb"] == "heat" and not fire_here
            v = max(p.itemval.get(sig, 0.0), part_of.get(sig, 0.0))
            if recipe["verb"] == "strike":
                v = max(v, belief(p, f"{recipe['target']}/{recipe['tool']}@{world.season}") or 0.0)
            v = max(v, 0.5 * max(inquiry.pull(p, "m:" + sig), inquiry.pull(p, "f:" + sig)))
            hold = _holding(p, sig) and v == p.itemval.get(sig, 0.0)
            canm = (not heat_blocked) and can_make(p, recipe)
            run_skip = v <= best_u and best_u > 0.05
            if not heat_blocked and not (v <= best_u or hold or not can_make(p, recipe)):
                u = c.worth_weight * v * (0.6 + 0.4 * g["diligence"]) * (1.0 - 0.5 * hunger)
                if u > best_u:
                    best, best_u = sig, u
            info.append((sig, recipe, v, hold, canm, run_skip))
        expect = best if (best is not None and p.energy >= COST["make"]) else None
        if expect != off_t:
            self.mismatch["make_option"] += 1
        if p.age(tick) < ADULT or not (LATE[0] <= tick < LATE[1]):
            return
        pm = 0.0
        if offered:
            top = max(o[0] for o in steered)
            ws = [math.exp((o[0] - top) / c.choice_temperature) for o in steered]
            pm = ws[steered.index(offered[0])] / sum(ws)
        rec = []
        for sig, recipe, v, hold, canm, run_skip in info:
            k = self.cls(world, sig)
            if k is None:
                continue
            if hold:
                step = 0
            elif v <= 0.05:
                step = 1
            elif not canm:
                step = 2
            elif sig != best:
                step = 3 if run_skip else 4
                if k == "new" and best is not None:
                    self.winner[self.cls(world, best) or "other"] += 1
            else:
                step = 5
            early = "early" if k == "new" and tick - world.knowledge[sig]["first_tick"] < 5 * WPY else "later"
            key = f"{k}|{'nested' if self.nested(recipe) else 'simple'}|{early}"
            rec.append((sig, k, key, step, pm if step == 5 else None))
        self.pending[p.id] = rec

    def decided(self, world, p, chosen):
        rec = self.pending.pop(p.id, None)
        if not rec:
            return
        made = chosen[0] == "make"
        for sig, k, key, step, pm in rec:
            if step == 5 and made and chosen[1] == sig:
                step = 6
            if step in (5, 6):
                self.p5[k][0] += 1
                self.p5[k][1] += pm or 0.0
            self.steps[key][step] += 1
            if k == "new":
                self.per_kind[sig][step] += 1
            self.s["classified"] += 1

    def __call__(self, world, events):
        pass

    def results(self):
        new_kinds = [s for s in self.played if self.cls(self.w, s) == "new"]
        return {"steps_fields": list(STEPS), "steps": dict(self.steps),
                "per_kind": {s: self.per_kind.get(s, [0] * 7) for s in new_kinds},
                "p5_fields": ["eligible decisions", "sum make probability"], "p5": self.p5,
                "winner": dict(self.winner), "mismatch": dict(self.mismatch), "sums": dict(self.s)}


def install(w, obs):
    from acl import decision, knowhow, thought
    o_steer, o_decide, o_remember = thought.steer, decision.decide, knowhow.remember_recipe

    def steer(p, options):
        out = o_steer(p, options)
        if w.people.get(p.id) is p:
            obs.classify(w, p, out)
        return out

    def decide(world, p):
        d = o_decide(world, p)
        if world is w:
            obs.decided(world, p, d.chosen)
        return d

    def remember_recipe(world, p, sig, recipe, how, source=None, props=None, meant=None):
        new = sig not in world.knowledge
        out = o_remember(world, p, sig, recipe, how, source, props, meant)
        if world is w and new and how == "made":
            obs.played.add(sig)
        return out

    thought.steer = steer
    decision.decide = decide
    knowhow.remember_recipe = remember_recipe


def hashrun(seed, years, observe):
    LATE[0], LATE[1] = 0, years * WPY       # zero checks: every year counted
    base.setup(CODE)
    w = base.make_world(seed, ARMS["c"])
    obs = None
    if observe:
        obs = UP1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results()
        tot = [sum(v[i] for v in r["steps"].values()) for i in range(7)]
        extra = ":" + json.dumps({**obs.mismatch, "_classified": obs.s["classified"], "_steps": tot,
                                  "_new_kinds": len(r["per_kind"])}, sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.split()[-1]

    def hs(x):
        return x.split(":")[:2]
    lines, ok = [], True
    from concurrent.futures import ThreadPoolExecutor
    specs = [(seed, years, o) for seed, years in ((501, 20), (601, 60)) for o in (0, 1)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        off, on = got[(seed, years, 0)], got[(seed, years, 1)]
        ro = hs(off) == hs(on)
        info = json.loads(on.split(":", 2)[2])
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = ro and not any(mism.values()) and info["_classified"] > 0
        ok &= t
        lines.append(f"seed {seed}, {years} years: observer read-only: {'yes' if ro else 'NO'}; reproduced make option "
                     f"= the code's at every decision, and no make offered to a child (mismatches): {mism or 'none'}; "
                     f"person x kind x decisions classified {info['_classified']}; by step {dict(zip(STEPS, info['_steps']))}; "
                     f"new kinds {info['_new_kinds']}")
    lines.append(f"code_v11 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = base.make_world(seed, ARMS[arm])
    obs = UP1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_v11", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, mismatches {res['mismatch']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4] == "1"))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: every year counted; never study data
        LATE[0], LATE[1] = 0, int(sys.argv[4]) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
