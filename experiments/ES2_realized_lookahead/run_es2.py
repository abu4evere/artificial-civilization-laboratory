"""ES2 — do minds learn more accurately when they look ahead by their real next choice? (questions.md, frozen as
`ES2-frozen`). A nature-change test in a copy: `code_es2` = `code_v11` + `realized_lookahead` (0 = v11). Arms v11 (0),
r (1), x (sham). ES1's runner, adapted. The observer is read-only:
  biology._learn      arms v11 and sham: every habit update, replayed (max look-ahead)
  biology.apply_held  arm r: every held update completed at the next decision, replayed (expected over the real choice)
  for both            the realized return G = sum_k 0.8^k r over the person's next updates (VC1's method), by situation
                      and action; closed when the weight falls below 0.001 or at death (censored); held updates dropped
                      at death are counted
  thought.steer       every 20th decision: the instinct share Var(score - 0.6 q) / Var(score) (described)
  forage action       TR1's food with and without the tool in hand
  events              make, death; a yearly census

  python experiments/ES2_realized_lookahead/run_es2.py zero
  python experiments/ES2_realized_lookahead/run_es2.py one <arm> <seed> <years> <out>
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
CODES = {"es2": HERE / "code_es2", "v11": EXP / "NV11_nature_v11" / "code_v11"}
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(21501, 21533))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9989, 9988)
V11 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
       "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1,
       "ground_items": 1, "curiosity_pull": 1}
LP = {"founders": 80, "width": 80, "height": 80}
ARMS = {"c": {**LP, "realized_lookahead": 0}, "r": {**LP, "realized_lookahead": 1}, "x": {**LP, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
LATE = (100 * WPY, 200 * WPY)
ADULT = 16 * WPY
CUT = 0.001                                # close G when the weight 0.8^k falls below this (31 updates)


def setup(code="es2"):
    sys.path.insert(0, str(CODES[code]))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **{**V11, **kw}))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def rng_state(w):
    return hashlib.sha256(repr(w.rng.getstate()).encode()).hexdigest()


def fingerprint(code="es2"):
    from run_e7 import code_hash
    return code_hash(CODES[code] / "acl")


def realized(c, p, opts, base):
    """ES2's look-ahead, replayed: the expected habit value of this decision under its real choice."""
    from acl.person import A
    if not opts:
        return p.q[base + A["rest"]]
    top = max(s for s, _ in opts)
    w = [math.exp((s - top) / c.choice_temperature) for s, _ in opts]
    return sum(wi * p.q[base + A[a]] for wi, (_, a) in zip(w, opts)) / sum(w)


def forage_got(rate, eff, room, crop, plants):
    want = min(rate * eff, room)
    from_crop = min(crop, want * 1.3)
    from_wild = min(plants, max(0.0, want - from_crop / 1.3))
    return from_crop + from_wild


class ES2Obs:
    def __init__(self, w):
        from acl.person import ACTIONS, N_ACTIONS
        self.w = w
        self.acts = ACTIONS
        self.N = N_ACTIONS
        self.mismatch = Counter()
        self.cal = defaultdict(lambda: [0, 0.0, 0.0, 0, 0.0, 0.0])   # "ctx|action" -> [n, sum |q-G|, sum (q-G),
                                                                    #   censored, sum q, sum G]
        self.pending = defaultdict(list)                     # person -> [[key, q, acc, disc, late]]
        self.inst = [0, 0.0]                                 # sampled decisions, sum of instinct shares
        self.s = defaultdict(float)
        self.census = []

    def close(self, e, censored):
        key, q, acc, _, late = e
        if not late:
            return
        c = self.cal[key]
        c[0] += 1
        c[1] += abs(q - acc)
        c[2] += q - acc
        c[3] += censored
        c[4] += q
        c[5] += acc

    def on_learn(self, world, p, i, before, after, r, fut):
        c = world.cfg
        unclipped = before + c.learning_rate * (r + c.discount * fut - before)
        if abs(max(-1.5, min(1.5, unclipped)) - after) > 1e-12:
            self.mismatch["td_replay"] += 1
        keep = []
        for e in self.pending.get(p.id, ()):
            e[2] += e[3] * r
            e[3] *= c.discount
            if e[3] < CUT:
                self.close(e, 0)
            else:
                keep.append(e)
        late = LATE[0] <= world.tick < LATE[1]
        keep.append([f"{i // self.N}|{self.acts[i % self.N]}", before, r, c.discount, late])
        self.pending[p.id] = keep
        self.s["updates"] += 1

    def instinct(self, world, p, options):
        """Every 20th decision: the share of the options' score variance not carried by habit (described)."""
        self.s["decisions"] += 1
        if self.s["decisions"] % 20 or len(options) < 2:
            return
        from acl.person import A
        b = p.last_ctx * self.N
        lw = world.cfg.learned_weight
        sc = [o[0] for o in options]
        ins = [o[0] - lw * p.q[b + A[o[1]]] for o in options]

        def var(x):
            m = sum(x) / len(x)
            return sum((v - m) ** 2 for v in x) / len(x)
        vs = var(sc)
        if vs > 0:
            self.inst[0] += 1
            self.inst[1] += var(ins) / vs

    def before_forage(self, world, p, eff):
        from acl.matter import best_item, carry_capacity
        from acl.mind import forage_rate
        tile = world.tile(p.loc)
        _, tf = best_item(p, "forage")
        rate = forage_rate(world, p)
        room = max(0.0, carry_capacity(world, p) - p.edible())
        return (forage_got(rate, eff, room, tile.crop, tile.plants),
                forage_got(rate / tf, eff, room, tile.crop, tile.plants))

    def after_forage(self, world, p, got):
        if LATE[0] <= world.tick < LATE[1] and p.age(world.tick) >= ADULT and p.alive:
            self.s["food_with"] += got[0]
            self.s["food_without"] += got[1]

    def __call__(self, world, events):
        tick = world.tick - 1
        late = LATE[0] <= tick < LATE[1]
        for ev in events:
            k = ev["k"]
            if k == "death":
                for e in self.pending.pop(ev.get("a"), ()):
                    self.close(e, 1)                   # rewards end at death
                q = world.people.get(ev.get("a"))
                if q is not None and getattr(q, "held", None) is not None:
                    self.s["held_dropped"] += 1        # a held update that will never be completed
                if late and ev.get("age", 0) >= 16:
                    self.s["adult_deaths"] += 1
            elif k == "make" and late:
                a = ev.get("a")
                if a in world.people and world.people[a].age(world.tick) >= ADULT:
                    self.s["adult_makes"] += 1
        if late:
            living = world.living()
            self.s["living_weeks"] += len(living)
            self.s["adult_weeks"] += sum(1 for p in living if p.age(world.tick) >= ADULT)
        if tick % WPY == WPY - 1:
            living = world.living()
            self.census.append([tick // WPY, len(living), sum(1 for p in living if p.age(world.tick) >= ADULT)])

    def results(self):
        return {"cal_fields": ["n", "sum_abs", "sum_signed", "censored", "sum_q", "sum_G"],
                "cal": {k: v for k, v in self.cal.items()}, "instinct": self.inst,
                "sums": dict(self.s), "mismatch": dict(self.mismatch),
                "open_at_end": sum(len(v) for v in self.pending.values()),
                "census_fields": ["year", "living", "adults"], "census": self.census}


def install(w, obs):
    from acl import actions, biology, thought
    from acl.mind import context_index
    from acl.person import A
    o_learn = biology._learn
    o_forage = actions.HANDLERS["forage"]
    o_held = getattr(biology, "apply_held", None)
    o_steer = thought.steer

    def learn(world, p):
        if world is not w or p.last_action is None or getattr(world.cfg, "realized_lookahead", 0):
            return o_learn(world, p)              # arm r: the update is held; recorded when completed
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

    def apply_held(world, p, opts, base):
        if world is not w:
            return o_held(world, p, opts, base)
        i, r = p.held
        fut = realized(world.cfg, p, opts, base)
        before = p.q[i]
        out = o_held(world, p, opts, base)
        obs.on_learn(world, p, i, before, p.q[i], r, fut)
        return out

    def steer(p, options):
        out = o_steer(p, options)
        if w.people.get(p.id) is p:
            obs.instinct(w, p, out)
        return out

    def forage(world, p, target, eff):
        if world is not w:
            return o_forage(world, p, target, eff)
        got = obs.before_forage(world, p, eff)
        out = o_forage(world, p, target, eff)
        obs.after_forage(world, p, got)
        return out

    biology._learn = learn
    if o_held is not None:
        biology.apply_held = apply_held
    thought.steer = steer
    actions.HANDLERS["forage"] = forage


def hashrun(code, arm, seed, years, observe):
    setup(code)
    kw = dict(ARMS[arm])
    if code == "v11":
        kw.pop("realized_lookahead", None)
    w = make_world(seed, kw)
    obs = None
    if observe:
        obs = ES2Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        extra = ":" + json.dumps({**obs.mismatch, "_updates": obs.s["updates"]}, sort_keys=True, separators=(",", ":"))
    return world_hash(w) + ":" + rng_state(w) + extra


def reload_check(seed):
    setup()
    from acl.world import World
    a = make_world(seed, ARMS["r"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    held = sum(1 for p in b.people.values() if p.alive and p.held is not None)
    for x in (a, b):
        for _ in range(5 * WPY):
            x.step()
    return world_hash(a) == world_hash(b) and b.cfg.realized_lookahead == 1 and held > 0


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
    specs = [(code, arm, seed, years, obs) for seed, years in ((501, 20), (601, 60))
             for code, arm, obs in (("v11", "c", 0), ("es2", "c", 0), ("es2", "r", 1), ("es2", "r", 0), ("es2", "x", 0))]
    with ThreadPoolExecutor(5) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        v11 = got[("v11", "c", seed, years, 0)]
        c0 = got[("es2", "c", seed, years, 0)]
        e1 = got[("es2", "r", seed, years, 1)]
        e0 = got[("es2", "r", seed, years, 0)]
        x0 = got[("es2", "x", seed, years, 0)]
        same, ro, acts, sham = hs(v11) == hs(c0), hs(e1) == hs(e0), hs(e0) != hs(c0), hs(x0) != hs(c0)
        info = json.loads(e1.split(":", 2)[2])
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = same and ro and acts and sham and not any(mism.values()) and info.get("_updates", 0) > 0
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_es2 with realized_lookahead 0 = code_v11: {'yes' if same else 'NO'}; "
                     f"observer read-only (arm r): {'yes' if ro else 'NO'}; the law acts: {'yes' if acts else 'NO'}; "
                     f"the sham acts: {'yes' if sham else 'NO'}; update-replay mismatches: {mism or 'none'}; habit "
                     f"updates replayed {info.get('_updates'):.0f}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm r, seed 501 (held updates saved): saved at year 10 and reloaded, continues exactly to year 15: "
                 f"{'yes' if t else 'NO'}")
    lines.append(f"code_es2 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = ES2Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_es2", "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": world_hash(w), **obs.results()}
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
