"""LM1 — memory or parts? (proposal.md, frozen as `LM1-frozen`). `code_lm1` = `code_v2` + `memory_ties_by_age` (M1) and
`parts_first` (L1), both default 0, plus read-only logging to `world.lm1log` (not saved; read by nothing in the world).

  python experiments/LM1_memory_and_parts/run_lm1.py zero    # hard stops: off = code_v2; each acts; read-only; reload; M1 random state
  python experiments/LM1_memory_and_parts/run_lm1.py smoke   # throwaway seeds 9951-9952, 10 years, every arm (code check only)
  python experiments/LM1_memory_and_parts/run_lm1.py run     # c, m, l, ml on seeds 7001-7256, 120 years (skips saved worlds)
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
CODES = {"lm1": HERE / "code_lm1", "v2": EXP / "NV2_nature_v2" / "code_v2"}
OUT = HERE / "output"
WPY, YEARS = 52, 120
SEEDS = tuple(range(7001, 7257))
SMOKE_SEEDS = (9951, 9952)
V2 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1}
ARMS = {"c": {}, "m": {"memory_ties_by_age": 1}, "l": {"parts_first": 1},
        "ml": {"memory_ties_by_age": 1, "parts_first": 1}}


def setup(code="lm1"):
    sys.path.insert(0, str(CODES[code]))
    for d in ("E7_passive", "F1_baseline_fragility", "CA1_chain_audit"):
        sys.path.insert(1, str(EXP / d))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **V2, **kw))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["lm1"] / "acl")


class Makes:
    """Read-only: who made which kind of thing (for 'makes it' among learners)."""

    def __init__(self):
        self.by = {}

    def __call__(self, world, events):
        for e in events:
            if e["k"] == "make" and e.get("a") and e.get("thing"):
                self.by.setdefault(e["thing"], set()).add(e["a"])


def observers(w):
    from run_ca1 import Chain
    from run_f1 import Probe
    return Probe(), Chain(), Makes()


def summarise(w, ch, mk, log):
    kinds = ch.results(w)
    first = {s: k["first_by"] for s, k in ch.kinds.items()}
    learners = {s: set(k["learners"]) for s, k in ch.kinds.items()}
    ks = {k["sig"]: k for k in kinds}
    useful = [k for k in kinds if k["max_factor"] is not None and k["max_factor"] >= 1.05]
    passed = [k for k in useful if k["transmitted"]]
    made_by_learner = sum(1 for k in useful if (mk.by.get(k["sig"], set()) & learners[k["sig"]]))
    improved, improved_passed = 0, 0
    for y in kinds:
        for x in y["parts"]:
            xk = ks.get(x)
            if (xk and xk["max_factor"] is not None and xk["max_factor"] >= 1.05 and y["max_factor"] is not None
                    and y["max_factor"] > xk["max_factor"] and first[y["sig"]] in learners.get(x, ())):
                improved += 1
                improved_passed += bool(y["transmitted"] and y["testable"] and y["retained"])
    held_obj = sum(1 for k in useful if any(it.get("sig") == k["sig"] for q in w.people.values() if q.id != first[k["sig"]]
                                            for it in getattr(q, "items", [])))
    ties = [r for r in log if r[0] == "tie"]
    parts = [r for r in log if r[0] == "part"]
    return {"useful": len(useful), "passed": len(passed),
            "link3": len(passed) / len(useful) if useful else None,
            "created_kinds": len(kinds), "made_by_learner": made_by_learner, "improved_by_learner": improved,
            "improved_passed": improved_passed, "held_by_other_at_end": held_obj,
            "ties": len(ties), "tie_composite_share": (sum(sum(r[1]) / len(r[1]) for r in ties) / len(ties)) if ties else None,
            "tie_drop_composite": (sum(r[2] for r in ties) / len(ties)) if ties else None,
            "tie_drop_oldest": (sum(r[3] for r in ties) / len(ties)) if ties else None,
            "part_lessons": len(parts), "part_taken": sum(1 for r in parts if r[1])}


def run_world(arm, seed, years, observe=True, logit=True):
    setup()
    w = make_world(seed, ARMS[arm])
    if logit:
        w.lm1log = []
    obs = observers(w) if observe else None
    if observe:
        w.observers += list(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    return w, obs


def hashrun(code, arm, seed, years, observe):
    setup(code)
    w = make_world(seed, ARMS[arm] if code == "lm1" else {})
    if observe:
        w.lm1log = []
        from run_ca1 import Chain
        from run_f1 import Probe
        w.observers += [Probe(), Chain(), Makes()]
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def reload_check(seed):
    setup()
    from acl.world import World
    a = make_world(seed, ARMS["ml"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for w in (a, b):
        for _ in range(5 * WPY):
            w.step()
    return world_hash(a) == world_hash(b)


def m1_random_check(seed):
    """M1 draws no random numbers: the random state just before and after every tie-breaking drop is the same."""
    setup()
    from acl import knowhow
    w = make_world(seed, ARMS["m"])
    orig = knowhow.remember_recipe
    bad = Counter()

    def wrapped(world, p, sig, recipe, how, source=None, props=None, meant=None):
        before = world.rng.getstate()
        full = len(p.recipes) >= knowhow.MAX_RECIPES and sig not in p.recipes
        orig(world, p, sig, recipe, how, source, props, meant)
        if full:
            bad["drops"] += 1
            bad["changed"] += world.rng.getstate() != before
    knowhow.remember_recipe = wrapped
    import acl.actions, acl.information, acl.biology, acl.marks  # noqa: E401
    for mod in (acl.actions, acl.information, acl.biology, acl.marks):
        if hasattr(mod, "remember_recipe"):
            mod.remember_recipe = wrapped
    for _ in range(20 * WPY):
        w.step()
    return bad["drops"] > 0 and bad["changed"] == 0, dict(bad)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for seed, years in ((11, 5), (501, 5), (501, 20), (601, 20)):
        t = call("lm1", "c", seed, years, 0) == call("v2", "c", seed, years, 0)
        ok &= t
        lines.append(f"seed {seed}, {years} years: both settings 0 = code_v2: {'yes' if t else 'NO'}")
    base = call("lm1", "c", 501, 20, 0)
    for arm in ("m", "l", "ml"):
        t = call("lm1", arm, 501, 20, 0) != base
        ok &= t
        lines.append(f"arm {arm}, seed 501, 20 years: the setting changes the world (it acts): {'yes' if t else 'NO'}")
    for arm in ("c", "ml"):
        t = call("lm1", arm, 501, 20, 1) == call("lm1", arm, 501, 20, 0)
        ok &= t
        lines.append(f"arm {arm}, seed 501, 20 years: identical with and without observers and logging: {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm ml, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["m1rand", "501"], capture_output=True, text=True)
    t = r.stdout.split()[:1] == ["True"]
    ok &= t
    lines.append(f"arm m, seed 501, 20 years: M1 leaves the random state unchanged at every full-memory drop: "
                 f"{'yes' if t else 'NO'} ({r.stdout.strip()})")
    setup()
    lines.append(f"code_lm1 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years, out):
    setup()
    f0 = fingerprint()
    w, (probe, ch, mk) = run_world(arm, seed, years)
    res = {"arm": arm, "seed": seed, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "world_hash": world_hash(w), "pops": probe.pops, "deaths": probe.results().get("deaths"),
           **summarise(w, ch, mk, w.lm1log)}
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}", flush=True)


def batch(seeds=SEEDS, years=YEARS, out=OUT):
    q = (HERE / "proposal.md").read_text(encoding="utf-8")
    if "SIGNED OFF" not in q.splitlines()[0]:
        sys.exit("ABORT: LM1 is not signed off")
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
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "m1rand":
        ok, info = m1_random_check(int(sys.argv[2]))
        print(ok, info)
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "run":
        batch()
    elif cmd == "smoke":
        batch(SMOKE_SEEDS, years=10, out=HERE / "output_smoke")
