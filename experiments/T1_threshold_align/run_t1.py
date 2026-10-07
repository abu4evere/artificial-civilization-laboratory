"""T1 — align the two thresholds (preregistration.md, frozen as `T1-frozen`). A copy of the control code with one setting
(`partner_pull_radius`); F1's observer for the whole run and C1's observer for the first 40 years (both read-only).

  python experiments/T1_threshold_align/run_t1.py zero   # setting off reproduces the control world; on, it differs
  python experiments/T1_threshold_align/run_t1.py run    # the 64 seeds
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
CODES = {"t1": HERE / "code_t1", "e13r": EXP / "E13R_replication" / "code_e13r"}
OUT = HERE / "output"
WPY, YEARS, C1_YEARS = 52, 120, 40
SEEDS = tuple(range(501, 517)) + tuple(range(601, 617)) + tuple(range(811, 819)) + tuple(range(1101, 1125))
ON = {"partner_pull_radius": 2}


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    for d in ("E7_passive", "F1_baseline_fragility", "C1_couples_apart"):
        sys.path.insert(1, str(EXP / d))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, **kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **kw))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def hash_run(code, seed, years, kw):
    setup(code)
    w = make_world(seed, **kw)
    for _ in range(years * WPY):
        w.step()
    return {"hash": world_hash(w)}


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(code, seed, kw):
        out = subprocess.run(me + ["hashrun", code, str(seed), json.dumps(kw)], capture_output=True, text=True).stdout
        return json.loads(out.strip().splitlines()[-1])["hash"]
    lines, ok = [], True
    for seed in (601, 811):
        t = call("e13r", seed, {}) == call("t1", seed, {})
        ok &= t
        lines.append(f"setting off, seed {seed}, 20 years: copy reproduces the control world: {'yes' if t else 'NO'}")
    t = call("t1", 601, ON) != call("e13r", 601, {})
    ok &= t
    lines.append(f"setting on, seed 601, 20 years: the world differs from the control: {'yes' if t else 'NO'}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "zero.txt").write_text("\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n", encoding="utf-8")
    print("\n".join(lines), f"\nAll: {'PASS' if ok else 'FAIL'}", flush=True)
    return ok


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["t1"] / "acl")


def run_one(seed, years=YEARS, out=None):
    setup("t1")
    import run_c1
    from run_f1 import Probe as F1Probe
    f0 = fingerprint()
    w = make_world(seed, **ON)
    f1p, c1p = F1Probe(), run_c1.Probe()
    w.observers += [f1p, c1p]
    for week in range(years * WPY):
        if week == C1_YEARS * WPY:
            w.observers.remove(c1p)            # C1's window is the first 40 years; observers never touch the world
        w.step()
        if not w.living():
            break
    res = {"seed": seed, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "world_hash": world_hash(w), **f1p.results(), "c1": c1p.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: alive {len(w.living())}, pops {f1p.pops}", flush=True)


def run_all():
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: zero checks have not passed")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [s for s in SEEDS if not (OUT / f"seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda s: subprocess.call(me + ["one", str(s)]), todo))
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "hashrun":
        print(json.dumps(hash_run(sys.argv[2], int(sys.argv[3]), 20, json.loads(sys.argv[4]))))
    elif cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "one":
        run_one(int(sys.argv[2]))
    elif cmd == "run":
        run_all()
