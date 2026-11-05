"""PB2 — the episodic brain helps choose, in a copy of nature (questions.md, frozen as `PB2-frozen`).
`code_pb2` = `code_v13` + `brain`, `brain_shadow`, `brain_on_year` (v13_to_pb2.diff); brain 0 = v13.
Arms: c (v13 with a read-only shadow memory scoring r-hat against q), P (brain 1), G (2), G0 (3), sham.
The observer is AM1's (M3, M5, M2 and the rest, unchanged; `../AM1_autonomy_measures/run_am1.py`), counted over years
130-170, plus:
  R          AF1's lineage remaking: world-new kinds made in play, first made in years 130-165, whose own recipe is
             chosen again by a `make` action within 5 years (by anyone; by the inventor apart); intent test 1: remakes
             per adult week holding the kind's inputs, the inventor against others (all others, and others who know the
             recipe); test 2: remakes preceded within 8 weeks by the maker gathering one of its materials
  M3, M5     also apart for people born after the brain came on
  actions    adults' (16-49) chosen actions, by kind
  goals      adult goal weeks by output and direction; each adoption (output, direction, LP); weeks each goal was held
  brain      decisions steered by r-hat and fallbacks to q; arm c: squared errors and moments of r, r-hat and q
  food       a year-end census of adults' edible food

  python experiments/PB2_brain_steers/run_pb2.py zero
  python experiments/PB2_brain_steers/run_pb2.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "AM1_autonomy_measures"))
import run_am1 as A  # noqa: E402

base = A.base
base.CODES["pb2"] = HERE / "code_pb2"
base.CODES["v13"] = HERE.parent / "NV13_nature_v13" / "code_v13"
CODE = "pb2"
A.CODE = "pb2"
WPY, YEARS = base.WPY, 170
SEEDS = tuple(range(23201, 23233))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9893, 9892)
ARMS = {"c": {**base.LP, "brain": 0, "brain_shadow": 1},
        "P": {**base.LP, "brain": 1},
        "G": {**base.LP, "brain": 2},
        "G0": {**base.LP, "brain": 3},
        "x": {**base.LP, "brain": 0, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
ADULT, OLD = 16 * WPY, 50 * WPY
WIN = [130 * WPY, 170 * WPY]
REMAKE = 5 * WPY


class M3Split(A.AM1Obs):
    """AM1's observer, unchanged, plus its M3 and M5 chain counts for people born after the brain came on (year 100),
    counted read-only just before AM1 closes the chains."""
    def __init__(self, w):
        super().__init__(w)
        self.born_from = getattr(w.cfg, "brain_on_year", 100) * WPY

    def __call__(self, world, events):
        tick = world.tick - 1
        for pid, chains in self.chains.items():
            p = world.people.get(pid)
            if p is None or p.birth < self.born_from:
                continue
            for ch in chains:
                if ch[0] + A.CHAIN > tick and len(ch) == 5:
                    continue
                made = len(ch) == 6
                self.s[f"b_m3_{ch[3]}_chains"] += 1
                self.s[f"b_m3_{ch[3]}_made"] += made
                if ch[4]:
                    self.s[f"b_m5_{ch[3]}_chains"] += 1
                    self.s[f"b_m5_{ch[3]}_made"] += made
        return super().__call__(world, events)


class PB2Obs:
    def __init__(self, w):
        self.w = w
        self.s = Counter()
        self.kinds = {}                        # sig -> [first tick, inventor, remade, remade by inventor, recipe]
        self.opp = Counter()                   # intent test 1: adult weeks holding a tracked kind's inputs
        self.rem = Counter()                   # remakes (makes of a tracked kind within its window), by who
        self.gathers = defaultdict(list)       # pid -> [(tick, material)] in the last 8 weeks
        self.actions = Counter()
        self.goals = Counter()                 # goal weeks by "output:direction"
        self.adopt = []                        # [tick, person, output, direction, LP at adoption]
        self.kept = Counter()                  # weeks a finished goal was held, by "output:direction" -> [n, weeks]
        self.held = {}                         # pid -> [tick adopted, output, direction]
        self.born_from = getattr(w.cfg, "brain_on_year", 100) * WPY

    def invented(self, world, p, sig, recipe):
        """AF1's rule: a world-new kind made in play; tracked if first made in years 130-165."""
        t = world.tick
        if WIN[0] <= t and t + REMAKE <= WIN[1]:
            self.kinds[sig] = [t, p.id, 0, 0, recipe]

    def made(self, world, p, sig):
        """A `make` action that made sig (AF1's lineage: the kind's own recipe chosen again within 5 years)."""
        from acl.mind import recipe_materials
        t = world.tick
        kd = self.kinds.get(sig)
        if kd is None or not (kd[0] < t <= kd[0] + REMAKE):
            return
        who = "inv" if p.id == kd[1] else "oth"
        self.rem[who] += 1
        self.s["remakes"] += 1
        kd[2] = 1
        if who == "inv":
            kd[3] = 1
        mats = set(recipe_materials(kd[4]))
        if any(m in mats for _, m in self.gathers.get(p.id, [])):
            self.s["remakes_prepared"] += 1
            self.s[f"remakes_prepared_{who}"] += 1

    def __call__(self, world, events):
        from acl import mind
        tick = world.tick - 1
        for ev in events:
            if ev["k"] == "gather" and ev.get("a"):
                self.gathers[ev["a"]].append((tick, ev.get("kind")))
        for pid in list(self.gathers):
            g = [x for x in self.gathers[pid] if x[0] > tick - A.CHAIN]
            if g:
                self.gathers[pid] = g
            else:
                del self.gathers[pid]
        if not (WIN[0] <= tick < WIN[1]):
            return
        for d in world.week_decisions:
            p = world.people.get(d.agent_id)
            if p is not None and ADULT <= p.age(d.tick) < OLD:
                self.actions[d.chosen[0]] += 1
        living = world.living()
        live = [p for p in living if ADULT <= p.age(world.tick) < OLD]
        # intent test 1: weeks in which an adult holds the inputs of a kind still in its window
        tracked = [(sig, kd) for sig, kd in self.kinds.items() if kd[0] <= tick < kd[0] + REMAKE]
        for sig, kd in tracked:
            for p in live:
                if mind.can_make(p, kd[4]):
                    if p.id == kd[1]:
                        self.opp["inv"] += 1
                        self.opp["inv_knows"] += sig in p.recipes
                    else:
                        self.opp["oth"] += 1
                        self.opp["oth_knows"] += sig in p.recipes
        # goals (arms G and G0)
        for p in living:
            b = getattr(p, "brain", None)
            g = b.goal if b is not None else None
            h = self.held.get(p.id)
            if h is not None and (g is None or [h[1], h[2]] != g[:2]):
                k = f"{h[1]}:{h[2]}"
                self.kept[k + ":n"] += 1
                self.kept[k + ":weeks"] += tick - h[0]
                del self.held[p.id]
                h = None
            if g is not None:
                if h is None:
                    lp = b.lp()
                    self.adopt.append([tick, p.id, g[0], g[1], round(float(lp[g[0]]), 5) if lp is not None else None])
                    self.held[p.id] = [tick, g[0], g[1]]
                if ADULT <= p.age(world.tick) < OLD:
                    self.goals[f"{g[0]}:{g[1]}"] += 1
        for pid in [q for q in self.held if not self.w.people[q].alive]:
            del self.held[pid]
        if tick % WPY == WPY - 1:              # food: a year-end census of adults' edible food
            self.s["census_adults"] += len(live)
            self.s["census_food"] += sum(p.edible() for p in live)
        self.s["adult_weeks_win"] += len(live)
        self.s["living_weeks_win"] += len(living)
        self.s["adult_weeks_born_after"] += sum(1 for p in live if p.birth >= self.born_from)

    def results(self, world):
        k = list(self.kinds.values())
        st = world.brain_stats or getattr(world, "_shadow_stats", None) or {}
        valid = getattr(world, "_brain_valid", None)
        return {"kinds_fields": ["first_tick", "inventor", "remade", "remade_by_inventor"],
                "kinds": [e[:4] for e in k], "n_kinds": len(k), "n_remade": sum(e[2] for e in k),
                "n_remade_by_inventor": sum(e[3] for e in k), "sums": dict(self.s), "opp": dict(self.opp),
                "rem": dict(self.rem), "actions": dict(self.actions), "goals": dict(self.goals),
                "adopt": self.adopt, "kept": dict(self.kept), "fallback": st.get("fallback", 0),
                "steered": st.get("steered", 0), "rq": st.get("rq"),
                "valid_fields": ["se_rhat", "se_q", "n", "r", "r2", "rhat", "rhat2", "q", "q2", "r_rhat", "r_q"],
                "valid": list(valid) if valid is not None else None}


def install(w, am1, pb2):
    A.install(w, am1)
    from acl import actions, knowhow
    o_rem, o_make = knowhow.remember_recipe, actions.HANDLERS["make"]

    def remember_recipe(world, p, sig, recipe, how, source=None, props=None, meant=None):
        new = sig not in world.knowledge
        out = o_rem(world, p, sig, recipe, how, source, props, meant)
        if world is w and new and how == "made" and props is not None:
            pb2.invented(world, p, sig, recipe)
        return out

    def make(world, p, sig, eff):
        if world is not w:
            return o_make(world, p, sig, eff)
        n0 = len(world.events)
        out = o_make(world, p, sig, eff)
        if any(ev["k"] == "make" and ev.get("a") == p.id for ev in world.events[n0:]):
            pb2.made(world, p, sig)
        return out
    knowhow.remember_recipe = remember_recipe
    actions.HANDLERS["make"] = make


def whash(w):
    """The world's hash without the brains (saved worlds hold them; hashing them as JSON is slow), plus a digest of
    every brain and the brain statistics."""
    import hashlib
    if not hasattr(w, "brain_stats"):          # code_v13: no brains
        return base.world_hash(w) + "|-"
    brains = {pid: p.brain for pid, p in w.people.items()}
    stats = w.brain_stats
    for p in w.people.values():
        p.brain = None
    w.brain_stats = None
    try:
        h = base.world_hash(w)
    finally:
        for pid, b in brains.items():
            w.people[pid].brain = b
        w.brain_stats = stats
    dg = hashlib.sha256()
    for pid in sorted(brains):
        if brains[pid] is not None:
            dg.update(pid.encode())
            dg.update(brains[pid].digest().encode())
    dg.update(json.dumps(stats, sort_keys=True).encode())
    return h + "|" + dg.hexdigest()[:24]


def make(seed, arm, on_year=None, code=CODE):
    base.setup(code)
    kw = dict(ARMS[arm])
    if code != CODE:
        for k in ("brain", "brain_shadow", "brain_on_year"):
            kw.pop(k, None)
    elif on_year is not None:
        kw["brain_on_year"] = on_year
    w = base.make_world(seed, kw)
    if code == CODE and arm == "c":
        w._brain_valid = [0.0] * 11
    return w


def hashrun(code, arm, seed, years, observe, on_year):
    A.LATE[0], A.LATE[1] = 0, years * WPY
    WIN[0], WIN[1] = 0, years * WPY
    w = make(seed, arm, on_year, code)
    if observe:
        am1 = M3Split(w)
        pb2 = PB2Obs(w)
        install(w, am1, pb2)
        w.observers.append(am1)
        w.observers.append(pb2)
    for _ in range(years * WPY):
        w.step()
    return whash(w) + ":" + base.rng_state(w)


def reload_check(seed):
    """Arm G with the brain on from year 5: saved at year 10 and reloaded, continues exactly to year 15."""
    w = make(seed, "G", 5)
    from acl.world import World
    for _ in range(10 * WPY):
        w.step()
    b = World.from_dict(json.loads(json.dumps(w.to_dict())))
    for x in (w, b):
        for _ in range(5 * WPY):
            x.step()
    goals = sum(1 for p in w.people.values() if p.brain is not None and p.brain.goal is not None)
    return whash(w) == whash(b) and b.cfg.brain == 2, goals


def unit_check(seed):
    """In a G0 world (brain from year 5, 30 years): (a) with no own week for an action, the value term is q exactly;
    (b) goal outputs never include 'a new kind made' (output 7) or distance (output 6); (c) the brain's end of week
    never touches the world's random generator. Returns (a breaks, b breaks, c calls, checks)."""
    w = make(seed, "G0", 5)
    from acl import brain
    o_steer, o_week = brain.steer, brain.week_end
    bad = [0, 0, 0, 0]

    def steer(world, p, action, target, qv, ctx, cur, hunger):
        out = o_steer(world, p, action, target, qv, ctx, cur, hunger)
        b = brain.brain_of(world, p)
        st = b.own.get(action)
        if st is None or st.n == 0:
            bad[3] += 1
            if out[0] != qv:
                bad[0] += 1
        return out

    rng = w.rng
    calls = [0]
    names = ("random", "randrange", "choice", "shuffle", "uniform", "randint", "gauss", "sample")
    saved = {n: getattr(rng, n) for n in names}

    def counting(n):
        f = saved[n]

        def g(*a, **k):
            calls[0] += 1
            return f(*a, **k)
        return g

    def week_end(world, events):
        if world is not w:
            return o_week(world, events)
        for n in names:
            setattr(rng, n, counting(n))
        try:
            return o_week(world, events)
        finally:
            for n in names:
                setattr(rng, n, saved[n])
            for p in world.living():
                b = p.brain
                if b is not None and b.goal is not None and brain.GOAL_OUT[b.goal[0]] in (6, 7):
                    bad[1] += 1
    brain.steer, brain.week_end = steer, week_end
    for _ in range(30 * WPY):
        w.step()
    bad[2] = calls[0]
    return bad


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    from concurrent.futures import ThreadPoolExecutor
    specs = []
    for seed, years in ((501, 20), (601, 60)):
        specs += [("v13", "c", seed, years, 0, 5), ("pb2", "x0", seed, years, 0, 5), ("pb2", "c", seed, years, 0, 5),
                  ("pb2", "c", seed, years, 1, 5), ("pb2", "P", seed, years, 0, 5), ("pb2", "G", seed, years, 0, 5),
                  ("pb2", "G0", seed, years, 0, 5), ("pb2", "x", seed, years, 0, 5)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
        uc = ex.submit(lambda: subprocess.run(me + ["unit", "701"], capture_output=True, text=True).stdout.split())
        rl, uc = rl.result(), uc.result()
    for seed, years in ((501, 20), (601, 60)):
        g = {(c, a, o): got[(c, a, sd, yr, o, 5)] for c, a, sd, yr, o, _ in specs if sd == seed}
        world_part = lambda s: s.split("|")[0]  # noqa: E731
        same = world_part(g[("v13", "c", 0)]) == world_part(g[("pb2", "x0", 0)])
        shadow_ro = world_part(g[("pb2", "c", 0)]) == world_part(g[("pb2", "x0", 0)]) == \
            world_part(g[("pb2", "c", 1)])
        acts = all(world_part(g[("pb2", a, 0)]) != world_part(g[("pb2", "x0", 0)]) for a in ("P", "G", "G0", "x"))
        t = same and shadow_ro and acts
        ok &= t
        lines.append(f"seed {seed}, {years} years (brain from year 5): code_pb2 with brain 0 = code_v13: "
                     f"{'yes' if same else 'NO'}; the shadow memory (and the observers) leave the world unchanged: "
                     f"{'yes' if shadow_ro else 'NO'}; P, G, G0 and the sham act: {'yes' if acts else 'NO'}")
    t = rl[-2:-1] == ["True"]
    ok &= t
    lines.append(f"arm G, seed 501 (brain from year 5): saved at year 10 with memories and goals, reloaded, continues "
                 f"exactly to year 15: {'yes' if t else 'NO'} (people holding a goal at the end: "
                 f"{rl[-1] if rl else '?'})")
    t = len(uc) >= 4 and uc[-4] == "0" and uc[-3] == "0" and uc[-2] == "0" and int(uc[-1]) > 0
    ok &= t
    lines.append(f"unit checks, arm G0, seed 701 (brain from year 5, 30 years): no own week -> the value term is q "
                 f"exactly (breaks {uc[-4] if uc else '?'} of {uc[-1] if uc else '?'} checks); goals never on 'a new "
                 f"kind' or distance (breaks {uc[-3] if len(uc) > 2 else '?'}); the brain never draws from the world's "
                 f"generator (calls {uc[-2] if len(uc) > 1 else '?'}): {'yes' if t else 'NO'}")
    lines.append(f"code_pb2 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    on_year = None
    if years < YEARS:                          # a smoke run: brain from 40% of the run, counted over its last 30%
        on_year = max(1, int(years * 0.4))
        A.LATE[0], A.LATE[1] = int(years * 0.7) * WPY, years * WPY
        WIN[0], WIN[1] = A.LATE[0], A.LATE[1]
    else:
        A.LATE[0], A.LATE[1] = WIN[0], WIN[1]
    w = make(seed, arm, on_year)
    f0 = base.fingerprint(CODE)
    am1 = M3Split(w)
    pb2 = PB2Obs(w)
    install(w, am1, pb2)
    w.observers.append(am1)
    w.observers.append(pb2)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_pb2", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": whash(w), "am1": am1.results(),
           "pb2": pb2.results(w)}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, kinds {res['pb2']['n_kinds']}, steered {res['pb2']['steered']}",
          flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        code, arm = sys.argv[2], sys.argv[3]
        if arm == "x0":
            arm = "c_off"
            ARMS["c_off"] = {**base.LP, "brain": 0, "brain_shadow": 0}
        print(hashrun(code, arm, int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1", int(sys.argv[7])))
    elif cmd == "reload":
        ok, goals = reload_check(int(sys.argv[2]))
        print(ok, goals)
    elif cmd == "unit":
        print(*unit_check(int(sys.argv[2])))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
