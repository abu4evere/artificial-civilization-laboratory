"""TA1 — why do tools not reach hands? (questions.md, frozen as `TA1-frozen`). Read-only on `code_v10` (live nature).
Wrappers call the original unchanged and only note the state at that moment:
  actions.HANDLERS["forage"]  before each forage: the forager's hands, recipes and materials; who is within reach
  matter.wear                 forage tools that wear out
The observer reads the law's events (`make`) and takes a weekly look at every forage tool in living hands, on the
ground and on bodies, so that each tool's entry into a hand and exit from it is accounted for.

  python experiments/TA1_tool_access/run_ta1.py zero
  python experiments/TA1_tool_access/run_ta1.py one <arm> <seed> <years> <out>
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
CODE = EXP / "NV10_nature_v10" / "code_v10"
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(21101, 21133))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9995, 9994)
V10 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
       "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1,
       "ground_items": 1, "curiosity_pull": 1}
LP = {"founders": 80, "width": 80, "height": 80}
ARMS = {"lp": {**LP}}
JOBS = [f"lp:{s}" for s in SEEDS]
LATE = (100 * WPY, 200 * WPY)
ADULT = 16 * WPY


def setup():
    sys.path.insert(0, str(CODE))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **{**V10, **kw}))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def rng_state(w):
    return hashlib.sha256(repr(w.rng.getstate()).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODE / "acl")


def forage_got(rate, eff, room, crop, plants):
    """`actions._forage`'s own arithmetic (as TR1)."""
    want = min(rate * eff, room)
    from_crop = min(crop, want * 1.3)
    from_wild = min(plants, max(0.0, want - from_crop / 1.3))
    return from_crop + from_wild


def ff(item):
    from acl.matter import factor
    return factor(item, "forage")


def band(age_weeks):
    y = age_weeks / WPY
    return "0-11" if y < 12 else "12-15" if y < 16 else "16-39" if y < 40 else "40-59" if y < 60 else "60+"


class TA1Obs:
    def __init__(self, w):
        self.w = w
        self.mismatch = Counter()
        self.q1 = Counter()                     # bare-handed adult forage weeks, years 100-200, by flag
        self.q5 = [0.0, 0.0]                    # (food with nearest holder's tool, food without) over (a') weeks
        self.hold = Counter()                   # (band, holds) person-weeks, years 100-200
        self.hold_forage = Counter()            # adult holders: foraged that week or not
        self.enter = Counter()                  # forage-tool entries into hands, by way
        self.exit = Counter()                   # exits, by way
        self.held_weeks = [0, 0]                # sum of weeks held, number of exits
        self.makes = Counter()                  # forage-tool makes: by someone already holding one, or not
        self.prev = {}                          # (pid, id(item)) -> (item, tick entered)  in living hands
        self.prev_ground = {}
        self.prev_bodies = {}
        self.keep = []                          # references to last week's items (so their ids are not reused)
        self.wear_destroyed = 0                 # forage tools worn to nothing (the wrapper)
        self.worn_ids = set()                   # ids of forage tools worn to nothing this week
        self.foraged = set()
        self.cache_tick = -1
        self.best = {}
        self.census = []

    def refresh(self, world):
        if self.cache_tick == world.tick:
            return
        self.cache_tick = world.tick
        by = {}
        for q in world.living():
            for it in q.items:
                f = ff(it)
                if f > by.get(it["sig"], 1.0):
                    by[it["sig"]] = f
        self.best = by

    def before_forage(self, world, p, eff):
        self.foraged.add(p.id)
        if not (LATE[0] <= world.tick < LATE[1]) or p.age(world.tick) < ADULT:
            return
        if any(ff(it) > 1.0 + 1e-12 for it in p.items):
            self.q1["tool_in_hand"] += 1
            return
        from acl.matter import carry_capacity
        from acl.mind import can_make, forage_rate
        self.refresh(world)
        c = world.cfg
        q1 = self.q1
        q1["bare"] += 1
        near = world.people_near(p.loc, c.reach, exclude=p.id)
        holders = [(q, max(ff(it) for it in q.items)) for q in near if q.items and max(ff(it) for it in q.items) > 1.0 + 1e-12]
        a = bool(holders)
        room = len(p.items) < c.item_limit
        q1["a"] += a
        q1["a_feasible"] += a and room
        q1["e"] += len(p.items) >= c.item_limit
        q1["empty"] += len(p.items) == 0
        q1["clogged"] += len(p.items) > 0
        good = [s for s in p.recipes if self.best.get(s, 1.0) > 1.0 + 1e-12]
        if not good:
            k = "d"
        elif any(can_make(p, p.recipes[s]) for s in good):
            k = "b"
        else:
            k = "c"
        q1[k] += 1
        prio = "e" if len(p.items) >= c.item_limit else k      # Gemini's priority partition
        q1["prio_" + prio] += 1
        if a and room:                                          # Q5: the nearest holder's actual tool
            from acl.util import distance
            q, f = min(holders, key=lambda h: (distance(p.loc, h[0].loc, c.width, c.height), h[0].id))
            tile = world.tile(p.loc)
            base = forage_rate(world, p)                        # bare-handed: tool factor 1
            rm = max(0.0, carry_capacity(world, p) - p.edible())
            self.q5[0] += forage_got(base * f, eff, rm, tile.crop, tile.plants)
            self.q5[1] += forage_got(base, eff, rm, tile.crop, tile.plants)

    def wore(self, item):
        if ff(item) > 1.0 + 1e-12 and item["uses"] <= 1:
            self.wear_destroyed += 1
            self.worn_ids.add(id(item))

    def __call__(self, world, events):
        tick = world.tick - 1
        late = LATE[0] <= tick < LATE[1]
        made_by = defaultdict(set)
        for ev in events:
            if ev["k"] == "make" and "a" in ev:
                made_by[ev["a"]].add(ev.get("thing"))
        # this week's forage tools: in living hands, on the ground, on bodies
        living = world.living()
        now = {}
        for p in living:
            for it in p.items:
                if ff(it) > 1.0 + 1e-12:
                    now[(p.id, id(it))] = it
        ground = {id(g["item"]): g["item"] for g in getattr(world, "ground", []) if ff(g["item"]) > 1.0 + 1e-12}
        bodies = {id(it): it for b in getattr(world, "bodies", []) for it in b.get("items", []) if ff(it) > 1.0 + 1e-12}
        in_hands_now = {k[1] for k in now}
        in_hands_prev = {k[1] for k in self.prev}
        alive = {p.id for p in living}
        for key, it in now.items():
            if key in self.prev:
                continue
            pid, iid = key
            if iid in in_hands_prev:
                way = "passed"                      # was in another's hands (inheritance)
            elif iid in self.prev_ground:
                way = "picked_up"
            elif iid in self.prev_bodies:
                way = "from_body"
            else:
                way = "made"                        # a new item: made, or changed from another
                held_before = any(k[0] == pid for k in self.prev)
                if it["sig"] in made_by.get(pid, ()):
                    self.makes["by_holder" if held_before else "by_bare"] += 1
            self.enter[way] += 1
            self.prev[key] = (it, tick)
        for key in [k for k in self.prev if k not in now]:
            pid, iid = key
            it, t0 = self.prev.pop(key)
            if iid in in_hands_now:
                way = "passed"
            elif iid in ground:
                way = "dropped"
            elif iid in bodies:
                way = "to_body"
            elif iid in self.worn_ids:
                way = "worn"
            elif pid not in alive:
                way = "lost_at_death"
            else:
                way = "used_or_changed"             # used up as a part, or changed by heat, wet or the like
            self.exit[way] += 1
            self.held_weeks[0] += tick - t0
            self.held_weeks[1] += 1
        for iid in self.worn_ids:
            if iid in in_hands_now:
                self.mismatch["worn_still_in_hand"] += 1
        self.worn_ids = set()
        self.prev_ground, self.prev_bodies = ground, bodies
        self.keep = list(now.values()) + list(ground.values()) + list(bodies.values())
        if late:
            holders = {k[0] for k in now}
            for p in living:
                b = band(p.age(world.tick))
                h = p.id in holders
                self.hold[f"{b}|{int(h)}"] += 1
                if h and p.age(world.tick) >= ADULT:
                    self.hold_forage[str(int(p.id in self.foraged))] += 1
        self.foraged = set()
        if tick % WPY == WPY - 1:
            self.census.append([tick // WPY, len(living), sum(1 for p in living if p.age(world.tick) >= ADULT),
                                len(now)])

    def results(self):
        held_end = len(self.prev)
        if held_end != sum(self.enter.values()) - sum(self.exit.values()):
            self.mismatch["accounting"] += 1
        return {"q1": dict(self.q1), "q5": self.q5, "hold": dict(self.hold), "hold_forage": dict(self.hold_forage),
                "enter": dict(self.enter), "exit": dict(self.exit), "held_weeks": self.held_weeks,
                "makes": dict(self.makes), "wear_destroyed": self.wear_destroyed, "held_end": held_end,
                "mismatch": dict(self.mismatch), "census_fields": ["year", "living", "adults", "forage_tools_in_hand"],
                "census": self.census}


def install(w, obs):
    from acl import actions, matter
    orig_forage = actions.HANDLERS["forage"]
    orig_wear = matter.wear

    def forage(world, p, target, eff):
        if world is w:
            obs.before_forage(world, p, eff)
        return orig_forage(world, p, target, eff)

    def wear(p, index):
        if index >= 0 and w.people.get(p.id) is p:
            obs.wore(p.items[index])
        return orig_wear(p, index)

    actions.HANDLERS["forage"] = forage
    matter.wear = wear


def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = TA1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        res = obs.results()
        extra = ":" + json.dumps({**res["mismatch"], "_bare": res["q1"].get("bare", 0),
                                  "_entries": sum(res["enter"].values()), "_exits": sum(res["exit"].values()),
                                  "_worn": res["exit"].get("worn", 0)}, sort_keys=True, separators=(",", ":"))
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
    from concurrent.futures import ThreadPoolExecutor
    specs = [(seed, years, obs) for seed, years in ((501, 20), (601, 120)) for obs in (1, 0)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", "lp", *sp), specs)))
    for seed, years in ((501, 20), (601, 120)):
        a, b = got[(seed, years, 1)], got[(seed, years, 0)]
        same = a.split(":")[:2] == b.split(":")[:2]
        info = json.loads(a.split(":", 2)[2])
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = same and not any(mism.values()) and info.get("_entries", 0) > 0
        if years > 100:
            t = t and info.get("_bare", 0) > 0
        ok &= t
        lines.append(f"arm lp, seed {seed}, {years} years: identical with and without the wrappers (state and random "
                     f"numbers): {'yes' if same else 'NO'}; accounting and wear mismatches: {mism or 'none'}; forage-tool "
                     f"entries {info.get('_entries')}, exits {info.get('_exits')} (worn {info.get('_worn')}), bare-handed "
                     f"adult forage weeks years 100+ {info.get('_bare')}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm lp, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_v10 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = TA1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v10 (read-only)", "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": world_hash(w), **obs.results()}
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
