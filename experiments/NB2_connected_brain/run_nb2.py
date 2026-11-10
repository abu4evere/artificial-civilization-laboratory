"""NB2: connect the world to the neural brain. Can the network decide? (questions.md, frozen as `NB2-frozen`).
`code_nb2` = `code_nb1` + NB2 (patch_nb2.py). Phase 1: arms c (v17), s (new options and sight, learning off), o (+ NB1's
REINFORCE), l (+ actor-critic instead), n (+ social learning: the full NB2); LP; seeds 25601-25616; 600 years.

Observers (read-only), as NB1's (run_nb1.NBObs: guard sums, yearly g, action mix, genome samples of generations 1, 9
and 18, people), plus at every 50th neural decision: the correlation of the network's and the instinct's parts, how
often the network's part changes the top option, the number of options, and which of an action's targets was taken.

  python experiments/NB2_connected_brain/run_nb2.py zero
  python experiments/NB2_connected_brain/run_nb2.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import json  # noqa: E402
import math  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
from collections import Counter  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "NB1_neural_brain"))
import run_nb1 as nb1run  # noqa: E402

base = nb1run.base
base.CODES["nb2"] = HERE / "code_nb2"
base.CODES["nb1"] = HERE.parent / "NB1_neural_brain" / "code_nb1"
CODE = "nb2"
WPY, YEARS = base.WPY, 600
SEEDS = tuple(range(25601, 25617))
NB = {"nb_brain": 1, "nb2": 1, "nb_options": 1}
ARMS = {"c": {**base.LP, "nb_brain": 0},
        "s": {**base.LP, **NB, "nb_learn": 0},
        "o": {**base.LP, **NB, "nb_learn": 1},
        "l": {**base.LP, **NB, "nb_learn": 1, "nb_critic": 1},
        "n": {**base.LP, **NB, "nb_learn": 1, "nb_critic": 1, "nb_social": 1}}
OUT = HERE / "output"
LATE = nb1run.LATE
CUR = nb1run.CUR


class NB2Obs(nb1run.NBObs):
    def __init__(self, w):
        super().__init__(w)
        self.ext = Counter()
        self.calls = 0

    def decision2(self, options, hand, net):
        self.decision(hand, net)
        n = len(options)
        self.ext["looks"] += 1
        self.ext["options"] += n
        top_h = max(range(n), key=lambda k: (hand[k], -k))
        top = max(range(n), key=lambda k: (hand[k] + net[k], -k))
        self.ext["override"] += int(top != top_h)
        a = options[top][1]
        same = [k for k in range(n) if options[k][1] == a]
        self.ext[f"target_rank_{same.index(top)}"] += 1
        self.ext[f"targets_offered_{min(len(same), 4)}"] += 1

    def results(self, world):
        r = super().results(world)
        r["ext"] = dict(self.ext)
        # the primary: people born in years 100-600 whose outcome is known (reached 16, or died before), and those
        # who reached 16
        end, lo, hi = world.tick, LATE[0], LATE[1]
        known = reached = 0
        for q in world.people.values():
            if not (lo <= q.birth < hi):
                continue
            age_end = (q.death_tick if not q.alive else end) - q.birth
            if age_end >= nb1run.ADULT:
                known += 1
                reached += 1
            elif not q.alive:
                known += 1
        r["late_births"] = [known, reached]
        return r


def install():
    from acl import brain_nb2
    if getattr(brain_nb2.rescore, "_nb2", False):
        return
    rescore0 = brain_nb2.rescore

    def rescore(world, p, options, near, hunger, fatigue, lw, base_):
        new = rescore0(world, p, options, near, hunger, fatigue, lw, base_)
        o = CUR[0] if CUR else None
        if o is not None and p.nb is not None and new is not options:
            o.calls += 1                      # kept on the observer, so a checkpoint keeps the sampling in step
            if o.calls % 50 == 0:
                from acl.person import A
                gf = world.cfg.nb_g_fixed
                g = gf if gf >= 0.0 else p.nb["g"]
                hand = [g * (s - lw * p.q[base_ + A[a]]) for s, a, _ in options]
                net = [n[0] - h for n, h in zip(new, hand)]
                o.decision2(options, hand, net)
        return new
    rescore._nb2 = True
    brain_nb2.rescore = rescore


def make(seed, arm, code=CODE, extra=None):
    base.setup(code)
    kw = dict(ARMS[arm])
    if extra:
        kw.update(extra)
    if code != CODE:
        for k in ("nb2", "nb_options", "nb_critic", "nb_social", "nb_g_fixed"):
            kw.pop(k, None)
        if code == "v17":
            kw.pop("nb_brain", None)
            kw.pop("nb_learn", None)
    return base.make_world(seed, kw)


def hashrun(code, arm, seed, years, observe):
    LATE[0], LATE[1] = 0, years * WPY
    if arm == "n1":                              # NB1's n arm, in code_nb1 or in code_nb2 with every NB2 switch off
        base.setup(code)
        w = base.make_world(seed, {**base.LP, "nb_brain": 1, "nb_learn": 1})
    else:
        w = make(seed, arm, code)
    obs = None
    if observe:
        if code == CODE and arm != "n1":
            install()
            obs = NB2Obs(w)
        else:
            nb1run.install()
            obs = nb1run.NBObs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results(w)
        extra = ":" + json.dumps({"corr": r["corr"], "ext": r.get("ext", {}),
                                  "last_year": r["years"][-1] if r["years"] else {}}, sort_keys=True,
                                 separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def reload_check(seed):
    w = make(seed, "n")
    from acl.world import World
    for _ in range(10 * WPY):
        w.step()
    b = World.from_dict(json.loads(json.dumps(w.to_dict())))
    # the week's working records (decisions, the carer's choice, last week's mood changes) are not saved: clear them in
    # both before comparing, as a fresh start of both from the saved state
    from acl import brain_nb2
    for d in (brain_nb2.LAST, brain_nb2.CHOSEN, brain_nb2.OBS):
        d.clear()
    for x in (w, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(w) == base.world_hash(b) and b.cfg.nb2 == 1


def ckpt_check(seed):
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        a = subprocess.run([sys.executable, str(Path(__file__).resolve()), "one", "n", str(seed), "15", str(td / "a")],
                           capture_output=True, text=True)
        me = [sys.executable, str(Path(__file__).resolve()), "part", "n", str(seed), "15", str(td / "b"), str(td / "ck")]
        b1 = subprocess.run(me + ["-1"], capture_output=True, text=True)          # a budget spent at once: checkpoint at year 1
        b2 = subprocess.run(me + ["1e9"], capture_output=True, text=True)         # the next job continues to the end
        if a.returncode or b1.returncode or b2.returncode:
            return False
        ra = json.loads((td / "a" / f"n_seed_{seed}.json").read_text())
        rb = json.loads((td / "b" / f"n_seed_{seed}.json").read_text())
        ra.pop("jobs", None)
        jobs = rb.pop("jobs", None)
        return ra == rb and jobs == 2


def unit_check(seed, years=8):
    """Actor scores and both gradients against independent computations; the option list keeps the body's limits and
    at most 4 targets per action; inheritance; g's range; learning off; g held fixed in the gardens."""
    import numpy as np
    w = make(seed, "n")
    from acl import brain_nb2 as b2, mind
    st = Counter()
    rescore0, learn0, child0 = b2.rescore, b2.learn, b2.child

    def indep_scores(wv, X):
        out = []
        for x in X:
            h = [math.tanh(wv[b2.N_HID * b2.N_IN + j] + sum(wv[j * b2.N_IN + i] * x[i] for i in range(b2.N_IN)))
                 for j in range(b2.N_HID)]
            out.append(sum(wv[b2.N_HID * b2.N_IN + b2.N_HID + j] * h[j] for j in range(b2.N_HID)) + wv[b2.N_ACTOR - 1])
        return out

    def rescore(world, p, options, near, hunger, fatigue, lw, base_):
        new = rescore0(world, p, options, near, hunger, fatigue, lw, base_)
        if p.nb is not None and new is not options and st["score_looks"] < 200:
            X = b2.LAST[(id(world), p.id)][0]
            ind = indep_scores(p.nb["w"], X.tolist())
            from acl.person import A
            hand = [p.nb["g"] * (s - lw * p.q[base_ + A[a]]) for s, a, _ in options]
            st["score_looks"] += 1
            if max(abs(n[0] - h - x) for n, h, x in zip(new, hand, ind)) > 1e-9:
                st["score_mismatch"] += 1
            per = Counter(a for _, a, _ in options)
            for a in ("forage", "hunt", "gather", "make", "take"):
                if per[a] > 4:
                    st["over_4_" + a] += 1
            for _, a, t in options:
                if p.energy < mind.COST[a]:
                    st["over_energy"] += 1
        return new

    def learn(world, p, r, on):
        rec = b2.LAST.get((id(world), p.id))
        if rec is not None and rec[3] is not None and p.nb is not None and on and st["grad_looks"] < 40:
            X, H, fs, (i, T), S, acts = rec
            wv = np.asarray(p.nb["w"], dtype=float)
            g_an = b2.grad_logpi(wv, X, H, fs, i, T)
            hand = fs - b2.actor_scores(wv, X)[0]

            def logpi(v):
                s = (hand + b2.actor_scores(v, X)[0]) / T
                return s[i] - (s.max() + math.log(np.exp(s - s.max()).sum()))
            for k in (0, 9, 300, b2.N_HID * b2.N_IN + 2, b2.N_ACTOR - 3, b2.N_ACTOR - 1):
                e = np.zeros_like(wv)
                e[k] = 1e-6
                num = (logpi(wv + e) - logpi(wv - e)) / 2e-6
                if abs(num - g_an[k]) > 1e-5 * max(1.0, abs(num)):
                    st["grad_mismatch"] += 1
            gv = b2.grad_value(wv, S)
            for k in (b2.N_ACTOR, b2.N_ACTOR + 40, b2.N_ACTOR + b2.N_HID * b2.N_BODY + 1, b2.N_W - 4, b2.N_W - 1):
                e = np.zeros_like(wv)
                e[k] = 1e-6
                num = (b2.value(wv + e, S)[0] - b2.value(wv - e, S)[0]) / 2e-6
                if abs(num - gv[k]) > 1e-5 * max(1.0, abs(num)):
                    st["value_grad_mismatch"] += 1
            if np.abs(g_an[b2.N_ACTOR:]).max() > 0 or np.abs(gv[:b2.N_ACTOR]).max() > 0:
                st["grad_crosstalk"] += 1
            st["grad_looks"] += 1
        return learn0(world, p, r, on)

    def child(world, mother, father):
        out = child0(world, mother, father)
        par = [x for x in (mother, father) if x is not None and x.nb is not None]
        if par and st["child_looks"] < 200:
            g = np.asarray(out["genome"])
            d = [float(np.abs(g - np.asarray(x.nb["genome"])).max()) for x in par]
            st["child_looks"] += 1
            if min(d) > 6 * b2.nb1.W_SD:
                st["child_not_one_parent"] += 1
            if not (0.0 <= out["g"] <= b2.nb1.G_MAX) or len(out["genome"]) != b2.N_W:
                st["g_or_size_wrong"] += 1
        return out
    b2.rescore, b2.learn, b2.child = rescore, learn, child
    try:
        for _ in range(years * WPY):
            w.step()
    finally:
        b2.rescore, b2.learn, b2.child = rescore0, learn0, child0
    x = make(seed, "s")
    for _ in range(3 * WPY):
        x.step()
    st["learn_off_changed"] = sum(1 for p in x.living() if p.nb is not None and p.nb["w"] != p.nb["genome"])
    st["learn_off_people"] = sum(1 for p in x.living() if p.nb is not None)
    # the gardens' fixed g: with nb_g_fixed 0 the instinct part is 0 in every option's score
    y = make(seed, "s", extra={"nb_g_fixed": 0.0})
    seen = []
    r0 = b2.rescore

    def rescore_g(world, p, options, near, hunger, fatigue, lw, base_):
        new = r0(world, p, options, near, hunger, fatigue, lw, base_)
        if p.nb is not None and new is not options and len(seen) < 50:
            X = b2.LAST[(id(world), p.id)][0]
            net = b2.actor_scores(p.nb["w"], X)[0]
            seen.append(max(abs(n[0] - float(v)) for n, v in zip(new, net)))
        return new
    b2.rescore = rescore_g
    try:
        for _ in range(WPY):
            y.step()
    finally:
        b2.rescore = r0
    st["g_fixed_looks"] = len(seen)
    st["g_fixed_mismatch"] = sum(1 for v in seen if v > 1e-9)
    ok = (st["score_looks"] > 0 and st["score_mismatch"] == 0 and st["grad_looks"] > 0 and st["grad_mismatch"] == 0
          and st["value_grad_mismatch"] == 0 and st["grad_crosstalk"] == 0 and st["child_looks"] > 0
          and st["child_not_one_parent"] == 0 and st["g_or_size_wrong"] == 0 and st["over_energy"] == 0
          and not any(k.startswith("over_4_") for k in st) and st["learn_off_changed"] == 0
          and st["learn_off_people"] > 0 and st["g_fixed_looks"] > 0 and st["g_fixed_mismatch"] == 0)
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
    specs = [(code, arm, seed, years, obs) for seed, years in ((501, 20), (601, 40))
             for code, arm, obs in (("nb1", "c", 0), ("nb2", "c", 0), ("nb1", "n1", 0), ("nb2", "n1", 0),
                                    ("nb2", "s", 0), ("nb2", "o", 0), ("nb2", "l", 0), ("nb2", "n", 0),
                                    ("nb2", "n", 1))]
    with ThreadPoolExecutor(2) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        unit = ex.submit(call, "unit", 701)
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
        ck = ex.submit(lambda: subprocess.run(me + ["ckcheck", "502"], capture_output=True, text=True).stdout.split())
    for seed, years in ((501, 20), (601, 40)):
        g = {a: hs(got[(code, a, seed, years, 0)]) for code, a, _ in
             (("nb2", "c", 0), ("nb2", "s", 0), ("nb2", "o", 0), ("nb2", "l", 0), ("nb2", "n", 0))}
        same_c = hs(got[("nb1", "c", seed, years, 0)]) == g["c"]
        same_n1 = hs(got[("nb1", "n1", seed, years, 0)]) == hs(got[("nb2", "n1", seed, years, 0)])
        ro = g["n"] == hs(got[("nb2", "n", seed, years, 1)])
        arms = ["c", "s", "o", "l", "n"]
        differ = all(g[a] != g[b] for i, a in enumerate(arms) for b in arms[i + 1:])
        ok &= same_c and same_n1 and ro and differ
        info = got[("nb2", "n", seed, years, 1)].split(":", 2)[2]
        lines.append(f"seed {seed}, {years} years: code_nb2 with NB2 off = code_nb1 (v17 arm c: {'yes' if same_c else 'NO'}; "
                     f"NB1's n arm: {'yes' if same_n1 else 'NO'}); observers read-only (n): {'yes' if ro else 'NO'}; "
                     f"the five arms all differ: {'yes' if differ else 'NO'}; n: {info}")
    u = json.loads(unit.result())
    ok &= u[0]
    lines.append(f"unit checks, arm n, seed 701, 8 years (actor scores = an independent computation; the actor's and the "
                 f"critic's gradients = finite differences, and neither touches the other's numbers; no option beyond "
                 f"the body's energy; at most 4 targets for forage, hunt, gather, make and take; a child's genome is one "
                 f"parent's; g within [0, 2]; learning off leaves the weights = the genome; g held at 0 in the gardens "
                 f"leaves only the network's score): {'yes' if u[0] else 'NO'}; {u[1]}")
    t = rl.result()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm n, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    t2 = ck.result()[-1:] == ["True"]
    ok &= t2
    lines.append(f"arm n, seed 502: 15 years in one job = 1 year, a checkpoint, and 14 years in a second job (world, "
                 f"brain records and every observed number): {'yes' if t2 else 'NO'}")
    lines.append(f"code_nb2 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def save_ckpt(w, obs, path, meta):
    """Everything needed to continue a world exactly in another job: the world, the observer, and the brain's working
    records of this week (re-keyed from this world's id)."""
    import pickle
    from acl import brain_nb2 as b2
    me = id(w)
    rec = {name: {k[1]: v for k, v in d.items() if k[0] == me}
           for name, d in (("LAST", b2.LAST), ("CHOSEN", b2.CHOSEN), ("OBS", b2.OBS))}
    obs.w = None
    blob = pickle.dumps({"meta": meta, "world": w.to_dict(), "obs": obs, "b2": rec}, protocol=4)
    obs.w = w
    tmp = Path(str(path) + ".tmp")
    tmp.write_bytes(blob)
    tmp.replace(path)


def load_ckpt(path):
    import pickle
    d = pickle.loads(Path(path).read_bytes())
    base.setup(CODE)
    from acl.world import World
    from acl import brain_nb2 as b2
    w = World.from_dict(d["world"])
    for name, dd in (("LAST", b2.LAST), ("CHOSEN", b2.CHOSEN), ("OBS", b2.OBS)):
        for pid, v in d["b2"][name].items():
            dd[(id(w), pid)] = v
    obs = d["obs"]
    obs.w = w
    CUR[:] = [obs]
    install()
    w.observers.append(obs)
    return d["meta"], w, obs


def run_one(arm, seed, years=YEARS, out=None, extra=None, founders_from=None, budget_min=None, ckpt=None, resume=None):
    """Runs a world to the end, or (with a budget) until the budget is spent, then saves a checkpoint to `ckpt` and
    returns None; `resume` continues from such a checkpoint."""
    import time
    t0 = time.time()
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    if resume is not None:
        meta, w, obs = load_ckpt(resume)
        assert meta["code_hash"] == f0, "checkpoint from different code"
        arm, seed, years = meta["arm"], meta["seed"], meta["years"]
    else:
        meta = {"arm": arm, "seed": seed, "years": years, "code_hash": f0, "jobs": 0}
        w = make(seed, arm, extra=extra)
        if founders_from is not None:              # the gardens: genomes as all the founders
            for p, gnm in zip([q for q in w.people.values() if q.nb is not None], founders_from):
                p.nb.update({"g": gnm["g"], "eta": gnm["eta"], "genome": list(gnm["genome"]), "w": list(gnm["genome"])})
        install()
        obs = NB2Obs(w)
        w.observers.append(obs)
    meta["jobs"] += 1
    while w.tick < years * WPY:
        w.step()
        if not w.living():
            break
        if budget_min is not None and w.tick % WPY == 0 and (time.time() - t0) / 60.0 > budget_min:
            save_ckpt(w, obs, ckpt, meta)
            print(f"{arm} seed {seed}: checkpoint at year {w.tick // WPY} (job {meta['jobs']})", flush=True)
            return None
    res = {"arm": arm, "seed": seed, "nature": "code_nb2", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), "jobs": meta["jobs"],
           **obs.results(w)}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, extinct {res['extinct']}", flush=True)
    return res


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "unit":
        print(json.dumps(unit_check(int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 8)))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "part":                   # one job's share: start or continue a world, checkpoint when the budget is spent
        arm, seed, years, outd, ckd, budget = (sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]),
                                               Path(sys.argv[6]), float(sys.argv[7]))
        ckd.mkdir(parents=True, exist_ok=True)
        ck = ckd / f"{arm}_seed_{seed}.ckpt"
        prev = ck if ck.exists() else None
        r = run_one(arm, seed, years, outd, budget_min=budget, ckpt=ck, resume=prev)
        if r is not None and ck.exists():
            ck.unlink()                   # finished: the checkpoint is no longer needed
    elif cmd == "ckcheck":                # zero check: 15 years straight = 10 years, checkpoint, 5 years resumed
        print(ckpt_check(int(sys.argv[2])))
    elif cmd == "smoke":                  # a code test of the analysis only: every year counted; never study data
        LATE[0], LATE[1] = 0, int(sys.argv[4]) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
