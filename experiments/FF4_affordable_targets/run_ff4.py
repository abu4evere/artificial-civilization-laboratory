"""FF4 — a whole action dropped because one target is too far: a fault fix in nature v15 (questions.md, frozen as
`FF4-frozen`). A check in a copy: `code_ff4` = `code_v15` + `fix_affordable_target` (0 = v15). Arms v15 (c), f, sham
(x); LP; seeds 24801-24832; 200 years, years 100-200 counted.

The observer is CI1's (the guard sums; `../CI1_children_and_aims/run_ci1.py`), plus, read-only, EG1's split of every
decision of a person aged 6+ (`../EG1_energy_gate`), read from `world.ff4log` (written by code_ff4 only when this
runner sets it) and from `thought.steer` (the options offered):
  a  a food option offered and chosen      b  offered, something else chosen
  c  food feasible (food at the best forage tile, or prey found) but no food option offered (energy)
  d  no food feasible
and the fix at work (weeks where the best target was unaffordable but another was affordable), per action.

  python experiments/FF4_affordable_targets/run_ff4.py zero
  python experiments/FF4_affordable_targets/run_ff4.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "CI1_children_and_aims"))
import run_ci1 as R  # noqa: E402

base = R.base
base.CODES["ff4"] = HERE / "code_ff4"
base.CODES["v15"] = HERE.parent / "NV15_nature_v15" / "code_v15"
CODE = "ff4"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(24801, 24833))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9905, 9906)
ARMS = {"c": {**base.LP, "fix_affordable_target": 0},
        "f": {**base.LP, "fix_affordable_target": 1},
        "x": {**base.LP, "fix_affordable_target": 0, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
BANDS = ((6, 12, "6-11"), (12, 16, "12-15"), (16, 30, "16-29"), (30, 50, "30-49"), (50, 999, "50+"))
COST = {"forage": 25, "hunt": 40, "gather": 25}
MOVE = 4
CUR = []


def band(years):
    for lo, hi, name in BANDS:
        if lo <= years < hi:
            return name
    return "50+"


def predicted(entry, fix, action):
    """Whether the option should be offered, from the log alone."""
    if action == "forage":
        _, _, e, best_d, got_best, off_d, got_off, would = entry
        return off_d is not None and e >= COST["forage"] + MOVE * off_d
    _, _, e, found, best_d, aff_found, aff_d, would = entry
    if not found:
        return False
    return e >= COST[action] + MOVE * best_d or bool(fix and aff_found)


class FF4Obs(R.CI1Obs):
    def __init__(self, w):
        super().__init__(w)
        w.ff4log = []
        self.fix = int(w.cfg.fix_affordable_target)
        self.eg = defaultdict(Counter)                     # "band|sex|starving" -> weeks, a, b, c, d, energy
        self.last4 = defaultdict(lambda: deque(maxlen=4))
        self.fixc = Counter()                              # the fix at work, per action (counted years)
        self.grown = Counter()                             # grown weeks per chosen action (counted years)
        self.chk = Counter()
        self.deaths = Counter()
        CUR[:] = [self]

    def decided(self, world, before, log, offered, chosen):
        years, sex, starving, energy, pid = before
        if years < 6:
            return
        fl = [e for e in log if e[0] == "forage" and e[1] == pid]
        hl = [e for e in log if e[0] == "hunt" and e[1] == pid]
        gl = [e for e in log if e[0] == "gather" and e[1] == pid]
        if len(fl) != 1 or len(hl) > 1 or len(gl) > 1:
            self.chk["missing_entry"] += 1
            return
        self.chk["weeks"] += 1
        for name, lst in (("forage", fl), ("hunt", hl), ("gather", gl)):
            if lst:
                self.chk[f"{name}_mismatch"] += int(predicted(lst[0], self.fix, name) != (name in offered))
        f = fl[0]
        f_feas, f_off, got_off = f[4] > 0, "forage" in offered, f[6]
        found = bool(hl and hl[0][3])
        h_off = "hunt" in offered
        food_offered = (f_off and got_off > 0) or h_off
        act = chosen[0] if chosen else "none"
        if not (f_feas or found):
            part = "d"
        elif not food_offered:
            part = "c"
        elif act in ("forage", "hunt"):
            part = "a"
        else:
            part = "b"
        self.last4[pid].append(part == "c" and starving >= 1)
        tick = world.tick
        if not (R.LATE[0] <= tick < R.LATE[1]):
            return
        s = self.eg[f"{band(years)}|{sex}|{1 if starving >= 1 else 0}"]
        s["weeks"] += 1
        s[part] += 1
        s["energy"] += energy
        for name, lst in (("forage", fl), ("hunt", hl), ("gather", gl)):
            if lst and lst[0][-1]:
                self.fixc[name] += 1
                self.fixc[f"{name}_starving"] += int(starving >= 1)
        if years >= 16:
            self.grown[act] += 1

    def __call__(self, world, events):
        super().__call__(world, events)
        tick = world.tick - 1
        if not (R.LATE[0] <= tick < R.LATE[1]):
            return
        for e in events:
            if e["k"] == "death" and e.get("age", 0) >= 6:
                self.deaths["all_6plus"] += 1
                if e.get("cause") == "starvation":
                    self.deaths["starvation_6plus"] += 1
                    self.deaths["starvation_blocked_last4"] += int(any(self.last4.get(e["a"], ())))
        for p in world.living():
            if p.age(world.tick) >= 6 * WPY:
                self.deaths["living_weeks_6plus"] += 1

    def results(self):
        r = super().results()
        r.pop("kinds", None)
        r.update({"eg": {k: dict(v) for k, v in sorted(self.eg.items())}, "fix": dict(self.fixc),
                  "grown_acts": dict(self.grown), "deaths6": dict(self.deaths), "check": dict(self.chk)})
        return r


def install():
    from acl import mind, thought
    if getattr(mind.decide, "_ff4", False):
        return
    dec0, steer0 = mind.decide, thought.steer
    seen = {}

    def steer(p, options):
        seen[p.id] = {o[1] for o in options}
        return steer0(p, options)

    def decide(world, p):
        o = CUR[0] if CUR else None
        log = getattr(world, "ff4log", None)
        if o is None or log is None:
            return dec0(world, p)
        log.clear()
        before = (p.years(world.tick), p.sex, p.starving, p.energy, p.id)
        seen.pop(p.id, None)
        chosen = dec0(world, p)
        o.decided(world, before, list(log), seen.pop(p.id, set()), chosen)
        log.clear()
        return chosen
    decide._ff4 = True
    mind.decide, thought.steer = decide, steer


def make(seed, arm, code=CODE):
    base.setup(code)
    kw = dict(ARMS[arm])
    if code != CODE:
        kw.pop("fix_affordable_target", None)
    return base.make_world(seed, kw)


def hashrun(code, arm, seed, years, observe):
    R.LATE[0], R.LATE[1] = 0, years * WPY       # zero checks: every year counted
    w = make(seed, arm, code)
    obs = None
    if observe:
        install()
        obs = FF4Obs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results()
        tot = Counter()
        for k, v in r["eg"].items():
            if k.endswith("|1"):
                tot.update(v)
        extra = ":" + json.dumps({"check": r["check"], "fix": r["fix"], "starving": {k: tot[k] for k in "abcd"}},
                                 sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def reload_check(seed):
    w = make(seed, "f")
    from acl.world import World
    for _ in range(10 * WPY):
        w.step()
    b = World.from_dict(json.loads(json.dumps(w.to_dict())))
    for x in (w, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(w) == base.world_hash(b) and b.cfg.fix_affordable_target == 1


def unit_check(seed, years=30):
    """In an f world: for every forage, hunt and gather weighed, (u1) the target offered is the first best-scored
    target among the affordable ones; (u2) when the first best-scored target overall is affordable, it is the one
    offered; (u3) the gate never drops an option the fix offered (the action is among the options whenever a target
    was passed on)."""
    w = make(seed, "f")
    from acl import mind, thought
    w.ff4unit = []
    st = Counter()
    seen = {}
    steer0 = thought.steer

    def steer(p, options):
        seen[p.id] = {o[1] for o in options}
        return steer0(p, options)
    thought.steer = steer
    dec0 = mind.decide

    def decide(world, p):
        world.ff4unit.clear()
        seen.pop(p.id, None)
        out = dec0(world, p)
        offered = seen.pop(p.id, set())
        for action, pid, e, cands, off in world.ff4unit:
            if pid != p.id:
                continue
            st["weighed"] += 1
            best = None
            for t, u, d in cands:
                if best is None or u > best[1]:
                    best = (t, u, d)
            aff = None
            for t, u, d in cands:
                if e >= COST[action] + MOVE * d and (aff is None or u > aff[1]):
                    aff = (t, u, d)
            if best is None:
                st["no_target"] += 1
                continue
            if e >= COST[action] + MOVE * best[2]:
                st["u2_cases"] += 1
                st["u2_bad"] += int(off != best[0])
            else:
                st["fixed_cases"] += 1
                st["u1_bad"] += int(off != (aff[0] if aff else None))
            if off is not None:
                st["u3_cases"] += 1
                st["u3_bad"] += int(action not in offered)
        world.ff4unit.clear()
        return out
    mind.decide = decide
    try:
        for _ in range(years * WPY):
            w.step()
    finally:
        mind.decide, thought.steer = dec0, steer0
    ok = (st["u1_bad"] == 0 and st["u2_bad"] == 0 and st["u3_bad"] == 0 and st["fixed_cases"] > 0
          and st["u2_cases"] > 0)
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
             for code, arm, obs in (("v15", "c", 0), ("ff4", "c", 0), ("ff4", "c", 1), ("ff4", "f", 0),
                                    ("ff4", "f", 1), ("ff4", "x", 0))]
    with ThreadPoolExecutor(2) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        hook = {arm: ex.submit(call, "hashrun", "ff4", arm, 701, 30, 1) for arm in ("c", "f")}
        unit = ex.submit(call, "unit", 701)
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
    for seed, years in ((501, 20), (601, 60)):
        same = hs(got[("v15", "c", seed, years, 0)]) == hs(got[("ff4", "c", seed, years, 0)])
        ro = (hs(got[("ff4", "c", seed, years, 0)]) == hs(got[("ff4", "c", seed, years, 1)])
              and hs(got[("ff4", "f", seed, years, 0)]) == hs(got[("ff4", "f", seed, years, 1)]))
        acts = hs(got[("ff4", "f", seed, years, 0)]) != hs(got[("ff4", "c", seed, years, 0)])
        sham = hs(got[("ff4", "x", seed, years, 0)]) != hs(got[("ff4", "c", seed, years, 0)])
        ok &= same and ro and acts and sham
        info = json.loads(got[("ff4", "f", seed, years, 1)].split(":", 2)[2])
        lines.append(f"seed {seed}, {years} years: code_ff4 with 0 = code_v15: {'yes' if same else 'NO'}; observer and "
                     f"logs read-only (c, f): {'yes' if ro else 'NO'}; the fix acts: {'yes' if acts else 'NO'}; the "
                     f"sham acts: {'yes' if sham else 'NO'}; f: {info}")
    for arm in ("c", "f"):
        info = json.loads(hook[arm].result().split(":", 2)[2])
        ch = info["check"]
        t = (ch.get("weeks", 0) > 0 and ch.get("missing_entry", 0) == 0 and ch.get("forage_mismatch", 0) == 0
             and ch.get("hunt_mismatch", 0) == 0 and ch.get("gather_mismatch", 0) == 0)
        ok &= t
        lines.append(f"seed 701, 30 years, arm {arm}: hook check (forage, hunt and gather offered exactly when the log "
                     f"predicts, every person-week aged 6+): {'yes' if t else 'NO'}; {info}")
    u = json.loads(unit.result())
    ok &= u[0]
    lines.append(f"unit checks, arm f, seed 701, 30 years (the offered target is the first best-scored affordable one; "
                 f"the best is offered when affordable; the gate never drops what the fix offered): "
                 f"{'yes' if u[0] else 'NO'}; {u[1]}")
    t = rl.result()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm f, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_ff4 fingerprint: {call('fp')}")
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
    obs = FF4Obs(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_ff4", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, check {res['check']}, fix {res['fix']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "unit":
        print(json.dumps(unit_check(int(sys.argv[2]))))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: every year counted; never study data
        R.LATE[0], R.LATE[1] = 0, int(sys.argv[4]) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
