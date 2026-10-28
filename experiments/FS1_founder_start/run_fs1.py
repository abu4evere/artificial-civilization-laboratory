"""FS1 — is the erosion the founders' head start wearing off? (questions.md, frozen as `FS1-frozen`).
Code `code_fs1` = `code_v8` + `founder_skill` (v8_to_fs1.diff). Arms: t (today), z (founders' skills all 0),
c (founders' crafting 0), x (sham). A read-only observer takes a yearly census and counts the law's `make` events.

  python experiments/FS1_founder_start/run_fs1.py zero
  python experiments/FS1_founder_start/run_fs1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"fs1": HERE / "code_fs1", "v8": EXP / "NV8_nature_v8" / "code_v8"}
CODE = CODES["fs1"]
OUT = HERE / "output"
WPY, YEARS = 52, 500
SEEDS = tuple(range(19901, 19933))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9961, 9960)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
LP = {"founders": 80, "width": 80, "height": 80}
ARMS = {"t": {**LP}, "z": {**LP, "founder_skill": "none"}, "c": {**LP, "founder_skill": "no_crafting"},
        "x": {**LP, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
AGES = (10, 20, 30, 40)
LATE = (300, 500)                         # years 300-499: the census years read for the late state


def setup(code="fs1"):
    sys.path.insert(0, str(CODES[code]))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


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


def fingerprint(code="fs1"):
    from run_e7 import code_hash
    return code_hash(CODES[code] / "acl")


class FS1Obs:
    """Yearly census, at each year's end. Reads people only; counts `make` events."""
    FIELDS = ["year", "living", "adults", "wb_adults_20_40", "wb_craft_sum_20_40", "adult_craft_sum", "items_adults",
              "makes"]

    def __init__(self, w):
        self.w = w
        self.makes = 0
        self.census = []
        self.by_age = {a: [0.0, 0] for a in AGES}    # world-born, years 300-499: [summed crafting skill, people]

    def __call__(self, world, events):
        tick = world.tick - 1
        self.makes += sum(1 for ev in events if ev["k"] == "make")
        if tick % WPY != WPY - 1:
            return
        year = tick // WPY
        living = world.living()
        adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
        wb = [p for p in living if p.generation > 0 and 20 * WPY <= p.age(world.tick) < 41 * WPY]
        self.census.append([year, len(living), len(adults), len(wb), sum(p.skills["crafting"] for p in wb),
                            sum(p.skills["crafting"] for p in adults), sum(len(p.items) for p in adults), self.makes])
        self.makes = 0
        if LATE[0] <= year < LATE[1]:
            for p in living:
                a = p.age(world.tick) // WPY
                if p.generation > 0 and a in self.by_age:
                    self.by_age[a][0] += p.skills["crafting"]
                    self.by_age[a][1] += 1

    def results(self):
        return {"census_fields": self.FIELDS, "census": self.census,
                "skill_by_age": {str(a): v for a, v in self.by_age.items()}}


def founders_view(w, with_skills):
    """Every founder's attributes at week 0 (skills only if asked)."""
    out = []
    for p in sorted(w.people.values(), key=lambda q: q.id):
        d = {"id": p.id, "name": p.name, "sex": p.sex, "birth": p.birth, "gen": p.generation, "genes": p.genes,
             "loc": list(p.loc), "food": p.food, "rel": sorted((k, r.affection, r.trust, r.familiarity)
                                                               for k, r in p.rel.items())}
        if with_skills:
            d["skills"] = p.skills
        out.append(d)
    return out


def startcheck(seed):
    """Only the founders' skills differ at the start: identity of everything else, and of the random state."""
    setup()
    w = {a: make_world(seed, ARMS[a]) for a in ("t", "z", "c")}
    same = all(json.dumps(founders_view(w[a], False), sort_keys=True) == json.dumps(founders_view(w["t"], False),
                                                                                    sort_keys=True) for a in "zc")
    rng = rng_state(w["z"]) == rng_state(w["t"]) == rng_state(w["c"])
    zt = all(all(v == 0.0 for v in p.skills.values()) for p in w["z"].people.values())
    ct = all(p.skills["crafting"] == 0.0 and p.skills["foraging"] == w["t"].people[p.id].skills["foraging"]
             and p.skills["hunting"] == w["t"].people[p.id].skills["hunting"] for p in w["c"].people.values())
    tt = all(0.2 <= v <= 0.4 for p in w["t"].people.values() for v in p.skills.values())
    return same and rng and zt and ct and tt


def hashrun(code, arm, seed, years, observe):
    setup(code)
    kw = dict(ARMS[arm])
    if code == "v8":
        kw.pop("founder_skill", None)
    w = make_world(seed, kw)
    obs = None
    if observe:
        obs = FS1Obs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        res = obs.results()
        extra = ":" + json.dumps({"_years": len(res["census"]), "_makes": sum(r[7] for r in res["census"])},
                                 sort_keys=True, separators=(",", ":"))
    return world_hash(w) + ":" + rng_state(w) + extra


def reload_check(seed, arm):
    setup()
    from acl.world import World
    a = make_world(seed, ARMS[arm])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for x in (a, b):
        for _ in range(5 * WPY):
            x.step()
    return world_hash(a) == world_hash(b) and b.cfg.founder_skill == ARMS[arm].get("founder_skill", "all")


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
             for code, arm, obs in (("v8", "t", 0), ("fs1", "t", 0), ("fs1", "t", 1), ("fs1", "z", 0),
                                    ("fs1", "z", 1), ("fs1", "c", 0), ("fs1", "x", 0))]
    with ThreadPoolExecutor(7) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        g = {(c, a, o): v for (c, a, s, y, o), v in got.items() if s == seed and y == years}
        same_v8 = hs(g[("v8", "t", 0)]) == hs(g[("fs1", "t", 0)])
        ro = hs(g[("fs1", "t", 1)]) == hs(g[("fs1", "t", 0)]) and hs(g[("fs1", "z", 1)]) == hs(g[("fs1", "z", 0)])
        z_acts = hs(g[("fs1", "z", 0)]) != hs(g[("fs1", "t", 0)])
        c_acts = hs(g[("fs1", "c", 0)]) != hs(g[("fs1", "t", 0)])
        sham = hs(g[("fs1", "x", 0)]) != hs(g[("fs1", "t", 0)])
        info = json.loads(g[("fs1", "t", 1)].split(":", 2)[2])
        t = same_v8 and ro and z_acts and c_acts and sham and info.get("_years") == years
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_fs1 with founder_skill 'all' equals code_v8: "
                     f"{'yes' if same_v8 else 'NO'}; observer read-only (arms t and z): {'yes' if ro else 'NO'}; "
                     f"z acts: {'yes' if z_acts else 'NO'}; c acts: {'yes' if c_acts else 'NO'}; the sham acts: "
                     f"{'yes' if sham else 'NO'}; census years {info.get('_years')}, make events (t) "
                     f"{info.get('_makes')}")
    for seed in (501, 601):
        r = subprocess.run(me + ["start", str(seed)], capture_output=True, text=True)
        t = r.stdout.split()[-1:] == ["True"]
        ok &= t
        lines.append(f"seed {seed}: at week 0 only the founders' skills differ between t, z and c (ids, names, sexes, "
                     f"ages, genes, places, food, relations and the random state identical; z all 0; c crafting 0, "
                     f"other skills as t; t in 0.2-0.4): {'yes' if t else 'NO'}")
    for arm in ("t", "z"):
        r = subprocess.run(me + ["reload", "501", arm], capture_output=True, text=True)
        t = r.stdout.split()[-1:] == ["True"]
        ok &= t
        lines.append(f"arm {arm}, seed 501: saved at year 10 and reloaded, continues exactly to year 15: "
                     f"{'yes' if t else 'NO'}")
    lines.append(f"code_fs1 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = FS1Obs(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v8 + founder_skill (FS1)", "code_hash": f0,
           "code_hash_after": fingerprint(), "final_tick": w.tick, "extinct": not w.living(),
           "world_hash": world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "start":
        print(startcheck(int(sys.argv[2])))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2]), sys.argv[3]))
    elif cmd == "fp":
        setup()
        print(fingerprint())
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
