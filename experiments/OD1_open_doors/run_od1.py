"""OD1 — open the world's closed doors, once (questions.md, frozen as `OD1-frozen`). `code_od1` = `code_v16` + five
switches, each 0 = v16 (patch_od1.py; v16_to_od1.diff). Arms v16 (c), doors D1-D5 (o), doors without D1 (p), sham (x);
LP; seeds 25301-25332; 200 years; years 100-200 counted for the guards; kinds born in years 100-190 followed 5 years.

Observers (read-only):
  CI1's   the guard sums (`../CI1_children_and_aims/run_ci1.py`)
  MP1's   the stage funnel of new kinds needing a made part (`../MP1_made_parts/run_mp1.py`)
  OD1's   the manipulation counts per door, the spread of what is carried, attacks by holders of a hard made thing,
          and the tool factor of things made with a stand-in against things made from the remembered inputs

  python experiments/OD1_open_doors/run_od1.py zero
  python experiments/OD1_open_doors/run_od1.py one <arm> <seed> <years> <out>
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
base.CODES["od1"] = HERE / "code_od1"
base.CODES["v16"] = HERE.parent / "NV16_nature_v16" / "code_v16"
CODE = "od1"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(25301, 25333))        # 32 new paired seeds, used by no study
DOORS = ("similar_parts", "containers_carry", "made_binders", "made_hammers", "layers_add")
OFF = {d: 0 for d in DOORS}
ARMS = {"c": {**base.LP, **OFF},
        "o": {**base.LP, **{d: 1 for d in DOORS}},
        "p": {**base.LP, **{d: 1 for d in DOORS}, "similar_parts": 0},
        "x": {**base.LP, **OFF, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
GROWN = 16 * WPY
USES = ("forage", "hunt", "wood", "stone", "fiber", "fight", "carry", "cold")
CUR = []
UNIT = []                                  # the unit check's tally, when it runs (never in a study run)


def best_use(item):
    from acl.matter import factor
    return max(factor(item, u) for u in USES)


class ODObs:
    def __init__(self, w):
        self.w = w
        self.d = Counter()
        CUR[:] = [self]

    def late(self, world):
        return R.LATE[0] <= world.tick < R.LATE[1]

    def made(self, world, p, recipe, standin, item):
        if not self.late(world) or item is None:
            return
        self.d["made_by_make"] += 1
        self.d["made_standin" if standin else "made_original"] += 1
        self.d["factor_standin" if standin else "factor_original"] += best_use(item)

    def crafted(self, world, p, recipe, item):
        from acl.matter import MATERIALS
        if not self.late(world):
            return
        if recipe["verb"] == "bind" and recipe["binder"] not in MATERIALS and item is not None:
            self.d["made_binder_used"] += 1
        if recipe["verb"] == "strike" and recipe["tool"] not in MATERIALS:
            self.d["made_hammer_used"] += 1
            self.d["made_hammer_flaked"] += int(item is not None)

    def __call__(self, world, events):
        from acl.matter import best_item, layered
        tick = world.tick - 1
        if not (R.LATE[0] <= tick < R.LATE[1]):
            return
        hard_holders = set()
        for p in world.living():
            if world.tick - p.birth < GROWN:
                continue
            d = self.d
            n, m = len(p.items), p.mat_total()
            d["grown_weeks"] += 1
            d["items_sum"] += n
            d["items_sq"] += n * n
            d["items_max"] = max(d["items_max"], n)
            d["mats_sum"] += m
            d["over_items_weeks"] += int(n > world.cfg.item_limit)
            d["over_mats_weeks"] += int(m > world.cfg.material_limit + 1e-9)
            if n >= 2 and world.cfg.layers_add:         # only where the door is open (else it is a counterfactual)
                for use in ("carry", "cold"):
                    d[f"layer_{use}_weeks"] += int(layered(p, use) > best_item(p, use)[1] + 1e-12)
            if any(it["hard"] >= 50 for it in p.items):
                hard_holders.add(p.id)
                d["hard_holder_weeks"] += 1
        for ev in events:
            if ev["k"] in ("attack", "kill"):
                self.d[f"{ev['k']}s"] += 1
                self.d[f"{ev['k']}s_by_hard_holder"] += int(ev.get("a") in hard_holders)

    def results(self):
        return {"od": dict(self.d)}


LAST = {}                                  # p.id -> the item the last _craft returned (runner state, not the world's)
STANDIN = {}                               # p.id -> (remembered recipe, resolved recipe) while a make with a stand-in runs


def install():
    from acl import actions, mind
    M.install()
    if getattr(actions._make, "_od1", False):
        return
    make0, craft0 = actions._make, actions._craft

    def _make(world, p, sig, eff):
        recipe = p.recipes.get(sig)
        o = CUR[0] if CUR else None
        r = mind.resolve_recipe(world, p, recipe) if recipe is not None else None     # pure: no draw, no change
        standin = r is not None and r != recipe
        if standin:
            STANDIN[p.id] = (recipe, r)
            if UNIT:
                check_standin(world, p, recipe, r)
        LAST.pop(p.id, None)
        try:
            make0(world, p, sig, eff)
        finally:
            STANDIN.pop(p.id, None)
        item = LAST.pop(p.id, None)
        if o is not None and recipe is not None:
            o.made(world, p, recipe, standin, item)

    def _craft(world, p, recipe):
        o = CUR[0] if CUR else None
        pre = check_craft_before(world, p, recipe) if UNIT else None
        item = craft0(world, p, recipe)
        if UNIT:
            check_craft_after(world, p, recipe, item, pre)
        if o is not None:
            o.crafted(world, p, recipe, item)
        LAST[p.id] = item
        return item
    _make._od1 = True
    actions._make = _make
    actions._craft = _craft
    actions.HANDLERS["make"] = _make


# --- unit checks (an o world, never a study run) --------------------------------------------------------------------

def check_standin(world, p, recipe, r):
    from acl.matter import PROPS
    from acl.mind import _props_of
    st = UNIT[0]
    st["standins"] += 1
    keys = [k for k in ("target", "tool", "material", "part", "binder") if k in recipe] + \
           ([("parts", 0), ("parts", 1)] if "parts" in recipe else [])
    for k in keys:
        a = recipe[k[0]][k[1]] if isinstance(k, tuple) else recipe[k]
        b = r[k[0]][k[1]] if isinstance(k, tuple) else r[k]
        if a == b:
            continue
        pa, pb = _props_of(world, p, a), _props_of(world, p, b)
        if pa is None or pb is None or max(abs(pa[x] - pb[x]) for x in PROPS) > 10:
            st["standin_too_far"] += 1


def check_craft_before(world, p, recipe):
    from acl.matter import MATERIALS
    from acl.mind import can_make
    tool = recipe.get("tool") if recipe["verb"] == "strike" else None
    binder = recipe.get("binder") if recipe["verb"] == "bind" else None
    tool = tool if tool and tool not in MATERIALS else None
    binder = binder if binder and binder not in MATERIALS else None
    return {"cnt": Counter(it["sig"] for it in p.items), "tool": tool, "binder": binder, "can": can_make(p, recipe),
            "g0": len(world.ground),        # corrected 8 Nov, before data: things set down at the carry limit count
                                            # as kept, not used up (explore_hammer_check.py traced all 5 zero-check cases)
            "tool_item": next((it for it in p.items if tool and it["sig"] == tool), None),
            "binder_item": next((it for it in p.items if binder and it["sig"] == binder), None)}


def check_craft_after(world, p, recipe, item, pre):
    st = UNIT[0]
    if not pre["can"]:
        return
    sub = STANDIN.get(p.id)
    via_standin = sub is not None and sub[1] is recipe
    cnt = Counter(it["sig"] for it in p.items)
    if pre["binder"] is not None:
        st["made_binders"] += 1
        b = pre["binder"]
        used = 1 + sum(1 for x in recipe["parts"] if x == b)
        made_same = int(item is not None and item["sig"] == b)
        down = sum(1 for g in world.ground[pre["g0"]:] if g["item"]["sig"] == b)
        if cnt[b] + down != pre["cnt"][b] - used + made_same:
            st["binder_not_used_up"] += 1
        if pre["binder_item"]["flex"] < 50:
            st["binder_flex_low"] += 1
            st["binder_flex_low_not_standin"] += int(not (via_standin and sub[0]["binder"] != b))
    if pre["tool"] is not None:
        st["made_hammers"] += 1
        t = pre["tool"]
        obj = pre["tool_item"]
        kept = any(it is obj for it in p.items)
        down = any(g["item"] is obj for g in world.ground[pre["g0"]:])
        st["hammer_set_down_at_limit"] += int(not kept and down)
        if not kept and not down:
            st["hammer_used_up"] += 1
        if pre["tool_item"]["hard"] < 50:
            st["hammer_hard_low"] += 1
            st["hammer_hard_low_not_standin"] += int(not (via_standin and sub[0]["tool"] != t))


def independent_layer(p, use):
    from acl.matter import factor
    es = sorted((factor(it, use) - 1.0 for it in p.items), reverse=True)
    es = [e for e in es if e > 0]
    v = 0.0
    for i, e in enumerate(es):
        v = e if i == 0 else v + e / 2          # the best fully, each next half (v >= e when sorted)
        v = min(v, 1.0)
    return 1.0 + v


def unit_check(seed, years=30):
    w = make(seed, "o")
    from acl import matter
    st = Counter()
    UNIT[:] = [st]
    install()
    CUR[:] = []
    try:
        for _ in range(years * WPY):
            w.step()
            if w.tick % 3 == 0:
                for p in w.living():
                    st["looks"] += 1
                    for use in ("carry", "cold"):
                        a, b = matter.layered(p, use), independent_layer(p, use)
                        if abs(a - b) > 1e-12:
                            st["layer_mismatch"] += 1
                        if a > 2.0 + 1e-12:
                            st["layer_over_cap"] += 1
                        st["layered_adds"] += int(a > matter.best_item(p, use)[1] + 1e-12)
                    f = matter.use_factor(w, p, "carry")
                    if matter.item_cap(w, p) != int(3 * f) or abs(matter.material_cap(w, p) - 20 * f) > 1e-9:
                        st["cap_mismatch"] += 1
                    st["over_old_item_limit"] += int(len(p.items) > 3)
        st.update(direct_door_check(w))
    finally:
        UNIT[:] = []
    ok = (st["looks"] > 0 and st["layer_mismatch"] == 0 and st["layer_over_cap"] == 0 and st["cap_mismatch"] == 0
          and st["standin_too_far"] == 0 and st["binder_not_used_up"] == 0 and st["hammer_used_up"] == 0
          and st["binder_flex_low_not_standin"] == 0 and st["hammer_hard_low_not_standin"] == 0
          and st["direct_ok"] == 2)
    return ok, dict(st)


def direct_door_check(w):
    """D3 and D4 by hand in a reloaded copy (they can be rare in 30 years): a grown person given a flexible made thing
    binds with it, and it is used up; given a hard made thing, strikes with it, and it stays."""
    from acl.world import World
    from acl import actions, matter
    out = Counter()
    x = World.from_dict(json.loads(json.dumps(w.to_dict())))
    p = next(q for q in sorted(x.living(), key=lambda q: q.id) if q.age(x.tick) >= GROWN)
    cord = matter.item_from("od1test_cord", {**matter.raw_props("fiber"), "flex": 70})
    rock = matter.item_from("od1test_rock", {**matter.raw_props("stone"), "hard": 75})
    p.items = [cord, rock]
    p.mats["wood"] = p.mats.get("wood", 0.0) + 2.0
    got = actions._craft(x, p, {"verb": "bind", "parts": ["wood", "wood"], "binder": "od1test_cord"})
    out["direct_ok"] += int(got is not None and not any(it["sig"] == "od1test_cord" for it in p.items))
    flaked = 0
    for _ in range(20):                       # a strike can fail to flake; the hammer stays either way
        p.mats["flint"] = max(p.mats.get("flint", 0.0), 1.0)
        flaked += int(actions._craft(x, p, {"verb": "strike", "target": "flint", "tool": "od1test_rock"}) is not None)
    out["direct_ok"] += int(any(it["sig"] == "od1test_rock" for it in p.items) and flaked > 0)
    out["direct_flaked_of_20"] = flaked
    return out


# --- the standard harness (as VW1's) ----------------------------------------------------------------------------------

def attach(w):
    ci = R.CI1Obs(w)
    mp = M.MP1Obs(w)
    od = ODObs(w)
    w.observers += [ci, mp, od]
    return ci, mp, od


def combined(ci, mp, od):
    r = ci.results()
    r.pop("kinds", None)
    m = mp.results()
    r.update({"stages": m["stages"], "fates": m["fates"], "parts_check": m["check"], **od.results()})
    return r


def make(seed, arm, code=CODE):
    base.setup(code)
    kw = dict(ARMS[arm])
    if code != CODE:
        for d in DOORS:
            kw.pop(d, None)
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
        extra = ":" + json.dumps({"od": r["od"], "parts_check": r["parts_check"]}, sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def reload_check(seed):
    w = make(seed, "o")
    from acl.world import World
    for _ in range(10 * WPY):
        w.step()
    b = World.from_dict(json.loads(json.dumps(w.to_dict())))
    for x in (w, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(w) == base.world_hash(b) and all(getattr(b.cfg, d) == 1 for d in DOORS)


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
             for code, arm, obs in (("v16", "c", 0), ("od1", "c", 0), ("od1", "c", 1), ("od1", "o", 0), ("od1", "o", 1),
                                    ("od1", "p", 0), ("od1", "x", 0))]
    with ThreadPoolExecutor(2) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        unit = ex.submit(call, "unit", 701)
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
    for seed, years in ((501, 20), (601, 60)):
        same = hs(got[("v16", "c", seed, years, 0)]) == hs(got[("od1", "c", seed, years, 0)])
        ro = (hs(got[("od1", "c", seed, years, 0)]) == hs(got[("od1", "c", seed, years, 1)])
              and hs(got[("od1", "o", seed, years, 0)]) == hs(got[("od1", "o", seed, years, 1)]))
        acts = hs(got[("od1", "o", seed, years, 0)]) != hs(got[("od1", "c", seed, years, 0)])
        pacts = hs(got[("od1", "p", seed, years, 0)]) != hs(got[("od1", "c", seed, years, 0)])
        sham = hs(got[("od1", "x", seed, years, 0)]) != hs(got[("od1", "c", seed, years, 0)])
        cinfo = json.loads(got[("od1", "c", seed, years, 1)].split(":", 2)[2])["od"]
        off = (cinfo.get("made_binder_used", 0) == 0 and cinfo.get("made_hammer_used", 0) == 0
               and cinfo.get("made_standin", 0) == 0 and cinfo.get("over_items_weeks", 0) == 0)
        ok &= same and ro and acts and pacts and sham and off
        info = got[("od1", "o", seed, years, 1)].split(":", 2)[2]
        lines.append(f"seed {seed}, {years} years: code_od1 with the five doors at 0 = code_v16: {'yes' if same else 'NO'}; "
                     f"observers read-only (c, o): {'yes' if ro else 'NO'}; doors act: {'yes' if acts else 'NO'}; "
                     f"doors without D1 act: {'yes' if pacts else 'NO'}; the sham acts: {'yes' if sham else 'NO'}; "
                     f"no door used in c: {'yes' if off else 'NO'}; o: {info}")
    u = json.loads(unit.result())
    ok &= u[0]
    lines.append(f"unit checks, arm o, seed 701, 30 years (stand-ins within 10 in all 10 properties; made binders used up; "
                 f"made hammers not used up, hard >= 50 unless a D1 stand-in; layered values equal an independent "
                 f"computation and never pass the cap; limits = 3 and 20 x the carry factor; D3 and D4 by a direct check): {'yes' if u[0] else 'NO'}; {u[1]}")
    t = rl.result()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm o, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_od1 fingerprint: {call('fp')}")
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
    res = {"arm": arm, "seed": seed, "nature": "code_od1", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
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
    elif cmd == "unit":                   # an optional third argument shortens it, for code tests only
        print(json.dumps(unit_check(int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 30)))
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
