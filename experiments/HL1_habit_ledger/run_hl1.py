"""HL1 — where do the habits come from? (questions.md, frozen as `HL1-frozen`). Read-only: live nature v7 (`code_v7`)
unchanged, with wrappers that read state before and after and call the original unchanged:
`biology._learn` (own TD), `actions._imitate` (copying in talk), `biology._upbringing` (carer), `biology._born`
(birth), `actions._give` (paid back), and `thought.steer` (as CO1, for Q1).

Every person keeps, for every habit entry, components by route that add up to the value. An update
q <- q + k(target - q) shrinks the existing components by (1 - k) and adds the rest to its own route.

  python experiments/HL1_habit_ledger/run_hl1.py zero
  python experiments/HL1_habit_ledger/run_hl1.py one <arm> <seed> <years> <out>
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
SEEDS = tuple(range(18601, 18633))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9951, 9950)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
ARMS = {"lp": {"founders": 80, "width": 80, "height": 80}}
JOBS = [f"lp:{s}" for s in SEEDS]
BIN_EDGES = (0, 5, 10, 20, 50, 100, 200)
ROUTES = ("td", "talk", "carer", "birth", "paid")
T = 0.2
HUNGER_EDGES = (0.25, 0.5, 0.75)
FOOD_EDGES = (0.5, 2.0)


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


def lse(xs):
    top = max(xs)
    return top + T * math.log(sum(math.exp((x - top) / T) for x in xs))


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


class HL1Obs:
    def __init__(self, w):
        from acl.person import ACTIONS, N_ACTIONS
        self.w = w
        self.N = N_ACTIONS
        self.acts = ACTIONS
        self.comp = {}                                 # pid -> {route: [floats]}
        self.cells = defaultdict(lambda: defaultdict(float))    # Q1, CO1's cells
        self.flows = defaultdict(lambda: defaultdict(float))    # Q2-Q4: bin -> counters
        self.week = {}
        self.mismatch = Counter()
        for p in w.living():
            self._init(p, "birth")

    def _init(self, p, route):
        n = len(p.q)
        self.comp[p.id] = {r: ([float(x) for x in p.q] if r == route else [0.0] * n) for r in ROUTES}

    def _comps(self, p):
        c = self.comp.get(p.id)
        if c is None:
            self._init(p, "birth")
            c = self.comp[p.id]
            self.mismatch["unseen_person"] += 1
        return c

    def _blend(self, p, before, after, other, route, b):
        """after = before + k(other - before) for every entry (k inferred); components shrink by 1-k."""
        k = None
        for i in range(len(before)):
            d = other[i] - before[i]
            if abs(d) > 1e-9:
                k = (after[i] - before[i]) / d
                break
        if k is None:
            return
        c = self._comps(p)
        for r in ROUTES:
            ci = c[r]
            for i in range(len(ci)):
                ci[i] *= (1.0 - k)
        add = c[route]
        for i in range(len(add)):
            add[i] += after[i] - (1.0 - k) * before[i]
        for i in range(len(before)):
            if abs(after[i] - before[i]) > 0:
                a = self.acts[i % self.N]
                b[f"{route}_d:{a}"] += after[i] - before[i]
        b[f"{route}_n"] += 1
        return k

    # -- wrapper hooks --
    def on_learn(self, world, p, i, before, after, r, fut):
        c = self._comps(p)
        alpha = world.cfg.learning_rate
        for rt in ROUTES:
            c[rt][i] *= (1.0 - alpha)
        c["td"][i] += after - (1.0 - alpha) * before
        unclipped = before + alpha * (r + world.cfg.discount * fut - before)
        if abs(max(-1.5, min(1.5, unclipped)) - after) > 1e-12:
            self.mismatch["td_replay"] += 1
        b = self.flows[bin_of(world.tick)]
        a = self.acts[i % self.N]
        b[f"td_n:{a}"] += 1
        b[f"td_d:{a}"] += after - before
        b[f"td_r:{a}"] += r
        b[f"td_f:{a}"] += fut
        b[f"td_clip:{a}"] += abs(unclipped) > 1.5
        if p.age(world.tick) >= 16 * WPY:                # operational note 1: adults only, for Q3
            b[f"atd_n:{a}"] += 1
            b[f"atd_r:{a}"] += r
            b[f"atd_f:{a}"] += fut

    def on_imitate(self, world, learner, model, before, after):
        b = self.flows[bin_of(world.tick)]
        k = self._blend(learner, before, after, model.q, "talk", b)
        if k is None:
            return
        rel = learner.rel.get(model.id)
        b["talk_for_respect" if rel and rel.respect >= 0.2 else "talk_for_mood"] += 1
        for i in range(len(before)):
            a = self.acts[i % self.N]
            b[f"talk_gap:{a}"] += model.q[i] - before[i]

    def on_upbringing(self, world, child, carer, before, after):
        self._blend(child, before, after, carer.q, "carer", self.flows[bin_of(world.tick)])

    def on_born(self, child):
        self._init(child, "birth")

    def on_paid(self, world, p, i, before, after):
        c = self._comps(p)
        c["paid"][i] += after - before
        b = self.flows[bin_of(world.tick)]
        b["paid_n"] += 1
        b[f"paid_d:{self.acts[i % self.N]}"] += after - before

    def on_options(self, world, p, before, after):
        from acl.matter import best_item
        from acl.mind import hunger_of
        from acl.person import A
        tick = world.tick
        if p.stage(tick) not in ("teen", "adult", "elder") or p.age(tick) < 16 * WPY:
            return
        mk = [i for i, o in enumerate(after) if o[1] == "make"]
        if not mk:
            return
        fam = defaultdict(list)
        for i, o in enumerate(after):
            if i != mk[0]:
                fam[o[1]].append(o[0])
        if not fam:
            return
        c = world.cfg
        L = {a: lse(xs) for a, xs in fam.items()}
        u_other = lse(list(L.values()))
        s = {a: math.exp((L[a] - u_other) / T) for a in L}
        base = p.last_ctx * self.N
        comps = self._comps(p)
        dep_need = sum(d.need(c, tick) for d in world.dependents(p.id))
        hunger = hunger_of(world, p, dep_need)
        _, tool_f = best_item(p, "forage")
        tile = world.tile(p.loc)
        need = p.need(c, tick)
        key = "|".join(map(str, (bin_of(tick), band(hunger, HUNGER_EDGES), int(tool_f > 1.0),
                                 band((tile.plants + tile.crop) / need, FOOD_EDGES))))
        cell = self.cells[key]
        cell["offered"] += 1
        lw = c.learned_weight
        total = 0.0
        for rt in ROUTES:
            v = lw * sum(s[a] * comps[rt][base + A[a]] for a in s)
            cell[f"hab_{rt}"] += v
            cell[f"make_{rt}"] += lw * comps[rt][base + A["make"]]
            total += v
        direct = lw * sum(s[a] * p.q[base + A[a]] for a in s)
        if abs(total - direct) > 1e-9:
            self.mismatch["q1_split"] += 1
        cell["hab_total"] += direct
        self.week[p.id] = 1

    def __call__(self, world, events):
        tick = world.tick - 1
        b = self.flows[bin_of(tick)]
        living = world.living()
        alive = {p.id for p in living}
        for pid in [x for x in self.comp if x not in alive]:
            del self.comp[pid]
        adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
        b["adult_pw"] += len(adults)
        for d in world.week_decisions:
            p = world.people.get(d.agent_id)
            if p is not None and p.age(world.tick) >= 16 * WPY and d.chosen:
                b[f"chosen:{d.chosen[0]}"] += 1
        if world.tick % 4 == 0:                        # mean habit per action (over situations), adults
            for p in adults:
                for a_i, a in enumerate(self.acts):
                    b[f"meanq:{a}"] += sum(p.q[a_i::self.N]) / (len(p.q) // self.N)
            b["meanq_n"] += len(adults)
        if world.tick % 520 == 0:                      # the ledger closes, for every living person and entry
            for p in living:
                c = self.comp.get(p.id)
                if c is None or not p.q:
                    continue
                for i in range(len(p.q)):
                    if abs(p.q[i] - sum(c[r][i] for r in ROUTES)) > 1e-9:
                        self.mismatch["ledger"] += 1
                        break

    def results(self):
        return {"cells": {k: dict(v) for k, v in self.cells.items()},
                "flows": {str(k): dict(v) for k, v in self.flows.items()}, "mismatch": dict(self.mismatch)}


def install(w, obs):
    from acl import actions, biology, thought
    from acl.mind import context_index
    from acl.person import A
    o_learn, o_imit, o_up, o_born, o_give, o_steer = (biology._learn, actions._imitate, biology._upbringing,
                                                      biology._born, actions._give, thought.steer)

    def learn(world, p):
        if world is not w or p.last_action is None:
            return o_learn(world, p)
        c = world.cfg
        i = p.last_ctx * obs.N + A[p.last_action]
        near = world.people_near(p.loc, c.reach, exclude=p.id)
        nxt = context_index(world, p, bool(near))
        fut = max(p.q[nxt * obs.N:(nxt + 1) * obs.N])
        r = p.reward + 2.0 * (p.mood - p.mood_before)
        before = p.q[i]
        out = o_learn(world, p)
        obs.on_learn(world, p, i, before, p.q[i], r, fut)
        return out

    def imitate(world, learner, model):
        if world is not w:
            return o_imit(world, learner, model)
        before = list(learner.q)
        out = o_imit(world, learner, model)
        if learner.q != before:
            obs.on_imitate(world, learner, model, before, list(learner.q))
        return out

    def upbringing(world, p):
        if world is not w:
            return o_up(world, p)
        before = list(p.q)
        carer = world.people.get(p.caregiver) if p.caregiver else None
        out = o_up(world, p)
        if carer is not None and p.q != before:
            obs.on_upbringing(world, p, carer, before, list(p.q))
        return out

    def born(world, mother, father, genes, name, sex, gen):
        child = o_born(world, mother, father, genes, name, sex, gen)
        if world is w:
            obs.on_born(child)
        return child

    def give(world, p, target, eff):
        if world is not w:
            return o_give(world, p, target, eff)
        q = world.people[target]
        i = q.last_ctx * obs.N + A["give"] if q.q else None
        before = q.q[i] if i is not None else None
        out = o_give(world, p, target, eff)
        if i is not None and q.q and q.q[i] != before:
            obs.on_paid(world, q, i, before, q.q[i])
        return out

    def steer(p, options):
        before = list(options)
        out = o_steer(p, options)
        if w.people.get(p.id) is p:
            obs.on_options(w, p, before, out)
        return out

    biology._learn = learn
    actions._imitate = imitate
    biology._upbringing = upbringing
    biology._born = born
    actions._give = give
    thought.steer = steer
    if hasattr(actions, "HANDLERS"):
        actions.HANDLERS = {k: (give if v is o_give else v) for k, v in actions.HANDLERS.items()}


def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = HL1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        res = obs.results()
        tdn = sum(v for b in res["flows"].values() for k, v in b.items() if k.startswith("td_n:"))
        extra = ":" + json.dumps({**res["mismatch"], "_td": tdn,
                                  "_talk": sum(b.get("talk_n", 0) for b in res["flows"].values()),
                                  "_offered": sum(c.get("offered", 0) for c in res["cells"].values())},
                                 sort_keys=True, separators=(",", ":"))
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
        t = same and not any(mism.values()) and info.get("_td", 0) > 0 and info.get("_talk", 0) > 0
        ok &= t
        lines.append(f"arm lp, seed {seed}, {years} years: identical with and without the observer (state and random "
                     f"numbers): {'yes' if same else 'NO'}; ledger, TD-replay and split mismatches: {mism or 'none'}; "
                     f"TD updates {info.get('_td')}, copying events {info.get('_talk')}, offered weeks {info.get('_offered')}")
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
    obs = HL1Obs(w)
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
