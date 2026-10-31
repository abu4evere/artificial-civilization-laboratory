"""IW1 — how does the worth of made things form? (questions.md, frozen as `IW1-frozen`). Read-only on `code_v9` (live
nature). The observer reads the law's events; wrappers call the original unchanged and only note the state at that
moment:
  knowhow.judge_item      each use of a made thing: felt help, worth before and after, which law called it;
  knowhow.remember_recipe how a person first got a kind (made, taught, watched, read ...), and kinds pushed out by the
                          12-recipe limit;
  knowhow.forget_useless  kinds forgotten as useless;
  thought.steer           every week's options: when making is offered, its kind, worth, prior uses, and which term
                          carries its worth (recomputed and checked against the option's own score).

  python experiments/IW1_item_worth/run_iw1.py zero
  python experiments/IW1_item_worth/run_iw1.py one <arm> <seed> <years> <out>
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
CODE = EXP / "NV9_nature_v9" / "code_v9"
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(20901, 20933))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9991, 9990)
V9 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1,
      "ground_items": 1, "curiosity_pull": 1}
LP = {"founders": 80, "width": 80, "height": 80}
ARMS = {"lp": {**LP}}
JOBS = [f"lp:{s}" for s in SEEDS]
LATE = (100 * WPY, 200 * WPY)              # years 100-200 (Q1, Q2, Q7, Q8)
ADULT = 16 * WPY
MAXN = 10                                  # use-index bins 0..10+ for trajectories (Q3)


def setup():
    sys.path.insert(0, str(CODE))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **{**V9, **kw}))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def rng_state(w):
    return hashlib.sha256(repr(w.rng.getstate()).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODE / "acl")


def ubin(n):
    return "0" if n == 0 else "1-2" if n <= 2 else "3-5" if n <= 5 else "6+"


class IW1Obs:
    def __init__(self, w):
        self.w = w
        self.mismatch = Counter()
        self.n = Counter()
        self.source = {}                        # (pid, sig) -> how first got
        self.cum = defaultdict(lambda: [0, 0.0])  # (pid, sig) -> [uses, sum felt]
        self.kind = defaultdict(lambda: [0, 0.0, 0])  # sig -> [uses, sum felt, makes late by adults]
        self.felt_hist = Counter()              # (caller, felt bin) -> uses
        self.traj = defaultdict(lambda: [0, 0.0, 0.0])  # "source|n" -> [count, sum worth before, sum felt]
        self.makes = []                         # chosen makes, adults, years 100-200
        self.pending = {}                       # pid -> offer record of this week
        self.off = defaultdict(lambda: [0, 0.0])  # sig -> [offers not chosen, sum worth] (adults, late)
        self.off_bins = Counter()               # prior-use bin of offers not chosen
        self.off_src = Counter()
        self.term = Counter()                   # which term carries the offered make's worth (late, adults)
        self.leave = Counter()                  # (reason, helpful/unhelpful/unused) -> person-kinds
        self.known = {}                         # pid -> set of sigs at last census
        self.census = []

    # --- wrappers' notes ---
    def judge(self, world, p, sig, felt, v0, v1, caller):
        felt = max(-1.0, min(1.0, felt))
        key = (p.id, sig)
        c = self.cum[key]
        src = self.source.get(key, "initial")
        t = self.traj[f"{src}|{min(c[0], MAXN)}"]
        t[0] += 1
        t[1] += v0
        t[2] += felt
        c[0] += 1
        c[1] += felt
        k = self.kind[sig]
        k[0] += 1
        k[1] += felt
        fb = "<0" if felt < 0 else "0-0.1" if felt <= 0.1 else "0.1-0.3" if felt <= 0.3 else ">0.3"
        self.felt_hist[f"{caller}|{fb}"] += 1
        self.n["uses"] += 1

    def remembered(self, p, sig, how, fresh, evicted):
        if fresh and (p.id, sig) not in self.source:
            self.source[(p.id, sig)] = how
        for s in evicted:
            self.left(p, s, "limit")

    def forgot(self, p, gone):
        for s in gone:
            self.left(p, s, "forget")

    def left(self, p, sig, reason):
        uses, tot = self.cum.get((p.id, sig), [0, 0.0])
        cls = "unused" if uses == 0 else "helpful" if tot / uses > 0.1 else "unhelpful"
        self.leave[f"{reason}|{cls}"] += 1

    def options(self, world, p, before):
        """An offered make: its kind, the worth the person holds, and which term carries it. Reads only."""
        if p.age(world.tick) < ADULT or not (LATE[0] <= world.tick < LATE[1]):
            return
        mk = [o for o in before if o[1] == "make"]
        if not mk:
            return
        from acl import inquiry
        from acl.knowhow import belief
        from acl.mind import _wanted_parts, hunger_of
        from acl.person import A, N_ACTIONS
        c = world.cfg
        u_opt, _, sig = mk[0]
        recipe = p.recipes[sig]
        iv = p.itemval.get(sig, 0.0)
        part = _wanted_parts(p).get(sig, 0.0)
        bel = 0.0
        if recipe["verb"] == "strike":
            bel = belief(p, f"{recipe['target']}/{recipe['tool']}@{world.season}") or 0.0
        sur = 0.5 * max(inquiry.pull(p, "m:" + sig), inquiry.pull(p, "f:" + sig))
        v = max(iv, part, bel, sur)
        g = p.genes
        hunger = hunger_of(world, p, sum(d.need(c, world.tick) for d in world.dependents(p.id)))
        u = c.worth_weight * v * (0.6 + 0.4 * g["diligence"]) * (1.0 - 0.5 * hunger)
        b = p.last_ctx * N_ACTIONS
        if c.curiosity_pull:
            n = p.tried[b + A["make"]] if p.tried is not None else 0
            u += 0.3 * g["curiosity"] * (1.0 - hunger) / (1 + n)
        u += c.learned_weight * p.q[b + A["make"]]
        if abs(u - u_opt) > 1e-9:
            self.mismatch["make_score_recompute"] += 1
        term = max((("itemval", iv), ("part", part), ("belief", bel), ("surprise", sur)), key=lambda x: x[1])[0]
        uses = self.cum.get((p.id, sig), [0, 0.0])[0]
        self.pending[p.id] = {"sig": sig, "iv": iv, "uses": uses, "term": term,
                              "src": self.source.get((p.id, sig), "initial")}

    # --- events ---
    def __call__(self, world, events):
        tick = world.tick - 1
        made = {ev["a"]: ev.get("thing") for ev in events if ev["k"] == "make" and "a" in ev}
        for pid, rec in self.pending.items():
            self.term[rec["term"]] += 1
            self.n["offered"] += 1
            if made.get(pid) == rec["sig"]:
                c = self.cum[(pid, rec["sig"])]
                self.makes.append([rec["sig"], round(rec["iv"], 6), rec["uses"], rec["src"], c[0], round(c[1], 6),
                                   pid])
                self.kind[rec["sig"]][2] += 1
                self.n["made_offered"] += 1
            else:
                o = self.off[rec["sig"]]
                o[0] += 1
                o[1] += rec["iv"]
                self.off_bins[ubin(rec["uses"])] += 1
                self.off_src[rec["src"]] += 1
        self.pending = {}
        for ev in events:
            if ev["k"] == "make":
                self.n["make_events"] += 1
        if tick % WPY == WPY - 1:
            living = world.living()
            now = {p.id: set(p.recipes) for p in living}
            for pid, sigs in self.known.items():
                if pid not in now:
                    for s in sigs:
                        uses, tot = self.cum.get((pid, s), [0, 0.0])
                        cls = "unused" if uses == 0 else "helpful" if tot / uses > 0.1 else "unhelpful"
                        self.leave[f"death|{cls}"] += 1
            self.known = now
            self.census.append([tick // WPY, len(living), sum(1 for p in living if p.age(world.tick) >= ADULT)])

    def results(self):
        # each chosen make, with the maker's cumulative uses and felt help of that kind at the end of the run:
        # the maker's later mean felt = (felt at the end - felt at the make) / (uses at the end - uses at the make)
        self.makes_out = [m + [*map(lambda x: round(x, 6), self.cum[(m[6], m[0])])] for m in self.makes]
        self.makes_out = [m[:6] + m[7:] for m in self.makes_out]
        return {"counts": dict(self.n), "mismatch": dict(self.mismatch),
                "makes_fields": ["sig", "itemval", "prior_uses", "source", "cum_uses_at_make", "cum_felt_at_make",
                                 "cum_uses_end", "cum_felt_end"],
                "makes": self.makes_out,
                "kinds_fields": ["uses", "felt_sum", "late_adult_makes", "offers_not_chosen", "offer_worth_sum"],
                "kinds": {s: [k[0], round(k[1], 6), k[2], self.off[s][0], round(self.off[s][1], 6)]
                          for s, k in self.kind.items()} | {s: [0, 0.0, 0, o[0], round(o[1], 6)]
                                                            for s, o in self.off.items() if s not in self.kind},
                "offer_bins": dict(self.off_bins), "offer_sources": dict(self.off_src), "terms": dict(self.term),
                "traj": {k: [v[0], round(v[1], 6), round(v[2], 6)] for k, v in self.traj.items()},
                "felt_hist": dict(self.felt_hist), "leave": dict(self.leave),
                "census_fields": ["year", "living", "adults"], "census": self.census}


def install(w, obs):
    import sys as _sys
    from acl import knowhow, thought
    orig_judge = knowhow.judge_item
    orig_rem = knowhow.remember_recipe
    orig_forget = knowhow.forget_useless
    orig_steer = thought.steer

    def judge_item(world, p, sig, felt):
        if world is not w:
            return orig_judge(world, p, sig, felt)
        v0 = p.itemval.get(sig, 0.0)
        caller = _sys._getframe(1).f_code.co_name
        out = orig_judge(world, p, sig, felt)
        v1 = p.itemval.get(sig, 0.0)
        f = max(-1.0, min(1.0, felt))
        rate = 0.3 if (abs(v0) > 0.1 and (f > 0.05) != (v0 > 0.05)) else 0.15
        if abs(max(-1.0, min(1.0, v0 + rate * (f - v0))) - v1) > 1e-12:
            obs.mismatch["judge_replay"] += 1
        obs.judge(world, p, sig, felt, v0, v1, caller)
        return out

    def remember_recipe(world, p, sig, recipe, how, source=None, props=None, meant=None):
        if world is not w:
            return orig_rem(world, p, sig, recipe, how, source, props, meant)
        before = set(p.recipes)
        fresh = sig not in p.recipes
        out = orig_rem(world, p, sig, recipe, how, source, props, meant)
        evicted = before - set(p.recipes)
        obs.remembered(p, sig, how, fresh and sig in p.recipes, evicted)
        if fresh and sig not in p.recipes:
            obs.left(p, sig, "limit")          # the new kind itself was the one pushed out
        return out

    def forget_useless(p):
        before = set(p.recipes)
        out = orig_forget(p)
        if w.people.get(p.id) is p:
            obs.forgot(p, before - set(p.recipes))
        return out

    def steer(p, options):
        before = list(options)
        out = orig_steer(p, options)
        if w.people.get(p.id) is p:
            obs.options(w, p, before)
        return out

    knowhow.judge_item = judge_item
    knowhow.remember_recipe = remember_recipe
    knowhow.forget_useless = forget_useless
    thought.steer = steer


def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = IW1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        extra = ":" + json.dumps({**obs.mismatch, "_uses": obs.n["uses"], "_offered": obs.n["offered"],
                                  "_made": obs.n["made_offered"], "_make_events": obs.n["make_events"]},
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
    # 120 years at the second seed, so that the late window (years 100-200) is entered and offers are checked
    specs = [(seed, years, obs) for seed, years in ((501, 20), (601, 120)) for obs in (1, 0)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", "lp", *sp), specs)))
    for seed, years in ((501, 20), (601, 120)):
        a, b = got[(seed, years, 1)], got[(seed, years, 0)]
        same = a.split(":")[:2] == b.split(":")[:2]
        info = json.loads(a.split(":", 2)[2])
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = same and not any(mism.values()) and info.get("_uses", 0) > 0
        if years > 100:
            t = t and info.get("_offered", 0) > 0
        ok &= t
        lines.append(f"arm lp, seed {seed}, {years} years: identical with and without the observer and wrappers "
                     f"(state and random numbers): {'yes' if same else 'NO'}; replay mismatches (worth update, make "
                     f"score): {mism or 'none'}; uses {info.get('_uses')}, offered makes (adults, years 100+) "
                     f"{info.get('_offered')}, chosen {info.get('_made')}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm lp, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_v9 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = IW1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v9 (read-only)", "code_hash": f0, "code_hash_after": fingerprint(),
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
