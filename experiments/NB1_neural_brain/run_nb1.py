"""NB1 — can a neural-brained people survive and improve over generations? (questions.md, frozen as `NB1-frozen`, with
amendments 1 and 2). `code_nb1` = `code_v17` + the neural brain (patch_nb1.py; v17_to_nb1.diff). Phase 1: arms v17 (c),
neural brain with learning (n), neural brain without learning (e); LP; seeds 25401-25416; 600 years.

Observers (read-only):
  guard sums  CI1's eight guards' sums over years 100-600 (CI1's definitions, without its per-kind tracking)
  yearly      population; in n and e the mean and sd of g, mean learning rate, and the genetic variance of the weights
  decisions   at every 50th neural decision: the correlation between the network's part and the hand-written part of
              the options' scores, and the ratio of their spreads
  actions     the grown's action mix per century (for its entropy)
  genomes     the first 60 births of generations 1, 9 and 18 (amendment 3) (for phase 2, the common garden)
  people      at the end, from the world's own record of everyone born: generation, reached 16, age at death

  python experiments/NB1_neural_brain/run_nb1.py zero
  python experiments/NB1_neural_brain/run_nb1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")      # tiny matrices: no threads, the same arithmetic every time
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import json  # noqa: E402
import math  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
from collections import Counter, defaultdict  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
sys.path.insert(0, str(HERE.parent / "CI1_children_and_aims"))
import run_es2 as base  # noqa: E402

base.CODES["nb1"] = HERE / "code_nb1"
base.CODES["v17"] = HERE.parent / "NV17_nature_v17" / "code_v17"
CODE = "nb1"
WPY, YEARS = base.WPY, 600
SEEDS = tuple(range(25401, 25417))        # 16 new paired seeds, used by no study
ARMS = {"c": {**base.LP, "nb_brain": 0},
        "n": {**base.LP, "nb_brain": 1, "nb_learn": 1},
        "e": {**base.LP, "nb_brain": 1, "nb_learn": 0}}
OUT = HERE / "output"
CHILD, ADULT, OLD = 12 * WPY, 16 * WPY, 50 * WPY
LATE = [100 * WPY, 600 * WPY]
SAMPLE_GENS, SAMPLE_N = (1, 9, 18), 60          # amendment 3
CUR = []


def kin_child(world, giver, q) -> bool:
    import run_ci1
    return run_ci1.kin_child(world, giver, q)


class NBObs:
    def __init__(self, w):
        self.w = w
        self.s = Counter()
        self.years = []
        self.acts = defaultdict(Counter)       # century -> action -> grown person-weeks
        self.corr = Counter()
        self.samples = {g: [] for g in SAMPLE_GENS}
        self.seen = len(w.people)
        CUR[:] = [self]

    def decision(self, hand, net):
        n = len(hand)
        if n < 3:
            return
        mh, mn = sum(hand) / n, sum(net) / n
        vh = sum((x - mh) ** 2 for x in hand)
        vn = sum((x - mn) ** 2 for x in net)
        self.corr["looks"] += 1
        if vh > 0 and vn > 0:
            self.corr["corr_n"] += 1
            self.corr["corr_sum"] += sum((a - mh) * (b - mn) for a, b in zip(hand, net)) / math.sqrt(vh * vn)
        self.corr["sd_hand"] += math.sqrt(vh / n)
        self.corr["sd_net"] += math.sqrt(vn / n)

    def __call__(self, world, events):
        tick = world.tick - 1
        living = world.living()
        # newly born people (the world's dict keeps insertion order): genome samples for phase 2
        ppl = world.people
        if len(ppl) > self.seen:
            for p in list(ppl.values())[self.seen:]:
                g = p.generation
                if g in self.samples and len(self.samples[g]) < SAMPLE_N and p.nb is not None:
                    self.samples[g].append({"g": p.nb["g"], "eta": p.nb["eta"], "genome": list(p.nb["genome"])})
            self.seen = len(ppl)
        for p in living:
            if p.age(world.tick) >= ADULT and p.last_action:
                self.acts[tick // (100 * WPY)][p.last_action] += 1
        if tick % WPY == WPY - 1:
            self.yearly(world, tick, living)
        if not (LATE[0] <= tick < LATE[1]):
            return
        for ev in events:                      # CI1's guard sums, as CI1Obs counts them
            k = ev["k"]
            if k == "death":
                child = ev.get("age", 99) < 12
                self.s["deaths"] += 1
                self.s[f"death_{ev.get('cause', '?')}"] += 1
                if child:
                    self.s["child_deaths"] += 1
                    self.s[f"child_death_{ev.get('cause', '?')}"] += 1
            elif k == "give":
                a, t = world.people.get(ev.get("a")), world.people.get(ev.get("b"))
                if a is not None and t is not None and t.age(tick) < CHILD and kin_child(world, a, t):
                    self.s["gifts_kin_children"] += 1
        for p in living:
            age = p.age(world.tick)
            if age < CHILD:
                self.s["child_weeks"] += 1
            elif age >= ADULT:
                self.s["adult_weeks"] += 1
        self.s["living_weeks"] += len(living)
        if tick % WPY == WPY - 1:
            adults = [p for p in living if ADULT <= p.age(world.tick) < OLD]
            self.s["census_adults"] += len(adults)
            self.s["census_health"] += sum(p.health for p in adults)

    def yearly(self, world, tick, living):
        row = {"year": (tick + 1) // WPY, "pop": len(living)}
        nbs = [p.nb for p in living if p.nb is not None]
        if nbs:
            import numpy as np
            gs = np.array([x["g"] for x in nbs])
            row["g_mean"], row["g_sd"] = float(gs.mean()), float(gs.std())
            row["eta_mean"] = float(np.mean([x["eta"] for x in nbs]))
            G = np.array([x["genome"] for x in nbs])
            row["w_var"] = float(G.var(axis=0).mean())
            row["gen_mean"] = float(np.mean([p.generation for p in living]))
        self.years.append(row)

    def people(self, world):
        """From the world's own record of everyone born in it: per generation, births with a known outcome, those who
        reached 16, and the ages at death of those who died grown."""
        end = world.tick
        gen = defaultdict(lambda: [0, 0, 0, 0.0, 0])      # known, reached16, adult deaths, sum of their ages, censored
        for p in world.people.values():
            if p.birth < 0:
                continue                           # founders
            age_end = (p.death_tick if not p.alive else end) - p.birth
            row = gen[p.generation]
            if age_end >= ADULT:
                row[0] += 1
                row[1] += 1
                if not p.alive:
                    row[2] += 1
                    row[3] += age_end / WPY
            elif not p.alive:
                row[0] += 1
            else:
                row[4] += 1
        return {str(k): v for k, v in sorted(gen.items())}

    def results(self, world):
        return {"sums": dict(self.s), "years": self.years, "acts": {str(k): dict(v) for k, v in self.acts.items()},
                "corr": dict(self.corr), "gens": self.people(world), "samples": {str(k): v for k, v in self.samples.items()}}


def install():
    from acl import brain_nb
    if getattr(brain_nb.rescore, "_nb1", False):
        return
    rescore0 = brain_nb.rescore
    calls = [0]

    def rescore(world, p, options, near, hunger, fatigue, lw, base_):
        new = rescore0(world, p, options, near, hunger, fatigue, lw, base_)
        o = CUR[0] if CUR else None
        if o is not None and p.nb is not None and new is not options:
            calls[0] += 1
            if calls[0] % 50 == 0:
                from acl.person import A
                g = p.nb["g"]
                hand = [g * (s - lw * p.q[base_ + A[a]]) for s, a, _ in options]
                net = [n[0] - h for n, h in zip(new, hand)]
                o.decision(hand, net)
        return new
    rescore._nb1 = True
    brain_nb.rescore = rescore


def make(seed, arm, code=CODE):
    base.setup(code)
    kw = dict(ARMS[arm])
    if code != CODE:
        kw.pop("nb_brain", None)
        kw.pop("nb_learn", None)
    return base.make_world(seed, kw)


def hashrun(code, arm, seed, years, observe):
    LATE[0], LATE[1] = 0, years * WPY
    w = make(seed, arm, code)
    obs = None
    if observe:
        install()
        obs = NBObs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results(w)
        extra = ":" + json.dumps({"corr": r["corr"], "last_year": r["years"][-1] if r["years"] else {},
                                  "samples": {k: len(v) for k, v in r["samples"].items()}}, sort_keys=True,
                                 separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def reload_check(seed):
    w = make(seed, "n")
    from acl.world import World
    for _ in range(10 * WPY):
        w.step()
    b = World.from_dict(json.loads(json.dumps(w.to_dict())))
    for x in (w, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(w) == base.world_hash(b) and b.cfg.nb_brain == 1


def unit_check(seed, years=10):
    """The network's scores and learning step against independent computations; inheritance; g's range; learning off."""
    import numpy as np
    w = make(seed, "n")
    from acl import brain_nb, biology
    st = Counter()
    rescore0, learn0, child0 = brain_nb.rescore, brain_nb.learn, brain_nb.child

    def indep_scores(wv, X):
        nin, nh = brain_nb.N_IN, brain_nb.N_HID
        out = []
        for x in X:
            h = []
            for j in range(nh):
                z = wv[nh * nin + j] + sum(wv[j * nin + i] * x[i] for i in range(nin))
                h.append(math.tanh(z))
            out.append(sum(wv[nh * nin + nh + j] * h[j] for j in range(nh)) + wv[-1])
        return out

    def rescore(world, p, options, near, hunger, fatigue, lw, base_):
        new = rescore0(world, p, options, near, hunger, fatigue, lw, base_)
        if p.nb is not None and new is not options and st["score_looks"] < 300:
            X = brain_nb.LAST[(id(world), p.id)][0]
            ind = indep_scores(p.nb["w"], X.tolist())
            from acl.person import A
            hand = [p.nb["g"] * (s - lw * p.q[base_ + A[a]]) for s, a, _ in options]
            st["score_looks"] += 1
            if max(abs(n[0] - h - x) for n, h, x in zip(new, hand, ind)) > 1e-9:
                st["score_mismatch"] += 1
        return new

    def learn(world, p, r, on):
        rec = brain_nb.LAST.get((id(world), p.id))
        if rec is not None and rec[3] is not None and p.nb is not None and on and st["grad_looks"] < 60:
            X, H, fs, (i, T) = rec
            wv = np.asarray(p.nb["w"], dtype=float)
            g_an = brain_nb.grad_logpi(wv, X, H, fs, i, T)
            hand = fs - brain_nb.scores(wv, X)[0]          # the hand-written part, fixed while w moves

            def logpi(v):
                s = (hand + brain_nb.scores(v, X)[0]) / T
                return s[i] - (s.max() + math.log(np.exp(s - s.max()).sum()))
            idx = [0, 7, 100, brain_nb.N_HID * brain_nb.N_IN + 3, brain_nb.N_W - 5]
            for k in idx:
                e = np.zeros_like(wv)
                e[k] = 1e-6
                num = (logpi(wv + e) - logpi(wv - e)) / 2e-6
                if abs(num - g_an[k]) > 1e-5 * max(1.0, abs(num)):
                    st["grad_mismatch"] += 1
            st["grad_looks"] += 1
        return learn0(world, p, r, on)

    def child(world, mother, father):
        out = child0(world, mother, father)
        par = [x for x in (mother, father) if x is not None and x.nb is not None]
        if par and st["child_looks"] < 200:
            g = np.asarray(out["genome"])
            d = [float(np.abs(g - np.asarray(x.nb["genome"])).max()) for x in par]
            st["child_looks"] += 1
            if min(d) > 6 * brain_nb.W_SD:
                st["child_not_one_parent"] += 1
            if not (0.0 <= out["g"] <= brain_nb.G_MAX):
                st["g_out_of_range"] += 1
        return out
    brain_nb.rescore, brain_nb.learn, brain_nb.child = rescore, learn, child
    try:
        for _ in range(years * WPY):
            w.step()
    finally:
        brain_nb.rescore, brain_nb.learn, brain_nb.child = rescore0, learn0, child0
    # learning off: the working weights stay the genome
    x = make(seed, "e")
    for _ in range(3 * WPY):
        x.step()
    diff = [p for p in x.living() if p.nb is not None and p.nb["w"] != p.nb["genome"]]
    st["learn_off_changed"] = len(diff)
    st["learn_off_people"] = sum(1 for p in x.living() if p.nb is not None)
    ok = (st["score_looks"] > 0 and st["score_mismatch"] == 0 and st["grad_looks"] > 0 and st["grad_mismatch"] == 0
          and st["child_looks"] > 0 and st["child_not_one_parent"] == 0 and st["g_out_of_range"] == 0
          and st["learn_off_changed"] == 0 and st["learn_off_people"] > 0)
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
             for code, arm, obs in (("v17", "c", 0), ("nb1", "c", 0), ("nb1", "c", 1), ("nb1", "n", 0), ("nb1", "n", 1),
                                    ("nb1", "e", 0))]
    with ThreadPoolExecutor(2) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        unit = ex.submit(call, "unit", 701)
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
    for seed, years in ((501, 20), (601, 60)):
        same = hs(got[("v17", "c", seed, years, 0)]) == hs(got[("nb1", "c", seed, years, 0)])
        ro = (hs(got[("nb1", "c", seed, years, 0)]) == hs(got[("nb1", "c", seed, years, 1)])
              and hs(got[("nb1", "n", seed, years, 0)]) == hs(got[("nb1", "n", seed, years, 1)]))
        acts = hs(got[("nb1", "n", seed, years, 0)]) != hs(got[("nb1", "c", seed, years, 0)])
        eacts = hs(got[("nb1", "e", seed, years, 0)]) != hs(got[("nb1", "c", seed, years, 0)])
        ne = hs(got[("nb1", "n", seed, years, 0)]) != hs(got[("nb1", "e", seed, years, 0)])
        ok &= same and ro and acts and eacts and ne
        info = got[("nb1", "n", seed, years, 1)].split(":", 2)[2]
        lines.append(f"seed {seed}, {years} years: code_nb1 with nb_brain 0 = code_v17: {'yes' if same else 'NO'}; "
                     f"observers read-only (c, n): {'yes' if ro else 'NO'}; n acts: {'yes' if acts else 'NO'}; e acts: "
                     f"{'yes' if eacts else 'NO'}; n and e differ: {'yes' if ne else 'NO'}; n: {info}")
    u = json.loads(unit.result())
    ok &= u[0]
    lines.append(f"unit checks, arm n, seed 701, 10 years (scores = an independent computation; the learning step = a "
                 f"finite-difference gradient; a child's genome is one parent's within the mutation; g within [0, 2]; "
                 f"learning off leaves the weights = the genome): {'yes' if u[0] else 'NO'}; {u[1]}")
    t = rl.result()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm n, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_nb1 fingerprint: {call('fp')}")
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
    obs = NBObs(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_nb1", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results(w)}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, extinct {res['extinct']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "unit":
        print(json.dumps(unit_check(int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 10)))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: every year counted; never study data
        LATE[0], LATE[1] = 0, int(sys.argv[4]) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
