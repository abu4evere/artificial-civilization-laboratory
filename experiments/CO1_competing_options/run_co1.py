"""CO1 — what made the other options stronger? (questions.md, frozen as `CO1-frozen`). Read-only: live nature v7
(`code_v7`) unchanged, with one read-only wrapper on `thought.steer` (as MK1) that reads every option's score before and
after the thought's pull, and calls the original unchanged.

For every person-week in which "make" is offered, the other options are grouped by action family; each family's soft
score L_a splits exactly into habit h_a + T·ln n_a + per-entry score M_a, and U_other = Σ s_a·L_a + T·H. Sums go into
MK1's matched-state cells. Within-world counterfactual swaps use each world's own early (years 0-10) means.

  python experiments/CO1_competing_options/run_co1.py zero
  python experiments/CO1_competing_options/run_co1.py one <arm> <seed> <years> <out>
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
SEEDS = tuple(range(18401, 18433))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9955, 9954)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
ARMS = {"lp": {"founders": 80, "width": 80, "height": 80}}
JOBS = [f"lp:{s}" for s in SEEDS]
BIN_EDGES = (0, 5, 10, 20, 50, 100, 200)
EARLY_END = 10 * WPY
T = 0.2
HUNGER_EDGES = (0.25, 0.5, 0.75)
FOOD_EDGES = (0.5, 2.0)
SWAPS = ("n", "h", "m", "all")


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


class CO1Obs:
    def __init__(self, w):
        self.w = w
        assert abs(w.cfg.choice_temperature - T) < 1e-12
        self.cells = defaultdict(lambda: defaultdict(float))
        self.early = defaultdict(lambda: [0.0, 0.0, 0.0, 0])   # (state, family) -> sums of n, h, m, count (years 0-10)
        self.week = {}
        self.mismatch = Counter()

    def on_options(self, world, p, before, after):
        from acl.matter import best_item
        from acl.mind import hunger_of
        from acl.person import A, N_ACTIONS
        tick = world.tick
        if p.stage(tick) not in ("teen", "adult", "elder"):
            return
        mk = [i for i, o in enumerate(after) if o[1] == "make"]
        if not mk:
            return
        c = world.cfg
        u_m = after[mk[0]][0]
        fam = defaultdict(list)
        for i, o in enumerate(after):
            if i != mk[0]:
                fam[o[1]].append(o[0])
        if not fam:
            return
        lw = c.learned_weight
        base = p.last_ctx * N_ACTIONS
        parts = {}
        for a, xs in fam.items():
            L = lse(xs)
            h = lw * p.q[base + A[a]]
            n = len(xs)
            parts[a] = (L, h, n, L - h - T * math.log(n))
        u_other = lse([v[0] for v in parts.values()])
        direct = lse([x for xs in fam.values() for x in xs])
        if abs(u_other - direct) > 1e-9:
            self.mismatch["family_lse"] += 1
        s = {a: math.exp((v[0] - u_other) / T) for a, v in parts.items()}
        ent = -sum(x * math.log(x) for x in s.values() if x > 0)
        recon = sum(s[a] * (parts[a][1] + T * math.log(parts[a][2]) + parts[a][3]) for a in parts) + T * ent
        if abs(recon - u_other) > 1e-9:
            self.mismatch["identity"] += 1
        dep_need = sum(d.need(c, tick) for d in world.dependents(p.id))
        hunger = hunger_of(world, p, dep_need)
        _, tool_f = best_item(p, "forage")
        tile = world.tile(p.loc)
        need = p.need(c, tick)
        age = "teen" if p.age(tick) < 16 * WPY else "adult"
        state = (age, band(hunger, HUNGER_EDGES), int(tool_f > 1.0), band((tile.plants + tile.crop) / need, FOOD_EDGES))
        bi = bin_of(tick)
        cell = self.cells["|".join(map(str, (bi,) + state))]
        cell["offered"] += 1
        cell["u_m"] += u_m
        cell["u_other"] += u_other
        cell["spread"] += T * ent
        cell["logit"] += (u_m - u_other) / T
        cell["near"] += len(world.people_near(p.loc, c.reach, exclude=p.id))
        for a, (L, h, n, m) in parts.items():
            cell[f"{a}:present"] += 1
            cell[f"{a}:s"] += s[a]
            cell[f"{a}:sh"] += s[a] * h
            cell[f"{a}:sn"] += s[a] * T * math.log(n)
            cell[f"{a}:sm"] += s[a] * m
            cell[f"{a}:n"] += n
            cell[f"{a}:h"] += h
            cell[f"{a}:m"] += m
        # grouped: every family as one entry
        ug = lse([v[1] + v[3] for v in parts.values()])
        cell["logit_grouped"] += (u_m - ug) / T
        if tick < EARLY_END:
            for a, (L, h, n, m) in parts.items():
                e = self.early[(state, a)]
                e[0] += n
                e[1] += h
                e[2] += m
                e[3] += 1
        else:
            for sw in SWAPS:
                vals = []
                for a, (L, h, n, m) in parts.items():
                    e = self.early.get((state, a))
                    if e is not None and e[3] > 0:
                        en, eh, em = e[0] / e[3], e[1] / e[3], e[2] / e[3]
                        n2 = en if sw in ("n", "all") else n
                        h2 = eh if sw in ("h", "all") else h
                        m2 = em if sw in ("m", "all") else m
                    else:
                        n2, h2, m2 = n, h, m
                        cell[f"swap_{sw}_unmatched"] += 1
                    vals.append(h2 + T * math.log(n2) + m2)
                cell[f"logit_swap_{sw}"] += (u_m - lse(vals)) / T
            cell["swapped"] += 1
        self.week[p.id] = cell

    def __call__(self, world, events):
        chosen = {d.agent_id: (d.chosen[0] if d.chosen else None) for d in world.week_decisions}
        for pid, cell in self.week.items():
            if chosen.get(pid) == "make":
                cell["chosen"] += 1
        self.week = {}

    def results(self):
        return {"cells": {k: dict(v) for k, v in self.cells.items()}, "mismatch": dict(self.mismatch)}


def install(w, obs):
    from acl import thought
    orig = thought.steer

    def steer(p, options):
        before = list(options)
        out = orig(p, options)
        if w.people.get(p.id) is p:
            obs.on_options(w, p, before, out)
        return out

    thought.steer = steer


def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = CO1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        off = sum(c.get("offered", 0) for c in obs.cells.values())
        sw = sum(c.get("swapped", 0) for c in obs.cells.values())
        extra = ":" + json.dumps({**obs.mismatch, "_offered": off, "_swapped": sw}, sort_keys=True,
                                 separators=(",", ":"))
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
        t = same and not any(mism.values()) and info.get("_offered", 0) > 0 and info.get("_swapped", 0) > 0
        ok &= t
        lines.append(f"arm lp, seed {seed}, {years} years: identical with and without the observer (state and random "
                     f"numbers): {'yes' if same else 'NO'}; identity and family mismatches: {mism or 'none'}; offered "
                     f"weeks {info.get('_offered')}, swapped weeks {info.get('_swapped')}")
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
    obs = CO1Obs(w)
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
