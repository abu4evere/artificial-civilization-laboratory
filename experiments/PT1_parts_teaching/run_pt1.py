"""PT1 — does parts-first teaching work? (questions.md, frozen as `PT1-frozen`). Read-only: live nature v7 (`code_v7`)
unchanged, with read-only wrappers on `information.hear_how` and `knowhow.remember_recipe` that read state before each
call (the random draw from a copy of the generator's state, never consuming it) and call the originals unchanged.

  python experiments/PT1_parts_teaching/run_pt1.py zero
  python experiments/PT1_parts_teaching/run_pt1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import hashlib
import json
import random
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODE = EXP / "NV7_nature_v7" / "code_v7"
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(18801, 18833))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9947, 9946)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
ARMS = {"lp": {"founders": 80, "width": 80, "height": 80}}
JOBS = [f"lp:{s}" for s in SEEDS]
USES = ("forage", "hunt", "wood", "stone", "fiber", "fight", "carry", "cold")
ERAS = (50, 100, 200)
# chain record fields (a list per (learner, whole) chain, from its first G4 failure)
CHAIN = ("t0", "era", "origin", "useful", "rel", "age", "cls", "nmiss_direct", "nmiss_all", "depth", "fails",
         "ever_reach", "pt", "pk", "pm", "ah", "wt", "wh", "wm", "end")


def era_of(tick):
    y = tick / WPY
    for i, e in enumerate(ERAS):
        if y < e:
            return i
    return len(ERAS) - 1


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


def relation(world, teacher, learner):
    if teacher.id in (learner.mother, learner.father):
        return "parent"
    if learner.caregiver == teacher.id:
        return "carer"
    if world.kinship(teacher, learner) > 0:
        return "kin"
    return "other"


def age_band(weeks):
    y = weeks / WPY
    return "child" if y < 12 else ("teen" if y < 16 else "adult")


def made_parts(recipe):
    """The made parts a recipe needs, in the code's order (as `can_follow` and parts-first read them)."""
    from acl.matter import MATERIALS
    parts = list(recipe.get("parts", ())) + ([recipe["part"]] if recipe.get("verb") == "heat" else [])
    return [x for x in parts if x not in MATERIALS]


class PT1Obs:
    def __init__(self, w):
        self.w = w
        self.useful_cache = {}
        self.cells = defaultdict(lambda: defaultdict(float))
        self.mismatch = Counter()
        self.founder_kinds = set()
        self.chains = {}                         # (learner, whole) -> list (CHAIN fields)
        self.cmeta = {}                          # (learner, whole) -> {"sel": part or None, "need": set of direct parts not yet held}
        self.by_learner = defaultdict(set)       # learner -> open chain keys
        self.ctx = []                            # stack of lesson contexts during hear_how
        self.evicted = defaultdict(dict)         # learner -> {sig: (tick, cell key)}
        self.n_fail = 0
        self.n_mem = 0
        for p in w.living():                     # founders start with no recipes; kept for safety, as LA1
            self.founder_kinds.update(p.recipes)

    # --- helpers -------------------------------------------------------------------------------------------
    def useful(self, sig):
        if sig not in self.useful_cache:
            props = (self.w.knowledge.get(sig) or {}).get("props")
            if props is None:
                return False
            self.useful_cache[sig] = maxf(props) > 1.0
        return self.useful_cache[sig]

    def origin(self, sig):
        return "founder" if sig in self.founder_kinds else "worldborn"

    def lookup(self, teacher, sig):
        r = teacher.recipes.get(sig)
        if r is None:
            r = (self.w.knowledge.get(sig) or {}).get("recipe")
        return r

    def missing(self, learner, teacher, recipe):
        """Direct missing parts; all missing parts, recursively; levels needed (1 = every missing part can be followed)."""
        direct = [x for x in made_parts(recipe) if x not in learner.recipes]
        allm, seen = set(), set()

        def levels(rec, stack):
            miss = [x for x in made_parts(rec) if x not in learner.recipes]
            if not miss:
                return 0
            d = 1
            for m in miss:
                allm.add(m)
                if m in stack:
                    continue
                r = self.lookup(teacher, m)
                if r is None:
                    continue
                seen.add(m)
                d = max(d, 1 + levels(r, stack | {m}))
            return d
        depth = levels(recipe, frozenset())
        return direct, allm, depth

    def gate_info(self, world, learner, teacher, meant, recipe, parent):
        from acl.information import _openness, _sig_of, credence
        from acl.knowhow import can_follow
        sig = _sig_of(recipe)
        holds = any(it["sig"] == meant for it in teacher.items)
        c = credence(world, learner, teacher, evidence=0.15 if holds else 0.0)
        o = _openness(learner, parent)
        own = learner.itemval.get(sig)
        bad = own is not None and own < -0.1 and ("m:" + sig) not in learner.heard
        g = random.Random()
        g.setstate(world.rng.getstate())
        draw = g.random()
        known = sig in learner.recipes
        follow = can_follow(learner, recipe)
        if known:
            gate = "g1"
        elif bad:
            gate = "g2"
        elif draw >= c * o:
            gate = "g3"
        elif not follow:
            gate = "g4"
        else:
            gate = "taken"
        return {"sig": sig, "c": c, "o": o, "p": c * o, "gate": gate, "follow": follow}

    # --- the lesson wrapper ----------------------------------------------------------------------------------
    def lesson(self, orig, world, learner, teacher, meant, recipe, claim, parent, part_lesson):
        info = self.gate_info(world, learner, teacher, meant, recipe, parent)
        tick = world.tick
        era = era_of(tick)
        if not part_lesson:
            fail = None
            if info["gate"] == "g4":
                fail = self.open_failure(world, learner, teacher, meant, recipe, tick, era, info["p"])
            self.ctx.append({"claim": claim, "c": info["c"], "part": False, "meant": meant, "fail": fail,
                             "part_seen": False})
            before = set(learner.recipes)
            out = orig(world, learner, teacher, meant, recipe, claim, parent, part_lesson)
            ctx = self.ctx.pop()
            if info["gate"] != "g4" and (info["gate"] == "taken") != bool(out):
                self.mismatch["outcome"] += 1
            if fail is not None:
                sel = fail["sel"]
                if (sel is None) != (not ctx["part_seen"]):
                    self.mismatch["part_selection"] += 1
            if info["gate"] == "taken":
                key = (learner.id, meant)
                if key in self.chains:                         # the whole taken again after a G4 failure
                    ch = self.chains[key]
                    if ch[CHAIN.index("wt")] is None:
                        ch[CHAIN.index("wt")] = tick
            return out
        # a part lesson, shown by parts-first inside the whole lesson above
        parent_ctx = self.ctx[-1] if self.ctx else None
        fail = parent_ctx["fail"] if parent_ctx else None
        if parent_ctx is not None:
            parent_ctx["part_seen"] = True
            if fail is None or fail["sel"] != meant:
                self.mismatch["part_selection"] += 1
        self.ctx.append({"claim": claim, "c": info["c"], "part": True, "meant": meant, "fail": None,
                         "part_seen": False})
        out = orig(world, learner, teacher, meant, recipe, claim, parent, part_lesson)
        self.ctx.pop()
        if (info["gate"] == "taken") != bool(out):
            self.mismatch["outcome_part"] += 1
        if fail is not None:
            cell = self.cells[fail["cell"]]
            cell[f"pl_{info['gate']}"] += 1
            cell["pl_variant"] += info["sig"] != meant
            if info["gate"] in ("g3", "g4", "taken"):
                cell["pl_reached_g3"] += 1
                cell["pl_sum_p"] += info["p"]
            kept = info["gate"] == "taken" and info["sig"] in learner.recipes
            cell["pl_kept"] += kept
            ch = self.chains.get(fail["key"])
            if ch is not None and info["gate"] == "taken":
                if ch[CHAIN.index("pt")] is None:
                    ch[CHAIN.index("pt")] = tick
                if kept and ch[CHAIN.index("pk")] is None:
                    ch[CHAIN.index("pk")] = tick
        return out

    def open_failure(self, world, learner, teacher, meant, recipe, tick, era, p_whole):
        from acl.knowhow import can_follow
        self.n_fail += 1
        origin, usef = self.origin(meant), int(self.useful(meant))
        direct, allm, depth = self.missing(learner, teacher, recipe)
        known_parts = [x for x in made_parts(recipe) if x in teacher.recipes]
        sel = known_parts[0] if known_parts else None
        if sel is None:
            cls = "none"
        elif sel in learner.recipes:
            cls = "wrong"
        elif not can_follow(learner, teacher.recipes[sel]):
            cls = "deep"
        else:
            cls = "reach"
        other = any(x in teacher.recipes and x != sel for x in direct)
        ckey = f"{era}|{origin}|{usef}|{cls}"
        cell = self.cells[ckey]
        cell["fail"] += 1
        cell["whole_sum_p"] += p_whole
        cell["teacher_knew_missing_other"] += other and (sel is None or sel not in direct)
        cell["teacher_knows_a_missing"] += any(x in teacher.recipes for x in direct)
        cell["nmiss_direct"] += len(direct)
        cell["nmiss_all"] += len(allm)
        cell[f"depth_{min(depth, 3)}"] += 1
        key = (learner.id, meant)
        rel, age = relation(world, teacher, learner), age_band(learner.age(tick))
        ch = self.chains.get(key)
        if ch is None:
            ch = [tick, era, origin, usef, rel, age, cls, len(direct), len(allm), depth, 0, 0,
                  None, None, None, None, None, None, None, None]
            self.chains[key] = ch
            self.cmeta[key] = {"sel": sel if cls == "reach" else None, "need": set(direct), "sel_any": sel}
            self.by_learner[learner.id].add(key)
            if not direct:
                ch[CHAIN.index("ah")] = tick
        ch[CHAIN.index("fails")] += 1
        if cls == "reach":
            ch[CHAIN.index("ever_reach")] = 1
            if self.cmeta[key]["sel"] is None:
                self.cmeta[key]["sel"] = sel
        return {"key": key, "sel": sel, "cell": ckey}

    # --- the memory wrapper ----------------------------------------------------------------------------------
    def memory(self, orig, world, p, sig, recipe, how, source, props, meant):
        from acl.knowhow import MAX_RECIPES
        tick = world.tick
        if world is self.w and how in ("made", "heated") and sig not in world.knowledge and p.birth < 0:
            self.founder_kinds.add(sig)
        fresh = sig not in p.recipes
        over = fresh and len(p.recipes) + 1 > MAX_RECIPES
        pred = None
        if over:
            vals = {s: p.itemval.get(s, 0.0) for s in p.recipes}
            vals[sig] = p.itemval.get(sig, 0.0)
            pred = min(vals, key=lambda s: (vals[s], s))
        before = set(p.recipes)
        out = orig(world, p, sig, recipe, how, source, props, meant)
        if over:
            gone = (before | {sig}) - set(p.recipes)
            actual = next(iter(gone)) if len(gone) == 1 else None
            if actual != pred:
                self.mismatch["eviction_pred"] += 1
            if how == "taught" and self.ctx:
                self.n_mem += 1
                ctx = self.ctx[-1]
                lm = ctx["meant"]
                ckey = f"mem|{era_of(tick)}|{self.origin(lm)}|{int(self.useful(lm))}|{'part' if ctx['part'] else 'whole'}"
                cell = self.cells[ckey]
                cell["n"] += 1
                cell["evict_new"] += pred == sig
                cell["sum_evicted_val"] += vals[pred]
                low = vals[pred]
                ties = sum(1 for v in vals.values() if v == low)
                cell["sum_ties"] += ties
                cell["tied"] += ties > 1
                cell["evicted_composite"] += pred.startswith("(")
                cell["held_composite"] += sum(1 for s in vals if s.startswith("(")) / len(vals)
                lv = max(vals[sig], 0.5 * ctx["claim"] * ctx["c"])
                vals2 = dict(vals)
                vals2[sig] = lv
                pred2 = min(vals2, key=lambda s: (vals2[s], s))
                cell["replay_survive"] += pred2 != sig
                cell["replay_survive_if_evicted"] += (pred == sig) and (pred2 != sig)
                cell["sum_replay_evicted_val"] += vals2[pred2]
                cell["sum_lesson_val"] += lv
                self.evicted[p.id][pred] = (tick, ckey)
        if fresh and sig in p.recipes:
            self.gained(p, sig, tick, how)
        return out

    def gained(self, p, sig, tick, how):
        e = self.evicted.get(p.id)
        if e and sig in e:
            t0, ckey = e.pop(sig)
            cell = self.cells[ckey]
            cell["relearned"] += 1
            cell["sum_relearn_weeks"] += tick - t0
            cell[f"relearned_{how}"] += 1
        for key in list(self.by_learner.get(p.id, ())):
            ch, meta = self.chains[key], self.cmeta[key]
            if sig in meta["need"]:
                meta["need"].discard(sig)
                if not meta["need"] and ch[CHAIN.index("ah")] is None:
                    ch[CHAIN.index("ah")] = tick
            if sig == key[1] and ch[CHAIN.index("wh")] is None:
                ch[CHAIN.index("wh")] = tick

    # --- weekly events ----------------------------------------------------------------------------------------
    def __call__(self, world, events):
        if (world.tick - 1) % WPY == 0:                  # population, once a year
            cell = self.cells[f"pop|{era_of(world.tick - 1)}"]
            cell["years"] += 1
            cell["sum_pop"] += len(world.living())
        for ev in events:
            k = ev["k"]
            if k in ("make", "play"):
                thing = ev.get("thing")
                a = ev.get("a")
                if not thing or a not in self.by_learner:
                    continue
                for key in self.by_learner[a]:
                    ch, meta = self.chains[key], self.cmeta[key]
                    if meta["sel"] is not None and thing == meta["sel"] and ch[CHAIN.index("pm")] is None:
                        ch[CHAIN.index("pm")] = ev["t"]
                    if thing == key[1] and ch[CHAIN.index("wm")] is None:
                        ch[CHAIN.index("wm")] = ev["t"]
            elif k == "death":
                a = ev.get("a")
                for key in self.by_learner.pop(a, ()):
                    self.chains[key][CHAIN.index("end")] = ev["t"]
                self.evicted.pop(a, None)

    def results(self):
        return {"cells": {k: dict(v) for k, v in self.cells.items()}, "mismatch": dict(self.mismatch),
                "chain_fields": CHAIN, "chains": [[k[0], k[1]] + v for k, v in self.chains.items()]}


def install(w, obs):
    from acl import information, knowhow
    orig = information.hear_how
    orig_rem = knowhow.remember_recipe

    def remember_recipe(world, p, sig, recipe, how, source=None, props=None, meant=None):
        if world is not w:
            return orig_rem(world, p, sig, recipe, how, source, props, meant)
        return obs.memory(orig_rem, world, p, sig, recipe, how, source, props, meant)

    def hear_how(world, learner, teacher, meant, recipe, claim, parent, part_lesson=False):
        if world is not w:
            return orig(world, learner, teacher, meant, recipe, claim, parent, part_lesson)
        return obs.lesson(orig, world, learner, teacher, meant, recipe, claim, parent, part_lesson)

    knowhow.remember_recipe = remember_recipe
    information.hear_how = hear_how


def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = PT1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        res = obs.results()
        extra = ":" + json.dumps({**res["mismatch"], "_fail": obs.n_fail, "_mem": obs.n_mem,
                                  "_chains": len(res["chains"])}, sort_keys=True, separators=(",", ":"))
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
    for seed, years in ((501, 20), (601, 60)):
        a = call("hashrun", "lp", seed, years, 1)
        b = call("hashrun", "lp", seed, years, 0)
        same = a.split(":")[:2] == b.split(":")[:2]
        info = json.loads(a.split(":", 2)[2]) if a.count(":") >= 2 else {"?": 1}
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = same and not any(mism.values()) and info.get("_fail", 0) > 0 and info.get("_mem", 0) > 0
        ok &= t
        lines.append(f"arm lp, seed {seed}, {years} years: identical with and without the observer (state and random "
                     f"numbers): {'yes' if same else 'NO'}; outcome, part-selection and eviction mismatches: "
                     f"{mism or 'none'}; G4 failures {info.get('_fail')}, lesson memory overflows {info.get('_mem')}, "
                     f"chains {info.get('_chains')}")
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
    obs = PT1Obs(w)
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
    print(f"{arm} seed {seed}: done, tick {w.tick}, mismatches {res['mismatch']}, chains {len(res['chains'])}",
          flush=True)


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
