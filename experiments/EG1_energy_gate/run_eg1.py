"""EG1 — when someone is starving, does the energy rule stand between them and food? (questions.md, frozen as
`EG1-frozen`). Read-only: one arm on `code_eg1` (= code_v15 plus logging lines that write to `world.eg1log`, set here,
never saved, read by nothing in nature), LP, seeds 24701-24732, 200 years, years 100-200 counted.

The observer wraps (never changes) `mind.decide` and `thought.steer`. For every decision of a person aged 6+ it reads,
before the call, their age, sex, `p.starving` and energy; from `eg1log`, what `decide` itself weighed for forage (the
best tile's distance and expected food, the most food at an affordable tile looked at, the food on one's own tile) and
hunt (a prey tile found, its distance); from `steer`, the options actually offered; and the action chosen.

  python experiments/EG1_energy_gate/run_eg1.py zero
  python experiments/EG1_energy_gate/run_eg1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.CODES["v15"] = HERE.parent / "NV15_nature_v15" / "code_v15"
base.CODES["eg1"] = HERE / "code_eg1"
CODE = "eg1"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(24701, 24733))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9903, 9904)
ARMS = {"c": dict(base.LP)}
JOBS = [f"c:{s}" for s in SEEDS]
OUT = HERE / "output"
LATE = [100 * WPY, 200 * WPY]
BANDS = ((6, 12, "6-11"), (12, 16, "12-15"), (16, 30, "16-29"), (30, 50, "30-49"), (50, 999, "50+"))
FORAGE_COST, HUNT_COST, MOVE = 25, 40, 4  # v15 `mind.COST` and `MOVE_COST`, checked against the code in zero
CUR = []                                  # the observer of this process (one world per process)


def band(years):
    for lo, hi, name in BANDS:
        if lo <= years < hi:
            return name
    return "50+"


class EG1Obs:
    def __init__(self, w):
        self.w = w
        w.eg1log = []
        self.s = defaultdict(Counter)            # "band|sex|starving" -> counts over counted person-weeks
        self.instead = Counter()                 # chosen action in blocked starving weeks
        self.last4 = defaultdict(lambda: deque(maxlen=4))   # pid -> blocked-starving flags of their last 4 decisions
        self.run = Counter()                     # pid -> current run of blocked starving weeks
        self.runs = Counter()                    # run length -> runs (closed in the counted years, or open at the end)
        self.deaths = Counter()
        self.chk = Counter()                     # hook check: predicted vs offered
        CUR[:] = [self]

    def decided(self, world, before, log, offered, chosen):
        tick = world.tick
        years, sex, starving, energy, pid = before
        if years < 6:
            return
        fl = [e for e in log if e[0] == "forage" and e[1] == pid]
        hl = [e for e in log if e[0] == "hunt" and e[1] == pid]
        if len(fl) != 1 or len(hl) > 1:
            self.chk["missing_forage_entry"] += 1
            return
        _, _, e_f, f_d, got_best, afford_got, own_got = fl[0]
        f_feas = got_best > 0
        f_aff = e_f >= FORAGE_COST + MOVE * f_d
        found, h_d = (hl[0][3], hl[0][4]) if hl else (False, 0)
        h_aff = found and e_f >= HUNT_COST + MOVE * h_d
        f_off, h_off = "forage" in offered, "hunt" in offered
        self.chk["weeks"] += 1
        self.chk["forage_mismatch"] += int(f_aff != f_off)
        self.chk["hunt_mismatch"] += int(h_aff != h_off)
        self.chk["energy_mismatch"] += int(abs(e_f - energy) > 1e-9)
        feas = f_feas or found
        food_offered = (f_feas and f_off) or h_off
        act = chosen[0] if chosen else "none"
        if not feas:
            part = "d"
        elif not food_offered:
            part = "c"
        elif act in ("forage", "hunt"):
            part = "a"
        else:
            part = "b"
        blocked_starving = part == "c" and starving >= 1
        self.last4[pid].append(blocked_starving)
        counted = LATE[0] <= tick < LATE[1]
        if blocked_starving:
            self.run[pid] += 1
        elif self.run[pid]:
            if counted:
                self.runs[self.run[pid]] += 1
            self.run[pid] = 0
        if not counted:
            return
        key = f"{band(years)}|{sex}|{1 if starving >= 1 else 0}"
        s = self.s[key]
        s["weeks"] += 1
        s[part] += 1
        s["energy"] += energy
        if part == "c":
            s["c_affordable_tile_with_food"] += int(afford_got > 0)
            s["c_own_tile_unaffordable"] += int(energy < FORAGE_COST)
            s["c_forage_blocked"] += int(f_feas and not f_off)
            s["c_hunt_blocked"] += int(found and not h_off)
            if starving >= 1:
                self.instead[act] += 1
        if act == "rest" and years >= 16:
            s["rest"] += 1
            s[f"rest_{part}"] += 1

    def __call__(self, world, events):
        tick = world.tick - 1
        if not LATE[0] <= tick < LATE[1]:
            return
        for e in events:
            if e["k"] == "death" and e.get("age", 0) >= 6:
                pid = e["a"]
                cause = e.get("cause")
                self.deaths[f"{cause}"] += 1
                if cause == "starvation":
                    self.deaths["starvation_blocked_last4"] += int(any(self.last4.get(pid, ())))
                    self.deaths["starvation_decided_last4"] += int(len(self.last4.get(pid, ())) > 0)
                if self.run.get(pid):
                    self.runs[self.run[pid]] += 1
                    self.run[pid] = 0

    def results(self):
        runs = Counter(self.runs)
        for pid, n in self.run.items():            # runs still open at the end
            if n and self.w.people.get(pid) is not None and self.w.people[pid].alive:
                runs[n] += 1
        return {"sums": {k: dict(v) for k, v in sorted(self.s.items())}, "instead": dict(self.instead),
                "runs": {str(k): v for k, v in sorted(runs.items())}, "deaths": dict(self.deaths),
                "check": dict(self.chk)}


def install():
    from acl import mind, thought
    if getattr(mind.decide, "_eg1", False):
        return
    dec0, steer0 = mind.decide, thought.steer
    seen = {}

    def steer(p, options):
        seen[p.id] = {o[1] for o in options}
        return steer0(p, options)

    def decide(world, p):
        o = CUR[0] if CUR else None
        log = getattr(world, "eg1log", None)
        if o is None or log is None:
            return dec0(world, p)
        log.clear()
        before = (p.years(world.tick), p.sex, p.starving, p.energy, p.id)
        seen.pop(p.id, None)
        chosen = dec0(world, p)
        o.decided(world, before, list(log), seen.pop(p.id, set()), chosen)
        log.clear()
        return chosen
    decide._eg1 = True
    mind.decide, thought.steer = decide, steer


def make(seed, arm="c", code=CODE):
    base.setup(code)
    return base.make_world(seed, dict(ARMS[arm]))


def hashrun(code, seed, years, observe):
    LATE[0], LATE[1] = 0, years * WPY       # zero checks: every year counted
    w = make(seed, "c", code)
    obs = None
    if observe:
        install()
        obs = EG1Obs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results()
        tot = Counter()
        for v in r["sums"].values():
            tot.update(v)
        extra = ":" + json.dumps({"check": r["check"], "weeks": tot["weeks"], "c": tot["c"], "d": tot["d"]},
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


def costs():
    from acl import mind
    return [mind.COST["forage"], mind.COST["hunt"], mind.MOVE_COST]


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
    specs = [(code, seed, years, obs) for seed, years in ((501, 20), (601, 60))
             for code, obs in (("v15", 0), ("eg1", 0), ("eg1", 1))]
    with ThreadPoolExecutor(2) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        hook = ex.submit(call, "hashrun", "eg1", 701, 30, 1)
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
    for seed, years in ((501, 20), (601, 60)):
        same = hs(got[("v15", seed, years, 0)]) == hs(got[("eg1", seed, years, 0)])
        ro = hs(got[("v15", seed, years, 0)]) == hs(got[("eg1", seed, years, 1)])
        ok &= same and ro
        lines.append(f"seed {seed}, {years} years: code_eg1 with no log = code_v15 (world and random stream): "
                     f"{'yes' if same else 'NO'}; with the log on = code_v15: {'yes' if ro else 'NO'}")
    info = json.loads(hook.result().split(":", 2)[2])
    ch = info["check"]
    t = (ch.get("weeks", 0) > 0 and ch.get("forage_mismatch", 0) == 0 and ch.get("hunt_mismatch", 0) == 0
         and ch.get("energy_mismatch", 0) == 0 and ch.get("missing_forage_entry", 0) == 0)
    ok &= t
    lines.append(f"seed 701, 30 years: hook check (forage and hunt offered exactly when the log predicts, every "
                 f"person-week aged 6+): {'yes' if t else 'NO'}; {info}")
    t = rl.result()[-1:] == ["True"]
    ok &= t
    lines.append(f"seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    c = json.loads(call("costs"))
    t = c == [FORAGE_COST, HUNT_COST, MOVE]
    ok &= t
    lines.append(f"costs in code_eg1 (forage, hunt, a tile): {c}: match the observer's {'yes' if t else 'NO'}")
    lines.append(f"code_eg1 fingerprint: {call('fp')}")
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
    obs = EG1Obs(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_eg1 (= code_v15 + logging)", "code_hash": f0,
           "code_hash_after": base.fingerprint(CODE), "final_tick": w.tick, "extinct": not w.living(),
           "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, check {res['check']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] == "1"))
    elif cmd == "reload":
        base.setup(CODE)
        print(reload_check(int(sys.argv[2])))
    elif cmd == "costs":
        base.setup(CODE)
        print(json.dumps(costs()))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: every year counted; never study data
        LATE[0], LATE[1] = 0, int(sys.argv[4]) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
