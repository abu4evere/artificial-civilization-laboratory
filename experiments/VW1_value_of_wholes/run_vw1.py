"""VW1 — what a valued whole needs is wanted: a law tested in a copy of v16 (questions.md, frozen as `VW1-frozen`).
`code_vw1` = `code_v16` + `want_down` (0 = v16; v16_to_vw1.diff). Arms v16 (c), VW (w), sham (x); LP; seeds
25201-25232; 200 years; years 100-200 counted for the guards; kinds born in years 100-190 followed for 5 years.

Observers (read-only):
  CI1's   the guard sums (`../CI1_children_and_aims/run_ci1.py`)
  MP1's   the stage funnel of new kinds needing a made part and each tracked part's fate (`../MP1_made_parts/run_mp1.py`)
  VW1's   the grown's weeks by action (food-production displacement), and the make options offered: how many are a
          part of a valued whole one level down, and how many only deeper (read at `thought.steer`)

  python experiments/VW1_value_of_wholes/run_vw1.py zero
  python experiments/VW1_value_of_wholes/run_vw1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "MP1_made_parts"))
sys.path.insert(0, str(HERE.parent / "CI1_children_and_aims"))
import run_mp1 as M  # noqa: E402
import run_ci1 as R  # noqa: E402

base = M.base
base.CODES["vw1"] = HERE / "code_vw1"
base.CODES["v16"] = HERE.parent / "NV16_nature_v16" / "code_v16"
CODE = "vw1"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(25201, 25233))        # 32 new paired seeds, used by no study
ARMS = {"c": {**base.LP, "want_down": 0},
        "w": {**base.LP, "want_down": 1},
        "x": {**base.LP, "want_down": 0, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
GROWN = 16 * WPY
CUR = []


class VWObs:
    def __init__(self, w):
        self.w = w
        self.acts = Counter()
        self.mech = Counter()
        CUR[:] = [self]

    def offered(self, world, p, options):
        from acl import mind
        if not (R.LATE[0] <= world.tick < R.LATE[1]):
            return
        for o in options:
            if o[1] != "make":
                continue
            lvl1 = mind._wanted_parts(p, 0)
            deep = mind._wanted_parts(p, 1)
            self.mech["make_offers"] += 1
            self.mech["offer_part_level1"] += int(o[2] in lvl1)
            self.mech["offer_part_deeper_only"] += int(o[2] in deep and o[2] not in lvl1)

    def __call__(self, world, events):
        tick = world.tick - 1
        if not (R.LATE[0] <= tick < R.LATE[1]):
            return
        for p in world.living():
            if world.tick - p.birth >= GROWN:
                self.acts["grown_weeks"] += 1
                self.acts[f"doing_{(p.doing or 'none').split()[0]}"] += 1    # "gather fiber" -> gather

    def results(self):
        return {"acts": dict(self.acts), "mech": dict(self.mech)}


def install():
    from acl import thought
    M.install()
    if getattr(thought.steer, "_vw1", False):
        return
    steer0 = thought.steer

    def steer(p, options):
        o = CUR[0] if CUR else None
        if o is not None:
            o.offered(o.w, p, options)
        return steer0(p, options)
    steer._vw1 = True
    thought.steer = steer


def attach(w):
    ci = R.CI1Obs(w)
    mp = M.MP1Obs(w)
    vw = VWObs(w)
    w.observers += [ci, mp, vw]
    return ci, mp, vw


def combined(ci, mp, vw):
    r = ci.results()
    r.pop("kinds", None)
    m = mp.results()
    r.update({"stages": m["stages"], "fates": m["fates"], "parts_check": m["check"], **vw.results()})
    return r


def make(seed, arm, code=CODE):
    base.setup(code)
    kw = dict(ARMS[arm])
    if code != CODE:
        kw.pop("want_down", None)
    return base.make_world(seed, kw)


def hashrun(code, arm, seed, years, observe):
    R.LATE[0], R.LATE[1] = 0, years * WPY
    M.WIN[0], M.WIN[1] = 0, (years - 5) * WPY
    w = make(seed, arm, code)
    obs = None
    if observe:
        install()
        obs = attach(w)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = combined(*obs)
        extra = ":" + json.dumps({"stages": {k: v for k, v in r["stages"].items() if k.startswith("stage_")},
                                  "mech": r["mech"], "parts_check": r["parts_check"]},
                                 sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def reload_check(seed):
    w = make(seed, "w")
    from acl.world import World
    for _ in range(10 * WPY):
        w.step()
    b = World.from_dict(json.loads(json.dumps(w.to_dict())))
    for x in (w, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(w) == base.world_hash(b) and b.cfg.want_down == 1


def independent_wants(p):
    """The law, computed a second way (a depth-first walk over every path; the highest value wins)."""
    from acl.matter import MATERIALS
    from acl.mind import _holding

    def parts_of(r):
        return list(r.get("parts", ())) + ([r["part"]] if r["verb"] == "heat" else [])
    W = {}

    def visit(sig, v, seen, level):
        r = p.recipes.get(sig)
        if r is None:
            return
        for part in parts_of(r):
            if part in MATERIALS or _holding(p, part, worn_ok=True) or part in seen:
                continue
            nv = 0.8 * v
            if level > 1 and nv < 0.01:
                continue
            if nv > W.get(part, 0.0):
                W[part] = nv
            visit(part, nv, seen | {part}, level + 1)
    for sig, r in p.recipes.items():
        v = p.itemval.get(sig, 0.0)
        if v <= 0 or _holding(p, sig):
            continue
        visit(sig, v, {sig}, 1)
    return W


def unit_check(seed, years=30):
    w = make(seed, "w")
    from acl import mind
    from acl.mind import _holding, recipe_materials
    st = Counter()
    dec0 = mind.decide

    def decide(world, p):
        if p.recipes and (world.tick + int(p.id[1:])) % 7 == 0:
            deep = mind._wanted_parts(p, 1)
            lvl1 = mind._wanted_parts(p, 0)
            ind = independent_wants(p)
            st["looks"] += 1
            st["deep_keys"] += len(deep)
            st["deeper_only"] += sum(1 for k in deep if k not in lvl1)
            if set(deep) != set(ind) or any(abs(deep[k] - ind[k]) > 1e-12 for k in deep):
                st["deep_mismatch"] += 1
            if any(deep.get(k, 0.0) < v - 1e-12 for k, v in lvl1.items()):
                st["level1_not_kept"] += 1
            want = mind._material_wants(p, world.season, 1)
            for sig, v in deep.items():
                r = p.recipes.get(sig)
                if r is None or _holding(p, sig):
                    continue
                for kind in recipe_materials(r):
                    if kind in want and p.mats.get(kind, 0.0) < 1.0 and want[kind] < v - 1e-12:
                        st["material_not_wanted"] += 1
        return dec0(world, p)
    mind.decide = decide
    try:
        for _ in range(years * WPY):
            w.step()
    finally:
        mind.decide = dec0
    ok = (st["looks"] > 0 and st["deeper_only"] > 0 and st["deep_mismatch"] == 0 and st["level1_not_kept"] == 0
          and st["material_not_wanted"] == 0)
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
             for code, arm, obs in (("v16", "c", 0), ("vw1", "c", 0), ("vw1", "c", 1), ("vw1", "w", 0), ("vw1", "w", 1),
                                    ("vw1", "x", 0))]
    with ThreadPoolExecutor(2) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        unit = ex.submit(call, "unit", 701)
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
    for seed, years in ((501, 20), (601, 60)):
        same = hs(got[("v16", "c", seed, years, 0)]) == hs(got[("vw1", "c", seed, years, 0)])
        ro = (hs(got[("vw1", "c", seed, years, 0)]) == hs(got[("vw1", "c", seed, years, 1)])
              and hs(got[("vw1", "w", seed, years, 0)]) == hs(got[("vw1", "w", seed, years, 1)]))
        acts = hs(got[("vw1", "w", seed, years, 0)]) != hs(got[("vw1", "c", seed, years, 0)])
        sham = hs(got[("vw1", "x", seed, years, 0)]) != hs(got[("vw1", "c", seed, years, 0)])
        ok &= same and ro and acts and sham
        info = got[("vw1", "w", seed, years, 1)].split(":", 2)[2]
        lines.append(f"seed {seed}, {years} years: code_vw1 with want_down 0 = code_v16: {'yes' if same else 'NO'}; "
                     f"observers read-only (c, w): {'yes' if ro else 'NO'}; VW acts: {'yes' if acts else 'NO'}; the sham "
                     f"acts: {'yes' if sham else 'NO'}; w: {info}")
    u = json.loads(unit.result())
    ok &= u[0]
    lines.append(f"unit checks, arm w, seed 701, 30 years (the wanted map equals an independent computation of the law; "
                 f"v16's one-level values kept; the materials of every wanted, known, unheld recipe wanted): "
                 f"{'yes' if u[0] else 'NO'}; {u[1]}")
    t = rl.result()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm w, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_vw1 fingerprint: {call('fp')}")
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
    obs = attach(w)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_vw1", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **combined(*obs)}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, parts check {res['parts_check']}", flush=True)


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
        R.LATE[0], R.LATE[1] = 0, int(sys.argv[4]) * WPY
        M.WIN[0], M.WIN[1] = 0, (int(sys.argv[4]) - 5) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
