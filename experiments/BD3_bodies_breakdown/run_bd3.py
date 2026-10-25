"""BD3 — what in a body keeps more people alive? (questions.md, frozen as `BD3-frozen`). `code_bd3` = `code_v6` + five
probe switches, each default 0 (= nature v6 exactly), and read-only logging (`world.bd1log`, the Avoid observer).
The full difference is `v6_to_bd3.diff`.

  python experiments/BD3_bodies_breakdown/run_bd3.py zero    # hard stops (writes output/zero.txt)
  python experiments/BD3_bodies_breakdown/run_bd3.py one <arm> <seed> <years> <out>    # one world (cloud-run)
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
CODES = {"bd3": HERE / "code_bd3", "v6": EXP / "NV6_nature_v6" / "code_v6"}
OUT = HERE / "output"
WPY, YEARS = 52, 120
SEEDS = tuple(range(15001, 16025))       # 1,024 new seeds, used by no study
SMOKE_SEEDS = (9967, 9966)
V6 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1}
PARTS = ("eat", "carried", "foul", "seen", "tools")
ARMS = {"f": {}, "n": {"bodies_stay": 0},
        **{f"f_{x}": {f"bd3_no_{x}": 1} for x in PARTS},
        "f_eat_carried": {"bd3_no_eat": 1, "bd3_no_carried": 1},
        "f_all": {f"bd3_no_{x}": 1 for x in PARTS}}
DELAYS = (4, 14, 52, 104)                # weeks after a foul exposure at which return is checked
BINS = ((0, 4), (5, 14), (15, 52), (53, 104))


def setup(code="bd3"):
    sys.path.insert(0, str(CODES[code]))
    for d in ("E7_passive", "F1_baseline_fragility"):
        sys.path.insert(1, str(EXP / d))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **{**V6, **kw}))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def rng_state(w):
    return hashlib.sha256(repr(w.rng.getstate()).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["bd3"] / "acl")


class Weeks:
    """Read-only: living person-weeks."""

    def __init__(self):
        self.n = 0

    def __call__(self, world, events):
        self.n += len(world.living())


class Avoid:
    """Read-only. After someone meets a rotten body within one tile (a foul exposure, or in F-foul the same moment
    without the penalty), (1) whether they are back within one tile of it 4, 14, 52 and 104 weeks later; (2) each later
    week (up to 104) in which the place was within reach of where they stood and they were not already there, whether
    they went there. First exposure per person and body only."""

    def __init__(self):
        self.seen = 0                    # log rows already read
        self.places = {}                 # body id -> (x, y, death tick)
        self.exp = {}                    # (person, body) -> exposure tick, while being followed
        self.done = set()                # pairs followed to the end
        self.back = Counter()            # delay -> back within one tile
        self.alive_at = Counter()        # delay -> still alive
        self.opp = Counter()             # weeks-since-exposure bin -> weeks the place was within reach
        self.went = Counter()            # same bin -> weeks they went there
        self.exp_bins = Counter()        # weeks-since-death bin of the exposure
        self.last = {}                   # person -> location at the end of last week

    def __call__(self, world, events):
        from acl.util import distance
        c = world.cfg
        tick = world.tick
        log = world.bd1log
        for r in log[self.seen:]:
            if r[0] == "body":
                self.places[r[2]] = (r[7][0], r[7][1], r[1])
            elif r[0] in ("foul", "foul_opp") and (r[2], r[3]) not in self.exp and (r[2], r[3]) not in self.done:
                self.exp[(r[2], r[3])] = r[1]
                pl = self.places.get(r[3])
                if pl:
                    since = r[1] - pl[2]
                    for k, (a, b) in enumerate(BINS):
                        if a <= since <= b:
                            self.exp_bins[k] += 1
        self.seen = len(log)
        for key in [k for k, t0 in self.exp.items() if tick - t0 > max(DELAYS)]:
            self.done.add(key)
            del self.exp[key]
        for (pid, bid), t0 in self.exp.items():
            age = tick - t0
            if age <= 0:
                continue
            p = world.people[pid]
            if not p.alive or bid not in self.places:
                continue
            x, y, _ = self.places[bid]
            near = distance(p.loc, (x, y), c.width, c.height) <= 1
            if age in DELAYS:
                self.alive_at[age] += 1
                self.back[age] += int(near)
            before = self.last.get(pid)
            if before is not None and distance(before, (x, y), c.width, c.height) > 1 \
                    and distance(before, (x, y), c.width, c.height) <= c.reach + 1:
                k = next(i for i, (a, b) in enumerate(((1, 4), (5, 14), (15, 52), (53, 104))) if a <= age <= b)
                self.opp[k] += 1
                self.went[k] += int(near)
        self.last = {p.id: p.loc for p in world.living()}

    def results(self):
        return {"exposures": len(self.exp) + len(self.done), "exp_bins": [self.exp_bins[k] for k in range(4)],
                "back": [self.back[d] for d in DELAYS], "alive_at": [self.alive_at[d] for d in DELAYS],
                "opp": [self.opp[k] for k in range(4)], "went": [self.went[k] for k in range(4)]}


def observers(w):
    from run_f1 import Probe
    w.bd1log = []
    return Probe(), Weeks(), Avoid()


def summarise(w, wk, av):
    """What bodies did, from the log. Body rows: (tick, id, meat, food, tools, carried, place)."""
    log = w.bd1log
    c = Counter(r[0] for r in log)
    ate = [r for r in log if r[0] == "ate"]
    src = [r for r in log if r[0] == "ate_src"]
    body = [r for r in log if r[0] == "body"]
    bones = [r[3] for r in log if r[0] == "bones"]
    return {"person_years": wk.n / WPY, "bodies": len(body), "bones": len(bones), "weeks_to_bones": bones,
            "opp_meat": sum(1 for r in body if r[3] > 0), "opp_carried": sum(1 for r in body if r[6] > 0),
            "opp_tools": sum(1 for r in body if r[5] > 0), "carried_food": sum(r[6] for r in body),
            "left_with_body": sum(1 for r in body if r[4] - r[3] > 1e-9),
            "foul_weeks": c["foul"], "foul_opp": c["foul_opp"],
            "seen": c["seen"], "seen_opp": len({(r[2], r[3]) for r in log if r[0] == "seen_opp"}),
            "tools": c["tools"], "kinvisit": c["kinvisit"],
            "toplants": sum(r[3] for r in log if r[0] == "toplants"),
            "ate_n": len(ate), "ate_food": sum(r[4] for r in ate), "ate_kin": sum(1 for r in ate if r[5]),
            "ate_rotten": sum(1 for r in ate if r[6]),
            "meat_meals": sum(1 for r in src if r[4] > 1e-9), "meat_food": sum(r[4] for r in src),
            "carried_meals": sum(1 for r in src if r[5] > 1e-9), "carried_eaten": sum(r[5] for r in src),
            "avoid": av.results()}


def hashrun(code, seed, years, kw, observe):
    setup(code)
    w = make_world(seed, kw)
    if observe:
        w.observers += list(observers(w))
    for _ in range(years * WPY):
        w.step()
    return world_hash(w) + ":" + rng_state(w)


def reload_check(seed, arm):
    setup("bd3")
    from acl.world import World
    a = make_world(seed, ARMS[arm])
    a.bd1log = []
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    b.bd1log = []
    for w in (a, b):
        for _ in range(5 * WPY):
            w.step()
    return len(a.bodies) > 0 and world_hash(a) == world_hash(b)


def unit_tests():
    """Source tests on hand-made stores (no world run): mixed stores, partial takes, rotten meat, conservation."""
    setup("bd3")
    from acl import biology
    lines = []
    w = make_world(11, {"bd3_no_eat": 1})
    for _ in range(3):
        w.step()
    b = {"id": "dead", "flesh": True, "meat0": 18.0, "add": 0.0}
    w.bodies.append(b)
    e = ["dead", 18.0 + 5.0, 1.0, 0]                       # 18 meat, 5 carried
    t1 = abs(biology.body_meat_left(w, "dead", e) - 18.0) < 1e-9 and abs(biology.takeable(w, "dead", e) - 5.0) < 1e-9
    lines.append(f"mixed store, fresh: meat 18 not takeable, carried 5 takeable: {'yes' if t1 else 'NO'}")
    b["add"] = 0.5 * biology.BONES_ADD                     # half the flesh gone by warmth (rotten)
    e[1] = 9.0 + 5.0
    t2 = abs(biology.takeable(w, "dead", e) - 5.0) < 1e-9
    lines.append(f"rotten store (half the flesh gone): still only the carried 5 takeable: {'yes' if t2 else 'NO'}")
    e[1] = 9.0 + 2.0                                       # 3 of the carried food already taken
    t3 = abs(biology.takeable(w, "dead", e) - 2.0) < 1e-9
    lines.append(f"after a partial take of carried food: 2 left takeable: {'yes' if t3 else 'NO'}")
    w.cfg.bd3_no_eat = 0
    t4 = abs(biology.takeable(w, "dead", e) - 11.0) < 1e-9
    lines.append(f"switch off: the whole store takeable, as v6: {'yes' if t4 else 'NO'}")
    w.bodies.remove(b)
    t5 = abs(biology.body_meat_left(w, "someone", ["someone", 4.0, 0.0, 0]) - 0.0) < 1e-9
    lines.append(f"an ordinary store has no flesh: {'yes' if t5 else 'NO'}")
    ok = t1 and t2 and t3 and t4 and t5
    # conservation in F-carried and the no-eat arm, over whole runs: food the dead carried, where it went
    for arm in ("f_carried", "f_eat"):
        w = make_world(501, ARMS[arm])
        w.bd1log = []
        for _ in range(20 * WPY):
            w.step()
        body = [r for r in w.bd1log if r[0] == "body"]
        carried = sum(r[6] for r in body)
        plants = sum(r[3] for r in w.bd1log if r[0] == "toplants")
        left = sum(r[4] - r[3] for r in body)
        meat_meals = sum(1 for r in w.bd1log if r[0] == "ate_src" and r[4] > 1e-9)
        if arm == "f_carried":
            t = carried > 0 and abs(carried - plants) < 1e-3 and left < 1e-6
            lines.append(f"F-carried, seed 501, 20 years: carried food {carried:.2f} all went to plants "
                         f"({plants:.2f}), none left with bodies: {'yes' if t else 'NO'}")
        else:
            t = meat_meals == 0 and len(body) > 0
            lines.append(f"F-eat, seed 501, 20 years: {len(body)} bodies, no meal took meat: {'yes' if t else 'NO'}")
        ok &= t
    return ok, lines


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for seed, years in ((11, 5), (501, 5), (501, 20), (601, 20)):
        for arm in ("f", "n"):
            t = call("bd3", seed, years, json.dumps(ARMS[arm]), 0) == call("v6", seed, years, json.dumps(ARMS[arm]), 0)
            ok &= t
            lines.append(f"seed {seed}, {years} years, arm {arm}: switches 0 = code_v6 (state and random numbers): "
                         f"{'yes' if t else 'NO'}")
    base = {s: call("bd3", s, 20, json.dumps(ARMS["f"]), 0) for s in (501, 601)}
    for arm in ARMS:
        if arm in ("f", "n"):
            continue
        acts = [s for s in (501, 601) if call("bd3", s, 20, json.dumps(ARMS[arm]), 0) != base[s]]
        t = bool(acts)
        ok &= t
        lines.append(f"arm {arm}, seeds 501 and 601, 20 years: the switch changes the world (it acts) in at least one: "
                     f"{'yes, seed ' + ' and '.join(map(str, acts)) if t else 'NO'}")
    for arm in ARMS:
        t = call("bd3", 501, 20, json.dumps(ARMS[arm]), 1) == call("bd3", 501, 20, json.dumps(ARMS[arm]), 0)
        ok &= t
        lines.append(f"arm {arm}, seed 501, 20 years: identical with and without observers and logging: "
                     f"{'yes' if t else 'NO'}")
    for arm in ("f", "f_all"):
        r = subprocess.run(me + ["reload", "501", arm], capture_output=True, text=True)
        t = r.stdout.split()[-1:] == ["True"]
        ok &= t
        lines.append(f"arm {arm}, seed 501: saved at year 10 (bodies held) and reloaded, continues exactly to year 15: "
                     f"{'yes' if t else 'NO'}")
    r = subprocess.run(me + ["units"], capture_output=True, text=True)
    t = r.returncode == 0 and "All units: PASS" in r.stdout
    ok &= t
    lines += [ln for ln in r.stdout.splitlines() if ln.strip() and not ln.startswith("All units")] or [r.stderr[-1500:]]
    lines.append(f"source tests: {'yes' if t else 'NO'}")
    setup("bd3")
    lines.append(f"code_bd3 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup("bd3")
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    probe, wk, av = observers(w)
    w.observers += [probe, wk, av]
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v6", "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "world_hash": world_hash(w), "pops": probe.pops,
           "deaths": probe.results().get("deaths"), **summarise(w, wk, av)}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), json.loads(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2]), sys.argv[3]))
    elif cmd == "units":
        ok, lines = unit_tests()
        print("\n".join(lines))
        print(f"All units: {'PASS' if ok else 'FAIL'}")
        sys.exit(0 if ok else 1)
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
