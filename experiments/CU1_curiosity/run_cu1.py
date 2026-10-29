"""CU1 — a curiosity law (questions.md, frozen as `CU1-frozen`). Nature-change study: `code_cu1` = `code_v8` + one
setting, `curiosity_pull` (0 = v8 exactly; v8_to_cu1.diff). Arms v (v8), c (curiosity pull), x (sham).
A read-only observer wraps:
  thought.steer     the situation-action pairs each adult is offered (years 100-200);
  biology._learn    each own learning update: the pairs actually practised, and a check of `tried`;
and takes a yearly census (living, adults, making events, made things held, world-born adults' crafting skill).

  python experiments/CU1_curiosity/run_cu1.py zero
  python experiments/CU1_curiosity/run_cu1.py one <arm> <seed> <years> <out>
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
CODES = {"cu1": HERE / "code_cu1", "v8": EXP / "NV8_nature_v8" / "code_v8"}
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(20201, 20233))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9991, 9990)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
LP = {"founders": 80, "width": 80, "height": 80}
ARMS = {"v": {**LP}, "c": {**LP, "curiosity_pull": 1}, "x": {**LP, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
WINDOW = (100 * WPY, 200 * WPY)
FIELDS = ["year", "living", "adults", "makes", "items_adults", "wb_adults_20_40", "wb_craft_sum_20_40"]


def setup(code="cu1"):
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


def fingerprint(code="cu1"):
    from run_e7 import code_hash
    return code_hash(CODES[code] / "acl")


class CU1Obs:
    def __init__(self, w):
        from acl.person import ACTIONS, N_ACTIONS
        self.w = w
        self.acts, self.N = ACTIONS, N_ACTIONS
        self.make = ACTIONS.index("make")
        self.mismatch = Counter()
        self.offered = defaultdict(set)      # person -> pair indices offered (adults, window)
        self.updated = defaultdict(set)      # person -> pair indices practised (adults, window)
        self.own = defaultdict(Counter)      # person -> pair index -> own updates (whole run; the `tried` check)
        self.makes = 0
        self.census = []

    def in_window(self, world, p):
        return WINDOW[0] <= world.tick < WINDOW[1] and p.age(world.tick) >= 16 * WPY

    def offer(self, world, p, options):
        if self.in_window(world, p):
            base = p.last_ctx * self.N
            s = self.offered[p.id]
            for _, action, _ in options:
                s.add(base + self.acts.index(action))

    def learned(self, world, p, i):
        self.own[p.id][i] += 1
        if self.in_window(world, p):
            self.updated[p.id].add(i)

    def __call__(self, world, events):
        self.makes += sum(1 for ev in events if ev["k"] == "make")
        tick = world.tick - 1
        if tick % WPY == WPY - 1:
            living = world.living()
            adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
            wb = [p for p in living if p.generation > 0 and 20 * WPY <= p.age(world.tick) < 41 * WPY]
            self.census.append([tick // WPY, len(living), len(adults), self.makes, sum(len(p.items) for p in adults),
                                len(wb), sum(p.skills["crafting"] for p in wb)])
            self.makes = 0

    def results(self):
        if self.w.cfg.__dict__.get("curiosity_pull"):
            for pid, cnt in self.own.items():
                p = self.w.people.get(pid)
                tried = p.tried if p is not None else None
                if tried is None or any(tried[i] != n for i, n in cnt.items()) or sum(tried) != sum(cnt.values()):
                    self.mismatch["tried_vs_updates"] += 1
        hit = off = mk_hit = mk_off = 0
        for pid, s in self.offered.items():
            u = self.updated.get(pid, set())
            off += len(s)
            hit += len(s & u)
            ms = {i for i in s if i % self.N == self.make}
            mk_off += len(ms)
            mk_hit += len(ms & u)
        return {"spread": {"offered": off, "practised": hit, "make_offered": mk_off, "make_practised": mk_hit,
                           "people": len(self.offered)},
                "mismatch": dict(self.mismatch), "census_fields": FIELDS, "census": self.census}


def install(w, obs):
    from acl import biology, thought
    from acl.person import A
    o_steer, o_learn = thought.steer, biology._learn

    def steer(p, options):
        out = o_steer(p, options)
        if w.people.get(p.id) is p:
            obs.offer(w, p, out)
        return out

    def learn(world, p):
        if world is not w or p.last_action is None:
            return o_learn(world, p)
        i = p.last_ctx * obs.N + A[p.last_action]
        out = o_learn(world, p)
        obs.learned(world, p, i)
        return out

    thought.steer = steer
    biology._learn = learn


def hashrun(code, arm, seed, years, observe):
    setup(code)
    kw = dict(ARMS[arm])
    if code == "v8":
        kw.pop("curiosity_pull", None)
    w = make_world(seed, kw)
    obs = None
    if observe:
        obs = CU1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        res = obs.results()
        extra = ":" + json.dumps({**res["mismatch"], "_updates": sum(sum(c.values()) for c in obs.own.values()),
                                  "_makes": sum(r[3] for r in res["census"])}, sort_keys=True, separators=(",", ":"))
    return world_hash(w) + ":" + rng_state(w) + extra


def reload_check(seed):
    setup()
    from acl.world import World
    a = make_world(seed, ARMS["c"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for x in (a, b):
        for _ in range(5 * WPY):
            x.step()
    held = any(p.tried is not None for p in b.people.values())
    return world_hash(a) == world_hash(b) and b.cfg.curiosity_pull == 1 and held


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.split()[-1]

    def hs(x):
        return x.split(":")[:2]
    from concurrent.futures import ThreadPoolExecutor
    specs = [(code, arm, seed, years, obs) for seed, years in ((501, 20), (601, 60))
             for code, arm, obs in (("v8", "v", 0), ("cu1", "v", 0), ("cu1", "c", 1), ("cu1", "c", 0),
                                    ("cu1", "x", 0), ("cu1", "v", 1))]
    with ThreadPoolExecutor(6) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    lines, ok = [], True
    for seed, years in ((501, 20), (601, 60)):
        g = {(c, a, o): v for (c, a, s, y, o), v in got.items() if s == seed and y == years}
        same_v8 = hs(g[("v8", "v", 0)]) == hs(g[("cu1", "v", 0)])
        ro = hs(g[("cu1", "c", 1)]) == hs(g[("cu1", "c", 0)]) and hs(g[("cu1", "v", 1)]) == hs(g[("cu1", "v", 0)])
        acts = hs(g[("cu1", "c", 0)]) != hs(g[("cu1", "v", 0)])
        sham = hs(g[("cu1", "x", 0)]) != hs(g[("cu1", "v", 0)])
        info = json.loads(g[("cu1", "c", 1)].split(":", 2)[2])
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = same_v8 and ro and acts and sham and not any(mism.values()) and info.get("_updates", 0) > 0
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_cu1 with 0 equals code_v8: {'yes' if same_v8 else 'NO'}; "
                     f"observer read-only (arms c and v): {'yes' if ro else 'NO'}; the setting acts: "
                     f"{'yes' if acts else 'NO'}; the sham acts: {'yes' if sham else 'NO'}; tried-vs-updates "
                     f"mismatches (c): {mism or 'none'}; own updates (c) {info.get('_updates')}, make events (c) "
                     f"{info.get('_makes')}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm c, seed 501 (tried saved): saved at year 10 and reloaded, continues exactly to year 15: "
                 f"{'yes' if t else 'NO'}")
    lines.append(f"code_cu1 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = CU1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v8 + curiosity_pull (CU1)", "code_hash": f0,
           "code_hash_after": fingerprint(), "final_tick": w.tick, "extinct": not w.living(),
           "world_hash": world_hash(w), **obs.results()}
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
