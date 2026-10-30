"""NV9 zero checks. `code_v9` = `code_v8` + `curiosity_pull` on by default (v8_to_v9.diff; `code_v9` is CU1's
`code_cu1` with the setting's default changed to 1).

  python experiments/NV9_nature_v9/run_nv9.py zero    # hard stops; writes zero.txt

Checks: v9's code with curiosity_pull 0 equals code_v8; v9 equals code_cu1's arm c (the arm CU1 and LC1 tested); v9 acts
(differs from v8); reload is exact with `tried` held; the live package's defaults equal v9.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"v9": HERE / "code_v9", "v8": EXP / "NV8_nature_v8" / "code_v8",
         "cu1": EXP / "CU1_curiosity" / "code_cu1", "live": EXP.parent}
WPY = 52
V2 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1}
V3 = {**V2, "parts_first": 1}
V4 = {**V3, "bodies_stay": 1}
V5 = {**V4, "digging": 1}
V6 = {**V5, "body_rot": 1}
V7 = {**V6, "twins": 1, "sex_ratio_birth": 1}
V8 = {**V7, "ground_items": 1}
V8_OFF = {**V8, "curiosity_pull": 0}
V9 = {**V8, "curiosity_pull": 1}


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
        w = make_world(seed, {"v9": V9, "v8": V8, "v8off": V8_OFF}[which])
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def reload_check(seed):
    setup("v9")
    from acl.world import World
    a = make_world(seed, V9)
    for _ in range(10 * WPY):
        a.step()
    if not any(p.tried is not None for p in a.people.values()):
        return False                               # the check needs `tried` held
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
        t = call("v9", "v8off", seed, years) == call("v8", "v8", seed, years)
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_v9 with curiosity_pull 0 = code_v8: {'yes' if t else 'NO'}")
    for seed in (501, 601):
        v9 = call("v9", "v9", seed, 20)
        t = v9 == call("cu1", "v9", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: v9 = code_cu1's arm c: {'yes' if t else 'NO'}")
        t = v9 == call("live", "defaults", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: the live package with its own defaults = v9: {'yes' if t else 'NO'}")
    t = call("v9", "v9", 501, 20) != call("v9", "v8off", 501, 20)
    ok &= t
    lines.append(f"seed 501, 20 years: curiosity_pull changes the world (it acts): {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"v9, seed 501 (`tried` held): saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
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
