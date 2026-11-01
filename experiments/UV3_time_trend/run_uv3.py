"""UV3 — is the shrinking habit gap rising returns or climbing values? (questions.md, frozen as `UV3-frozen`).
Read-only: ES2's arm r replayed on ES2's seeds with `code_es2`, unchanged. UV1's observer (`../UV1_undervaluation_by_
experience/run_uv1.py`, itself ES2's plus k, age and death-closed) is reused as it is; UV3's observer adds:
  prim     for updates with k >= 80 at ages 16-44: n, sum q, sum G by quarter x age bin x situation x action x death-closed
  dec      for all updates: n, sum q, sum G by decade x k bin x age bin x birth decade x death-closed
  newborn  at every birth: the mean of the child's habit values, summed by birth decade
  tools    adults' foraged food with and without the tool in hand (TR1's measure, as in ES2), by quarter

  python experiments/UV3_time_trend/run_uv3.py zero
  python experiments/UV3_time_trend/run_uv3.py one r <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "UV1_undervaluation_by_experience"))
import run_uv1 as uv1  # noqa: E402

base = uv1.base
SEEDS = base.SEEDS                        # ES2's seeds: the worlds replay exactly
SMOKE_SEEDS = base.SMOKE_SEEDS
ARMS = {"r": base.ARMS["r"]}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
YEARS, WPY = base.YEARS, base.WPY
OUT = HERE / "output"
HIGH, PRIME = ("80-159", "160+"), ("16-29", "30-44")


def quarter(tick):
    y = tick // WPY
    return str((y - 100) // 25) if 100 <= y < 200 else "-"


class UV3Obs(uv1.UV1Obs):
    def __init__(self, w):
        super().__init__(w)
        self.prim = defaultdict(lambda: [0, 0.0, 0.0])       # "quarter|agebin|ctx|action|censored" -> [n, sum q, sum G]
        self.dec = defaultdict(lambda: [0, 0.0, 0.0])        # "decade|kbin|agebin|birthdecade|censored" -> [n, q, G]
        self.newborn = defaultdict(lambda: [0, 0.0])         # birth decade -> [births, sum of mean habit value]
        self.tools = defaultdict(lambda: [0.0, 0.0])         # quarter -> [food with tool, food without]

    def on_learn(self, world, p, i, before, after, r, fut):
        super().on_learn(world, p, i, before, after, r, fut)
        self.pending[p.id][-1].append((world.tick, p.birth))

    def close(self, e, censored):
        super().close(e[:6], censored)
        key, q, acc, _, late, (kb, ab, _), (tick, birth) = e
        if not late:
            return
        ctx, act = key.split("|", 1)
        if kb in HIGH and ab in PRIME:
            c = self.prim[f"{quarter(tick)}|{ab}|{ctx}|{act}|{censored}"]
            c[0] += 1
            c[1] += q
            c[2] += acc
        c = self.dec[f"{tick // WPY // 10}|{kb}|{ab}|{birth // WPY // 10}|{censored}"]
        c[0] += 1
        c[1] += q
        c[2] += acc

    def after_forage(self, world, p, got):
        super().after_forage(world, p, got)
        if base.LATE[0] <= world.tick < base.LATE[1] and p.age(world.tick) >= base.ADULT and p.alive:
            t = self.tools[quarter(world.tick)]
            t[0] += got[0]
            t[1] += got[1]

    def __call__(self, world, events):
        super().__call__(world, events)
        for ev in events:
            if ev["k"] == "birth":
                child = world.people.get(ev.get("b"))
                if child is not None and child.q:
                    nb = self.newborn[str(child.birth // WPY // 10)]
                    nb[0] += 1
                    nb[1] += sum(child.q) / len(child.q)

    def results(self):
        return {**super().results(), "prim_fields": ["n", "sum_q", "sum_G"],
                "prim_key": "quarter|agebin|ctx|action|censored", "prim": dict(self.prim),
                "dec_key": "decade|kbin|agebin|birthdecade|censored", "dec": dict(self.dec),
                "newborn_fields": ["births", "sum_mean_q"], "newborn": dict(self.newborn),
                "tools_fields": ["food_with", "food_without"], "tools": dict(self.tools)}


def hashrun(arm, seed, years, observe):
    """Zero checks only: every update of the run is counted (ES2 counts years 100-200), so the table check has data."""
    base.LATE = (0, years * WPY)
    base.setup()
    w = base.make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = UV3Obs(w)
        base.install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        n_cal = sum(v[0] for v in obs.cal.values())
        n_dec = sum(v[0] for v in obs.dec.values())
        births = sum(v[0] for v in obs.newborn.values())
        extra = ":" + json.dumps({**obs.mismatch, "_updates": obs.s["updates"], "_n_cal": n_cal, "_n_dec": n_dec,
                                  "_births": births}, sort_keys=True, separators=(",", ":"))
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
    specs = [("r", seed, years, obs) for seed, years in ((501, 20), (601, 60)) for obs in (0, 1)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        off, on = got[("r", seed, years, 0)], got[("r", seed, years, 1)]
        ro = hs(off) == hs(on)
        info = json.loads(on.split(":", 2)[2])
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        tabled = info["_n_dec"] == info["_n_cal"] and info["_n_cal"] > 0
        born = info["_births"] > 0 or years < 60
        t = ro and not any(mism.values()) and info.get("_updates", 0) > 0 and tabled and born
        ok &= t
        lines.append(f"seed {seed}, {years} years, arm r: observer read-only: {'yes' if ro else 'NO'}; "
                     f"update-replay mismatches: {mism or 'none'}; habit updates replayed {info['_updates']:.0f}; "
                     f"every counted update in the decade table once ({info['_n_dec']} = {info['_n_cal']}): "
                     f"{'yes' if tabled else 'NO'}; newborns recorded: {info['_births']}")
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
    obs = UV3Obs(w)
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
