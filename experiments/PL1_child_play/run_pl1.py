"""PL1 — how much do ACL's children play, against forager children? (questions.md, frozen as `PL1-frozen`).
Read-only on `code_v8` (live nature). Wrappers call the original unchanged and only note the state:
  thought.steer            the options weighed this week (is play available);
  actions.perform          the option chosen;
  actions._gain_skill      each gain in crafting skill, by what the person was doing;
  actions.HANDLERS["play"] play carried out (a check: equals play chosen).

  python experiments/PL1_child_play/run_pl1.py zero
  python experiments/PL1_child_play/run_pl1.py one <arm> <seed> <years> <out>
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
CODE = EXP / "NV8_nature_v8" / "code_v8"
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(20101, 20133))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9981, 9980)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
LP = {"founders": 80, "width": 80, "height": 80}
ARMS = {"o": {**LP}}                       # o = live nature v8
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
BANDS = ((1, 2), (3, 6), (7, 12), (13, 18))   # completed years, inclusive


def band_of(years):
    for lo, hi in BANDS:
        if lo <= years <= hi:
            return f"{lo}-{hi}"
    return None


def setup():
    sys.path.insert(0, str(CODE))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


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


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODE / "acl")


class PL1Obs:
    def __init__(self, w):
        self.w = w
        self.mismatch = Counter()
        self.n = Counter()                    # "band|key" -> count or summed skill
        self.avail = {}                       # person -> tick at which play was among the options weighed
        self.kids = defaultdict(lambda: defaultdict(lambda: [0, 0]))   # person -> band -> [weeks, play]
        self.census = []

    def chose(self, world, p, action):
        tick = world.tick
        b = band_of(p.age(tick) // WPY)
        if b is None:
            return
        avail = self.avail.get(p.id) == tick
        play = action == "play"
        self.n[f"{b}|weeks"] += 1
        self.n[f"{b}|avail"] += avail
        self.n[f"{b}|play"] += play
        self.n[f"{b}|play_when_avail"] += play and avail
        if not play:
            self.n[f"{b}|noplay_unavail"] += not avail
            self.n[f"{b}|noplay_avail"] += avail
        if play and not avail:
            self.mismatch["play_chosen_unavailable"] += 1
        k = self.kids[p.id][b]
        k[0] += 1
        k[1] += play

    def skill(self, world, p, gain):
        b = band_of(p.age(world.tick) // WPY) or "other_ages"
        what = p.doing if p.doing in ("play", "make") else "other"
        self.n[f"{b}|craft_{what}"] += gain

    def __call__(self, world, events):
        tick = world.tick - 1
        if tick % WPY == WPY - 1:
            living = world.living()
            self.census.append([tick // WPY, len(living), sum(1 for p in living if p.age(world.tick) >= 16 * WPY)])

    def results(self):
        chosen_play = sum(v for k, v in self.n.items() if k.endswith("|play"))
        if self.n["play_handler_kids"] != chosen_play:
            self.mismatch["play_handler_vs_chosen"] += 1
        surv = Counter()
        end = self.w.tick
        for pid, bands in self.kids.items():
            p = self.w.people.get(pid)
            if p is None:
                continue
            last = end if p.alive else p.death_tick
            age_end = (last - p.birth) // WPY
            for b, (wk, pl) in bands.items():
                hi = int(b.split("-")[1])
                if age_end >= hi + 1:
                    surv[f"{b}|weeks"] += wk
                    surv[f"{b}|play"] += pl
                    surv[f"{b}|children"] += 1
        return {"counts": dict(self.n), "survivors": dict(surv), "mismatch": dict(self.mismatch),
                "census_fields": ["year", "living", "adults"], "census": self.census}


def install(w, obs):
    from acl import actions, thought
    o_steer, o_perform, o_gain, o_play = thought.steer, actions.perform, actions._gain_skill, actions.HANDLERS["play"]

    def steer(p, options):
        out = o_steer(p, options)
        if w.people.get(p.id) is p and any(o[1] == "play" for o in out):
            obs.avail[p.id] = w.tick
        return out

    def perform(world, p, option):
        if world is w:
            obs.chose(world, p, option[0])
        return o_perform(world, p, option)

    def gain(world, p, skill):
        if world is not w or skill != "crafting":
            return o_gain(world, p, skill)
        before = p.skills["crafting"]
        out = o_gain(world, p, skill)
        obs.skill(world, p, p.skills["crafting"] - before)
        return out

    def play(world, p, target, eff):
        if world is w and band_of(p.age(world.tick) // WPY) is not None:
            obs.n["play_handler_kids"] += 1
        return o_play(world, p, target, eff)

    thought.steer = steer
    actions.perform = perform
    actions._gain_skill = gain
    actions.HANDLERS["play"] = play


def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = PL1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        res = obs.results()
        n = res["counts"]
        extra = ":" + json.dumps({**res["mismatch"], "_weeks_3_6": n.get("3-6|weeks", 0),
                                  "_play_3_6": n.get("3-6|play", 0), "_avail_3_6": n.get("3-6|avail", 0),
                                  "_play_handler_kids": n.get("play_handler_kids", 0)},
                                 sort_keys=True, separators=(",", ":"))
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
    specs = [(seed, years, obs) for seed, years in ((501, 20), (601, 60)) for obs in (1, 0)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", "o", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        a, b = got[(seed, years, 1)], got[(seed, years, 0)]
        same = a.split(":")[:2] == b.split(":")[:2]
        info = json.loads(a.split(":", 2)[2])
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = same and not any(mism.values()) and info.get("_weeks_3_6", 0) > 0
        ok &= t
        shown = ", ".join(f"{k[1:]} {v}" for k, v in sorted(info.items()) if k.startswith("_"))
        lines.append(f"arm v8, seed {seed}, {years} years: identical with and without the observer and wrappers (state "
                     f"and random numbers): {'yes' if same else 'NO'}; wrapper-vs-law mismatches: {mism or 'none'}; "
                     f"{shown}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm v8, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
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
    obs = PL1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v8 (read-only audit)", "code_hash": f0,
           "code_hash_after": fingerprint(), "final_tick": w.tick, "extinct": not w.living(),
           "world_hash": world_hash(w), **obs.results()}
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
