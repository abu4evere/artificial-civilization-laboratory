"""NV6 zero checks. `code_v6` = `code_v5` + `body_rot` (v5_to_v6.diff).

  python experiments/NV6_nature_v6/run_nv6.py zero    # hard stops; writes zero.txt

Checks: v6's code with body_rot 0 equals code_v5; v6 equals code_bd2's R arm (the arm BD2 tested); v6 acts
(differs from v5); reload is exact; the live package's defaults equal v6.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"v6": HERE / "code_v6", "v5": EXP / "NV5_nature_v5" / "code_v5",
         "bd2": EXP / "BD2_realistic_rot" / "code_bd2", "live": EXP.parent}
WPY = 52
V2 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1}
V3 = {**V2, "parts_first": 1}
V4 = {**V3, "bodies_stay": 1}
V5 = {**V4, "digging": 1}
V6 = {**V5, "body_rot": 1}


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
        w = make_world(seed, V6 if which == "v6" else V5)
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def reload_check(seed):
    setup("v6")
    from acl.world import World
    a = make_world(seed, V6)
    a.pits.setdefault("0,0", [0.7, 0])
    for _ in range(10 * WPY):
        a.step()
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
        t = call("v6", "v5", seed, years) == call("v5", "v5", seed, years)
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_v6 with body_rot 0 = code_v5: {'yes' if t else 'NO'}")
    for seed in (501, 601):
        v6 = call("v6", "v6", seed, 20)
        t = v6 == call("bd2", "v6", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: v6 = code_bd2's R arm: {'yes' if t else 'NO'}")
        t = v6 == call("live", "defaults", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: the live package with its own defaults = v6: {'yes' if t else 'NO'}")
    t = call("v6", "v6", 501, 20) != call("v6", "v5", 501, 20)
    ok &= t
    lines.append(f"seed 501, 20 years: body_rot changes the world (it acts): {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"v6, seed 501 (a pit held): saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
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
