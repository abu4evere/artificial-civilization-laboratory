"""PM1 — why are the parts of new kinds never made again? (questions.md, frozen as `PM1-frozen`). Read-only: one arm on
`code_v16`, LP, seeds 25001-25032, 200 years; kinds born in years 100-190 are followed for 5 years each (MP1's rule).

For each followed kind K (world-new, needing at least one made part) and each of its direct made parts X, at every
decision of a person who knows K, the furthest part-making stage reached:
  P0  X's recipe not known (P0a: no living person knows it; P0b: someone else does)
  P1  known, but the inputs are not in hand (or a heat recipe with no fire here)
  P2  inputs in hand, but X is not valued enough to be eligible (the make block's own value test)
  P3  eligible, but making X is not the make option offered (too young, too tired, the utility floor, or another
      recipe won the single make slot)
  P4  offered, but not chosen
  P5  chosen
  P6  X made (a make or play event of X by a knower of K)
  P7  all of K's made parts held at once by one knower (MP1's C, D or E)

The make block's state is read exactly where the code reads it: a wrapper on `mind._wanted_parts` (called only there)
recomputes the block's candidates with the code's own functions (no random draw); `thought.steer` gives the options
offered; `mind.decide` gives the choice. Nothing is changed.

  python experiments/PM1_part_making/run_pm1.py zero
  python experiments/PM1_part_making/run_pm1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.CODES["v16"] = HERE.parent / "NV16_nature_v16" / "code_v16"
CODE = "v16"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(25001, 25033))        # 32 new seeds, used by no study
ARMS = {"c": dict(base.LP)}
JOBS = [f"c:{s}" for s in SEEDS]
OUT = HERE / "output"
WIN = [100 * WPY, 190 * WPY]
FOLLOW = 5 * WPY
CUR = []
P3_REASONS = ("age", "energy", "floor", "other_won")


def made_parts(recipe):
    from acl.matter import MATERIALS
    out = [x for x in recipe.get("parts", ()) if x not in MATERIALS]
    if recipe.get("verb") == "heat" and recipe.get("part") not in MATERIALS:
        out.append(recipe["part"])
    return out


def depth(sig, knowledge, memo, seen=()):
    if sig in memo:
        return memo[sig]
    rec = knowledge.get(sig)
    if rec is None or sig in seen:
        return 0
    parts = made_parts(rec["recipe"])
    d = 0 if not parts else 1 + max(depth(x, knowledge, memo, seen + (sig,)) for x in parts)
    memo[sig] = d
    return d


class PM1Obs:
    def __init__(self, w):
        self.w = w
        self.kinds = {}            # sig -> dict
        self.memo = {}
        self.known_any = set()
        self.known_tick = -1
        self.chk = Counter()
        self.slot = Counter()      # P3 'other_won': what won the slot
        self.instead = Counter()   # P4: what was chosen instead
        self.ctx = None            # the make block's candidates for the person deciding now
        CUR[:] = [self]

    def active(self, tick):
        return {k: kd for k, kd in self.kinds.items() if kd["t0"] < tick <= kd["t0"] + FOLLOW}

    def refresh_known(self, world):
        if self.known_tick != world.tick:
            self.known_any = set()
            for q in world.living():
                self.known_any.update(q.recipes)
            self.known_tick = world.tick

    # called from the _wanted_parts wrapper, inside decide's make block
    def make_block(self, world, p, part_of):
        from acl import inquiry
        from acl.knowhow import belief
        from acl.mind import can_make, hunger_of, _holding
        c = world.cfg
        deps = world.dependents(p.id)
        dep_need = sum(d.need(c, world.tick) for d in deps)
        hunger = hunger_of(world, p, dep_need)
        fire_here = world.tile(p.loc).fire > 0
        season = world.season
        g = p.genes
        info = {}
        cands = []
        for sig, recipe in p.recipes.items():
            if recipe["verb"] == "heat" and not fire_here:
                info[sig] = "inputs"
                continue
            v = max(p.itemval.get(sig, 0.0), part_of.get(sig, 0.0))
            if recipe["verb"] == "strike":
                v = max(v, belief(p, f"{recipe['target']}/{recipe['tool']}@{season}") or 0.0)
            v = max(v, 0.5 * max(inquiry.pull(p, "m:" + sig), inquiry.pull(p, "f:" + sig)))
            if not can_make(p, recipe):
                info[sig] = "inputs"
                continue
            if v <= 0.05 or (_holding(p, sig) and v == p.itemval.get(sig, 0.0)):
                info[sig] = "value"
                continue
            u = c.worth_weight * v * (0.6 + 0.4 * g["diligence"]) * (1.0 - 0.5 * hunger)
            cands.append((sig, v, u))
            info[sig] = "eligible"
        best, best_u = None, 0.05
        for sig, v, u in cands:
            if u > best_u:
                best, best_u = sig, u
        self.ctx = {"pid": p.id, "info": info, "cands": {s: u for s, _, u in cands}, "best": best}

    def decided(self, world, p, offered, chosen):
        from acl.mind import COST
        ctx, self.ctx = self.ctx, None
        tick = world.tick
        # zero check: the make option offered is the one the block's own rule predicts
        if ctx is not None and ctx["pid"] == p.id:
            predicted = ctx["best"] if p.energy >= COST["make"] else None
            got = offered.get("make")
            self.chk["looks"] += 1
            self.chk["make_mismatch"] += int(predicted != got)
        else:                                   # the make block did not run (too young): no make option at all
            self.chk["looks_no_block"] += 1
            self.chk["make_mismatch"] += int(offered.get("make") is not None)
        act = self.active(tick)
        if not act:
            return
        ks = [k for k in p.recipes if k in act]
        if not ks:
            return
        self.refresh_known(world)
        stage_gate = ctx is not None and ctx["pid"] == p.id     # the make block ran for this person (age gate passed)
        for k in ks:
            kd = act[k]
            for x in kd["parts"]:
                if x not in p.recipes:
                    st = 0
                    if x in self.known_any:
                        kd["p0b"] = 1
                elif not stage_gate:
                    st = 3
                    kd["p3"]["age"] += 1
                else:
                    why = ctx["info"].get(x, "inputs")
                    if why == "inputs":
                        st = 1
                    elif why == "value":
                        st = 2
                    elif offered.get("make") == x:
                        st = 5 if chosen == ("make", x) else 4
                        if st == 4:
                            self.instead[chosen[0] if chosen else "none"] += 1
                    else:
                        st = 3
                        if p.energy < COST["make"]:
                            kd["p3"]["energy"] += 1
                        elif ctx["cands"].get(x, 0.0) <= 0.05:
                            kd["p3"]["floor"] += 1
                        else:
                            kd["p3"]["other_won"] += 1
                            w = offered.get("make")
                            self.slot["another part of the kind" if w in kd["parts"] else
                                      ("another new kind" if w in self.kinds else "an old recipe")] += 1
                kd["stage"] = max(kd["stage"], st)

    def __call__(self, world, events):
        from acl.mind import can_make
        tick = world.tick - 1
        for ev in events:
            if ev["k"] not in ("make", "play") or ev.get("thing") is None:
                continue
            sig = ev["thing"]
            maker = world.people.get(ev.get("a"))
            for k, kd in self.kinds.items():
                if kd["t0"] < tick <= kd["t0"] + FOLLOW and sig in kd["parts"] and maker is not None \
                        and k in maker.recipes:
                    kd["stage"] = max(kd["stage"], 6)
                    kd["made_events"] += 1
            if sig in self.kinds:
                continue
            rec = world.knowledge.get(sig)
            if rec is not None and rec.get("first_tick") == tick and rec.get("first_by") == ev.get("a") \
                    and WIN[0] <= tick < WIN[1]:
                parts = sorted(set(made_parts(rec["recipe"])))
                if parts:
                    self.kinds[sig] = {"t0": tick, "inv": ev.get("a"), "parts": parts,
                                       "need": Counter(made_parts(rec["recipe"])), "stage": 0, "p0b": 0,
                                       "p3": Counter(), "depth": depth(sig, world.knowledge, self.memo),
                                       "valued": 0, "made_events": 0, "all_held": 0}
        act = {k: kd for k, kd in self.kinds.items() if kd["t0"] < tick <= kd["t0"] + FOLLOW}
        if not act:
            return
        for q in world.living():
            ks = [k for k in q.recipes if k in act]
            if not ks:
                continue
            have = Counter(it["sig"] for it in q.items)
            for k in ks:
                kd = act[k]
                if all(have[x] >= n for x, n in kd["need"].items()):
                    kd["stage"] = max(kd["stage"], 7)
                    kd["all_held"] += 1
                if q.id == kd["inv"] and q.itemval.get(k, 0.0) > 0:
                    kd["valued"] = 1

    def results(self):
        out = Counter()
        p3 = Counter()
        for kd in self.kinds.values():
            s = kd["stage"]
            lab = ("P0b" if kd["p0b"] else "P0a") if s == 0 else f"P{s}"
            out[f"stage_{lab}"] += 1
            out["kinds"] += 1
            out[f"depth{min(kd['depth'], 3)}_{lab}"] += 1
            out[f"valued{kd['valued']}_{lab}"] += 1
            out[f"valued{kd['valued']}"] += 1
            if s == 3:
                p3.update(kd["p3"])
            if s == 6 and kd["made_events"] == 0:        # P7 may come from parts held without a new make
                self.chk["made_without_event"] += 1
            if s == 7 and kd["all_held"] == 0:
                self.chk["p7_without_all"] += 1
        return {"stages": dict(out), "p3_reasons": dict(p3), "slot": dict(self.slot), "instead": dict(self.instead),
                "check": dict(self.chk)}


def install():
    from acl import mind, thought
    if getattr(mind.decide, "_pm1", False):
        return
    dec0, steer0, wanted0 = mind.decide, thought.steer, mind._wanted_parts
    cur = {"world": None, "pid": None, "offered": {}}

    def wanted(p):
        out = wanted0(p)
        o = CUR[0] if CUR else None
        if o is not None and cur["world"] is not None and cur["pid"] == p.id:
            o.make_block(cur["world"], p, out)
        return out

    def steer(p, options):
        if cur["pid"] == p.id:
            cur["offered"] = {o[1]: o[2] for o in options if o[1] == "make"}
        return steer0(p, options)

    def decide(world, p):
        o = CUR[0] if CUR else None
        if o is None:
            return dec0(world, p)
        cur["world"], cur["pid"], cur["offered"] = world, p.id, {}
        o.ctx = None
        try:
            chosen = dec0(world, p)
        finally:
            cur["world"], cur["pid"] = None, None
        o.decided(world, p, cur["offered"], chosen)
        return chosen
    decide._pm1 = True
    mind.decide, thought.steer, mind._wanted_parts = decide, steer, wanted


def make(seed, arm="c", code=CODE):
    base.setup(code)
    return base.make_world(seed, dict(ARMS[arm]))


def hashrun(code, seed, years, observe):
    WIN[0], WIN[1] = 0, (years - 5) * WPY
    w = make(seed, "c", code)
    obs = None
    if observe:
        install()
        obs = PM1Obs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results()
        extra = ":" + json.dumps({"stages": {k: v for k, v in r["stages"].items() if k.startswith("stage_")},
                                  "check": r["check"], "p3": r["p3_reasons"]}, sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def reload_check(seed):
    w = make(seed)
    from acl.world import World
    for _ in range(10 * WPY):
        w.step()
    b = World.from_dict(json.loads(json.dumps(w.to_dict())))
    for x in (w, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(w) == base.world_hash(b)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.strip().splitlines()[-1]

    def hs(x):
        return x.split(":")[:2]
    lines, ok = [], True
    from concurrent.futures import ThreadPoolExecutor
    specs = [(seed, years, obs) for seed, years in ((501, 20), (601, 60)) for obs in (0, 1)]
    with ThreadPoolExecutor(2) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", CODE, *sp), specs)))
        chk = ex.submit(call, "hashrun", CODE, 701, 30, 1)
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
    for seed, years in ((501, 20), (601, 60)):
        ro = hs(got[(seed, years, 0)]) == hs(got[(seed, years, 1)])
        ok &= ro
        lines.append(f"seed {seed}, {years} years: observer read-only (world and random stream): {'yes' if ro else 'NO'}; "
                     f"{got[(seed, years, 1)].split(':', 2)[2]}")
    info = json.loads(chk.result().split(":", 2)[2])
    ch = info["check"]
    t = (ch.get("looks", 0) > 0 and ch.get("make_mismatch", 0) == 0 and ch.get("made_without_event", 0) == 0
         and ch.get("p7_without_all", 0) == 0)
    ok &= t
    lines.append(f"seed 701, 30 years: eligibility check (the make option offered is exactly the one the block's own rule "
                 f"predicts, at every look) and event checks: {'yes' if t else 'NO'}; {info}")
    t = rl.result()[-1:] == ["True"]
    ok &= t
    lines.append(f"seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_v16 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = make(seed, arm)
    install()
    obs = PM1Obs(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_v16", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, check {res['check']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] == "1"))
    elif cmd == "reload":
        base.setup(CODE)
        print(reload_check(int(sys.argv[2])))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: kinds from the start; never study data
        WIN[0], WIN[1] = 0, (int(sys.argv[4]) - 5) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
