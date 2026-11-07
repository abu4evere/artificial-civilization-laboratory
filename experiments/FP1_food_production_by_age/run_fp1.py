"""FP1 — food production by age in nature v15, against forager evidence (questions.md, frozen as `FP1-frozen`). Read-only:
one arm on `code_v15`, LP, seeds 24301-24332, 200 years, years 100-200 counted.

The observer keeps a food account for every person-week (food + seeds held, ACL's one food unit). It reads held food
before and after each step that can change it, by wrapping (never changing) these functions:
  actions.perform        the week's action: the actor's change, and the target person's (gifts, theft)
  actions.resolve_hunts  meat each hunter actually received
  biology.die            what the dead carried, and what heirs received
  biology.body_phase     rot (recomputed by the code's own formula from the state at entry), feeding (the HF4 ledger's
                         fed_out, and fed_in from it), and eating (the change across the eating step)
Nested deaths are taken out of the enclosing step, so nothing is counted twice. The zero check: for every person-week,
held food at the end - at the start = the sum of the recorded flows (within 1e-6).

  python experiments/FP1_food_production_by_age/run_fp1.py zero
  python experiments/FP1_food_production_by_age/run_fp1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.CODES["v15"] = HERE.parent / "NV15_nature_v15" / "code_v15"
CODE = "v15"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(24301, 24333))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9901, 9900)
ARMS = {"c": dict(base.LP)}
JOBS = [f"c:{s}" for s in SEEDS]
OUT = HERE / "output"
LATE = [100 * WPY, 200 * WPY]
BANDS = ((0, 3, "0-2"), (3, 8, "3-7"), (8, 12, "8-11"), (12, 16, "12-15"), (16, 30, "16-29"), (30, 40, "30-39"),
         (40, 50, "40-49"), (50, 999, "50+"))
PRODUCTION = ("act:forage", "hunt")
CUR = []                                  # the observer of this process (one world per process)


def band(years):
    for lo, hi, name in BANDS:
        if lo <= years < hi:
            return name
    return "50+"


def edible(p):
    return p.food + p.seeds


class FP1Obs:
    def __init__(self, w):
        self.w = w
        self.start = {p.id: edible(p) for p in w.living()}
        self.flows = defaultdict(Counter)        # pid -> category -> amount (this week)
        self.need = {}                           # pid -> (need, deficit) from the ledger (this week)
        self.nested = None                       # pid -> change made by deaths inside an enclosing step
        self.s = defaultdict(Counter)            # "band|sex" -> sums over counted person-weeks
        self.acts = defaultdict(Counter)         # "band|sex" -> action -> weeks
        self.offer = defaultdict(Counter)        # "band|sex" -> forage/hunt offered, chosen
        self.hunts = Counter()                   # party size -> tried / succeeded
        self.ev = Counter()                      # event-based check: forage got, counted weeks
        self.max_res, self.n_res, self.weeks = 0.0, 0, 0
        CUR[:] = [self]

    def add(self, pid, cat, amount):
        if amount:
            self.flows[pid][cat] += amount

    def __call__(self, world, events):
        tick = world.tick - 1
        counted = LATE[0] <= tick < LATE[1]
        dec = {d.agent_id: d for d in world.week_decisions}
        end = {p.id: edible(p) for p in world.living()}
        for pid in set(self.start) | set(end) | set(self.flows):
            p = world.people[pid]
            d_e = end.get(pid, 0.0) - self.start.get(pid, 0.0)
            fl = self.flows.get(pid, Counter())
            res = d_e - sum(fl.values())
            if abs(res) > 1e-6:
                self.n_res += 1
            self.max_res = max(self.max_res, abs(res))
            if not counted or pid not in self.start:
                continue
            key = f"{band((tick - p.birth) / WPY)}|{p.sex}"
            s = self.s[key]
            s["person_weeks"] += 1
            for cat, v in fl.items():
                s[cat] += v
            s["production"] += sum(fl.get(c, 0.0) for c in PRODUCTION)
            need, deficit = self.need.get(pid, (0.0, 0.0))
            s["need"] += need
            s["unmet"] += need * deficit
            if fl.get("act:forage", 0.0) > 0 or fl.get("hunt", 0.0) > 0:
                s["active_weeks"] += 1
                s["active_production"] += sum(fl.get(c, 0.0) for c in PRODUCTION)
                s["active_need"] += need
            dd = dec.get(pid)
            if dd is not None:
                act = dd.chosen[0] if dd.chosen else "none"
                self.acts[key][act] += 1
                offered = {c[0] for c in dd.candidates}
                for a in ("forage", "hunt"):
                    if a in offered:
                        self.offer[key][f"{a}_offered"] += 1
                    if act == a:
                        self.offer[key][f"{a}_chosen"] += 1
        if counted:
            self.weeks += 1
            for e in events:
                if e["k"] == "forage":
                    self.ev["forage_got_events"] += e.get("got", 0.0)
                    self.ev["forage_n"] += 1
                elif e["k"] == "hunt":
                    n = len(e.get("party") or [1])
                    self.hunts[f"{n}_tried"] += 1
                    self.hunts[f"{n}_succeeded"] += int(bool(e.get("success")))
                    self.ev["hunt_meat_events"] += e.get("meat", 0.0)
        self.start = end
        self.flows = defaultdict(Counter)
        self.need = {}

    def results(self):
        return {"sums": {k: dict(v) for k, v in self.s.items()}, "acts": {k: dict(v) for k, v in self.acts.items()},
                "offer": {k: dict(v) for k, v in self.offer.items()}, "hunts": dict(self.hunts), "ev": dict(self.ev),
                "max_residual": self.max_res, "n_residual": self.n_res, "counted_weeks": self.weeks}


def install():
    """Wrap the four functions (once per process). The wrappers read held food only; they call the originals unchanged."""
    from acl import actions, biology
    if getattr(actions, "_fp1", False):
        return
    actions._fp1 = True
    perform0, hunts0, die0, body0 = actions.perform, actions.resolve_hunts, biology.die, biology.body_phase

    def with_nested(fn):
        o = CUR[0]
        outer, o.nested = o.nested, Counter()
        try:
            fn()
            return o.nested
        finally:
            inner = o.nested
            o.nested = outer
            if outer is not None:
                for k, v in inner.items():
                    outer[k] += v

    def perform(world, p, option, *a, **k):
        if not CUR:
            return perform0(world, p, option, *a, **k)
        o = CUR[0]
        tgt = option[1] if isinstance(option, (tuple, list)) and len(option) > 1 and isinstance(option[1], str) \
            and option[1] in world.people and option[1] != p.id else None
        q = world.people[tgt] if tgt else None
        e_p, e_q = edible(p), (edible(q) if q is not None else 0.0)
        out = []
        nested = with_nested(lambda: out.append(perform0(world, p, option, *a, **k)))
        act = option[0] if isinstance(option, (tuple, list)) else str(option)
        o.add(p.id, f"act:{act}", edible(p) - e_p - nested.get(p.id, 0.0))
        if q is not None:
            o.add(q.id, f"by:{act}", edible(q) - e_q - nested.get(q.id, 0.0))
        return out[0] if out else None

    def resolve_hunts(world, *a, **k):
        if not CUR:
            return hunts0(world, *a, **k)
        o = CUR[0]
        ids = sorted({i for v in world.hunts.values() for i in v})
        before = {i: edible(world.people[i]) for i in ids}
        nested = with_nested(lambda: hunts0(world, *a, **k))
        for i in ids:
            o.add(i, "hunt", edible(world.people[i]) - before[i] - nested.get(i, 0.0))

    def die(world, p, *a, **k):
        if not CUR:
            return die0(world, p, *a, **k)
        o = CUR[0]
        ids = [q.id for q in world.living()]
        if p.id not in ids:
            ids.append(p.id)
        before = {i: edible(world.people[i]) for i in ids}
        r = die0(world, p, *a, **k)
        for i in ids:
            d = edible(world.people[i]) - before[i]
            if d:
                o.add(i, "death:died_with" if i == p.id else "death:inherited", d)
                if o.nested is not None:
                    o.nested[i] += d
        return r

    def body_phase(world, *a, **k):
        if not CUR:
            return body0(world, *a, **k)
        o = CUR[0]
        c = world.cfg
        living = list(world.living())
        e0, spoil = {}, {}
        for p in living:
            e0[p.id] = edible(p)
            rate = c.spoil_rate * (c.smoke_keep if world.tile(p.loc).fire > 0 else 1.0)
            kept = min(p.kept, p.food)
            food_after = (p.food - kept) * (1.0 - rate) + kept * (1.0 - rate * c.kept_keep)
            spoil[p.id] = (p.food - food_after) + p.seeds * c.seed_spoil
        had = hasattr(world, "ledger")
        old = getattr(world, "ledger", None)
        world.ledger = []
        try:
            nested = with_nested(lambda: body0(world, *a, **k))
            ledger = world.ledger
        finally:
            if had:
                world.ledger = old
            else:
                del world.ledger
        for pid, _adult, need, held_before, deficit, fed_out in ledger:
            p = world.people[pid]
            fed_in = held_before - (e0[pid] - spoil[pid]) + fed_out
            e_end = edible(p) if p.alive else 0.0
            eaten = held_before - (e_end - nested.get(pid, 0.0))
            o.add(pid, "rot", -spoil[pid])
            o.add(pid, "fed_in", fed_in)
            o.add(pid, "fed_out", -fed_out)
            o.add(pid, "eaten", -eaten)
            o.need[pid] = (need, deficit)

    actions.perform, actions.resolve_hunts, biology.die, biology.body_phase = perform, resolve_hunts, die, body_phase


def make(seed, arm="c", code=CODE):
    base.setup(code)
    return base.make_world(seed, dict(ARMS[arm]))


def hashrun(code, seed, years, observe):
    LATE[0], LATE[1] = 0, years * WPY       # zero checks: every year counted
    w = make(seed, "c", code)
    obs = None
    if observe:
        install()
        obs = FP1Obs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results()
        extra = ":" + json.dumps({"max_residual": r["max_residual"], "n_residual": r["n_residual"],
                                  "forage_events": round(r["ev"].get("forage_got_events", 0.0), 2),
                                  "forage_n": r["ev"].get("forage_n", 0),
                                  "forage_flows": round(sum(v.get("act:forage", 0.0) for v in r["sums"].values()), 2),
                                  "hunt_flows": round(sum(v.get("hunt", 0.0) for v in r["sums"].values()), 2),
                                  "hunt_events": round(r["ev"].get("hunt_meat_events", 0.0), 2)},
                                 sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def reload_check(seed):
    w = make(seed)
    from acl.world import World
    for _ in range(10 * WPY):
        w.step()
    b = World.from_dict(json.loads(json.dumps(w.to_dict())))
    for x in (w, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(w) == base.world_hash(b)


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
    specs = [(seed, years, obs) for seed, years in ((501, 20), (601, 60)) for obs in (0, 1)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", CODE, *sp), specs)))
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
        cons = ex.submit(call, "hashrun", CODE, 701, 30, 1)
    for seed, years in ((501, 20), (601, 60)):
        ro = hs(got[(seed, years, 0)]) == hs(got[(seed, years, 1)])
        info = json.loads(got[(seed, years, 1)].split(":", 2)[2])
        t = ro and info["n_residual"] == 0 and abs(info["forage_events"] - info["forage_flows"]) <= 0.005 * info["forage_n"] + 0.01
        ok &= t
        lines.append(f"seed {seed}, {years} years: observer read-only (world and random stream): {'yes' if ro else 'NO'}; "
                     f"conservation breaches {info['n_residual']} (largest {info['max_residual']:.2e}); {info}")
    info = json.loads(cons.result().split(":", 2)[2])
    t = info["n_residual"] == 0
    ok &= t
    lines.append(f"seed 701, 30 years: every person-week conserves held food (end - start = recorded flows, within 1e-6): "
                 f"{'yes' if t else 'NO'}; breaches {info['n_residual']}, largest {info['max_residual']:.2e}; {info}")
    t = rl.result()[-1:] == ["True"]
    ok &= t
    lines.append(f"seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_v15 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = make(seed, arm)
    install()
    obs = FP1Obs(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_v15", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, residual breaches {res['n_residual']}", flush=True)


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
