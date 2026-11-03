"""AF1 — open what made things can do (questions.md, frozen as `AF1-frozen`). A nature-change test in a copy:
`code_af1` = `code_v11` + `similar_parts` (S) + `containers_carry` (K); both 0 = v11. Arms v11 (c), S (s), K (k),
S+K (sk), sham (x). ES2's runner supplies the set-up (`../ES2_realized_lookahead/run_es2.py`); AF1's observer records:
  kinds         every world-new kind made in play in years 100-195: inventor; whether its own recipe is chosen again
                by a `make` action within 260 weeks (lineage); recipe availability at 1, 2 and 5 years; functional
                remaking at D = 5, 10, 20 (each make assigned to the nearest late kind only)
  use           makes that used a stand-in input (S); made things and materials held by adults (K)
  census        living and adult weeks, adult makes, extinction

  python experiments/AF1_open_affordances/run_af1.py zero
  python experiments/AF1_open_affordances/run_af1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.CODES["af1"] = HERE / "code_af1"
CODE = "af1"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(22301, 22333))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9909, 9908)
ARMS = {"c": {**base.LP, "similar_parts": 0, "containers_carry": 0},
        "s": {**base.LP, "similar_parts": 1, "containers_carry": 0},
        "k": {**base.LP, "similar_parts": 0, "containers_carry": 1},
        "sk": {**base.LP, "similar_parts": 1, "containers_carry": 1},
        "x": {**base.LP, "similar_parts": 0, "containers_carry": 0, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
ADULT = 16 * WPY
WIN = 5 * WPY
LATE = [100 * WPY, 200 * WPY]
DS = (5, 10, 20)
PROPS = ("edge", "reach", "hard", "contain", "warm", "float", "tight", "plastic", "fuel", "flex")


class AF1Obs:
    def __init__(self, w):
        self.w = w
        self.kinds = {}        # sig -> [tick, inventor, remade, weeks, avail1, avail2, avail5, f5, f10, f20, props]
        self.s = Counter()
        self.mismatch = Counter()

    def invented(self, world, p, sig, props):
        t = world.tick
        if LATE[0] <= t and t + WIN <= LATE[1] and props is not None:
            self.kinds[sig] = [t, p.id, 0, None, None, None, None, 0, 0, 0, {k: props[k] for k in PROPS}]

    def made(self, world, p, recipe_sig, product, used_standin):
        t = world.tick
        late = LATE[0] <= t < LATE[1]
        if late and p.age(t) >= ADULT:
            self.s["adult_makes"] += 1
            self.s["standin_makes"] += used_standin
        e = self.kinds.get(recipe_sig)
        if e is not None and e[0] < t <= e[0] + WIN and not e[2]:
            e[2], e[3] = 1, t - e[0]
        best = None
        for sig, k in self.kinds.items():                  # functional: the nearest late kind, invented earlier
            if not (k[0] < t <= k[0] + WIN):
                continue
            d = max(abs(product[q] - k[10][q]) for q in PROPS)
            if d <= max(DS) and (best is None or (d, k[0]) < (best[0], best[1][0])):
                best = (d, k)
        if best is not None:
            for j, D in enumerate(DS):
                if best[0] <= D:
                    best[1][7 + j] = 1

    def __call__(self, world, events):
        tick = world.tick - 1
        living = None
        for sig, e in self.kinds.items():
            age = tick - e[0]
            for j, wks in enumerate((WPY, 2 * WPY, WIN)):
                if age == wks and e[4 + j] is None:
                    living = living if living is not None else world.living()
                    e[4 + j] = int(any(sig in q.recipes for q in living))
        if LATE[0] <= tick < LATE[1]:
            living = living if living is not None else world.living()
            adults = [p for p in living if p.age(world.tick) >= ADULT]
            self.s["living_weeks"] += len(living)
            self.s["adult_weeks"] += len(adults)
            if tick % WPY == WPY - 1:
                self.s["census_adults"] += len(adults)
                self.s["census_items"] += sum(len(p.items) for p in adults)
                self.s["census_mats"] += sum(p.mat_total() for p in adults)

    def results(self):
        k = [e[:10] for e in self.kinds.values()]
        return {"kinds_fields": ["first_tick", "inventor", "remade", "weeks", "avail1", "avail2", "avail5",
                                 "f5", "f10", "f20"], "kinds": k, "n_kinds": len(k),
                "n_remade": sum(e[2] for e in k), "sums": dict(self.s), "mismatch": dict(self.mismatch)}


def install(w, obs):
    from acl import actions, knowhow, mind
    o_rem, o_make = knowhow.remember_recipe, actions.HANDLERS["make"]

    def remember_recipe(world, p, sig, recipe, how, source=None, props=None, meant=None):
        new = sig not in world.knowledge
        out = o_rem(world, p, sig, recipe, how, source, props, meant)
        if world is w and new and how == "made":
            obs.invented(world, p, sig, props)
        return out

    def make(world, p, sig, eff):
        if world is not w:
            return o_make(world, p, sig, eff)
        recipe = p.recipes.get(sig)
        standin = 0
        if recipe is not None:
            r = mind.resolve_recipe(world, p, recipe)
            standin = int(r is not None and r != recipe)
        n0 = len(world.events)
        out = o_make(world, p, sig, eff)
        for ev in world.events[n0:]:
            if ev["k"] == "make" and ev.get("a") == p.id:
                obs.made(world, p, sig, {q: ev.get(q, 0) for q in PROPS}, standin)
        return out
    knowhow.remember_recipe = remember_recipe
    actions.HANDLERS["make"] = make


def hashrun(code, arm, seed, years, observe):
    LATE[0], LATE[1] = 0, years * WPY       # zero checks: every year counted
    base.setup(code)
    kw = dict(ARMS[arm])
    if code == "v11":
        kw.pop("similar_parts", None)
        kw.pop("containers_carry", None)
    w = base.make_world(seed, kw)
    obs = None
    if observe:
        obs = AF1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results()
        extra = ":" + json.dumps({"_kinds": r["n_kinds"], "_remade": r["n_remade"], "_makes": obs.s["adult_makes"],
                                  "_standin": obs.s["standin_makes"]}, sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def reload_check(seed):
    base.setup(CODE)
    from acl.world import World
    a = base.make_world(seed, ARMS["sk"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for x in (a, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(a) == base.world_hash(b) and b.cfg.similar_parts == 1 and b.cfg.containers_carry == 1


def exact_check(seed):
    """S makes a recipe exactly as v11 whenever the exact inputs are held: across a 30-year S world, at every adult
    decision, for every known recipe the person can make exactly, resolve_recipe returns the recipe unchanged."""
    base.setup(CODE)
    from acl import mind, thought
    w = base.make_world(seed, ARMS["s"])
    bad, n = 0, 0
    o_steer = thought.steer

    def steer(p, options):
        nonlocal bad, n
        if w.people.get(p.id) is p:
            for sig, r in p.recipes.items():
                if mind.can_make(p, r):
                    n += 1
                    bad += mind.resolve_recipe(w, p, r) is not r
        return o_steer(p, options)
    thought.steer = steer
    for _ in range(30 * WPY):
        w.step()
    return bad == 0 and n > 0, n


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
             for code, arm, obs in (("v11", "c", 0), ("af1", "c", 0), ("af1", "c", 1), ("af1", "s", 0), ("af1", "s", 1),
                                    ("af1", "k", 0), ("af1", "k", 1), ("af1", "sk", 0), ("af1", "sk", 1),
                                    ("af1", "x", 0))]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        g = {(c, a, o): got[(c, a, sd, yr, o)] for c, a, sd, yr, o in specs if sd == seed}
        same = hs(g[("v11", "c", 0)]) == hs(g[("af1", "c", 0)])
        ro = all(hs(g[("af1", a, 0)]) == hs(g[("af1", a, 1)]) for a in ("c", "s", "k", "sk"))
        acts = all(hs(g[("af1", a, 0)]) != hs(g[("af1", "c", 0)]) for a in ("s", "k", "sk", "x"))
        distinct = len({tuple(hs(g[("af1", a, 0)])) for a in ("s", "k", "sk")}) == 3
        info = {a: json.loads(g[("af1", a, 1)].split(":", 2)[2]) for a in ("c", "s", "k", "sk")}
        t = same and ro and acts and distinct
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_af1 with both settings 0 = code_v11: {'yes' if same else 'NO'}; "
                     f"observer read-only (c, s, k, sk): {'yes' if ro else 'NO'}; S, K, S+K and the sham act: "
                     f"{'yes' if acts else 'NO'}; S, K and S+K differ: {'yes' if distinct else 'NO'}; {info}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm S+K, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["exact", "701"], capture_output=True, text=True)
    out = r.stdout.split()
    t = len(out) >= 2 and out[-2] == "True"
    ok &= t
    lines.append(f"arm S, seed 701, 30 years: with the exact inputs held, the recipe is made exactly as in v11 "
                 f"(checked {out[-1] if out else '?'} times): {'yes' if t else 'NO'}")
    lines.append(f"code_af1 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = base.make_world(seed, ARMS[arm])
    obs = AF1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_af1", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, kinds {res['n_kinds']}, remade {res['n_remade']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "exact":
        ok, n = exact_check(int(sys.argv[2]))
        print(ok, n)
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: every year counted; never study data
        LATE[0], LATE[1] = 0, int(sys.argv[4]) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
