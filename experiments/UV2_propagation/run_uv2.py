"""UV2 — does the habit floor come from unpractised choices further ahead? (questions.md, frozen as `UV2-frozen`).
Read-only: ES2's arm r replayed on ES2's seeds with `code_es2`, unchanged. UV1's observer (`../UV1_undervaluation_by_
experience/run_uv1.py`, itself ES2's plus k, age and death-closed) is reused as it is; UV2's observer adds:
  U    at each decision that completes a held update: the choice-probability mass (the choice's own softmax over the
       options' scores) on options whose habit the person had updated fewer than 20 times; with no options, the
       look-ahead is rest's value, so U = 1 if that habit has fewer than 20 updates, else 0
  D    for each update: U at the decision that completed it, plus every later U of the same person, weighted exactly as
       G weights the later rewards (1, 0.8, 0.64 ... per habit update), closed with G; Dn = D / (the weights accrued)
  and sums n, (q - G) and |q - G| by k bin, age bin, Dn bin, one-step U bin, year quarter and death-closed.

  python experiments/UV2_propagation/run_uv2.py zero
  python experiments/UV2_propagation/run_uv2.py one r <seed> <years> <out>
"""
from __future__ import annotations

import json
import math
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
UNPRACTISED = 20                          # fewer earlier updates of that habit than this
DN_EDGES, DN_BINS = (0.0, 0.05, 0.1, 0.2, 0.4), ("0-0.05", "0.05-0.1", "0.1-0.2", "0.2-0.4", "0.4-1")
U_EDGES, U_BINS = (0.0, 0.1, 0.25, 0.5), ("0-0.1", "0.1-0.25", "0.25-0.5", "0.5-1")


def year_quarter(tick):
    y = tick // WPY
    return str((y - 100) // 25) if 100 <= y < 200 else "-"


class UV2Obs(uv1.UV1Obs):
    def __init__(self, w):
        super().__init__(w)
        self.u_now = None
        self.uv2 = defaultdict(lambda: [0, 0.0, 0.0])        # "kbin|agebin|dnbin|ubin|quarter|censored" -> [n,
        self.dn_bad = 0                                      #   sum (q-G), sum |q-G|]

    def unpractised(self, world, p, opts, b):
        from acl.person import A
        kk = self.k[p.id]
        if not opts:
            return 1.0 if kk[b + A["rest"]] < UNPRACTISED else 0.0
        top = max(s for s, _ in opts)
        w = [math.exp((s - top) / world.cfg.choice_temperature) for s, _ in opts]
        return sum(wi for wi, (_, a) in zip(w, opts) if kk[b + A[a]] < UNPRACTISED) / sum(w)

    def on_learn(self, world, p, i, before, after, r, fut):
        u, self.u_now = self.u_now, None
        if u is None:                                        # every update in arm r is completed at a decision
            self.mismatch["u_missing"] += 1
            u = 0.0
        for e in self.pending.get(p.id, ()):
            e[6][0] += e[3] * u                              # the same weight G gives this update's reward
            e[6][1] += e[3]
        super().on_learn(world, p, i, before, after, r, fut)
        self.pending[p.id][-1].append([u, 1.0, u, year_quarter(world.tick)])

    def close(self, e, censored):
        super().close(e[:6], censored)
        _, q, acc, _, late, (kb, ab, _), (d, wsum, u1, yq) = e
        if not late:
            return
        dn = d / wsum
        if not -1e-9 <= dn <= 1 + 1e-9:
            self.dn_bad += 1
        c = self.uv2[f"{kb}|{ab}|{uv1.bin_of(dn, DN_EDGES, DN_BINS)}|{uv1.bin_of(u1, U_EDGES, U_BINS)}|{yq}|{censored}"]
        c[0] += 1
        c[1] += q - acc
        c[2] += abs(q - acc)

    def results(self):
        return {**super().results(), "uv2_fields": ["n", "sum_signed", "sum_abs"],
                "uv2_key": "kbin|agebin|dnbin|ubin|quarter|censored", "uv2": dict(self.uv2), "dn_bad": self.dn_bad}


def install(w, obs):
    base.install(w, obs)
    from acl import biology
    inner = biology.apply_held

    def apply_held(world, p, opts, b):
        if world is w:
            obs.u_now = obs.unpractised(world, p, opts, b)
        return inner(world, p, opts, b)
    biology.apply_held = apply_held


def hashrun(arm, seed, years, observe):
    """Zero checks only: every update of the run is counted (ES2 counts years 100-200), so the binning check has data."""
    base.LATE = (0, years * WPY)
    base.setup()
    w = base.make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = UV2Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        n_cal = sum(v[0] for v in obs.cal.values())
        n_uv2 = sum(v[0] for v in obs.uv2.values())
        extra = ":" + json.dumps({**obs.mismatch, "_updates": obs.s["updates"], "_n_cal": n_cal, "_n_uv2": n_uv2,
                                  "_dn_bad": obs.dn_bad}, sort_keys=True, separators=(",", ":"))
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
        binned = info["_n_uv2"] == info["_n_cal"] and info["_n_cal"] > 0
        t = ro and not any(mism.values()) and info.get("_updates", 0) > 0 and binned and info["_dn_bad"] == 0
        ok &= t
        lines.append(f"seed {seed}, {years} years, arm r: observer read-only: {'yes' if ro else 'NO'}; "
                     f"update-replay mismatches (incl. a missing U): {mism or 'none'}; habit updates replayed "
                     f"{info['_updates']:.0f}; every counted update binned once ({info['_n_uv2']} = {info['_n_cal']}): "
                     f"{'yes' if binned else 'NO'}; Dn outside [0, 1]: {info['_dn_bad']}")
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
    obs = UV2Obs(w)
    install(w, obs)
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
