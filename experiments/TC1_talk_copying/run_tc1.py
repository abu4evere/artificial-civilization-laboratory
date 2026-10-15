"""TC1 — does copying whole habit tables in talk make everyone alike? (questions.md, frozen as `TC1-frozen`.)
`code_tc1` = `code_bl0` (BL0's hooks) + `talk_copy` and `sham_draw`; BL0's observer, unchanged except that imitation
credits T only on the values that moved.

  python experiments/TC1_talk_copying/run_tc1.py zero        # defaults = control world and code_bl0; parts add up in S and N
  python experiments/TC1_talk_copying/run_tc1.py discovery   # 501-516, 601-616; arms w, s, n, sham
  python experiments/TC1_talk_copying/run_tc1.py holdout     # 811-818, 1101-1124 (after the discovery reading)
  python experiments/TC1_talk_copying/run_tc1.py smoke       # throwaway: seed 9601, 10 years, every arm (code check only)
"""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "BL0_habit_use"))
import run_bl0 as R  # noqa: E402

R.CODES["tc1"] = HERE / "code_tc1"
OUT = HERE / "output"
BL0_OUT = EXP / "BL0_habit_use" / "output"
ARMS = {"w": {}, "s": {"talk_copy": "situation"}, "n": {"talk_copy": "none"}, "sham": {"sham_draw": 1}}
SMOKE_SEED = 9601


class TC1Obs(R.BL0):
    def blend(self, world, p, other, rate, row, idx=None):
        if idx is None:
            return super().blend(world, p, other, rate, row)
        m, o = self._m(p), self._m(other)
        m[:4, idx] *= 1.0 - rate
        m[row, idx] += rate * np.asarray(other.q)[idx]
        m[4:, idx] = (1.0 - rate) * m[4:, idx] + rate * o[4:, idx]
        self.changed[p.id][idx] = world.tick
        self.n["imitation"] += 1


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **kw))


def run(arm, seed, years, observe):
    R.setup("tc1")
    w = make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = TC1Obs(seed)
        w.bl0 = obs
        w.observers.append(obs)
    for _ in range(years * R.WPY):
        w.step()
        if not w.living():
            break
    return w, obs


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*a):
        return subprocess.run(me + ["hashrun", *map(str, a)], capture_output=True, text=True).stdout.strip().splitlines()[-1].split()

    def ctrl(code, seed):
        return subprocess.run([sys.executable, str(EXP / "BL0_habit_use" / "run_bl0.py"), "hashrun", code, str(seed), "0"],
                              capture_output=True, text=True).stdout.strip().splitlines()[-1].split()[0]
    lines, ok = [], True
    for seed in (501, 601):
        c, b = ctrl("e13r", seed), ctrl("bl0", seed)
        plain, logged = call("w", seed, 0), call("w", seed, 1)
        t = plain[0] == c == b and logged[0] == c
        ok &= t
        lines.append(f"seed {seed}, 20 years: code_tc1 defaults = control code = code_bl0 (without and with the log): "
                     f"{'yes' if t else 'NO'}")
        for arm in ("s", "n"):
            r = call(arm, seed, 1)
            good = r[0] != c and float(r[1]) <= 1e-9
            ok &= good
            lines.append(f"  arm {arm}: differs from W: {'yes' if r[0] != c else 'NO'}; parts add up (largest error {r[1]}): "
                         f"{'yes' if float(r[1]) <= 1e-9 else 'NO'}")
    R.setup("tc1")
    lines.append(f"code_tc1 fingerprint: {R.fingerprint('tc1')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=R.YEARS, out=None):
    R.setup("tc1")
    f0 = R.fingerprint("tc1")
    w, obs = run(arm, seed, years, True)
    res = {"arm": arm, "seed": seed, "code_hash": f0, "code_hash_after": R.fingerprint("tc1"), "final_tick": w.tick,
           "world_hash": R.world_hash(w), "temperature": w.cfg.choice_temperature, **obs.results()}
    if arm == "w" and out is None:
        ref = json.loads((BL0_OUT / f"seed_{seed}.json").read_text(encoding="utf-8"))
        saved = json.loads(json.dumps(res))      # compare as saved (numeric keys become text, as in BL0's file)
        keys = [k for k in ref if k not in ("seed", "code_hash", "code_hash_after")]
        res["reproduces_bl0"] = all(json.dumps(ref[k], sort_keys=True) == json.dumps(saved.get(k), sort_keys=True) for k in keys)
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    flag = "" if res.get("reproduces_bl0", True) else "  HARD STOP: W does not reproduce BL0"
    print(f"{arm} seed {seed}: ended week {w.tick}, pops {obs.pops}, split error {obs.max_err:.2g}{flag}", flush=True)


def batch(seeds):
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: the zero check has not passed (run 'zero')")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [(a, s) for s in seeds for a in ARMS if not (OUT / f"{a}_seed_{s}.json").exists()]
    stop = []

    def go(t):
        if stop:
            return
        subprocess.call(me + ["one", t[0], str(t[1])])
        f = OUT / f"{t[0]}_seed_{t[1]}.json"
        if not f.exists() or not json.loads(f.read_text(encoding="utf-8")).get("reproduces_bl0", True):
            stop.append(t)

    with ThreadPoolExecutor(4) as pool:
        list(pool.map(go, todo))
    print(f"HARD STOP at {stop[0]}" if stop else "ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        w, obs = run(sys.argv[2], int(sys.argv[3]), 20, sys.argv[4] == "1")
        print(R.world_hash(w) + " " + (f"{obs.max_err:.3g}" if obs else "-"))
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]))
    elif cmd == "smoke":
        for a in ARMS:
            run_one(a, SMOKE_SEED, years=10, out=HERE / "output_smoke")
    elif cmd == "discovery":
        batch(R.DISCOVERY)
    elif cmd == "holdout":
        if not (HERE / "findings_discovery.md").exists():
            sys.exit("ABORT: the discovery reading has not been written down")
        batch(R.HOLDOUT)
