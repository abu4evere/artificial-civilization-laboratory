"""NB3-A: why do the feeling people starve? An exact replay of NB3's worlds with read-only recorders (questions.md,
NB3A-frozen). Code: NB3's code_nb3, unchanged. Arms c, fH, f; seeds 25801-25816; each world to its end.
Validity: each replay must end with the world fingerprint of NB3's phase-1 result.

Readings of the plan's open points are in IMPLEMENTATION.md. Recorders only read; the matched survivors are drawn
from a recorder-only generator, numpy.random.default_rng([seed, 85]), never the world's.

  python experiments/NB3A_feeding_autopsy/run_nb3a.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import json  # noqa: E402
import sys  # noqa: E402
from collections import Counter, defaultdict, deque  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "NB3_feelings"))
import run_nb3 as P  # noqa: E402

base = P.base
WPY, YEARS = P.WPY, 600
SEEDS = P.SEEDS
ARMS = {a: P.ARMS[a] for a in ("c", "fH", "f")}
CODE = P.CODE
NB3_OUT = HERE.parent / "NB3_feelings" / "output"
FOOD_ACTS = ("forage", "hunt", "take")        # gather brings materials, not food (IMPLEMENTATION.md)
HIST = 24
N_CAND = 4                                    # survivor candidates kept per death (the first still alive after 8 weeks)
CUR = [None]                                  # the autopsy recorder of the world now stepping


def agegroup_years(y):
    return "u12" if y < 12 else ("12_15" if y < 16 else "16+")


class Autopsy:
    def __init__(self, w, seed):
        self.w = w
        self.rng = np.random.default_rng([seed, 85])
        self.decade = defaultdict(Counter)
        self.hist = {}                        # pid -> deque of the last 24 weekly records
        self.offered = {}                     # pid -> a food act was offered this week
        self.netchg = {}                      # pid -> the network changed the top option this week
        self.gained = defaultdict(float)      # pid -> food gained by own food acts this week
        self.gain_by = Counter()              # act -> food gained this week (all people)
        self.spoil_pre = None                 # food held by the living just before the body phase
        self.pre = {}                         # pid -> (food held, need) just before the body phase
        self.starved = []
        self.survivors = []
        self.pending = []                     # deaths waiting for a survivor to stay alive 8 more weeks
        self.checks = Counter()

    # --- read-only hooks -------------------------------------------------------------------------------------------
    def on_steer(self, p, options):
        if any(o[1] in FOOD_ACTS for o in options):
            self.offered[p.id] = True

    def on_rescore(self, world, p, options, new, lw, base_):
        from acl.person import A
        from acl import brain_nb3
        gf = world.cfg.nb_g_fixed
        g = gf if gf >= 0.0 else p.nb["g"]
        hand = [g * (s - lw * p.q[base_ + A[a]]) for s, a, _ in options]
        if world.cfg.nb3:
            hand = [h + brain_nb3.harm_bias(world, p, a, t) for h, (_, a, t) in zip(hand, options)]
        n = len(options)
        top_h = max(range(n), key=lambda k: (hand[k], -k))
        top = max(range(n), key=lambda k: (new[k][0], -k))
        self.netchg[p.id] = top != top_h

    def on_food_act(self, act, gains):
        for pid, got in gains.items():
            self.gained[pid] += got
            self.gain_by[act] += got

    # --- the week ----------------------------------------------------------------------------------------------------
    def kin_rich(self, world, q):
        c = world.cfg
        return any(world.kinship(q, o) > 0 and o.edible() > 2.0 * o.need(c, world.tick)
                   for o in world.people_near(q.loc, c.reach, exclude=q.id))

    def __call__(self, world, events):
        tick = world.tick - 1
        dec = tick // (10 * WPY)
        c = world.cfg
        d = self.decade[dec]
        living = world.living()
        ledger = getattr(world, "ledger", None) or []
        lrow = {r[0]: r for r in ledger}
        # the food economy
        adults = 0
        for p in living:
            if p.age(world.tick) >= 16 * WPY:
                adults += 1
        d["adult_weeks"] += adults
        d["living_weeks"] += len(living)
        for act, v in self.gain_by.items():
            d[f"gained:{act}"] += v
        eaten = 0.0
        held = 0.0
        for pid, need, held_before, deficit, fed in ((r[0], r[2], r[3], r[4], r[5]) for r in ledger):
            q = world.people.get(pid)
            if q is not None:
                eaten += max(0.0, held_before - q.edible())
            held += held_before
            d["fed_to_dependents"] += fed
        d["eaten"] += eaten
        if self.spoil_pre is not None:
            d["spoiled"] += max(0.0, self.spoil_pre - held)
        for ev in events:
            k = ev["k"]
            if k == "birth":
                d["births"] += 1
            elif k == "give":
                a, b = world.people.get(ev.get("a")), world.people.get(ev.get("b"))
                amt = float(ev.get("amount", 0.0))
                if a is not None and b is not None:
                    kind = "own_child" if b.id in a.children else ("kin" if world.kinship(a, b) > 0 else "other")
                    d[f"given:{kind}"] += amt
                    if b.age(world.tick) < 12 * WPY:
                        d["child_weeks_given"] += 1
            elif k == "put" and ev.get("thing") in ("food", "seeds"):
                d["stored"] += float(ev.get("amount", 0.0))
        # each living person's week
        for p in living:
            r = lrow.get(p.id)
            need = r[2] if r else p.need(c, tick)
            deficit = r[4] if r else 0.0
            y = p.age(world.tick) / WPY
            rec = {"t": tick, "age": round(y, 2), "health": round(p.health, 1), "held": round(p.edible(), 3),
                   "need": round(need, 3), "deficit": round(deficit, 3), "ate": round(max(0.0, (r[3] if r else 0.0)
                                                                                     - p.edible()), 3),
                   "act": p.last_action, "food_offered": bool(self.offered.get(p.id)),
                   "food_chosen": p.last_action in FOOD_ACTS, "gained": round(self.gained.get(p.id, 0.0), 3),
                   "kin_rich": self.kin_rich(world, p), "net_changed": self.netchg.get(p.id)}
            if y < 12:
                cg = world.people.get(p.caregiver) if p.caregiver else None
                if cg is not None and cg.alive:
                    cr = lrow.get(cg.id)
                    cg_pre = self.pre.get(cg.id, (cg.edible(), cg.need(c, tick)))
                    rec["cg"] = {"alive": True, "same_tile": cg.loc == p.loc, "held": round(cg_pre[0], 3),
                                 "need": round(cg_pre[1], 3), "fed_out": round(cr[5] if cr else 0.0, 3),
                                 "act": cg.last_action}
                    me_pre = self.pre.get(p.id, (p.edible(), p.need(c, tick)))
                    rec["want"] = round(max(0.0, me_pre[1] - me_pre[0]), 3)
                else:
                    rec["cg"] = {"alive": False}
            self.hist.setdefault(p.id, deque(maxlen=HIST)).append(rec)
            if r and deficit <= 0.05 and r[3] >= need and rec["ate"] < 0.5 * need:
                self.checks["held_but_did_not_eat"] += 1
        # deaths by cause; starvation deaths get their history and a matched survivor
        for ev in events:
            if ev["k"] != "death":
                continue
            age = ev.get("age", 99)
            grp = agegroup_years(age)
            cause = ev.get("cause", "?")
            d[f"death:{cause}:{grp}"] += 1
            if cause != "starvation":
                continue
            q = world.people.get(ev.get("a"))
            if q is None:
                continue
            row = {"t": tick, "age_group": grp, "weather": world.weather, "wet": world.sky.get("wet"),
                   "hard": world.sky.get("hard"), "season": world.season, "stash": self.stash_of(world, q.id),
                   "hist": list(self.hist.get(q.id, []))}
            self.starved.append(row)
            cands = [p for p in living if p.id != q.id and agegroup_years(p.age(world.tick) / WPY) == grp]
            order = self.rng.permutation(len(cands)) if cands else []
            snaps = [(cands[i].id, list(self.hist.get(cands[i].id, [])), self.stash_of(world, cands[i].id))
                     for i in list(order)[:N_CAND]]
            self.pending.append({"death_t": tick, "idx": len(self.starved) - 1, "snaps": snaps, "due": tick + 8})
        # survivors whose 8 weeks have passed
        keep = []
        for pd in self.pending:
            if tick < pd["due"]:
                keep.append(pd)
                continue
            pick = next(((pid, h, st) for pid, h, st in pd["snaps"]
                         if world.people.get(pid) is not None and world.people[pid].alive), None)
            self.survivors.append({"death_idx": pd["idx"], "t": pd["death_t"],
                                   "found": pick is not None, "hist": pick[1] if pick else None,
                                   "stash": pick[2] if pick else None})
        self.pending = keep
        self.pre = {}
        for pid in [k for k in self.hist if k not in world.people or not world.people[k].alive]:
            del self.hist[pid]
        self.offered.clear()
        self.netchg.clear()
        self.gained.clear()
        self.gain_by.clear()
        if ledger is not None and hasattr(world, "ledger"):
            world.ledger.clear()

    def stash_of(self, world, pid):
        """Food in the stashes p owns: read at the week of death (and the survivor's same week), not every week."""
        tot, n = 0.0, 0
        for t in world.stash_tiles() if hasattr(world, "stash_tiles") else _stash_tiles(world):
            for st in t.stash:
                if st[0] == pid:
                    tot += st[1] + st[2]
                    n += 1
        return {"stashes": n, "food": round(tot, 3)}

    def results(self):
        for pd in self.pending:               # worlds that ended within 8 weeks of a death
            self.survivors.append({"death_idx": pd["idx"], "t": pd["death_t"], "found": False, "hist": None,
                                   "stash": None, "ended": True})
        return {"decades": {str(k): dict(v) for k, v in sorted(self.decade.items())}, "starved": self.starved,
                "survivors": self.survivors, "checks": dict(self.checks)}


def _stash_tiles(world):
    tiles = getattr(world, "tiles", None)
    if isinstance(tiles, dict):
        return [t for t in tiles.values() if getattr(t, "stash", None)]
    if isinstance(tiles, list):
        flat = []
        for row in tiles:
            for t in (row if isinstance(row, list) else [row]):
                if getattr(t, "stash", None):
                    flat.append(t)
        return flat
    return []


def install():
    """Read-only wrappers: thought.steer (which acts were offered), brain_nb.rescore (did the network change the top
    option), the food acts (food gained by everyone on the tile), and the body phase (food held before it)."""
    from acl import thought, brain_nb, actions, biology
    if getattr(thought.steer, "_nb3a", False):
        return
    steer0, rescore0, body0 = thought.steer, brain_nb.rescore, biology.body_phase

    def steer(p, options):
        out = steer0(p, options)
        if CUR[0] is not None:
            CUR[0].on_steer(p, out)
        return out

    def rescore(world, p, options, near, hunger, fatigue, lw, base_):
        new = rescore0(world, p, options, near, hunger, fatigue, lw, base_)
        if CUR[0] is not None and p.nb is not None and new is not options and len(new) == len(options):
            CUR[0].on_rescore(world, p, options, new, lw, base_)
        return new

    def body_phase(world):
        if CUR[0] is not None:
            liv = list(world.living())
            CUR[0].spoil_pre = sum(q.food + q.seeds for q in liv)
            CUR[0].pre = {q.id: (q.edible(), q.need(world.cfg, world.tick)) for q in liv}
        return body0(world)

    def wrap(act, fn):
        def wrapped(world, p, target, eff):
            here = [q for q in world.living() if q.loc == p.loc]
            before = {q.id: q.edible() for q in here}
            out = fn(world, p, target, eff)
            if CUR[0] is not None:
                gains = {}
                for q in here:
                    g = q.edible() - before[q.id]
                    if g > 0:
                        gains[q.id] = g
                CUR[0].on_food_act(act, gains)
            return out
        return wrapped
    for act in FOOD_ACTS:
        actions.HANDLERS[act] = wrap(act, actions.HANDLERS[act])
    steer._nb3a = True
    thought.steer = steer
    brain_nb.rescore = rescore
    biology.body_phase = body_phase


def save_ckpt(w, nbobs, obs, path, meta):
    """The world, NB3's observer, this recorder, and the brain's working records (as run_nb3.save_ckpt)."""
    import pickle
    from acl import brain_nb2 as b2, brain_nb3 as b3
    me = id(w)
    rec = {name: {k[1]: v for k, v in d.items() if k[0] == me}
           for name, d in (("LAST", b2.LAST), ("CHOSEN", b2.CHOSEN), ("OBS", b2.OBS))}
    rec["APPR"] = {k[1]: v for k, v in b3.APPR.items() if k[0] == me}
    nbobs.w = obs.w = None
    blob = pickle.dumps({"meta": meta, "world": w.to_dict(), "nbobs": nbobs, "obs": obs, "b2": rec}, protocol=4)
    nbobs.w = obs.w = w
    tmp = Path(str(path) + ".tmp")
    tmp.write_bytes(blob)
    tmp.replace(path)


def load_ckpt(path):
    import pickle
    d = pickle.loads(Path(path).read_bytes())
    base.setup(CODE)
    from acl.world import World
    from acl import brain_nb2 as b2, brain_nb3 as b3
    w = World.from_dict(d["world"])
    for name, dd in (("LAST", b2.LAST), ("CHOSEN", b2.CHOSEN), ("OBS", b2.OBS)):
        for pid, v in d["b2"][name].items():
            dd[(id(w), pid)] = v
    for pid, v in d["b2"].get("APPR", {}).items():
        b3.APPR[(id(w), pid)] = v
    nbobs, obs = d["nbobs"], d["obs"]
    nbobs.w = obs.w = w
    P.CUR[:] = [nbobs]
    P.install()
    w.observers.append(nbobs)
    install()
    CUR[0] = obs
    w.ledger = []
    w.observers.append(obs)
    return d["meta"], w, nbobs, obs


def run_part(arm, seed, years, out, ckpt_dir, budget_min):
    """long-run's entry: start or continue one world; checkpoint when the budget is spent; the result at the end."""
    import time
    t0 = time.time()
    ckpt_dir = Path(ckpt_dir)
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    ck = ckpt_dir / f"{arm}_seed_{seed}.ckpt"
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    if ck.exists():
        meta, w, nbobs, obs = load_ckpt(ck)
        assert meta["code_hash"] == f0, "checkpoint from different code"
    else:
        meta = {"arm": arm, "seed": seed, "years": years, "code_hash": f0, "jobs": 0}
        w = P.make(seed, arm)
        P.install()
        nbobs = P.NB2Obs(w)
        w.observers.append(nbobs)
        install()
        obs = Autopsy(w, seed)
        CUR[0] = obs
        w.ledger = []
        w.observers.append(obs)
    meta["jobs"] += 1
    while w.tick < years * WPY:
        w.step()
        if not w.living():
            break
        if budget_min >= 0 and w.tick % WPY == 0 and (time.time() - t0) / 60.0 > budget_min:
            save_ckpt(w, nbobs, obs, ck, meta)
            print(f"{arm} seed {seed}: checkpoint at year {w.tick // WPY} (job {meta['jobs']})", flush=True)
            return
        if budget_min < 0 and w.tick == WPY:  # the zero check's forced break after one year
            save_ckpt(w, nbobs, obs, ck, meta)
            print(f"{arm} seed {seed}: checkpoint at year 1 (job {meta['jobs']})", flush=True)
            return
    finish(w, obs, arm, seed, f0, out, meta["jobs"])


def finish(w, obs, arm, seed, f0, out, jobs):
    prev_f = NB3_OUT / f"{arm}_seed_{seed}.json"
    prev = json.loads(prev_f.read_text()) if prev_f.exists() else {}
    same = base.world_hash(w) == prev.get("world_hash") and w.tick == prev.get("final_tick")
    res = {"arm": arm, "seed": seed, "nature": "code_nb3", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "same_as_nb3": same, "jobs": jobs, **obs.results()}
    out = Path(out or HERE / "output")
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, same as NB3: {same}", flush=True)


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = P.make(seed, arm)
    P.install()                                  # NB3's own observer too, so the replay is the same program
    nbobs = P.NB2Obs(w)
    w.observers.append(nbobs)
    install()
    obs = Autopsy(w, seed)
    CUR[0] = obs
    w.ledger = []
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    prev = json.loads((NB3_OUT / f"{arm}_seed_{seed}.json").read_text())
    same = base.world_hash(w) == prev["world_hash"] and w.tick == prev["final_tick"]
    res = {"arm": arm, "seed": seed, "nature": "code_nb3", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "same_as_nb3": same, **obs.results()}
    out = out or HERE / "output"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, same as NB3: {same}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "part":
        assert sys.argv[2] in ARMS
        run_part(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6], float(sys.argv[7]))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
