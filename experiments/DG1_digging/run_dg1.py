"""DG1 — digging (questions.md, frozen as `DG1-frozen`). `code_dg1` = `code_v4` + `digging` (D), default 0, and
`pit_keep`, + read-only logging (`world.dg1log`, not saved; read by nothing in the world). The full difference is
`v4_to_dg1.diff`.

  python experiments/DG1_digging/run_dg1.py zero    # hard stops: off = code_v4; D acts; read-only; reload
  python experiments/DG1_digging/run_dg1.py one <arm> <seed> <years> <out>    # one world (cloud-run)
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"dg1": HERE / "code_dg1", "v4": EXP / "NV4_nature_v4" / "code_v4"}
OUT = HERE / "output"
WPY, YEARS = 52, 120
SEEDS = tuple(range(13001, 13513))       # 512 new seeds, used by no study
SMOKE_SEEDS = (9979, 9978)
V3 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1}            # nature v4 (the name V3 is kept from the template)
ARMS = {"c": {}, "d": {"digging": 1}, "dw": {"digging": 1, "pit_keep": 0.75}}


def setup(code="dg1"):
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
    return code_hash(CODES["dg1"] / "acl")


class Weeks:
    """Read-only: living person-weeks."""

    def __init__(self):
        self.n = 0

    def __call__(self, world, events):
        self.n += len(world.living())


def observers(w):
    from run_f1 import Probe
    w.dg1log = []
    return Probe(), Weeks()


def summarise(w, wk):
    """Digs and food set down in pits, from the log; pits standing at the end."""
    log = w.dg1log
    digs = [r for r in log if r[0] == "dig"]
    pf = [r for r in log if r[0] == "pitfood"]
    return {"person_years": wk.n / WPY, "digs": len(digs), "diggers": len({r[2] for r in digs}),
            "dig_tiles": len({(r[3], r[4]) for r in digs}), "pit_food_puts": len(pf),
            "pit_food": sum(r[5] for r in pf), "pit_food_people": len({r[2] for r in pf}),
            "pits_end": len(w.pits), "deep_pits_end": sum(1 for v in w.pits.values() if v[0] >= 0.5),
            "digs_by_decade": {str(k): v for k, v in Counter(min(11, r[1] // 520) for r in digs).items()}}


def hashrun(code, seed, years, kw, observe):
    setup(code)
    w = make_world(seed, kw)
    if observe:
        w.observers += list(observers(w))
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def reload_check(seed):
    setup("dg1")
    from acl.world import World
    a = make_world(seed, ARMS["d"])
    a.dg1log = []
    for _ in range(10 * WPY):
        a.step()
    a.pits.setdefault("0,0", [0.7, a.tick])        # make sure a pit is held across the save (a test of saving only)
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    b.dg1log = []
    for w in (a, b):
        for _ in range(5 * WPY):
            w.step()
    return world_hash(a) == world_hash(b)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for seed, years in ((11, 5), (501, 5), (501, 20), (601, 20)):
        t = call("dg1", seed, years, "{}", 0) == call("v4", seed, years, "{}", 0)
        ok &= t
        lines.append(f"seed {seed}, {years} years: digging 0 = code_v4: {'yes' if t else 'NO'}")
    t = call("dg1", 501, 20, json.dumps(ARMS["d"]), 0) != call("dg1", 501, 20, "{}", 0)
    ok &= t
    lines.append(f"arm d, seed 501, 20 years: the setting changes the world (it acts): {'yes' if t else 'NO'}")
    for arm in ("c", "d"):
        t = call("dg1", 501, 20, json.dumps(ARMS[arm]), 1) == call("dg1", 501, 20, json.dumps(ARMS[arm]), 0)
        ok &= t
        lines.append(f"arm {arm}, seed 501, 20 years: identical with and without observers and logging: "
                     f"{'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm d, seed 501: saved at year 10 (a pit held) and reloaded, continues exactly to year 15: "
                 f"{'yes' if t else 'NO'}")
    setup("dg1")
    lines.append(f"code_dg1 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup("dg1")
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    probe, wk = observers(w)
    w.observers += [probe, wk]
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v4", "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "world_hash": world_hash(w), "pops": probe.pops, "deaths": probe.results().get("deaths"), **summarise(w, wk)}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), json.loads(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
