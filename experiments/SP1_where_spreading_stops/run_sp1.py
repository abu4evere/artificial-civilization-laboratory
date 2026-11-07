"""SP1 - where does the spreading of new kinds stop? (questions.md, frozen as `SP1-frozen`). Read-only: one arm on
`code_v15`, LP, seeds 24401-24432, 200 years; kinds born in years 100-190 followed to year 200.

The observer wraps, never changes, information.show_how, information.hear_how and knowhow.can_follow, and reads the
week's events, the decision log and people's state at each week's end. Every check it makes is a pure function of
state: it draws no random numbers.

  python experiments/SP1_where_spreading_stops/run_sp1.py zero
  python experiments/SP1_where_spreading_stops/run_sp1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from itertools import islice
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.CODES["v15"] = HERE.parent / "NV15_nature_v15" / "code_v15"
CODE = "v15"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(24401, 24433))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9901, 9900)
ARMS = {"c": dict(base.LP)}
JOBS = [f"c:{s}" for s in SEEDS]
OUT = HERE / "output"
BIRTH = [100 * WPY, 190 * WPY]            # kinds first known in [100, 190) years are followed
CUR = []                                  # the observer of this process (one world per process)
STACK = []                                # frames of hear_how calls in progress (can_follow's result)
OFFERS = []                               # the recomputed offers of the show_how call in progress


class SP1Obs:
    def __init__(self, w):
        self.w = w
        self.n_known = len(w.knowledge)
        self.kinds = {}                          # sig -> record (followed kinds only)
        self.raw = defaultdict(Counter)          # sig -> counts from the wrappers (all sigs; kept for followed)
        self.acq = {}                            # (pid, sig) -> how a non-inventor got it
        self.taken = []                          # (learner, sig) lessons taken this week (any level)
        self.check = Counter()                   # zero-check counters
        CUR[:] = [self]

    def inventor(self, sig):
        rec = self.w.knowledge.get(sig)
        return rec["first_by"] if rec else None

    def __call__(self, world, events):
        tick = world.tick - 1
        # new kinds this week
        learn_by = {}
        for e in events:
            if e["k"] == "learn" and "thing" in e:
                learn_by.setdefault((e.get("a"), e["thing"]), e.get("how"))
        if len(world.knowledge) > self.n_known:
            for sig in islice(world.knowledge, self.n_known, None):
                rec = world.knowledge[sig]
                if BIRTH[0] <= rec["first_tick"] < BIRTH[1]:
                    how = learn_by.get((rec["first_by"], sig), "made")
                    self.kinds[sig] = {"born": rec["first_tick"], "inv": rec["first_by"], "origin": how,
                                       "w": Counter(), "learned": Counter(), "made_other": Counter(), "makers": [],
                                       "learners": []}
            self.n_known = len(world.knowledge)
        # the lessons taken, against the learn events (zero check 3)
        taught = Counter((e.get("a"), e["thing"]) for e in events
                         if e["k"] == "learn" and e.get("how") == "taught" and "thing" in e)
        mine = Counter(self.taken)
        self.check["taken"] += sum(mine.values())
        self.check["taken_mismatch"] += sum(((mine - taught) + (taught - mine)).values())
        self.taken = []
        # events of followed kinds
        for e in events:
            sig = e.get("thing")
            k = self.kinds.get(sig)
            if k is None:
                continue
            a = e.get("a")
            if e["k"] == "learn" and a != k["inv"] and (a, sig) not in self.acq:
                how = e.get("how", "?")
                self.acq[(a, sig)] = how
                k["learned"][how] += 1
                k["learners"].append([a, e["t"], how])
            elif e["k"] == "make":
                if a == k["inv"]:
                    k["w"]["inv_makes"] += 1
                else:
                    how = self.acq.get((a, sig), "own")
                    k["made_other"][how] += 1
                    k["makers"].append([a, e["t"], how])
        # decisions
        for d in world.week_decisions:
            ch = d.chosen
            if ch and ch[0] == "make" and ch[1] in self.kinds:
                k = self.kinds[ch[1]]
                k["w"]["inv_chose_make" if d.agent_id == k["inv"] else "oth_chose_make"] += 1
            for c in d.candidates:
                if c[0] == "make" and c[1] in self.kinds:
                    k = self.kinds[c[1]]
                    k["w"]["inv_make_top4" if d.agent_id == k["inv"] else "oth_make_top4"] += 1
        # knower-weeks
        from acl.mind import can_make
        for p in world.living():
            for sig, recipe in p.recipes.items():
                k = self.kinds.get(sig)
                if k is None:
                    continue
                who = "inv" if p.id == k["inv"] else "oth"
                if who == "oth" and (p.id, sig) not in self.acq:
                    self.acq[(p.id, sig)] = "own"
                    k["learned"]["own"] += 1
                    k["learners"].append([p.id, tick, "own"])
                w = k["w"]
                w[f"{who}_weeks"] += 1
                v = p.itemval.get(sig, 0.0)
                w[f"{who}_val05"] += int(v > 0.05)
                w[f"{who}_val15"] += int(v > 0.15)
                w[f"{who}_canmake"] += int(can_make(p, recipe))
                if who == "oth" and self.acq.get((p.id, sig)) != "own":
                    w["lrn_weeks"] += 1
                    w["lrn_canmake"] += int(can_make(p, recipe))

    def results(self):
        out = {}
        for sig, k in self.kinds.items():
            rec = self.w.knowledge.get(sig, {})
            lost = [t for t in rec.get("lost", []) if t >= k["born"]]
            out[sig] = {"born": k["born"], "inv": k["inv"], "origin": k["origin"], "lost": lost[0] if lost else None,
                        "w": dict(k["w"]), "raw": dict(self.raw.get(sig, {})), "learned": dict(k["learned"]),
                        "made_other": dict(k["made_other"]), "learners": k["learners"], "makers": k["makers"]}
        return {"kinds": out, "check": dict(self.check)}


def install():
    """Wrap the three functions (once per process). The wrappers read state only; they call the originals unchanged."""
    from acl import information, knowhow
    if getattr(information, "_sp1", False):
        return
    information._sp1 = True
    show0, hear0, follow0 = information.show_how, information.hear_how, knowhow.can_follow

    def offers_of(teacher):
        """The code's own offer rule (information.show_how), recomputed before the call; no random draws."""
        offers = []
        for sig in teacher.recipes:
            v = teacher.itemval.get(sig, 0.0)
            if v > 0.15:
                offers.append((v, "m", sig))
        for key, v in information._beliefs_of(teacher).items():
            if v > 0.15:
                offers.append((v, "b", key))
        offers.sort(key=lambda o: (-o[0], o[2]))
        return offers[:3]

    def show_how(world, teacher, learner, parent):
        if not CUR:
            return show0(world, teacher, learner, parent)
        o = CUR[0]
        for sig in teacher.recipes:
            o.raw[sig]["occ_inv" if o.inventor(sig) == teacher.id else "occ_oth"] += 1
        offers = offers_of(teacher)
        for _v, kind, what in offers:
            if kind == "m":
                o.raw[what]["offered_inv" if o.inventor(what) == teacher.id else "offered_oth"] += 1
        OFFERS.append([what for _v, kind, what in offers if kind == "m"])
        try:
            return show0(world, teacher, learner, parent)
        finally:
            OFFERS.pop()

    def hear_how(world, learner, teacher, meant, recipe, claim, parent, part_lesson=False):
        if not CUR:
            return hear0(world, learner, teacher, meant, recipe, claim, parent, part_lesson)
        o = CUR[0]
        sig = information._sig_of(recipe)
        known = sig in learner.recipes
        own = learner.itemval.get(sig)
        distrust = (not known) and own is not None and own < -0.1 and "m:" + sig not in learner.heard
        if not part_lesson:
            if OFFERS:
                o.check["top_lessons"] += 1
                o.check["offer_miss"] += int(meant not in OFFERS[-1])
            else:
                o.check["lessons_outside_show"] += 1
        frame = {"cf": None}
        STACK.append(frame)
        try:
            r = hear0(world, learner, teacher, meant, recipe, claim, parent, part_lesson)
        finally:
            STACK.pop()
        cf = frame["cf"]
        if known:
            res = "known"
        elif distrust:
            res = "distrust"
        elif cf is None:
            res = "declined"
        elif cf is False:
            res = "missing_part"
        else:
            res = "taken" if sig == meant else "taken_wrong"
            o.taken.append((learner.id, sig))
        lvl = "part" if part_lesson else "top"
        o.raw[meant][f"{lvl}_shown"] += 1
        o.raw[meant][f"{lvl}_{res}"] += 1
        if o.inventor(meant) == teacher.id:
            o.raw[meant][f"{lvl}_shown_by_inv"] += 1
        return r

    def can_follow(learner, recipe):
        r = follow0(learner, recipe)
        if STACK and STACK[-1]["cf"] is None:
            STACK[-1]["cf"] = r
        return r

    information.show_how, information.hear_how, knowhow.can_follow = show_how, hear_how, can_follow


def make(seed, arm="c", code=CODE):
    base.setup(code)
    return base.make_world(seed, dict(ARMS[arm]))


def hashrun(code, seed, years, observe):
    BIRTH[0], BIRTH[1] = 0, years * WPY       # zero checks: every year followed
    w = make(seed, "c", code)
    obs = None
    if observe:
        install()
        obs = SP1Obs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results()
        ks = r["kinds"].values()
        extra = ":" + json.dumps({**r["check"], "kinds": len(r["kinds"]),
                                  "shown": sum(k["raw"].get("top_shown", 0) for k in ks),
                                  "learned_other": sum(sum(k["learned"].values()) for k in ks)},
                                 sort_keys=True, separators=(",", ":"))
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
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", CODE, *sp), specs)))
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
    for seed, years in ((501, 20), (601, 60)):
        ro = hs(got[(seed, years, 0)]) == hs(got[(seed, years, 1)])
        info = json.loads(got[(seed, years, 1)].split(":", 2)[2])
        t = ro and info.get("offer_miss", 0) == 0 and info.get("taken_mismatch", 0) == 0 and info.get("top_lessons", 0) > 0
        ok &= t
        lines.append(f"seed {seed}, {years} years: observer read-only (world and random stream): {'yes' if ro else 'NO'}; "
                     f"offer replica misses {info.get('offer_miss', 0)} of {info.get('top_lessons', 0)} lessons; "
                     f"taken lessons without a matching learn event {info.get('taken_mismatch', 0)} "
                     f"(of {info.get('taken', 0)}); {info}")
    t = rl.result()[-1:] == ["True"]
    ok &= t
    lines.append(f"seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_v15 fingerprint: {call('fp')}")
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
    obs = SP1Obs(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_v15", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w),
           "birth_window": list(BIRTH), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, kinds followed {len(res['kinds'])}, checks {res['check']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: every year followed; never study data
        BIRTH[0], BIRTH[1] = 0, int(sys.argv[4]) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
