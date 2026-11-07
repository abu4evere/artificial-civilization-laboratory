"""NV16 zero checks. `code_v16` = `code_v15` + FF4's fault fix (`fix_affordable_target`, default 1: forage, hunt and
gather are offered at the best target the person can afford when the best one is too far), without FF4's study logging.
A fault fix with FF4's harm check passed ("no harm"; GPT and Gemini's blind recomputes matched), adopted by CLAUDE.md's
safe path (a fault fix needs no confirmatory run).

  python experiments/NV16_nature_v16/run_nv16.py zero    # hard stops; writes zero.txt

Checks: v16's code with fix_affordable_target 0 equals code_v15; v16 equals FF4's arm f (code_ff4 with the fix on,
FF4's set-up: v11's laws and 80 founders on 80 x 80), world and random stream; v16 acts (differs from the fix off);
reload is exact; the live package's defaults equal v16.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"v16": HERE / "code_v16", "v15": EXP / "NV15_nature_v15" / "code_v15",
         "ff4": EXP / "FF4_affordable_targets" / "code_ff4", "live": EXP.parent}
WPY = 52
V11 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
       "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1,
       "ground_items": 1, "curiosity_pull": 1}
LP = {"founders": 80, "width": 80, "height": 80}           # FF4's set-up (run_es2.LP)
SETS = {"v16": dict(V11), "v16off": {**V11, "fix_affordable_target": 0}, "v15": dict(V11),
        "v16lp": {**V11, **LP}, "ff4f": {**V11, **LP, "fix_affordable_target": 1}}


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()
    return acl


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **kw))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def rng_state(w):
    return hashlib.sha256(repr(w.rng.getstate()).encode()).hexdigest()


def hashrun(code, which, seed, years):
    setup(code)
    if which == "defaults":                       # the live package as it runs: its own defaults
        from acl.config import Config
        from acl.world import World
        w = World(Config(seed=seed, anticipation_weight=1.0))
    else:
        w = make_world(seed, SETS[which])
    for _ in range(years * WPY):
        w.step()
    return world_hash(w) + ":" + rng_state(w)


def reload_check(seed):
    setup("v16")
    from acl.world import World
    a = make_world(seed, SETS["v16"])
    for _ in range(10 * WPY):
        a.step()
    if a.cfg.fix_affordable_target != 1:
        return False
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for w in (a, b):
        for _ in range(5 * WPY):
            w.step()
    return world_hash(a) == world_hash(b) and b.cfg.fix_affordable_target == 1


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for seed, years in ((11, 5), (501, 5), (501, 20), (601, 20)):
        t = call("v16", "v16off", seed, years) == call("v15", "v15", seed, years)
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_v16 with fix_affordable_target 0 = code_v15 (world and random "
                     f"stream): {'yes' if t else 'NO'}")
    for seed in (501, 601):
        t = call("v16", "v16lp", seed, 20) == call("ff4", "ff4f", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years, FF4's set-up: v16 = FF4's arm f (code_ff4, fix_affordable_target 1), "
                     f"world and random stream: {'yes' if t else 'NO'}")
        v16 = call("v16", "v16", seed, 20)
        t = v16 == call("live", "defaults", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: the live package with its own defaults = v16: {'yes' if t else 'NO'}")
    t = call("v16", "v16", 501, 20) != call("v16", "v16off", 501, 20)
    ok &= t
    lines.append(f"seed 501, 20 years: the fix changes the world (it acts): {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"v16, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (HERE / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
