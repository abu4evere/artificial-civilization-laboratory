"""MO1 — the memory order (questions.md, frozen as `MO1-frozen`). Nature-change study: `code_mo1` = `code_v7` + one
setting, `lesson_value_first` (0 = v7 exactly; v7_to_mo1.diff). Arms c (v7), o (setting 1), s (sham: one extra draw in
week one). A read-only observer wraps `knowhow.remember_recipe` and reads weekly events and a yearly census.

  python experiments/MO1_memory_order/run_mo1.py zero
  python experiments/MO1_memory_order/run_mo1.py one <arm> <seed> <years> <out>
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
CODES = {"mo1": HERE / "code_mo1", "v7": EXP / "NV7_nature_v7" / "code_v7"}
CODE = CODES["mo1"]
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(18901, 18933))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9945, 9944)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
LP = {"founders": 80, "width": 80, "height": 80}
ARMS = {"c": {**LP}, "o": {**LP, "lesson_value_first": 1}, "s": {**LP, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
USES = ("forage", "hunt", "wood", "stone", "fiber", "fight", "carry", "cold")
LEARNED = ("taught", "copied")


def setup(code="mo1"):
    sys.path.insert(0, str(CODES[code]))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


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


def fingerprint(code="mo1"):
    from run_e7 import code_hash
    return code_hash(CODES[code] / "acl")


def maxf(props):
    from acl.matter import factor
    if not props or "edge" not in props:
        return 1.0
    return max(factor(props, u) for u in USES)


class MO1Obs:
    def __init__(self, w):
        self.w = w
        self.useful_cache = {}
        self.founder_kinds = set()
        for p in w.living():
            self.founder_kinds.update(p.recipes)
        self.mismatch = Counter()
        self.c = defaultdict(float)                  # pooled counters
        self.pending = []                            # [tick, learner, sig, how]: learned recipes awaiting the 52-week check
        self.last_make = {}                          # (person, sig) -> last week they made it
        self.evicted = {}                            # (person, sig) -> week evicted by a learning overflow
        self.census = []                             # per year: [year, living, adults, recipes, useful, makes, wb_kinds]
        self.makes_year = 0
        self.n_learned = 0
        self.n_over = 0

    def useful(self, sig):
        if sig not in self.useful_cache:
            props = (self.w.knowledge.get(sig) or {}).get("props")
            if props is None:
                return False
            self.useful_cache[sig] = maxf(props) > 1.0
        return self.useful_cache[sig]

    def memory(self, orig, world, p, sig, recipe, how, source, props, meant):
        from acl.knowhow import MAX_RECIPES
        tick = world.tick
        if how in ("made", "heated") and sig not in world.knowledge and p.birth < 0:
            self.founder_kinds.add(sig)
        fresh = sig not in p.recipes
        over = fresh and len(p.recipes) + 1 > MAX_RECIPES
        vals = pred = None
        if over:
            vals = {s: p.itemval.get(s, 0.0) for s in p.recipes}
            vals[sig] = p.itemval.get(sig, 0.0)
            pred = min(vals, key=lambda s: (vals[s], s))
        before = set(p.recipes)
        out = orig(world, p, sig, recipe, how, source, props, meant)
        if over:
            gone = (before | {sig}) - set(p.recipes)
            if len(gone) != 1 or next(iter(gone)) != pred:
                self.mismatch["eviction_pred"] += 1
        if fresh and (p.id, sig) in self.evicted:
            t0 = self.evicted.pop((p.id, sig))
            self.c["relearned"] += 1
            self.c["relearn_weeks"] += tick - t0
        if how in LEARNED and fresh:
            self.n_learned += 1
            c = self.c
            c[f"learned_{how}"] += 1
            if over:
                self.n_over += 1
                c["over"] += 1
                c[f"over_{how}"] += 1
                survived = pred != sig
                c["over_survived"] += survived
                c[f"over_survived_{how}"] += survived
                c["evicted_val_sum"] += vals[pred]
                if survived:
                    c["displaced"] += 1
                    c["displaced_val_sum"] += vals[pred]
                    c["displaced_useful"] += self.useful(pred)
                    lm = self.last_make.get((p.id, pred))
                    c["displaced_made_52"] += lm is not None and tick - lm <= WPY
                self.evicted[(p.id, pred)] = tick
            self.pending.append([tick, p.id, sig, how])       # every recipe taken, kept at once or not (P1)
        return out

    def __call__(self, world, events):
        tick = world.tick - 1
        for ev in events:
            if ev["k"] == "make" and ev.get("thing"):
                self.last_make[(ev["a"], ev["thing"])] = ev["t"]
                self.makes_year += 1
        if tick % WPY == WPY - 1:
            self.year_end(world, tick)

    def year_end(self, world, tick):
        living = world.living()
        adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
        rec = sum(len(p.recipes) for p in adults)
        use = sum(sum(1 for s in p.recipes if self.useful(s)) for p in adults)
        wb = {s for p in living for s in p.recipes if s not in self.founder_kinds}
        self.census.append([tick // WPY, len(living), len(adults), rec, use, self.makes_year, len(wb)])
        self.makes_year = 0
        # the 52-week check of learned recipes
        keep = []
        c = self.c
        for t0, pid, sig, how in self.pending:
            if tick - t0 < WPY:
                keep.append([t0, pid, sig, how])
                continue
            p = world.people.get(pid)
            if p is None or not p.alive:
                c["check_censored"] += 1
                continue
            c["checked"] += 1
            c[f"checked_{how}"] += 1
            held = sig in p.recipes
            c["held_52"] += held
            c[f"held_52_{how}"] += held
            c["bad_52"] += p.itemval.get(sig, 0.0) < -0.1
            lm = self.last_make.get((pid, sig))
            c["made_52"] += lm is not None and lm >= t0
        self.pending = keep

    def results(self):
        return {"counts": dict(self.c), "mismatch": dict(self.mismatch), "census_fields":
                ["year", "living", "adults", "recipes_adults", "useful_adults", "makes", "wb_kinds_alive"],
                "census": self.census}


def install(w, obs):
    from acl import knowhow
    orig = knowhow.remember_recipe

    def remember_recipe(world, p, sig, recipe, how, source=None, props=None, meant=None):
        if world is not w:
            return orig(world, p, sig, recipe, how, source, props, meant)
        return obs.memory(orig, world, p, sig, recipe, how, source, props, meant)

    knowhow.remember_recipe = remember_recipe


def hashrun(code, arm, seed, years, observe):
    setup(code)
    kw = dict(ARMS[arm])
    if code == "v7":
        kw.pop("lesson_value_first", None)
    w = make_world(seed, kw)
    obs = None
    if observe:
        obs = MO1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        res = obs.results()
        extra = ":" + json.dumps({**res["mismatch"], "_learned": obs.n_learned, "_over": obs.n_over},
                                 sort_keys=True, separators=(",", ":"))
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
    return world_hash(a) == world_hash(b) and b.cfg.lesson_value_first == 1


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
    specs = [(code, arm, seed, years, obs) for seed, years in ((501, 20), (601, 60))
             for code, arm, obs in (("v7", "c", 0), ("mo1", "c", 0), ("mo1", "o", 1), ("mo1", "o", 0),
                                    ("mo1", "s", 0), ("mo1", "c", 1))]
    with ThreadPoolExecutor(6) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        v7 = got[("v7", "c", seed, years, 0)]
        c0 = got[("mo1", "c", seed, years, 0)]
        o1 = got[("mo1", "o", seed, years, 1)]
        o0 = got[("mo1", "o", seed, years, 0)]
        s0 = got[("mo1", "s", seed, years, 0)]
        c1 = got[("mo1", "c", seed, years, 1)]
        same_v7 = hs(v7) == hs(c0)
        ro = hs(o1) == hs(o0) and hs(c1) == hs(c0)
        acts = hs(o0) != hs(c0)
        sham = hs(s0) != hs(c0)
        info = json.loads(o1.split(":", 2)[2])
        info_c = json.loads(c1.split(":", 2)[2])
        mism = {k: v for d in (info, info_c) for k, v in d.items() if not k.startswith("_")}
        t = same_v7 and ro and acts and sham and not any(mism.values()) and info.get("_over", 0) > 0
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_mo1 with the setting 0 equals code_v7: {'yes' if same_v7 else 'NO'}; "
                     f"observer read-only (arms o and c): {'yes' if ro else 'NO'}; the setting acts: "
                     f"{'yes' if acts else 'NO'}; the sham acts: {'yes' if sham else 'NO'}; eviction-prediction "
                     f"mismatches: {mism or 'none'}; learned recipes (o) {info.get('_learned')}, overflows "
                     f"{info.get('_over')}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm o, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_mo1 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = MO1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "mo1", "code_hash": f0, "code_hash_after": fingerprint(),
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
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "fp":
        setup()
        print(fingerprint())
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
