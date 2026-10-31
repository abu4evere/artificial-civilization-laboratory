"""ES1 — do minds learn more accurately with an expected look-ahead? (questions.md, frozen as `ES1-frozen`). A nature-
change test in a copy: `code_es1` = `code_v11` + `expected_lookahead` (0 = v11). Arms v11 (0), e (1), x (sham).
The observer is read-only:
  biology._learn    every habit update (all ages): replayed under the arm's own rule (mismatch counter), and the
                    realized return G = sum_k 0.8^k r over the person's next updates (VC1's method), closed when the
                    weight falls below 0.001 or at death (censored)
  forage action     TR1's food with and without the tool in hand
  events            make, death; a yearly census

  python experiments/ES1_expected_lookahead/run_es1.py zero
  python experiments/ES1_expected_lookahead/run_es1.py one <arm> <seed> <years> <out>
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
CODES = {"es1": HERE / "code_es1", "v11": EXP / "NV11_nature_v11" / "code_v11"}
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(21401, 21433))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9999, 9998)
V11 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
       "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1,
       "ground_items": 1, "curiosity_pull": 1}
LP = {"founders": 80, "width": 80, "height": 80}
ARMS = {"c": {**LP, "expected_lookahead": 0}, "e": {**LP, "expected_lookahead": 1}, "x": {**LP, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
LATE = (100 * WPY, 200 * WPY)
ADULT = 16 * WPY
CUT = 0.001                                # close G when the weight 0.8^k falls below this (31 updates)


def setup(code="es1"):
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


def fingerprint(code="es1"):
    from run_e7 import code_hash
    return code_hash(CODES[code] / "acl")


def lookahead(c, row):
    """The arm's own look-ahead over the next situation's habit values (the law, replayed)."""
    if getattr(c, "expected_lookahead", 0):
        k = c.learned_weight / c.choice_temperature
        top = max(row)
        w = [math.exp(k * (v - top)) for v in row]
        return sum(wi * v for wi, v in zip(w, row)) / sum(w)
    return max(row)


def forage_got(rate, eff, room, crop, plants):
    want = min(rate * eff, room)
    from_crop = min(crop, want * 1.3)
    from_wild = min(plants, max(0.0, want - from_crop / 1.3))
    return from_crop + from_wild


class ES1Obs:
    def __init__(self, w):
        from acl.person import ACTIONS, N_ACTIONS
        self.w = w
        self.acts = ACTIONS
        self.N = N_ACTIONS
        self.mismatch = Counter()
        self.cal = defaultdict(lambda: [0, 0.0, 0.0, 0])    # action -> [n closed, sum |q-G|, sum (q-G), censored]
        self.pending = defaultdict(list)                     # person -> [[action, q, acc, disc, late]]
        self.s = defaultdict(float)
        self.census = []

    def close(self, e, censored):
        a, q, acc, _, late = e
        if not late:
            return
        c = self.cal[a]
        c[0] += 1
        c[1] += abs(q - acc)
        c[2] += q - acc
        c[3] += censored

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
        keep.append([self.acts[i % self.N], before, r, c.discount, late])
        self.pending[p.id] = keep
        self.s["updates"] += 1

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
        return {"cal_fields": ["n", "sum_abs", "sum_signed", "censored"], "cal": {k: v for k, v in self.cal.items()},
                "sums": dict(self.s), "mismatch": dict(self.mismatch),
                "open_at_end": sum(len(v) for v in self.pending.values()),
                "census_fields": ["year", "living", "adults"], "census": self.census}


def install(w, obs):
    from acl import actions, biology
    from acl.mind import context_index
    from acl.person import A
    o_learn = biology._learn
    o_forage = actions.HANDLERS["forage"]

    def learn(world, p):
        if world is not w or p.last_action is None:
            return o_learn(world, p)
        c = world.cfg
        i = p.last_ctx * obs.N + A[p.last_action]
        near = world.people_near(p.loc, c.reach, exclude=p.id)
        nxt = context_index(world, p, bool(near))
        fut = lookahead(c, p.q[nxt * obs.N:(nxt + 1) * obs.N])
        r = p.reward + 2.0 * (p.mood - p.mood_before)
        before = p.q[i]
        out = o_learn(world, p)
        obs.on_learn(world, p, i, before, p.q[i], r, fut)
        return out

    def forage(world, p, target, eff):
        if world is not w:
            return o_forage(world, p, target, eff)
        got = obs.before_forage(world, p, eff)
        out = o_forage(world, p, target, eff)
        obs.after_forage(world, p, got)
        return out

    biology._learn = learn
    actions.HANDLERS["forage"] = forage


def hashrun(code, arm, seed, years, observe):
    setup(code)
    kw = dict(ARMS[arm])
    if code == "v11":
        kw.pop("expected_lookahead", None)
    w = make_world(seed, kw)
    obs = None
    if observe:
        obs = ES1Obs(w)
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
    a = make_world(seed, ARMS["e"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for x in (a, b):
        for _ in range(5 * WPY):
            x.step()
    return world_hash(a) == world_hash(b) and b.cfg.expected_lookahead == 1


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
             for code, arm, obs in (("v11", "c", 0), ("es1", "c", 0), ("es1", "e", 1), ("es1", "e", 0), ("es1", "x", 0))]
    with ThreadPoolExecutor(5) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        v11 = got[("v11", "c", seed, years, 0)]
        c0 = got[("es1", "c", seed, years, 0)]
        e1 = got[("es1", "e", seed, years, 1)]
        e0 = got[("es1", "e", seed, years, 0)]
        x0 = got[("es1", "x", seed, years, 0)]
        same, ro, acts, sham = hs(v11) == hs(c0), hs(e1) == hs(e0), hs(e0) != hs(c0), hs(x0) != hs(c0)
        info = json.loads(e1.split(":", 2)[2])
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = same and ro and acts and sham and not any(mism.values()) and info.get("_updates", 0) > 0
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_es1 with expected_lookahead 0 = code_v11: {'yes' if same else 'NO'}; "
                     f"observer read-only (arm e): {'yes' if ro else 'NO'}; the law acts: {'yes' if acts else 'NO'}; "
                     f"the sham acts: {'yes' if sham else 'NO'}; update-replay mismatches: {mism or 'none'}; habit "
                     f"updates replayed {info.get('_updates'):.0f}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm e, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_es1 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = ES1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_es1", "code_hash": f0, "code_hash_after": fingerprint(),
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
