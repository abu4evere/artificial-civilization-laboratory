"""NA1 — who actually gets a chance to learn? (questions.md, frozen as `NA1-frozen`). Read-only: live nature v7
(`code_v7`) unchanged, with a weekly observer and two read-only wrappers (`knowhow.remember_recipe`,
`information.hear_how`) that read state before and after and call the original unchanged.

For every useful kind (a factor > 1 for any use) it follows, per non-knower aged 4+, the stages co-present (within
reach of a living knower), talked, offered, took, made, passed; once with the inventor (while alive) and once with any
knower. It also keeps the A→B→C ratchet ledger.

  python experiments/NA1_cultural_network/run_na1.py zero
  python experiments/NA1_cultural_network/run_na1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODE = EXP / "NV7_nature_v7" / "code_v7"
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(18501, 18533))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9953, 9952)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
ARMS = {"lp": {"founders": 80, "width": 80, "height": 80}}
JOBS = [f"lp:{s}" for s in SEEDS]
USES = ("forage", "hunt", "wood", "stone", "fiber", "fight", "carry", "cold")
ERAS = (50, 100, 200)
MIN_AGE = 4 * WPY
STAGES = ("cop", "talk", "off", "took")


def era_of(tick):
    y = tick / WPY
    for i, e in enumerate(ERAS):
        if y < e:
            return i
    return len(ERAS) - 1


def setup():
    sys.path.insert(0, str(CODE))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **{**V7, **kw}))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def rng_state(w):
    return hashlib.sha256(repr(w.rng.getstate()).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODE / "acl")


def maxf(props):
    from acl.matter import factor
    if not props or "edge" not in props:
        return 1.0
    return max(factor(props, u) for u in USES)


class NA1Obs:
    def __init__(self, w):
        self.w = w
        self.kinds = {}                       # sig -> record
        self.fac = {}                         # sig -> best factor (cached)
        self.acq = defaultdict(dict)          # pid -> sig -> (route, source)
        self.ratchet = []                     # [tick, B, A, k, k2, f_k, f_k2, completed tick, C]
        self.pending = defaultdict(list)      # k2 -> indices into ratchet
        self.pop = Counter()
        self.mismatch = Counter()
        for p in w.living():
            for sig in p.recipes:
                self._kind(sig, -1, None, True)
                self.acq[p.id][sig] = ("founding", None)

    def factor(self, sig):
        if sig not in self.fac:
            props = (self.w.knowledge.get(sig) or {}).get("props")
            if props is None:
                return 1.0
            self.fac[sig] = maxf(props)
        return self.fac[sig]

    def _kind(self, sig, tick, inventor, founder):
        k = self.kinds.get(sig)
        if k is None:
            k = self.kinds[sig] = {"first": tick, "inv": inventor, "founder": founder, "inv_death": None,
                                   **{f"{s}_i": set() for s in STAGES}, **{f"{s}_a": set() for s in STAGES},
                                   "made": set(), "passed": set(), "knowers_ever": set(), "variant": set()}
        return k

    def _add(self, k, stage, pid, by_inventor):
        k[f"{stage}_a"].add(pid)
        if by_inventor:
            k[f"{stage}_i"].add(pid)

    # -- wrappers --
    def on_remember(self, world, p, sig, how, source, existed, gained):
        if not gained:
            return
        if how in ("made", "heated"):
            route = "rediscovered" if existed else "invented"
        elif how in ("taught", "copied", "read"):
            route = how
        else:
            route = "other"
        self.acq[p.id][sig] = (route, source)
        if route == "invented":
            if self.factor(sig) > 1.0:
                self._kind(sig, world.tick, p.id, p.birth < 0)
            # the ratchet: B improves a kind B learned socially
            rec = p.recipes.get(sig) or {}
            parts = list(rec.get("parts", ())) + ([rec.get("part")] if rec.get("verb") == "heat" else [])
            for part in parts:
                got = self.acq[p.id].get(part)
                if got and got[0] in ("taught", "copied", "read") and self.factor(sig) > self.factor(part):
                    self.pending[sig].append(len(self.ratchet))
                    self.ratchet.append([world.tick, p.id, got[1], part, sig, round(self.factor(part), 4),
                                         round(self.factor(sig), 4), None, None])
        elif route in ("taught", "copied", "read"):
            for i in self.pending.get(sig, ()):
                r = self.ratchet[i]
                if r[7] is None and p.id != r[1]:
                    r[7], r[8] = world.tick, p.id

    def on_lesson(self, world, learner, teacher, meant, before, after):
        k = self.kinds.get(meant)
        if k is None or learner.age(world.tick) < MIN_AGE:
            return
        if meant in before:
            return                                            # not a non-knower of this kind
        inv = teacher.id == k["inv"]
        for stage in ("cop", "talk", "off"):                  # a lesson is given in a talk, within reach
            self._add(k, stage, learner.id, inv)
        if meant in after:
            self._add(k, "took", learner.id, inv)
            if teacher.id in k["took_a"]:
                k["passed"].add(teacher.id)
        elif after - before:
            k["variant"].add(learner.id)                      # operational note 1: took something, not this kind
        elif meant in learner.recipes:
            self.mismatch["took_outside_lesson"] += 1

    # -- the week --
    def __call__(self, world, events):
        tick = world.tick - 1
        living = world.living()
        alive = {p.id: p for p in living}
        era = era_of(tick)
        self.pop[f"{era}|pw"] += len(living)
        reach = world.cfg.reach
        for k in self.kinds.values():
            if k["inv"] and k["inv_death"] is None and k["inv"] not in alive:
                k["inv_death"] = tick
        useful = {}
        for p in living:
            for sig in p.recipes:
                if sig in self.kinds:
                    useful.setdefault(p.id, []).append(sig)
                    self.kinds[sig]["knowers_ever"].add(p.id)
        near_sum = 0
        for p in living:
            if p.age(world.tick) < MIN_AGE:
                continue
            near = world.people_near(p.loc, reach, exclude=p.id)
            near_sum += len(near)
            for q in near:
                for sig in useful.get(q.id, ()):
                    if sig not in p.recipes:
                        k = self.kinds[sig]
                        self._add(k, "cop", p.id, q.id == k["inv"])
        self.pop[f"{era}|near"] += near_sum
        for e in events:
            kd = e.get("k")
            if kd == "talk" and e.get("b"):
                a, b = alive.get(e["a"]), alive.get(e["b"])
                if a is None or b is None:
                    continue
                for x, y in ((a, b), (b, a)):
                    if y.age(world.tick) < MIN_AGE:
                        continue
                    for sig in useful.get(x.id, ()):
                        if sig not in y.recipes:
                            k = self.kinds[sig]
                            self._add(k, "cop", y.id, x.id == k["inv"])
                            self._add(k, "talk", y.id, x.id == k["inv"])
            elif kd in ("make", "play") and e.get("thing") in self.kinds:
                k = self.kinds[e["thing"]]
                if e["a"] in k["took_a"]:
                    k["made"].add(e["a"])

    def results(self):
        kinds = []
        for sig, k in self.kinds.items():
            for s in STAGES[1:]:
                prev = STAGES[STAGES.index(s) - 1]
                if not k[f"{s}_a"] <= k[f"{prev}_a"]:
                    self.mismatch["containment"] += 1
            kinds.append([k["first"], int(k["founder"]), era_of(max(k["first"], 0)), k["inv_death"],
                          round(self.factor(sig), 4), len(k["knowers_ever"]),
                          *[len(k[f"{s}_i"]) for s in STAGES], *[len(k[f"{s}_a"]) for s in STAGES],
                          len(k["made"]), len(k["passed"]), len(k["variant"])])
        return {"kinds": kinds, "ratchet": self.ratchet, "pop": dict(self.pop), "mismatch": dict(self.mismatch)}


def install(w, obs):
    from acl import information, knowhow
    orig_rem, orig_hear = knowhow.remember_recipe, information.hear_how

    def remember_recipe(world, p, sig, recipe, how, source=None, props=None, meant=None):
        if world is not w:
            return orig_rem(world, p, sig, recipe, how, source, props, meant)
        existed = sig in world.knowledge
        had = sig in p.recipes
        out = orig_rem(world, p, sig, recipe, how, source, props, meant)
        obs.on_remember(world, p, sig, how, source, existed, (not had) and sig in p.recipes)
        return out

    def hear_how(world, learner, teacher, meant, recipe, claim, parent, part_lesson=False):
        if world is not w:
            return orig_hear(world, learner, teacher, meant, recipe, claim, parent, part_lesson)
        before = set(learner.recipes)
        out = orig_hear(world, learner, teacher, meant, recipe, claim, parent, part_lesson)
        obs.on_lesson(world, learner, teacher, meant, before, set(learner.recipes))
        return out

    knowhow.remember_recipe = remember_recipe
    information.hear_how = hear_how


def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = NA1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        res = obs.results()
        extra = ":" + json.dumps({**res["mismatch"], "_kinds": len(res["kinds"]),
                                  "_took": sum(k[13] for k in res["kinds"]), "_ratchet": len(res["ratchet"])},
                                 sort_keys=True, separators=(",", ":"))
    return world_hash(w) + ":" + rng_state(w) + extra


def reload_check(seed):
    setup()
    from acl.world import World
    a = make_world(seed, ARMS["lp"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for x in (a, b):
        for _ in range(5 * WPY):
            x.step()
    return world_hash(a) == world_hash(b)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for seed, years in ((501, 20), (601, 60)):
        a = call("hashrun", "lp", seed, years, 1)
        b = call("hashrun", "lp", seed, years, 0)
        same = a.split(":")[:2] == b.split(":")[:2]
        info = json.loads(a.split(":", 2)[2]) if a.count(":") >= 2 else {"?": 1}
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = same and not any(mism.values()) and info.get("_kinds", 0) > 0 and info.get("_took", 0) > 0
        ok &= t
        lines.append(f"arm lp, seed {seed}, {years} years: identical with and without the observer (state and random "
                     f"numbers): {'yes' if same else 'NO'}; internal mismatches: {mism or 'none'}; useful kinds "
                     f"{info.get('_kinds')}, lessons taken {info.get('_took')}, ratchet entries {info.get('_ratchet')}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm lp, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_v7 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = NA1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v7", "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "world_hash": world_hash(w), **obs.results()}
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
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "fp":
        setup()
        print(fingerprint())
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
