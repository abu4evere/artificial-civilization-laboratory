"""AW1 — learning a craft from others (questions.md, frozen as `AW1-frozen`). Nature-change study: `code_aw1` =
`code_v9` + one setting, `skill_pass` (0 = v9 exactly; v9_to_aw1.diff). Arms v (v9), w (watching: 1), t (being
shown: 2), x (sham). A read-only observer counts the practice steps the law passes (a wrapper on `actions._pass_skill`)
and takes a yearly census (CU1's, plus children's crafting skill and teens' making).

  python experiments/AW1_watch_and_teach/run_aw1.py zero
  python experiments/AW1_watch_and_teach/run_aw1.py one <arm> <seed> <years> <out>
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
CODES = {"aw1": HERE / "code_aw1", "v9": EXP / "NV9_nature_v9" / "code_v9"}
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(20601, 20633))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9987, 9986)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
V9 = {**V7, "ground_items": 1, "curiosity_pull": 1}       # nature v9's settings, explicit
LP = {"founders": 80, "width": 80, "height": 80}
ARMS = {"v": {**LP}, "w": {**LP, "skill_pass": 1}, "t": {**LP, "skill_pass": 2}, "x": {**LP, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
FIELDS = ["year", "living", "adults", "makes", "items_adults", "wb_adults_20_40", "wb_craft_sum_20_40",
          "kids_6_11", "kids_craft_sum_6_11", "teens_12_15", "teen_makes", "passed_watched", "passed_shown"]


def setup(code="aw1"):
    sys.path.insert(0, str(CODES[code]))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


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


def fingerprint(code="aw1"):
    from run_e7 import code_hash
    return code_hash(CODES[code] / "acl")


class AW1Obs:
    """Read-only: counts the law's practice steps and takes a yearly census; changes nothing."""

    def __init__(self, w):
        self.w = w
        self.passed = Counter()              # this year's steps passed, by how ("watched" / "shown")
        self.total = Counter()               # whole run
        self.makes = self.teen_makes = 0
        self.census = []

    def passed_step(self, world, q, how):
        if world is self.w:
            self.passed[how] += 1
            self.total[how] += 1

    def __call__(self, world, events):
        for ev in events:
            if ev["k"] == "make":
                self.makes += 1
                p = world.people.get(ev.get("a"))
                if p is not None and 12 * WPY <= p.age(world.tick) < 16 * WPY:
                    self.teen_makes += 1
        tick = world.tick - 1
        if tick % WPY == WPY - 1:
            living = world.living()
            adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
            wb = [p for p in living if p.generation > 0 and 20 * WPY <= p.age(world.tick) < 41 * WPY]
            kids = [p for p in living if 6 * WPY <= p.age(world.tick) < 12 * WPY]
            teens = [p for p in living if 12 * WPY <= p.age(world.tick) < 16 * WPY]
            self.census.append([tick // WPY, len(living), len(adults), self.makes, sum(len(p.items) for p in adults),
                                len(wb), sum(p.skills["crafting"] for p in wb), len(kids),
                                sum(p.skills["crafting"] for p in kids), len(teens), self.teen_makes,
                                self.passed["watched"], self.passed["shown"]])
            self.makes = self.teen_makes = 0
            self.passed = Counter()

    def results(self):
        return {"passed_total": dict(self.total), "census_fields": FIELDS, "census": self.census}


def install(w, obs):
    from acl import actions
    o_pass = actions._pass_skill

    def pass_skill(world, q, how):
        out = o_pass(world, q, how)
        obs.passed_step(world, q, how)
        return out
    actions._pass_skill = pass_skill


def hashrun(code, arm, seed, years, observe):
    setup(code)
    kw = dict(ARMS[arm])
    if code == "v9":
        kw.pop("skill_pass", None)
    w = make_world(seed, kw)
    obs = None
    if observe:
        obs = AW1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        extra = ":" + json.dumps({"_watched": obs.total["watched"], "_shown": obs.total["shown"],
                                  "_makes": sum(r[3] for r in obs.census)}, sort_keys=True, separators=(",", ":"))
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
    return world_hash(a) == world_hash(b) and b.cfg.skill_pass == ARMS[arm]["skill_pass"]


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
    specs = [(code, arm, seed, years, obs) for seed, years in ((501, 20), (601, 60))
             for code, arm, obs in (("v9", "v", 0), ("aw1", "v", 0), ("aw1", "w", 0), ("aw1", "w", 1),
                                    ("aw1", "t", 0), ("aw1", "t", 1), ("aw1", "x", 0))]
    with ThreadPoolExecutor(7) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    lines, ok = [], True
    for seed, years in ((501, 20), (601, 60)):
        g = {(c, a, o): v for (c, a, s, y, o), v in got.items() if s == seed and y == years}
        same_v9 = hs(g[("v9", "v", 0)]) == hs(g[("aw1", "v", 0)])
        ro = hs(g[("aw1", "w", 1)]) == hs(g[("aw1", "w", 0)]) and hs(g[("aw1", "t", 1)]) == hs(g[("aw1", "t", 0)])
        acts_w = hs(g[("aw1", "w", 0)]) != hs(g[("aw1", "v", 0)])
        acts_t = hs(g[("aw1", "t", 0)]) != hs(g[("aw1", "v", 0)])
        sham = hs(g[("aw1", "x", 0)]) != hs(g[("aw1", "v", 0)])
        iw = json.loads(g[("aw1", "w", 1)].split(":", 2)[2])
        it = json.loads(g[("aw1", "t", 1)].split(":", 2)[2])
        kinds = iw["_watched"] > 0 and iw["_shown"] == 0 and it["_shown"] > 0 and it["_watched"] == 0
        t = same_v9 and ro and acts_w and acts_t and sham and kinds
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_aw1 with 0 equals code_v9: {'yes' if same_v9 else 'NO'}; "
                     f"observer read-only (arms w and t): {'yes' if ro else 'NO'}; W acts: {'yes' if acts_w else 'NO'}; "
                     f"T acts: {'yes' if acts_t else 'NO'}; the sham acts: {'yes' if sham else 'NO'}; steps passed "
                     f"(w: watched {iw['_watched']}, shown {iw['_shown']}; t: watched {it['_watched']}, shown "
                     f"{it['_shown']}), each only its own kind: {'yes' if kinds else 'NO'}; make events w {iw['_makes']}, "
                     f"t {it['_makes']}")
    for arm in ("w", "t"):
        r = subprocess.run(me + ["reload", "501", arm], capture_output=True, text=True)
        t = r.stdout.split()[-1:] == ["True"]
        ok &= t
        lines.append(f"arm {arm}, seed 501: saved at year 10 and reloaded, continues exactly to year 15, setting kept: "
                     f"{'yes' if t else 'NO'}")
    lines.append(f"code_aw1 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = AW1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v9 + skill_pass (AW1)", "skill_pass": w.cfg.skill_pass,
           "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick, "extinct": not w.living(),
           "world_hash": world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, passed {res['passed_total']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2]), sys.argv[3]))
    elif cmd == "fp":
        setup()
        print(fingerprint())
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
