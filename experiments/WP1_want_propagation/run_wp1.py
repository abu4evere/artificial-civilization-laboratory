"""WP1 — want propagation (questions.md, frozen as `WP1-frozen`). A nature-change test in a copy: `code_wp1` =
`code_v11` + `want_propagation` (0 = v11). Arms v11 (c), A1 (a1), A2 (a2), sham (s). ES2's runner supplies the set-up
(`../ES2_realized_lookahead/run_es2.py`); WP1's light observer records:
  kinds      every world-new kind made in play in years 100-195: inventor, and whether (and by whom, how soon) anyone
             makes it again within 260 weeks
  census     living and adult weeks, gathers, makes and nested makes by adults, recipes per adult (yearly), extinction

  python experiments/WP1_want_propagation/run_wp1.py zero
  python experiments/WP1_want_propagation/run_wp1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.CODES["wp1"] = HERE / "code_wp1"
CODE = "wp1"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(22201, 22233))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9919, 9918)
ARMS = {"c": {**base.LP, "want_propagation": 0}, "a1": {**base.LP, "want_propagation": 1},
        "a2": {**base.LP, "want_propagation": 2}, "s": {**base.LP, "want_propagation": 0, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
ADULT = 16 * WPY
WIN = 5 * WPY
LATE = [100 * WPY, 200 * WPY]


class WP1Obs:
    def __init__(self, w):
        self.w = w
        self.kinds = {}                                   # sig -> [tick, inventor, remade_by, weeks]
        self.s = Counter()
        self.yearly = {}
        self.mismatch = Counter()

    def nested(self, sig):
        from acl.matter import MATERIALS
        rec = self.w.knowledge.get(sig)
        if rec is None:
            return False
        r = rec["recipe"]
        if r.get("verb") == "bind":
            return any(x not in MATERIALS for x in r["parts"])
        return r.get("verb") == "heat" and r["part"] not in MATERIALS

    def invented(self, world, p, sig):
        t = world.tick
        if LATE[0] <= t and t + WIN <= LATE[1]:
            self.kinds[sig] = [t, p.id, None, None]

    def __call__(self, world, events):
        tick = world.tick - 1
        late = LATE[0] <= tick < LATE[1]
        for ev in events:
            k = ev["k"]
            if k == "make":
                sig = ev.get("thing")
                e = self.kinds.get(sig)
                if e is not None and e[2] is None and e[0] < tick <= e[0] + WIN:
                    e[2] = "inventor" if ev.get("a") == e[1] else "other"
                    e[3] = tick - e[0]
                if late:
                    q = world.people.get(ev.get("a"))
                    if q is not None and q.age(world.tick) >= ADULT:
                        self.s["adult_makes"] += 1
                        self.s["adult_nested_makes"] += self.nested(sig)
            elif k == "gather" and late:
                q = world.people.get(ev.get("a"))
                if q is not None and q.age(world.tick) >= ADULT:
                    self.s["adult_gathers"] += 1
        if late:
            living = world.living()
            self.s["living_weeks"] += len(living)
            self.s["adult_weeks"] += sum(1 for p in living if p.age(world.tick) >= ADULT)
            if tick % WPY == WPY - 1:
                adults = [p for p in living if p.age(world.tick) >= ADULT]
                self.yearly[str(tick // WPY)] = [len(adults), sum(len(p.recipes) for p in adults)]

    def results(self):
        k = list(self.kinds.values())
        return {"kinds_fields": ["first_tick", "inventor", "remade_by", "weeks"], "kinds": k,
                "n_kinds": len(k), "n_remade": sum(1 for e in k if e[2] is not None),
                "sums": dict(self.s), "yearly": self.yearly, "mismatch": dict(self.mismatch)}


def install(w, obs):
    from acl import knowhow
    o_rem = knowhow.remember_recipe

    def remember_recipe(world, p, sig, recipe, how, source=None, props=None, meant=None):
        new = sig not in world.knowledge
        out = o_rem(world, p, sig, recipe, how, source, props, meant)
        if world is w and new and how == "made":
            obs.invented(world, p, sig)
        return out
    knowhow.remember_recipe = remember_recipe


def hashrun(code, arm, seed, years, observe):
    LATE[0], LATE[1] = 0, years * WPY       # zero checks: every year counted
    base.setup(code)
    kw = dict(ARMS[arm])
    if code == "v11":
        kw.pop("want_propagation", None)
    w = base.make_world(seed, kw)
    obs = None
    if observe:
        obs = WP1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results()
        extra = ":" + json.dumps({"_kinds": r["n_kinds"], "_remade": r["n_remade"],
                                  "_makes": obs.s["adult_makes"]}, sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def reload_check(seed):
    base.setup(CODE)
    from acl.world import World
    a = base.make_world(seed, ARMS["a2"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for x in (a, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(a) == base.world_hash(b) and b.cfg.want_propagation == 2


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
             for code, arm, obs in (("v11", "c", 0), ("wp1", "c", 0), ("wp1", "c", 1), ("wp1", "a1", 0),
                                    ("wp1", "a1", 1), ("wp1", "a2", 0), ("wp1", "a2", 1), ("wp1", "s", 0))]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        g = {(c, a, o): got[(c, a, sd, yr, o)] for c, a, sd, yr, o in specs if sd == seed}
        same = hs(g[("v11", "c", 0)]) == hs(g[("wp1", "c", 0)])
        ro = all(hs(g[("wp1", a, 0)]) == hs(g[("wp1", a, 1)]) for a in ("c", "a1", "a2"))
        acts = all(hs(g[("wp1", a, 0)]) != hs(g[("wp1", "c", 0)]) for a in ("a1", "a2", "s"))
        a12 = hs(g[("wp1", "a1", 0)]) != hs(g[("wp1", "a2", 0)])
        info = {a: json.loads(g[("wp1", a, 1)].split(":", 2)[2]) for a in ("c", "a1", "a2")}
        t = same and ro and acts and a12
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_wp1 with want_propagation 0 = code_v11: {'yes' if same else 'NO'}; "
                     f"observer read-only (c, a1, a2): {'yes' if ro else 'NO'}; A1, A2 and the sham act: "
                     f"{'yes' if acts else 'NO'}; A1 and A2 differ: {'yes' if a12 else 'NO'}; kinds / remade / adult "
                     f"makes {info}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm A2, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_wp1 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = base.make_world(seed, ARMS[arm])
    obs = WP1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_wp1", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, kinds {res['n_kinds']}, remade {res['n_remade']}", flush=True)


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
        LATE[0], LATE[1] = 0, int(sys.argv[4]) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
