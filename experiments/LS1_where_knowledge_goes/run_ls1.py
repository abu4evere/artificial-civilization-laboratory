"""LS1 — where does knowledge go? (questions.md, frozen as `LS1-frozen`). Read-only: live nature v7 (`code_v7`)
unchanged, with a logging observer and read-only wrappers that read state at the moment the world uses it and then
call the original, unchanged:

- `knowhow.remember_recipe` (every gain, and push-out by the 12-recipe limit), `knowhow.forget_useless`;
- `information.hear_how` (every lesson offered, and whether it was taken);
- `thought.steer` (the full list of scored options, so "weighed" is known for every option, not only the top four);
- the forage action (the tool in hand, as M1).

Deaths are seen by the observer (a person's recipes end with them).

  python experiments/LS1_where_knowledge_goes/run_ls1.py zero    # hard stops (writes output/zero.txt)
  python experiments/LS1_where_knowledge_goes/run_ls1.py one <arm> <seed> <years> <out>    # one world (cloud-run)
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
CODE = EXP / "NV7_nature_v7" / "code_v7"
OUT = HERE / "output"
WPY, YEARS = 52, 1000
DECADE = 10 * WPY
LP_SEEDS = tuple(range(18001, 18065))     # 64 new seeds, used by no study
D80_SEEDS = tuple(range(18101, 18133))    # 32 new seeds, used by no study
SEEDS = LP_SEEDS                           # for tools that need one list; JOBS is authoritative
SMOKE_SEEDS = (9961, 9960)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
ARMS = {"lp": {"founders": 80, "width": 80, "height": 80}, "d80": {"founders": 80}}
JOBS = [f"lp:{s}" for s in LP_SEEDS] + [f"d80:{s}" for s in D80_SEEDS]
USES = ("forage", "hunt", "wood", "stone", "fiber", "fight", "carry", "cold")
BIN_EDGES = (0, 5, 10, 20, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000)   # years


def bin_of(tick):
    y = tick / WPY
    for i in range(len(BIN_EDGES) - 1):
        if y < BIN_EDGES[i + 1]:
            return i
    return len(BIN_EDGES) - 2


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


def maxf(props):
    from acl.matter import factor
    if not props or "edge" not in props:
        return 1.0
    return max(factor(props, u) for u in USES)


def age_band(weeks):
    y = weeks / WPY
    if y < 6:
        return "0-5"
    if y < 12:
        return "6-11"
    if y < 16:
        return "12-15"
    if y < 30:
        return "16-29"
    if y < 50:
        return "30-49"
    return "50+"


def relation(world, teacher, learner):
    if teacher.id in (learner.mother, learner.father):
        return "parent"
    if learner.caregiver == teacher.id:
        return "carer"
    if world.kinship(teacher, learner) > 0:
        return "kin"
    return "other"


# --- the observer -----------------------------------------------------------------------------------------------

class LS1Obs:
    """Read-only. Keeps a shadow of every person's recipes, updated from the wrappers' before/after differences and
    from deaths, and checks the shadow against the world at every decade (counts) and every century (sets)."""

    def __init__(self, w):
        self.w = w
        self.shadow = {}                         # pid -> set of sigs
        self.ever = defaultdict(dict)            # pid -> sig -> [gain tick, route]
        self.bins = defaultdict(lambda: defaultdict(float))     # bin -> counter (ledger, teaching, funnel, tools)
        self.dec = defaultdict(lambda: defaultdict(float))      # decade -> counter (population, A4, ledger balance)
        self.kinds = {}                          # sig -> record
        self.living_holders = Counter()          # sig -> number of living holders (from the shadow)
        self.person = {}                         # pid -> record of world-born people and founders
        self.made_sigs = defaultdict(set)        # pid -> sigs deliberately made
        self.taught_younger = defaultdict(set)   # pid -> sigs taught (taken) to someone younger
        self.taught_any = defaultdict(set)
        self.carer_sigs = defaultdict(set)       # child pid -> sigs held by their carer while 0-16
        self.talk = defaultdict(Counter)         # pid -> partner -> talks
        self.pending25 = []                      # (tick due, pid, [sigs]) survival checks 25 years after a death
        self.lessons = []                        # taken lessons: (tick, teacher, learner, sig, relation, bin)
        self.options = {}                        # pid -> (feasible, weighed, best make score) this week
        self.registry = {}                       # id(item) -> [obj, maker pid or None, made tick, last seen tick]
        self.tool_state = {}                     # pid -> [holding a forage tool?, tick it was lost or None]
        self.last_skill = {}
        self.last_carer = {}                     # child pid -> their most recent carer (carers end at 12)
        self.mismatch = Counter()
        self.stock_start = 0
        self.dec_in = 0
        self.dec_out = 0
        self.land = sum(1 for row in w.tiles for t in row if not t.water)
        self.by_maker = defaultdict(list)        # maker pid -> sigs they first made (for M1's B-retained)
        self.due25 = []                          # (tick due, sig): 25 years after the maker's death
        for p in w.living():
            self.shadow[p.id] = set(p.recipes)
            self._person(p)

    # -- helpers --
    def _person(self, p):
        if p.id not in self.person:
            self.person[p.id] = {"born": p.birth, "gen": p.generation, "founder": p.birth < 0, "death": None,
                                 "skill16": None, "skill30": None, "hab16": None, "hab30": None,
                                 "carer_hab16": None, "talk_hab16": None, "practice": 0, "inh": None}
        return self.person[p.id]

    @staticmethod
    def make_habit(p):
        from acl.person import A, N_ACTIONS
        if not p.q:
            return None
        k = A["make"]
        vals = p.q[k::N_ACTIONS]
        return sum(vals) / len(vals) if vals else None

    def kind(self, sig, tick, p, invented):
        k = self.kinds.get(sig)
        if k is None:
            k = self.kinds[sig] = {"first": tick, "by": p.id, "by_founder": p.birth < 0, "gen": p.generation,
                                   "holders": set(), "max_gen": p.generation, "wb_holder": False,
                                   "maker_death": None, "at25": None, "vanished": None, "vanish_ch": None,
                                   "invented": invented}
            self.by_maker[p.id].append(sig)
        return k

    def gain(self, p, sig, route):
        tick = self.w.tick
        sh = self.shadow.setdefault(p.id, set())
        if sig in sh:
            return
        sh.add(sig)
        self.living_holders[sig] += 1
        b = self.bins[bin_of(tick)]
        b["in_" + route] += 1
        self.dec_in += 1
        self.ever[p.id].setdefault(sig, [tick, route])
        k = self.kind(sig, tick, p, route == "invented")
        k["holders"].add(p.id)
        k["max_gen"] = max(k["max_gen"], p.generation)
        if p.birth >= 0:
            k["wb_holder"] = True
        if k["vanished"] is not None:          # it had vanished and came back (rediscovered or read)
            k["vanished"] = None
            k["vanish_ch"] = None

    def lose(self, p_id, sig, channel):
        tick = self.w.tick
        sh = self.shadow.get(p_id)
        if not sh or sig not in sh:
            return
        sh.discard(sig)
        self.living_holders[sig] -= 1
        b = self.bins[bin_of(tick)]
        b["out_" + channel] += 1
        self.dec_out += 1
        if self.living_holders[sig] <= 0:
            k = self.kinds.get(sig)
            if k is not None:
                k["vanished"] = tick
                k["vanish_ch"] = channel
                b["ext_" + channel] += 1

    # -- wrappers call these --
    def on_remember(self, p, sig, how, before, after, kind_existed):
        gained = after - before
        lost = before - after
        for s in gained:
            if how in ("made", "heated"):
                route = "rediscovered" if kind_existed else "invented"
            elif how in ("taught", "copied", "read"):
                route = how
            else:
                route = "other"
            self.gain(p, s, route)
        for s in lost:
            self.lose(p.id, s, "pushout")

    def on_forget(self, p, before, after):
        for s in before - after:
            self.lose(p.id, s, "useless")

    def on_lesson(self, world, learner, teacher, meant, before, after, part_lesson):
        tick = world.tick
        b = self.bins[bin_of(tick)]
        rel = relation(world, teacher, learner)
        b["lesson_offered"] += 1
        b[f"lesson_offered_{rel}"] += 1
        new = after - before
        if new:
            b["lesson_taken"] += 1
            b[f"lesson_taken_{rel}"] += 1
            for s in new:
                self.lessons.append((tick, teacher.id, learner.id, s, rel, bin_of(tick)))
                self.taught_any[teacher.id].add(s)
                if learner.birth > teacher.birth:
                    self.taught_younger[teacher.id].add(s)

    def on_options(self, world, p, options):
        from acl.mind import can_make
        st = p.stage(world.tick)
        if st not in ("teen", "adult", "elder"):
            self.options[p.id] = (False, False, None)
            return
        fire = world.tile(p.loc).fire > 0
        feasible = any((r["verb"] != "heat" or fire) and can_make(p, r) for r in p.recipes.values())
        makes = [o[0] for o in options if o[1] == "make"]
        self.options[p.id] = (feasible, bool(makes), max(makes) if makes else None)

    def on_forage(self, world, p, f, got, item):
        tick = world.tick
        d = self.dec[tick // DECADE]
        d["forage_acts"] += 1
        d["forage_got"] += got
        if f > 1.0:
            d["tool_acts"] += 1
            d["tool_got"] += got
            d["owed"] += got * (1.0 - 1.0 / f)
            r = self.registry.get(id(item)) if item is not None else None
            if r is None or r[0] is not item:
                d["tool_origin_unknown"] += 1
            else:
                d["tool_origin_own" if r[1] == p.id else ("tool_origin_other" if r[1] else "tool_origin_unknown")] += 1
                if r[2] < 2 * DECADE:
                    d["tool_made_first_20y"] += 1

    # -- the week --
    def __call__(self, world, events):
        tick = world.tick - 1
        bi = bin_of(tick)
        b = self.bins[bi]
        d = self.dec[tick // DECADE]
        living = world.living()
        alive_ids = {p.id for p in living}
        # deaths: everything the dead held is lost (death channel)
        for pid in list(self.shadow):
            if pid not in alive_ids:
                q = world.people.get(pid)
                if q is not None and not q.alive:
                    held = list(self.shadow[pid])
                    useful_acq = [s for s, (t, r) in self.ever[pid].items()]
                    for s in held:
                        self.lose(pid, s, "death")
                    del self.shadow[pid]
                    rec = self.person.get(pid)
                    if rec is not None:
                        rec["death"] = q.death_tick
                        self._close(q, final=True)
                    for sig in self.by_maker.pop(pid, ()):
                        k = self.kinds[sig]
                        if k["maker_death"] is None:
                            k["maker_death"] = world.tick
                            self.due25.append((world.tick + 25 * WPY, sig))
                    if useful_acq:
                        self.pending25.append((tick + 25 * WPY, pid, useful_acq))
        # people: births, ages
        for p in living:
            if p.id not in self.shadow:
                self.shadow[p.id] = set(p.recipes)      # newborns hold nothing
            rec = self._person(p)
            age = p.age(world.tick)
            sk = p.skills["crafting"]
            if sk > self.last_skill.get(p.id, sk):
                rec["practice"] += 1
            self.last_skill[p.id] = sk
            if age == 16 * WPY:
                rec["skill16"] = round(sk, 4)
                rec["hab16"] = self.make_habit(p)
                carer = world.people.get(self.last_carer.get(p.id)) if self.last_carer.get(p.id) else None
                rec["carer_hab16"] = self.make_habit(carer) if carer is not None and carer.alive else None
                tops = [world.people.get(x) for x, _ in self.talk[p.id].most_common(3)]
                habs = [self.make_habit(t) for t in tops if t is not None and t.alive]
                habs = [h for h in habs if h is not None]
                rec["talk_hab16"] = sum(habs) / len(habs) if habs else None
            if age == 30 * WPY:
                rec["skill30"] = round(sk, 4)
                rec["hab30"] = self.make_habit(p)
                self._close(p, final=False)
            if p.caregiver:
                self.last_carer[p.id] = p.caregiver
            if age < 16 * WPY and p.caregiver:
                carer = world.people.get(p.caregiver)
                if carer is not None and carer.alive:
                    self.carer_sigs[p.id].update(carer.recipes)
            # the making funnel (teen and up), from the options seen this week
            band = age_band(age)
            feas, weighed, best = self.options.pop(p.id, (False, False, None))
            b[f"pw_{band}"] += 1
            if band in ("12-15", "16-29", "30-49", "50+"):
                b[f"feasible_{band}"] += feas
                b[f"weighed_{band}"] += weighed
                b[f"weighed_not_feasible_{band}"] += weighed and not feas
            # tools held for foraging, and replacement
            from acl.matter import best_item
            i, f = best_item(p, "forage")
            holding = f > 1.0
            ts = self.tool_state.setdefault(p.id, [holding, None])
            if ts[0] and not holding:
                ts[1] = world.tick
            elif not ts[0] and holding and ts[1] is not None:
                if world.tick - ts[1] <= WPY:
                    b["tool_replaced"] += 1
                ts[1] = None
            if ts[1] is not None and world.tick - ts[1] > WPY:
                b["tool_not_replaced"] += 1
                ts[1] = None
            ts[0] = holding
            # items: who made each thing in hand
            made_now = {e.get("thing") for e in events if e.get("k") in ("make", "play") and e.get("a") == p.id}
            for it in p.items:
                r = self.registry.get(id(it))
                if r is None or r[0] is not it:
                    maker = p.id if it["sig"] in made_now else None
                    self.registry[id(it)] = [it, maker, world.tick, world.tick]
                else:
                    r[3] = world.tick
        # what was chosen this week
        for dcs in world.week_decisions:
            act = dcs.chosen[0] if dcs.chosen else None
            p = world.people.get(dcs.agent_id) if hasattr(dcs, "agent_id") else None
            if p is None:
                continue
            band = age_band(dcs.tick - p.birth)
            if act == "make":
                b[f"chosen_{band}"] += 1
                b[f"chosen_weighed_{band}"] += 1
            elif act == "play":
                b[f"play_{band}"] += 1
            else:
                cand = [c for c in dcs.candidates if c[0] == "make"]
                if cand:
                    b[f"beaten_by_{act}"] += 1
        for e in events:
            k = e.get("k")
            if k == "make" and e.get("thing"):
                self.made_sigs[e["a"]].add(e["thing"])
                b["made_deliberate"] += 1
            elif k == "play" and e.get("thing"):
                b["made_play"] += 1
            elif k == "talk":
                self.talk[e["a"]][e.get("b")] += 1
                if e.get("b"):
                    self.talk[e["b"]][e["a"]] += 1
        # tools: who made the one used in decades 2-4 (registry at the moment of use is read in on_forage_item)
        b["pw"] += len(living)
        b["held_recipe_weeks"] += sum(len(self.shadow.get(p.id, ())) for p in living)
        if world.tick <= 100 * WPY:                    # Q2: useful know-how held in years 0-100, by the kind's origin
            for p in living:
                for sig in self.shadow.get(p.id, ()):
                    k = self.kinds.get(sig)
                    if k is None:
                        continue
                    if "useful" not in k:
                        k["useful"] = maxf((world.knowledge.get(sig) or {}).get("props")) > 1.0
                    if k["useful"]:
                        b["useful_held_weeks_founder" if k["by_founder"] else "useful_held_weeks_worldborn"] += 1
        # survival checks 25 years after a death
        if self.pending25 and self.pending25[0][0] <= tick:
            due = [x for x in self.pending25 if x[0] <= tick]
            self.pending25 = [x for x in self.pending25 if x[0] > tick]
            held_now = set()
            for p in living:
                held_now.update(p.recipes)
            for _, pid, sigs in due:
                rec = self.person.get(pid)
                if rec is not None:
                    us = [s for s in sigs if maxf((world.knowledge.get(s) or {}).get("props")) > 1.0]
                    rec["surv25"] = [sum(1 for s in us if s in held_now), len(us)]
        # B-retained by M1's rule: a kind's maker died; 25 years later, does anyone alive know it?
        if self.due25 and self.due25[0][0] <= world.tick:
            held_now = set()
            for p in living:
                held_now.update(p.recipes)
            while self.due25 and self.due25[0][0] <= world.tick:
                _, sig = self.due25.pop(0)
                self.kinds[sig]["at25"] = sig in held_now
        # decade boundary: population and the ledger check
        if world.tick % DECADE == 0:
            dd = self.dec[(world.tick - 1) // DECADE]
            dd["pop"] = len(living)
            dd["adults"] = sum(1 for p in living if p.age(world.tick) >= 16 * WPY)
            actual = sum(len(p.recipes) for p in living)
            if actual != self.stock_start + self.dec_in - self.dec_out:
                self.mismatch["ledger"] += 1
            dd["stock_end"] = actual
            dd["in"] = self.dec_in
            dd["out"] = self.dec_out
            self.stock_start, self.dec_in, self.dec_out = actual, 0, 0
            kinds_actual = set()
            for p in living:
                kinds_actual.update(p.recipes)
            kinds_obs = {s for s, n in self.living_holders.items() if n > 0}
            if kinds_actual != kinds_obs:
                self.mismatch["kinds"] += 1
            if world.tick % (10 * DECADE) == 0:
                for p in living:
                    if set(p.recipes) != self.shadow.get(p.id, set()):
                        self.mismatch["holdings"] += 1
            # prune the item registry (things not seen held for two years)
            self.registry = {k_: v for k_, v in self.registry.items() if world.tick - v[3] <= 2 * WPY}

    def _close(self, p, final):
        """At 30 (or death), the person's inheritance, use and onward passing. Useful = a kind with a factor > 1."""
        rec = self.person.get(p.id)
        if rec is None or rec.get("inh") is not None or p.birth < 0:
            return
        w = self.w
        useful = lambda s: maxf((w.knowledge.get(s) or {}).get("props")) > 1.0   # noqa: E731
        carer = {s for s in self.carer_sigs.pop(p.id, set()) if useful(s)}
        limit = p.birth + 30 * WPY
        ever = self.ever.get(p.id, {})
        got = {s: r for s, (t, r) in ever.items() if t <= limit}
        inh = [s for s in carer if s in got]
        routes = Counter(got[s] for s in inh)
        acq16 = Counter(r for s, (t, r) in ever.items() if t <= p.birth + 16 * WPY)
        acq30 = Counter(r for s, (t, r) in ever.items() if t <= limit)
        acquired_other = [s for s, (t, r) in ever.items() if r in ("taught", "copied", "read")]
        rec["inh"] = [len(inh), len(carer), dict(routes)]
        rec["acq16"] = dict(acq16)
        rec["acq30"] = dict(acq30)
        rec["acq30_useful"] = sum(1 for s in got if useful(s))
        rec["used"] = [sum(1 for s in acquired_other if s in self.made_sigs.get(p.id, ())), len(acquired_other)]
        rec["onward"] = [sum(1 for s in ever if s in self.taught_younger.get(p.id, ())), len(ever)]
        rec["closed_at30"] = not final

    def results(self):
        w = self.w
        kinds = []
        for sig, k in self.kinds.items():
            kinds.append([k["first"], int(k["by_founder"]), k["gen"], len(k["holders"]), k["max_gen"],
                          int(k["wb_holder"]), k["maker_death"], k["at25"], k["vanished"], k["vanish_ch"],
                          round(maxf((w.knowledge.get(sig) or {}).get("props")), 4), int(k["invented"])])
        # taken lessons: later made or passed on
        les = defaultdict(lambda: defaultdict(int))
        for tick, t, l_, s, rel, bi in self.lessons:
            c = les[f"{bi}|{rel}"]
            c["taken"] += 1
            c["made"] += s in self.made_sigs.get(l_, ())
            c["passed"] += s in self.taught_any.get(l_, ())
        for p in w.living():
            self._close(p, final=True)
        end = w.tick

        def reached16(r):
            last = r["death"] if r["death"] is not None else end
            return r["founder"] or last - r["born"] >= 16 * WPY
        people = [[pid, r["born"], r["gen"], int(r["founder"]), r["death"], r["skill16"], r["skill30"], r["hab16"],
                   r["hab30"], r["carer_hab16"], r["talk_hab16"], r["practice"], r.get("inh"), r.get("acq16"),
                   r.get("acq30"), r.get("acq30_useful"), r.get("used"), r.get("onward"), r.get("surv25")]
                  for pid, r in self.person.items() if reached16(r)]
        return {"bins": {str(k): dict(v) for k, v in sorted(self.bins.items())},
                "decades": {str(k): dict(v) for k, v in sorted(self.dec.items())},
                "kinds": kinds, "lessons": {k: dict(v) for k, v in les.items()}, "people": people,
                "mismatch": dict(self.mismatch), "land": self.land}


def install(w, obs):
    """The read-only wrappers. Each reads before and after and calls the original unchanged."""
    from acl import actions, information, knowhow, thought
    orig_rem, orig_forget, orig_hear, orig_steer, orig_forage = (knowhow.remember_recipe, knowhow.forget_useless,
                                                                  information.hear_how, thought.steer,
                                                                  actions._forage)

    def remember_recipe(world, p, sig, recipe, how, source=None, props=None, meant=None):
        if world is not w:
            return orig_rem(world, p, sig, recipe, how, source, props, meant)
        before = set(p.recipes)
        existed = sig in world.knowledge
        out = orig_rem(world, p, sig, recipe, how, source, props, meant)
        obs.on_remember(p, sig, how, before, set(p.recipes), existed)
        return out

    def forget_useless(p):
        before = set(p.recipes)
        out = orig_forget(p)
        if p.id in obs.shadow:
            obs.on_forget(p, before, set(p.recipes))
        return out

    def hear_how(world, learner, teacher, meant, recipe, claim, parent, part_lesson=False):
        if world is not w:
            return orig_hear(world, learner, teacher, meant, recipe, claim, parent, part_lesson)
        before = set(learner.recipes)
        out = orig_hear(world, learner, teacher, meant, recipe, claim, parent, part_lesson)
        obs.on_lesson(world, learner, teacher, meant, before, set(learner.recipes), part_lesson)
        return out

    def steer(p, options):
        out = orig_steer(p, options)
        if p.id in obs.shadow or w.people.get(p.id) is p:
            obs.on_options(w, p, out)
        return out

    def forage(world, p, target, eff):
        if world is w and p.age(world.tick) >= 16 * WPY:
            from acl.matter import best_item
            i, f = best_item(p, "forage")
            item = p.items[i] if i >= 0 else None
            before = p.food + p.seeds
            orig_forage(world, p, target, eff)
            obs.on_forage(world, p, f, p.food + p.seeds - before, item)
            return
        return orig_forage(world, p, target, eff)

    knowhow.remember_recipe = remember_recipe
    knowhow.forget_useless = forget_useless
    information.hear_how = hear_how
    thought.steer = steer
    actions._forage = forage
    if hasattr(actions, "HANDLERS"):
        actions.HANDLERS = {k: (forage if v is orig_forage else v) for k, v in actions.HANDLERS.items()}


# --- zero checks --------------------------------------------------------------------------------------------------

def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    if observe:
        obs = LS1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        extra = ":" + json.dumps(obs.mismatch, sort_keys=True)
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
    for arm, seed, years in (("lp", 501, 20), ("d80", 501, 20), ("lp", 601, 100), ("d80", 601, 100)):
        a = call("hashrun", arm, seed, years, 1)
        b = call("hashrun", arm, seed, years, 0)
        same = a.split(":")[:2] == b.split(":")[:2]
        mism = json.loads(a.split(":", 2)[2]) if a.count(":") >= 2 else {"?": 1}
        t = same and not any(mism.values())
        ok &= t
        lines.append(f"arm {arm}, seed {seed}, {years} years: identical with and without the observer (state and "
                     f"random numbers): {'yes' if same else 'NO'}; ledger, kind-count and holdings mismatches: "
                     f"{mism or 'none'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm lp, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_v7 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = LS1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v7", "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "world_hash": world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, mismatches {dict(obs.mismatch)}", flush=True)


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
