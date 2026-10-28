"""IC1 — how does information pass between people today, and where could words begin? (questions.md, frozen as
`IC1-frozen`). Read-only on `code_v8` (live nature). The observer reads the law's events; four wrappers call the
original unchanged and only note the state at that moment:
  information.hear_place   each place offered in talk;
  actions.HANDLERS["talk"] the start of each talk (both people's positions);
  actions._imitate         each habit copy, with its size;
  mind._nearest_spring     each thirst decision with a water target (seen or told).

  python experiments/IC1_information_channels/run_ic1.py zero
  python experiments/IC1_information_channels/run_ic1.py one <arm> <seed> <years> <out>
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
SEEDS = tuple(range(19701, 19733))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9941, 9940)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
LP = {"founders": 80, "width": 80, "height": 80}
ARMS = {"o": {**LP}}                       # o = live nature v8 (ground_items 1 by default in code_v8)
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
SHARED_MIN = 5                             # B2: a pair "shares" water moments when it has at least this many


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


def fresh_tiles(world, loc, radius):
    """Fresh-water tiles within `radius` (the same square and the same test as weather.fresh_near). Draws nothing."""
    from acl.weather import FRESH
    c = world.cfg
    out = set()
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            n = ((loc[0] + dx) % c.width, (loc[1] + dy) % c.height)
            if world.tile(n).biome in FRESH:
                out.add(n)
    return out


class IC1Obs:
    def __init__(self, w):
        self.w = w
        self.mismatch = Counter()
        self.n = Counter()                 # all counts, by name
        self.pairs = Counter()             # pair -> talks in which both see the same fresh-water tile
        self.pair_src = defaultdict(set)   # pair -> water sources shared (the shared tile nearest the first speaker)
        self.pair_weeks = defaultdict(set) # pair -> weeks with such a talk
        self.told = {}                     # (listener, spot) -> out of sight at the telling (accepted water places)
        self.told_used = set()             # (listener, spot) later chosen as a thirst target
        self.dist = Counter()              # distance bands of accepted water places, listener and speaker
        self.imit_size = 0.0
        self.census = []                   # [year, living, adults]

    # --- wrappers' notes ---
    def place(self, world, listener, speaker, key, out, before):
        kind = key[:2]
        self.n[f"{kind}offered"] += 1
        if not out:
            return
        self.n[f"{kind}accepted"] += 1
        for k, v in before.items():
            if k in ("spot", "d_listener", "d_speaker", "thirst"):
                continue
            self.n[f"{kind}acc_{k}"] += int(v)
        if kind == "w:":
            self.n["w:acc_thirst_sum"] += before["thirst"]
            for who in ("listener", "speaker"):
                d = before["d_" + who]
                self.dist[f"{who}_{'sight' if d <= world.cfg.perception else ('5-12' if d <= 12 else '13+')}"] += 1
            self.told[(listener.id, before["spot"])] = before["d_listener"] > world.cfg.perception

    def talk(self, world, p, q):
        c = world.cfg
        fp = fresh_tiles(world, p.loc, c.perception)
        fq = fresh_tiles(world, q.loc, c.perception)
        adults = p.age(world.tick) >= 16 * WPY and q.age(world.tick) >= 16 * WPY
        self.n["talks"] += 1
        self.n["talks_either_sees"] += bool(fp or fq)
        both = fp & fq
        if both:
            from acl.fauna import near
            from acl.util import distance
            pair = tuple(sorted((p.id, q.id)))
            self.n["talks_shared"] += 1
            self.n["talks_shared_adults"] += adults
            self.n["shared_fresh_tiles_sum"] += len(both)
            hp = {id(g) for g in near(world, p.loc, c.perception)}
            self.n["shared_herds_sum"] += sum(1 for g in near(world, q.loc, c.perception) if id(g) in hp)
            self.pairs[pair] += 1
            src = min(both, key=lambda t: (distance(p.loc, t, c.width, c.height), t))
            self.pair_src[pair].add(src)
            self.pair_weeks[pair].add(world.tick)

    # --- events ---
    def __call__(self, world, events):
        tick = world.tick - 1
        for ev in events:
            k = ev["k"]
            if k == "learn":
                if "spot" in ev:
                    self.n["ev_learn_" + ev["spot"][:1]] += 1
                elif "belief" in ev:
                    self.n["ev_learn_belief"] += 1
                elif "thing" in ev:
                    self.n["ev_learn_thing_" + str(ev.get("how"))] += 1
            elif k in ("verified", "refuted"):
                self.n[f"ev_{k}_{str(ev.get('claim', ''))[:1]}"] += 1
            elif k == "vouched":
                self.n["ev_vouched"] += 1
            elif k == "told":
                self.n["ev_story_" + str(ev.get("heard"))] += 1
            elif k == "read":
                self.n["ev_read"] += 1
            elif k == "talk":
                self.n["ev_talk"] += 1
        living = world.living()
        self.n["person_weeks"] += len(living)
        self.n["adult_weeks"] += sum(1 for p in living if p.age(world.tick) >= 16 * WPY)
        if tick % WPY == WPY - 1:
            self.census.append([tick // WPY, len(living), sum(1 for p in living if p.age(world.tick) >= 16 * WPY)])

    def results(self):
        if self.n["talks"] != self.n["ev_talk"]:
            self.mismatch["talks_vs_events"] += 1
        for kind in ("w", "g"):
            if self.n[f"{kind}:accepted"] != self.n[f"ev_learn_{kind}"]:
                self.mismatch[f"{kind}_accepted_vs_events"] += 1
        def longest(weeks):
            best = run = 0
            last = None
            for t in sorted(weeks):
                run = run + 1 if last is not None and t == last + 1 else 1
                best, last = max(best, run), t
            return best
        pairs = sorted(([n, len(self.pair_src[k]), longest(self.pair_weeks[k])] for k, n in self.pairs.items()),
                       reverse=True)
        told = {"accepted": len(self.told), "out_of_sight": sum(self.told.values()),
                "used": len(self.told_used), "used_out_of_sight": sum(self.told[k] for k in self.told_used)}
        return {"counts": dict(self.n), "imit_size_sum": self.imit_size, "pairs_fields": ["shared_talks",
                "sources", "longest_run_weeks"], "pairs": pairs, "told_water": told, "dist": dict(self.dist),
                "mismatch": dict(self.mismatch), "census_fields": ["year", "living", "adults"],
                "census": self.census}


def install(w, obs):
    from acl import actions, information, mind
    from acl.util import distance
    from acl.weather import fresh_near
    orig_hear = information.hear_place
    orig_talk = actions.HANDLERS["talk"]
    orig_imit = actions._imitate
    orig_near = mind._nearest_spring

    def hear_place(world, listener, speaker, key, claim):
        if world is not w or key[:2] not in ("w:", "g:"):
            return orig_hear(world, listener, speaker, key, claim)
        c = world.cfg
        spot = tuple(int(v) for v in key[2:].split(","))
        before = {}
        if key[:2] == "w:":
            before = {
                "new": not listener.springs,                                     # knew no water of their own
                "redundant": fresh_near(world, listener.loc, c.perception) is not None,
                "true": fresh_near(world, spot, 1) is not None,
                "both_see": (fresh_near(world, spot, 1) is not None
                             and distance(listener.loc, spot, c.width, c.height) <= c.perception
                             and distance(speaker.loc, spot, c.width, c.height) <= c.perception),
                "speaker_saw": [spot[0], spot[1]] in speaker.springs,            # own sight, not relayed
                "first_option": not listener.springs and not any(k[:2] == "w:" for k in listener.heard),
                "spot": spot,
                "d_listener": distance(listener.loc, spot, c.width, c.height),
                "d_speaker": distance(speaker.loc, spot, c.width, c.height),
                "thirst": listener.thirst,
            }
        out = orig_hear(world, listener, speaker, key, claim)
        obs.place(world, listener, speaker, key, out, before)
        return out

    def talk(world, p, target, eff):
        if world is w:
            obs.talk(world, p, world.people[target])
        return orig_talk(world, p, target, eff)

    def _imitate(world, learner, model):
        if world is not w:
            return orig_imit(world, learner, model)
        r = learner.rel.get(model.id)
        respect = r.respect if r else 0.0
        gate_pass = not (respect < 0.2 and model.mood <= learner.mood + 0.1)
        before = list(learner.q)
        out = orig_imit(world, learner, model)
        size = sum(abs(a - b) for a, b in zip(learner.q, before))
        changed = size > 0
        obs.n["imit_calls"] += 1
        obs.n["imit_copies"] += gate_pass
        obs.imit_size += size
        if changed and not gate_pass:
            obs.mismatch["imitate_gate"] += 1
        return out

    def _nearest_spring(world, p):
        out = orig_near(world, p)
        if world is w and out is not None:
            own = [out[0], out[1]] in p.springs
            obs.n["thirst_target"] += 1
            obs.n["thirst_target_told"] += not own
            if not own and (p.id, tuple(out)) in obs.told:
                obs.told_used.add((p.id, tuple(out)))
        return out

    information.hear_place = hear_place
    actions.HANDLERS["talk"] = talk
    actions._imitate = _imitate
    mind._nearest_spring = _nearest_spring


def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = IC1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        res = obs.results()
        n = res["counts"]
        extra = ":" + json.dumps({**res["mismatch"], "_talks": n.get("talks", 0), "_w_acc": n.get("w:accepted", 0),
                                  "_shared": n.get("talks_shared", 0), "_imit": n.get("imit_copies", 0),
                                  "_told_target": n.get("thirst_target_told", 0)},
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
        t = same and not any(mism.values()) and info.get("_talks", 0) > 0 and info.get("_w_acc", 0) > 0
        ok &= t
        lines.append(f"arm v8, seed {seed}, {years} years: identical with and without the observer and wrappers (state "
                     f"and random numbers): {'yes' if same else 'NO'}; wrapper-vs-event mismatches: {mism or 'none'}; "
                     f"talks {info.get('_talks')}, water places accepted {info.get('_w_acc')}, talks sharing water "
                     f"{info.get('_shared')}, habit copies {info.get('_imit')}, thirst targets told "
                     f"{info.get('_told_target')}")
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
    obs = IC1Obs(w)
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
