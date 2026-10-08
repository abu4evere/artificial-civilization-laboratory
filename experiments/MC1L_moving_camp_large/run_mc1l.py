"""MC1-L — MC1 re-tested at 256 new seeds (preregistration.md, frozen as `MC1L-frozen`). Uses MC1's code copy and runner
unchanged; only the seeds and output folder differ.

  python experiments/MC1L_moving_camp_large/run_mc1l.py checks   # fingerprint equals MC1's; zero check on two new seeds
  python experiments/MC1L_moving_camp_large/run_mc1l.py run      # c, m, s on seeds 2001-2256
"""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "MC1_moving_camp"))
import run_mc1 as M  # noqa: E402

OUT = HERE / "output"
SEEDS = tuple(range(2001, 2257))
MC1_HASH = json.loads((EXP / "MC1_moving_camp" / "output" / "m_seed_501.json").read_text(encoding="utf-8"))["code_hash"]


def checks():
    M.setup("mc1")
    fp = M.fingerprint()
    lines = [f"code_mc1 fingerprint equals MC1's recorded one: {'yes' if fp == MC1_HASH else 'NO'}"]
    ok = fp == MC1_HASH
    me = [sys.executable, str((EXP / "MC1_moving_camp" / "run_mc1.py").resolve())]
    for seed in (2001, 2002):
        a = subprocess.run(me + ["hashrun", "e13r", str(seed), "{}", "0"], capture_output=True, text=True).stdout.split()[-1]
        b = subprocess.run(me + ["hashrun", "mc1", str(seed), "{}", "1"], capture_output=True, text=True).stdout.split()[-1]
        t = a == b
        ok &= t
        lines.append(f"settings off, ledger on, seed {seed}, 20 years: copy reproduces the control world: {'yes' if t else 'NO'}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "checks.txt").write_text("\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n", encoding="utf-8")
    print("\n".join(lines), f"\nAll: {'PASS' if ok else 'FAIL'}", flush=True)
    return ok


def run_one(arm, seed, years=M.YEARS, out=None):
    """As MC1's run_one, without its check against F1's saved file (the new seeds have none)."""
    M.setup("mc1")
    import run_c1
    from run_f1 import Probe as F1Probe
    from run_hf4 import Ledger
    f0 = M.fingerprint()
    w = M.make_world(seed, **M.ARMS[arm])
    f1p, c1p, lg = F1Probe(), run_c1.Probe(), Ledger()
    w.ledger = lg.buf
    w.observers += [lg, f1p, c1p]
    for week in range(years * M.WPY):
        if week == M.C1_YEARS * M.WPY and c1p in w.observers:
            w.observers.remove(c1p)
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "years": years, "code_hash": f0, "code_hash_after": M.fingerprint(),
           "final_tick": w.tick, "world_hash": M.world_hash(w), "c1": c1p.results(), "ledger": lg.results(),
           **f1p.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: alive {len(w.living())}, pops {f1p.pops}", flush=True)


def run_all():
    v = OUT / "checks.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: checks have not passed")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [(a, s) for a in ("c", "m", "s") for s in SEEDS if not (OUT / f"{a}_seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["one", j[0], str(j[1])]), todo))
    bad = [(a, s) for a in ("c", "m", "s") for s in SEEDS
           if json.loads((OUT / f"{a}_seed_{s}.json").read_text(encoding="utf-8"))["code_hash"] != MC1_HASH]
    print("ALL DONE; code fingerprint unchanged" if not bad else f"HARD STOP: fingerprint changed in {bad[:5]}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "checks":
        sys.exit(0 if checks() else 1)
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]))
    elif cmd == "run":
        run_all()
