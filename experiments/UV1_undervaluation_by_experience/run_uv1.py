"""UV1 — does habit under-valuation fade with experience? (questions.md, frozen as `UV1-frozen`). Read-only: ES2's
arms v11 (c) and r replayed on ES2's seeds with `code_es2`, unchanged. ES2's runner and observer
(`../ES2_realized_lookahead/run_es2.py`) are reused as they are; UV1's observer adds, for every habit update:
  k              how many earlier updates the same person made to the same habit (the exact q entry), over the life
  age            in years, at the update
  crisis         the situation was weak or under half a week of food, with company
  death-closed   its G was closed by death (censored)
and sums n, (q - G) and |q - G| by k bin, age bin, crisis, action and death-closed.

  python experiments/UV1_undervaluation_by_experience/run_uv1.py zero
  python experiments/UV1_undervaluation_by_experience/run_uv1.py one <arm> <seed> <years> <out>
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

SEEDS = base.SEEDS                        # ES2's seeds: the worlds replay exactly
SMOKE_SEEDS = base.SMOKE_SEEDS
ARMS = {"c": base.ARMS["c"], "r": base.ARMS["r"]}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
YEARS, WPY = base.YEARS, base.WPY
OUT = HERE / "output"
K_EDGES = (0, 10, 20, 40, 80, 160)
K_BINS = ("0-9", "10-19", "20-39", "40-79", "80-159", "160+")
AGE_EDGES = (1, 6, 12, 16, 30, 45, 60)
AGE_BINS = ("1-5", "6-11", "12-15", "16-29", "30-44", "45-59", "60+")


def bin_of(x, edges, names):
    j = 0
    for i, e in enumerate(edges):
        if x >= e:
            j = i
    return names[j]


class UV1Obs(base.ES2Obs):
    def __init__(self, w):
        super().__init__(w)
        self.k = defaultdict(Counter)                        # person -> q index -> earlier updates
        self.uv = defaultdict(lambda: [0, 0.0, 0.0])         # "kbin|agebin|crisis|action|censored" -> [n, sum (q-G),
        self.people = defaultdict(set)                       #   sum |q-G|]; kbin -> people with a counted update

    def on_learn(self, world, p, i, before, after, r, fut):
        super().on_learn(world, p, i, before, after, r, fut)
        k = self.k[p.id][i]
        self.k[p.id][i] = k + 1
        self.pending[p.id][-1].append((bin_of(k, K_EDGES, K_BINS),
                                       bin_of(p.age(world.tick) // WPY, AGE_EDGES, AGE_BINS), p.id))

    def close(self, e, censored):
        super().close(e[:5], censored)
        key, q, acc, _, late, (kb, ab, pid) = e
        if not late:
            return
        ctx, act = key.split("|", 1)
        ctx = int(ctx)
        crisis = int(ctx // 8 == 0 and (ctx % 8) // 4 == 1)
        c = self.uv[f"{kb}|{ab}|{crisis}|{act}|{censored}"]
        c[0] += 1
        c[1] += q - acc
        c[2] += abs(q - acc)
        self.people[kb].add(pid)

    def results(self):
        return {**super().results(), "uv_fields": ["n", "sum_signed", "sum_abs"],
                "uv_key": "kbin|agebin|crisis|action|censored", "uv": dict(self.uv),
                "people_by_k": {kb: len(v) for kb, v in self.people.items()}}


def hashrun(arm, seed, years, observe):
    """Zero checks only: every update of the run is counted (ES2 counts years 100-200), so the binning check has data."""
    base.LATE = (0, years * WPY)
    base.setup()
    w = base.make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = UV1Obs(w)
        base.install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        n_cal = sum(v[0] for v in obs.cal.values())
        n_uv = sum(v[0] for v in obs.uv.values())
        extra = ":" + json.dumps({**obs.mismatch, "_updates": obs.s["updates"], "_n_cal": n_cal, "_n_uv": n_uv},
                                 sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


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
    specs = [(arm, seed, years, obs) for seed, years in ((501, 20), (601, 60)) for arm in ARMS for obs in (0, 1)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        for arm in ARMS:
            off, on = got[(arm, seed, years, 0)], got[(arm, seed, years, 1)]
            ro = hs(off) == hs(on)
            info = json.loads(on.split(":", 2)[2])
            mism = {k: v for k, v in info.items() if not k.startswith("_")}
            binned = info["_n_uv"] == info["_n_cal"] and info["_n_cal"] > 0
            t = ro and not any(mism.values()) and info.get("_updates", 0) > 0 and binned
            ok &= t
            lines.append(f"seed {seed}, {years} years, arm {arm}: observer read-only: {'yes' if ro else 'NO'}; "
                         f"update-replay mismatches: {mism or 'none'}; habit updates replayed {info['_updates']:.0f}; "
                         f"every counted update binned once ({info['_n_uv']} = {info['_n_cal']}): "
                         f"{'yes' if binned else 'NO'}")
    lines.append(f"code_es2 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup()
    f0 = base.fingerprint()
    w = base.make_world(seed, ARMS[arm])
    obs = UV1Obs(w)
    base.install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_es2", "code_hash": f0, "code_hash_after": base.fingerprint(),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, mismatches {res['mismatch']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] == "1"))
    elif cmd == "fp":
        base.setup()
        print(base.fingerprint())
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
