"""AM2 — AM1's autonomy battery, unchanged, on nature v12 (questions.md, frozen as `AM2-frozen`): AM1's runner with only
the code, seeds and labels changed (am1_to_am2.diff).
Read-only on live nature v12 (`code_v12`); the arms change existing settings only: v12 (c), no habits (h,
learned_weight 0), fewer acts (a, stage E0-C), more chance (t, choice_temperature 0.25; amendment 1), sham (x). ES2's runner supplies
the set-up (`../ES2_realized_lookahead/run_es2.py`). AM1's observer records, for adults aged 16-49 in years 100-200:
  M1   SC1's C12 snapshots (year-t action and situation shares, habit summary) every 5 years
  M2   per adult-year: mutual information of consecutive actions, minus a time-shuffled copy (own random stream)
  M3   gather chains and opportunity-matched chains, and whether a recipe using the material is made within 8 weeks
  M5   the same, for chains whose next decision is a food action
  M4   decisions whose target is new to the person
  M6a  first makes of a recipe that use an input the person never used or gathered before
  M6b  completions of established gather-make chains under a cue (season x food band) not seen before for that pair

  python experiments/AM2_autonomy_measures_v12/run_am2.py zero
  python experiments/AM2_autonomy_measures_v12/run_am2.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import math
import random
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.CODES["v12"] = HERE.parent / "NV12_nature_v12" / "code_v12"
CODE = "v12"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(22801, 22833))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9905, 9904)
ARMS = {"c": {**base.LP},
        "h": {**base.LP, "learned_weight": 0.0},
        "a": {**base.LP, "stage": "E0-C"},
        "t": {**base.LP, "choice_temperature": 0.25},     # amendment 1 (survival only; 0.6 died out)
        "x": {**base.LP, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
ADULT, OLD = 16 * WPY, 50 * WPY
LATE = [100 * WPY, 200 * WPY]
CHAIN = 8
GATHERABLE = ("stone", "flint", "wood", "fiber", "clay", "char")
TILE_ACTS = ("forage", "hunt", "explore", "flee", "join")
PERSON_ACTS = ("give", "care", "talk", "court", "steal", "attack")
FOOD_ACTS = ("forage", "hunt", "take")


class AM1Obs:
    def __init__(self, w):
        from acl.person import A, N_ACTIONS
        self.w, self.A, self.N = w, A, N_ACTIONS
        self.s = Counter()
        self.snaps = []
        self.ya, self.yc = {}, {}
        self.seq = defaultdict(list)
        self.tiles = defaultdict(set)
        self.people = defaultdict(set)
        self.made = defaultdict(set)
        self.handled = defaultdict(set)
        self.chains = defaultdict(list)   # pid -> [[tick, m, recipes, kind 'g'|'m', next food action or None]]
        self.done = defaultdict(lambda: defaultdict(list))   # pid -> (m, recipe) -> cues of completions
        self.rng = random.Random(w.cfg.seed * 7919 + 1)

    def counted(self, p, tick):
        return LATE[0] <= tick < LATE[1] and ADULT <= p.age(tick) < OLD

    def decision(self, world, p, option):
        """Before p acts this week (p is where they decided, p.last_ctx is this week's situation)."""
        from acl.mind import recipe_materials
        tick = world.tick
        act, target = option
        here = (p.loc[0], p.loc[1])
        ok = self.counted(p, tick)
        if act in TILE_ACTS or act == "gather":
            t = target[0] if act == "gather" else target
            t = (t[0], t[1]) if isinstance(t, tuple) else None
            if ok and t is not None:
                self.s["m4_tile_decisions"] += 1
                self.s["m4_tile_new"] += t not in self.tiles[p.id]
            if t is not None:
                self.tiles[p.id].add(t)
        elif act in PERSON_ACTS:
            if ok:
                self.s["m4_person_decisions"] += 1
                self.s["m4_person_new"] += target not in self.people[p.id]
            self.people[p.id].add(target)
        elif act == "make" and ok:
            self.s["m4_make_decisions"] += 1
            self.s["m4_make_new"] += target not in self.made[p.id]
        self.tiles[p.id].add(here)
        if act == "gather":
            self.handled[p.id].add(target[1])
        if not ok:
            return
        self.s["adult_decisions"] += 1
        y = tick // WPY
        if y % 5 == 0:
            a = self.ya.setdefault((p.id, y), [0] * self.N)
            c = self.yc.setdefault((p.id, y), [0] * 32)
            a[self.A[act]] += 1
            c[p.last_ctx] += 1
        self.seq[p.id].append(self.A[act])
        for ch in self.chains.get(p.id, ()):
            if ch[4] is None and ch[0] < tick:
                ch[4] = act in FOOD_ACTS
        rel = {}
        for sig, r in p.recipes.items():
            if p.itemval.get(sig, 0.0) > 0.05:
                for m in recipe_materials(r):
                    if m in GATHERABLE and p.mats.get(m, 0.0) < 1.0:
                        rel.setdefault(m, set()).add(sig)
        if not rel or tick + CHAIN >= LATE[1]:
            return
        if act == "gather" and target[1] in rel:
            m = target[1]
            self.chains[p.id].append([tick, m, frozenset(rel[m]), "g", None])
        elif act != "gather":
            tile = world.tile(p.loc)
            for m in GATHERABLE:
                if m in rel and tile.material(m) >= 1.0:
                    self.chains[p.id].append([tick, m, frozenset(rel[m]), "m", None])
                    break

    def made_thing(self, world, p, sig, recipe, how):
        """p made a thing by recipe `sig` this week (how: 'make' or 'play')."""
        from acl.mind import recipe_materials
        from acl.matter import MATERIALS
        tick = world.tick
        ok = self.counted(p, tick)
        inputs = set(recipe_materials(recipe)) | {x for x in recipe.get("parts", ()) if x not in MATERIALS}
        if recipe.get("verb") == "heat":
            inputs.add(recipe["part"])
        if sig not in self.made[p.id]:
            if ok:
                self.s["m6a_new_acts"] += 1
                self.s["m6a_new_in_steps"] += any(x not in self.handled[p.id] for x in inputs)
            self.made[p.id].add(sig)
        self.handled[p.id] |= inputs
        if how != "make":
            return
        cue = (world.season, p.last_ctx // 8)
        for ch in self.chains.get(p.id, ()):
            if ch[0] < tick <= ch[0] + CHAIN and sig in ch[2] and len(ch) == 5:
                ch.append(True)
                if ch[3] == "g":
                    prior = self.done[p.id][(ch[1], sig)]
                    if len(prior) >= 2 and ok:
                        self.s["m6b_established"] += 1
                        self.s["m6b_new_cue"] += cue not in prior
                    prior.append(cue)

    def __call__(self, world, events):
        tick = world.tick - 1
        for pid in list(self.chains):
            keep = []
            for ch in self.chains[pid]:
                if ch[0] + CHAIN > tick and len(ch) == 5:
                    keep.append(ch)
                    continue
                made = len(ch) == 6
                k = ch[3]
                self.s[f"m3_{k}_chains"] += 1
                self.s[f"m3_{k}_made"] += made
                if ch[4]:
                    self.s[f"m5_{k}_chains"] += 1
                    self.s[f"m5_{k}_made"] += made
            if keep:
                self.chains[pid] = keep
            else:
                del self.chains[pid]
        if LATE[0] <= tick < LATE[1]:
            living = world.living()
            self.s["living_weeks"] += len(living)
            self.s["adult_weeks"] += sum(1 for p in living if ADULT <= p.age(world.tick) < OLD)
        if tick % WPY == WPY - 1:
            self.year_end(world, tick // WPY)

    def year_end(self, world, y):
        for pid, s in self.seq.items():
            if len(s) >= 40:
                sh = list(s)
                self.rng.shuffle(sh)
                self.s["m2_person_years"] += 1
                self.s["m2_mi_sum"] += mi(s) - mi(sh)
        self.seq = defaultdict(list)
        if y % 5 == 0 and LATE[0] <= y * WPY < LATE[1]:
            for p in world.living():
                if not (ADULT <= p.age(world.tick) < OLD):
                    continue
                a, c = self.ya.get((p.id, y)), self.yc.get((p.id, y))
                if not a or not sum(a):
                    continue
                tot = sum(c)
                hab = [round(sum(c[x] / tot * p.q[x * self.N + j] for x in range(32) if c[x]), 4)
                       for j in range(self.N)]
                self.snaps.append([p.id, y, round(p.years(world.tick), 2), p.sex,
                                   [p.genes[g] for g in sorted(p.genes)], a, c, hab])
        for key in [k for k in self.ya if k[1] < y - 6]:
            self.ya.pop(key, None)
            self.yc.pop(key, None)

    def results(self):
        return {"sums": dict(self.s), "snap_fields": ["person", "year", "age", "sex", "genes", "actions", "situations",
                                                       "habit"], "snaps": self.snaps}


def mi(s):
    """Mutual information (bits) between consecutive entries of s."""
    pairs = Counter(zip(s, s[1:]))
    n = sum(pairs.values())
    if not n:
        return 0.0
    left, right = Counter(), Counter()
    for (x, y), k in pairs.items():
        left[x] += k
        right[y] += k
    return sum(k / n * math.log2(k * n / (left[x] * right[y])) for (x, y), k in pairs.items())


def install(w, obs):
    from acl import actions, knowhow
    o_perform, o_make, o_rem = actions.perform, actions.HANDLERS["make"], knowhow.remember_recipe

    def perform(world, p, option):
        if world is w and option:
            obs.decision(world, p, option)
        return o_perform(world, p, option)

    def make(world, p, sig, eff):
        if world is not w:
            return o_make(world, p, sig, eff)
        recipe = p.recipes.get(sig)
        n0 = len(world.events)
        out = o_make(world, p, sig, eff)
        if recipe is not None and any(ev["k"] == "make" and ev.get("a") == p.id for ev in world.events[n0:]):
            obs.made_thing(world, p, sig, recipe, "make")
        return out

    def remember_recipe(world, p, sig, recipe, how, source=None, props=None, meant=None):
        out = o_rem(world, p, sig, recipe, how, source, props, meant)
        if world is w and how == "made":
            obs.made_thing(world, p, sig, recipe, "play")
        return out
    actions.perform = perform
    actions.HANDLERS["make"] = make
    knowhow.remember_recipe = remember_recipe


def hashrun(arm, seed, years, observe):
    LATE[0], LATE[1] = 0, years * WPY       # zero checks: every year counted
    base.setup(CODE)
    w = base.make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = AM1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        extra = ":" + json.dumps({k: obs.s[k] for k in ("adult_decisions", "m3_g_chains", "m3_g_made", "m3_m_chains",
                                                        "m3_m_made", "m6a_new_acts", "m6b_established")},
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
    specs = [(arm, seed, years, obs) for seed, years in ((501, 20), (601, 60))
             for arm, obs in (("c", 0), ("c", 1), ("h", 0), ("h", 1), ("a", 0), ("a", 1), ("t", 0), ("t", 1), ("x", 0))]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        g = {(a, o): got[(a, sd, yr, o)] for a, sd, yr, o in specs if sd == seed}
        ro = all(hs(g[(a, 0)]) == hs(g[(a, 1)]) for a in ("c", "h", "a", "t"))
        acts = all(hs(g[(a, 0)]) != hs(g[("c", 0)]) for a in ("h", "a", "t", "x"))
        info = {a: json.loads(g[(a, 1)].split(":", 2)[2]) for a in ("c", "h", "a", "t")}
        sane = info["a"]["m3_g_made"] == 0 and info["a"]["m3_m_made"] == 0
        t = ro and acts and sane
        ok &= t
        lines.append(f"seed {seed}, {years} years: observer read-only (c, h, a, t): {'yes' if ro else 'NO'}; h, a, t and "
                     f"the sham act: {'yes' if acts else 'NO'}; arm a completes no chain: {'yes' if sane else 'NO'}; "
                     f"{info}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm c, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_v12 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = base.make_world(seed, ARMS[arm])
    obs = AM1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_v12", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, chains {obs.s['m3_g_chains']}/{obs.s['m3_m_chains']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: every year counted; never study data
        LATE[0], LATE[1] = 0, int(sys.argv[4]) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
