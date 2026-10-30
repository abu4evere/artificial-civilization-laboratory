"""CO2 — what makes the other options beat making under nature v9? (questions.md, frozen as `CO2-frozen`). Read-only:
CO1's frozen runner (`../CO1_competing_options/run_co1.py`, unchanged) pointed at `code_v9`, with one addition: the
curiosity pull is split out of each option's per-entry score, and making's own score is split into habit, curiosity
and the rest (Q5).

  python experiments/CO2_choice_v9/run_co2.py zero
  python experiments/CO2_choice_v9/run_co2.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "CO1_competing_options"))
import run_co1 as base  # noqa: E402

CODE = EXP / "NV9_nature_v9" / "code_v9"
OUT = HERE / "output"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(20701, 20733))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9985, 9984)
ARMS = base.ARMS
JOBS = [f"lp:{s}" for s in SEEDS]
V9 = {**base.V7, "ground_items": 1, "curiosity_pull": 1}
T = base.T

base.CODE, base.OUT, base.YEARS, base.SEEDS, base.SMOKE_SEEDS, base.JOBS = CODE, OUT, YEARS, SEEDS, SMOKE_SEEDS, JOBS
base.V7 = V9                               # CO1 passes these settings to every world (explicit = code_v9's v9)


class CO2Obs(base.CO1Obs):
    """CO1's observer, plus the curiosity split (Q5). Reads only."""

    def on_options(self, world, p, before, after):
        self.week.pop(p.id, None)
        super().on_options(world, p, before, after)
        cell = self.week.get(p.id)
        if cell is None:                   # not an offered week for this person (CO1's own filters)
            return
        from acl.mind import hunger_of
        from acl.person import A, N_ACTIONS
        c, tick = world.cfg, world.tick
        mk = [i for i, o in enumerate(after) if o[1] == "make"][0]
        u_m = after[mk][0]
        fam = defaultdict(list)
        for i, o in enumerate(after):
            if i != mk:
                fam[o[1]].append(o[0])
        lw, b = c.learned_weight, p.last_ctx * N_ACTIONS
        hunger = hunger_of(world, p, sum(d.need(c, tick) for d in world.dependents(p.id)))
        cur = 0.3 * p.genes["curiosity"] * (1.0 - hunger) if c.curiosity_pull else 0.0

        def tried(a):
            return p.tried[b + A[a]] if p.tried is not None else 0
        parts = {}
        for a, xs in fam.items():
            L = base.lse(xs)
            parts[a] = (L, lw * p.q[b + A[a]], len(xs), cur / (1 + tried(a)))
        u_other = base.lse([v[0] for v in parts.values()])
        s = {a: math.exp((v[0] - u_other) / T) for a, v in parts.items()}
        ent = -sum(x * math.log(x) for x in s.values() if x > 0)
        h_m, c_m = lw * p.q[b + A["make"]], cur / (1 + tried("make"))
        habit = sum(s[a] * parts[a][1] for a in parts) - h_m
        curio = sum(s[a] * parts[a][3] for a in parts) - c_m
        mult = sum(s[a] * T * math.log(parts[a][2]) for a in parts) + T * ent
        gap = u_other - u_m
        built = gap - habit - curio - mult          # the built-in and thought pull, by the exact identity
        m_other = sum(s[a] * (parts[a][0] - parts[a][1] - T * math.log(parts[a][2]) - parts[a][3]) for a in parts)
        if abs(built - (m_other - (u_m - h_m - c_m))) > 1e-9:
            self.mismatch["q5_identity"] += 1
        if c.curiosity_pull and cur > 0 and c_m <= 0:
            self.mismatch["q5_curiosity"] += 1
        for k, v in (("q5_gap", gap), ("q5_habit", habit), ("q5_curiosity", curio), ("q5_mult", mult),
                     ("q5_built", built), ("h_m", h_m), ("c_m", c_m), ("c_other", sum(s[a] * parts[a][3] for a in parts))):
            cell[k] += v
        cell["q5_n"] += 1


base.CO1Obs = CO2Obs                       # hashrun and the runner below build CO2's observer


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    from concurrent.futures import ThreadPoolExecutor
    specs = [(seed, years, obs) for seed, years in ((501, 20), (601, 60)) for obs in (1, 0)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", "lp", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        a, b_ = got[(seed, years, 1)], got[(seed, years, 0)]
        same = a.split(":")[:2] == b_.split(":")[:2]
        info = json.loads(a.split(":", 2)[2]) if a.count(":") >= 2 else {"?": 1}
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = same and not any(mism.values()) and info.get("_offered", 0) > 0 and info.get("_swapped", 0) > 0
        ok &= t
        lines.append(f"arm lp, seed {seed}, {years} years: identical with and without the observer (state and random "
                     f"numbers): {'yes' if same else 'NO'}; identity, family and Q5 mismatches: {mism or 'none'}; "
                     f"offered weeks {info.get('_offered')}, swapped weeks {info.get('_swapped')}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm lp, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_v9 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup()
    f0 = base.fingerprint()
    w = base.make_world(seed, ARMS[arm])
    obs = CO2Obs(w)
    base.install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v9", "code_hash": f0, "code_hash_after": base.fingerprint(),
           "final_tick": w.tick, "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, mismatches {res['mismatch']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(base.hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] == "1"))
    elif cmd == "reload":
        print(base.reload_check(int(sys.argv[2])))
    elif cmd == "fp":
        base.setup()
        print(base.fingerprint())
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
