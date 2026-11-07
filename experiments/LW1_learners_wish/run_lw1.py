"""LW1 — a learner's wish for the part they could not follow (questions.md, frozen as `LW1-frozen`). A test in a copy:
`code_lw1` = `code_v15` + `learn_wish` (0 = v15; v15_to_lw1.diff). Arms v15 (c), LW (w), sham (x); LP; seeds 24601-24632;
200 years, years 100-200 counted.

The observer is CI1's (the guard sums; `../CI1_children_and_aims/run_ci1.py`), plus, read-only:
  kinds       invented kinds (first record made or heated) born in years 100-190: learned by a non-inventor within 5 years
              by a lesson, watching or reading (the co-primary), and made by a non-inventor within 5 years
  pairs       learner-kind pairs whose lesson failed on a missing made part: a missing part learned within 5 years
  wishes      the law's own log (formed, met and the met lesson's outcome, ended by cause)
  time        grown weeks spent foraging and talking

  python experiments/LW1_learners_wish/run_lw1.py zero
  python experiments/LW1_learners_wish/run_lw1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "CI1_children_and_aims"))
import run_ci1 as R  # noqa: E402

base = R.base
base.CODES["lw1"] = HERE / "code_lw1"
base.CODES["v15"] = HERE.parent / "NV15_nature_v15" / "code_v15"
CODE = "lw1"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(24601, 24633))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9901, 9900)
ARMS = {"c": {**base.LP, "learn_wish": 0},
        "w": {**base.LP, "learn_wish": 1},
        "x": {**base.LP, "learn_wish": 0, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
WIN = [100 * WPY, 190 * WPY]              # kinds born here are followed
LATER = 5 * WPY
CUR = []


def made_missing(recipe, learner):
    from acl.matter import MATERIALS
    need = list(recipe.get("parts", ())) + ([recipe["part"]] if recipe.get("verb") == "heat" else [])
    return [x for x in need if x not in MATERIALS and x not in learner.recipes]


class LW1Obs(R.CI1Obs):
    def __init__(self, w):
        super().__init__(w)
        w.lwlog = []
        self.ck = {}                      # sig -> [t0, inventor, learned_social, made_other]
        self.pairs = {}                   # (learner, sig) -> [t, missing parts, got_part]
        self.wish = Counter()
        self.ctx = []
        self.met_seen = 0
        CUR[:] = [self]

    def __call__(self, world, events):
        super().__call__(world, events)
        tick = world.tick - 1
        counted = R.LATE[0] <= tick < R.LATE[1]
        log, world.lwlog = world.lwlog, []
        self.met_seen = 0
        if counted:
            for e in log:
                self.wish["form" if e[0] == "form" else ("met" if e[0] == "met" else f"end_{e[3]}")] += 1
        for e in events:
            if e["k"] == "make" and e.get("thing") in self.ck:
                r = self.ck[e["thing"]]
                if e.get("a") != r[1] and r[0] < tick <= r[0] + LATER:
                    r[3] = 1
        for (pid, sig), pe in self.pairs.items():
            if pe[2] or tick - pe[0] > LATER:
                continue
            p = world.people.get(pid)
            if p is not None and p.alive and any(x in p.recipes for x in pe[1]):
                pe[2] = 1
        if counted:
            for p in world.living():
                if p.age(world.tick) >= 16 * WPY:
                    self.s["grown_weeks_forage"] += int(p.doing == "forage")
                    self.s["grown_weeks_talk"] += int(p.doing == "talk")

    def results(self):
        r = super().results()
        ck = list(self.ck.values())
        r.update({"lw_kinds": len(ck), "lw_learned": sum(x[2] for x in ck), "lw_made_other": sum(x[3] for x in ck),
                  "lw_pairs": len(self.pairs), "lw_pairs_got_part": sum(p[2] for p in self.pairs.values()),
                  "wish": dict(self.wish)})
        return r


def install():
    from acl import information, knowhow
    if getattr(knowhow, "_lw1", False):
        return
    knowhow._lw1 = True
    rr0, hear0 = knowhow.remember_recipe, information.hear_how

    def remember_recipe(world, p, sig, recipe, how, *a, **k):
        if not CUR:
            return rr0(world, p, sig, recipe, how, *a, **k)
        o = CUR[0]
        new = sig not in world.knowledge
        fresh = sig not in p.recipes
        out = rr0(world, p, sig, recipe, how, *a, **k)
        t = world.tick
        if new and how in ("made", "heated") and WIN[0] <= t < WIN[1]:
            o.ck[sig] = [t, p.id, 0, 0]
        elif fresh and sig in o.ck and p.id != o.ck[sig][1] and how in ("taught", "copied", "read") \
                and t - o.ck[sig][0] <= LATER:
            o.ck[sig][2] = 1
        return out

    def hear_how(world, learner, teacher, meant, recipe, claim, parent, part_lesson=False, *a, **k):
        if not CUR:
            return hear0(world, learner, teacher, meant, recipe, claim, parent, part_lesson, *a, **k)
        o = CUR[0]
        miss = made_missing(recipe, learner) if (not part_lesson and meant in o.ck) else []
        got = hear0(world, learner, teacher, meant, recipe, claim, parent, part_lesson, *a, **k)
        if miss and not got and all(x not in learner.recipes for x in miss) and meant not in learner.recipes:
            key = (learner.id, meant)
            if key not in o.pairs:
                o.pairs[key] = [world.tick, set(miss), 0]
        return got

    knowhow.remember_recipe, information.hear_how = remember_recipe, hear_how


def make(seed, arm, code=CODE):
    base.setup(code)
    kw = dict(ARMS[arm])
    if code != CODE:
        kw.pop("learn_wish", None)
    return base.make_world(seed, kw)


def hashrun(code, arm, seed, years, observe):
    R.LATE[0], R.LATE[1] = 0, years * WPY       # zero checks: every year counted
    WIN[0], WIN[1] = 0, years * WPY
    w = make(seed, arm, code)
    obs = None
    if observe:
        install()
        obs = LW1Obs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results()
        extra = ":" + json.dumps({"kinds": r["lw_kinds"], "learned": r["lw_learned"], "pairs": r["lw_pairs"],
                                  "wish": r["wish"]}, sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def reload_check(seed):
    w = make(seed, "w")
    from acl.world import World
    for _ in range(10 * WPY):
        w.step()
    held = sum(1 for p in w.living() if p.wish is not None)
    b = World.from_dict(json.loads(json.dumps(w.to_dict())))
    same = all(b.people[p.id].wish == p.wish for p in w.living())
    for x in (w, b):
        for _ in range(5 * WPY):
            x.step()
    return (base.world_hash(w) == base.world_hash(b) and b.cfg.learn_wish == 1 and same and held > 0), held


def unit_check(seed, years=30):
    """In an LW world: (u1) every wish forms on a failed follow, on the first missing made part, in order; (u2) every
    lesson shown for a wish is the wished part, unknown to the learner, held at most 52 weeks, from a speaker who knows
    it; (u3) every wish ending matches its cause; (u4) no talk gives two top-level lessons."""
    w = make(seed, "w")
    from acl import information, knowhow
    st = Counter()
    exp = []
    o_show, o_hear, o_follow = information.show_how, information.hear_how, knowhow.can_follow

    def follow(learner, recipe, *a, **k):
        out = o_follow(learner, recipe, *a, **k)
        if not out and exp is not None:
            miss = made_missing(recipe, learner)
            exp.append((learner.id, miss[0] if miss else None))
        return out

    def hear(world, learner, teacher, meant, recipe, claim, parent, part_lesson=False, *a, **k):
        return o_hear(world, learner, teacher, meant, recipe, claim, parent, part_lesson, *a, **k)

    def show(world, teacher, learner, parent, *a, **k):
        before = list(learner.wish) if learner.wish is not None else None
        knew_before = before is not None and before[0] in learner.recipes
        teacher_knows = before is not None and before[0] in teacher.recipes
        n0 = len(world.lwlog)
        exp.clear()
        tops = [0]

        def counting(world_, learner_, teacher_, meant_, recipe_, claim_, parent_, part_lesson=False, *a_, **k_):
            if not part_lesson:
                tops[0] += 1
            return o_hear(world_, learner_, teacher_, meant_, recipe_, claim_, parent_, part_lesson, *a_, **k_)
        information.hear_how = counting
        try:
            out = o_show(world, teacher, learner, parent, *a, **k)
        finally:
            information.hear_how = hear
        st["talks_with_lesson_calls"] += 1
        if tops[0] > 1:
            st["two_lessons"] += 1
        new = world.lwlog[n0:]
        forms = [(e[1], e[2]) for e in new if e[0] == "form"]
        want = [(pid, part) for pid, part in exp if part is not None]
        if forms != want:
            st["form_mismatch"] += 1
        st["forms"] += len(forms)
        for e in new:
            if e[0] == "met":
                st["met"] += 1
                if before is None or e[2] != before[0] or knew_before or not teacher_knows \
                        or world.tick - before[1] > 52 or e[3] != teacher.id:
                    st["met_bad"] += 1
            elif e[0] == "end":
                st["ended"] += 1
                ok = (e[3] == "known" and e[2] in learner.recipes) or \
                     (e[3] == "expired" and before is not None and world.tick - before[1] > 52)
                if not ok:
                    st["end_bad"] += 1
        return out

    knowhow.can_follow, information.hear_how, information.show_how = follow, hear, show
    w.lwlog = []
    for _ in range(years * WPY):
        w.step()
        w.lwlog = []
    knowhow.can_follow, information.hear_how, information.show_how = o_follow, o_hear, o_show
    ok = (st["two_lessons"] == 0 and st["form_mismatch"] == 0 and st["met_bad"] == 0 and st["end_bad"] == 0
          and st["forms"] > 0 and st["met"] > 0)
    return ok, dict(st)


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
    specs = [(code, arm, seed, years, obs) for seed, years in ((501, 20), (601, 60))
             for code, arm, obs in (("v15", "c", 0), ("lw1", "c", 0), ("lw1", "c", 1), ("lw1", "w", 0), ("lw1", "w", 1),
                                    ("lw1", "x", 0))]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        side = list(ex.map(lambda a: subprocess.run(me + a, capture_output=True, text=True).stdout.strip().splitlines(),
                           [["reload", "501"], ["unit", "701"]]))
    for seed, years in ((501, 20), (601, 60)):
        g = {(c, a, o): got[(c, a, sd, yr, o)] for c, a, sd, yr, o in specs if sd == seed}
        same = hs(g[("v15", "c", 0)]) == hs(g[("lw1", "c", 0)])
        ro = all(hs(g[("lw1", a, 0)]) == hs(g[("lw1", a, 1)]) for a in ("c", "w"))
        acts = all(hs(g[("lw1", a, 0)]) != hs(g[("lw1", "c", 0)]) for a in ("w", "x"))
        info = {a: json.loads(g[("lw1", a, 1)].split(":", 2)[2]) for a in ("c", "w")}
        t = same and ro and acts
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_lw1 with learn_wish 0 = code_v15: {'yes' if same else 'NO'}; "
                     f"observer read-only (c, w): {'yes' if ro else 'NO'}; LW and the sham act: {'yes' if acts else 'NO'}; "
                     f"{info}")
    out = side[0][-1] if side[0] else ""
    t = out.startswith("True")
    ok &= t
    lines.append(f"arm w, seed 501: saved at year 10 (wishes held: {out.split()[-1] if out else '?'}) and reloaded, "
                 f"continues exactly to year 15, wishes saved: {'yes' if t else 'NO'}")
    out = side[1][-1] if side[1] else ""
    t = out.startswith("True")
    ok &= t
    lines.append(f"unit checks, arm w, seed 701, 30 years (wishes form on the first missing made part of a failed follow; "
                 f"every wish lesson shows the wished part, unknown, at most 52 weeks old, from a speaker who knows it; "
                 f"endings match their cause; no talk gives two lessons): {'yes' if t else 'NO'}; {out[5:] if t else out}")
    lines.append(f"code_lw1 fingerprint: {call('fp')}")
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
    obs = LW1Obs(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_lw1", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, kinds {res['lw_kinds']}, learned by others {res['lw_learned']}, "
          f"wishes {res['wish']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        ok, n = reload_check(int(sys.argv[2]))
        print(ok, n)
    elif cmd == "unit":
        ok, st = unit_check(int(sys.argv[2]))
        print(ok, json.dumps(st, sort_keys=True, separators=(",", ":")))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: every year counted; never study data
        R.LATE[0], R.LATE[1] = 0, int(sys.argv[4]) * WPY
        WIN[0], WIN[1] = 0, int(sys.argv[4]) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
