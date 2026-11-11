"""NB3: feelings (questions.md, frozen as `NB3-frozen`). Built from run_nb2.py; code_nb3 = code_nb2 + feelings.
Arms c (v17), n2 (NB2 unchanged), f0, fH, f, f-E (fmE), f-H (fmH); seeds 25801-25816; 600 years.

NB2's docstring follows.
NB2: connect the world to the neural brain. Can the network decide? (questions.md, frozen as `NB2-frozen`).
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
sys.path.insert(0, str(HERE.parent / "NB2_connected_brain"))
import run_nb1 as nb1run  # noqa: E402

base = nb1run.base
base.CODES["nb3"] = HERE / "code_nb3"
base.CODES["nb2"] = HERE.parent / "NB2_connected_brain" / "code_nb2"
base.CODES["nb1"] = HERE.parent / "NB1_neural_brain" / "code_nb1"
CODE = "nb3"
WPY, YEARS = base.WPY, 600
SEEDS = tuple(range(25801, 25817))
NB = {"nb_brain": 1, "nb2": 1, "nb_options": 1}
FULL = {**base.LP, **NB, "nb_learn": 1, "nb_critic": 1, "nb_social": 1}
F3 = {"nb3": 1, "nb3_no_attack_joy": 1}
ALLF = {**F3, "nb3_E": 1, "nb3_G": 1, "nb3_L": 1, "nb3_A": 1, "nb3_C": 1, "nb3_H": 1}
ARMS = {"c": {**base.LP, "nb_brain": 0},
        "n2": dict(FULL),
        "f0": {**FULL, **F3},
        "fH": {**FULL, **F3, "nb3_H": 1},
        "f": {**FULL, **ALLF},
        "fmE": {**FULL, **ALLF, "nb3_E": 0},
        "fmH": {**FULL, **ALLF, "nb3_H": 0}}
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


_yearly0 = nb1run.NBObs.yearly


def _yearly_nb3(self, world, tick, living):
    """NB2's yearly record, plus the mean of each NB3 feeling gene (read-only)."""
    _yearly0(self, world, tick, living)
    nbs = [p.nb for p in living if p.nb is not None and "E" in p.nb]
    if nbs and self.years:
        for k in ("E", "G", "L", "A", "C", "H"):
            self.years[-1][f"{k}_mean"] = round(sum(x[k] for x in nbs) / len(nbs), 5)


nb1run.NBObs.yearly = _yearly_nb3
_call0 = nb1run.NBObs.__call__


def _call_nb3(self, world, events):
    """NB1's observer, plus each genome sample's feeling genes, so the garden can keep them (read-only)."""
    seen0 = self.seen
    had = {g: len(v) for g, v in self.samples.items()}
    _call0(self, world, events)
    if self.seen > seen0:
        put = dict(had)
        for p in list(world.people.values())[seen0:self.seen]:
            g = p.generation
            if g in self.samples and p.nb is not None and put[g] < len(self.samples[g]):
                if "E" in p.nb:
                    self.samples[g][put[g]].update({k: p.nb[k] for k in ("E", "G", "L", "A", "C", "H")})
                put[g] += 1


nb1run.NBObs.__call__ = _call_nb3


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
                if world.cfg.nb3:             # NB3: the inborn reluctance is an instinct, not the network
                    from acl import brain_nb3
                    hand = [h + brain_nb3.harm_bias(world, p, a, t) for h, (_, a, t) in zip(hand, options)]
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
        for k in [k for k in kw if k.startswith("nb3")]:
            kw.pop(k, None)
    if code not in (CODE, "nb2"):
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
    w = make(seed, "f")
    from acl.world import World
    for _ in range(10 * WPY):
        w.step()
    b = World.from_dict(json.loads(json.dumps(w.to_dict())))
    from acl import brain_nb2, brain_nb3
    for d in (brain_nb2.LAST, brain_nb2.CHOSEN, brain_nb2.OBS, brain_nb3.APPR):
        d.clear()
    for x in (w, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(w) == base.world_hash(b) and b.cfg.nb3 == 1


def ckpt_check(seed):
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        a = subprocess.run([sys.executable, str(Path(__file__).resolve()), "one", "f", str(seed), "15", str(td / "a")],
                           capture_output=True, text=True)
        me = [sys.executable, str(Path(__file__).resolve()), "part", "f", str(seed), "15", str(td / "b"), str(td / "ck")]
        b1 = subprocess.run(me + ["-1"], capture_output=True, text=True)
        b2 = subprocess.run(me + ["1e9"], capture_output=True, text=True)
        if a.returncode or b1.returncode or b2.returncode:
            return False
        ra = json.loads((td / "a" / f"f_seed_{seed}.json").read_text())
        rb = json.loads((td / "b" / f"f_seed_{seed}.json").read_text())
        ra.pop("jobs", None)
        jobs = rb.pop("jobs", None)
        return ra == rb and jobs == 2


def unit_check(seed, years=8):
    """NB3's feelings against independent readings: the feeling genes come from the same parent as the network genome,
    within the mutation, in [0, 2]; attack and steal options carry -H in their score unless in defence; guilt rises by
    the frozen amounts for an attack one starts and not in defence; empathy, guilt and approval parts of the feeling
    equal an independent computation in sampled weeks."""
    import numpy as np
    w = make(seed, "f")
    from acl import brain_nb2 as b2, brain_nb3 as b3, actions
    st = Counter()
    child0, rescore0, feel0, attack0 = b2.child, b2.rescore, b3.feel, actions._attack
    handler0 = actions.HANDLERS["attack"]

    def child(world, mother, father):
        out = child0(world, mother, father)
        par = [x for x in (mother, father) if x is not None and x.nb is not None]
        if par and st["child_looks"] < 200:
            g = np.asarray(out["genome"])
            src = min(par, key=lambda x: float(np.abs(g - np.asarray(x.nb["genome"])).max()))
            st["child_looks"] += 1
            for k in b3.GENES:
                if not (0.0 <= out[k] <= b3.GENE_MAX) or abs(out[k] - src.nb[k]) > 6 * b3.GENE_SD:
                    st["gene_bad"] += 1
        return out

    def rescore(world, p, options, near, hunger, fatigue, lw, base_):
        new = rescore0(world, p, options, near, hunger, fatigue, lw, base_)
        if p.nb is not None and new is not options and st["hb_looks"] < 400:
            from acl.person import A
            X = b2.LAST[(id(world), p.id)][0]
            net = b2.actor_scores(p.nb["w"], X)[0]
            for k, ((s, a, t), n) in enumerate(zip(options, new)):
                hand = p.nb["g"] * (s - lw * p.q[base_ + A[a]])
                bias = n[0] - hand - float(net[k])
                expect = 0.0
                if a in ("attack", "steal"):
                    expect = -p.nb["H"]
                    if a == "attack" and isinstance(t, str) and t in world.people and b3.defence(world, p, world.people[t]):
                        expect = 0.0
                    st["hb_harm_options"] += 1
                if abs(bias - expect) > 1e-9:
                    st["hb_mismatch"] += 1
            st["hb_looks"] += 1
        return new

    def attack(world, p, target, eff):
        q = world.people.get(target)
        g0 = p.nb.get("guilt", 0.0) if p.nb is not None else None
        defending = q is not None and b3.defence(world, p, q)
        kin = q is not None and world.kinship(p, q) > 0
        out = attack0(world, p, target, eff)
        if p.alive and p.nb is not None and q is not None and g0 is not None and st["guilt_looks"] < 300:
            want = 0.0 if defending else 0.3 + ((1.0 * (2.0 if kin else 1.0)) if not q.alive else 0.0)
            if abs((p.nb.get("guilt", 0.0) - g0) - want) > 1e-9:
                st["guilt_mismatch"] += 1
            st["guilt_looks"] += 1
        return out

    def feel(world, p):
        snap = None
        if p.nb is not None and st["feel_looks"] < 300:
            nb = p.nb
            c = world.cfg
            num = den = 0.0
            for q in world.people_near(p.loc, c.reach, exclude=p.id):
                kin = world.kinship(p, q) > 0 or p.partner == q.id
                r = p.rel.get(q.id)
                wt = 1.0 if kin else (0.5 if r is not None and r.affection > 0.3 else 0.2)
                if q.nb is None:
                    last = b3.distress(world, q)
                elif q.nb.get("d_week") == world.tick:
                    last = q.nb.get("d_last", q.nb.get("d_now", 0.0))
                else:
                    last = q.nb.get("d_now", b3.distress(world, q))
                d = b3.distress(world, q)
                num += wt * (max(0.0, d - last) + 0.25 * d)
                den += wt
            emp = -nb["E"] * num / den if den else 0.0
            snap = emp - nb["G"] * nb.get("guilt", 0.0) + nb["A"] * b3.APPR.get((id(world), p.id), 0.0)
            # love and curiosity, computed independently
            tick = world.tick
            young = [world.people[k] for k in p.children if world.people[k].alive and world.people[k].age(tick) < 12 * 52]
            love = 0.0
            if young:
                small = [k for k in young if k.age(tick) < 6 * 52]
                well = 0.0
                if small:
                    good = 0
                    for k in small:
                        carer = world.people.get(k.caregiver)
                        if k.edible() >= 0.5 * k.need(c, tick) and k.health >= 50 and carer is not None and carer.loc == k.loc:
                            good += 1
                    well = good / len(small)
                love = well - 0.5 * sum(b3.distress(world, k) for k in young) / len(young)
            ch = b2.CHOSEN.get((id(world), p.id))
            care = 0.1 if (ch is not None and ch[0] == tick and ch[1] in ("care", "give") and ch[2] in p.children) else 0.0
            cur = 0.0
            if p.last_action not in ("attack", "steal"):
                cur = 0.1 / (1 + nb["cnt"].get(f"{p.last_ctx}:{p.last_action}", 0))
            snap += nb["L"] * (love + care) + nb["C"] * cur
        out = feel0(world, p)
        if snap is not None:
            st["feel_looks"] += 1
            if abs(out - snap) > 1e-9:
                st["feel_mismatch"] += 1
        return out

    b2.child, b2.rescore, b3.feel, actions._attack = child, rescore, feel, attack
    actions.HANDLERS["attack"] = attack
    try:
        for _ in range(years * WPY):
            w.step()
    finally:
        b2.child, b2.rescore, b3.feel, actions._attack = child0, rescore0, feel0, attack0
        actions.HANDLERS["attack"] = handler0
    ok = (st["child_looks"] > 0 and st["gene_bad"] == 0 and st["hb_looks"] > 0 and st["hb_mismatch"] == 0
          and st["hb_harm_options"] > 0 and st["guilt_mismatch"] == 0 and st["feel_looks"] > 0 and st["feel_mismatch"] == 0)
    return ok, dict(st)


def hashrun(code, arm, seed, years, observe):
    LATE[0], LATE[1] = 0, years * WPY
    w = make(seed, arm, code)
    obs = None
    if observe:
        install()
        obs = NB2Obs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results(w)
        extra = ":" + json.dumps({"ext": r.get("ext", {}), "last_year": r["years"][-1] if r["years"] else {}},
                                 sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


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
    arms = list(ARMS)
    specs = [("nb2", "n2", 501, 20, 0)] + [("nb3", a, 501, 20, 0) for a in arms] + [("nb3", "f", 501, 20, 1)]
    with ThreadPoolExecutor(2) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        unit = ex.submit(call, "unit", 701)
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
        ck = ex.submit(lambda: subprocess.run(me + ["ckcheck", "502"], capture_output=True, text=True).stdout.split())
    same = hs(got[("nb2", "n2", 501, 20, 0)]) == hs(got[("nb3", "n2", 501, 20, 0)])
    differ = all(hs(got[("nb3", x, 501, 20, 0)]) != hs(got[("nb3", y, 501, 20, 0)])
                 for i, x in enumerate(arms) for y in arms[i + 1:])
    ro = hs(got[("nb3", "f", 501, 20, 0)]) == hs(got[("nb3", "f", 501, 20, 1)])
    ok &= same and differ and ro
    lines.append(f"seed 501, 20 years: code_nb3 with NB3 off (arm n2) = code_nb2's full arm: {'yes' if same else 'NO'}; "
                 f"the seven arms all differ: {'yes' if differ else 'NO'}; observers read-only (f): {'yes' if ro else 'NO'}")
    u = json.loads(unit.result())
    ok &= u[0]
    lines.append(f"unit checks, arm f, seed 701, 8 years (feeling genes from the genome's parent within the mutation, in "
                 f"[0, 2]; attack and steal scores carry -H unless in defence; guilt rises by the frozen amounts for an "
                 f"attack one starts, not in defence; the week's feeling = an independent computation of all its parts): "
                 f"{'yes' if u[0] else 'NO'}; {u[1]}")
    t = rl.result()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm f, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    t2 = ck.result()[-1:] == ["True"]
    ok &= t2
    lines.append(f"arm f, seed 502: 15 years in one job = 1 year, a checkpoint, and 14 years in a second job: "
                 f"{'yes' if t2 else 'NO'}")
    lines.append(f"code_nb3 fingerprint: {call('fp')}")
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
    from acl import brain_nb3 as b3
    rec["APPR"] = {k[1]: v for k, v in b3.APPR.items() if k[0] == me}
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
    from acl import brain_nb3 as b3
    for pid, v in d["b2"].get("APPR", {}).items():
        b3.APPR[(id(w), pid)] = v
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
                p.nb.update({k: gnm[k] for k in ("E", "G", "L", "A", "C", "H") if k in gnm})  # NB3: as inherited
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
    res = {"arm": arm, "seed": seed, "nature": "code_nb3", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
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
