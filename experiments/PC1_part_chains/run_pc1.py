"""PC1 — the part chains of new kinds (questions.md, frozen as `PC1-frozen`). Read-only on `code_v15`: one arm, LP, seeds
24501-24532, 200 years; invented kinds born in years 100-190 followed to year 200.

The observer wraps, never changes, knowhow.remember_recipe (births), information.hear_how (lessons and the one-level
part lesson that may follow) and knowhow.can_follow (read inside a lesson, to tell "declined" from "missing part").
Every check it makes is a pure function of state; it draws no random numbers.

  python experiments/PC1_part_chains/run_pc1.py zero
  python experiments/PC1_part_chains/run_pc1.py one <arm> <seed> <years> <out>
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

base.CODES["v15"] = HERE.parent / "NV15_nature_v15" / "code_v15"
CODE = "v15"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(24501, 24533))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9901, 9900)
ARMS = {"c": dict(base.LP)}
JOBS = [f"c:{s}" for s in SEEDS]
OUT = HERE / "output"
WIN = [100 * WPY, 190 * WPY]              # kinds born in this window are followed
END = [200 * WPY]
LATER = 5 * WPY
CUR = []


def made_parts(recipe):
    from acl.matter import MATERIALS
    parts = list(recipe.get("parts", ())) + ([recipe["part"]] if recipe.get("verb") == "heat" else [])
    return [x for x in parts if x not in MATERIALS]


def tree(world, sig, path=()):
    """(depth, set of made parts, parts with no record, cycle) of sig's recipe, recursively by the world's records."""
    rec = world.knowledge.get(sig)
    if rec is None:
        return 0, set(), {sig}, False
    depth, parts, unknown, cyc = 0, set(), set(), False
    for x in made_parts(rec["recipe"]):
        parts.add(x)
        if x in path or x == sig:
            cyc = True
            continue
        d, p, u, c = tree(world, x, path + (sig,))
        depth, cyc = max(depth, d + 1), cyc or c
        parts |= p
        unknown |= u
    return depth, parts, unknown, cyc


def tree2(world, sig):
    """An independent check of tree(): depth and part count by a breadth-first walk with explicit levels."""
    level, depth, seen, frontier = 0, 0, set(), [(sig, (sig,))]
    while frontier:
        nxt = []
        for s, path in frontier:
            rec = world.knowledge.get(s)
            if rec is None:
                continue
            for x in made_parts(rec["recipe"]):
                seen.add(x)
                if x in path:
                    continue
                depth = max(depth, level + 1)
                nxt.append((x, path + (x,)))
        frontier, level = nxt, level + 1
        if level > 50:
            break
    return depth, len(seen)


def further(world, learner, part, path=()):
    """How many further levels of made parts the learner does not know lie beneath `part` (0 if none)."""
    rec = world.knowledge.get(part)
    if rec is None:
        return 0
    best = 0
    for x in made_parts(rec["recipe"]):
        if x in learner.recipes or x in path or x == part:
            continue
        best = max(best, 1 + further(world, learner, x, path + (part,)))
    return best


class PC1Obs:
    def __init__(self, w):
        self.w = w
        self.kinds = {}               # sig -> (t0, depth, nparts, unknown, cycle)
        self.tree_mismatch = 0
        self.ctx = []
        self.rows = []                # one per failed-on-part top-level lesson of a followed kind
        self.lessons = Counter()      # top-level lessons of followed kinds, by outcome
        self.taken = Counter()        # event check for taken part lessons
        self.pending = {}             # (learner, sig) -> [t, missing parts, got_part, got_K, made_K]
        CUR[:] = [self]

    def __call__(self, world, events):
        tick = world.tick - 1
        for e in events:
            if e["k"] == "learn" and e.get("how") == "taught" and e.get("thing") is not None and e.get("meant"):
                self.taken[("ev", tick, e.get("a"), e["thing"])] += 1
            elif e["k"] == "learn" and e.get("how") == "taught" and e.get("thing") is not None:
                self.taken[("ev", tick, e.get("a"), e["thing"])] += 1
            if e["k"] == "make" and e.get("thing") is not None:
                key = (e.get("a"), e["thing"])
                pe = self.pending.get(key)
                if pe is not None and tick - pe[0] <= LATER:
                    pe[4] = 1
        for (pid, sig), pe in self.pending.items():
            if tick - pe[0] > LATER:
                continue
            p = world.people.get(pid)
            if p is None or not p.alive:
                continue
            if any(x in p.recipes for x in pe[1]):
                pe[2] = 1
            if sig in p.recipes:
                pe[3] = 1

    def results(self):
        k = list(self.kinds.values())
        later = Counter()
        for pe in self.pending.values():
            later["pairs"] += 1
            later["got_part"] += pe[2]
            later["got_K"] += pe[3]
            later["made_K"] += pe[4]
        ob = Counter({key[1:]: v for key, v in self.taken.items() if key[0] == "ob"})
        ev = Counter({key[1:]: v for key, v in self.taken.items() if key[0] == "ev"})
        mism = sum(max(0, v - ev.get(key, 0)) for key, v in ob.items())
        return {"kinds": k, "n_kinds": len(k), "tree_mismatch": self.tree_mismatch, "rows": self.rows,
                "lessons": dict(self.lessons), "later": dict(later), "part_taken": sum(ob.values()),
                "part_taken_mismatch": mism}


def install():
    from acl import information, knowhow
    if getattr(knowhow, "_pc1", False):
        return
    knowhow._pc1 = True
    rr0, hear0, follow0 = knowhow.remember_recipe, information.hear_how, knowhow.can_follow

    def remember_recipe(world, p, sig, recipe, how, *a, **k):
        if not CUR:
            return rr0(world, p, sig, recipe, how, *a, **k)
        new = sig not in world.knowledge
        out = rr0(world, p, sig, recipe, how, *a, **k)
        if new and how in ("made", "heated") and WIN[0] <= world.tick < WIN[1]:
            o = CUR[0]
            d, parts, unknown, cyc = tree(world, sig)
            d2, n2 = tree2(world, sig)
            if (d, len(parts)) != (d2, n2):
                o.tree_mismatch += 1
            o.kinds[sig] = (world.tick, d, len(parts), len(unknown), int(cyc))
        return out

    def hear_how(world, learner, teacher, meant, recipe, claim, parent, part_lesson=False, *a, **k):
        if not CUR:
            return hear0(world, learner, teacher, meant, recipe, claim, parent, part_lesson, *a, **k)
        o = CUR[0]
        sig = information._sig_of(recipe)
        knew = sig in learner.recipes
        own = learner.itemval.get(sig)
        distrust = (not knew) and own is not None and own < -0.1 and "m:" + sig not in learner.heard
        followed = (not part_lesson) and meant in o.kinds and world.tick < END[0]
        info = None
        if followed:
            missing = [x for x in made_parts(recipe) if x not in learner.recipes]
            info = {"missing": missing,
                    "teacher_knows": [x in teacher.recipes for x in missing],
                    "alive_known": [bool(world.knowledge.get(x, {}).get("alive", False)) for x in missing],
                    "deepest": (1 + max((further(world, learner, x) for x in missing), default=0)) if missing else 0}
        o.ctx.append({"follow": None, "part": None})
        try:
            got = hear0(world, learner, teacher, meant, recipe, claim, parent, part_lesson, *a, **k)
        finally:
            ctx = o.ctx.pop()
        if got:
            outcome = "taken"
        elif knew:
            outcome = "knew"
        elif distrust:
            outcome = "distrust"
        elif ctx["follow"] is False:
            outcome = "missing_part"
        else:
            outcome = "declined"
        if part_lesson:
            if o.ctx:
                o.ctx[-1]["part"] = (meant, outcome)
            if got:
                o.taken[("ob", world.tick, learner.id, sig)] += 1
            return got
        if followed:
            o.lessons[outcome] += 1
            if outcome == "missing_part":
                miss = info["missing"]
                tk = info["teacher_knows"]
                part = ctx["part"]
                o.rows.append([len(miss), sum(tk), int(all(tk)) if miss else 0, sum(info["alive_known"]),
                               info["deepest"], int(part is not None), part[1] if part else "none",
                               int(part is not None and part[0] in miss)])
                key = (learner.id, meant)
                if key not in o.pending:
                    o.pending[key] = [world.tick, set(miss), 0, 0, 0]
        return got

    def can_follow(learner, recipe, *a, **k):
        out = follow0(learner, recipe, *a, **k)
        if CUR and CUR[0].ctx and CUR[0].ctx[-1]["follow"] is None:
            CUR[0].ctx[-1]["follow"] = out
        return out

    knowhow.remember_recipe, information.hear_how, knowhow.can_follow = remember_recipe, hear_how, can_follow


def make(seed, arm="c", code=CODE):
    base.setup(code)
    return base.make_world(seed, dict(ARMS[arm]))


def hashrun(code, seed, years, observe):
    WIN[0], WIN[1], END[0] = 0, years * WPY, years * WPY     # zero checks: every year followed
    w = make(seed, "c", code)
    obs = None
    if observe:
        install()
        obs = PC1Obs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results()
        extra = ":" + json.dumps({"kinds": r["n_kinds"], "tree_mismatch": r["tree_mismatch"], "failed_rows": len(r["rows"]),
                                  "lessons": r["lessons"], "part_taken": r["part_taken"],
                                  "part_taken_mismatch": r["part_taken_mismatch"]}, sort_keys=True, separators=(",", ":"))
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
    rl = subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split()
    for seed, years in ((501, 20), (601, 60)):
        ro = hs(got[(seed, years, 0)]) == hs(got[(seed, years, 1)])
        info = json.loads(got[(seed, years, 1)].split(":", 2)[2])
        t = ro and info["tree_mismatch"] == 0 and info["part_taken_mismatch"] == 0 and info["failed_rows"] > 0
        ok &= t
        lines.append(f"seed {seed}, {years} years: observer read-only (world and random stream): {'yes' if ro else 'NO'}; "
                     f"tree check mismatches {info['tree_mismatch']}; part lessons taken without a matching learn event "
                     f"{info['part_taken_mismatch']} (of {info['part_taken']}); failed-on-part lessons observed "
                     f"{info['failed_rows']}: {'yes' if t else 'NO'}; {info}")
    t = rl[-1:] == ["True"]
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
    obs = PC1Obs(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_v15", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, kinds {res['n_kinds']}, failed-on-part lessons {len(res['rows'])}, "
          f"tree mismatches {res['tree_mismatch']}, part-taken mismatches {res['part_taken_mismatch']}", flush=True)


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
        WIN[0], WIN[1], END[0] = 0, int(sys.argv[4]) * WPY, int(sys.argv[4]) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
