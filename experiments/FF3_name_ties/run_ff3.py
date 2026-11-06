"""FF3 — memory ties settled by name, a fault fix in nature v13 (questions.md, frozen as `FF3-frozen`). A fault-fix check
in a copy: `code_ff3` = `code_v13` + `fix_name_ties` (0 = v13; v13_to_ff3.diff). Arms v13 (c), f, sham (x). ES2's
runner supplies the set-up (`../ES2_realized_lookahead/run_es2.py`). FF3's observer records, for years 100-200 (adults:
16 and over):
  census     living and adult weeks, adult makes
  the fix    from the code's log at each eviction of the four memories: evictions, those with a tie, and (recipes)
             those that dropped the newest recipe; draws made
  kinds      world-new kinds first made in years 100-195, and those made again by their inventor within 5 years

  python experiments/FF3_name_ties/run_ff3.py zero
  python experiments/FF3_name_ties/run_ff3.py one <arm> <seed> <years> <out>
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

base.CODES["ff3"] = HERE / "code_ff3"
base.CODES["v13"] = HERE.parent / "NV13_nature_v13" / "code_v13"
CODE = "ff3"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(23901, 23933))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9903, 9902)
ARMS = {"c": {**base.LP, "fix_name_ties": 0},
        "f": {**base.LP, "fix_name_ties": 1},
        "x": {**base.LP, "fix_name_ties": 0, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
ADULT = 16 * WPY
LATE = [100 * WPY, 200 * WPY]
REMAKE = 5 * WPY
MEM = {1: "recipes", 2: "marks", 3: "records", 4: "puzzles"}


class FF3Obs:
    def __init__(self, w):
        self.w = w
        self.s = Counter()
        self.kinds = {}                  # sig -> [first tick, inventor id, remade]
        w.ff3log = []

    def __call__(self, world, events):
        tick = world.tick - 1
        log, world.ff3log = world.ff3log, []
        for e in log:                    # every year, for the zero checks' "acts where triggered"
            if e[0] == "evict" and e[2] > 1:
                self.s["ties_all"] += 1
            if e[0] == "evict" and abs(e[3] - e[4]) > 1e-12:
                self.s["not_min_all"] += 1
        for ev in events:                # world-new kinds (first made this week) and their remaking
            if ev["k"] not in ("make", "play") or ev.get("thing") is None:
                continue
            sig = ev["thing"]
            kd = self.kinds.get(sig)
            if kd is not None:
                if ev["k"] == "make" and ev.get("a") == kd[1] and kd[0] < tick <= kd[0] + REMAKE:
                    kd[2] = 1
                continue
            rec = world.knowledge.get(sig)
            if rec is not None and rec.get("first_tick") == tick and rec.get("first_by") == ev.get("a")                     and LATE[0] <= tick < LATE[1] - REMAKE:
                self.kinds[sig] = [tick, ev.get("a"), 0]
        if not (LATE[0] <= tick < LATE[1]):
            return
        for e in log:
            if e[0] == "evict":
                m = MEM[e[1]]
                self.s[f"{m}_evict"] += 1
                self.s[f"{m}_tie"] += int(e[2] > 1)
                self.s[f"{m}_newest_dropped"] += e[5]
            elif e[0] == "draw":
                self.s[f"{MEM[e[1]]}_draws"] += 1
        for ev in events:
            if ev["k"] == "make" and ev.get("a") in world.people and world.people[ev["a"]].age(tick) >= ADULT:
                self.s["adult_makes"] += 1
        living = world.living()
        self.s["living_weeks"] += len(living)
        self.s["adult_weeks"] += sum(1 for p in living if p.age(world.tick) >= ADULT)

    def results(self):
        s = dict(self.s)
        s["new_kinds"] = len(self.kinds)
        s["remade_kinds"] = sum(k[2] for k in self.kinds.values())
        return {"sums": s}


def hashrun(code, arm, seed, years, observe):
    LATE[0], LATE[1] = 0, years * WPY       # zero checks: every year counted
    base.setup(code)
    kw = dict(ARMS[arm])
    if code == "v13":
        kw.pop("fix_name_ties", None)
    w = base.make_world(seed, kw)
    obs = None
    if observe:
        obs = FF3Obs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        extra = ":" + json.dumps({k: obs.s[k] for k in ("ties_all", "not_min_all", "adult_makes")}, sort_keys=True,
                                 separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def reload_check(seed):
    base.setup(CODE)
    from acl.world import World
    a = base.make_world(seed, ARMS["f"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for x in (a, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(a) == base.world_hash(b) and b.cfg.fix_name_ties == 1


def unit_check(seed):
    """In an f world (30 years): every eviction drops an item at the memory's minimum; every draw leaves the world's
    generator untouched. Then a synthetic three-way tie: even over 30,000 draws, and the same pick in any order."""
    base.setup(CODE)
    import acl.util as util
    import acl.knowhow as knowhow
    import acl.marks as marks
    import acl.information as information
    import acl.inquiry as inquiry
    w = base.make_world(seed, ARMS["f"])
    w.ff3log = []
    o_pick = util.tie_pick
    moved = [0, 0]

    def pick(world, p, which, tied, size):
        before = world.rng.getstate()
        out = o_pick(world, p, which, tied, size)
        moved[1] += 1
        moved[0] += int(world.rng.getstate() != before)
        return out
    for mod in (knowhow, marks, information, inquiry):
        mod.tie_pick = pick
    evicts = not_min = 0
    for _ in range(30 * WPY):
        w.step()
        for e in w.ff3log:
            if e[0] == "evict":
                evicts += 1
                not_min += int(abs(e[3] - e[4]) > 1e-12)
        w.ff3log = []

    class P:
        id = "p00042"

    class C:
        seed = 777

    class Wd:
        cfg = C()
        tick = 0
    items = ["(stone+wood)#fiber", "((stone+wood)#fiber+bone)#hide", "flint/stone"]
    n = Counter()
    order_same = True
    wd, p = Wd(), P()
    for t in range(30_000):
        wd.tick = t
        a = o_pick(wd, p, 1, list(items), 12)
        b = o_pick(wd, p, 1, list(reversed(items)), 12)
        order_same &= a == b
        n[a] += 1
    shares = [n[x] / 30_000 for x in items]
    even = all(0.31 <= s <= 0.356 for s in shares)
    return evicts, not_min, moved[1], moved[0], even, order_same, shares


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
             for code, arm, obs in (("v13", "c", 0), ("ff3", "c", 0), ("ff3", "c", 1), ("ff3", "f", 0), ("ff3", "f", 1),
                                    ("ff3", "x", 0))]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        side = dict(zip(("reload", "unit"), ex.map(lambda a: call(*a), (("reload", 501), ("unit", 701)))))
    for seed, years in ((501, 20), (601, 60)):
        g = {(c, a, o): got[(c, a, sd, yr, o)] for c, a, sd, yr, o in specs if sd == seed}
        same = hs(g[("v13", "c", 0)]) == hs(g[("ff3", "c", 0)])
        ro = all(hs(g[("ff3", a, 0)]) == hs(g[("ff3", a, 1)]) for a in ("c", "f"))
        sham = hs(g[("ff3", "x", 0)]) != hs(g[("ff3", "c", 0)])
        info = json.loads(g[("ff3", "f", 1)].split(":", 2)[2])
        differs = hs(g[("ff3", "f", 0)]) != hs(g[("ff3", "c", 0)])
        trig = info["ties_all"] > 0
        acts = differs if trig else True
        note = f"f: triggered ({info['ties_all']} ties), acts: {'yes' if differs else 'NO'}" if trig else \
            "f: not triggered" + (" (but differs)" if differs else "")
        t = same and ro and sham and acts
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_ff3 with 0 = code_v13: {'yes' if same else 'NO'}; observer and log "
                     f"read-only (c, f): {'yes' if ro else 'NO'}; the sham acts: {'yes' if sham else 'NO'}; {note}")
    t = side["reload"] == "True"
    ok &= t
    lines.append(f"arm f, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    u = json.loads(side["unit"])
    t1 = u[0] > 0 and u[1] == 0
    t2 = u[2] > 0 and u[3] == 0
    t3, t4 = u[4], u[5]
    ok &= t1 and t2 and t3 and t4
    lines.append(f"unit checks, arm f, seed 701, 30 years: evictions {u[0]}, not at the minimum {u[1]}: "
                 f"{'yes' if t1 else 'NO'}; draws {u[2]}, the world's generator moved by a draw {u[3]}: "
                 f"{'yes' if t2 else 'NO'}")
    lines.append(f"unit checks, a synthetic three-way tie, 30,000 draws: shares {', '.join(f'{s:.4f}' for s in u[6])} "
                 f"(each within 0.31-0.356): {'yes' if t3 else 'NO'}; the same pick in either order: "
                 f"{'yes' if t4 else 'NO'}")
    lines.append(f"code_ff3 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = base.make_world(seed, ARMS[arm])
    obs = FF3Obs(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_ff3", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, recipe ties {obs.s['recipes_tie']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "unit":
        print(json.dumps(unit_check(int(sys.argv[2]))))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: every year counted; never study data
        LATE[0], LATE[1] = 0, int(sys.argv[4]) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
