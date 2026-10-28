"""LR1 — does nature v8 stay healthy over 1,000 years? (questions.md, frozen as `LR1-frozen`). Read-only on `code_v8`:
arms v7 (`ground_items` 0, equal to `code_v7`), v8 (live nature) and x (sham); a read-only observer reads the law's
`drop` / `pickup` events and takes a yearly census.

  python experiments/LR1_long_run_v8/run_lr1.py zero
  python experiments/LR1_long_run_v8/run_lr1.py one <arm> <seed> <years> <out>
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
CODES = {"op1": EXP / "NV8_nature_v8" / "code_v8", "v7": EXP / "NV7_nature_v7" / "code_v7"}
CODE = CODES["op1"]
OUT = HERE / "output"
WPY, YEARS = 52, 1000
SEEDS = tuple(range(19601, 19633))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9931, 9930)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
LP = {"founders": 80, "width": 80, "height": 80}
ARMS = {"c": {**LP, "ground_items": 0}, "o": {**LP}, "x": {**LP, "sham_draw": 1}}   # c = v7, o = v8, x = sham
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


class LR1Obs:
    def __init__(self, w):
        self.w = w
        self.mismatch = Counter()
        self.y = defaultdict(float)
        self.census = []      # [year, living, adults, items_adults, ground, ground_max_tile, drops, pickups, pickups_other]
        self.drops = self.picks = 0

    def __call__(self, world, events):
        tick = world.tick - 1
        for ev in events:
            if ev["k"] == "drop":
                self.y["drops"] += 1
                self.drops += 1
            elif ev["k"] == "pickup":
                self.y["pickups"] += 1
                self.y["pickups_other"] += ev.get("a") != ev.get("b")
                self.picks += 1
        if tick % WPY == WPY - 1:
            living = world.living()
            adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
            ground = getattr(world, "ground", [])
            per_tile = Counter((g["x"], g["y"]) for g in ground)
            if self.drops - self.picks != len(ground):
                self.mismatch["conservation"] += 1
            self.census.append([tick // WPY, len(living), len(adults), sum(len(p.items) for p in adults), len(ground),
                                max(per_tile.values()) if per_tile else 0, self.y["drops"], self.y["pickups"],
                                self.y["pickups_other"]])
            self.y = defaultdict(float)

    def results(self):
        return {"counts": {"drops": self.drops, "pickups": self.picks}, "mismatch": dict(self.mismatch),
                "census_fields": ["year", "living", "adults", "items_adults", "ground", "ground_max_tile", "drops",
                                  "pickups", "pickups_other"], "census": self.census}


def install(w, obs):
    pass


def hashrun(code, arm, seed, years, observe):
    setup(code)
    kw = dict(ARMS[arm])
    if code == "v7":
        kw.pop("ground_items", None)
    w = make_world(seed, kw)
    obs = None
    if observe:
        obs = LR1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        res = obs.results()
        extra = ":" + json.dumps({**res["mismatch"], "_drops": res["counts"].get("drops", 0),
                                  "_pickups": res["counts"].get("pickups", 0)}, sort_keys=True, separators=(",", ":"))
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
    return world_hash(a) == world_hash(b) and b.cfg.ground_items == 1 and bool(b.ground)


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
        lines.append(f"seed {seed}, {years} years: code_v8 with ground_items 0 equals code_v7: {'yes' if same_v7 else 'NO'}; "
                     f"observer read-only (arms v8 and v7): {'yes' if ro else 'NO'}; the setting acts: "
                     f"{'yes' if acts else 'NO'}; the sham acts: {'yes' if sham else 'NO'}; conservation "
                     f"mismatches: {mism or 'none'}; drops (v8) {info.get('_drops')}, pick-ups "
                     f"{info.get('_pickups')}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm o, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_v8 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = LR1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v8 (read-only check)", "code_hash": f0, "code_hash_after": fingerprint(),
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
