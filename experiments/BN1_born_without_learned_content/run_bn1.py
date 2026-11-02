"""BN1 — born without learned content (questions.md, frozen as `BN1-frozen`). A nature-change test in a copy:
`code_bn1` = `code_v11` + `newborn_values` (0 = v11). Arms v11 (c), z (1), x (2), sham (s), and reference v11 worlds
(r, only for the fixed cell weights). ES2's runner supplies the set-up, the habit-update replay and the realized
return G (`../ES2_realized_lookahead/run_es2.py`); BN1's observer adds:
  early     habit updates started at ages 52-103 weeks (the first year of habit learning), years 100-200:
            n, sum |q - G|, sum (q - G) by situation x action, apart for G closed by death
  births    every newborn's values checked against its arm's law (v11: half the parents' mean; z: all 0;
            x: a within-situation permutation of the inherited values); mismatches counted
  census    children's weeks and deaths, recipes known per adult (yearly)

  python experiments/BN1_born_without_learned_content/run_bn1.py zero
  python experiments/BN1_born_without_learned_content/run_bn1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.CODES["bn1"] = HERE / "code_bn1"
CODE = "bn1"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(21801, 21833))        # 32 new paired seeds, used by no study
REF_SEEDS = tuple(range(21901, 21909))    # 8 reference v11 worlds, only for the fixed cell weights
SMOKE_SEEDS = (9959, 9958)
ARMS = {"c": {**base.LP, "newborn_values": 0}, "z": {**base.LP, "newborn_values": 1},
        "x": {**base.LP, "newborn_values": 2}, "s": {**base.LP, "newborn_values": 0, "sham_draw": 1},
        "r": {**base.LP, "newborn_values": 0}}
JOBS = [f"{a}:{s}" for a in ("c", "z", "x", "s") for s in SEEDS] + [f"r:{s}" for s in REF_SEEDS]
OUT = HERE / "output"
EARLY = (52, 104)                         # ages in weeks: the first year of habit learning
CHILD = 16 * WPY


class BN1Obs(base.ES2Obs):
    def __init__(self, w):
        super().__init__(w)
        self.early = {"0": defaultdict(lambda: [0, 0.0, 0.0]), "1": defaultdict(lambda: [0, 0.0, 0.0])}
        self.yearly = defaultdict(lambda: [0, 0, 0])      # year -> [adults, recipes known by adults, children]

    def on_learn(self, world, p, i, before, after, r, fut):
        super().on_learn(world, p, i, before, after, r, fut)
        self.pending[p.id][-1].append(p.age(world.tick))

    def close(self, e, censored):
        super().close(e[:5], censored)
        key, q, acc, _, late, age = e
        if late and EARLY[0] <= age < EARLY[1]:
            c = self.early[str(censored)][key]
            c[0] += 1
            c[1] += abs(q - acc)
            c[2] += q - acc

    def newborn(self, world, child, mq, fq):
        """Check a newborn's values against its arm's law, right after birth (before any upbringing). The parents'
        values are taken just before the birth, since a mother who dies in childbirth loses hers (`die`)."""
        from acl.person import N_ACTIONS
        inherited = [0.25 * (a + b) for a, b in zip(mq, fq)]
        mode = world.cfg.newborn_values
        if mode == 0:
            ok = len(child.q) == len(inherited) and all(abs(a - b) < 1e-12 for a, b in zip(child.q, inherited))
        elif mode == 1:
            ok = all(v == 0.0 for v in child.q)
        else:
            ok = len(child.q) == len(inherited) and all(
                sorted(child.q[s:s + N_ACTIONS]) == sorted(inherited[s:s + N_ACTIONS])
                for s in range(0, len(inherited), N_ACTIONS))
        self.s["births_checked"] += 1
        if not ok:
            self.mismatch["newborn_law"] += 1

    def __call__(self, world, events):
        super().__call__(world, events)
        tick = world.tick - 1
        late = base.LATE[0] <= tick < base.LATE[1]
        if not late:
            return
        for ev in events:
            if ev["k"] == "death" and ev.get("age", 99) < 16:
                self.s["child_deaths"] += 1
        living = world.living()
        self.s["child_weeks"] += sum(1 for p in living if p.age(world.tick) < CHILD)
        if tick % WPY == WPY - 1:
            y = self.yearly[str(tick // WPY)]
            adults = [p for p in living if p.age(world.tick) >= CHILD]
            y[0] += len(adults)
            y[1] += sum(len(p.recipes) for p in adults)
            y[2] += len(living) - len(adults)

    def results(self):
        return {**super().results(), "early_fields": ["n", "sum_abs", "sum_signed"],
                "early": {k: dict(v) for k, v in self.early.items()},
                "yearly_fields": ["adults", "adult_recipes", "children"], "yearly": dict(self.yearly)}


def install(w, obs):
    base.install(w, obs)
    from acl import biology
    o_birth = biology.give_birth

    def give_birth(world, mother):
        if world is not w:
            return o_birth(world, mother)
        before = set(world.people)
        father = world.people.get(mother.pregnant)
        mq = list(mother.q)
        fq = list(father.q) if father and father.alive else list(mother.q)
        out = o_birth(world, mother)
        for cid in set(world.people) - before:
            obs.newborn(world, world.people[cid], mq, fq)
        return out
    biology.give_birth = give_birth


def hashrun(code, arm, seed, years, observe):
    base.LATE = (0, years * WPY)          # zero checks: every year counted
    base.setup(code)
    kw = dict(ARMS[arm])
    if code == "v11":
        kw.pop("newborn_values", None)
    w = base.make_world(seed, kw)
    obs = None
    if observe:
        obs = BN1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        extra = ":" + json.dumps({**obs.mismatch, "_updates": obs.s["updates"], "_births": obs.s["births_checked"]},
                                 sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def reload_check(seed):
    base.setup(CODE)
    from acl.world import World
    a = base.make_world(seed, ARMS["x"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for x in (a, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(a) == base.world_hash(b) and b.cfg.newborn_values == 2


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
    specs = [(code, arm, seed, years, obs) for seed, years in ((501, 20), (601, 60))
             for code, arm, obs in (("v11", "c", 0), ("bn1", "c", 0), ("bn1", "c", 1), ("bn1", "z", 0),
                                    ("bn1", "z", 1), ("bn1", "x", 0), ("bn1", "x", 1), ("bn1", "s", 0))]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        g = {(c, a, o): got[(c, a, sd, yr, o)] for c, a, sd, yr, o in specs if sd == seed}
        same = hs(g[("v11", "c", 0)]) == hs(g[("bn1", "c", 0)])
        ro = all(hs(g[("bn1", a, 0)]) == hs(g[("bn1", a, 1)]) for a in ("c", "z", "x"))
        acts = hs(g[("bn1", "z", 0)]) != hs(g[("bn1", "c", 0)]) and hs(g[("bn1", "x", 0)]) != hs(g[("bn1", "c", 0)])
        sham = hs(g[("bn1", "s", 0)]) != hs(g[("bn1", "c", 0)])
        infos = {a: json.loads(g[("bn1", a, 1)].split(":", 2)[2]) for a in ("c", "z", "x")}
        mism = {a: {k: v for k, v in i.items() if not k.startswith("_")} for a, i in infos.items()}
        births = {a: i["_births"] for a, i in infos.items()}
        t = same and ro and acts and sham and not any(any(m.values()) for m in mism.values()) \
            and all(b > 0 for b in births.values())
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_bn1 with newborn_values 0 = code_v11: {'yes' if same else 'NO'}; "
                     f"observer read-only (c, z, x): {'yes' if ro else 'NO'}; z and x act: {'yes' if acts else 'NO'}; "
                     f"the sham acts: {'yes' if sham else 'NO'}; mismatches (replay, newborn law): "
                     f"{ {a: m or 'none' for a, m in mism.items()} }; newborns checked {births}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm x, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_bn1 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = base.make_world(seed, ARMS[arm])
    obs = BN1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_bn1", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
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
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: every year counted; never study data
        assert sys.argv[2] in ARMS
        base.LATE = (0, int(sys.argv[4]) * WPY)
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
