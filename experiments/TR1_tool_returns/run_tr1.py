"""TR1 — what do tools really add? (questions.md, frozen as `TR1-frozen`). Read-only on `code_v10` (live nature).
Wrappers call the original unchanged; before it acts, each computes counterfactuals from the same state with pure
functions:
  actions.HANDLERS["forage"]  food with the tool in hand (checked against the food actually got), without a tool, with
                              the best tool the person knows, with the best tool in anyone's hands;
  actions.resolve_hunts       each hunt's kill chance with the hunters' tools, with none, with the world's best.
The observer reads the law's `hunt` events (meat per kill).

  python experiments/TR1_tool_returns/run_tr1.py zero
  python experiments/TR1_tool_returns/run_tr1.py one <arm> <seed> <years> <out>
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
SEEDS = tuple(range(21001, 21033))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9993, 9992)
V10 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
       "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1,
       "ground_items": 1, "curiosity_pull": 1}       # mortality_base: code_v10's own default (v10)
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
    """`actions._forage`'s own arithmetic: what a forage of this rate takes from this tile."""
    want = min(rate * eff, room)
    from_crop = min(crop, want * 1.3)
    from_wild = min(plants, max(0.0, want - from_crop / 1.3))
    return from_crop + from_wild


class TR1Obs:
    def __init__(self, w):
        self.w = w
        self.mismatch = Counter()
        self.s = defaultdict(float)             # sums, adults, years 100-200
        self.season = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])   # season -> [with, without, known_best, world_best]
        self.cache_tick = -1
        self.best = {}                          # use -> {sig: best factor among existing items}
        self.world_best = {}                    # use -> best factor in anyone's hands
        self.kills = [0, 0.0]                   # kills, meat (all hunts, whole run)
        self.census = []

    def refresh(self, world):
        """Best existing tools this week, by kind and in the whole world. Reads only."""
        if self.cache_tick == world.tick:
            return
        from acl.matter import factor
        self.cache_tick = world.tick
        for use in ("forage", "hunt"):
            by = {}
            for q in world.living():
                for it in q.items:
                    f = factor(it, use)
                    if f > by.get(it["sig"], 1.0):
                        by[it["sig"]] = f
            self.best[use] = by
            self.world_best[use] = max(by.values(), default=1.0)

    def late_adult(self, world, p):
        return LATE[0] <= world.tick < LATE[1] and p.age(world.tick) >= ADULT

    def before_forage(self, world, p, eff):
        from acl.matter import best_item, carry_capacity
        from acl.mind import forage_rate
        self.refresh(world)
        tile = world.tile(p.loc)
        idx, tf = best_item(p, "forage")
        rate = forage_rate(world, p)
        base = rate / tf
        room = max(0.0, carry_capacity(world, p) - p.edible())
        crop, plants = tile.crop, tile.plants
        known = max([1.0] + [self.best["forage"].get(s, 1.0) for s in p.recipes])
        got = {"with": forage_got(rate, eff, room, crop, plants),
               "without": forage_got(base, eff, room, crop, plants),
               "known": forage_got(base * max(tf, known), eff, room, crop, plants),
               "world": forage_got(base * max(tf, self.world_best["forage"]), eff, room, crop, plants)}
        return {"idx": idx, "tf": tf, "base": base, "eff": eff, "got": got, "food0": p.food + p.seeds}

    def after_forage(self, world, p, info):
        actual = p.food + p.seeds - info["food0"]
        g = info["got"]
        if not p.alive:                         # amendment 1: died within the forage; their food went to body or heir
            self.s["died_in_forage"] += 1
        elif abs(actual - g["with"]) > 1e-9:
            self.mismatch["forage_replay"] += 1
        self.s["forage_weeks_all"] += 1
        if not self.late_adult(world, p):
            return
        s = self.s
        s["weeks"] += 1
        s["with"] += g["with"]
        s["without"] += g["without"]
        s["known"] += g["known"]
        s["world"] += g["world"]
        se = self.season[world.season]
        se[0] += g["with"]
        se[1] += g["without"]
        se[2] += g["known"]
        se[3] += g["world"]
        if info["idx"] >= 0 and info["tf"] > 1.0 + 1e-12:
            added = g["with"] - g["without"]
            uncapped = info["base"] * info["eff"] * (info["tf"] - 1.0)
            s["tool_weeks"] += 1
            s["added"] += added
            s["uncapped"] += uncapped
            s["felt"] += info["tf"] - 1.0
            kind = "zero" if added <= 1e-9 else "partial" if added < uncapped - 1e-9 else "full"
            s["tw_" + kind] += 1
            if g["without"] > 1e-12:
                s["norm_gain"] += g["with"] / g["without"] - 1.0
                s["norm_n"] += 1
                s["felt_n"] += info["tf"] - 1.0

    def before_hunts(self, world):
        from acl import fauna
        from acl.matter import best_item
        from acl.mind import hunt_chance
        self.refresh(world)
        for loc, ids in world.hunts.items():
            hunters = [world.people[i] for i in ids if world.people[i].alive]
            if not hunters:
                continue
            if not (LATE[0] <= world.tick < LATE[1]) or not any(h.age(world.tick) >= ADULT for h in hunters):
                continue
            n = len(hunters)
            skill = sum(h.skills["hunting"] for h in hunters) / n
            tool = sum(best_item(h, "hunt")[1] for h in hunters) / n
            prey = fauna.prey_here(world, loc) >= 1
            wb = sum(max(best_item(h, "hunt")[1], self.world_best["hunt"]) for h in hunters) / n
            s = self.s
            s["hunts"] += 1
            s["hunters"] += n
            s["adult_hunters"] += sum(1 for h in hunters if h.age(world.tick) >= ADULT)
            if prey:
                s["h_with"] += hunt_chance(world, n, skill, tool)
                s["h_without"] += hunt_chance(world, n, skill, 1.0)
                s["h_world"] += hunt_chance(world, n, skill, wb)

    def __call__(self, world, events):
        tick = world.tick - 1
        for ev in events:
            if ev["k"] == "hunt" and ev.get("success"):
                self.kills[0] += 1
                self.kills[1] += ev.get("meat", 0.0)
                if LATE[0] <= tick < LATE[1]:
                    party = ev.get("party", [])
                    ad = sum(1 for i in party if i in world.people and world.people[i].age(world.tick) >= ADULT)
                    self.s["hunt_meat_adults"] += ev.get("meat", 0.0) * ad / max(1, len(party))
                    self.s["late_kills"] += 1
        if tick % WPY == WPY - 1:
            living = world.living()
            self.census.append([tick // WPY, len(living), sum(1 for p in living if p.age(world.tick) >= ADULT)])

    def results(self):
        return {"sums": dict(self.s), "season": {k: v for k, v in self.season.items()},
                "kills_all": self.kills, "mismatch": dict(self.mismatch),
                "census_fields": ["year", "living", "adults"], "census": self.census}


def install(w, obs):
    from acl import actions
    orig_forage = actions.HANDLERS["forage"]
    orig_hunts = actions.resolve_hunts

    def forage(world, p, target, eff):
        if world is not w:
            return orig_forage(world, p, target, eff)
        info = obs.before_forage(world, p, eff)
        out = orig_forage(world, p, target, eff)
        obs.after_forage(world, p, info)
        return out

    def resolve_hunts(world):
        if world is w:
            obs.before_hunts(world)
        return orig_hunts(world)

    actions.HANDLERS["forage"] = forage
    actions.resolve_hunts = resolve_hunts


def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = TR1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        s = obs.s
        extra = ":" + json.dumps({**obs.mismatch, "_forages": s["forage_weeks_all"], "_late_weeks": s["weeks"],
                                  "_tool_weeks": s["tool_weeks"], "_hunts": s["hunts"]},
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
    from concurrent.futures import ThreadPoolExecutor
    specs = [(seed, years, obs) for seed, years in ((501, 20), (601, 120)) for obs in (1, 0)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", "lp", *sp), specs)))
    for seed, years in ((501, 20), (601, 120)):
        a, b = got[(seed, years, 1)], got[(seed, years, 0)]
        same = a.split(":")[:2] == b.split(":")[:2]
        info = json.loads(a.split(":", 2)[2])
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = same and not any(mism.values()) and info.get("_forages", 0) > 0
        if years > 100:
            t = t and info.get("_late_weeks", 0) > 0 and info.get("_hunts", 0) > 0
        ok &= t
        lines.append(f"arm lp, seed {seed}, {years} years: identical with and without the wrappers (state and random "
                     f"numbers): {'yes' if same else 'NO'}; forage replay mismatches: {mism or 'none'}; forages "
                     f"{info.get('_forages'):.0f}, adult forage weeks years 100+ {info.get('_late_weeks'):.0f} (with "
                     f"a tool {info.get('_tool_weeks'):.0f}), adult hunts years 100+ {info.get('_hunts'):.0f}")
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
    obs = TR1Obs(w)
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
