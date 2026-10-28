"""PG0 — the "why" audit (questions.md, frozen as `PG0-frozen`). Read-only: live nature v7 (`code_v7`) unchanged, with
read-only wrappers on `actions._play` and `actions._judge_use` that read state before calling the originals, and weekly
events. Predictions use only a person's own past uses, kept by the observer, with its own random generator (never the
world's).

  python experiments/PG0_why_audit/run_pg0.py zero
  python experiments/PG0_why_audit/run_pg0.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import subprocess
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODE = EXP / "NV7_nature_v7" / "code_v7"
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(19501, 19533))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9933, 9932)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
ARMS = {"lp": {"founders": 80, "width": 80, "height": 80}}
JOBS = [f"lp:{s}" for s in SEEDS]
USES = ("forage", "hunt", "wood", "stone", "fiber", "fight", "carry", "cold")
ERAS = (50, 100, 200)
K = 5                                     # nearest past uses
HIST = 200                                # past uses kept per person


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


def knn(hist, x, use, k=K):
    same = [(sum((a - b) ** 2 for a, b in zip(v, x)), f) for v, u, f in hist if u == use]
    if len(same) < k:
        return None
    same.sort(key=lambda t: t[0])
    return sum(f for _, f in same[:k]) / k


class PG0Obs:
    def __init__(self, w):
        from acl.matter import PROPS
        self.w = w
        self.props = PROPS
        self.c = defaultdict(float)
        self.mismatch = Counter()
        self.hist = defaultdict(lambda: deque(maxlen=HIST))    # person -> (props, use, felt, sig) of past uses
        self.seen = set()                                       # (person, sig) already used
        self.learn = {}                                         # (person, sig) -> uses so far, until learned
        self.pending = {}                                       # (maker, sig) -> week: new useful kinds not yet used
        self.remade = {}                                        # sig -> [first week, puzzle-led, remade?]
        self.shuf = random.Random(20261027)                     # the observer's own generator
        self.census = []

    def useful(self, sig):
        props = (self.w.knowledge.get(sig) or {}).get("props")
        return props is not None and maxf(props) > 1.0

    def vec(self, item):
        return tuple(item.get(k, 0) / 100.0 for k in self.props)

    # --- play ---------------------------------------------------------------------------------------------------
    def play(self, orig, world, p, target, eff):
        th = p.thoughts[0] if p.thoughts else None
        led = bool(th and th[0] == "puzzle" and th[1][:2] in ("m:", "f:") and p.recipes.get(th[1][2:]) is not None)
        known_world = set(world.knowledge)
        known_me = set(p.recipes)
        n_ev = len(world.events)
        out = orig(world, p, target, eff)
        made = [e for e in world.events[n_ev:] if e["k"] == "play" and e.get("a") == p.id and e.get("thing")]
        era = era_of(world.tick)
        tag = "led" if led else "free"
        self.c[f"play:{tag}"] += 1
        self.c[f"play:{tag}:{era}"] += 1
        for e in made:
            sig = e["thing"]
            self.c[f"made:{tag}"] += 1
            new_world = sig not in known_world
            if new_world:
                use = self.useful(sig)
                self.c[f"newworld:{tag}"] += 1
                self.c[f"newworld_useful:{tag}"] += use
                self.c[f"newworld:{tag}:{era}"] += 1
                self.c[f"newworld_useful:{tag}:{era}"] += use
                self.remade[sig] = [world.tick, tag, False, use]
                if use:
                    self.pending[(p.id, sig)] = world.tick
            elif sig not in known_me:
                self.c[f"newme:{tag}"] += 1
        return out

    # --- first use and learning ---------------------------------------------------------------------------------------
    def judge_use(self, orig, world, p, index, use):
        from acl.matter import factor
        if index < 0:
            return orig(world, p, index, use)
        it = p.items[index]
        sig = it["sig"]
        felt = max(-1.0, min(1.0, factor(it, use) - 1.0))
        x = self.vec(it)
        key = (p.id, sig)
        if key not in self.seen:
            self.seen.add(key)
            before = p.itemval.get(sig, 0.0)
            hist = [h for h in self.hist[p.id] if h[3] != sig]
            pred = knn([(h[0], h[1], h[2]) for h in hist], x, use)
            era = era_of(world.tick)
            new_world_kind = sig in self.remade
            grp = "wb" if new_world_kind else "all"
            for g in ({"all", grp}):
                self.c[f"first:{g}"] += 1
                self.c[f"first_err_before:{g}"] += abs(felt - before)
                if pred is not None:
                    vecs = [h[0] for h in hist]
                    self.shuf.shuffle(vecs)
                    shuf = [(v, h[1], h[2]) for v, h in zip(vecs, hist)]
                    ps = knn(shuf, x, use)
                    self.c[f"pred_n:{g}"] += 1
                    self.c[f"pred_err_knn:{g}"] += abs(felt - pred)
                    self.c[f"pred_err_shuf:{g}"] += abs(felt - ps)
                    self.c[f"pred_err_zero:{g}"] += abs(felt)
                    self.c[f"pred_n:{g}:{era}"] += 1
                    self.c[f"pred_err_knn:{g}:{era}"] += abs(felt - pred)
                    self.c[f"pred_err_shuf:{g}:{era}"] += abs(felt - ps)
                else:
                    self.c[f"pred_nohist:{g}"] += 1
            if self.pending.pop(key, None) is not None:
                self.c["new_useful_used_by_maker"] += 1
            self.learn[key] = 0
        out = orig(world, p, index, use)
        if key in self.learn:
            self.learn[key] += 1
            if abs(p.itemval.get(sig, 0.0) - felt) < 0.1:
                self.c["learned"] += 1
                self.c["uses_to_learn"] += self.learn.pop(key)
        self.hist[p.id].append((x, use, felt, sig))
        return out

    def __call__(self, world, events):
        tick = world.tick - 1
        for ev in events:
            if ev["k"] in ("make", "play") and ev.get("thing") in self.remade:
                r = self.remade[ev["thing"]]
                if ev["t"] > r[0] and not r[2]:
                    r[2] = True
        if tick % 4 == 0 and self.pending:              # new useful kinds lost before their maker used them
            for (pid, sig), t0 in list(self.pending.items()):
                p = world.people.get(pid)
                if p is None or not p.alive:
                    self.c["new_useful_lost_dead"] += 1
                    del self.pending[(pid, sig)]
                elif not any(it["sig"] == sig for it in p.items):
                    self.c["new_useful_lost_gone"] += 1
                    del self.pending[(pid, sig)]
        if tick % WPY == WPY - 1:
            self.census.append([tick // WPY, len(world.living())])

    def results(self):
        c = dict(self.c)
        for sig, (t0, tag, again, use) in self.remade.items():
            c[f"newworld_remade:{tag}"] = c.get(f"newworld_remade:{tag}", 0) + again
            c[f"newworld_useful_remade:{tag}"] = c.get(f"newworld_useful_remade:{tag}", 0) + (again and use)
        c["new_useful_pending_end"] = len(self.pending)
        return {"counts": c, "mismatch": dict(self.mismatch), "census_fields": ["year", "living"], "census": self.census}


def install(w, obs):
    from acl import actions
    o_play, o_judge = actions._play, actions._judge_use

    def play(world, p, target, eff):
        if world is not w:
            return o_play(world, p, target, eff)
        return obs.play(o_play, world, p, target, eff)

    def judge_use(world, p, index, use):
        if world is not w:
            return o_judge(world, p, index, use)
        return obs.judge_use(o_judge, world, p, index, use)

    actions._play = play
    actions._judge_use = judge_use
    if hasattr(actions, "HANDLERS"):
        actions.HANDLERS = {k: (play if v is o_play else v) for k, v in actions.HANDLERS.items()}


def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = PG0Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        res = obs.results()
        extra = ":" + json.dumps({**res["mismatch"], "_firsts": res["counts"].get("first:all", 0),
                                  "_plays": res["counts"].get("play:led", 0) + res["counts"].get("play:free", 0)},
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
        t = same and not any(mism.values()) and info.get("_firsts", 0) > 0 and info.get("_plays", 0) > 0
        ok &= t
        lines.append(f"arm lp, seed {seed}, {years} years: identical with and without the observer (state and random "
                     f"numbers): {'yes' if same else 'NO'}; mismatches: {mism or 'none'}; first uses "
                     f"{info.get('_firsts')}, plays {info.get('_plays')}")
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
    obs = PG0Obs(w)
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
