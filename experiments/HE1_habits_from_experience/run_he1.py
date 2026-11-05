"""HE1 — habits learn from experience: a law test in a copy (questions.md, frozen as `HE1-frozen`).
The candidate law is an existing setting (`discount` 0), so the worlds run on `code_v13`: c (v13), h (the law), x
(sham). The observers are PB2's, unchanged (`../PB2_brain_steers/run_pb2.py`: AM1's M3/M5/M2, R, actions, food,
kinds), counted over years 100-200, plus HE1's census:
  health      adults' (16-49) mean health at year ends
  deaths      deaths by cause (from the `death` events), all ages; starvation is the hunger guard
  unit        (zero checks only) every habit update with discount 0 equals clamp(q + 0.05 (r - q))

  python experiments/HE1_habits_from_experience/run_he1.py zero
  python experiments/HE1_habits_from_experience/run_he1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "PB2_brain_steers"))
import run_pb2 as R  # noqa: E402

A, base = R.A, R.base
CODE = "v13"
R.CODE = A.CODE = "v13"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(23501, 23533))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9887, 9886)
ARMS = {"c": {**base.LP}, "h": {**base.LP, "discount": 0.0}, "x": {**base.LP, "sham_draw": 1}}
R.ARMS = ARMS
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
R.OUT = OUT
ADULT, OLD = 16 * WPY, 50 * WPY
WIN = [100 * WPY, 200 * WPY]


class HE1Obs:
    def __init__(self, w):
        self.w = w
        self.s = Counter()

    def __call__(self, world, events):
        tick = world.tick - 1
        if not (WIN[0] <= tick < WIN[1]):
            return
        for ev in events:
            if ev["k"] == "death":
                self.s[f"death_{ev.get('cause', '?')}"] += 1
                self.s["deaths"] += 1
        if tick % WPY == WPY - 1:
            adults = [p for p in world.living() if ADULT <= p.age(world.tick) < OLD]
            self.s["census_adults"] += len(adults)
            self.s["census_health"] += sum(p.health for p in adults)


def make(seed, arm, code=CODE):
    base.setup(code)
    w = base.make_world(seed, dict(ARMS[arm]))
    w.brain_stats = None                       # read by PB2's observer; not part of v13 (never saved or read here)
    return w


def observe(w):
    am1, pb2, he1 = R.M3Split(w), R.PB2Obs(w), HE1Obs(w)
    R.install(w, am1, pb2)
    w.observers += [am1, pb2, he1]
    return am1, pb2, he1


def set_window(a, b):
    A.LATE[0], A.LATE[1] = a, b
    R.WIN[0], R.WIN[1] = a, b
    WIN[0], WIN[1] = a, b


def hashrun(arm, seed, years, obs):
    set_window(0, years * WPY)
    w = make(seed, arm)
    if obs:
        observe(w)
    for _ in range(years * WPY):
        w.step()
    return base.world_hash(w) + ":" + base.rng_state(w)


def unit_check(seed, years=20):
    """With discount 0, every habit update equals clamp(q + 0.05 (r - q)); read-only. Returns (wrong, checked)."""
    w = make(seed, "h")
    from acl import biology
    from acl.person import A as ACT, N_ACTIONS
    from acl.util import clamp
    o_learn = biology._learn
    bad, n = [0], [0]

    def _learn(world, p):
        i = p.last_ctx * N_ACTIONS + ACT[p.last_action]
        r = p.reward + 2.0 * (p.mood - p.mood_before)
        want = clamp(p.q[i] + world.cfg.learning_rate * (r - p.q[i]), -1.5, 1.5)
        out = o_learn(world, p)
        n[0] += 1
        bad[0] += p.q[i] != want
        return out
    biology._learn = _learn
    for _ in range(years * WPY):
        w.step()
    return bad[0], n[0]


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    from concurrent.futures import ThreadPoolExecutor
    specs = [(arm, seed, years, o) for seed, years in ((501, 20), (601, 60)) for arm, o in
             (("c", 0), ("c", 1), ("h", 0), ("h", 1), ("x", 0))]
    with ThreadPoolExecutor(4) as ex:
        jobs = [ex.submit(call, "hashrun", *sp) for sp in specs]
        uc = ex.submit(lambda: subprocess.run(me + ["unit", "701"], capture_output=True, text=True).stdout.split())
        got = {sp: j.result() for sp, j in zip(specs, jobs)}
        uc = uc.result()
    for seed, years in ((501, 20), (601, 60)):
        g = {(a, o): got[(a, sd, yr, o)] for a, sd, yr, o in specs if sd == seed}
        ro = g[("c", 0)] == g[("c", 1)] and g[("h", 0)] == g[("h", 1)]
        acts = g[("h", 0)] != g[("c", 0)] and g[("x", 0)] != g[("c", 0)]
        t = ro and acts
        ok &= t
        lines.append(f"seed {seed}, {years} years: the observers leave the world unchanged (c and h): "
                     f"{'yes' if ro else 'NO'}; h and the sham act: {'yes' if acts else 'NO'}")
    t = len(uc) >= 2 and uc[-2] == "0" and int(uc[-1]) > 0
    ok &= t
    lines.append(f"unit check, arm h, seed 701, 20 years: every habit update = clamp(q + 0.05 (r - q)) (wrong "
                 f"{uc[-2] if len(uc) > 1 else '?'} of {uc[-1] if uc else '?'}): {'yes' if t else 'NO'}")
    lines.append(f"code_v13 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    if years < YEARS:                          # a smoke run: counted over its last half
        set_window(years // 2 * WPY, years * WPY)
    else:
        set_window(100 * WPY, 200 * WPY)
    w = make(seed, arm)
    f0 = base.fingerprint(CODE)
    am1, pb2, he1 = observe(w)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_v13", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), "am1": am1.results(),
           "pb2": pb2.results(w), "he1": dict(he1.s)}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, kinds {res['pb2']['n_kinds']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] == "1"))
    elif cmd == "unit":
        print(*unit_check(int(sys.argv[2])))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
