"""HC1 — habit copying in talk (questions.md, frozen as `HC1-frozen`). Nature-change study: `code_hc1` = `code_v7` + one
setting, `talk_copy` ("whole" = v7 exactly; v7_to_hc1.diff). Arms w (v7), s ("situation"), x (sham: one extra draw in
week one). A read-only observer (VC1's) wraps `biology._learn`, replays each update exactly and follows the realised
discounted return; a yearly census counts the living.

  python experiments/HC1_habit_copying/run_hc1.py zero
  python experiments/HC1_habit_copying/run_hc1.py one <arm> <seed> <years> <out>
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
CODES = {"hc1": HERE / "code_hc1", "v7": EXP / "NV7_nature_v7" / "code_v7"}
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(19201, 19233))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9939, 9938)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
LP = {"founders": 80, "width": 80, "height": 80}
ARMS = {"w": {**LP}, "s": {**LP, "talk_copy": "situation"}, "x": {**LP, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
ERAS = (50, 100, 200)
CUT = 0.001
SUMS = ("n", "q", "G", "cens")


def era_of(tick):
    y = tick / WPY
    for i, e in enumerate(ERAS):
        if y < e:
            return i
    return len(ERAS) - 1


def setup(code="hc1"):
    sys.path.insert(0, str(CODES[code]))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


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


def fingerprint(code="hc1"):
    from run_e7 import code_hash
    return code_hash(CODES[code] / "acl")


class HC1Obs:
    def __init__(self, w):
        from acl.person import ACTIONS, N_ACTIONS
        self.w = w
        self.acts = ACTIONS
        self.N = N_ACTIONS
        self.cells = defaultdict(lambda: [0.0] * len(SUMS))    # "era|action" -> sums
        self.pending = defaultdict(list)       # person -> [[key, q, acc, disc]]
        self.mismatch = Counter()
        self.census = []                       # [year, living, adults]
        self.n_upd = 0

    def close(self, e, censored):
        key, q, acc, _ = e
        c = self.cells[key]
        c[0] += 1
        c[1] += q
        c[2] += acc
        c[3] += censored

    def on_learn(self, world, p, i, before, after, r, fut):
        alpha, gamma = world.cfg.learning_rate, world.cfg.discount
        unclipped = before + alpha * (r + gamma * fut - before)
        if abs(max(-1.5, min(1.5, unclipped)) - after) > 1e-12:
            self.mismatch["td_replay"] += 1
        keep = []
        for e in self.pending.get(p.id, ()):
            e[2] += e[3] * r
            e[3] *= gamma
            if e[3] < CUT:
                self.close(e, 0)
            else:
                keep.append(e)
        if p.age(world.tick) >= 16 * WPY:
            self.n_upd += 1
            keep.append([f"{era_of(world.tick)}|{self.acts[i % self.N]}", before, r, gamma])
        if keep:
            self.pending[p.id] = keep
        else:
            self.pending.pop(p.id, None)

    def __call__(self, world, events):
        for ev in events:
            if ev["k"] == "death":
                for e in self.pending.pop(ev.get("a"), ()):
                    self.close(e, 1)
        tick = world.tick - 1
        if tick % WPY == WPY - 1:
            living = world.living()
            self.census.append([tick // WPY, len(living),
                                sum(1 for p in living if p.age(world.tick) >= 16 * WPY)])

    def results(self):
        return {"sums": SUMS, "cells": dict(self.cells), "mismatch": dict(self.mismatch),
                "census_fields": ["year", "living", "adults"], "census": self.census,
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
        obs.on_learn(world, p, i, before, p.q[i], r, fut)
        return out

    biology._learn = learn


def hashrun(code, arm, seed, years, observe):
    setup(code)
    kw = dict(ARMS[arm])
    if code == "v7":
        kw.pop("talk_copy", None)
    w = make_world(seed, kw)
    obs = None
    if observe:
        obs = HC1Obs(w)
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
    a = make_world(seed, ARMS["s"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for x in (a, b):
        for _ in range(5 * WPY):
            x.step()
    return world_hash(a) == world_hash(b) and b.cfg.talk_copy == "situation"


def zero():
    from concurrent.futures import ThreadPoolExecutor
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.split()[-1]

    def hs(x):
        return x.split(":")[:2]
    specs = [(code, arm, seed, years, obs) for seed, years in ((501, 20), (601, 60))
             for code, arm, obs in (("v7", "w", 0), ("hc1", "w", 0), ("hc1", "s", 1), ("hc1", "s", 0),
                                    ("hc1", "x", 0), ("hc1", "w", 1))]
    with ThreadPoolExecutor(6) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    lines, ok = [], True
    for seed, years in ((501, 20), (601, 60)):
        v7 = got[("v7", "w", seed, years, 0)]
        w0 = got[("hc1", "w", seed, years, 0)]
        s1 = got[("hc1", "s", seed, years, 1)]
        s0 = got[("hc1", "s", seed, years, 0)]
        x0 = got[("hc1", "x", seed, years, 0)]
        w1 = got[("hc1", "w", seed, years, 1)]
        same_v7 = hs(v7) == hs(w0)
        ro = hs(s1) == hs(s0) and hs(w1) == hs(w0)
        acts = hs(s0) != hs(w0)
        sham = hs(x0) != hs(w0)
        info = json.loads(s1.split(":", 2)[2])
        info_w = json.loads(w1.split(":", 2)[2])
        mism = {k: v for d in (info, info_w) for k, v in d.items() if not k.startswith("_")}
        t = same_v7 and ro and acts and sham and not any(mism.values()) and info.get("_updates", 0) > 0
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_hc1 with 'whole' equals code_v7: {'yes' if same_v7 else 'NO'}; "
                     f"observer read-only (arms s and w): {'yes' if ro else 'NO'}; the setting acts: "
                     f"{'yes' if acts else 'NO'}; the sham acts: {'yes' if sham else 'NO'}; TD-replay mismatches: "
                     f"{mism or 'none'}; adult updates (s) {info.get('_updates')}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm s, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_hc1 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = HC1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "hc1", "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": world_hash(w), "actions": list(obs.acts),
           **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, mismatches {res['mismatch']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "fp":
        setup()
        print(fingerprint())
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
