"""PB0 — would knowing what happens next change people's choices? (questions.md, frozen as `PB0-frozen`). Read-only
on live nature v12 (`code_v12`). ES2's runner supplies the set-up (`../ES2_realized_lookahead/run_es2.py`).

At the start of every 5th week in the sampling window (years 100-110 of a 110-year world; the last 10 years of a
shorter one, as in a smoke run), the observer draws one living adult with its own random stream and studies that
week's decision in copies of the world, never touching the real one:
  record run   a copy runs the week unchanged and records the person's full option list (scores after
               thought.steer) and the softmax pick
  options      the top 6 by score plus the pick (every option in the all-options sample, every 4th decision)
  week 1       each option is forced in its own copy of the start of the week (mind.decide runs as usual, then its
               returned option is replaced), with the same random state, so nothing differs before the person's turn
  replays      each option's week-1 state is copied 4 times; replay i reseeds the copy's generator with a seed made
               from (world seed, decision number, i), the same for every option; run to week 4 (to 26 in the long
               sample, every 8th decision)
  outcome      the person's own learning signal, r = reward + 2 x (mood - mood at the week's start), summed over the
               weeks they are alive; its reward and mood parts; food, health and alive at the horizon

  python experiments/PB0_prediction_audit/run_pb0.py zero
  python experiments/PB0_prediction_audit/run_pb0.py one c <seed> <years> <out>
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import random
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.CODES["v12"] = HERE.parent / "NV12_nature_v12" / "code_v12"
CODE = "v12"
WPY, YEARS = base.WPY, 110
SEEDS = tuple(range(22901, 22933))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9899, 9898)
ARMS = {"c": {**base.LP}}
JOBS = [f"c:{s}" for s in SEEDS]
OUT = HERE / "output"
ADULT = 16 * WPY
EVERY, K, REPLAYS = 5, 6, 4
H_MAIN, H_LONG = 4, (13, 26)
ALL_EVERY, LONG_EVERY = 4, 8


def clone(w):
    from acl.world import World
    return World.from_dict(json.loads(json.dumps(w.to_dict())))


def replay_seed(world_seed, dn, i):
    return int(hashlib.sha256(f"pb0:{world_seed}:{dn}:{i}".encode()).hexdigest()[:16], 16)


@contextlib.contextmanager
def hooks(target, pid, force=None, record=None):
    """In world `target` only, at person pid's first decision: record the options and the pick, and/or replace the
    returned option with `force`. mind.decide always runs in full, so its draws and side effects are unchanged."""
    from acl import mind, thought
    o_steer, o_decide = thought.steer, mind.decide
    done = [False]

    def steer(p, options):
        out = o_steer(p, options)
        if record is not None and not done[0] and target.people.get(pid) is p:
            record["options"] = [(float(s), a, t) for s, a, t in out]
        return out

    def decide(world, p):
        out = o_decide(world, p)
        if world is target and p.id == pid and not done[0]:
            done[0] = True
            if record is not None:
                record["picked"] = out
                record["ctx"] = p.last_ctx
            if force is not None:
                out = force
        return out
    thought.steer, mind.decide = steer, decide
    try:
        yield done
    finally:
        thought.steer, mind.decide = o_steer, o_decide


def week_r(w, pid):
    """The person's learning signal for the week just run, split into its parts; None if they are dead."""
    p = w.people.get(pid)
    if p is None or not p.alive:
        return None
    return p.reward, 2.0 * (p.mood - p.mood_before)


def end_state(w, pid):
    p = w.people.get(pid)
    if p is None or not p.alive:
        return [0, 0.0, 0.0]
    return [1, round(p.edible(), 3), round(p.health, 3)]


def aim(t):
    return json.dumps(t, separators=(",", ":"))


class PB0Obs:
    def __init__(self, w, lo, hi):
        self.w, self.lo, self.hi = w, lo, hi
        self.rng = random.Random(w.cfg.seed * 7919 + 11)
        self.decisions = []
        self.n = 0
        self.s = Counter()

    def __call__(self, world, events):
        tick = world.tick                     # the coming week: the world is between steps
        if self.lo <= tick - 1 < self.hi:
            living = world.living()
            self.s["living_weeks"] += len(living)
            self.s["adult_weeks"] += sum(1 for p in living if p.age(tick - 1) >= ADULT)
        if not (self.lo <= tick < self.hi) or (tick - self.lo) % EVERY:
            return
        adults = sorted(p.id for p in world.living() if p.age(tick) >= ADULT)
        if not adults:
            return
        pid = adults[self.rng.randrange(len(adults))]
        dn = self.n
        self.n += 1
        self.decisions.append(study(world, pid, dn, all_options=dn % ALL_EVERY == 0, long=dn % LONG_EVERY == 0))

    def results(self):
        return {"decisions": self.decisions, "sums": dict(self.s), "n_sampled": self.n}


def study(world, pid, dn, all_options=False, long=False):
    start = world.to_dict()
    blob = json.dumps(start)
    from acl.world import World

    def fresh():
        return World.from_dict(json.loads(blob))
    rec = {}
    w0 = fresh()
    with hooks(w0, pid, record=rec):
        w0.step()
    out = {"dn": dn, "tick": world.tick, "pid": pid, "season": world.season}
    if "picked" not in rec or "options" not in rec:
        out["skipped"] = True                  # the person did not decide this week (died before their turn)
        return out
    opts = rec["options"]
    order = sorted(range(len(opts)), key=lambda k: (-opts[k][0], k))
    top = order[0]
    picked = next((k for k in range(len(opts)) if (opts[k][1], aim(opts[k][2])) == (rec["picked"][0],
                                                                                   aim(rec["picked"][1]))), None)
    chosen = list(range(len(opts))) if all_options else sorted(set(order[:K]) | ({picked} if picked is not None else set()))
    horizons = (H_MAIN,) + (H_LONG if long else ())
    hmax = max(horizons)
    res = {}
    for k in chosen:
        _, a, t = opts[k]
        w1 = fresh()
        with hooks(w1, pid, force=(a, t)):
            w1.step()
        r1 = week_r(w1, pid)
        s1 = json.dumps(w1.to_dict())
        reps = []
        for i in range(REPLAYS):
            wi = World.from_dict(json.loads(s1))
            wi.rng.seed(replay_seed(world.cfg.seed, dn, i))
            rew, mood = (r1 if r1 is not None else (0.0, 0.0))
            alive = r1 is not None
            marks = {}
            for week in range(2, hmax + 1):
                if alive:
                    wi.step()
                    x = week_r(wi, pid)
                    if x is None:
                        alive = False
                    else:
                        rew += x[0]
                        mood += x[1]
                if week in horizons:
                    marks[week] = [round(rew, 5), round(mood, 5)] + end_state(wi, pid)
                if not wi.living():
                    alive = False
            reps.append(marks)
        res[k] = {"r1": None if r1 is None else [round(r1[0], 5), round(r1[1], 5)], "replays": reps}
    out.update({"ctx": rec["ctx"], "options": [[round(s, 5), a, aim(t)] for s, a, t in opts], "top": top,
                "picked": picked, "all": all_options, "long": long, "outcomes": res})
    return out


def windows(years):
    hi = years * WPY
    lo = max(0, years - 10) * WPY
    return lo, hi


def hashrun(seed, years, observe):
    base.setup(CODE)
    w = base.make_world(seed, ARMS["c"])
    obs = None
    if observe:
        obs = PB0Obs(w, 10 * WPY, 12 * WPY)   # zero checks: sampling in years 10-12 only
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        extra = ":" + json.dumps({"sampled": obs.n, "skipped": sum(1 for d in obs.decisions if d.get("skipped"))},
                                 sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def copy_check(seed):
    """A copy with nothing forced reproduces the real world's next week; forcing the softmax's own pick reproduces the
    record run. Checked at 6 weeks in years 10-12. Returns (copies equal, forced-pick equal, checks)."""
    base.setup(CODE)
    w = base.make_world(seed, ARMS["c"])
    for _ in range(10 * WPY):
        w.step()
    rng = random.Random(seed)
    eq_copy = eq_force = n = 0
    for _ in range(6):
        for _ in range(rng.randrange(5, 15)):
            w.step()
        adults = sorted(p.id for p in w.living() if p.age(w.tick) >= ADULT)
        pid = adults[rng.randrange(len(adults))]
        c = clone(w)
        rec = {}
        c2 = clone(w)
        with hooks(c2, pid, record=rec):
            c2.step()
        c3 = clone(w)
        with hooks(c3, pid, force=rec.get("picked")):
            c3.step()
        c.step()
        w.step()
        n += 1
        eq_copy += base.world_hash(c) == base.world_hash(w) and base.rng_state(c) == base.rng_state(w)
        eq_force += base.world_hash(c3) == base.world_hash(c2) and base.world_hash(c2) == base.world_hash(w)
    return eq_copy == n, eq_force == n, n


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
    specs = [(seed, years, obs) for seed, years in ((501, 20), (601, 60)) for obs in (0, 1)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        cc = ex.submit(lambda: subprocess.run(me + ["copycheck", "701"], capture_output=True, text=True).stdout.split())
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
        cc, rl = cc.result(), rl.result()
    for seed, years in ((501, 20), (601, 60)):
        same = hs(got[(seed, years, 0)]) == hs(got[(seed, years, 1)])
        info = json.loads(got[(seed, years, 1)].split(":", 2)[2])
        t = same and info["sampled"] > 0
        ok &= t
        lines.append(f"seed {seed}, {years} years: the observer and its copies are read-only (sampling in years 10-12): "
                     f"{'yes' if same else 'NO'}; {info}")
    t = cc[-3:-1] == ["True", "True"]
    ok &= t
    lines.append(f"seed 701: a copy with nothing forced reproduces the real week, and forcing the softmax's own pick "
                 f"reproduces the record run ({cc[-1] if cc else '?'} checks): copies {cc[-3] if len(cc) > 2 else '?'}, "
                 f"forced pick {cc[-2] if len(cc) > 1 else '?'}: {'yes' if t else 'NO'}")
    t = rl[-1:] == ["True"]
    ok &= t
    lines.append(f"seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
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
    lo, hi = windows(years)
    obs = PB0Obs(w, lo, hi)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_v12", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "window": [lo, hi], "world_hash": base.world_hash(w),
           **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, decisions {obs.n}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4] == "1"))
    elif cmd == "copycheck":
        print(*copy_check(int(sys.argv[2])))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
