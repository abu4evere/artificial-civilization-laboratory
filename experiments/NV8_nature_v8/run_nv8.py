"""NV8 zero checks. `code_v8` = `code_v7` + `ground_items` on by default (v7_to_v8.diff; `code_v8` is OP1's `code_op1`
with the setting's default changed to 1).

  python experiments/NV8_nature_v8/run_nv8.py zero    # hard stops; writes zero.txt

Checks: v8's code with ground_items 0 equals code_v7; v8 equals code_op1's arm o (the arm OP1 and PD1 tested); v8 acts
(differs from v7); reload is exact with things on the ground; the live package's defaults equal v8.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"v8": HERE / "code_v8", "v7": EXP / "NV7_nature_v7" / "code_v7",
         "op1": EXP / "OP1_objects_persist" / "code_op1", "live": EXP.parent}
WPY = 52
V2 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1}
V3 = {**V2, "parts_first": 1}
V4 = {**V3, "bodies_stay": 1}
V5 = {**V4, "digging": 1}
V6 = {**V5, "body_rot": 1}
V7 = {**V6, "twins": 1, "sex_ratio_birth": 1}
V7_OFF = {**V7, "ground_items": 0}
V8 = {**V7, "ground_items": 1}


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


def hashrun(code, which, seed, years):
    setup(code)
    if which == "defaults":                       # the live package as it runs: its own defaults
        from acl.config import Config
        from acl.world import World
        w = World(Config(seed=seed, anticipation_weight=1.0))
    else:
        w = make_world(seed, {"v8": V8, "v7": V7, "v7off": V7_OFF}[which])
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def reload_check(seed):
    setup("v8")
    from acl.world import World
    a = make_world(seed, V8)
    for _ in range(10 * WPY):
        a.step()
    if not a.ground:
        return False                               # the check needs things lying on the ground
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
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
        t = call("v8", "v7off", seed, years) == call("v7", "v7", seed, years)
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_v8 with ground_items 0 = code_v7: {'yes' if t else 'NO'}")
    for seed in (501, 601):
        v8 = call("v8", "v8", seed, 20)
        t = v8 == call("op1", "v8", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: v8 = code_op1's arm o: {'yes' if t else 'NO'}")
        t = v8 == call("live", "defaults", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: the live package with its own defaults = v8: {'yes' if t else 'NO'}")
    t = call("v8", "v8", 501, 20) != call("v8", "v7off", 501, 20)
    ok &= t
    lines.append(f"seed 501, 20 years: ground_items changes the world (it acts): {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"v8, seed 501 (things on the ground): saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
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
