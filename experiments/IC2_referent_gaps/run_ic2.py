"""IC2 — where is there a real information gap: water, game or danger? (questions.md, frozen as `IC2-frozen`).
Read-only on `code_v8` (live nature). The observer reads the law's events; four wrappers call the original unchanged
and only note the state at that moment:
  actions.HANDLERS["talk"]  the start of each talk: shared attention and information gaps, both directions;
  information.hear_place    each game place accepted (with the age of the speaker's sighting);
  actions.perform           each chosen option: does it go to a told game place, and is it reached;
  fauna._go_for_people      which animal group mauled whom (health before and after; draws nothing).

  python experiments/IC2_referent_gaps/run_ic2.py zero
  python experiments/IC2_referent_gaps/run_ic2.py one <arm> <seed> <years> <out>
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
CODE = EXP / "NV8_nature_v8" / "code_v8"
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(19801, 19833))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9951, 9950)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
LP = {"founders": 80, "width": 80, "height": 80}
ARMS = {"o": {**LP}}                       # o = live nature v8 (ground_items 1 by default in code_v8)
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
REFS = ("water", "game", "danger")
FRESH_WEEKS = 12                           # a sighting counts as known for 12 weeks
DANGER = ("wolf", "bear")
NEAR_MISS_TILES, NEAR_MISS_WEEKS, MAUL_WEEKS = 2, 2, 4


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


def fresh_tiles(world, loc, radius):
    """Fresh-water tiles within `radius` (the same square and test as weather.fresh_near). Draws nothing."""
    from acl.weather import FRESH
    c = world.cfg
    out = set()
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            n = ((loc[0] + dx) % c.width, (loc[1] + dy) % c.height)
            if world.tile(n).biome in FRESH:
                out.add(n)
    return out


def groups_seen(world, loc, radius):
    """Game groups (prey other than fish) and danger groups (wolves, bears) with animals in them, by id."""
    from acl.fauna import PREY, near
    game, danger = {}, {}
    for g in near(world, loc, radius):
        if g["n"] <= 0:
            continue
        if g["sp"] in PREY and g["sp"] != "fish":
            game[g["id"]] = g
        elif g["sp"] in DANGER:
            danger[g["id"]] = g
    return game, danger


def age_band(age):
    return "0-4" if age <= 4 else ("5-8" if age <= 8 else "9-12")


class IC2Obs:
    def __init__(self, w):
        self.w = w
        self.mismatch = Counter()
        self.n = Counter()
        self.pairs = {r: Counter() for r in REFS}      # pair -> talks in which both see the same instance
        self.told = {}                                  # (listener, spot) -> out of sight at the telling
        self.told_used = set()                          # (listener, spot) later chosen as a destination
        self.last_gap = {}                              # (listener, danger group) -> last tick of a danger gap
        self.pending = []                               # [listener, group, tick] decision-relevant danger gaps
        self.census = []

    # --- the talk wrapper's note ---
    def talk(self, world, p, q):
        from acl.mind import hunger_of
        from acl.util import distance
        c = world.cfg
        tick = world.tick
        adult = {x.id: x.age(tick) >= 16 * WPY for x in (p, q)}
        seen = {}
        for x in (p, q):
            game, danger = groups_seen(world, x.loc, c.perception)
            own = [(s[0], s[1], tick - s[2]) for s in x.sightings if tick - s[2] <= FRESH_WEEKS]
            told = {tuple(int(v) for v in k[2:].split(",")) for k in x.heard if k[:2] == "g:"}
            seen[x.id] = {"fresh": fresh_tiles(world, x.loc, c.perception), "game": game, "danger": danger,
                          "own": own, "known": {(a, b) for a, b, _ in own} | told,
                          "springs": {tuple(s) for s in x.springs}}
        sp, sq = seen[p.id], seen[q.id]
        self.n["talks"] += 1
        both_adults = adult[p.id] and adult[q.id]
        pair = tuple(sorted((p.id, q.id)))
        shared = {"water": sp["fresh"] & sq["fresh"], "game": sp["game"].keys() & sq["game"].keys(),
                  "danger": sp["danger"].keys() & sq["danger"].keys()}
        for r, s in shared.items():
            if s:
                self.n[f"{r}_shared"] += 1
                self.n[f"{r}_shared_adults"] += both_adults
                self.n[f"{r}_shared_clutter"] += len(s)
                self.pairs[r][pair] += 1
        for k, l in ((p, q), (q, p)):
            if not adult[l.id]:
                continue
            a, b = seen[k.id], seen[l.id]
            self.n["directions_adult_listener"] += 1
            # game
            gap = [(x, y, age) for x, y, age in a["own"] if not b["game"] and (x, y) not in b["known"]]
            if gap:
                self.n["game_gap"] += 1
                self.n["game_gap_age_" + age_band(min(age for _, _, age in gap))] += 1
                deps = world.dependents(l.id)
                hunger = hunger_of(world, l, sum(d.need(c, tick) for d in deps))
                if hunger > 0.3 and any(distance(l.loc, (x, y), c.width, c.height) <= 3 * c.reach
                                        for x, y, _ in gap):
                    self.n["game_relevant"] += 1
            # water
            if a["springs"] - b["springs"] and not b["fresh"]:
                self.n["water_gap"] += 1
                if not b["springs"]:
                    self.n["water_relevant"] += 1
            # danger
            unseen = [g for gid, g in a["danger"].items() if gid not in b["danger"]]
            if unseen:
                self.n["danger_gap"] += 1
                for g in unseen:
                    self.last_gap[(l.id, g["id"])] = tick
                close = [g for g in unseen if distance(l.loc, (g["x"], g["y"]), c.width, c.height) <= 3 * c.reach]
                if close:
                    self.n["danger_relevant"] += 1
                    for g in close:
                        self.pending.append([l.id, g["id"], tick])

    # --- the hear_place wrapper's note (game places) ---
    def place(self, world, listener, speaker, key, out, spot, age):
        self.n["g_offered"] += 1
        if not out:
            return
        from acl.util import distance
        c = world.cfg
        self.n["g_accepted"] += 1
        band = "relayed" if age is None else (age_band(age) if age <= FRESH_WEEKS else "older")
        self.n["g_acc_age_" + band] += 1
        self.told[(listener.id, spot)] = distance(listener.loc, spot, c.width, c.height) > c.perception

    # --- the perform wrapper's note ---
    def chose(self, p, spot, reached, sees_game):
        self.n["chose_told_game"] += 1
        self.n["chose_told_game_reached"] += reached
        self.n["chose_told_game_sees_game"] += sees_game
        if (p.id, spot) in self.told:
            self.told_used.add((p.id, spot))

    # --- the mauling wrapper's note ---
    def mauled(self, world, victim, gids, route):
        """gids: the groups that could have mauled: the one hungry group, or for a surprised bear the bear groups on
        that tile (amendment 1)."""
        tick = world.tick
        self.n["maulings"] += 1
        self.n["maulings_" + route] += 1
        ts = [self.last_gap.get((victim, g)) for g in gids]
        self.n["maulings_after_gap"] += any(t is not None and tick - t <= MAUL_WEEKS for t in ts)

    # --- events, once a week ---
    def __call__(self, world, events):
        from acl.util import distance
        c = world.cfg
        tick = world.tick - 1
        for ev in events:
            k = ev["k"]
            if k == "talk":
                self.n["ev_talk"] += 1
            elif k == "learn" and str(ev.get("spot", ""))[:1] == "g":
                self.n["ev_learn_g"] += 1
            elif k == "mauled":
                self.n["ev_mauled"] += 1
        if self.pending:
            groups = {g["id"]: g for g in world.animals}
            keep = []
            for l, gid, t0 in self.pending:
                person, g = world.people.get(l), groups.get(gid)
                if person is not None and person.alive and g is not None and g["n"] > 0 and \
                        distance(person.loc, (g["x"], g["y"]), c.width, c.height) <= NEAR_MISS_TILES:
                    self.n["danger_near_miss"] += 1
                elif world.tick - t0 < NEAR_MISS_WEEKS:
                    keep.append([l, gid, t0])
            self.pending = keep
        if len(self.last_gap) > 50000:
            self.last_gap = {k: t for k, t in self.last_gap.items() if world.tick - t <= MAUL_WEEKS}
        living = world.living()
        self.n["person_weeks"] += len(living)
        self.n["adult_weeks"] += sum(1 for p in living if p.age(world.tick) >= 16 * WPY)
        if tick % WPY == WPY - 1:
            self.census.append([tick // WPY, len(living), sum(1 for p in living if p.age(world.tick) >= 16 * WPY)])

    def results(self):
        if self.n["talks"] != self.n["ev_talk"]:
            self.mismatch["talks_vs_events"] += 1
        if self.n["g_accepted"] != self.n["ev_learn_g"]:
            self.mismatch["game_accepted_vs_events"] += 1
        if self.n["maulings"] != self.n["ev_mauled"]:
            self.mismatch["maulings_vs_events"] += 1
        hist = {r: sorted(Counter(self.pairs[r].values()).items()) for r in REFS}
        told = {"accepted": len(self.told), "out_of_sight": sum(self.told.values()),
                "used": len(self.told_used), "used_out_of_sight": sum(self.told[k] for k in self.told_used)}
        return {"counts": dict(self.n), "pair_hist_fields": ["moments", "pairs"], "pair_hist": hist,
                "told_game": told, "mismatch": dict(self.mismatch), "census_fields": ["year", "living", "adults"],
                "census": self.census}


def install(w, obs):
    from acl import actions, fauna, information
    from acl.util import distance
    orig_hear = information.hear_place
    orig_talk = actions.HANDLERS["talk"]
    orig_perform = actions.perform
    orig_maul = fauna._go_for_people

    def hear_place(world, listener, speaker, key, claim):
        if world is not w or key[:2] != "g:":
            return orig_hear(world, listener, speaker, key, claim)
        spot = tuple(int(v) for v in key[2:].split(","))
        own = [world.tick - s[2] for s in speaker.sightings if (s[0], s[1]) == spot]
        age = min(own) if own else None
        out = orig_hear(world, listener, speaker, key, claim)
        obs.place(world, listener, speaker, key, out, spot, age)
        return out

    def talk(world, p, target, eff):
        if world is w:
            obs.talk(world, p, world.people[target])
        return orig_talk(world, p, target, eff)

    def perform(world, p, option):
        if world is not w:
            return orig_perform(world, p, option)
        c = world.cfg
        action, target = option
        hit = None
        obs.n["chosen"] += 1
        if isinstance(target, tuple) and action in ("forage", "hunt", "explore", "flee", "join"):
            for key in p.heard:
                if key[:2] != "g:":
                    continue
                spot = tuple(int(v) for v in key[2:].split(","))
                d = distance(p.loc, spot, c.width, c.height)
                if (d <= c.reach and target == spot) or (
                        action == "join" and c.reach < d <= 3 * c.reach
                        and world.step_toward_land(p.loc, spot, c.reach, p) == target):
                    hit = spot
                    break
        out = orig_perform(world, p, option)
        if hit is not None:
            game, _ = groups_seen(world, p.loc, c.perception)
            obs.chose(p, hit, p.loc == target, bool(game))
        return out

    def _go_for_people(world, g, sp):
        if world is not w:
            return orig_maul(world, g, sp)
        before = {q.id: q.health for q in world.people_near((g["x"], g["y"]), 1)}
        out = orig_maul(world, g, sp)
        for pid, h in before.items():
            if world.people[pid].health < h:
                obs.mauled(world, pid, [g["id"]], "hungry")
        return out

    orig_surprised = fauna.surprised

    def surprised(world, p, loc):
        # Amendment 1: the second route to a mauling (a bear surprised while someone forages or hunts close by).
        if world is not w:
            return orig_surprised(world, p, loc)
        bears = [g["id"] for g in world.herds.get(loc, ()) if g["sp"] == "bear" and g["n"] > 0]
        h = p.health
        out = orig_surprised(world, p, loc)
        if p.health < h:
            obs.mauled(world, p.id, bears, "surprised")
        return out

    information.hear_place = hear_place
    actions.HANDLERS["talk"] = talk
    actions.perform = perform
    fauna._go_for_people = _go_for_people
    fauna.surprised = surprised


def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = IC2Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        res = obs.results()
        n = res["counts"]
        extra = ":" + json.dumps({**res["mismatch"], **{"_" + k: n.get(k, 0) for k in (
            "talks", "g_accepted", "maulings", "game_gap", "game_relevant", "water_gap", "danger_gap",
            "game_shared", "danger_shared", "chose_told_game")}}, sort_keys=True, separators=(",", ":"))
    return world_hash(w) + ":" + rng_state(w) + extra


def reload_check(seed):
    setup()
    from acl.world import World
    a = make_world(seed, ARMS["o"])
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
    specs = [(seed, years, obs) for seed, years in ((501, 20), (601, 60)) for obs in (1, 0)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", "o", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        a, b = got[(seed, years, 1)], got[(seed, years, 0)]
        same = a.split(":")[:2] == b.split(":")[:2]
        info = json.loads(a.split(":", 2)[2])
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = same and not any(mism.values()) and info.get("_talks", 0) > 0 and info.get("_g_accepted", 0) > 0
        ok &= t
        shown = ", ".join(f"{k[1:]} {v}" for k, v in sorted(info.items()) if k.startswith("_"))
        lines.append(f"arm v8, seed {seed}, {years} years: identical with and without the observer and wrappers (state "
                     f"and random numbers): {'yes' if same else 'NO'}; wrapper-vs-event mismatches: {mism or 'none'}; "
                     f"{shown}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm v8, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_v8 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = IC2Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v8 (read-only audit)", "code_hash": f0,
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
