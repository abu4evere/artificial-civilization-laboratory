"""LH1 — a fairer look-ahead (questions.md, frozen as `LH1-frozen`). `code_lh1` = `code_v13` + `lookahead_rule`
(v13_to_lh1.diff); rule 0 = v13. Arms: c (v13), e (rule 1: the real next choice), m (rule 2: the experienced value of
the next situation), x (sham). The observers are HE1's (PB2's observers plus health and deaths by cause), counted over
years 100-200.

  python experiments/LH1_fair_lookahead/run_lh1.py zero
  python experiments/LH1_fair_lookahead/run_lh1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "HE1_habits_from_experience"))
import run_he1 as H  # noqa: E402

R, A, base = H.R, H.A, H.base
base.CODES["lh1"] = HERE / "code_lh1"
CODE = "lh1"
H.CODE = R.CODE = A.CODE = "lh1"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(23601, 23633))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9885, 9884)
ARMS = {"c": {**base.LP, "lookahead_rule": 0}, "e": {**base.LP, "lookahead_rule": 1},
        "m": {**base.LP, "lookahead_rule": 2}, "x": {**base.LP, "sham_draw": 1}}
H.ARMS = R.ARMS = ARMS
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
H.OUT = R.OUT = OUT


def make(seed, arm, code=CODE):
    base.setup(code)
    kw = dict(ARMS[arm])
    if code != CODE:
        kw.pop("lookahead_rule", None)
    w = base.make_world(seed, kw)
    w.brain_stats = None                       # read by PB2's observer; not part of the world (never saved or read here)
    return w


H.make = make


def hashrun(code, arm, seed, years, obs):
    H.set_window(0, years * WPY)
    w = make(seed, arm, code)
    if obs:
        H.observe(w)
    for _ in range(years * WPY):
        w.step()
    return base.world_hash(w) + ":" + base.rng_state(w)


def reload_check(arm, seed):
    w = make(seed, arm)
    from acl.world import World
    for _ in range(10 * WPY):
        w.step()
    held = sum(1 for p in w.living() if (p.held if arm == "e" else p.vexp) is not None)
    b = World.from_dict(json.loads(json.dumps(w.to_dict())))
    for x in (w, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(w) == base.world_hash(b) and b.cfg.lookahead_rule == w.cfg.lookahead_rule, held


def unit_check(seed, years=15):
    """Rule 2: every habit update uses future = the stored situation value read before this week's r is added.
    Rule 1: every completed update equals ES2's formula. Returns (wrong m, checked m, wrong e, checked e)."""
    import math
    base.setup(CODE)
    from acl import biology
    from acl.person import A as ACT, N_ACTIONS
    from acl.util import clamp
    out = []
    for arm in ("m", "e"):
        w = make(seed, arm)
        bad, n = [0], [0]
        if arm == "m":
            o_learn = biology._learn
            from acl.mind import context_index

            def _learn(world, p, o_learn=o_learn):
                c = world.cfg
                near = world.people_near(p.loc, c.reach, exclude=p.id)
                nxt = context_index(world, p, bool(near))
                i = p.last_ctx * N_ACTIONS + ACT[p.last_action]
                r = p.reward + 2.0 * (p.mood - p.mood_before)
                want = clamp(p.q[i] + c.learning_rate * (r + c.discount * biology.situation_value(p, nxt) - p.q[i]),
                             -1.5, 1.5)
                res = o_learn(world, p)
                n[0] += 1
                bad[0] += p.q[i] != want
                return res
            biology._learn = _learn
        else:
            o_apply = biology.apply_held

            def apply_held(world, p, opts, base_i, o_apply=o_apply):
                c = world.cfg
                i, r = p.held
                if opts:
                    top = max(s for s, _ in opts)
                    wts = [math.exp((s - top) / c.choice_temperature) for s, _ in opts]
                    fut = sum(wi * p.q[base_i + ACT[a]] for wi, (_, a) in zip(wts, opts)) / sum(wts)
                else:
                    fut = p.q[base_i + ACT["rest"]]
                want = clamp(p.q[i] + c.learning_rate * (r + c.discount * fut - p.q[i]), -1.5, 1.5)
                res = o_apply(world, p, opts, base_i)
                n[0] += 1
                bad[0] += p.q[i] != want
                return res
            biology.apply_held = apply_held
        for _ in range(years * WPY):
            w.step()
        out += [bad[0], n[0]]
        if arm == "m":
            biology._learn = o_learn
    return out


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    from concurrent.futures import ThreadPoolExecutor
    specs = []
    for seed, years in ((501, 20), (601, 60)):
        specs += [("v13", "c", seed, years, 0), ("lh1", "c", seed, years, 0), ("lh1", "c", seed, years, 1),
                  ("lh1", "e", seed, years, 0), ("lh1", "e", seed, years, 1), ("lh1", "m", seed, years, 0),
                  ("lh1", "m", seed, years, 1), ("lh1", "x", seed, years, 0)]
    with ThreadPoolExecutor(4) as ex:
        jobs = [ex.submit(call, "hashrun", *sp) for sp in specs]
        rle = ex.submit(lambda: subprocess.run(me + ["reload", "e", "501"], capture_output=True, text=True).stdout.split())
        rlm = ex.submit(lambda: subprocess.run(me + ["reload", "m", "501"], capture_output=True, text=True).stdout.split())
        uc = ex.submit(lambda: subprocess.run(me + ["unit", "701"], capture_output=True, text=True).stdout.split())
        got = {sp: j.result() for sp, j in zip(specs, jobs)}
        rle, rlm, uc = rle.result(), rlm.result(), uc.result()
    for seed, years in ((501, 20), (601, 60)):
        g = {(c, a, o): got[(c, a, sd, yr, o)] for c, a, sd, yr, o in specs if sd == seed}
        same = g[("v13", "c", 0)] == g[("lh1", "c", 0)]
        ro = all(g[("lh1", a, 0)] == g[("lh1", a, 1)] for a in ("c", "e", "m"))
        acts = all(g[("lh1", a, 0)] != g[("lh1", "c", 0)] for a in ("e", "m", "x"))
        t = same and ro and acts
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_lh1 with rule 0 = code_v13: {'yes' if same else 'NO'}; the "
                     f"observers leave the world unchanged (c, e, m): {'yes' if ro else 'NO'}; e, m and the sham act: "
                     f"{'yes' if acts else 'NO'}")
    for arm, rl in (("e", rle), ("m", rlm)):
        t = rl[-2:-1] == ["True"]
        ok &= t
        lines.append(f"arm {arm}, seed 501: saved at year 10 ({'held updates' if arm == 'e' else 'situation tables'} "
                     f"present: {rl[-1] if rl else '?'}), reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    t = len(uc) >= 4 and uc[-4] == "0" and int(uc[-3]) > 0 and uc[-2] == "0" and int(uc[-1]) > 0
    ok &= t
    lines.append(f"unit checks, seed 701, 15 years: rule 2 future = the stored situation value (wrong "
                 f"{uc[-4] if len(uc) > 3 else '?'} of {uc[-3] if len(uc) > 2 else '?'}); rule 1 = ES2's formula (wrong "
                 f"{uc[-2] if len(uc) > 1 else '?'} of {uc[-1] if uc else '?'}): {'yes' if t else 'NO'}")
    lines.append(f"code_lh1 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    if years < YEARS:                          # a smoke run: counted over its last half
        H.set_window(years // 2 * WPY, years * WPY)
    else:
        H.set_window(100 * WPY, 200 * WPY)
    w = make(seed, arm)
    f0 = base.fingerprint(CODE)
    am1, pb2, he1 = H.observe(w)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_lh1", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
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
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(*reload_check(sys.argv[2], int(sys.argv[3])))
    elif cmd == "unit":
        print(*unit_check(int(sys.argv[2])))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
