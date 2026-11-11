"""NB2-A: why did NB2's people die out? An exact replay of NB2's worlds with read-only recorders (questions.md,
NB2A-frozen). Code: NB2's code_nb2, unchanged. Arms c, s, n; seeds 25601-25616; each world to its end.
Validity: each replay must end with the world fingerprint of NB2's phase-1 result.

  python experiments/NB2A_autopsy/run_nb2a.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import json  # noqa: E402
import sys  # noqa: E402
from collections import Counter, defaultdict  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "NB2_connected_brain"))
import run_nb2 as P  # noqa: E402

base = P.base
WPY, YEARS = P.WPY, 600
SEEDS = P.SEEDS
ARMS = {a: P.ARMS[a] for a in ("c", "s", "n")}
CODE = P.CODE
NB2_OUT = HERE.parent / "NB2_connected_brain" / "output"


def agegroup(p, tick):
    y = p.age(tick) / WPY
    return "u12" if y < 12 else ("12_15" if y < 16 else "16+")


class Autopsy:
    def __init__(self, w):
        self.w = w
        self.decade = defaultdict(Counter)      # decade -> counts
        self.attacks = []                       # one row per attack
        self.starved = []                       # one row per death by starvation
        self.kid_acts = defaultdict(Counter)    # "decade:group" -> action -> weeks
        self.last8 = defaultdict(list)          # pid -> the last 8 weeks' actions

    def attack_row(self, world, p, q, source):
        tick = world.tick
        from acl.mind import hunger_of
        r = p.rel.get(q.id)
        grudge = r.grudge if r is not None else 0.0
        return {"t": tick, "source": source, "a_age": agegroup(p, tick), "b_age": agegroup(q, tick),
                "kin": round(world.kinship(p, q), 3), "partner": p.partner == q.id, "grudge": round(grudge, 3),
                "old_brain_offers": grudge > 0.15, "hunger": round(hunger_of(world, p, 0.0), 3),
                "anger": round(p.anger, 3), "temper": round(p.genes["temper"], 3)}

    def __call__(self, world, events):
        tick = world.tick - 1
        dec = tick // (10 * WPY)
        living = world.living()
        d = self.decade[dec]
        if tick % WPY == WPY - 1:
            d["pop_yearends"] += len(living)
        for ev in events:
            k = ev["k"]
            if k == "birth":
                d["births"] += 1
            elif k == "death":
                q = world.people.get(ev.get("a"))
                age = ev.get("age", 99)
                grp = "u12" if age < 12 else ("12_15" if age < 16 else "16+")
                cause = ev.get("cause", "?")
                d[f"death:{cause}:{grp}"] += 1
                if cause == "starvation" and q is not None:
                    need = q.need(world.cfg, tick) or 1.0
                    kin_rich = any(world.kinship(q, o) > 0 and o.edible() > 2.0 * o.need(world.cfg, tick)
                                   for o in world.people_near(q.loc, world.cfg.reach, exclude=q.id))
                    acts = self.last8.get(q.id, [])
                    self.starved.append({"t": tick, "age": grp, "food_held": round(q.edible() / need, 3),
                                         "kin_with_surplus_near": kin_rich,
                                         "forage_share_8w": round(sum(1 for a in acts if a == "forage") / len(acts), 3)
                                         if acts else None})
        for p in living:
            a = p.last_action
            if a:
                h = self.last8[p.id]
                h.append(a)
                if len(h) > 8:
                    h.pop(0)
            y = p.age(world.tick) / WPY
            if 3 <= y < 16 and a:
                self.kid_acts[f"{dec}:{'3_11' if y < 12 else '12_15'}"][a] += 1

    def results(self):
        return {"decades": {str(k): dict(v) for k, v in sorted(self.decade.items())}, "attacks": self.attacks,
                "starved": self.starved, "kid_acts": {k: dict(v) for k, v in self.kid_acts.items()}}


def install(obs_ref):
    """Read-only wrappers around the attack: the chosen attack (the action table) and the retaliation after a noticed
    theft (the module function). They read the state before the attack, call the original, and read the outcome."""
    from acl import actions
    if getattr(actions._attack, "_nb2a", False):
        return
    orig = actions._attack

    def make(source):
        def wrapped(world, p, target, eff):
            o = obs_ref[0]
            q = world.people.get(target)
            row = o.attack_row(world, p, q, source) if (o is not None and q is not None) else None
            out = orig(world, p, target, eff)
            if row is not None:
                row["killed_target"] = not q.alive
                row["killed_attacker"] = not p.alive
                o.attacks.append(row)
            return out
        wrapped._nb2a = True
        return wrapped
    actions.HANDLERS["attack"] = make("chosen")
    actions._attack = make("retaliation")


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = P.make(seed, arm)
    P.install()                                  # NB2's own observer too, so the replay is the same program
    nbobs = P.NB2Obs(w)
    w.observers.append(nbobs)
    ref = [None]
    install(ref)
    obs = Autopsy(w)
    ref[0] = obs
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    prev = json.loads((NB2_OUT / f"{arm}_seed_{seed}.json").read_text())
    same = base.world_hash(w) == prev["world_hash"] and w.tick == prev["final_tick"]
    res = {"arm": arm, "seed": seed, "nature": "code_nb2", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "same_as_nb2": same, **obs.results()}
    out = out or HERE / "output"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, same as NB2: {same}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
