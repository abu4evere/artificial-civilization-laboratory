"""RF1 — why do the inputs never come together? (questions.md, frozen as `RF1-frozen`). Read-only on live nature v13
(`code_v13`); VA1's runner and observer supply the set-up and the kinds (world-new kinds first made in play in years
130-165, each followed 5 years in its inventor's weeks). Wrappers only watch:
  thought.steer      (VA1's wrapper) the options a person is offered, just before the choice
  mind.softmax_pick  the index the choice drew; the original is called with the same arguments, so the draw is untouched
  week's end         VA1's stages (inputs in hand while the recipe is known), and whether a chosen gather added stock

A wanting week: the inventor is grown, the recipe is known, its value (itemval, or the value as a part of a valued
thing, as the make option computes it) is above 0.05, and no fresh one is held (_holding, worn_ok False). The missing
inputs are read from the recipe exactly as can_make reads it (raw, part, wet; a fill recipe has none to get). A heat
recipe's fire is the make option's own separate test, not an input: it is tallied apart, so that the unit check
"missing is empty exactly when can_make is True" holds.

  python experiments/RF1_remaking_funnel/run_rf1.py zero
  python experiments/RF1_remaking_funnel/run_rf1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "VA1_value_at_invention"))
import run_va1 as V  # noqa: E402

base = V.base
CODE = "v13"
WPY, YEARS = V.WPY, 170
SEEDS = tuple(range(23801, 23833))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9887, 9886)
ARMS = {"c": {**base.LP}}
JOBS = [f"c:{s}" for s in SEEDS]
OUT = HERE / "output"
WIN = V.WIN                                # VA1's window list, shared (VA1Obs reads it)
REMAKE = V.REMAKE
GROWN = ("teen", "adult", "elder")
KIND_FIELDS = ["ww", "obt", "off", "cho", "comp", "full", "lost", "make_offered", "remade"]
NOT = ("young", "gone", "low", "held")      # amendment 1: why a decision week of the inventor was not a wanting week


def missing_inputs(p, recipe):
    """What the recipe still needs that p does not have, read as can_make reads it: [(type, what)]."""
    from acl.matter import SOFT_WHEN_WET, MATERIALS
    verb = recipe["verb"]
    out = []
    if verb == "shape":
        m = recipe["material"]
        if p.mats.get(m, 0.0) < 1.0:
            out.append(("raw", m))
        elif p.damp.get(m, 0) < SOFT_WHEN_WET:
            out.append(("wet", m))
        return out
    if verb == "heat":
        part = recipe["part"]
        if part in MATERIALS:
            if p.mats.get(part, 0.0) < 1.0:
                out.append(("raw", part))
        elif not any(it["sig"] == part for it in p.items):
            out.append(("part", part))
        return out
    if verb == "fill":
        return [("fill", None)]
    need: dict = {}
    if verb == "strike":
        need[recipe["target"]] = 1
        need[recipe["tool"]] = need.get(recipe["tool"], 0) + 1
        if recipe["tool"] != recipe["target"]:
            need[recipe["tool"]] = 1
    else:
        made: dict = {}
        for part in recipe["parts"]:
            if part in p.mats:
                need[part] = need.get(part, 0) + 1
            else:
                made[part] = made.get(part, 0) + 1
        for sig, n in made.items():
            if sum(1 for it in p.items if it["sig"] == sig) < n:
                out.append(("part", sig))
        need[recipe["binder"]] = need.get(recipe["binder"], 0) + 1
    for k, n in need.items():
        if p.mats.get(k, 0.0) < n:
            out.append(("raw", k))
    return out


class RF1Obs(V.VA1Obs):
    def __init__(self, w):
        super().__init__(w)
        self.pending = None             # (person, options, [(sig, missing, info)]) between the offer and the draw
        self.unit2 = [0, 0]             # [wrong, checked]: missing empty exactly when can_make
        self.week = {}                  # sig -> {kind: stock at the decision} for a chosen gather this week
        self.tally = {"ww": 0, "raw": 0, "raw_ungatherable": 0, "part": 0, "wet": 0, "fill": 0, "fire_away": 0,
                      "at_limit": 0, "instead": {}}

    def _wanting(self, world, p, kd, sig):
        """None if p is wanting the kind this week; otherwise why not (amendment 1): young, gone, low, held."""
        from acl.mind import _holding, _wanted_parts
        if p is None or not p.alive or p.stage(world.tick) not in GROWN:
            return "young"
        if sig not in p.recipes:
            return "gone"
        v = max(p.itemval.get(sig, 0.0), _wanted_parts(p).get(sig, 0.0))
        if v <= 0.05:
            return "low"
        if _holding(p, sig):
            return "held"
        return None

    def offered(self, world, p, options):
        super().offered(world, p, options)
        if world is not self.w:
            return
        from acl.mind import can_make, _material_wants, GATHERABLE
        tick = world.tick
        mine = [(sig, kd) for sig, kd in self.kinds.items()
                if kd["inv"] == p.id and kd["recipe"] is not None and kd["t"] <= tick < kd["t"] + REMAKE]
        rows = []
        c = world.cfg
        for sig, kd in mine:
            why = self._wanting(world, p, kd, sig)
            if why is not None:
                nw = kd.setdefault("not", {})
                nw[why] = nw.get(why, 0) + 1
                continue
            recipe = p.recipes[sig]
            miss = missing_inputs(p, recipe)
            self.unit2[1] += 1
            self.unit2[0] += int((len(miss) == 0) != can_make(p, recipe))
            room = p.mat_total() < c.material_limit
            wants = _material_wants(p, world.season)
            obt = False
            raw_kinds, parts = set(), set()
            t = self.tally
            t["ww"] += 1
            t["at_limit"] += int(not room)
            if recipe["verb"] == "heat" and world.tile(p.loc).fire <= 0:
                t["fire_away"] += 1
            for typ, what in miss:
                t[typ] += 1
                if typ == "raw":
                    raw_kinds.add(what)
                    if what not in GATHERABLE:
                        t["raw_ungatherable"] += 1
                    if room and self._near(world, p, what):
                        obt = True
                elif typ == "part":
                    parts.add(what)
                    if what in p.recipes:
                        obt = True
            off = any((o[1] == "gather" and o[2][1] in raw_kinds) or (o[1] == "make" and o[2] in parts)
                      for o in options)
            kd["ww"] = kd.get("ww", 0) + 1
            kd["obt"] = kd.get("obt", 0) or int(obt)
            kd["off"] = kd.get("off", 0) or int(off)
            kd.setdefault("cho", 0)
            kd.setdefault("comp", 0)
            kd.setdefault("lost", 0)
            lv = kd.setdefault("levels", {})
            for k in raw_kinds:                      # lower than after an earlier completed gather: lost or used up
                if k in lv and p.mats.get(k, 0.0) < lv[k] - 1e-9:
                    kd["lost"] = 1
            rows.append((sig, raw_kinds, parts, {k: wants.get(k, 0.0) for k in raw_kinds}))
        self.pending = (p, options, rows) if rows else None

    def _near(self, world, p, kind):
        c = world.cfg
        r = c.reach
        x0, y0 = p.loc
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if world.tile(((x0 + dx) % c.width, (y0 + dy) % c.height)).material(kind) >= 1.0:
                    return True
        return False

    def picked(self, i):
        if self.pending is None:
            return
        p, options, rows = self.pending
        self.pending = None
        o = options[i]
        toward = False
        for sig, raw_kinds, parts, _ in rows:
            kd = self.kinds[sig]
            if (o[1] == "gather" and o[2][1] in raw_kinds) or (o[1] == "make" and o[2] in parts):
                kd["cho"] = 1
                toward = True
                if o[1] == "gather":
                    self.week.setdefault(sig, {})[o[2][1]] = (p.id, p.mats.get(o[2][1], 0.0))
        if not toward:
            ins = self.tally["instead"]
            ins[o[1]] = ins.get(o[1], 0) + 1

    def __call__(self, world, events):
        super().__call__(world, events)
        for sig, got in self.week.items():          # did a chosen gather of a missing input add stock?
            kd = self.kinds[sig]
            for kind, (pid, before) in got.items():
                p = world.people.get(pid)
                if p is not None and p.mats.get(kind, 0.0) > before + 1e-9:
                    kd["comp"] = 1
                    kd["levels"][kind] = p.mats.get(kind, 0.0)
        self.week = {}

    def results(self):
        out = super().results()
        rows = []
        for sig, kd in self.kinds.items():
            nw = kd.get("not", {})
            rows.append([kd.get("ww", 0), kd.get("obt", 0), kd.get("off", 0), kd.get("cho", 0), kd.get("comp", 0),
                         kd["inputs"], kd.get("lost", 0), kd["offered"], kd["remade"]] + [nw.get(k, 0) for k in NOT])
        out.update({"rf1_fields": KIND_FIELDS + [f"not_{k}" for k in NOT], "rf1": rows, "tally": self.tally,
                    "unit2": self.unit2})
        return out


def install(w, obs):
    V.install(w, obs)
    import acl.mind as mind
    o_pick = mind.softmax_pick

    def pick(rng, scores, temperature):
        i = o_pick(rng, scores, temperature)
        obs.picked(i)
        return i
    mind.softmax_pick = pick


def hashrun(seed, years, observe):
    WIN[0], WIN[1] = 0, years * WPY
    base.setup(CODE)
    w = base.make_world(seed, ARMS["c"])
    obs = None
    if observe:
        obs = RF1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = f":{len(obs.kinds)},{obs.unit2[0]},{obs.unit2[1]}" if obs else ""
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
                     f"kinds tracked {nk}; wanting weeks {checked}, missing inputs empty exactly when can_make "
                     f"(wrong {wrong}): {'yes' if unit else 'NO'}")
    lines.append(f"code_v13 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    if years < YEARS:                          # a smoke run: kinds from 60% of the run
        WIN[0], WIN[1] = int(years * 0.6) * WPY, years * WPY
    else:
        WIN[0], WIN[1] = 130 * WPY, 170 * WPY
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = base.make_world(seed, ARMS["c"])
    obs = RF1Obs(w)
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
    print(f"{arm} seed {seed}: done, tick {w.tick}, kinds {res['n_kinds']}, wanting weeks {obs.tally['ww']}", flush=True)


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
