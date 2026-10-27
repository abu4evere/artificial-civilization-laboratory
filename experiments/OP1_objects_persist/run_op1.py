"""OP1 — objects in the world (questions.md, frozen as `OP1-frozen`). Nature-change study: `code_op1` = `code_v7` + one
setting, `ground_items` (0 = v7 exactly; v7_to_op1.diff). Arms c (v7), o (setting 1), x (sham: one extra draw in week
one). A read-only observer wraps `actions._keep` (to count carry-limit overflows) and reads weekly events and a yearly
census.

  python experiments/OP1_objects_persist/run_op1.py zero
  python experiments/OP1_objects_persist/run_op1.py one <arm> <seed> <years> <out>
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
CODES = {"op1": HERE / "code_op1", "v7": EXP / "NV7_nature_v7" / "code_v7"}
CODE = CODES["op1"]
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(19301, 19333))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9937, 9936)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
LP = {"founders": 80, "width": 80, "height": 80}
ARMS = {"c": {**LP}, "o": {**LP, "ground_items": 1}, "x": {**LP, "sham_draw": 1}}
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]


def setup(code="op1"):
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


def fingerprint(code="op1"):
    from run_e7 import code_hash
    return code_hash(CODES[code] / "acl")


class OP1Obs:
    def __init__(self, w):
        self.w = w
        self.mismatch = Counter()
        self.c = defaultdict(float)
        self.census = []                       # [year, living, adults, items_adults, makes]
        self.makes_year = 0
        self.weeks = []                        # weeks on the ground at pick-up

    def keep(self, orig, p, item, limit, world):
        over = max(0, len(p.items) + 1 - limit)
        g0 = len(world.ground) if world is not None and hasattr(world, "ground") else 0
        out = orig(p, item, limit, world) if world is not None else orig(p, item, limit)
        if over and world is self.w:
            self.c["keep_overflow"] += over
            if world.cfg.ground_items if hasattr(world.cfg, "ground_items") else False:
                if len(world.ground) - g0 != over:
                    self.mismatch["drop_missing"] += 1
            else:
                self.c["deleted_at_limit"] += over
        return out

    def __call__(self, world, events):
        tick = world.tick - 1
        for ev in events:
            k = ev["k"]
            if k == "drop":
                self.c["drops"] += 1
            elif k == "pickup":
                self.c["pickups"] += 1
                self.c["pickups_by_other"] += ev.get("a") != ev.get("b")
                self.weeks.append(ev.get("weeks", 0))
            elif k == "make" and ev.get("thing"):
                self.makes_year += 1
        if tick % WPY == WPY - 1:
            living = world.living()
            adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
            self.census.append([tick // WPY, len(living), len(adults), sum(len(p.items) for p in adults),
                                self.makes_year])
            self.makes_year = 0

    def results(self):
        ground = len(getattr(self.w, "ground", []))
        c = dict(self.c)
        c["ground_end"] = ground
        if getattr(self.w.cfg, "ground_items", 0) and c.get("drops", 0) - c.get("pickups", 0) != ground:
            self.mismatch["conservation"] += 1
        ws = sorted(self.weeks)
        return {"counts": c, "mismatch": dict(self.mismatch), "pickup_weeks_median": ws[len(ws) // 2] if ws else None,
                "census_fields": ["year", "living", "adults", "items_adults", "makes"], "census": self.census}


def install(w, obs):
    from acl import actions
    orig = actions._keep

    def keep(p, item, limit, world=None):
        if world is None:
            return orig(p, item, limit) if orig.__code__.co_argcount == 3 else orig(p, item, limit, None)
        return obs.keep(orig, p, item, limit, world)

    actions._keep = keep


def hashrun(code, arm, seed, years, observe):
    setup(code)
    kw = dict(ARMS[arm])
    if code == "v7":
        kw.pop("ground_items", None)
    w = make_world(seed, kw)
    obs = None
    if observe:
        obs = OP1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        res = obs.results()
        extra = ":" + json.dumps({**res["mismatch"], "_drops": res["counts"].get("drops", 0),
                                  "_over": res["counts"].get("keep_overflow", 0)}, sort_keys=True, separators=(",", ":"))
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
    return world_hash(a) == world_hash(b) and b.cfg.ground_items == 1


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
             for code, arm, obs in (("v7", "c", 0), ("op1", "c", 0), ("op1", "o", 1), ("op1", "o", 0),
                                    ("op1", "x", 0), ("op1", "c", 1))]
    with ThreadPoolExecutor(6) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        v7 = got[("v7", "c", seed, years, 0)]
        c0 = got[("op1", "c", seed, years, 0)]
        o1 = got[("op1", "o", seed, years, 1)]
        o0 = got[("op1", "o", seed, years, 0)]
        s0 = got[("op1", "x", seed, years, 0)]
        c1 = got[("op1", "c", seed, years, 1)]
        same_v7 = hs(v7) == hs(c0)
        ro = hs(o1) == hs(o0) and hs(c1) == hs(c0)
        acts = hs(o0) != hs(c0)
        sham = hs(s0) != hs(c0)
        info = json.loads(o1.split(":", 2)[2])
        info_c = json.loads(c1.split(":", 2)[2])
        mism = {k: v for d in (info, info_c) for k, v in d.items() if not k.startswith("_")}
        t = same_v7 and ro and acts and sham and not any(mism.values()) and info.get("_drops", 0) > 0
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_op1 with the setting 0 equals code_v7: {'yes' if same_v7 else 'NO'}; "
                     f"observer read-only (arms o and c): {'yes' if ro else 'NO'}; the setting acts: "
                     f"{'yes' if acts else 'NO'}; the sham acts: {'yes' if sham else 'NO'}; eviction-prediction "
                     f"mismatches: {mism or 'none'}; drops (o) {info.get('_drops')}, overflows "
                     f"{info.get('_over')}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm o, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_op1 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = OP1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "op1", "code_hash": f0, "code_hash_after": fingerprint(),
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
