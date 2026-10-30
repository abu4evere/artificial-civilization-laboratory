"""LS2 — where does knowledge go under nature v9? (questions.md, frozen as `LS2-frozen`). Read-only: LS1's observer,
ledger and wrappers (`../LS1_where_knowledge_goes/run_ls1.py`, unchanged) pointed at `code_v9` (live nature v9).
LP only, 40 new seeds, 1,000 years. The zero checks and `run_one` are LS1's, re-stated here so that every subprocess
runs this runner (and so `code_v9`), and the record says v9.

  python experiments/LS2_knowledge_v9/run_ls2.py zero
  python experiments/LS2_knowledge_v9/run_ls2.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "LS1_where_knowledge_goes"))
import run_ls1 as base  # noqa: E402

CODE = EXP / "NV9_nature_v9" / "code_v9"
OUT = HERE / "output"
WPY, YEARS = base.WPY, 1000
LP_SEEDS = tuple(range(20401, 20441))      # 40 new seeds, used by no study
D80_SEEDS = ()                             # LS1's secondary arm is dropped (questions.md)
SEEDS = LP_SEEDS
SMOKE_SEEDS = (9995, 9994)
ARMS = {"lp": {"founders": 80, "width": 80, "height": 80}, "d80": {"founders": 80}}
JOBS = [f"lp:{s}" for s in LP_SEEDS]
V9 = {**base.V7, "ground_items": 1, "curiosity_pull": 1}
BIN_EDGES, DECADE = base.BIN_EDGES, base.DECADE

base.CODE, base.OUT, base.YEARS = CODE, OUT, YEARS
base.LP_SEEDS, base.D80_SEEDS, base.SEEDS, base.SMOKE_SEEDS, base.JOBS = LP_SEEDS, D80_SEEDS, SEEDS, SMOKE_SEEDS, JOBS
base.V7 = V9                               # LS1 passes these settings to every world (explicit, = code_v9's defaults)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    from concurrent.futures import ThreadPoolExecutor
    specs = [(arm, seed, years, obs) for arm, seed, years in (("lp", 501, 20), ("lp", 601, 100)) for obs in (1, 0)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for arm, seed, years in (("lp", 501, 20), ("lp", 601, 100)):
        a, b = got[(arm, seed, years, 1)], got[(arm, seed, years, 0)]
        same = a.split(":")[:2] == b.split(":")[:2]
        mism = json.loads(a.split(":", 2)[2]) if a.count(":") >= 2 else {"?": 1}
        t = same and not any(mism.values())
        ok &= t
        lines.append(f"arm {arm}, seed {seed}, {years} years: identical with and without the observer (state and "
                     f"random numbers): {'yes' if same else 'NO'}; ledger, kind-count and holdings mismatches: "
                     f"{mism or 'none'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm lp, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    fp = call("fp")
    lines.append(f"code_v9 fingerprint: {fp}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup()
    f0 = base.fingerprint()
    w = base.make_world(seed, ARMS[arm])
    obs = base.LS1Obs(w)
    base.install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v9", "code_hash": f0, "code_hash_after": base.fingerprint(),
           "final_tick": w.tick, "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, mismatches {dict(obs.mismatch)}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(base.hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] == "1"))
    elif cmd == "reload":
        print(base.reload_check(int(sys.argv[2])))
    elif cmd == "fp":
        base.setup()
        print(base.fingerprint())
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
