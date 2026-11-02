"""SC1 — a scorecard of the creator's twelve capacities on live v11 (questions.md, frozen as `SC1-frozen`; operational
note 1). Read-only. ES2's runner supplies the set-up, the habit-update replay and the realized return G
(`../ES2_realized_lookahead/run_es2.py`), on `code_v11`. SC1's observer adds, in years 100-200:
  C3   habit calibration by k (earlier updates of the same habit), adults 16-44, by situation x action
  C4   own tests of a made thing's worth (`tested`, m:), and the first make within 13 weeks: alternative / same / other
  C5   gathers (wanted or not, by `mind._material_wants` at the decision), and a make using that material in 26 weeks
  C6   world-new kinds made in play (years 100-195), their best use factor, and whether anyone makes them in 260 weeks
  C7   new m: puzzles, own (from surprise) or told (from a lesson), by size, and a make of that kind in 26 weeks
  C9   told water and game places checked by the listener, against one random land tile at the same distance from
       where they were told (the observer's own random stream), checked the same way at the same moment
  C10b world-new nested kinds, whether the inventor learned the part from someone, against their repertoire's share;
       improvement; holders per kind; kinds outliving their first maker; nesting depth
  C12  adults' action and situation shares and habit summaries in years 100, 105, ..., 195; rare/familiar situations
  and described measures (company, mood, loneliness, memories, paths of recipe gains).

  python experiments/SC1_bob_scorecard/run_sc1.py zero
  python experiments/SC1_bob_scorecard/run_sc1.py one c <seed> <years> <out>
"""
from __future__ import annotations

import json
import random
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

CODE = "v11"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(22001, 22033))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9939, 9938)
ARMS = {"c": dict(base.LP)}
JOBS = [f"c:{s}" for s in SEEDS]
OUT = HERE / "output"
ADULT = 16 * WPY
W4, W5, W7, W6 = 13, 26, 26, 260           # follow-up windows in weeks (operational note 1)
SOCIAL = ("taught", "copied", "read")
USES = ("forage", "hunt", "wood", "stone", "fiber", "fight", "carry", "cold")


def best_factor(props):
    from acl.matter import factor
    item = dict(props)
    item.setdefault("wet", 0)
    return max(factor(item, u) for u in USES)


class SC1Obs(base.ES2Obs):
    def __init__(self, w):
        super().__init__(w)
        self.rng = random.Random(f"SC1-observer-{w.cfg.seed}")    # never the world's stream
        self.k = defaultdict(Counter)
        self.c3 = defaultdict(lambda: [0, 0.0])                 # "lo|hi" + "|ctx|action" -> [n, sum |q-G|]
        self.c4 = defaultdict(lambda: [0, 0, 0, 0, 0])           # "s"/"c" -> [tests, followed, alt, same, other]
        self.c4_open = []
        self.pre = {}                                            # person -> gather facts at the decision
        self.c5 = defaultdict(lambda: [0, 0])                    # "w|kind|season" -> [gathers, made in 26 weeks]
        self.c5_open = []
        self.c6 = {}                                             # sig -> [tick, class, remade]
        self.c7 = defaultdict(lambda: [0, 0])                    # "own|bin" -> [puzzles, acted]
        self.c7_open = []
        self.origin = None
        self.heard_at = {}
        self.c9 = defaultdict(lambda: [0, 0, 0])                 # "w:"/"g:" -> [checked, verified, control true]
        self.path = {}                                           # (person, sig) -> how
        self.c10 = defaultdict(float)                            # nested, social_part, opportunity, improved
        self.holders = defaultdict(set)
        self.depth_cache = {}
        self.yearly = {}                                         # year -> described numbers
        self.ya = defaultdict(lambda: [0] * self.N)
        self.yc = defaultdict(lambda: [0] * 32)
        self.snaps = []
        self.visits = defaultdict(Counter)
        self.xs = defaultdict(lambda: [[0] * self.N, [0] * self.N])   # person -> [familiar, rare] action counts
        self.paths = Counter()

    # --- windows ------------------------------------------------------------------------------------------------
    @staticmethod
    def late(tick):
        return base.LATE[0] <= tick < base.LATE[1]

    @staticmethod
    def fits(tick, window):
        return tick + window <= base.LATE[1]

    # --- C3 -----------------------------------------------------------------------------------------------------
    def on_learn(self, world, p, i, before, after, r, fut):
        super().on_learn(world, p, i, before, after, r, fut)
        k = self.k[p.id][i]
        self.k[p.id][i] = k + 1
        age = p.age(world.tick)
        band = "lo" if k < 20 else ("hi" if k >= 80 else None)
        self.pending[p.id][-1].append(band if 16 * WPY <= age < 45 * WPY else None)

    def close(self, e, censored):
        super().close(e[:5], censored)
        key, q, acc, _, late, band = e
        if late and band and not censored:
            c = self.c3[f"{band}|{key}"]
            c[0] += 1
            c[1] += abs(q - acc)

    # --- recipes ------------------------------------------------------------------------------------------------
    def recipe_of(self, world, p, sig):
        r = p.recipes.get(sig)
        if r is None and sig in world.knowledge:
            r = world.knowledge[sig]["recipe"]
        return r

    def mats_of(self, world, p, sig):
        from acl.mind import recipe_materials
        r = self.recipe_of(world, p, sig)
        return set(recipe_materials(r)) if r else set()

    def made_parts(self, recipe):
        from acl.matter import MATERIALS
        if recipe.get("verb") == "bind":
            return [x for x in recipe["parts"] if x not in MATERIALS]
        if recipe.get("verb") == "heat" and recipe["part"] not in MATERIALS:
            return [recipe["part"]]
        return []

    def depth(self, world, sig, seen=()):
        if sig in self.depth_cache:
            return self.depth_cache[sig]
        rec = world.knowledge.get(sig)
        d = 1
        if rec is not None and sig not in seen:
            parts = self.made_parts(rec["recipe"])
            if parts:
                d = 1 + max(self.depth(world, x, seen + (sig,)) for x in parts)
        self.depth_cache[sig] = d
        return d

    def on_remember(self, world, p, sig, recipe, how, fresh, world_new, props, meant):
        tick = world.tick
        if fresh:
            self.path[(p.id, sig)] = how
            self.holders[sig].add(p.id)
            if self.late(tick):
                self.paths[how + ("_variant" if meant and meant != sig else "")] += 1
        if not (world_new and how == "made" and self.late(tick)):
            return
        if props is not None and self.fits(tick, W6):
            f = best_factor(props)
            cls = "f" if f >= 1.10 else ("n" if f < 1.02 else "m")
            self.c6[sig] = [tick, cls, 0, round(f, 4)]
        parts = self.made_parts(recipe)
        if parts:
            others = [s for s in p.recipes if s != sig]
            opp = (sum(1 for s in others if self.path.get((p.id, s)) in SOCIAL) / len(others)) if others else 0.0
            social = any(self.path.get((p.id, x)) in SOCIAL for x in parts)
            self.c10["nested"] += 1
            self.c10["social_part"] += social
            self.c10["opportunity"] += opp
            if props is not None:
                pf = [best_factor(world.knowledge[x]["props"]) for x in parts
                      if x in world.knowledge and world.knowledge[x].get("props")]
                if pf:
                    self.c10["compared"] += 1
                    self.c10["improved"] += best_factor(props) > max(pf)

    # --- C5 -----------------------------------------------------------------------------------------------------
    def before_gather(self, world, p, kind):
        from acl.mind import _material_wants, recipe_materials
        if kind == "earth" or p.age(world.tick) < ADULT:
            return
        knows = any(kind in recipe_materials(r) for r in p.recipes.values())
        if not knows or p.mats.get(kind, 0.0) >= 1.0:
            return
        wanted = _material_wants(p, world.season).get(kind, 0.0) > 0
        self.pre[p.id] = (kind, int(wanted), world.season)

    # --- C7 -----------------------------------------------------------------------------------------------------
    def on_notice(self, world, p, key, new):
        if not new or self.origin is None or not key.startswith("m:") or key not in p.puzzles:
            return
        tick = world.tick
        if not (self.late(tick) and self.fits(tick, W7)):
            return
        sig = key[2:]
        if sig not in p.recipes:
            return
        size = p.puzzles[key][0]
        b = "a" if 0.25 <= size < 0.35 else ("b" if 0.35 <= size <= 0.45 else None)
        if b is None:
            return
        self.c7_open.append([p.id, sig, f"{self.origin}|{b}", tick])

    # --- C9 -----------------------------------------------------------------------------------------------------
    def control_check(self, world, kind, at):
        from acl.fauna import PREY, near
        from acl.weather import fresh_near
        if kind == "w:":
            return fresh_near(world, at, 1) is not None
        return any(g["sp"] in PREY and g["sp"] != "fish" and g["n"] > 0 for g in near(world, at, 1))

    def on_tested(self, world, p, hkey, outcome, rec):
        if rec is None or hkey[:2] not in ("g:", "w:") or not self.late(world.tick):
            return
        from acl.util import distance
        c = world.cfg
        x, y = (int(v) for v in hkey[2:].split(","))
        loc0 = rec[0]
        d = distance(loc0, (x, y), c.width, c.height)
        ring = []
        for dy in range(-d, d + 1):
            for dx in range(-d, d + 1):
                if max(abs(dx), abs(dy)) != d:
                    continue
                t = ((loc0[0] + dx) % c.width, (loc0[1] + dy) % c.height)
                if not world.tile(t).water:
                    ring.append(t)
        if not ring:
            return
        at = ring[self.rng.randrange(len(ring))]
        v = self.c9[hkey[:2]]
        v[0] += 1
        v[1] += outcome > 0.05
        v[2] += self.control_check(world, hkey[:2], at)

    # --- each week ----------------------------------------------------------------------------------------------
    def __call__(self, world, events):
        super().__call__(world, events)
        tick = world.tick - 1
        late = self.late(tick)
        for ev in events:
            k = ev["k"]
            a = ev.get("a")
            if k == "tested" and late and str(ev.get("about", "")).startswith("m:") and self.fits(tick, W4):
                p = world.people.get(a)
                gap = abs(ev.get("gap", 0.0))
                cls = "s" if gap >= 0.25 else ("c" if gap < 0.1 else None)
                if p is not None and cls:
                    sig = ev["about"][2:]
                    m = self.mats_of(world, p, sig)
                    opp = any(s != sig and m & self.mats_of(world, p, s) for s in p.recipes)
                    if opp:
                        self.c4[cls][0] += 1
                        self.c4_open.append([a, sig, cls, tick, m])
            elif k == "gather" and a in self.pre:
                kind, wanted, season = self.pre.pop(a)
                if late and self.fits(tick, W5) and ev.get("kind") == kind:
                    self.c5_open.append([a, kind, f"{wanted}|{kind}|{season}", tick])
            elif k == "make":
                self.on_make(world, a, ev.get("thing"), tick)
        self.pre.clear()
        self.expire(tick)
        if late:
            self.decisions(world)
        if tick % WPY == WPY - 1:
            self.year_end(world, tick // WPY)

    def on_make(self, world, a, sig, tick):
        p = world.people.get(a)
        if sig in self.c6:
            e = self.c6[sig]
            if tick - e[0] <= W6:
                e[2] = 1
        keep = []
        for e in self.c4_open:
            if e[0] == a and tick > e[3]:
                v = self.c4[e[2]]
                v[1] += 1
                if sig == e[1]:
                    v[3] += 1
                elif p is not None and e[4] & self.mats_of(world, p, sig):
                    v[2] += 1
                else:
                    v[4] += 1
            else:
                keep.append(e)
        self.c4_open = keep
        if p is not None:
            m = self.mats_of(world, p, sig)
            keep = []
            for e in self.c5_open:
                if e[0] == a and e[1] in m and tick > e[3]:
                    self.c5[e[2]][0] += 1
                    self.c5[e[2]][1] += 1
                else:
                    keep.append(e)
            self.c5_open = keep
        keep = []
        for e in self.c7_open:
            if e[0] == a and e[1] == sig and tick > e[3]:
                self.c7[e[2]][0] += 1
                self.c7[e[2]][1] += 1
            else:
                keep.append(e)
        self.c7_open = keep

    def expire(self, tick):
        self.c4_open = [e for e in self.c4_open if tick - e[3] < W4]
        keep = []
        for e in self.c5_open:
            if tick - e[3] >= W5:
                self.c5[e[2]][0] += 1
            else:
                keep.append(e)
        self.c5_open = keep
        keep = []
        for e in self.c7_open:
            if tick - e[3] >= W7:
                self.c7[e[2]][0] += 1
            else:
                keep.append(e)
        self.c7_open = keep

    def decisions(self, world):
        y = (world.tick - 1) // WPY
        snap = y % 5 == 0
        for d in world.week_decisions:
            p = world.people.get(d.agent_id)
            if p is None or p.age(world.tick) < ADULT:
                continue
            act = self.acts.index(d.chosen[0])
            ctx = p.last_ctx
            self.s["adult_decisions"] += 1
            self.s["company_decisions"] += (ctx % 8) >= 4
            rare = self.visits[p.id][ctx] < 5
            self.visits[p.id][ctx] += 1
            self.xs[p.id][1 if rare else 0][act] += 1
            if snap:
                self.ya[(p.id, y)][act] += 1
                self.yc[(p.id, y)][ctx] += 1

    def year_end(self, world, y):
        living = world.living()
        adults = [p for p in living if p.age(world.tick) >= ADULT]
        if base.LATE[0] <= y * WPY < base.LATE[1]:
            alive = [s for s, r in world.knowledge.items() if r["alive"]]
            outlived = sum(1 for s in alive if not (world.people.get(world.knowledge[s]["first_by"]) and
                                                   world.people[world.knowledge[s]["first_by"]].alive))
            depths = [max((self.depth(world, s) for s in p.recipes), default=0) for p in adults]
            self.yearly[str(y)] = {
                "adults": len(adults), "living": len(living),
                "mood": sum(p.mood for p in adults), "loneliness": sum(p.loneliness for p in adults),
                "memories": sum(len(p.memories) for p in adults),
                "memories_told": sum(1 for p in adults for m in p.memories if m.source),
                "kinds_alive": len(alive), "kinds_outliving_first_maker": outlived,
                "depth_sum": sum(depths), "depth_max": max(depths, default=0)}
            if y % 5 == 0:
                for p in adults:
                    a, c = self.ya.get((p.id, y)), self.yc.get((p.id, y))
                    if not a or not sum(a):
                        continue
                    tot = sum(c)
                    hab = [round(sum(c[x] / tot * p.q[x * self.N + j] for x in range(32) if c[x]), 4)
                           for j in range(self.N)]
                    self.snaps.append([p.id, y, round(p.years(world.tick), 2), p.sex,
                                       [p.genes[g] for g in sorted(p.genes)], a, c, hab])
        for key in [k for k in self.ya if k[1] < y - 6]:
            self.ya.pop(key, None)
            self.yc.pop(key, None)

    def results(self):
        late_kinds = [s for s, r in self.w.knowledge.items() if self.late(r["first_tick"])]
        return {**super().results(),
                "c3": {k: v for k, v in self.c3.items()}, "c4_fields": ["tests", "followed", "alt", "same", "other"],
                "c4": dict(self.c4), "c5": dict(self.c5),
                "c6": {cls: [sum(1 for e in self.c6.values() if e[1] == cls),
                             sum(e[2] for e in self.c6.values() if e[1] == cls)] for cls in ("f", "n", "m")},
                "c6_kinds_fields": ["best_factor", "remade"],
                "c6_kinds": [[e[3], e[2]] for e in self.c6.values()],
                "c7": dict(self.c7), "c9_fields": ["checked", "verified", "control_true"], "c9": dict(self.c9),
                "c10": dict(self.c10),
                "holders_late_kinds": [len(self.holders[s]) for s in late_kinds],
                "paths": dict(self.paths), "yearly": self.yearly,
                "snap_fields": ["person", "year", "age", "sex", "genes", "actions", "situations", "habit"],
                "snaps": self.snaps,
                "cross": {pid: v for pid, v in self.xs.items() if sum(v[0]) and sum(v[1])}}


def install(w, obs):
    base.install(w, obs)
    from acl import actions, information, inquiry, knowhow
    o_remember, o_perform = knowhow.remember_recipe, actions.perform
    o_notice, o_surprised, o_wonder = inquiry.notice, inquiry.surprised, information._wonder
    o_hear, o_tested = information.hear_place, information.tested

    def remember_recipe(world, p, sig, recipe, how, source=None, props=None, meant=None):
        if world is not w:
            return o_remember(world, p, sig, recipe, how, source, props, meant)
        fresh, world_new = sig not in p.recipes, sig not in world.knowledge
        out = o_remember(world, p, sig, recipe, how, source, props, meant)
        obs.on_remember(world, p, sig, recipe, how, fresh, world_new, props, meant)
        return out

    def perform(world, p, option):
        if world is w and option and option[0] == "gather":
            obs.before_gather(world, p, option[1][1])
        return o_perform(world, p, option)

    def notice(world, p, key, size, expected=0.0):
        new = key not in p.puzzles
        out = o_notice(world, p, key, size, expected)
        if world is w:
            obs.on_notice(world, p, key, new)
        return out

    def surprised(world, p, key, expected, got):
        prev, obs.origin = obs.origin, "own"
        try:
            return o_surprised(world, p, key, expected, got)
        finally:
            obs.origin = prev

    def wonder(world, p, key, claim):
        prev, obs.origin = obs.origin, "told"
        try:
            return o_wonder(world, p, key, claim)
        finally:
            obs.origin = prev

    def hear_place(world, listener, speaker, key, claim):
        out = o_hear(world, listener, speaker, key, claim)
        if world is w and out:
            obs.heard_at[(listener.id, key)] = (listener.loc, world.tick)
        return out

    def tested(world, p, hkey, outcome):
        rec = obs.heard_at.pop((p.id, hkey), None) if world is w else None
        out = o_tested(world, p, hkey, outcome)
        if world is w:
            obs.on_tested(world, p, hkey, outcome, rec)
        return out

    knowhow.remember_recipe = remember_recipe
    actions.perform = perform
    inquiry.notice = notice
    inquiry.surprised = surprised
    information._wonder = wonder
    information.hear_place = hear_place
    information.tested = tested


def hashrun(seed, years, observe):
    base.LATE = (0, years * WPY)          # zero checks: every year counted
    base.setup(CODE)
    w = base.make_world(seed, ARMS["c"])
    obs = None
    if observe:
        obs = SC1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results()
        info = {**obs.mismatch, "_updates": obs.s["updates"], "_c3": sum(v[0] for v in r["c3"].values()),
                "_c4": sum(v[0] for v in r["c4"].values()), "_c5": sum(v[0] for v in r["c5"].values()),
                "_c6": sum(v[0] for v in r["c6"].values()), "_c7": sum(v[0] for v in r["c7"].values()),
                "_c9": sum(v[0] for v in r["c9"].values()), "_c10": r["c10"].get("nested", 0),
                "_snaps": len(r["snaps"])}
        extra = ":" + json.dumps(info, sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


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
    specs = [(seed, years, o) for seed, years in ((501, 20), (601, 60)) for o in (0, 1)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        off, on = got[(seed, years, 0)], got[(seed, years, 1)]
        ro = hs(off) == hs(on)
        info = json.loads(on.split(":", 2)[2])
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = ro and not any(mism.values()) and info["_updates"] > 0
        ok &= t
        counts = {k[1:]: v for k, v in info.items() if k.startswith("_") and k != "_updates"}
        lines.append(f"seed {seed}, {years} years: observer read-only (state and random stream; the observer's own "
                     f"stream, the material-want and recipe reads included): {'yes' if ro else 'NO'}; update-replay "
                     f"mismatches: {mism or 'none'}; habit updates replayed {info['_updates']:.0f}; samples {counts}")
    lines.append(f"code_v11 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = base.make_world(seed, ARMS[arm])
    obs = SC1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_v11", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
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
        print(hashrun(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4] == "1"))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: every year counted; never study data
        base.LATE = (0, int(sys.argv[4]) * WPY)
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
