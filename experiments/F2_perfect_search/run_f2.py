"""F2 — perfect partner finding (preregistration.md, frozen as `F2-frozen`). A diagnostic copy of the control code with
oracle pairing switched on; F1's observer records the same measures; F1's replays are the paired controls.

  python experiments/F2_perfect_search/run_f2.py zero      # switch off reproduces the control world; switch on pairs
  python experiments/F2_perfect_search/run_f2.py run       # the 64 seeds
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
CODES = {"f2": HERE / "code_f2", "e13r": EXP / "E13R_replication" / "code_e13r"}
OUT = HERE / "output"
WPY, YEARS = 52, 120
SEEDS = tuple(range(501, 517)) + tuple(range(601, 617)) + tuple(range(811, 819)) + tuple(range(1101, 1125))


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    sys.path.insert(1, str(EXP / "E7_passive"))
    sys.path.insert(2, str(EXP / "F1_baseline_fragility"))
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
    pairs = 0
    for _ in range(years * WPY):
        pairs += sum(1 for e in w.step() if e["k"] == "pair" and e.get("oracle"))
    return {"hash": world_hash(w), "oracle_pairs": pairs}


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(code, seed, kw):
        out = subprocess.run(me + ["hashrun", code, str(seed), json.dumps(kw)], capture_output=True, text=True).stdout
        return json.loads(out.strip().splitlines()[-1])
    lines, ok = [], True
    for seed in (601, 811):
        a, b = call("e13r", seed, {}), call("f2", seed, {})
        t = a["hash"] == b["hash"] and b["oracle_pairs"] == 0
        ok &= t
        lines.append(f"switch off, seed {seed}, 20 years: copy reproduces the control world: {'yes' if t else 'NO'}")
    c = call("f2", 601, {"oracle_pairing": 1})
    t = c["oracle_pairs"] > 0
    ok &= t
    lines.append(f"switch on, seed 601, 20 years: oracle pairings made: {c['oracle_pairs']} ({'yes' if t else 'NO'})")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "zero.txt").write_text("\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n", encoding="utf-8")
    print("\n".join(lines), f"\nAll: {'PASS' if ok else 'FAIL'}", flush=True)
    return ok


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["f2"] / "acl")


def run_one(seed, years=YEARS, out=None):
    setup("f2")
    from run_f1 import Probe
    f0 = fingerprint()
    w = make_world(seed, oracle_pairing=1)
    probe = Probe()
    w.observers.append(probe)
    oracle = 0
    for _ in range(years * WPY):
        oracle += sum(1 for e in w.step() if e["k"] == "pair" and e.get("oracle"))
        if not w.living():
            break
    res = {"seed": seed, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "world_hash": world_hash(w), "oracle_pairs": oracle, **probe.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: alive {len(w.living())}, pops {probe.pops}, oracle pairings {oracle}", flush=True)


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
