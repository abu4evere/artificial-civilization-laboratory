"""LD1 — why does the habit look-ahead lock choices, and where does remaking fail? (questions.md, frozen as `LD1-frozen`).
Read-only on live nature v13 (`code_v13`); worlds c (v13) and c0 (v13 with discount 0). ES2's runner supplies the
set-up (`../ES2_realized_lookahead/run_es2.py`). Wrappers only watch, nothing is written to the world:
  _learn       biology._learn: the shadow tables q_r (from r) and q_f (from 0.8 x max next q), the look-ahead term by
               action and next food band; entries written by other code or clamped are marked (the exactness check)
  steer        thought.steer sees every scored option of a decision (after the thought pulls): the softmax shares of
               make, gather, forage, play and person-aimed acts under four score versions (actual, scale, direction,
               none); whether the top option changes without the habit term; whether a tracked kind was offered
  kinds        world-new kinds made in play in years 130-165 (AF1's rule), followed 5 years in their inventor's weeks:
               recipe held, inputs in hand, not already holding one, valued > 0.05, offered, remade; others who learn it
  census       year ends: the share of adults' q entries at the clamp; the gap |q - (q_r + q_f)|

  python experiments/LD1_lookahead_diagnosis/run_ld1.py zero
  python experiments/LD1_lookahead_diagnosis/run_ld1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.CODES["v13"] = HERE.parent / "NV13_nature_v13" / "code_v13"
CODE = "v13"
WPY, YEARS = base.WPY, 170
SEEDS = tuple(range(23401, 23433))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9889, 9888)
ARMS = {"c": {**base.LP}, "c0": {**base.LP, "discount": 0.0}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
ADULT, OLD = 16 * WPY, 50 * WPY
START = [100 * WPY]                        # shadow tables from here
WIN = [130 * WPY, 170 * WPY]               # counted here
REMAKE = 5 * WPY
CLASSES = {"make": "make", "gather": "gather", "forage": "forage", "play": "play", "give": "person", "care": "person",
           "talk": "person", "court": "person", "steal": "person", "attack": "person"}
VERSIONS = ("actual", "scale", "direction", "none")


class LD1Obs:
    def __init__(self, w):
        from acl.person import A, N_ACTIONS
        self.w, self.A, self.N = w, A, N_ACTIONS
        self.s = Counter()
        self.qr, self.qf, self.seen, self.dirty, self.clamped = {}, {}, {}, {}, {}
        self.kinds = {}        # sig -> dict
        self.learners = {}     # sig -> set of others who learned it

    # -- shadow tables
    def table(self, p):
        if p.id not in self.qr:
            self.qr[p.id] = list(p.q)
            self.qf[p.id] = [0.0] * len(p.q)
            self.seen[p.id] = list(p.q)
            self.dirty[p.id] = [False] * len(p.q)
            self.clamped[p.id] = [False] * len(p.q)
        return self.qr[p.id], self.qf[p.id]

    def learn(self, world, p, run):
        """Wraps one habit update: the same r, next situation and future as _learn computes, then the shadow update."""
        from acl.mind import context_index
        c = world.cfg
        tick = world.tick
        if tick < START[0]:
            return run()
        qr, qf = self.table(p)
        near = world.people_near(p.loc, c.reach, exclude=p.id)
        nxt = context_index(world, p, bool(near))
        N = self.N
        future = max(p.q[nxt * N:(nxt + 1) * N])
        r = p.reward + 2.0 * (p.mood - p.mood_before)
        i = p.last_ctx * N + self.A[p.last_action]
        seen, dirty = self.seen[p.id], self.dirty[p.id]
        if p.q != seen:                        # written by other code since we last looked
            for j in range(len(p.q)):
                if p.q[j] != seen[j]:
                    dirty[j] = True
        old = p.q[i]
        raw = old + c.learning_rate * (r + c.discount * future - old)
        out = run()
        if p.q[i] != raw:
            self.clamped[p.id][i] = True
        qr[i] += c.learning_rate * (r - qr[i])
        qf[i] += c.learning_rate * (c.discount * future - qf[i])
        seen[:] = p.q
        if WIN[0] <= tick < WIN[1] and ADULT <= p.age(tick) < OLD:
            a = p.last_action
            band = nxt // 8
            self.s[f"la_{a}_n"] += 1
            self.s[f"la_{a}_sum"] += c.discount * future
            self.s[f"la_band{band}_n"] += 1
            self.s[f"la_band{band}_sum"] += c.discount * future
        return out

    # -- decisions
    def decision(self, world, p, options):
        tick = world.tick
        if not (WIN[0] <= tick < WIN[1] and ADULT <= p.age(tick) < OLD) or not options:
            return
        c = world.cfg
        lw, T, N = c.learned_weight, c.choice_temperature, self.N
        ctx = p.last_ctx
        base_i = ctx * N
        qr, qf = self.table(p)
        mean_f = sum(qf[base_i:base_i + N]) / N
        s = [o[0] for o in options]
        h = [lw * p.q[base_i + self.A[o[1]]] for o in options]
        ver = {"actual": s,
               "scale": [x - y + 0.2 * y for x, y in zip(s, h)],
               "direction": [x - y + lw * (qr[base_i + self.A[o[1]]] + mean_f) for x, y, o in zip(s, h, options)],
               "none": [x - y + lw * qr[base_i + self.A[o[1]]] for x, y, o in zip(s, h, options)]}
        self.s["decisions"] += 1
        for v, sc in ver.items():
            top = max(sc)
            wts = [math.exp((x - top) / T) for x in sc]
            tot = sum(wts)
            for wgt, o in zip(wts, options):
                k = CLASSES.get(o[1])
                if k:
                    self.s[f"sh_{v}_{k}"] += wgt / tot
        no_h = [x - y for x, y in zip(s, h)]
        self.s["top_changes"] += int(max(range(len(s)), key=lambda k: s[k]) != max(range(len(s)), key=lambda k: no_h[k]))
        self.s["abs_h"] += sum(abs(y) for y in h) / len(h)
        self.s["abs_rest"] += sum(abs(y) for y in no_h) / len(no_h)
        for o in options:
            if o[1] == "make":
                kd = self.kinds.get(o[2])
                if kd is not None and kd["inv"] == p.id and kd["t"] <= tick < kd["t"] + REMAKE:
                    kd["offered"] = 1

    # -- kinds
    def invented(self, world, p, sig, recipe):
        t = world.tick
        if WIN[0] <= t and t + REMAKE <= WIN[1]:
            self.kinds[sig] = {"t": t, "inv": p.id, "recipe": recipe, "first": None, "held": 0, "inputs": 0,
                               "free": 0, "offered": 0, "remade": 0, "lost_at": None, "died": 0}

    def learned_by(self, world, p, sig):
        kd = self.kinds.get(sig)
        if kd is not None and p.id != kd["inv"] and kd["t"] <= world.tick < kd["t"] + REMAKE:
            self.learners.setdefault(sig, set()).add(p.id)

    def made(self, world, p, sig):
        kd = self.kinds.get(sig)
        if kd is not None and p.id == kd["inv"] and kd["t"] < world.tick <= kd["t"] + REMAKE:
            kd["remade"] = 1

    def __call__(self, world, events):
        from acl.mind import _holding, can_make
        tick = world.tick - 1
        for sig, kd in self.kinds.items():
            if not (kd["t"] <= tick < kd["t"] + REMAKE):
                continue
            p = world.people.get(kd["inv"])
            alive = p is not None and p.alive
            held = alive and sig in p.recipes
            if kd["first"] is None:
                kd["first"] = int(held)
            if not held:
                if kd["lost_at"] is None:
                    kd["lost_at"] = tick - kd["t"]
                    kd["died"] = int(not alive)
                continue
            kd["held"] = 1
            if can_make(p, kd["recipe"]):
                kd["inputs"] = 1
                if not _holding(p, sig) and p.itemval.get(sig, 0.0) > 0.05:
                    kd["free"] = 1
        if tick % WPY == WPY - 1 and WIN[0] <= tick < WIN[1]:
            for p in world.living():
                if not (ADULT <= p.age(world.tick) < OLD):
                    continue
                self.s["census_entries"] += len(p.q)
                self.s["census_clamp"] += sum(1 for x in p.q if abs(x) >= 1.49)
                self.s["census_absq"] += sum(abs(x) for x in p.q)
                if p.id in self.qr:
                    qr, qf = self.qr[p.id], self.qf[p.id]
                    self.s["gap_n"] += len(p.q)
                    self.s["gap_sum"] += sum(abs(a - b - c) for a, b, c in zip(p.q, qr, qf))
        if WIN[0] <= tick < WIN[1]:
            living = world.living()
            self.s["living_weeks"] += len(living)
            self.s["adult_weeks"] += sum(1 for p in living if ADULT <= p.age(world.tick) < OLD)

    def exactness(self, world):
        """Over living people with shadow tables: entries never written by other code and never clamped, whose q
        still equals what we saw, satisfy q = q_r + q_f (to 1e-9)."""
        n = bad = 0
        for p in world.living():
            if p.id not in self.qr:
                continue
            qr, qf, seen = self.qr[p.id], self.qf[p.id], self.seen[p.id]
            d, cl = self.dirty[p.id], self.clamped[p.id]
            for j, x in enumerate(p.q):
                if d[j] or cl[j] or x != seen[j]:
                    continue
                n += 1
                bad += abs(x - qr[j] - qf[j]) > 1e-9
        return n, bad

    def results(self):
        stages = Counter()
        lost = []
        for kd in self.kinds.values():
            if kd["remade"]:
                st = 5
            elif kd["offered"]:
                st = 4
            elif kd["free"]:
                st = 3
            elif kd["inputs"]:
                st = 2
            elif kd["held"]:
                st = 1
            else:
                st = 0
            stages[st] += 1
            if kd["lost_at"] is not None:
                lost.append(kd["lost_at"])
        return {"sums": dict(self.s), "n_kinds": len(self.kinds), "stages": {str(k): v for k, v in sorted(stages.items())},
                "first_week_lost": sum(1 for kd in self.kinds.values() if kd["first"] == 0),
                "died_lost": sum(kd["died"] for kd in self.kinds.values()),
                "lost_weeks": sorted(lost), "spread": sum(1 for s in self.kinds if self.learners.get(s))}


def install(w, obs):
    from acl import actions, biology, knowhow, thought
    o_learn, o_steer, o_rem, o_make = biology._learn, thought.steer, knowhow.remember_recipe, actions.HANDLERS["make"]

    def _learn(world, p):
        if world is not w:
            return o_learn(world, p)
        return obs.learn(world, p, lambda: o_learn(world, p))

    def steer(p, options):
        out = o_steer(p, options)
        obs.decision(w, p, out)
        return out

    def remember_recipe(world, p, sig, recipe, how, source=None, props=None, meant=None):
        new = sig not in world.knowledge
        out = o_rem(world, p, sig, recipe, how, source, props, meant)
        if world is w:
            if new and how == "made" and props is not None:
                obs.invented(world, p, sig, recipe)
            else:
                obs.learned_by(world, p, sig)
        return out

    def make(world, p, sig, eff):
        if world is not w:
            return o_make(world, p, sig, eff)
        n0 = len(world.events)
        out = o_make(world, p, sig, eff)
        if any(ev["k"] == "make" and ev.get("a") == p.id for ev in world.events[n0:]):
            obs.made(world, p, sig)
        return out
    biology._learn = _learn
    thought.steer = steer
    knowhow.remember_recipe = remember_recipe
    actions.HANDLERS["make"] = make


def hashrun(arm, seed, years, observe):
    START[0], WIN[0], WIN[1] = 5 * WPY, 0, years * WPY     # zero checks: everything on from year 5
    base.setup(CODE)
    w = base.make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = LD1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        n, bad = obs.exactness(w)
        extra = f":{obs.s['decisions']},{len(obs.kinds)},{n},{bad}"
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    from concurrent.futures import ThreadPoolExecutor
    specs = [(arm, seed, years, obs) for seed, years in ((501, 20), (601, 60)) for arm in ("c", "c0") for obs in (0, 1)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        g = {(a, o): got[(a, sd, yr, o)] for a, sd, yr, o in specs if sd == seed}
        hs = lambda x: x.split(":")[:2]  # noqa: E731
        ro = hs(g[("c", 0)]) == hs(g[("c", 1)]) and hs(g[("c0", 0)]) == hs(g[("c0", 1)])
        acts = hs(g[("c0", 0)]) != hs(g[("c", 0)])
        info = {a: g[(a, 1)].split(":")[2].split(",") for a in ("c", "c0")}
        exact = all(int(info[a][2]) > 0 and info[a][3] == "0" for a in ("c", "c0"))
        seen = all(int(info[a][0]) > 0 for a in ("c", "c0"))
        t = ro and acts and exact and seen
        ok &= t
        lines.append(f"seed {seed}, {years} years (shadow tables from year 5): the observers leave the world unchanged "
                     f"(c and c0): {'yes' if ro else 'NO'}; c0 acts: {'yes' if acts else 'NO'}; decisions seen "
                     f"{info['c'][0]}/{info['c0'][0]}, kinds tracked {info['c'][1]}/{info['c0'][1]}; q = q_r + q_f on "
                     f"clean entries (c: {info['c'][3]} wrong of {info['c'][2]}; c0: {info['c0'][3]} wrong of "
                     f"{info['c0'][2]}): {'yes' if exact else 'NO'}")
    lines.append(f"code_v13 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    if years < YEARS:                          # a smoke run: shadow from 40% of the run, counted over its last 30%
        START[0] = int(years * 0.4) * WPY
        WIN[0], WIN[1] = int(years * 0.7) * WPY, years * WPY
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = base.make_world(seed, ARMS[arm])
    obs = LD1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    n, bad = obs.exactness(w)
    res = {"arm": arm, "seed": seed, "nature": "code_v13", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), "exact": [n, bad],
           **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, decisions {obs.s['decisions']}, kinds {len(obs.kinds)}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] == "1"))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
