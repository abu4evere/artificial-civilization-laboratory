"""DF1 — who feeds the children, and what does it cost them? (questions.md, frozen as `DF1-frozen`). Read-only: one arm
on `code_v16`, LP, seeds 25101-25132, 200 years, years 100-200 counted.

The observer wraps (never changes) `biology.body_phase`, collecting the body phase's own ledger (`world.ledger`: need,
food held after feeding, deficit, food fed out), and reads, at the start of each body phase, who each grown person
feeds (`world.dependents`) and whether they are those children's mother, father or someone else. A feeding-caused short
week: the person held at least their own need before feeding (held after feeding + fed out >= need) and ended short
(deficit > 0.05). Gifts of food to one's own children under 12 come from the give events. The energy link: at each
decision of a grown person, whether energy is below 25 (in v16, forage is then offered nowhere: one's own tile costs
25), by what the person's last body phase was (feeding-caused short, short for other reasons, not short).

  python experiments/DF1_dependents_feeding/run_df1.py zero
  python experiments/DF1_dependents_feeding/run_df1.py one <arm> <seed> <years> <out>
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

base.CODES["v16"] = HERE.parent / "NV16_nature_v16" / "code_v16"
CODE = "v16"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(25101, 25133))        # 32 new seeds, used by no study
ARMS = {"c": dict(base.LP)}
JOBS = [f"c:{s}" for s in SEEDS]
OUT = HERE / "output"
LATE = [100 * WPY, 200 * WPY]
GROWN, CHILD = 16 * WPY, 12 * WPY
CUR = []


def band(age_weeks):
    y = age_weeks / WPY
    return "16-29" if y < 30 else ("30-49" if y < 50 else "50+")


class DF1Obs:
    def __init__(self, w):
        self.w = w
        self.s = defaultdict(Counter)      # "sex|band" -> sums over counted grown person-weeks
        self.carers = Counter()            # dependents fed by: mother / father / other (counted body phases)
        self.gifts = Counter()             # food gifts to one's own children under 12, by giver sex
        self.energy = Counter()            # next decision energy < 25, by last week's kind and sex
        self.last = {}                     # pid -> "fcs" / "short" / "ok" (the last body phase)
        self.chk = Counter()
        CUR[:] = [self]

    def body(self, world, ledger, deps):
        tick = world.tick
        counted = LATE[0] <= tick < LATE[1]
        for pid, _adult, need, held_after, deficit, fed_out in ledger:
            p = world.people[pid]
            age = tick - p.birth
            short = deficit > 0.05
            fcs = short and fed_out > 0 and held_after + fed_out >= need - 1e-9
            if age >= GROWN:
                self.last[pid] = "fcs" if fcs else ("short" if short else "ok")
            if not counted or age < GROWN:
                continue
            s = self.s[f"{p.sex}|{band(age)}"]
            s["weeks"] += 1
            s["short"] += int(short)
            s["fcs"] += int(fcs)
            s["fed_out"] += fed_out
            d = deps.get(pid, [])
            if d:
                s["weeks_with_deps"] += 1
                s["deps"] += len(d)
        if counted:
            for pid, d in deps.items():
                for kind in d:
                    self.carers[kind] += 1

    def decided(self, world, p):
        if not (LATE[0] <= world.tick < LATE[1]) or world.tick - p.birth < GROWN or p.id not in self.last:
            return
        k = f"{p.sex}|{self.last[p.id]}"
        self.energy[f"{k}|n"] += 1
        self.energy[f"{k}|low"] += int(p.energy < 25)

    def __call__(self, world, events):
        tick = world.tick - 1
        if not (LATE[0] <= tick < LATE[1]):
            return
        for e in events:
            if e["k"] != "give" or e.get("amount") is None:
                continue
            a, b = world.people.get(e["a"]), world.people.get(e.get("b"))
            if a is None or b is None or tick - b.birth >= CHILD:
                continue
            if a.id in (b.mother, b.father):
                self.gifts[f"{a.sex}|n"] += 1
                self.gifts[f"{a.sex}|amount"] += e["amount"]

    def results(self):
        return {"sums": {k: dict(v) for k, v in sorted(self.s.items())}, "carers": dict(self.carers),
                "gifts": dict(self.gifts), "energy": dict(self.energy), "check": dict(self.chk)}


def install(check=False):
    from acl import biology, mind
    if getattr(biology.body_phase, "_df1", False):
        return
    body0, dec0 = biology.body_phase, mind.decide

    def body(world, *a, **k):
        o = CUR[0] if CUR else None
        if o is None:
            return body0(world, *a, **k)
        deps = {}
        for p in world.living():
            if world.tick - p.birth >= GROWN:
                d = world.dependents(p.id)
                if d:
                    deps[p.id] = ["mother" if c.mother == p.id else ("father" if c.father == p.id else "other")
                                  for c in d]
        before = {}
        if check:                                   # zero check only: dependents' food before the body phase
            for p in world.living():
                for c in world.dependents(p.id):
                    before[c.id] = (p.id, c.food + c.seeds)
        had = hasattr(world, "ledger")
        old = getattr(world, "ledger", None)
        world.ledger = []
        try:
            out = body0(world, *a, **k)
            ledger = world.ledger
        finally:
            if had:
                world.ledger = old
            else:
                del world.ledger
        o.body(world, ledger, deps)
        if check:
            o._check_ledger(world, ledger)
        return out

    def decide(world, p):
        o = CUR[0] if CUR else None
        if o is not None:
            o.decided(world, p)
        return dec0(world, p)
    body._df1 = True
    biology.body_phase, mind.decide = body, decide
    if check:
        _install_feed_check(biology)


def _install_feed_check(biology):
    """Zero check 2: the food fed out (the ledger) equals what the dependents gained in the feeding step. The feeding
    step runs from the start of body_phase (after rot) to the call of `_who_is_inside`; each caregiver's dependents are
    read at `world.dependents` calls inside it."""
    inside0 = biology._who_is_inside
    state = {"in": False, "snap": {}, "gain": Counter()}

    def inside(world, living):
        o = CUR[0] if CUR else None
        if o is not None and state["in"]:
            for cid, (pid, e0) in state["snap"].items():
                c = world.people[cid]
                state["gain"][pid] += (c.food + c.seeds) - e0
            o._fed_gain = dict(state["gain"])
            state["in"] = False
        return inside0(world, living)
    biology._who_is_inside = inside

    from acl import world as wmod
    dep0 = wmod.World.dependents

    def dependents(self, pid):
        out = dep0(self, pid)
        if state["in"]:
            for cid, (ppid, e0) in list(state["snap"].items()):
                c = self.people[cid]
                state["gain"][ppid] += (c.food + c.seeds) - e0
                state["snap"].pop(cid)
            for c in out:
                state["snap"][c.id] = (pid, c.food + c.seeds)
        return out
    wmod.World.dependents = dependents

    spoil0 = biology._wet_and_dry

    def wet_and_dry(world, p):                      # runs inside the rot loop, before feeding; marks the start
        state["in"] = True
        state["snap"] = {}
        state["gain"] = Counter()
        return spoil0(world, p)
    biology._wet_and_dry = wet_and_dry


def _check_ledger(self, world, ledger):
    gain = getattr(self, "_fed_gain", {}) or {}
    for pid, _adult, _need, _held, _deficit, fed_out in ledger:
        g = gain.get(pid, 0.0)
        if fed_out > 0 or g:
            self.chk["feeders"] += 1
            if abs(g - fed_out) > 1e-6:
                self.chk["ledger_mismatch"] += 1
    self._fed_gain = {}


DF1Obs._check_ledger = _check_ledger


def make(seed, arm="c", code=CODE):
    base.setup(code)
    return base.make_world(seed, dict(ARMS[arm]))


def hashrun(code, seed, years, observe, check=False):
    LATE[0], LATE[1] = 0, years * WPY
    w = make(seed, "c", code)
    obs = None
    if observe:
        install(check)
        obs = DF1Obs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results()
        tot = Counter()
        for v in r["sums"].values():
            tot.update(v)
        extra = ":" + json.dumps({"check": r["check"], "weeks": tot["weeks"], "fcs": tot["fcs"], "carers": r["carers"]},
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
    with ThreadPoolExecutor(2) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", CODE, *sp), specs)))
        chk = ex.submit(call, "check", 701, 30)
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
    for seed, years in ((501, 20), (601, 60)):
        ro = hs(got[(seed, years, 0)]) == hs(got[(seed, years, 1)])
        ok &= ro
        lines.append(f"seed {seed}, {years} years: observer read-only (world and random stream): {'yes' if ro else 'NO'}; "
                     f"{got[(seed, years, 1)].split(':', 2)[2]}")
    info = json.loads(chk.result().split(":", 2)[2])
    t = info["check"].get("feeders", 0) > 0 and info["check"].get("ledger_mismatch", 0) == 0
    ok &= t
    lines.append(f"seed 701, 30 years: the ledger's food fed out equals the dependents' gain in the feeding step, every "
                 f"feeder-week (within 1e-6): {'yes' if t else 'NO'}; {info}")
    t = rl.result()[-1:] == ["True"]
    ok &= t
    lines.append(f"seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_v16 fingerprint: {call('fp')}")
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
    obs = DF1Obs(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_v16", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] == "1"))
    elif cmd == "check":
        print(hashrun(CODE, int(sys.argv[2]), int(sys.argv[3]), True, check=True))
    elif cmd == "reload":
        base.setup(CODE)
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
