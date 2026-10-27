"""CL1 — which route carries the miscalibration? (questions.md, frozen as `CL1-frozen`). Read-only: live nature v7
(`code_v7`) unchanged. HL1's route ledger (wrappers on `biology._learn`, `actions._imitate`, `biology._upbringing`,
`biology._born`, `actions._give`; each calls the original unchanged) joined with VC1's realised discounted return.

At every adult TD update: q (before) = C_td + C_talk + C_carer + C_birth + C_paid, and G follows (VC1), so
q - G = (C_td - G) + C_talk + C_carer + C_birth + C_paid exactly.

  python experiments/CL1_calibration_ledger/run_cl1.py zero
  python experiments/CL1_calibration_ledger/run_cl1.py one <arm> <seed> <years> <out>
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
SEEDS = tuple(range(19101, 19133))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9941, 9940)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
ARMS = {"lp": {"founders": 80, "width": 80, "height": 80}}
JOBS = [f"lp:{s}" for s in SEEDS]
ERAS = (50, 100, 200)
ROUTES = ("td", "talk", "carer", "birth", "paid")
CUT = 0.001
SUMS = ("n", "q", "G", "cens", "gap", "gap_n", "link_n") + tuple(f"C_{r}" for r in ROUTES)


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


class CL1Obs:
    def __init__(self, w):
        from acl.person import ACTIONS, N_ACTIONS
        self.w = w
        self.N = N_ACTIONS
        self.acts = ACTIONS
        self.comp = {}                                 # pid -> {route: [floats]}  (HL1's ledger)
        self.cells = defaultdict(lambda: [0.0] * len(SUMS))
        self.pending = defaultdict(list)               # pid -> [[key, comps(list), q, acc, disc]]
        self.last = {}                                 # pid -> (key, nxt, max row, row)
        self.mismatch = Counter()
        self.n_upd = 0
        for p in w.living():
            self._init(p, "birth")

    # --- HL1's ledger -----------------------------------------------------------------------------------------
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

    def _blend(self, p, before, after, other, route):
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

    def on_imitate(self, world, learner, model, before, after):
        self._blend(learner, before, after, model.q, "talk")

    def on_upbringing(self, world, child, carer, before, after):
        self._blend(child, before, after, carer.q, "carer")

    def on_born(self, child):
        self._init(child, "birth")

    def on_paid(self, world, p, i, before, after):
        self._comps(p)["paid"][i] += after - before

    # --- the update: split q, then follow the realised return (VC1) --------------------------------------------
    def close(self, e, censored):
        key, comps, q, acc, _ = e
        c = self.cells[key]
        c[0] += 1
        c[1] += q
        c[2] += acc
        c[3] += censored
        for j, v in enumerate(comps):
            c[7 + j] += v

    def on_learn(self, world, p, i, before, after, r, fut, nxt):
        c = self._comps(p)
        comps = [c[rt][i] for rt in ROUTES]
        if abs(sum(comps) - before) > 1e-9:
            self.mismatch["ledger_at_update"] += 1
        alpha, gamma = world.cfg.learning_rate, world.cfg.discount
        for rt in ROUTES:
            c[rt][i] *= (1.0 - alpha)
        c["td"][i] += after - (1.0 - alpha) * before
        unclipped = before + alpha * (r + gamma * fut - before)
        if abs(max(-1.5, min(1.5, unclipped)) - after) > 1e-12:
            self.mismatch["td_replay"] += 1
        keep = []
        for e in self.pending.get(p.id, ()):
            e[3] += e[4] * r
            e[4] *= gamma
            if e[4] < CUT:
                self.close(e, 0)
            else:
                keep.append(e)
        lk = self.last.pop(p.id, None)
        if lk is not None:
            key, nx, mx, row = lk
            cell = self.cells[key]
            cell[6] += 1
            if p.last_ctx == nx:
                cell[4] += gamma * (mx - row[i % self.N])
                cell[5] += 1
        if p.age(world.tick) >= 16 * WPY:
            self.n_upd += 1
            key = f"{era_of(world.tick)}|{self.acts[i % self.N]}"
            keep.append([key, comps, before, r, gamma])
            row = p.q[nxt * self.N:(nxt + 1) * self.N]
            self.last[p.id] = (key, nxt, max(row), list(row))
        if keep:
            self.pending[p.id] = keep
        else:
            self.pending.pop(p.id, None)

    def __call__(self, world, events):
        for ev in events:
            if ev["k"] == "death":
                a = ev.get("a")
                for e in self.pending.pop(a, ()):
                    self.close(e, 1)
                self.last.pop(a, None)
        living = world.living()
        alive = {p.id for p in living}
        for pid in [x for x in self.comp if x not in alive]:
            del self.comp[pid]
        if world.tick % 520 == 0:                      # HL1's decade closure: the ledger adds up for everyone
            for p in living:
                c = self.comp.get(p.id)
                if c is None or not p.q:
                    continue
                for i in range(len(p.q)):
                    if abs(p.q[i] - sum(c[r][i] for r in ROUTES)) > 1e-9:
                        self.mismatch["ledger"] += 1
                        break

    def results(self):
        return {"sums": SUMS, "cells": dict(self.cells), "mismatch": dict(self.mismatch),
                "open_at_end": sum(len(v) for v in self.pending.values())}


def install(w, obs):
    from acl import actions, biology
    from acl.mind import context_index
    from acl.person import A
    o_learn, o_imit, o_up, o_born, o_give = (biology._learn, actions._imitate, biology._upbringing,
                                             biology._born, actions._give)

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

    biology._learn = learn
    actions._imitate = imitate
    biology._upbringing = upbringing
    biology._born = born
    actions._give = give
    if hasattr(actions, "HANDLERS"):
        actions.HANDLERS = {k: (give if v is o_give else v) for k, v in actions.HANDLERS.items()}


def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = CL1Obs(w)
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
                     f"numbers): {'yes' if same else 'NO'}; TD-replay and ledger mismatches: {mism or 'none'}; adult "
                     f"updates {info.get('_updates')}")
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
    obs = CL1Obs(w)
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
