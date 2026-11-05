"""PB1 — a shadow brain: can a small predictor learn what ACL's actions do? (questions.md, frozen as `PB1-frozen`).
Read-only on live nature v13 (`code_v13`). ES2's runner supplies the set-up (`../ES2_realized_lookahead/run_es2.py`).

The observer wraps decision.decide (read-only) to capture, for every person aged 16+ who decides in the followed
period, the inputs perceived at that decision and their state then; at the week's end it computes the 9-output vector
of changes. For each followed adult (born in years 60-100, age 16+), every predictor variant first predicts the week
(the prediction is scored), then learns from it (prequential). Observed weeks of others within perception are then
learned from by the observation variants, with the actor's hidden inputs replaced by the observer's own running means
and only the visible outputs updated.

Implementation notes (not choices about the measure):
  - outputs are standardised by a running, past-only mean and spread per world (Welford); a week is scored only after
    30 own weeks have entered those statistics in that world (burn-in), so that a spread exists;
  - the observed weeks of one observer in one week are applied as one batched update (the sum of their gradients);
  - amendment 1 (questions.md, before any study data): the spread has a floor of 0.05 raw units, and standardised
    values (truths, predictions and learning targets alike, for every variant) are clipped to +-10; an unfamiliar place
    is the action's destination tile never stood on.

  python experiments/PB1_shadow_predictor/run_pb1.py zero
  python experiments/PB1_shadow_predictor/run_pb1.py one c <seed> <years> <out>
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.CODES["v13"] = HERE.parent / "NV13_nature_v13" / "code_v13"
CODE = "v13"
WPY, YEARS = base.WPY, 120
SEEDS = tuple(range(23001, 23033))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9897, 9896)
ARMS = {"c": {**base.LP}}
JOBS = [f"c:{s}" for s in SEEDS]
OUT = HERE / "output"
ADULT = 16 * WPY
BORN = [60 * WPY, 100 * WPY]              # followed: born in years 60-100
COMMON = ("forage", "gather", "give", "talk", "put", "join", "rest", "take", "care", "make")
SOCIAL = ("give", "care", "talk", "court", "steal", "attack")
VARIANTS = ("B", "L", "N", "LO", "LO5", "NO")
OBS_W = {"LO": 1.0, "LO5": 0.5, "NO": 1.0}
NOUT = 9
VISIBLE = np.array([1, 0, 0, 0, 1, 1, 1, 1, 0], dtype=float)   # food gained, materials, things, distance, new kind
HIDDEN_IN = 4                            # the first 4 inputs: food weeks, health, energy, thirst
LR_L, LR_N, HID, BURN = 0.1, 0.01, 16, 30
STD_FLOOR, ZCLIP = 0.05, 10.0
CASES = ("all", "u_pair", "u_prop", "rare", "u_place", "w0", "w1", "w2", "w3")
WBANDS = (100, 500, 1000)


def setup_acl():
    from acl import fauna, matter, weather
    from acl.person import ACTIONS
    return fauna, matter, weather, ACTIONS


class Feat:
    """Builds the input vector perceived at a decision (all read-only queries)."""

    def __init__(self, world):
        fauna, matter, weather, ACTIONS = setup_acl()
        self.fauna, self.matter, self.weather = fauna, matter, weather
        self.ACT = {a: i for i, a in enumerate(ACTIONS)}
        self.NA = len(ACTIONS)
        self.MAT = matter.MATERIALS
        self.PROPS = matter.PROPS
        self.D = 4 + 3 + 1 + 2 + 4 + 1 + 1 + 3 + len(self.MAT) + 5 + 2 * self.NA + self.NA + 2 + 10 + 3 + 10 + 1 + 1

    def body(self, world, p):
        c, t = world.cfg, world.tick
        return [min(1.0, p.edible() / max(1e-9, p.need(c, t)) / 6.0), p.health / 100.0, p.energy / 100.0,
                float(p.thirst)]

    def __call__(self, world, p, action, target, last2):
        from acl.util import distance
        c, t = world.cfg, world.tick
        w, h = c.width, c.height
        x = self.body(world, p)
        st = p.stage(t)
        x += [1.0 if st == s else 0.0 for s in ("teen", "adult", "elder")]
        x.append(1.0 if p.sex == "F" else 0.0)
        mate = world.people.get(p.partner) if p.partner else None
        x.append(1.0 if mate is not None and mate.alive and distance(p.loc, mate.loc, w, h) <= c.reach else 0.0)
        x.append(1.0 if any(d.alive and distance(p.loc, d.loc, w, h) <= c.reach for d in world.dependents(p.id))
                 else 0.0)
        x += [1.0 if world.season == s else 0.0 for s in range(4)]
        x.append(1.0 if self.weather.raining(world, p.loc) else 0.0)
        x.append(min(1.0, len(world.people_near(p.loc, c.reach, exclude=p.id)) / 12.0))
        tile = world.tile(p.loc)
        x += [min(1.0, tile.plants / 10.0), 1.0 if self.weather.fresh_near(world, p.loc, c.perception) else 0.0,
              1.0 if tile.fire > 0 else 0.0]
        x += [min(1.0, tile.material(m) / 20.0) for m in self.MAT]
        if p.items:
            x += [max(it[k] for it in p.items) / 100.0 for k in ("edge", "reach", "hard", "contain")]
        else:
            x += [0.0, 0.0, 0.0, 0.0]
        x.append(min(1.0, len(p.items) / 3.0))
        for k in range(2):
            v = [0.0] * self.NA
            if len(last2) > k and last2[k] in self.ACT:
                v[self.ACT[last2[k]]] = 1.0
            x += v
        v = [0.0] * self.NA
        v[self.ACT[action]] = 1.0
        x += v
        tp = [0.0] * 2                    # target tile: plants, prey (forage, hunt)
        mp = [0.0] * 10                   # gather: the material's properties
        rp = [0.0] * 3                    # social: affection, trust, familiarity
        kp = [0.0] * 10                   # make: the result's known properties
        if action in ("forage", "hunt") and isinstance(target, (tuple, list)) and len(target) == 2:
            tt = world.tile(tuple(target))
            tp = [min(1.0, tt.plants / 10.0), min(1.0, self.fauna.prey_here(world, tuple(target)) / 20.0)]
        elif action == "gather" and isinstance(target, (tuple, list)) and len(target) == 2 and target[1] in self.MAT:
            mp = [v / 100.0 for v in self.matter.RAW[target[1]]]
        elif action in SOCIAL and isinstance(target, str):
            r = p.rel.get(target)
            if r is not None:
                rp = [float(r.affection), float(r.trust), float(r.familiarity)]
        elif action == "make" and isinstance(target, str):
            k = world.knowledge.get(target)
            props = k.get("props") if k else None
            if props:
                kp = [float(props.get(q, 0)) / 100.0 for q in self.PROPS]
        x += tp + mp + rp + kp
        x.append(0.0)                     # observed flag (0 = own week)
        x.append(1.0)                     # bias
        assert len(x) == self.D, (len(x), self.D)
        return np.array(x, dtype=float)


class Lin:
    def __init__(self, D):
        self.W = np.zeros((D, NOUT))

    def predict(self, x):
        return x @ self.W

    def learn(self, X, Z, M, scale=1.0):
        """X (n,D), Z (n,9) standardised targets, M (n,9) masks: one (batched) normalised LMS step."""
        E = (Z - X @ self.W) * M
        nrm = 1.0 + (X * X).sum(1, keepdims=True)
        self.W += scale * LR_L * (X / nrm).T @ E


class Net:
    def __init__(self, D, rng):
        self.W1 = rng.normal(0.0, 0.1, (D, HID))
        self.b1 = np.zeros(HID)
        self.W2 = np.zeros((HID, NOUT))

    def predict(self, x):
        return np.tanh(x @ self.W1 + self.b1) @ self.W2

    def learn(self, X, Z, M, scale=1.0):
        H = np.tanh(X @ self.W1 + self.b1)
        E = (Z - H @ self.W2) * M
        gW2 = H.T @ E
        dH = (E @ self.W2.T) * (1.0 - H * H)
        self.W2 += scale * LR_N * gW2
        self.W1 += scale * LR_N * X.T @ dH
        self.b1 += scale * LR_N * dH.sum(0)


class Table:
    """B: running means of raw outputs per (situation, action), per action, overall."""

    def __init__(self):
        self.sa, self.a, self.o = {}, {}, [np.zeros(NOUT), 0]

    @staticmethod
    def _add(cell, y):
        cell[0] += (y - cell[0]) / (cell[1] + 1)
        cell[1] += 1

    def predict(self, ctx, act, world_mean):
        if (ctx, act) in self.sa:
            return self.sa[(ctx, act)][0]
        if act in self.a:
            return self.a[act][0]
        if self.o[1]:
            return self.o[0]
        return world_mean

    def learn(self, ctx, act, y):
        for key, store in (((ctx, act), self.sa), (act, self.a)):
            if key not in store:
                store[key] = [np.zeros(NOUT), 0]
            self._add(store[key], y)
        self._add(self.o, y)


class Person:
    def __init__(self, D, rng, variants):
        self.m = {}
        for v in variants:
            if v == "B":
                self.m[v] = Table()
            elif v in ("L", "LO", "LO5"):
                self.m[v] = Lin(D)
            else:
                self.m[v] = Net(D, rng)
        self.weeks = 0
        self.props_seen = set()
        self.hid_mean = np.zeros(HIDDEN_IN)
        self.hid_n = 0


class PB1Obs:
    def __init__(self, w, born, variants=VARIANTS, verify=False):
        self.w, self.born, self.variants, self.verify = w, born, variants, verify
        self.feat = Feat(w)
        self.rng = np.random.default_rng(w.cfg.seed * 7919 + 13)
        self.people = {}
        self.cap = {}                      # pid -> capture of this week's decision
        self.last = defaultdict(list)      # pid -> last 2 actions (most recent first)
        self.made = defaultdict(set)       # pid -> kinds made so far
        self.visited = defaultdict(set)    # pid -> tiles stood on (followed-born people, from birth)
        self.mean = np.zeros(NOUT)
        self.m2 = np.zeros(NOUT)
        self.n = 0
        self.sse = {v: {k: np.zeros(NOUT) for k in CASES} for v in VARIANTS}
        self.cnt = Counter()
        self.s = Counter()
        self.verify_bad = 0

    def followed(self, p, tick):
        return self.born[0] <= p.birth < self.born[1] and p.age(tick) >= ADULT

    def capture(self, world, p, chosen):
        t = world.tick
        if p.age(t) < ADULT or t < self.born[0] + ADULT:
            return
        action, target = chosen
        x = self.feat(world, p, action, target, self.last[p.id])
        self.cap[p.id] = {"x": x, "act": action, "ctx": p.last_ctx, "loc": tuple(p.loc), "edible": p.edible(),
                          "health": p.health, "energy": p.energy, "mats": p.mat_total(), "items": len(p.items),
                          "aff": sum(r.affection for r in p.rel.values()),
                          "target": target}

    def outcome(self, world, p, cap, gained):
        from acl.util import distance
        c = world.cfg
        newk = 0.0
        return np.array([gained, p.edible() - cap["edible"], p.health - cap["health"], p.energy - cap["energy"],
                         p.mat_total() - cap["mats"], len(p.items) - cap["items"],
                         distance(cap["loc"], tuple(p.loc), c.width, c.height), newk,
                         sum(r.affection for r in p.rel.values()) - cap["aff"]], dtype=float)

    def __call__(self, world, events):
        tick = world.tick - 1
        gained = Counter()
        newkind = set()
        for ev in events:
            k, a = ev["k"], ev.get("a")
            if k == "forage" and a:
                gained[a] += float(ev.get("got", 0.0))
            elif k == "take" and a:
                gained[a] += float(ev.get("food", 0.0))
            elif k == "hunt":
                party = ev.get("party", ())
                if party:
                    for i in party:
                        gained[i] += float(ev.get("meat", 0.0)) / len(party)
            elif k == "make" and a:
                sig = ev.get("thing")
                if sig and sig not in self.made[a]:
                    newkind.add(a)
                self.made[a].add(sig)
        for p in world.living():
            if self.born[0] <= p.birth < self.born[1]:
                self.visited[p.id].add(tuple(p.loc))
        caps, self.cap = self.cap, {}
        outs = {}
        for pid, cap in caps.items():
            p = world.people[pid]
            if not p.alive:
                continue
            y = self.outcome(world, p, cap, gained[pid])
            y[7] = 1.0 if pid in newkind else 0.0
            outs[pid] = y
            self.last[pid] = [cap["act"]] + self.last[pid][:1]
        if not outs:
            return
        std = np.sqrt(self.m2 / self.n) if self.n > 1 else np.ones(NOUT)
        std = np.maximum(std, STD_FLOOR)
        wmean = self.mean.copy()
        scoring = self.n >= BURN
        own = [pid for pid in outs if self.followed(world.people[pid], tick)]
        for pid in own:
            p = world.people[pid]
            cap, y = caps[pid], outs[pid]
            per = self.people.get(pid)
            if per is None:
                per = self.people[pid] = Person(self.feat.D, self.rng, self.variants)
            x = cap["x"]
            act, ctx = cap["act"], cap["ctx"]
            ek = self._edge_hard(x)
            tkey = self._target_key(cap)
            pkey = (act, ek[0], ek[1], tkey)
            unfam_pair = act in COMMON and (ctx, act) not in per.m["B"].sa if "B" in per.m else False
            unfam_prop = pkey not in per.props_seen
            z = np.clip((y - wmean) / std, -ZCLIP, ZCLIP)
            if scoring:
                self.cnt["all"] += 1
                cases = ["all"]
                if unfam_pair:
                    cases.append("u_pair")
                if unfam_prop:
                    cases.append("u_prop")
                if act not in COMMON:
                    cases.append("rare")
                if cap.get("new_place"):
                    cases.append("u_place")
                wb = sum(per.weeks >= b for b in WBANDS)
                cases.append(f"w{wb}")
                for cs in cases[1:]:
                    self.cnt[cs] += 1
                for v, mod in per.m.items():
                    if v == "B":
                        pred_raw = mod.predict(ctx, act, wmean)
                        e = (z - np.clip((pred_raw - wmean) / std, -ZCLIP, ZCLIP)) ** 2
                    else:
                        e = (z - np.clip(mod.predict(x), -ZCLIP, ZCLIP)) ** 2
                    for cs in cases:
                        self.sse[v][cs] += e
            # learn (after scoring)
            for v, mod in per.m.items():
                if v == "B":
                    mod.learn(ctx, act, y)
                else:
                    if self.verify:
                        before = mod.predict(x).copy()
                    mod.learn(x[None, :], z[None, :], np.ones((1, NOUT)))
                    if self.verify and np.allclose(before, mod.predict(x)) and not np.allclose(z, before):
                        self.verify_bad += 1
            per.weeks += 1
            per.props_seen.add(pkey)
            per.hid_mean = (per.hid_mean * per.hid_n + x[:HIDDEN_IN]) / (per.hid_n + 1)
            per.hid_n += 1
            self.s["own_weeks"] += 1
        # world statistics (past-only for the next week)
        for pid in own:
            y = outs[pid]
            self.n += 1
            d = y - self.mean
            self.mean += d / self.n
            self.m2 += d * (y - self.mean)
        # observed weeks
        obs_vars = [v for v in ("LO", "LO5", "NO") if v in self.variants]
        if obs_vars:
            from acl.util import distance
            c = world.cfg
            for pid in own:
                per = self.people[pid]
                O = world.people[pid]
                xs, zs = [], []
                for aid, y in outs.items():
                    if aid == pid:
                        continue
                    if distance(tuple(O.loc), caps[aid]["loc"], c.width, c.height) > c.perception:
                        continue
                    xo = caps[aid]["x"].copy()
                    xo[:HIDDEN_IN] = per.hid_mean
                    xo[-2] = 1.0
                    xs.append(xo)
                    zs.append(np.clip((y - wmean) / std, -ZCLIP, ZCLIP))
                if not xs:
                    continue
                X, Z = np.array(xs), np.array(zs)
                M = np.tile(VISIBLE, (len(xs), 1))
                self.s["observed"] += len(xs)
                for v in obs_vars:
                    per.m[v].learn(X, Z, M, OBS_W[v])
        living = world.living()
        self.s["living_weeks"] += len(living)
        self.s["followed_weeks"] += len(own)
        self.s["followed_people"] = len(self.people)

    @staticmethod
    def _edge_hard(x):
        i0 = 4 + 3 + 1 + 2 + 4 + 1 + 1 + 3 + 8      # start of the held best edge/reach/hard/contain block
        return (min(2, int(x[i0] * 3)), min(2, int(x[i0 + 2] * 3)))

    @staticmethod
    def _target_key(cap):
        t = cap["target"]
        if cap["act"] == "gather" and isinstance(t, (tuple, list)) and len(t) == 2:
            return str(t[1])
        if cap["act"] == "make" and isinstance(t, str):
            return t
        return ""

    def results(self):
        return {"variants": list(self.variants), "cases": list(CASES),
                "sse": {v: {k: [round(float(e), 6) for e in self.sse[v][k]] for k in CASES} for v in self.variants},
                "counts": dict(self.cnt), "sums": dict(self.s), "verify_bad": self.verify_bad}


def install(w, obs):
    from acl import decision
    o_decide = decision.decide

    def decide(world, p):
        d = o_decide(world, p)
        if world is w:
            obs.capture(world, p, d.chosen)
            act, tgt = d.chosen
            dest = None
            if act in ("forage", "hunt", "explore", "flee", "join") and isinstance(tgt, (tuple, list)) and len(tgt) == 2:
                dest = tuple(tgt)
            elif act in ("gather", "take") and isinstance(tgt, (tuple, list)) and tgt:
                dest = tuple(tgt[0]) if isinstance(tgt[0], (tuple, list)) else None
            loc_new = dest is not None and dest not in obs.visited[p.id]
            if p.id in obs.cap:
                obs.cap[p.id]["new_place"] = loc_new
        return d
    decision.decide = decide


def hashrun(seed, years, observe, variants="all"):
    base.setup(CODE)
    w = base.make_world(seed, ARMS["c"])
    obs = None
    if observe:
        vs = VARIANTS if variants == "all" else tuple(variants.split(","))
        obs = PB1Obs(w, [5 * WPY, years * WPY], vs, verify=True)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results()
        extra = ":" + json.dumps({"own": obs.s["own_weeks"], "obs": obs.s["observed"], "verify_bad": obs.verify_bad,
                                  "L_all": [round(e, 6) for e in r["sse"]["L"]["all"]]},
                                 sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def reload_check(seed):
    base.setup(CODE)
    from acl.world import World
    a = base.make_world(seed, ARMS["c"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for x in (a, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(a) == base.world_hash(b)


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
    specs = [(seed, years, obs, v) for seed, years in ((501, 20), (601, 60))
             for obs, v in ((0, "all"), (1, "all"), (1, "L"))]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
        rl = rl.result()
    for seed, years in ((501, 20), (601, 60)):
        ro = hs(got[(seed, years, 0, "all")]) == hs(got[(seed, years, 1, "all")]) == hs(got[(seed, years, 1, "L")])
        a = json.loads(got[(seed, years, 1, "all")].split(":", 2)[2])
        b = json.loads(got[(seed, years, 1, "L")].split(":", 2)[2])
        alone = a["L_all"] == b["L_all"]
        # people born after year 5 are first adult in year 21: in the 20-year world nobody is followed yet, so the
        # prequential check applies to the 60-year world (it must follow someone there)
        applies = years > 21
        prequential = a["verify_bad"] == 0 and (a["own"] > 0 or not applies)
        t = ro and alone and prequential
        ok &= t
        lines.append(f"seed {seed}, {years} years: observer and predictors read-only (following people born after year "
                     f"5): {'yes' if ro else 'NO'}; L-own's errors are the same alone as beside the other variants: "
                     f"{'yes' if alone else 'NO'}; each prediction is made before its update: "
                     f"{('yes' if prequential else 'NO') if applies else 'not applicable (nobody followed yet)'}; {a}")
    t = rl[-1:] == ["True"]
    ok &= t
    lines.append(f"seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_v13 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = base.make_world(seed, ARMS[arm])
    born = list(BORN) if years >= 110 else [max(0, years - 60) * WPY, max(1, years - 20) * WPY]
    obs = PB1Obs(w, born)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_v13", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "born": born, "world_hash": base.world_hash(w),
           **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, followed {obs.s['followed_people']}, own weeks "
          f"{obs.s['own_weeks']}, observed {obs.s['observed']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4] == "1", sys.argv[5]))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
