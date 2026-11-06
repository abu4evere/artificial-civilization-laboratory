"""VA1 — is a new invention valued before it is lost? (questions.md, frozen as `VA1-frozen`). Read-only on live nature
v13 (`code_v13`); ES2's runner supplies the set-up. Wrappers only watch:
  remember_recipe  a world-new kind made in play in years 130-165 (AF1's rule): before it enters, the inventor's other
                   recipes' values (is the cap full? the lowest value it must beat) and v_sim (the mean value of the
                   kinds they know, weighted by property similarity, 1 - mean |difference| / 100, clipped at 0)
  judge_item       every use of a tracked kind by its inventor within 5 years: week, felt, value before and after
  steer            whether a make option for the kind was offered to its inventor
  make             whether the inventor made it again (AF1's lineage rule)
  week's end       recipe held, inputs in hand, not already holding one, valued above 0.05 (LD1's stages); week of loss

  python experiments/VA1_value_at_invention/run_va1.py zero
  python experiments/VA1_value_at_invention/run_va1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.CODES["v13"] = HERE.parent / "NV13_nature_v13" / "code_v13"
CODE = "v13"
WPY, YEARS = base.WPY, 170
SEEDS = tuple(range(23701, 23733))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9883, 9882)
ARMS = {"c": {**base.LP}}
JOBS = [f"c:{s}" for s in SEEDS]
OUT = HERE / "output"
WIN = [130 * WPY, 170 * WPY]
REMAKE = 5 * WPY


class VA1Obs:
    def __init__(self, w):
        self.w = w
        self.kinds = {}
        self.uses = 0
        self.unit = [0, 0]          # [wrong, checked] (zero checks)

    def before_invent(self, world, p, sig, props):
        from acl.knowhow import MAX_RECIPES
        from acl.matter import PROPS
        t = world.tick
        if not (WIN[0] <= t and t + REMAKE <= WIN[1]) or props is None:
            return
        others = [p.itemval.get(s, 0.0) for s in p.recipes if s != sig]
        full = len([s for s in p.recipes if s != sig]) >= MAX_RECIPES
        num = den = 0.0
        for s in p.recipes:
            rec = world.knowledge.get(s)
            if s == sig or rec is None or not rec.get("props"):
                continue
            pr = rec["props"]
            d = sum(abs(props[k] - pr.get(k, 0)) for k in PROPS) / len(PROPS) / 100.0
            wgt = max(0.0, 1.0 - d)
            num += wgt * p.itemval.get(s, 0.0)
            den += wgt
        self.kinds[sig] = {"t": t, "inv": p.id, "recipe": None, "full": int(full),
                           "minval": min(others) if (full and others) else None,
                           "vsim": (num / den) if den > 0 else None,
                           "vmean": (sum(others) / len(others)) if others else None, "uses": [], "lost_at": None, "first": None,
                           "held": 0, "inputs": 0, "free": 0, "offered": 0, "remade": 0}

    def after_invent(self, sig, recipe):
        kd = self.kinds.get(sig)
        if kd is not None and kd["recipe"] is None:
            kd["recipe"] = recipe

    def judged(self, world, p, sig, felt, before, after):
        from acl.util import clamp
        f = clamp(felt, -1.0, 1.0)
        rate = 0.3 if (abs(before) > 0.1 and (f > 0.05) != (before > 0.05)) else 0.15
        self.unit[1] += 1
        self.unit[0] += abs(after - clamp(before + rate * (f - before), -1.0, 1.0)) > 1e-12
        kd = self.kinds.get(sig)
        if kd is not None and p.id == kd["inv"] and kd["t"] <= world.tick < kd["t"] + REMAKE:
            kd["uses"].append([world.tick - kd["t"], round(f, 4), round(before, 4), round(after, 4),
                               int(kd["lost_at"] is None and sig in p.recipes)])

    def offered(self, world, p, options):
        for o in options:
            if o[1] == "make":
                kd = self.kinds.get(o[2])
                if kd is not None and kd["inv"] == p.id and kd["t"] <= world.tick < kd["t"] + REMAKE:
                    kd["offered"] = 1

    def made(self, world, p, sig):
        kd = self.kinds.get(sig)
        if kd is not None and p.id == kd["inv"] and kd["t"] < world.tick <= kd["t"] + REMAKE:
            kd["remade"] = 1

    def __call__(self, world, events):
        from acl.mind import _holding, can_make
        tick = world.tick - 1
        for sig, kd in self.kinds.items():
            if not (kd["t"] <= tick < kd["t"] + REMAKE) or kd["recipe"] is None:
                continue
            p = world.people.get(kd["inv"])
            alive = p is not None and p.alive
            held = alive and sig in p.recipes
            if kd["first"] is None:
                kd["first"] = int(held)
            if not held:
                if kd["lost_at"] is None:
                    kd["lost_at"] = tick - kd["t"]
                continue
            kd["held"] = 1
            if can_make(p, kd["recipe"]):
                kd["inputs"] = 1
                if not _holding(p, sig) and p.itemval.get(sig, 0.0) > 0.05:
                    kd["free"] = 1

    def results(self):
        out = []
        for sig, kd in self.kinds.items():
            st = 5 if kd["remade"] else 4 if kd["offered"] else 3 if kd["free"] else 2 if kd["inputs"] else \
                1 if kd["held"] else 0
            used_before_loss = int(any(u[4] for u in kd["uses"]))
            first_felt = kd["uses"][0][1] if kd["uses"] else None
            out.append([kd["full"], kd["minval"], kd["vsim"], used_before_loss, len(kd["uses"]), first_felt,
                        kd["uses"][0][0] if kd["uses"] else None, kd["lost_at"], kd["first"], st, kd["vmean"]])
        return {"kind_fields": ["full", "minval", "vsim", "used_before_loss", "n_uses", "first_felt", "first_use_week",
                                "lost_week", "held_first_week", "stage", "vmean"], "kinds": out, "n_kinds": len(out),
                "unit": self.unit}


def install(w, obs):
    from acl import actions, knowhow, thought
    o_rem, o_judge, o_steer, o_make = (knowhow.remember_recipe, knowhow.judge_item, thought.steer,
                                       actions.HANDLERS["make"])

    def remember_recipe(world, p, sig, recipe, how, source=None, props=None, meant=None):
        new = sig not in world.knowledge
        if world is w and new and how == "made":
            obs.before_invent(world, p, sig, props)
        out = o_rem(world, p, sig, recipe, how, source, props, meant)
        if world is w and new and how == "made":
            obs.after_invent(sig, recipe)
        return out

    def judge_item(world, p, sig, felt):
        before = p.itemval.get(sig, 0.0)
        out = o_judge(world, p, sig, felt)
        if world is w:
            obs.judged(world, p, sig, felt, before, p.itemval.get(sig, 0.0))
        return out

    def steer(p, options):
        out = o_steer(p, options)
        obs.offered(w, p, out)
        return out

    def make(world, p, sig, eff):
        if world is not w:
            return o_make(world, p, sig, eff)
        n0 = len(world.events)
        out = o_make(world, p, sig, eff)
        if any(ev["k"] == "make" and ev.get("a") == p.id for ev in world.events[n0:]):
            obs.made(world, p, sig)
        return out
    knowhow.remember_recipe = remember_recipe
    knowhow.judge_item = judge_item
    thought.steer = steer
    actions.HANDLERS["make"] = make
    import acl.weather as weather                    # weather imported judge_item by name
    if getattr(weather, "judge_item", None) is o_judge:
        weather.judge_item = judge_item


def hashrun(seed, years, observe):
    WIN[0], WIN[1] = 0, years * WPY
    base.setup(CODE)
    w = base.make_world(seed, ARMS["c"])
    obs = None
    if observe:
        obs = VA1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = f":{len(obs.kinds)},{obs.unit[0]},{obs.unit[1]}" if obs else ""
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    from concurrent.futures import ThreadPoolExecutor
    specs = [(seed, years, o) for seed, years in ((501, 20), (601, 60)) for o in (0, 1)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        a, b = got[(seed, years, 0)], got[(seed, years, 1)]
        ro = a.split(":")[:2] == b.split(":")[:2]
        nk, wrong, checked = b.split(":")[2].split(",")
        unit = wrong == "0" and int(checked) > 0
        t = ro and unit and int(nk) > 0
        ok &= t
        lines.append(f"seed {seed}, {years} years: the observers leave the world unchanged: {'yes' if ro else 'NO'}; "
                     f"kinds tracked {nk}; every use's value = judge_item's rule (wrong {wrong} of {checked}): "
                     f"{'yes' if unit else 'NO'}")
    lines.append(f"code_v13 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    if years < YEARS:                          # a smoke run: kinds from 60% of the run
        WIN[0], WIN[1] = int(years * 0.6) * WPY, years * WPY
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = base.make_world(seed, ARMS["c"])
    obs = VA1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_v13", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, kinds {res['n_kinds']}", flush=True)


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
