"""NV2 — nature v2 against v1 (questions.md, frozen as `NV2-frozen`). `code_v2` = the control code (as `code_p2`, its
settings off) + four switches, one commit each. F1's probe, read-only.

  python experiments/NV2_nature_v2/run_nv2.py zero      # all off = control code; each change acts; knowledge_copy changes no behaviour
  python experiments/NV2_nature_v2/run_nv2.py run       # v1, v2, sham on seeds 4601-4856, 120 years
  python experiments/NV2_nature_v2/run_nv2.py smoke     # throwaway: seed 9701, 10 years, every arm (code check only)
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
CODES = {"v2": HERE / "code_v2", "e13r": EXP / "E13R_replication" / "code_e13r"}
OUT = HERE / "output"
WPY, YEARS = 52, 120
SEEDS = tuple(range(4601, 4857))
SMOKE_SEED = 9701
V2 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1}
ARMS = {"v1": {}, "v2": V2, "sham": {"sham_draw": 1}}
ALONE = {"last_seen": {"loved_location": "last_seen"}, "corner": {"corner_block": 1},
         "ashore": {"ashore_if_float_breaks": 1}, "knowledge": {"knowledge_copy": 1}}


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    for d in ("E7_passive", "F1_baseline_fragility"):
        sys.path.insert(1, str(EXP / d))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **kw))


def world_hash(w, drop=()):
    d = w.to_dict()
    d.pop("cfg")
    for k in drop:
        d.pop(k)
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["v2"] / "acl")


def hashrun(code, seed, years, kw, probe, weekly_no_knowledge=False):
    setup(code)
    w = make_world(seed, kw)
    if probe:
        from run_f1 import Probe
        w.observers.append(Probe())
    weekly = []
    for _ in range(years * WPY):
        w.step()
        if weekly_no_knowledge:
            weekly.append(world_hash(w, drop=("knowledge",)))
    return world_hash(w), hashlib.sha256("".join(weekly).encode()).hexdigest()


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(code, seed, kw, probe=0, weekly=0):
        out = subprocess.run(me + ["hashrun", code, str(seed), json.dumps(kw), str(probe), str(weekly)],
                             capture_output=True, text=True).stdout.strip().splitlines()[-1].split()
        return out
    lines, ok = [], True
    for seed in (501, 601):
        ctrl = call("e13r", seed, {})[0]
        off = call("v2", seed, {})[0]
        t = off == ctrl
        ok &= t
        lines.append(f"seed {seed}, 20 years: all four off = control code: {'yes' if t else 'NO'}")
        t = call("v2", seed, {}, probe=1)[0] == off
        ok &= t
        lines.append(f"  F1's probe leaves the world unchanged: {'yes' if t else 'NO'}")
        base_weekly = call("v2", seed, {}, weekly=1)[1]
        for name, kw in ALONE.items():
            h, wk = call("v2", seed, kw, weekly=1 if name == "knowledge" else 0)
            if name == "knowledge":
                t = wk == base_weekly
                lines.append(f"  knowledge_copy alone: every person and event identical to v1 every week (only the record "
                             f"may differ): {'yes' if t else 'NO'}; final state {'differs' if h != off else 'identical'}")
            else:
                t = h != off
                lines.append(f"  {name} alone: the world differs from v1 (the change acts): {'yes' if t else 'NO'}")
            ok &= t
    setup("v2")
    lines.append(f"code_v2 fingerprint: {fingerprint()}")
    lines.append("Reference fingerprints for v2: tests/reference_hashes.json (\"v2\"), test_nature_v2_replays.")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup("v2")
    from run_f1 import Probe
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    probe = Probe()
    w.observers.append(probe)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "world_hash": world_hash(w), **probe.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: alive {len(w.living())}, pops {probe.pops}", flush=True)


def batch():
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: the zero checks have not passed (run 'zero')")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [(a, s) for s in SEEDS for a in ARMS if not (OUT / f"{a}_seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda t: subprocess.call(me + ["one", t[0], str(t[1])]), todo))
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(*hashrun(sys.argv[2], int(sys.argv[3]), 20, json.loads(sys.argv[4]), sys.argv[5] == "1", sys.argv[6] == "1"))
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]))
    elif cmd == "smoke":
        for a in ARMS:
            run_one(a, SMOKE_SEED, years=10, out=HERE / "output_smoke")
    elif cmd == "run":
        batch()
