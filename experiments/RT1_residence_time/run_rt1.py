"""RT1 — residence time (questions.md, frozen as `RT1-frozen`, Amendment 1 as `RT1-amend1`). `code_rt1` = `code_v2`
(nature v2) + `residence_weeks`, one commit (and Amendment 1's two lines). Observers, all read-only: F1's probe, MB1a's
lineage observer (both loaded unchanged) and RT1's own movement and hunting observer.

  python experiments/RT1_residence_time/run_rt1.py zero     # hard stops: off = code_v2; observers read-only; R4 acts; save/reload exact
  python experiments/RT1_residence_time/run_rt1.py run      # c, r4, sham on seeds 5001-5256, 120 years (skips saved worlds)
  python experiments/RT1_residence_time/run_rt1.py smoke    # throwaway: seeds 9701-9702, 12 years, every arm (code check only)
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"rt1": HERE / "code_rt1", "v2": EXP / "NV2_nature_v2" / "code_v2"}
OUT = HERE / "output"
WPY, YEARS = 52, 120
SEEDS = tuple(range(5001, 5257))
SMOKE_SEEDS = (9701, 9702)
V2 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1}
ARMS = {"c": {}, "r4": {"residence_weeks": 4}, "sham": {"sham_draw": 1}}


def setup(code="rt1"):
    sys.path.insert(0, str(CODES[code]))
    for d in ("E7_passive", "F1_baseline_fragility", "MB1_multi_band"):
        sys.path.insert(1, str(EXP / d))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **V2, **kw))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")              # the settings list itself is left out, as every zero check has done (Amendment 1 note)
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["rt1"] / "acl")


class Moves:
    """RT1's observer: reads the world after each week; draws no random numbers; writes nothing to the world."""

    def __init__(self):
        self.hist = {}                    # adult id -> tiles slept on, one per adult week
        self.t = {"adult_weeks": 0, "changed": 0, "pairs": 0, "month_sum": 0, "month_n": 0,
                  "hunt_part": 0, "hunt_success_part": 0}

    def __call__(self, world, events):
        from acl.util import distance
        c, t = world.cfg, self.t
        for e in events:
            if e["k"] == "hunt":
                n = len(e.get("party") or [])
                t["hunt_part"] += n
                if e.get("success"):
                    t["hunt_success_part"] += n
        for p in world.living():
            if p.age(world.tick) < 16 * WPY:
                continue
            t["adult_weeks"] += 1
            h = self.hist.setdefault(p.id, [])
            if h:
                t["pairs"] += 1
                t["changed"] += h[-1] != p.loc
            h.append(p.loc)
            if len(h) % 4 == 1 and len(h) > 4:          # adult weeks 0-3, 4-7, ...: start of one run to the start of the next
                t["month_sum"] += distance(h[-5], h[-1], c.width, c.height)
                t["month_n"] += 1
                del h[:-1]                               # keep only what the next comparison needs

    def results(self):
        t = self.t
        return {"moves": dict(t), "changed_share": t["changed"] / t["pairs"] if t["pairs"] else None,
                "month_mean": t["month_sum"] / t["month_n"] if t["month_n"] else None}


def observers(w):
    from run_f1 import Probe
    from run_mb1a import Lineages
    return Probe(), Lineages(w), Moves()


def hashrun(code, seed, years, kw, observe):
    setup(code)
    w = make_world(seed, kw)
    if observe:
        w.observers += list(observers(w))
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def reload_check(seed):
    """R4: a world saved at year 10 and reloaded continues exactly as the straight run (to year 15)."""
    setup("rt1")
    from acl.world import World
    a = make_world(seed, ARMS["r4"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for w in (a, b):
        for _ in range(5 * WPY):
            w.step()
    return world_hash(a) == world_hash(b) and bool(a.bases)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for seed, years in ((11, 5), (501, 5), (501, 20), (601, 20)):
        t = call("rt1", seed, years, json.dumps({}), 0) == call("v2", seed, years, json.dumps({}), 0)
        ok &= t
        lines.append(f"seed {seed}, {years} years: residence_weeks 0 = code_v2 (settings left out): {'yes' if t else 'NO'}")
    for arm in ("c", "r4"):
        t = call("rt1", 501, 20, json.dumps(ARMS[arm]), 1) == call("rt1", 501, 20, json.dumps(ARMS[arm]), 0)
        ok &= t
        lines.append(f"arm {arm}, seed 501, 20 years: identical with and without the three observers: {'yes' if t else 'NO'}")
    t = call("rt1", 501, 20, json.dumps(ARMS["r4"]), 0) != call("rt1", 501, 20, json.dumps({}), 0)
    ok &= t
    lines.append(f"seed 501, 20 years: residence_weeks 4 changes the world (it acts): {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"R4, seed 501: saved at year 10 and reloaded, continues exactly to year 15 (bases kept): {'yes' if t else 'NO'}")
    setup("rt1")
    lines.append(f"code_rt1 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup("rt1")
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    probe, lin, mv = observers(w)
    w.observers += [probe, lin, mv]
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "world_hash": world_hash(w), **probe.results(), "mb1a": lin.results(), **mv.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: alive {len(w.living())}, pops {probe.pops}", flush=True)


def batch(seeds=SEEDS, years=YEARS, out=OUT):
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
    elif cmd == "run":
        batch()
    elif cmd == "smoke":
        batch(SMOKE_SEEDS, years=12, out=HERE / "output_smoke")
