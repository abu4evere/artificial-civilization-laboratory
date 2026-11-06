"""CI1 — children may make again (LG), and a held aim that keeps the pieces (IN) (questions.md, frozen as `CI1-frozen`,
amendment 1 before code). A test in a copy: `code_ci1` = `code_v14` + `child_make` + `held_aim` (both 0 = v14;
v14_to_ci1.diff). Arms v14 (c), LG (g), IN (i), LG+IN (b), sham (x). ES2's runner supplies the set-up
(`../ES2_realized_lookahead/run_es2.py`). CI1's observer records, for years 100-200:
  guards     living, child (under 12) and adult weeks; deaths by cause, of all and of children; adults' (16-49) health
             at year ends; food gifts to a child (under 12) of the giver's kin (own children, grandchildren, siblings'
             children)
  kinds      world-new kinds first made in years 100-195: the inventor's age class (child under 12 or grown), whether the
             inventor, alive and knowing the recipe, held the complete input set (can_make) at a week's end within 5
             years, and whether the inventor made it again within 5 years
  IN at work from the code's log: aims formed, endings by cause, puts, hands, makes and play trials kept off
  context    care given, food per adult, adult-weeks at the material limit, child health, makes by adults and by children

  python experiments/CI1_children_and_aims/run_ci1.py zero
  python experiments/CI1_children_and_aims/run_ci1.py one <arm> <seed> <years> <out>
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

base.CODES["ci1"] = HERE / "code_ci1"
base.CODES["v14"] = HERE.parent / "NV14_nature_v14" / "code_v14"
CODE = "ci1"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(24001, 24033))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9901, 9900)
ARMS = {"c": {**base.LP, "child_make": 0, "held_aim": 0},
        "g": {**base.LP, "child_make": 1, "held_aim": 0},
        "i": {**base.LP, "child_make": 0, "held_aim": 1},
        "b": {**base.LP, "child_make": 1, "held_aim": 1},
        "x": {**base.LP, "child_make": 0, "held_aim": 0, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
CHILD, ADULT, OLD = 12 * WPY, 16 * WPY, 50 * WPY
LATE = [100 * WPY, 200 * WPY]
WIN = 5 * WPY


def kin_child(world, giver, q) -> bool:
    """q (a child) is a child of the giver's kin: the giver's own child, grandchild, or a sibling's child."""
    parents = [world.people.get(x) for x in (q.mother, q.father) if x]
    for par in parents:
        if par is None:
            continue
        if par.id == giver.id or par.id in giver.children:
            return True
        if par.id != giver.id and ((par.mother and par.mother == giver.mother) or
                                   (par.father and par.father == giver.father)):
            return True
    return False


class CI1Obs:
    def __init__(self, w):
        self.w = w
        self.s = Counter()
        self.kinds = {}        # sig -> [first tick, inventor id, child (0/1), complete (0/1), remade (0/1)]
        w.ci1log = []

    def __call__(self, world, events):
        from acl.mind import can_make
        tick = world.tick - 1
        log, world.ci1log = world.ci1log, []
        for ev in events:                      # world-new kinds (first made this week), and remaking by the inventor
            if ev["k"] not in ("make", "play") or ev.get("thing") is None:
                continue
            sig = ev["thing"]
            kd = self.kinds.get(sig)
            if kd is not None:
                if ev["k"] == "make" and ev.get("a") == kd[1] and kd[0] < tick <= kd[0] + WIN:
                    kd[4] = 1
                continue
            rec = world.knowledge.get(sig)
            if rec is not None and rec.get("first_tick") == tick and rec.get("first_by") == ev.get("a") \
                    and LATE[0] <= tick < LATE[1] - WIN:
                inv = world.people.get(ev.get("a"))
                self.kinds[sig] = [tick, ev.get("a"), int(inv is not None and inv.age(tick) < CHILD), 0, 0]
        for sig, kd in self.kinds.items():     # a complete input set at the week's end
            if kd[3] or not (kd[0] <= tick <= kd[0] + WIN):
                continue
            p = world.people.get(kd[1])
            if p is not None and p.alive and sig in p.recipes and can_make(p, p.recipes[sig]):
                kd[3] = 1
        if not (LATE[0] <= tick < LATE[1]):
            return
        for e in log:
            if e[0] == "end":
                self.s[f"aim_end_{e[3]}"] += 1
            else:
                self.s[f"aim_{e[0]}"] += 1
        for ev in events:
            k = ev["k"]
            if k == "death":
                child = ev.get("age", 99) < 12
                self.s["deaths"] += 1
                self.s[f"death_{ev.get('cause', '?')}"] += 1
                if child:
                    self.s["child_deaths"] += 1
                    self.s[f"child_death_{ev.get('cause', '?')}"] += 1
            elif k == "give":
                a, t = world.people.get(ev.get("a")), world.people.get(ev.get("b"))
                if a is not None and t is not None and t.age(tick) < CHILD and kin_child(world, a, t):
                    self.s["gifts_kin_children"] += 1
            elif k == "care":
                self.s["care"] += 1
            elif k == "make":
                a = world.people.get(ev.get("a"))
                if a is not None:
                    self.s["makes_child" if a.age(tick) < CHILD else ("makes_adult" if a.age(tick) >= ADULT
                                                                      else "makes_teen")] += 1
        living = world.living()
        lim = world.cfg.material_limit
        for p in living:
            age = p.age(world.tick)
            if age < CHILD:
                self.s["child_weeks"] += 1
            elif age >= ADULT:
                self.s["adult_weeks"] += 1
                self.s["adult_weeks_at_limit"] += int(p.mat_total() >= lim - 1e-9)
        self.s["living_weeks"] += len(living)
        if tick % WPY == WPY - 1:
            adults = [p for p in living if ADULT <= p.age(world.tick) < OLD]
            kids = [p for p in living if p.age(world.tick) < CHILD]
            self.s["census_adults"] += len(adults)
            self.s["census_health"] += sum(p.health for p in adults)
            self.s["census_food"] += sum(p.food for p in adults)
            self.s["census_children"] += len(kids)
            self.s["census_child_health"] += sum(p.health for p in kids)

    def results(self):
        k = list(self.kinds.values())
        return {"sums": dict(self.s), "kind_fields": ["first_tick", "inventor", "child", "complete", "remade"],
                "kinds": k, "n_kinds": len(k), "n_complete": sum(e[3] for e in k), "n_remade": sum(e[4] for e in k)}


def make(seed, arm, code=CODE):
    base.setup(code)
    kw = dict(ARMS[arm])
    if code != CODE:
        kw.pop("child_make", None)
        kw.pop("held_aim", None)
    return base.make_world(seed, kw)


def hashrun(code, arm, seed, years, observe):
    LATE[0], LATE[1] = 0, years * WPY       # zero checks: every year counted
    w = make(seed, arm, code)
    obs = None
    if observe:
        obs = CI1Obs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results()
        extra = ":" + json.dumps({"kinds": r["n_kinds"], "complete": r["n_complete"],
                                  "aims": obs.s["aim_form"], "child_makes": obs.s["makes_child"]},
                                 sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def reload_check(seed):
    w = make(seed, "b")
    from acl.world import World
    for _ in range(10 * WPY):
        w.step()
    aims = sum(1 for p in w.living() if p.aim)
    b = World.from_dict(json.loads(json.dumps(w.to_dict())))
    same_aims = all(b.people[p.id].aim == p.aim for p in w.living())
    for x in (w, b):
        for _ in range(5 * WPY):
            x.step()
    return (base.world_hash(w) == base.world_hash(b) and b.cfg.child_make == 1 and b.cfg.held_aim == 1
            and same_aims and aims > 0), aims


def _independent_keep(p, MATERIALS):
    """The kept pieces, written again here from the plan's words (not the code's function)."""
    def needs(r):
        v = r["verb"]
        if v == "shape":
            return {r["material"]: 1}
        if v == "heat":
            return {r["part"]: 1}
        if v == "fill":
            return {}
        if v == "strike":
            return {r["target"]: 2} if r["target"] == r["tool"] else {r["target"]: 1, r["tool"]: 1}
        d = {}
        for x in list(r["parts"]) + [r["binder"]]:
            d[x] = d.get(x, 0) + 1
        return d

    def held(x):
        return p.mats.get(x, 0.0) if x in MATERIALS else sum(1 for it in p.items if it["sig"] == x)
    r = p.recipes.get(p.aim) if p.aim else None
    if r is None:
        return {}
    want = {}
    for x, n in needs(r).items():
        want[x] = want.get(x, 0) + n
        if x not in MATERIALS and n - held(x) > 0 and x in p.recipes:
            for y, k in needs(p.recipes[x]).items():
                want[y] = want.get(y, 0) + k * (n - held(x))
    return {x: min(n, held(x)) for x, n in want.items() if held(x) > 0}


def unit_check(seed, years=30):
    """In an LG+IN world: (1) no kept piece is set down, handed, or used up in a make or play worth no more than the aim
    while the aim is held (heat crafts, sparks and death are open; a drop at the carry limit is counted apart); (2) every
    aim formed meets the forming rule; (3) every make by a child is of a recipe they knew with can_make True before it;
    (4) the code's kept pieces equal the plan's, written again here."""
    base.setup(CODE)
    from acl import actions, mind, thought
    from acl.matter import MATERIALS
    w = make(seed, "b")
    w.ci1log = []
    st = Counter()
    o_perform, o_attend, o_steer, o_make = actions.perform, thought.attend, thought.steer, actions.HANDLERS["make"]
    o_fire = actions._hold_in_fire
    start = {}
    fired = set()

    def hold_in_fire(world, p, part):            # heating at a fire is open (amendment 1), even when the thing burns
        if world is w:
            fired.add(p.id)
        return o_fire(world, p, part)

    def held(p, x):
        return p.mats.get(x, 0.0) if x in MATERIALS else sum(1 for it in p.items if it["sig"] == x)

    def perform(world, p, option):
        if world is not w:
            return o_perform(world, p, option)
        aim0 = p.aim
        keep0 = _independent_keep(p, MATERIALS) if aim0 else {}
        if aim0:
            st["keep_compared"] += 1
            st["keep_mismatch"] += int(keep0 != mind.kept_pieces(w, p))
        before = {x: held(p, x) for x in keep0}
        n0 = len(w.events)
        fired.discard(p.id)
        out = o_perform(world, p, option)
        act, target = option
        if aim0 and p.alive and p.aim == aim0 and act in ("put", "give", "make", "play") and \
                not (act == "make" and target == aim0):
            evs = w.events[n0:]
            open_use = p.id in fired or any(e["k"] == "fire" and e.get("a") == p.id for e in evs) or \
                any(e["k"] in ("play", "make") and e.get("a") == p.id and "^" in str(e.get("thing", "")) for e in evs)
            dropped = any(e["k"] == "drop" and e.get("a") == p.id for e in evs)
            st["checked"] += 1
            for x, k in keep0.items():
                if held(p, x) < min(before[x], k) - 1e-9:
                    if open_use:
                        st["open_use"] += 1
                    elif dropped:
                        st["drop_at_limit"] += 1
                    else:
                        st["violations"] += 1
                        st[f"violation_{act}"] += 1
                        st[f"violation_{act}_{'material' if x in MATERIALS else 'made'}"] += 1
        return out

    def attend(world, p, *a, **k):
        if world is w:
            start[p.id] = len(w.ci1log)
        return o_attend(world, p, *a, **k)

    def steer(p, options):
        if w.people.get(p.id) is p and p.id in start:
            for e in w.ci1log[start.pop(p.id):]:
                if e[0] == "form" and e[1] == p.id:
                    cands = {s: p.itemval.get(s, 0.0) for s, r in p.recipes.items() if r["verb"] != "fill"
                             and p.itemval.get(s, 0.0) > 0.05 and not mind._holding(p, s) and not mind.can_make(p, r)}
                    st["forms"] += 1
                    st["form_bad"] += int(not cands or e[2] not in cands or cands[e[2]] < max(cands.values()))
        return o_steer(p, options)

    def make_h(world, p, sig, eff):
        if world is w and p.age(w.tick) < CHILD:
            r = p.recipes.get(sig)
            st["child_makes_checked"] += 1
            st["child_make_bad"] += int(r is None or not mind.can_make(p, r))
        return o_make(world, p, sig, eff)
    actions.perform, thought.attend, thought.steer, actions.HANDLERS["make"] = perform, attend, steer, make_h
    actions._hold_in_fire = hold_in_fire
    for _ in range(years * WPY):
        w.step()
        w.ci1log = []
        start.clear()
    ok = (st["violations"] == 0 and st["form_bad"] == 0 and st["child_make_bad"] == 0 and st["keep_mismatch"] == 0
          and st["checked"] > 0 and st["forms"] > 0 and st["child_makes_checked"] > 0)
    return ok, dict(st)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.strip().splitlines()[-1]

    def hs(x):
        return x.split(":")[:2]
    lines, ok = [], True
    from concurrent.futures import ThreadPoolExecutor
    specs = [(code, arm, seed, years, obs) for seed, years in ((501, 20), (601, 60))
             for code, arm, obs in (("v14", "c", 0), ("ci1", "c", 0), ("ci1", "c", 1), ("ci1", "g", 0), ("ci1", "g", 1),
                                    ("ci1", "i", 0), ("ci1", "i", 1), ("ci1", "b", 0), ("ci1", "b", 1),
                                    ("ci1", "x", 0))]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        side = list(ex.map(lambda a: subprocess.run(me + a, capture_output=True, text=True).stdout.strip().splitlines(),
                           [["reload", "501"], ["unit", "701"]]))
    for seed, years in ((501, 20), (601, 60)):
        g = {(c, a, o): got[(c, a, sd, yr, o)] for c, a, sd, yr, o in specs if sd == seed}
        same = hs(g[("v14", "c", 0)]) == hs(g[("ci1", "c", 0)])
        ro = all(hs(g[("ci1", a, 0)]) == hs(g[("ci1", a, 1)]) for a in ("c", "g", "i", "b"))
        acts = all(hs(g[("ci1", a, 0)]) != hs(g[("ci1", "c", 0)]) for a in ("g", "i", "b", "x"))
        distinct = len({tuple(hs(g[("ci1", a, 0)])) for a in ("g", "i", "b")}) == 3
        info = {a: json.loads(g[("ci1", a, 1)].split(":", 2)[2]) for a in ("c", "g", "i", "b")}
        t = same and ro and acts and distinct
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_ci1 with both settings 0 = code_v14: {'yes' if same else 'NO'}; "
                     f"observer read-only (c, g, i, b): {'yes' if ro else 'NO'}; g, i, b and the sham act: "
                     f"{'yes' if acts else 'NO'}; g, i and b differ: {'yes' if distinct else 'NO'}; {info}")
    out = side[0][-1] if side[0] else ""
    t = out.startswith("True")
    ok &= t
    lines.append(f"arm b, seed 501: saved at year 10 (aims held: {out.split()[-1] if out else '?'}) and reloaded, "
                 f"continues exactly to year 15, aims saved: {'yes' if t else 'NO'}")
    out = side[1][-1] if side[1] else ""
    t = out.startswith("True")
    ok &= t
    lines.append(f"unit checks, arm b, seed 701, 30 years (kept pieces never set down, handed or used up by a lower make "
                 f"or play; every aim formed meets the rule; every child make was makeable; the code's kept pieces "
                 f"equal the plan's): {'yes' if t else 'NO'}; {out[5:] if t else out}")
    lines.append(f"code_ci1 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = make(seed, arm)
    obs = CI1Obs(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_ci1", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, kinds {res['n_kinds']}, complete {res['n_complete']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        ok, n = reload_check(int(sys.argv[2]))
        print(ok, n)
    elif cmd == "unit":
        ok, st = unit_check(int(sys.argv[2]))
        print(ok, json.dumps(st, sort_keys=True, separators=(",", ":")))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: every year counted; never study data
        LATE[0], LATE[1] = 0, int(sys.argv[4]) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
