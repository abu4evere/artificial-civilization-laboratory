"""FX1 — fixing three faults in nature v11 (questions.md, frozen as `FX1-frozen`). A fault-fix check in a copy:
`code_fx1` = `code_v11` + `fix_make_choice` (F1) + `fix_overflow` (F2, F3); both 0 = v11. Arms v11 (c), f (both),
f1 (F1 only), f23 (F2 and F3 only), sham (x). ES2's runner supplies the set-up (`../ES2_realized_lookahead/run_es2.py`).
FX1's observer records, for years 100-200:
  census     living and adult weeks, adult makes, made things held by adults (yearly), things on the ground at the end
  kinds      world-new kinds made in play in years 100-195 and whether their own recipe is chosen again by a `make`
             action within 260 weeks (AF1's lineage measure R, unchanged)
  F1         from the code's log at each make choice: decisions of adults with a make option, those where v11's rule
             and the fixed rule offer different recipes, and those whose offer is the person's most recently learned
  F2, F3     from the code's log: an heir's things deleted (v11) or dropped (f); things from a body dropped

  python experiments/FX1_fault_fixes/run_fx1.py zero
  python experiments/FX1_fault_fixes/run_fx1.py one <arm> <seed> <years> <out>
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

base.CODES["fx1"] = HERE / "code_fx1"
CODE = "fx1"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(22401, 22433))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9907, 9906)
ARMS = {"c": {**base.LP, "fix_make_choice": 0, "fix_overflow": 0},
        "f": {**base.LP, "fix_make_choice": 1, "fix_overflow": 1},
        "f1": {**base.LP, "fix_make_choice": 1, "fix_overflow": 0},
        "f23": {**base.LP, "fix_make_choice": 0, "fix_overflow": 1},
        "x": {**base.LP, "fix_make_choice": 0, "fix_overflow": 0, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
ADULT = 16 * WPY
WIN = 5 * WPY
LATE = [100 * WPY, 200 * WPY]


class FX1Obs:
    def __init__(self, w):
        self.w = w
        self.kinds = {}        # sig -> [first tick, inventor, remade, weeks to remake]
        self.s = Counter()
        w.fx1log = []

    def invented(self, world, p, sig):
        t = world.tick
        if LATE[0] <= t and t + WIN <= LATE[1]:
            self.kinds[sig] = [t, p.id, 0, None]

    def made(self, world, p, sig):
        t = world.tick
        if LATE[0] <= t < LATE[1] and p.age(t) >= ADULT:
            self.s["adult_makes"] += 1
        e = self.kinds.get(sig)
        if e is not None and e[0] < t <= e[0] + WIN and not e[2]:
            e[2], e[3] = 1, t - e[0]

    def __call__(self, world, events):
        tick = world.tick - 1
        log, world.fx1log = world.fx1log, []
        if not (LATE[0] <= tick < LATE[1]):
            return
        for e in log:
            if e[0] == "offer":
                q = world.people[e[1]]
                if q.age(tick) >= ADULT:
                    self.s["offers"] += 1
                    self.s["offers_differ"] += int(e[2])
                    self.s["offers_newest"] += int(e[3])
                    self.s["old_rule_newest"] += int(e[6])
                    self.s["new_rule_newest"] += int(e[7])
            else:
                self.s[e[0]] += 1
        living = world.living()
        adults = [p for p in living if p.age(world.tick) >= ADULT]
        self.s["living_weeks"] += len(living)
        self.s["adult_weeks"] += len(adults)
        if tick % WPY == WPY - 1:
            self.s["census_adults"] += len(adults)
            self.s["census_items"] += sum(len(p.items) for p in adults)
        if tick == LATE[1] - 1:
            self.s["ground_end"] = len(world.ground)

    def results(self):
        k = list(self.kinds.values())
        return {"kinds_fields": ["first_tick", "inventor", "remade", "weeks"], "kinds": k, "n_kinds": len(k),
                "n_remade": sum(e[2] for e in k), "sums": dict(self.s)}


def install(w, obs):
    from acl import actions, knowhow
    o_rem, o_make = knowhow.remember_recipe, actions.HANDLERS["make"]

    def remember_recipe(world, p, sig, recipe, how, source=None, props=None, meant=None):
        new = sig not in world.knowledge
        out = o_rem(world, p, sig, recipe, how, source, props, meant)
        if world is w and new and how == "made" and props is not None:
            obs.invented(world, p, sig)
        return out

    def make(world, p, sig, eff):
        if world is not w:
            return o_make(world, p, sig, eff)
        n0 = len(world.events)
        out = o_make(world, p, sig, eff)
        if any(ev["k"] == "make" and ev.get("a") == p.id for ev in world.events[n0:]):
            obs.made(world, p, sig)
        return out
    knowhow.remember_recipe = remember_recipe
    actions.HANDLERS["make"] = make


def hashrun(code, arm, seed, years, observe):
    LATE[0], LATE[1] = 0, years * WPY       # zero checks: every year counted
    base.setup(code)
    kw = dict(ARMS[arm])
    if code == "v11":
        kw.pop("fix_make_choice", None)
        kw.pop("fix_overflow", None)
    w = base.make_world(seed, kw)
    obs = None
    if observe:
        obs = FX1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results()
        extra = ":" + json.dumps({"_kinds": r["n_kinds"], "_remade": r["n_remade"],
                                  **{k: obs.s[k] for k in ("adult_makes", "offers", "offers_differ", "offers_newest",
                                                           "heir_deleted", "heir_dropped", "body_dropped")}},
                                 sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def reload_check(seed):
    base.setup(CODE)
    from acl.world import World
    a = base.make_world(seed, ARMS["f"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for x in (a, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(a) == base.world_hash(b) and b.cfg.fix_make_choice == 1 and b.cfg.fix_overflow == 1


def argmax_check(seed):
    """F1 unit check: in an f world (30 years), at every decision of a teen or adult, the make option the code offers
    (from its log) equals the argmax of u among eligible recipes, computed here independently from the person's state
    with the plan's formula. Returns (all equal, decisions checked, decisions with a make option)."""
    base.setup(CODE)
    from acl import inquiry, mind, thought
    from acl.knowhow import belief
    w = base.make_world(seed, ARMS["f"])
    w.fx1log = []
    start = {}
    bad = n = with_offer = 0
    o_attend, o_steer = thought.attend, thought.steer

    def attend(world, p, *a, **k):
        if world is w:
            start[p.id] = len(w.fx1log)
        return o_attend(world, p, *a, **k)

    def expected(p):
        c, tick, season = w.cfg, w.tick, w.season
        dep_need = sum(d.need(c, tick) for d in w.dependents(p.id))
        hunger = mind.hunger_of(w, p, dep_need)
        fire_here = w.tile(p.loc).fire > 0
        part_of = mind._wanted_parts(p)
        best, best_u = None, 0.05
        for sig, r in p.recipes.items():
            if r["verb"] == "heat" and not fire_here:
                continue
            v = max(p.itemval.get(sig, 0.0), part_of.get(sig, 0.0))
            if r["verb"] == "strike":
                v = max(v, belief(p, f"{r['target']}/{r['tool']}@{season}") or 0.0)
            v = max(v, 0.5 * max(inquiry.pull(p, "m:" + sig), inquiry.pull(p, "f:" + sig)))
            if v <= 0.05 or (mind._holding(p, sig) and v == p.itemval.get(sig, 0.0)) or not mind.can_make(p, r):
                continue
            u = c.worth_weight * v * (0.6 + 0.4 * p.genes["diligence"]) * (1.0 - 0.5 * hunger)
            if u > best_u:
                best, best_u = sig, u
        return best

    def steer(p, options):
        nonlocal bad, n, with_offer
        if w.people.get(p.id) is p and p.stage(w.tick) in ("teen", "adult", "elder") and p.id in start:
            got = [e for e in w.fx1log[start.pop(p.id):] if e[0] == "offer" and e[1] == p.id]
            offered = got[-1][5] if got else None
            n += 1
            with_offer += offered is not None
            bad += offered != expected(p)
        return o_steer(p, options)
    thought.attend, thought.steer = attend, steer
    for _ in range(30 * WPY):
        w.step()
        w.fx1log = []
        start.clear()
    return bad == 0 and with_offer > 0, n, with_offer


def conserve_check(seed, arm):
    """F2/F3 unit check: over 60 years, count made things (in living hands, on the ground, with bodies) just before and
    after every death and every week's body phase for the dead; returns the number of things that vanished there."""
    base.setup(CODE)
    from acl import biology
    w = base.make_world(seed, ARMS[arm])
    lost = 0
    o_die, o_bw = biology.die, biology.bodies_week

    def total():
        return (sum(len(q.items) for q in w.people.values() if q.alive) + len(w.ground)
                + sum(len(b.get("items", ())) for b in w.bodies))

    def die(world, p, cause, killer):
        nonlocal lost
        if world is not w:
            return o_die(world, p, cause, killer)
        t0 = total()
        out = o_die(world, p, cause, killer)
        lost += t0 - total()
        return out

    def bodies_week(world):
        nonlocal lost
        if world is not w:
            return o_bw(world)
        t0 = total()
        out = o_bw(world)
        lost += t0 - total()
        return out
    biology.die, biology.bodies_week = die, bodies_week
    for _ in range(60 * WPY):
        w.step()
    return lost


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
             for code, arm, obs in (("v11", "c", 0), ("fx1", "c", 0), ("fx1", "c", 1), ("fx1", "f", 0), ("fx1", "f", 1),
                                    ("fx1", "f1", 0), ("fx1", "f1", 1), ("fx1", "f23", 0), ("fx1", "f23", 1),
                                    ("fx1", "x", 0))]
    extra = [("argmax", 701), ("conserve", 801, "f"), ("conserve", 801, "c")]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        side = dict(zip(extra, ex.map(lambda e: subprocess.run(me + [*map(str, e)], capture_output=True,
                                                               text=True).stdout.split(), extra)))
    for seed, years in ((501, 20), (601, 60)):
        g = {(c, a, o): got[(c, a, sd, yr, o)] for c, a, sd, yr, o in specs if sd == seed}
        same = hs(g[("v11", "c", 0)]) == hs(g[("fx1", "c", 0)])
        ro = all(hs(g[("fx1", a, 0)]) == hs(g[("fx1", a, 1)]) for a in ("c", "f", "f1", "f23"))
        acts = all(hs(g[("fx1", a, 0)]) != hs(g[("fx1", "c", 0)]) for a in ("f", "f1", "f23", "x"))
        distinct = len({tuple(hs(g[("fx1", a, 0)])) for a in ("f", "f1", "f23")}) == 3
        info = {a: json.loads(g[("fx1", a, 1)].split(":", 2)[2]) for a in ("c", "f", "f1", "f23")}
        t = same and ro and acts and distinct
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_fx1 with both settings 0 = code_v11: {'yes' if same else 'NO'}; "
                     f"observer and log read-only (c, f, f1, f23): {'yes' if ro else 'NO'}; f, f1, f23 and the sham act: "
                     f"{'yes' if acts else 'NO'}; f, f1 and f23 differ: {'yes' if distinct else 'NO'}; {info}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm f, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    out = side[("argmax", 701)]
    t = len(out) >= 3 and out[-3] == "True"
    ok &= t
    lines.append(f"F1 unit check, arm f, seed 701, 30 years: the offered recipe is the argmax of u at every teen or adult "
                 f"decision (checked {out[-2] if out else '?'}, with a make option {out[-1] if out else '?'}): "
                 f"{'yes' if t else 'NO'}")
    lf, lc = side[("conserve", 801, "f")], side[("conserve", 801, "c")]
    t = lf[-1:] == ["0"]
    ok &= t
    lines.append(f"F2/F3 unit check, seed 801, 60 years: made things vanished at deaths and from bodies: arm f "
                 f"{lf[-1] if lf else '?'} ({'yes, none' if t else 'NO'}); arm v11 {lc[-1] if lc else '?'} (the fault, "
                 f"shown)")
    lines.append(f"code_fx1 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = base.make_world(seed, ARMS[arm])
    obs = FX1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_fx1", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
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
    elif cmd == "argmax":
        ok, n, k = argmax_check(int(sys.argv[2]))
        print(ok, n, k)
    elif cmd == "conserve":
        print(conserve_check(int(sys.argv[2]), sys.argv[3]))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: every year counted; never study data
        LATE[0], LATE[1] = 0, int(sys.argv[4]) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
