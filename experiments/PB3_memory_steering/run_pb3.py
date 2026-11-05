"""PB3 — memory steering as a candidate law: prediction or myopia? (questions.md, frozen as `PB3-frozen`).
`code_pb3` = `code_pb2` + `brain_lookahead` (pb2_to_pb3.diff); brain 0 = v13; brain_lookahead 0 = code_pb2.
Arms: c (v13), c0 (v13 with discount 0), P (brain 1), Pp (P+: brain 1, brain_lookahead 1), x (sham). The observers are
PB2's, unchanged (`../PB2_brain_steers/run_pb2.py`: AM1's M3/M5/M2 counted over years 130-170, R, actions, food, the
brain's fallbacks), so every measure is defined exactly as in PB2.

  python experiments/PB3_memory_steering/run_pb3.py zero
  python experiments/PB3_memory_steering/run_pb3.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "PB2_brain_steers"))
import run_pb2 as R  # noqa: E402

A, base = R.A, R.base
base.CODES["pb3"] = HERE / "code_pb3"
CODE = "pb3"
R.CODE = A.CODE = "pb3"
WPY, YEARS = base.WPY, 170
SEEDS = tuple(range(23301, 23333))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9891, 9890)
ARMS = {"c": {**base.LP, "brain": 0},
        "c0": {**base.LP, "brain": 0, "discount": 0.0},
        "P": {**base.LP, "brain": 1},
        "Pp": {**base.LP, "brain": 1, "brain_lookahead": 1},
        "x": {**base.LP, "brain": 0, "sham_draw": 1}}
R.ARMS = ARMS
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
R.OUT = OUT
NEW = {"pb2": ("brain_lookahead",), "v13": ("brain", "brain_shadow", "brain_on_year", "brain_lookahead")}


def make(seed, arm, on_year=None, code=CODE):
    base.setup(code)
    kw = dict(ARMS[arm])
    for k in NEW.get(code, ()):
        kw.pop(k, None)
    if code != "v13" and on_year is not None:
        kw["brain_on_year"] = on_year
    return base.make_world(seed, kw)


R.make = make


def hashrun(code, arm, seed, years, observe, on_year):
    A.LATE[0], A.LATE[1] = 0, years * WPY
    R.WIN[0], R.WIN[1] = 0, years * WPY
    w = make(seed, arm, on_year, code)
    if observe:
        am1, pb2 = R.M3Split(w), R.PB2Obs(w)
        R.install(w, am1, pb2)
        w.observers += [am1, pb2]
    for _ in range(years * WPY):
        w.step()
    return R.whash(w) + ":" + base.rng_state(w)


def reload_check(seed):
    """Arm P+ with the brain on from year 5: saved at year 10 and reloaded, continues exactly to year 15."""
    w = make(seed, "Pp", 5)
    from acl.world import World
    for _ in range(10 * WPY):
        w.step()
    b = World.from_dict(json.loads(json.dumps(w.to_dict())))
    for x in (w, b):
        for _ in range(5 * WPY):
            x.step()
    open_weeks = sum(1 for p in w.people.values() if p.brain is not None and p.brain.pend is not None)
    return R.whash(w) == R.whash(b) and b.cfg.brain_lookahead == 1, open_weeks


def unit_check(seed):
    """In a P+ world (brain from year 5, 30 years): every completed two-week return equals r(t) + 0.8 r(t+1) from the
    person's next own week, and each living person's newest own week is still open (not used). Returns
    (wrong returns, wrong open weeks, returns checked)."""
    w = make(seed, "Pp", 5)
    from acl import brain
    log = {}
    o_chain = brain.Brain.chain2

    def chain2(self, act, ctx, r, disc):
        o_chain(self, act, ctx, r, disc)
        log.setdefault(id(self), (self, []))[1].append((act, self.own[act].n - 1, r))
    brain.Brain.chain2 = chain2
    for _ in range(30 * WPY):
        w.step()
    disc = w.cfg.discount
    bad_r, bad_open, n = 0, 0, 0
    living = {id(p.brain) for p in w.living() if p.brain is not None}
    for key, (b, seq) in log.items():
        if key not in living:
            continue
        for (a0, i0, r0), (a1, i1, r1) in zip(seq, seq[1:]):
            n += 1
            if b.r2ok[a0][i0] != 1 or b.r2[a0][i0] != r0 + disc * r1:
                bad_r += 1
        a, i, r = seq[-1]
        if b.r2ok[a][i] != 0 or b.pend != [a, b.pend[1], i, r]:
            bad_open += 1
    return bad_r, bad_open, n


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
        specs += [("v13", "c", seed, years, 0, 5), ("pb3", "c", seed, years, 0, 5), ("pb3", "c", seed, years, 1, 5),
                  ("pb2", "P", seed, years, 0, 5), ("pb3", "P", seed, years, 0, 5), ("pb3", "c0", seed, years, 0, 5),
                  ("pb3", "Pp", seed, years, 0, 5), ("pb3", "x", seed, years, 0, 5)]
    with ThreadPoolExecutor(4) as ex:
        jobs = [ex.submit(call, "hashrun", *sp) for sp in specs]
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
        uc = ex.submit(lambda: subprocess.run(me + ["unit", "701"], capture_output=True, text=True).stdout.split())
        got = {sp: j.result() for sp, j in zip(specs, jobs)}
        rl, uc = rl.result(), uc.result()
    world_part = lambda s: s.split("|")[0]  # noqa: E731
    for seed, years in ((501, 20), (601, 60)):
        g = {(c, a, o): got[(c, a, sd, yr, o, 5)] for c, a, sd, yr, o, _ in specs if sd == seed}
        same = world_part(g[("v13", "c", 0)]) == world_part(g[("pb3", "c", 0)])
        ro = g[("pb3", "c", 0)] == g[("pb3", "c", 1)]
        pb2 = g[("pb2", "P", 0)] == g[("pb3", "P", 0)]
        acts = (world_part(g[("pb3", "c0", 0)]) != world_part(g[("pb3", "c", 0)])
                and world_part(g[("pb3", "P", 0)]) != world_part(g[("pb3", "c", 0)])
                and world_part(g[("pb3", "Pp", 0)]) != world_part(g[("pb3", "P", 0)])
                and world_part(g[("pb3", "x", 0)]) != world_part(g[("pb3", "c", 0)]))
        t = same and ro and pb2 and acts
        ok &= t
        lines.append(f"seed {seed}, {years} years (brain from year 5): code_pb3 with brain 0 = code_v13: "
                     f"{'yes' if same else 'NO'}; the observers leave the world unchanged: {'yes' if ro else 'NO'}; "
                     f"P on code_pb3 (brain_lookahead 0) = P on code_pb2, world and memories: "
                     f"{'yes' if pb2 else 'NO'}; c0, P, P+ and the sham act: {'yes' if acts else 'NO'}")
    t = rl[-2:-1] == ["True"]
    ok &= t
    lines.append(f"arm P+, seed 501 (brain from year 5): saved at year 10 with memories and two-week returns, reloaded, "
                 f"continues exactly to year 15: {'yes' if t else 'NO'} (people with an open week at the end: "
                 f"{rl[-1] if rl else '?'})")
    t = len(uc) >= 3 and uc[-3] == "0" and uc[-2] == "0" and int(uc[-1]) > 0
    ok &= t
    lines.append(f"unit check, arm P+, seed 701 (brain from year 5, 30 years): every two-week return = r(t) + 0.8 r(t+1) "
                 f"from the next own week (wrong {uc[-3] if len(uc) > 2 else '?'} of {uc[-1] if uc else '?'}); the "
                 f"newest own week stays open and unused (wrong {uc[-2] if len(uc) > 1 else '?'}): "
                 f"{'yes' if t else 'NO'}")
    lines.append(f"code_pb3 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    on_year = None
    if years < YEARS:                          # a smoke run: brain from 40% of the run, counted over its last 30%
        on_year = max(1, int(years * 0.4))
        A.LATE[0], A.LATE[1] = int(years * 0.7) * WPY, years * WPY
        R.WIN[0], R.WIN[1] = A.LATE[0], A.LATE[1]
    else:
        A.LATE[0], A.LATE[1] = R.WIN[0], R.WIN[1]
    w = make(seed, arm, on_year)
    f0 = base.fingerprint(CODE)
    am1, pb2 = R.M3Split(w), R.PB2Obs(w)
    R.install(w, am1, pb2)
    w.observers += [am1, pb2]
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_pb3", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": R.whash(w), "am1": am1.results(),
           "pb2": pb2.results(w)}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, kinds {res['pb2']['n_kinds']}, steered {res['pb2']['steered']}",
          flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1",
                      int(sys.argv[7])))
    elif cmd == "reload":
        print(*reload_check(int(sys.argv[2])))
    elif cmd == "unit":
        print(*unit_check(int(sys.argv[2])))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
