"""M1 — a thousand years on nature v6 (questions.md, frozen as `M1-frozen`), with RH1's reproductive-history observer
running beside it in the D80 and C20 worlds' first 120 years (`../RH1_reproductive_histories/questions.md`, frozen as
`RH1-frozen`). Read-only: the code is `code_v6` unchanged; everything here only reads. Two read-only wrappers read state
at the exact moment the world uses it (foraging: the tool in hand; the body phase: who could conceive this week) and
then call the original, unchanged.

  python experiments/M1_millennium_v6/run_m1.py zero    # hard stops (writes output/zero.txt)
  python experiments/M1_millennium_v6/run_m1.py one <arm> <seed> <years> <out>    # one world (cloud-run)
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODE = EXP / "NV6_nature_v6" / "code_v6"
OUT = HERE / "output"
WPY, YEARS = 52, 1000
SEEDS = tuple(range(16801, 16865))       # 64 new seeds, used by no study (shared by RH1, declared before data)
SMOKE_SEEDS = (9963, 9962)
V6 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1}
ARMS = {"lp": {"founders": 80, "width": 80, "height": 80}, "d80": {"founders": 80}, "c20": {}}
RH1_ARMS = ("d80", "c20")
RH1_END = 120 * WPY
USES = ("forage", "hunt", "wood", "stone", "fiber", "fight", "carry", "cold")
SAMPLE = 25 * WPY
DECADE = 10 * WPY


def setup():
    sys.path.insert(0, str(CODE))
    for d in ("E7_passive", "F1_baseline_fragility"):
        sys.path.insert(1, str(EXP / d))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


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
    return code_hash(CODE / "acl")


def maxf(props):
    from acl.matter import factor
    if not props or "edge" not in props:
        return 1.0
    return max(factor(props, u) for u in USES)


# --- M1: the millennium observer ------------------------------------------------------------------------------

class Mill:
    """Read-only, after each week; draws no random numbers and writes nothing to the world."""

    def __init__(self):
        self.decades = {}                    # decade -> Counter
        self.samples = []
        self.kinds = {}                      # sig -> record
        self.how = {}                        # person -> {sig: how first learned}
        self.cohort = []                     # people reaching 30: [birth year, useful known, of them from others,
        #                                       best held factor, crafting skill]
        self.trad = {}                       # ("r"|"b", key) -> {"samples": [decade idx...], "start_holders": [...],
        #                                       "passed": bool}
        self.marks = []                      # shared marks per 10 years
        self.forage = {}                     # decade -> [adult forage acts, food got, food owed to tools, land]
        self.pops = []

    def _dec(self, tick):
        return self.decades.setdefault(tick // DECADE, Counter())

    def __call__(self, world, events):
        tick = world.tick - 1
        d = self._dec(tick)
        living = world.living()
        d["person_weeks"] += len(living)
        for e in events:
            k = e["k"]
            if k in ("make", "play") and e.get("thing"):
                d["deliberate" if k == "make" else "play_made"] += 1
                self._made(e["thing"], e["a"], tick, e)
            elif k == "learn" and "thing" in e:
                self.how.setdefault(e["a"], {}).setdefault(e["thing"], e.get("how"))
                kd = self.kinds.get(e["thing"])
                if kd is not None and e["a"] != kd["by"]:
                    kd["learners"] += 1
            elif k == "learn" and "belief" in e:
                key = ("b", e["belief"])
                if key in self.trad:
                    self.trad[key]["passed"] = True
            elif k == "death":
                self.how.pop(e["a"], None)
        for sig, rec in world.knowledge.items():
            if sig not in self.kinds:
                recipe = rec.get("recipe") or {}
                parts = list(recipe.get("parts", ())) + ([recipe["part"]] if recipe.get("verb") == "heat" else [])
                self.kinds[sig] = {"first": rec["first_tick"], "by": rec["first_by"], "learners": 0, "dead": None,
                                   "at25": None, "maxf": maxf(rec.get("props")), "makers10": [], "last_made": None,
                                   "n_made": 0, "parts": parts}
        known = None
        for sig, kd in self.kinds.items():
            if kd["at25"] is not None:
                continue
            if kd["dead"] is None:
                fb = world.people.get(kd["by"])
                if fb is not None and not fb.alive:
                    kd["dead"] = world.tick
            elif world.tick - kd["dead"] >= 25 * WPY:
                if known is None:
                    known = set()
                    for q in living:
                        known.update(q.recipes)
                kd["at25"] = sig in known
        for p in living:
            if p.age(world.tick) == 30 * WPY:
                self._cohort(world, p)
        if tick % DECADE == DECADE - 1:
            self.pops.append(len(living))
            self._traditions(world, tick // DECADE, living)
            from acl import marks
            self.marks.append(len(marks.shared(world)))
        if tick % SAMPLE == SAMPLE - 1 or tick == 0:
            self._sample(world, tick, living)

    def _made(self, sig, who, tick, e):
        kd = self.kinds.get(sig)
        if kd is None:
            return
        if kd["maxf"] == 1.0:
            kd["maxf"] = maxf(e)
        kd["n_made"] += 1
        kd["last_made"] = tick
        if tick - kd["first"] <= 10 * WPY and who not in kd["makers10"]:
            kd["makers10"].append(who)

    def _cohort(self, world, p):
        useful = [s for s in p.recipes if self.kinds.get(s, {}).get("maxf", 1.0) > 1.0]
        hows = self.how.get(p.id, {})
        others = sum(1 for s in useful if hows.get(s) not in (None, "made"))
        best = max([maxf(it) for it in p.items] or [1.0])
        self.cohort.append([round(p.birth / WPY, 2), len(useful), others, round(best, 4),
                            round(p.skills["crafting"], 4)])

    def _traditions(self, world, idx, living):
        holders = {}
        for p in living:
            for s in p.recipes:
                holders.setdefault(("r", s), []).append(p.id)
            for b in p.beliefs:
                holders.setdefault(("b", b), []).append(p.id)
        for key, hs in holders.items():
            if len(hs) < 3:
                continue
            t = self.trad.get(key)
            if t is None:
                t = self.trad[key] = {"samples": [], "start": hs, "passed": False}
            t["samples"].append(idx)
            if key[0] == "r" and not t["passed"]:
                kd = self.kinds.get(key[1])
                t["passed"] = bool(kd and kd["learners"] > 0)
            t["start_dead"] = all(not world.people[x].alive for x in t["start"])

    def _sample(self, world, tick, living):
        adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
        skills = sorted((p.skills["crafting"] for p in adults), reverse=True)
        bests = sorted(max([maxf(it) for it in p.items] or [1.0]) for p in adults)
        uses = set()
        for p in living:
            for it in p.items:
                from acl.matter import factor
                for u in USES:
                    if "edge" in it and factor(it, u) > 1.0:
                        uses.add(u)
        held = Counter(s for p in living for s in p.recipes)
        self.samples.append({
            "year": (tick + 1) // WPY, "population": len(living), "adults": len(adults),
            "best_item": round(bests[-1], 4) if bests else None,
            "median_adult_best": round(bests[len(bests) // 2], 4) if bests else None,
            "uses_covered": len(uses),
            "skill_best": round(skills[0], 4) if skills else None,
            "skill_mean_adults": round(sum(skills) / len(skills), 4) if skills else None,
            "recipes_unique": len(held), "recipes_total": sum(held.values()),
        })

    def results(self):
        index = {sig: i for i, sig in enumerate(self.kinds)}
        kinds = [[k["first"], k["learners"], k["dead"], k["at25"], round(k["maxf"], 4), len(k["makers10"]),
                  k["last_made"], k["n_made"], [index[x] for x in k["parts"] if x in index]]
                 for k in self.kinds.values()]
        trads = [[key[0], len(t["samples"]), t["samples"][0] if t["samples"] else None,
                  t["samples"][-1] if t["samples"] else None, t["passed"], t.get("start_dead", False),
                  self._longest_run(t["samples"])] for key, t in self.trad.items() if len(t["samples"]) >= 5]
        return {"decades": {str(k): dict(v) for k, v in sorted(self.decades.items())}, "samples": self.samples,
                "kinds": kinds, "cohort": self.cohort, "traditions": trads, "marks_shared": self.marks,
                "forage": {str(k): v for k, v in sorted(self.forage.items())}}

    @staticmethod
    def _longest_run(s):
        best = run = 0
        prev = None
        for x in s:
            run = run + 1 if prev is not None and x == prev + 1 else 1
            best = max(best, run)
            prev = x
        return best


# --- RH1: reproductive histories (first 120 years of D80 and C20) ------------------------------------------------

class Repro:
    """Read-only. Women's and men's reproductive histories, and the affection deadlock, per week."""

    def __init__(self):
        self.w = {}                          # woman id -> record
        self.m = {}                          # man id -> record
        self.on = True

    def _rec(self, p):
        d = self.w if p.sex == "F" else self.m
        r = d.get(p.id)
        if r is None:
            r = d[p.id] = {"born": p.birth, "fertile": 0, "partnered": 0, "elig": 0, "logq": 0.0,
                           "single_fertile": 0, "man_alive": 0, "man_sight": 0, "court_considered": 0,
                           "court_tried": 0, "courted_by": 0, "she_attracted": 0, "he_attracted": 0,
                           "beaten": Counter(), "first": {}, "births": [], "losses": [], "pairs": [],
                           "death": None, "children": 0}
        return r

    def before_body(self, world):
        """Called by the read-only body-phase wrapper, before the week's conceptions: who could conceive now."""
        from acl.biology import _youngest_alive
        from acl.config import CHILD_END
        from acl.util import distance
        c = world.cfg
        tick = world.tick
        if tick >= RH1_END:
            self.on = False
            return
        courting = {a for pair in world.courting for a in pair}
        for p in world.living():
            if p.sex != "F" or not (c.fertile_from <= p.years(tick) < c.fertile_until):
                continue
            r = self._rec(p)
            r["fertile"] += 1
            if p.partner is None:
                continue
            r["partnered"] += 1
            mate = world.people[p.partner]
            if (p.pregnant is None and mate.alive and distance(p.loc, mate.loc, c.width, c.height) <= c.camp_radius
                    and p.health >= 50 and not p.starving and mate.age(tick) >= CHILD_END
                    and not (tick - p.last_birth < c.nursing_weeks and _youngest_alive(world, p))):
                pt = c.conception_chance * (2.0 if p.id in courting else 1.0)
                r["elig"] += 1
                r["logq"] += math.log(1.0 - pt)

    def __call__(self, world, events):
        if not self.on:
            return
        from acl.util import distance
        tick = world.tick
        c = world.cfg
        for e in events:
            k = e["k"]
            if k == "pair":
                for a, b in ((e["a"], e["b"]), (e["b"], e["a"])):
                    p = world.people[a]
                    r = self._rec(p)
                    r["pairs"].append(tick)
                    r["first"].setdefault("pair", round(p.years(tick), 2))
            elif k == "birth":
                mum = world.people[e["a"]]
                r = self._rec(mum)
                prev = [world.people[x] for x in mum.children[:-1] if world.people[x].mother == mum.id]
                prev_alive = bool(prev) and prev[-1].alive
                r["births"].append([tick, prev_alive])
                r["first"].setdefault("birth", round(mum.years(tick), 2))
                if e.get("father"):
                    self._rec(world.people[e["father"]])["children"] += 1
            elif k == "death":
                p = world.people[e["a"]]
                if p.id in self.w or p.id in self.m or p.age(tick) >= 16 * WPY:
                    self._rec(p)["death"] = tick
                if p.partner and p.partner in world.people and world.people[p.partner].alive:
                    self._rec(world.people[p.partner])["losses"].append(tick)
        living = world.living()
        men = [q for q in living if q.sex == "M" and q.stage(tick) == "adult" and q.partner is None]
        for p in living:
            if p.sex != "F" or p.partner is not None or not (c.fertile_from <= p.years(tick) < c.fertile_until):
                continue
            r = self._rec(p)
            r["single_fertile"] += 1
            elig = [q for q in men if world.kinship(p, q) == 0 and abs(p.birth - q.birth) <= 15 * WPY
                    and q.id not in p.wards and p.id not in q.wards]
            if not elig:
                continue
            r["man_alive"] += 1
            sight = [q for q in elig if distance(p.loc, q.loc, c.width, c.height) <= c.perception]
            if not sight:
                continue
            r["man_sight"] += 1
            r["first"].setdefault("man_in_sight", round(p.years(tick), 2))
            ids = {q.id for q in sight}
            cons = [x for x in p.considered if x[0] == "court" and str(x[1]) in ids]
            if cons:
                r["court_considered"] += 1
                if any(x[3] for x in cons):
                    r["court_tried"] += 1
                    r["first"].setdefault("court_given", round(p.years(tick), 2))
                else:
                    chosen = next((x[0] for x in p.considered if x[3]), None)
                    r["beaten"][chosen or "none"] += 1
            if any(any(x[0] == "court" and str(x[1]) == p.id and x[3] for x in q.considered) for q in sight):
                r["courted_by"] += 1
                r["first"].setdefault("court_received", round(p.years(tick), 2))
            att_her = att_him = False
            for q in sight:
                rh, rm = p.rel.get(q.id), q.rel.get(p.id)
                a_her = (0.25 + 0.2 * p.genes["sociability"] + (rh.affection if rh else 0.0)
                         + 0.2 * (rh.respect if rh else 0.0) + 0.1 * min(q.health, 100.0) / 100.0)
                a_him = (0.25 + 0.2 * q.genes["sociability"] + (rm.affection if rm else 0.0)
                         + 0.2 * (rm.respect if rm else 0.0) + 0.1 * min(p.health, 100.0) / 100.0)
                att_her |= a_her > 0.55
                att_him |= a_him > 0.55
            r["she_attracted"] += int(att_her)
            r["he_attracted"] += int(att_him)

    def results(self):
        def pack(d):
            out = []
            for pid, r in d.items():
                rr = dict(r)
                rr["beaten"] = dict(r["beaten"])
                rr["logq"] = round(r["logq"], 4)
                out.append(rr)
            return out
        return {"women": pack(self.w), "men": pack(self.m)}


# --- wiring ---------------------------------------------------------------------------------------------------------

def attach(w, arm):
    """Observers, plus read-only wrappers. Returns (probe, mill, repro or None)."""
    from run_f1 import Probe
    from acl import actions, biology, world as world_mod
    probe, mill = Probe(), Mill()
    w.observers += [probe, mill]
    repro = None
    if arm in RH1_ARMS:
        repro = Repro()
        w.observers.append(repro)
    orig_forage = actions._forage

    def forage(world, p, target, eff):           # read-only: the tool in hand and the land, then the original
        if world is w and p.age(world.tick) >= 16 * WPY:
            from acl.matter import best_item
            _, f = best_item(p, "forage")
            tile = world.tile(p.loc)
            land = tile.plants + tile.crop
            before = p.food + p.seeds
            orig_forage(world, p, target, eff)
            got = p.food + p.seeds - before
            row = mill.forage.setdefault((world.tick) // DECADE, [0, 0.0, 0.0, 0.0])
            row[0] += 1
            row[1] += got
            row[2] += got * (1.0 - 1.0 / f) if f > 1.0 else 0.0
            row[3] += land
            return
        return orig_forage(world, p, target, eff)
    actions._forage = forage
    if hasattr(actions, "HANDLERS"):
        actions.HANDLERS = {k: (forage if v is orig_forage else v) for k, v in actions.HANDLERS.items()}
    if repro is not None:
        orig_body = world_mod.biology.body_phase

        def body_phase(world):                    # read-only: who could conceive this week, then the original
            if world is w:
                repro.before_body(world)
            return orig_body(world)
        world_mod.biology.body_phase = body_phase
    return probe, mill, repro


def hashrun(seed, years, arm, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    if observe:
        attach(w, arm)
    for _ in range(years * WPY):
        w.step()
    return world_hash(w) + ":" + rng_state(w)


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
    return world_hash(a) == world_hash(b)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for arm in ARMS:
        t = call(501, 20, arm, 1) == call(501, 20, arm, 0)
        ok &= t
        lines.append(f"arm {arm}, seed 501, 20 years: identical with and without observers and wrappers (state and "
                     f"random numbers): {'yes' if t else 'NO'}")
    t = call(601, 100, "lp", 1) == call(601, 100, "lp", 0)
    ok &= t
    lines.append(f"arm lp, seed 601, 100 years: identical with and without observers and wrappers: {'yes' if t else 'NO'}")
    for arm in ("lp", "c20"):
        r = subprocess.run(me + ["reload", "501", arm], capture_output=True, text=True)
        t = r.stdout.split()[-1:] == ["True"]
        ok &= t
        lines.append(f"arm {arm}, seed 501: saved at year 10 and reloaded, continues exactly to year 15: "
                     f"{'yes' if t else 'NO'}")
    setup()
    lines.append(f"code_v6 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    probe, mill, repro = attach(w, arm)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v6", "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "world_hash": world_hash(w), "pops": probe.pops,
           "deaths": probe.results().get("deaths"), **mill.results()}
    if repro is not None:
        res["rh1"] = repro.results()
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2]), sys.argv[3]))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
