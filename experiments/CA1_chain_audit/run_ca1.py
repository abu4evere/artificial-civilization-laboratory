"""CA1 — the chain audit (questions.md, frozen as `CA1-frozen`). `code_v2` with nature v2's settings, unchanged; one
read-only observer that follows every kind of thing from invention to retransmission.

  python experiments/CA1_chain_audit/run_ca1.py zero     # hard stop: the observer leaves the world unchanged
  python experiments/CA1_chain_audit/run_ca1.py pilot    # throwaway seed 9921, 10 years: timing and the observer's working
  python experiments/CA1_chain_audit/run_ca1.py run      # discovery 6301-6316, holdout 6317-6332, long 6401-6404 (2 workers)
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODE = EXP / "NV2_nature_v2" / "code_v2"
OUT = HERE / "output"
WPY = 52
DISCOVERY = tuple(range(6301, 6317))
HOLDOUT = tuple(range(6317, 6333))
LONG = tuple(range(6401, 6405))
V2 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1}
USES = ("forage", "hunt", "wood", "stone", "fiber", "fight", "carry", "cold")


def setup():
    sys.path.insert(0, str(CODE))
    for d in ("E7_passive", "F1_baseline_fragility"):
        sys.path.insert(1, str(EXP / d))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


def make_world(seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **V2))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODE / "acl")


def max_factor(props):
    from acl.matter import factor
    if not props:
        return None
    return max(factor(props, u) for u in USES)


class Chain:
    """Read-only, after each week. Draws no random numbers and writes nothing to the world."""

    def __init__(self):
        self.kinds = {}           # sig -> record
        self.gen = {}             # (sig, person id) -> generations from the first knower
        self.make_props = {}      # sig -> properties of the first one made

    def __call__(self, world, events):
        from acl.matter import PROPS
        for e in events:
            if e["k"] == "make" and e.get("thing") not in self.make_props:
                self.make_props[e["thing"]] = {k: e[k] for k in PROPS if k in e}
        first_how = {}
        for e in events:
            if e["k"] == "learn" and "thing" in e:
                first_how.setdefault((e["thing"], e["a"]), e["how"])
        for sig, rec in world.knowledge.items():
            if sig not in self.kinds:
                fb = rec["first_by"]
                self.kinds[sig] = {"first_by": fb, "first_tick": rec["first_tick"],
                                   "how": first_how.get((sig, fb), "made"), "learners": [], "route": None,
                                   "dead_tick": None, "retained": False, "gens": 0, "copy_error": False}
                self.gen[(sig, fb)] = 0
        for e in events:
            if e["k"] != "learn" or "thing" not in e:
                continue
            sig, who = e["thing"], e["a"]
            k = self.kinds.get(sig)
            if k is None:
                continue
            if e.get("meant") and e["meant"] != sig and who == k["first_by"]:
                k["copy_error"] = True
            if who != k["first_by"] and who not in k["learners"]:
                k["learners"].append(who)
                if k["route"] is None:
                    k["route"] = e["how"]
            src = e.get("b")
            g = self.gen.get((sig, src), 0) + 1 if src is not None else 1
            if (sig, who) not in self.gen:
                self.gen[(sig, who)] = g
                k["gens"] = max(k["gens"], g)
        living = world.living()
        known = set()
        for q in living:
            known.update(q.recipes)
        for sig, k in self.kinds.items():
            if k["retained"]:
                continue
            fb = world.people.get(k["first_by"])
            if fb is not None and not fb.alive:
                if k["dead_tick"] is None:
                    k["dead_tick"] = world.tick
                if sig in known:
                    k["retained"] = True

    def results(self, world):
        out = []
        for sig, k in self.kinds.items():
            rec = world.knowledge[sig]
            props = rec.get("props") or self.make_props.get(sig)
            recipe = rec.get("recipe") or {}
            parts = list(recipe.get("parts", ())) + ([recipe["part"]] if recipe.get("verb") == "heat" else [])
            out.append({"sig": sig, "first_tick": k["first_tick"], "how": k["how"], "copy_error": k["copy_error"],
                        "max_factor": max_factor(props), "transmitted": bool(k["learners"]),
                        "n_learners": len(k["learners"]), "route": k["route"],
                        "testable": k["dead_tick"] is not None, "retained": k["retained"],
                        "parts": [x for x in parts if x in world.knowledge], "gens": k["gens"]})
        return out


def run_world(seed, years, observe=True):
    setup()
    w = make_world(seed)
    from run_f1 import Probe
    probe, ch = Probe(), Chain()
    if observe:
        w.observers += [probe, ch]
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    return w, probe, ch


def hashrun(seed, years, observe):
    w, _, _ = run_world(seed, years, observe)
    return world_hash(w)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for seed in (501, 601):
        t = call(seed, 20, 1) == call(seed, 20, 0)
        ok &= t
        lines.append(f"seed {seed}, 20 years: identical with and without the chain observer: {'yes' if t else 'NO'}")
    setup()
    lines.append(f"code_v2 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(seed, years, out):
    setup()
    f0 = fingerprint()
    w, probe, ch = run_world(seed, years)
    res = {"seed": seed, "years": years, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "world_hash": world_hash(w), "pops": probe.pops, "kinds": ch.results(w)}
    out.mkdir(parents=True, exist_ok=True)
    (out / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: done, tick {w.tick}", flush=True)


def pilot():
    t0 = time.time()
    w, probe, ch = run_world(9921, 10)
    ks = ch.results(w)
    print(f"pilot seed 9921, 10 years: {time.time() - t0:.0f} s; observer followed {len(ks)} kinds of thing; "
          f"fields present: {sorted(ks[0]) if ks else []}", flush=True)


def batch():
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: the zero check has not passed (run 'zero')")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [(s, 300) for s in LONG] + [(s, 120) for s in DISCOVERY + HOLDOUT]
    todo = [(s, y) for s, y in todo if not (OUT / f"seed_{s}.json").exists()]
    with ThreadPoolExecutor(2) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["one", str(j[0]), str(j[1]), str(OUT)]), todo))
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4] == "1"))
    elif cmd == "one":
        run_one(int(sys.argv[2]), int(sys.argv[3]), Path(sys.argv[4]))
    elif cmd == "pilot":
        pilot()
    elif cmd == "run":
        batch()
