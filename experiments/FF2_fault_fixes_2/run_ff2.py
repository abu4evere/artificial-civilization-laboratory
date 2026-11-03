"""FF2 — fixing three more faults, in nature v12 (questions.md, frozen as `FF2-frozen`). A fault-fix check in a copy:
`code_ff2` = `code_v12` + `fix_hunt_expect` (F8) + `fix_mat_limit` (F4) + `fix_water_holder` (F5); all 0 = v12
(v12_to_ff2.diff). Arms v12 (c), f (all three), f8, f4, f5 (one each), sham (x). ES2's runner supplies the set-up
(`../ES2_realized_lookahead/run_es2.py`). FF2's observer records, for years 100-200 (adults: 16 and over):
  census     living and adult weeks, adult makes, made things held by adults (yearly)
  hunting    from the world's `hunt` events: hunts, successes, meat, adult hunter-weeks
  F8         from the code's log at each hunt option: options offered to adults, and the food per success the option
             expects under v12's rule and under the fixed rule (the same options)
  F4         from the code's log: material units past the limit, by source (hunt, inheritance)
  F5         from the code's log: adults' water-walk weeks, and those in which the best carry thing cannot hold water

  python experiments/FF2_fault_fixes_2/run_ff2.py zero
  python experiments/FF2_fault_fixes_2/run_ff2.py one <arm> <seed> <years> <out>
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

base.CODES["ff2"] = HERE / "code_ff2"
base.CODES["v12"] = HERE.parent / "NV12_nature_v12" / "code_v12"
CODE = "ff2"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(22701, 22733))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9901, 9900)
OFF = {"fix_hunt_expect": 0, "fix_mat_limit": 0, "fix_water_holder": 0}
ARMS = {"c": {**base.LP, **OFF},
        "f": {**base.LP, "fix_hunt_expect": 1, "fix_mat_limit": 1, "fix_water_holder": 1},
        "f8": {**base.LP, **OFF, "fix_hunt_expect": 1},
        "f4": {**base.LP, **OFF, "fix_mat_limit": 1},
        "f5": {**base.LP, **OFF, "fix_water_holder": 1},
        "x": {**base.LP, **OFF, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
ADULT = 16 * WPY
LATE = [100 * WPY, 200 * WPY]
TRIGGER = {"f8": "hunt_differs", "f4": "mat_over_units", "f5": "leaky_walks"}


class FF2Obs:
    def __init__(self, w):
        self.w = w
        self.s = Counter()
        w.ff2log = []

    def __call__(self, world, events):
        tick = world.tick - 1
        log, world.ff2log = world.ff2log, []
        # what each fix's log shows, every year counted (for the zero checks' "acts where triggered")
        for e in log:
            if e[0] == "hunt_opt" and abs(e[4] - e[5]) > 1e-9:
                self.s["hunt_differs"] += 1
            elif e[0] == "mat_over":
                self.s["mat_over_units"] += e[2]
            elif e[0] == "water_walk" and e[3] < e[2] - 1e-12:
                self.s["leaky_walks"] += 1
        if not (LATE[0] <= tick < LATE[1]):
            return
        for e in log:
            if e[0] == "hunt_opt":
                if world.people[e[1]].age(tick) >= ADULT:
                    self.s["hunt_opts"] += 1
                    self.s["opt_food_v12"] += e[4]
                    self.s["opt_food_fixed"] += e[5]
            elif e[0] == "mat_over":
                self.s[f"over_{e[1]}"] += e[2]
            elif e[0] == "water_walk":
                if world.people[e[1]].age(tick) >= ADULT:
                    self.s["walk_weeks"] += 1
                    self.s["walk_leaky"] += int(e[3] < e[2] - 1e-12)
        for ev in events:
            if ev["k"] == "hunt":
                self.s["hunts"] += 1
                self.s["hunt_successes"] += int(bool(ev.get("success")))
                self.s["hunt_meat"] += float(ev.get("meat", 0.0))
                self.s["adult_hunter_weeks"] += sum(1 for i in ev.get("party", ())
                                                    if world.people[i].age(tick) >= ADULT)
            elif ev["k"] == "make" and ev.get("a") in world.people and world.people[ev["a"]].age(tick) >= ADULT:
                self.s["adult_makes"] += 1
        living = world.living()
        adults = [p for p in living if p.age(world.tick) >= ADULT]
        self.s["living_weeks"] += len(living)
        self.s["adult_weeks"] += len(adults)
        if tick % WPY == WPY - 1:
            self.s["census_adults"] += len(adults)
            self.s["census_items"] += sum(len(p.items) for p in adults)

    def results(self):
        return {"sums": dict(self.s)}


def hashrun(code, arm, seed, years, observe):
    LATE[0], LATE[1] = 0, years * WPY       # zero checks: every year counted
    base.setup(code)
    kw = dict(ARMS[arm])
    if code == "v12":
        for k in OFF:
            kw.pop(k, None)
    w = base.make_world(seed, kw)
    obs = None
    if observe:
        obs = FF2Obs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        extra = ":" + json.dumps({k: round(obs.s[k], 6) for k in ("hunt_differs", "mat_over_units", "leaky_walks",
                                                                   "hunts", "adult_makes")},
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
    return (base.world_hash(a) == base.world_hash(b) and b.cfg.fix_hunt_expect == 1 and b.cfg.fix_mat_limit == 1
            and b.cfg.fix_water_holder == 1)


def f8_check(seed):
    """F8 unit check: in an f8 world (30 years), at every hunt option the log's fixed-rule food equals the mean of meat
    x number taken over take_prey's list on that tile, divided by n, both computed here independently from the world
    at the moment of the decision. Returns (all equal, options checked)."""
    base.setup(CODE)
    from acl import thought
    from acl.fauna import PREY, SPECIES
    w = base.make_world(seed, ARMS["f8"])
    w.ff2log = []
    start = {}
    bad = n_opts = 0
    o_attend, o_steer = thought.attend, thought.steer
    c = w.cfg

    def herds_at(x, y):
        return w.herds.get((x % c.width, y % c.height), ())

    def independent(p, t):
        prey = [g for g in herds_at(*t) if g["sp"] in PREY and g["n"] > 0]
        fish = None
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            for g in herds_at(t[0] + dx, t[1] + dy):
                if g["sp"] == "fish" and (fish is None or g["n"] > fish["n"]):
                    fish = g
        if fish is not None and fish["n"] > 0:
            prey.append(fish)
        if not prey:
            return None
        meat = []
        for g in prey:
            m = SPECIES[g["sp"]]["meat"]
            k = 1 if m >= 10 else max(1, round(10.0 / m))
            meat.append(m * min(g["n"], k))
        committed = len(w.hunts.get(t, ()))
        others = len(w.occ.get(t, ())) - (1 if t == p.loc else 0)
        n = 1 + committed + 0.25 * max(0, others - committed)
        return sum(meat) / len(meat) / n

    def attend(world, p, *a, **k):
        if world is w:
            start[p.id] = len(w.ff2log)
        return o_attend(world, p, *a, **k)

    def steer(p, options):
        nonlocal bad, n_opts
        if w.people.get(p.id) is p and p.id in start:
            for e in w.ff2log[start.pop(p.id):]:
                if e[0] == "hunt_opt" and e[1] == p.id:
                    n_opts += 1
                    v = independent(p, tuple(e[2]))
                    bad += v is None or abs(v - e[5]) > 1e-9
        return o_steer(p, options)
    thought.attend, thought.steer = attend, steer
    for _ in range(30 * WPY):
        w.step()
        w.ff2log = []
        start.clear()
    return bad == 0 and n_opts > 0, n_opts


def f4_check(seed):
    """F4 unit check: in an f world (60 years), materials are conserved at every hunt and death (in hands or on the
    pile), and nobody at or below the limit before a hunt or an inheritance is above it after. Returns (conservation
    breaks, limit breaks, successful hunts with spoils checked, deaths checked)."""
    base.setup(CODE)
    from acl import actions, biology, fauna
    w = base.make_world(seed, ARMS["f"])
    lim = w.cfg.material_limit
    breaks = over = hunts = deaths = 0
    got = {}
    o_take, o_res, o_die = fauna.take_prey, actions.resolve_hunts, biology.die

    def take_prey(world, loc):
        out = o_take(world, loc)
        if world is w:
            got[loc] = out[1] + int(round(out[2]))       # hide, and bone in whole units
        return out

    def pile_at(loc):
        return sum(w.tile(loc).pile.values())

    def resolve_hunts(world):
        nonlocal breaks, over, hunts
        if world is not w:
            return o_res(world)
        got.clear()
        parties = {loc: [w.people[i] for i in ids if w.people[i].alive] for loc, ids in w.hunts.items()}
        before = {loc: (sum(h.mat_total() for h in hs), pile_at(loc), {h.id: h.mat_total() for h in hs})
                  for loc, hs in parties.items()}
        out = o_res(world)
        for loc, hs in parties.items():
            if loc not in got:
                continue
            hunts += got[loc] > 0
            m0, p0, each = before[loc]
            breaks += abs((sum(h.mat_total() for h in hs) + pile_at(loc)) - (m0 + p0 + got[loc])) > 1e-6
            over += sum(1 for h in hs if each[h.id] <= lim + 1e-9 and h.mat_total() > lim + 1e-9)
        return out

    def die(world, p, cause, killer):
        nonlocal breaks, over, deaths
        if world is not w:
            return o_die(world, p, cause, killer)
        loc = p.loc
        here = [q for q in w.people.values() if q.alive and q.loc == loc and q is not p]
        each = {q.id: q.mat_total() for q in here}
        t0 = sum(each.values()) + p.mat_total() + pile_at(loc)
        out = o_die(world, p, cause, killer)
        deaths += 1
        breaks += abs(sum(q.mat_total() for q in here) + p.mat_total() + pile_at(loc) - t0) > 1e-6
        over += sum(1 for q in here if each[q.id] <= lim + 1e-9 and q.mat_total() > lim + 1e-9)
        return out
    fauna.take_prey, actions.resolve_hunts, biology.die = take_prey, resolve_hunts, die
    for _ in range(60 * WPY):
        w.step()
    return breaks, over, hunts, deaths


def f5_check(seed):
    """F5 unit check: in an f world (60 years), at every water walk the carry factor used equals the best carry factor
    among things that can hold water (1.0 if none), both computed here independently. Returns (breaks, walks, walks by
    someone with a carry thing that cannot hold water)."""
    base.setup(CODE)
    from acl import weather
    w = base.make_world(seed, ARMS["f"])
    w.ff2log = []
    breaks = walks = leaky = 0
    o_drink = weather.drink

    def drink(world, p):
        nonlocal breaks, walks, leaky
        if world is not w:
            return o_drink(world, p)
        fw = max([1.0 + it["contain"] / 100 for it in p.items if it["contain"] >= 40 and it["tight"] >= 50],
                 default=1.0)
        fc = max([1.0 + it["contain"] / 100 for it in p.items], default=1.0)
        n0 = len(w.ff2log)
        out = o_drink(world, p)
        for e in w.ff2log[n0:]:
            if e[0] == "water_walk" and e[1] == p.id:
                walks += 1
                leaky += fc > fw + 1e-12
                breaks += abs(e[4] - fw) > 1e-12
        return out
    weather.drink = drink
    for _ in range(60 * WPY):
        w.step()
        w.ff2log = []
    return breaks, walks, leaky


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
             for code, arm, obs in (("v12", "c", 0), ("ff2", "c", 0), ("ff2", "c", 1), ("ff2", "f", 0), ("ff2", "f", 1),
                                    ("ff2", "f8", 0), ("ff2", "f8", 1), ("ff2", "f4", 0), ("ff2", "f4", 1),
                                    ("ff2", "f5", 0), ("ff2", "f5", 1), ("ff2", "x", 0))]
    extra = [("f8check", 701), ("f4check", 801), ("f5check", 801)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        side = dict(zip(extra, ex.map(lambda e: subprocess.run(me + [*map(str, e)], capture_output=True,
                                                               text=True).stdout.split(), extra)))
    for seed, years in ((501, 20), (601, 60)):
        g = {(c, a, o): got[(c, a, sd, yr, o)] for c, a, sd, yr, o in specs if sd == seed}
        same = hs(g[("v12", "c", 0)]) == hs(g[("ff2", "c", 0)])
        ro = all(hs(g[("ff2", a, 0)]) == hs(g[("ff2", a, 1)]) for a in ("c", "f", "f8", "f4", "f5"))
        sham = hs(g[("ff2", "x", 0)]) != hs(g[("ff2", "c", 0)])
        info = {a: json.loads(g[("ff2", a, 1)].split(":", 2)[2]) for a in ("c", "f", "f8", "f4", "f5")}
        acts, notes = True, []
        for a, key in TRIGGER.items():
            trig = info[a][key] > 0
            differs = hs(g[("ff2", a, 0)]) != hs(g[("ff2", "c", 0)])
            if trig:
                acts &= differs
                notes.append(f"{a}: triggered, acts: {'yes' if differs else 'NO'}")
            else:
                notes.append(f"{a}: not triggered" + (" (but differs)" if differs else ""))
        trig_f = any(info["f"][k] > 0 for k in TRIGGER.values())
        differs_f = hs(g[("ff2", "f", 0)]) != hs(g[("ff2", "c", 0)])
        if trig_f:
            acts &= differs_f
        notes.append(f"f: {'triggered, acts: ' + ('yes' if differs_f else 'NO') if trig_f else 'not triggered'}")
        t = same and ro and sham and acts
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_ff2 with all three settings 0 = code_v12: "
                     f"{'yes' if same else 'NO'}; observer and log read-only (c, f, f8, f4, f5): {'yes' if ro else 'NO'}; "
                     f"the sham acts: {'yes' if sham else 'NO'}; {'; '.join(notes)}; {info}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm f, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    out = side[("f8check", 701)]
    t = len(out) >= 2 and out[-2] == "True"
    ok &= t
    lines.append(f"F8 unit check, arm f8, seed 701, 30 years: the fixed rule's food per success equals the independent "
                 f"value at every hunt option (checked {out[-1] if out else '?'}): {'yes' if t else 'NO'}")
    out = side[("f4check", 801)]
    t = len(out) >= 4 and out[-4] == "0" and out[-3] == "0"
    ok &= t
    lines.append(f"F4 unit check, arm f, seed 801, 60 years: conservation breaks {out[-4] if out else '?'}, people pushed "
                 f"over the limit {out[-3] if len(out) > 2 else '?'} (hunts with spoils {out[-2] if len(out) > 1 else '?'}, "
                 f"deaths {out[-1] if out else '?'}): {'yes, none' if t else 'NO'}")
    out = side[("f5check", 801)]
    t = len(out) >= 3 and out[-3] == "0"
    ok &= t
    lines.append(f"F5 unit check, arm f, seed 801, 60 years: walks where the factor used is not the best water-holder's "
                 f"{out[-3] if out else '?'} (water walks {out[-2] if len(out) > 1 else '?'}, by someone with a carry "
                 f"thing that cannot hold water {out[-1] if out else '?'}): {'yes, none' if t else 'NO'}")
    lines.append(f"code_ff2 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = base.make_world(seed, ARMS[arm])
    obs = FF2Obs(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_ff2", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, hunts {obs.s['hunts']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "f8check":
        ok, n = f8_check(int(sys.argv[2]))
        print(ok, n)
    elif cmd == "f4check":
        print(*f4_check(int(sys.argv[2])))
    elif cmd == "f5check":
        print(*f5_check(int(sys.argv[2])))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: every year counted; never study data
        LATE[0], LATE[1] = 0, int(sys.argv[4]) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
