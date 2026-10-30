"""AG1 — ageing anchored to forager evidence (questions.md, frozen as `AG1-frozen`). A calibration study on nature v9:
`code_v9` unchanged; each arm changes one existing setting, `mortality_base`. Arms v (v9), b (the !Kung step),
a (the forager average), x (sham). A read-only observer reads each week's events and the living: every death's age and
cause, person-weeks by age band, and LC1's yearly census.

  python experiments/AG1_ageing_anchor/run_ag1.py zero
  python experiments/AG1_ageing_anchor/run_ag1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODE = EXP / "NV9_nature_v9" / "code_v9"
OUT = HERE / "output"
WPY, YEARS = 52, 1000
SEEDS = tuple(range(20501, 20521))        # 20 new paired seeds, used by no study
SMOKE_SEEDS = (9989, 9988)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
V9 = {**V7, "ground_items": 1, "curiosity_pull": 1}       # nature v9's settings, explicit (as LS2)
LP = {"founders": 80, "width": 80, "height": 80}
B_BASE = 1.5e-5 * 0.0072 / 0.0249          # the !Kung at age 40 (SA1 note's table), ACL's rate unchanged
A_BASE = 1.47e-4 / 52                       # the forager average a3 (SA1 note), per week
ARMS = {"v": {**LP}, "b": {**LP, "mortality_base": B_BASE}, "a": {**LP, "mortality_base": A_BASE},
        "x": {**LP, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
BANDS = ((0, 16), (16, 30), (30, 45), (45, 60), (60, 70), (70, 200))
FIELDS = ["year", "living", "adults", "makes", "items_adults", "wb_adults_20_40", "wb_craft_sum_20_40", "aged_60"]


def setup():
    sys.path.insert(0, str(CODE))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **{**V9, **kw}))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def rng_state(w):
    return hashlib.sha256(repr(w.rng.getstate()).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODE / "acl")


def band_of(age_years):
    for i, (lo, hi) in enumerate(BANDS):
        if lo <= age_years < hi:
            return i
    return len(BANDS) - 1


class AG1Obs:
    """Read-only: called after each week with that week's events; looks at the living, changes nothing."""

    def __init__(self, w):
        self.w = w
        self.deaths = []                     # [tick, age in years, cause, generation]
        self.pw = {}                         # century -> [person-weeks per band]
        self.makes = 0
        self.census = []
        self.mismatch = Counter()

    def __call__(self, world, events):
        tick = world.tick - 1                # the week just lived
        for ev in events:
            if ev["k"] == "make":
                self.makes += 1
            elif ev["k"] == "death":
                self.deaths.append([ev["t"], ev.get("age"), ev.get("cause"), ev.get("generation")])
        living = world.living()
        row = self.pw.setdefault(tick // (100 * WPY), [0] * len(BANDS))
        for p in living:
            row[band_of(p.years(world.tick))] += 1
        if tick % WPY == WPY - 1:
            adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
            wb = [p for p in living if p.generation > 0 and 20 * WPY <= p.age(world.tick) < 41 * WPY]
            self.census.append([tick // WPY, len(living), len(adults), self.makes, sum(len(p.items) for p in adults),
                                len(wb), sum(p.skills["crafting"] for p in wb),
                                sum(1 for p in living if p.years(world.tick) >= 60)])
            self.makes = 0

    def results(self):
        dead = sum(1 for p in self.w.people.values() if not p.alive)
        if dead != len(self.deaths):
            self.mismatch["deaths_vs_dead"] += 1
        return {"deaths": self.deaths, "person_weeks": {str(k): v for k, v in sorted(self.pw.items())},
                "bands": BANDS, "census_fields": FIELDS, "census": self.census, "mismatch": dict(self.mismatch)}


def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = AG1Obs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        res = obs.results()
        extra = ":" + json.dumps({**res["mismatch"], "_deaths": len(res["deaths"])}, sort_keys=True,
                                 separators=(",", ":"))
    return world_hash(w) + ":" + rng_state(w) + extra


def reload_check(seed):
    setup()
    from acl.world import World
    a = make_world(seed, ARMS["a"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for x in (a, b):
        for _ in range(5 * WPY):
            x.step()
    return world_hash(a) == world_hash(b) and abs(b.cfg.mortality_base - A_BASE) < 1e-15


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.split()[-1]

    def hs(x):
        return x.split(":")[:2]
    from concurrent.futures import ThreadPoolExecutor
    specs = [(arm, seed, years, obs) for seed, years in ((501, 20), (601, 60))
             for arm, obs in (("v", 0), ("v", 1), ("a", 0), ("a", 1), ("b", 0), ("x", 0))]
    with ThreadPoolExecutor(6) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    lines, ok = [], True
    for seed, years in ((501, 20), (601, 60)):
        g = {(a, o): v for (a, s, y, o), v in got.items() if s == seed and y == years}
        ro = hs(g[("v", 1)]) == hs(g[("v", 0)]) and hs(g[("a", 1)]) == hs(g[("a", 0)])
        acts_a = hs(g[("a", 0)]) != hs(g[("v", 0)])
        acts_b = hs(g[("b", 0)]) != hs(g[("v", 0)])
        sham = hs(g[("x", 0)]) != hs(g[("v", 0)])
        infos = [json.loads(g[(a, 1)].split(":", 2)[2]) for a in ("v", "a")]
        mism = {k: v for i in infos for k, v in i.items() if not k.startswith("_")}
        t = ro and sham and not any(mism.values()) and (years < 60 or (acts_a and acts_b))
        ok &= t
        lines.append(f"seed {seed}, {years} years: observer read-only (arms v and a): {'yes' if ro else 'NO'}; "
                     f"arm a acts: {'yes' if acts_a else 'no'}; arm b acts: {'yes' if acts_b else 'no'} "
                     f"(required by 60 years); the sham acts: {'yes' if sham else 'NO'}; observer deaths equal the "
                     f"world's dead (v, a): {'yes' if not mism else 'NO ' + str(mism)}; deaths seen (v, a): "
                     f"{[i.get('_deaths') for i in infos]}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm a, seed 501: saved at year 10 and reloaded, continues exactly to year 15, with the anchored "
                 f"setting kept: {'yes' if t else 'NO'}")
    lines.append(f"code_v9 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = AG1Obs(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v9", "mortality_base": w.cfg.mortality_base, "code_hash": f0,
           "code_hash_after": fingerprint(), "final_tick": w.tick, "extinct": not w.living(),
           "world_hash": world_hash(w), **obs.results()}
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
