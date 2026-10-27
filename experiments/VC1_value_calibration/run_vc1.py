"""VC1 — are habits calibrated? (questions.md, frozen as `VC1-frozen`). Read-only: live nature v7 (`code_v7`) unchanged,
with one read-only wrapper on `biology._learn` that replays each weekly update exactly (as HL1) and then follows the
person's later rewards to measure the realised discounted return.

  python experiments/VC1_value_calibration/run_vc1.py zero
  python experiments/VC1_value_calibration/run_vc1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODE = EXP / "NV7_nature_v7" / "code_v7"
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(19001, 19033))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9943, 9942)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
ARMS = {"lp": {"founders": 80, "width": 80, "height": 80}}
JOBS = [f"lp:{s}" for s in SEEDS]
ERAS = (50, 100, 200)
CUT = 0.001                               # follow later rewards until the weight 0.8^k falls below this (31 weeks)
SUMS = ("n", "q", "G", "qq", "GG", "qG", "r", "y", "cens", "gap", "gap_n", "link_n")


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


class VC1Obs:
    def __init__(self, w):
        from acl.person import ACTIONS, N_ACTIONS
        self.w = w
        self.acts = ACTIONS
        self.N = N_ACTIONS
        self.cells = defaultdict(lambda: [0.0] * len(SUMS))    # "era|action" and "era|ctx|action" -> sums
        self.pending = defaultdict(list)       # person -> [[keys, q, acc, disc]]
        self.last = {}                         # person -> (entry keys, nxt, max of row, row snapshot)
        self.mismatch = Counter()
        self.n_upd = 0

    def add(self, keys, field, v):
        j = SUMS.index(field)
        for k in keys:
            self.cells[k][j] += v

    def close(self, entry, censored):
        keys, q, acc, _ = entry
        for k in keys:
            c = self.cells[k]
            c[0] += 1
            c[1] += q
            c[2] += acc
            c[3] += q * q
            c[4] += acc * acc
            c[5] += q * acc
            c[8] += censored

    def on_learn(self, world, p, i, before, after, r, fut, nxt):
        alpha, gamma = world.cfg.learning_rate, world.cfg.discount
        unclipped = before + alpha * (r + gamma * fut - before)
        if abs(max(-1.5, min(1.5, unclipped)) - after) > 1e-12:
            self.mismatch["td_replay"] += 1
        # this week's reward feeds every open realised return of this person
        keep = []
        for e in self.pending.get(p.id, ()):
            e[2] += e[3] * r
            e[3] *= gamma
            if e[3] < CUT:
                self.close(e, 0)
            else:
                keep.append(e)
        # the max gap of last week's update: its s' against the action actually taken now
        lk = self.last.pop(p.id, None)
        if lk is not None:
            keys, nx, mx, row = lk
            self.add(keys, "link_n", 1)
            if p.last_ctx == nx:
                self.add(keys, "gap", gamma * (mx - row[i % self.N]))
                self.add(keys, "gap_n", 1)
        if p.age(world.tick) >= 16 * WPY:
            self.n_upd += 1
            ctx, a = divmod(i, self.N)
            era = era_of(world.tick)
            act = self.acts[a]
            keys = (f"{era}|{act}", f"{era}|{ctx}|{act}")
            self.add(keys, "r", r)
            self.add(keys, "y", r + gamma * fut)
            keep.append([keys, before, r, gamma])
            row = p.q[nxt * self.N:(nxt + 1) * self.N]
            self.last[p.id] = (keys, nxt, max(row), list(row))
        if keep:
            self.pending[p.id] = keep
        else:
            self.pending.pop(p.id, None)

    def __call__(self, world, events):
        for ev in events:
            if ev["k"] == "death":
                a = ev.get("a")
                for e in self.pending.pop(a, ()):
                    self.close(e, 1)                     # rewards end at death
                self.last.pop(a, None)

    def results(self):
        return {"sums": SUMS, "cells": {k: v for k, v in self.cells.items()}, "mismatch": dict(self.mismatch),
                "open_at_end": sum(len(v) for v in self.pending.values())}


def install(w, obs):
    from acl import biology
    from acl.mind import context_index
    from acl.person import A
    o_learn = biology._learn

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
        obs.on_learn(world, p, i, before, p.q[i], r, fut, nxt)
        return out

    biology._learn = learn


def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = VC1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        extra = ":" + json.dumps({**obs.mismatch, "_updates": obs.n_upd}, sort_keys=True, separators=(",", ":"))
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
    from concurrent.futures import ThreadPoolExecutor
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.split()[-1]
    specs = [("hashrun", "lp", seed, years, obs) for seed, years in ((501, 20), (601, 60)) for obs in (1, 0)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call(*sp), specs)))
    lines, ok = [], True
    for seed, years in ((501, 20), (601, 60)):
        a = got[("hashrun", "lp", seed, years, 1)]
        b = got[("hashrun", "lp", seed, years, 0)]
        same = a.split(":")[:2] == b.split(":")[:2]
        info = json.loads(a.split(":", 2)[2])
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = same and not any(mism.values()) and info.get("_updates", 0) > 0
        ok &= t
        lines.append(f"arm lp, seed {seed}, {years} years: identical with and without the observer (state and random "
                     f"numbers): {'yes' if same else 'NO'}; TD-replay mismatches: {mism or 'none'}; adult updates "
                     f"{info.get('_updates')}")
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
    obs = VC1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v7", "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "world_hash": world_hash(w), "actions": list(obs.acts), **obs.results()}
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
