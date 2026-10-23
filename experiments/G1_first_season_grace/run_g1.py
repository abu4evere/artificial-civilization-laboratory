"""G1 — a first season of grace (questions.md, frozen as `G1-frozen`). `code_g1` = `code_v3` + `first_season_grace`
(G), default 0, plus read-only logging to `world.g1log` (not saved; read by nothing in the world). The full
difference is `v3_to_g1.diff`.

  python experiments/G1_first_season_grace/run_g1.py zero    # hard stops: off = code_v3; G acts; read-only; reload
  python experiments/G1_first_season_grace/run_g1.py smoke   # throwaway seeds 9991-9992, 8 years, both arms (code check only)
  python experiments/G1_first_season_grace/run_g1.py one <arm> <seed> <years> <out>    # one world (cloud-run)
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"g1": HERE / "code_g1", "v3": EXP / "NV3_nature_v3" / "code_v3"}
OUT = HERE / "output"
WPY, YEARS = 52, 120
SEEDS = tuple(range(9501, 9757))
SMOKE_SEEDS = (9991, 9992)
V3 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1}
ARMS = {"c": {}, "g": {"first_season_grace": 1}}
HOLD_WEEKS = 13                                    # manipulation check: still held by the inventor 13 weeks later


def setup(code="g1"):
    sys.path.insert(0, str(CODES[code]))
    for d in ("E7_passive", "F1_baseline_fragility", "CA1_chain_audit", "LM1_memory_and_parts"):
        sys.path.insert(1, str(EXP / d))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **V3, **kw))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["g1"] / "acl")


class Held:
    """Read-only, after each week: for every new kind of thing, whether its inventor still holds the recipe 13 weeks
    after inventing it, how many weeks they held it, whether they ever valued it above 0.15 while holding it, and the
    inventor's age when they invented it. Also recipes held per living person, summed over weeks."""

    def __init__(self):
        self.k = {}               # sig -> [first_tick, inventor, age_years, held_13 (None until known), held_weeks, holding]
        self.recipe_weeks = 0
        self.person_weeks = 0
        self.valued = set()

    def __call__(self, world, events):
        for sig, rec in world.knowledge.items():
            if sig not in self.k:
                p = world.people.get(rec["first_by"])
                age = p.years(rec["first_tick"]) if p is not None else None
                self.k[sig] = [rec["first_tick"], rec["first_by"], age, None, 0, True]
        for sig, r in self.k.items():
            if not r[5]:
                continue
            p = world.people.get(r[1])
            has = p is not None and p.alive and sig in p.recipes
            if has:
                r[4] += 1
                if p.itemval.get(sig, 0.0) > 0.15:
                    self.valued.add(sig)                        # pathway: ever valued above 0.15 by the inventor
                if world.tick - r[0] >= HOLD_WEEKS:
                    r[3] = True
            else:
                r[5] = False
                if p is not None and p.alive:
                    r[3] = world.tick - r[0] >= HOLD_WEEKS      # forgot before 13 weeks: False
                # an inventor who died before 13 weeks is left out (held_13 stays None)
        for p in world.living():
            self.recipe_weeks += len(p.recipes)
            self.person_weeks += 1

    def results(self):
        return {sig: {"first_tick": r[0], "age": r[2], "held_13": r[3], "held_weeks": r[4]} for sig, r in self.k.items()}


def observers(w):
    from run_ca1 import Chain
    from run_f1 import Probe
    from run_lm1 import Makes
    w.lm1log = []
    w.g1log = []
    return Probe(), Chain(), Makes(), Held()


def depth(sig, ks, memo, seen=()):
    """Longest chain of made parts under a kind (a kind with no made parts is 1)."""
    if sig in memo:
        return memo[sig]
    k = ks.get(sig)
    parts = [x for x in (k["parts"] if k else ()) if x in ks and x not in seen and x != sig]
    d = 1 + max((depth(x, ks, memo, seen + (sig,)) for x in parts), default=0)
    memo[sig] = d
    return d


def summarise_g1(w, ch, mk, held):
    from run_lm1 import summarise
    base = summarise(w, ch, mk, w.lm1log)
    kinds = ch.results(w)
    ks = {k["sig"]: k for k in kinds}
    hr = held.results()
    useful = [k for k in kinds if k["max_factor"] is not None and k["max_factor"] >= 1.05]
    h13 = [hr[k["sig"]]["held_13"] for k in useful if k["sig"] in hr and hr[k["sig"]]["held_13"] in (True, False)]
    child = [k for k in useful if k["sig"] in hr and hr[k["sig"]]["age"] is not None and hr[k["sig"]]["age"] < 16]
    memo = {}
    log = w.g1log
    usig = {k["sig"] for k in useful}
    offered = {r[3] for r in log if r[0] == "offer"}
    drops = [r for r in log if r[0] == "drop"]
    path = {"held13": 0, "used_again": 0, "valued": 0, "offered": 0, "learned": 0}
    for k in useful:
        s = k["sig"]
        fb = ch.kinds[s]["first_by"]
        path["held13"] += bool(hr.get(s, {}).get("held_13"))
        path["used_again"] += fb in mk.by.get(s, ())
        path["valued"] += s in held.valued
        path["offered"] += s in offered
        path["learned"] += bool(k["transmitted"])
    dk = Counter(r[5] for r in drops)
    disp = [r for r in drops if r[5] == "displaced"]
    return {**base, "path": path, "path_n": len(useful),
            "drops": dict(dk), "drops_teachable": sum(1 for r in drops if r[4] > 0.15),
            "displaced_teachable": sum(1 for r in disp if r[4] > 0.15),
            "displaced_useful": sum(1 for r in disp if r[3] in usig),
            "person_years": held.person_weeks / WPY,
            "useful_held13_n": len(h13), "useful_held13": sum(h13),
            "useful_held13_share": sum(h13) / len(h13) if h13 else None,
            "useful_held_weeks_mean": (sum(hr[k["sig"]]["held_weeks"] for k in useful if k["sig"] in hr) / len(useful))
            if useful else None,
            "recipes_per_person": held.recipe_weeks / held.person_weeks if held.person_weeks else None,
            "longest_chain": max((depth(k["sig"], ks, memo) for k in useful), default=0),
            "child_useful": len(child), "child_useful_passed": sum(1 for k in child if k["transmitted"])}


def hashrun(code, seed, years, kw, observe):
    setup(code)
    w = make_world(seed, kw)
    if observe:
        w.observers += list(observers(w))
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def reload_check(seed):
    setup("g1")
    from acl.world import World
    a = make_world(seed, ARMS["g"])
    for _ in range(10 * WPY):
        a.step()
    held = sum(len(p.recipe_got) for p in a.living())
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for w in (a, b):
        for _ in range(5 * WPY):
            w.step()
    return held > 0 and world_hash(a) == world_hash(b)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for seed, years in ((11, 5), (501, 5), (501, 20), (601, 20)):
        t = call("g1", seed, years, "{}", 0) == call("v3", seed, years, "{}", 0)
        ok &= t
        lines.append(f"seed {seed}, {years} years: first_season_grace 0 = code_v3: {'yes' if t else 'NO'}")
    t = call("g1", 501, 20, json.dumps(ARMS["g"]), 0) != call("g1", 501, 20, "{}", 0)
    ok &= t
    lines.append(f"arm g, seed 501, 20 years: the setting changes the world (it acts): {'yes' if t else 'NO'}")
    for arm in ("c", "g"):
        t = call("g1", 501, 20, json.dumps(ARMS[arm]), 1) == call("g1", 501, 20, json.dumps(ARMS[arm]), 0)
        ok &= t
        lines.append(f"arm {arm}, seed 501, 20 years: identical with and without observers: {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm g, seed 501: saved at year 10 (with first-held weeks) and reloaded, continues exactly to "
                 f"year 15: {'yes' if t else 'NO'}")
    setup("g1")
    lines.append(f"code_g1 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup("g1")
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    probe, ch, mk, held = observers(w)
    w.observers += [probe, ch, mk, held]
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v3", "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "world_hash": world_hash(w), "pops": probe.pops,
           "deaths": probe.results().get("deaths"), **summarise_g1(w, ch, mk, held)}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}", flush=True)


def batch(seeds=SEEDS, years=YEARS, out=OUT):
    q = (HERE / "questions.md").read_text(encoding="utf-8")
    if "SIGNED OFF" not in q.splitlines()[0]:
        sys.exit("ABORT: G1 is not signed off")
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: the zero checks have not passed (run 'zero')")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [(a, s) for s in seeds for a in ARMS if not (out / f"{a}_seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["one", j[0], str(j[1]), str(years), str(out)]), todo))
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), json.loads(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":
        batch(SMOKE_SEEDS, 8, HERE / "output_smoke")
    elif cmd == "run":
        batch()
