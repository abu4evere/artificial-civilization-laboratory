"""SA1 — sensitivity audit (questions.md, frozen as `SA1-frozen`). Control code (`code_e13r`, anticipation_weight 1.0,
as F1); one setting changed per arm; F1's 64 seeds; 120 years. Observers: F1's probe and E8.2's probe (loaded unchanged).

  python experiments/SA1_sensitivity/run_sa1.py zero    # hard stop: the observers leave the world unchanged
  python experiments/SA1_sensitivity/run_sa1.py run     # all 14 arms (C first; C must reproduce F1's saved pops)
"""
from __future__ import annotations

import hashlib
import json
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODE = EXP / "E13R_replication" / "code_e13r"
CODE_P2 = EXP / "P2_outward_search" / "code_p2"   # the sham only: the control code has no sham_draw (note in questions.md)
OUT = HERE / "output"
WPY, YEARS = 52, 120
F1_SEEDS = tuple(range(501, 517)) + tuple(range(601, 617)) + tuple(range(811, 819)) + tuple(range(1101, 1125))
ARMS = {
    "c": {},
    "conception_lo": {"conception_chance": 0.02}, "conception_hi": {"conception_chance": 0.08},
    "perception_lo": {"perception": 2}, "perception_hi": {"perception": 8},
    "reach_lo": {"reach": 2}, "reach_hi": {"reach": 6},
    "camp_lo": {"camp_radius": 1}, "camp_hi": {"camp_radius": 4},
    "mortality_lo": {"mortality_base": 0.75e-5}, "mortality_hi": {"mortality_base": 3.0e-5},
    "forage_lo": {"forage_base": 6.0}, "forage_hi": {"forage_base": 24.0},
    "s": {"sham_draw": 1},
}


def setup(code=None):
    code = code or CODE
    sys.path.insert(0, str(code))
    for d in ("E7_passive", "F1_baseline_fragility"):
        sys.path.insert(1, str(EXP / d))
    import acl
    assert Path(acl.__file__).resolve().parent == (code / "acl").resolve()


def e82_probe():
    """E8.2's Probe, loaded unchanged from its file and run against the control code's acl.matter (importing that file
    would bind E7's code copy)."""
    from acl import matter
    src = (EXP / "E8_crucible" / "run_e82.py").read_text(encoding="utf-8")
    body = src[src.index("def recipe_material_units"):src.index("\ndef run(seed)")]
    ns = {"matter": matter, "Counter": Counter, "defaultdict": defaultdict, "statistics": statistics, "WPY": WPY,
          "__name__": "e82_probe"}
    exec(compile(body, "E8_crucible/run_e82.py (Probe, unchanged)", "exec"), ns)
    return ns["Probe"]()


def make_world(seed, **kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **kw))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def fingerprint(code=None):
    from run_e7 import code_hash
    return code_hash((code or CODE) / "acl")


def hash_run(seed, years, observe, code=None):
    setup(code)
    w = make_world(seed)
    if observe:
        from run_f1 import Probe as F1Probe
        w.observers += [F1Probe(), e82_probe()]
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]
    call = lambda seed, obs: subprocess.run(me + ["hashrun", str(seed), "1" if obs else "0"],  # noqa: E731
                                            capture_output=True, text=True).stdout.strip().splitlines()[-1]
    lines, ok = [], True
    for seed in (501, 601):
        t = call(seed, False) == call(seed, True)
        ok &= t
        lines.append(f"control code, seed {seed}, 20 years: identical with and without both observers: {'yes' if t else 'NO'}")
        t2 = call(seed, False) == subprocess.run(me + ["hashrun", str(seed), "0", "p2"], capture_output=True,
                                                 text=True).stdout.strip().splitlines()[-1]
        ok &= t2
        lines.append(f"code_p2 with every setting off, seed {seed}, 20 years: identical to the control code: {'yes' if t2 else 'NO'}")
    setup()
    lines.append(f"code_e13r fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "zero.txt").write_text("\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n", encoding="utf-8")
    print("\n".join(lines), f"\nAll: {'PASS' if ok else 'FAIL'}", flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    code = CODE_P2 if arm == "s" else CODE
    setup(code)
    from run_f1 import Probe as F1Probe
    f0 = fingerprint(code)
    w = make_world(seed, **ARMS[arm])
    f1p, e82 = F1Probe(), e82_probe()
    w.observers += [f1p, e82]
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "settings": ARMS[arm], "code": code.name, "code_hash": f0, "code_hash_after": fingerprint(code),
           "final_tick": w.tick, "world_hash": world_hash(w), "e82": e82.results(), **f1p.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: pops {f1p.pops}", flush=True)


def control_matches_f1():
    bad = []
    for s in F1_SEEDS:
        mine = json.loads((OUT / f"c_seed_{s}.json").read_text(encoding="utf-8"))["pops"]
        f1 = json.loads((EXP / "F1_baseline_fragility" / "output" / f"seed_{s}.json").read_text(encoding="utf-8"))["pops"]
        if mine != f1:
            bad.append(s)
    return bad


def run():
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: zero check has not passed")
    me = [sys.executable, str(Path(__file__).resolve())]
    pool_run = lambda jobs: list(ThreadPoolExecutor(4).map(lambda j: subprocess.call(me + ["one", j[0], str(j[1])]), jobs))  # noqa: E731
    pool_run([("c", s) for s in F1_SEEDS if not (OUT / f"c_seed_{s}.json").exists()])
    bad = control_matches_f1()
    (OUT / "control_check.txt").write_text(
        f"control re-run reproduces F1's saved populations on all 64 seeds: {'yes' if not bad else 'NO: ' + str(bad)}\n"
        f"All: {'PASS' if not bad else 'FAIL'}\n", encoding="utf-8")
    if bad:
        sys.exit(f"HARD STOP: the control re-run does not reproduce F1 on seeds {bad}")
    pool_run([(a, s) for a in ARMS if a != "c" for s in F1_SEEDS if not (OUT / f"{a}_seed_{s}.json").exists()])
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hash_run(int(sys.argv[2]), 20, sys.argv[3] == "1", CODE_P2 if sys.argv[4:5] == ["p2"] else None))
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]))
    elif cmd == "run":
        run()
    elif cmd == "smokeone":   # analysis smoke test only: 5 years, a separate folder
        run_one(sys.argv[2], int(sys.argv[3]), years=5, out=HERE / "output_smoke")
