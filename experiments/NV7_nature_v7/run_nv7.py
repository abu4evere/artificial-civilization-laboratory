"""NV7 zero checks. `code_v7` = `code_v6` + `twins` + `sex_ratio_birth` + the nursing fix (v6_to_v7.diff;
`code_v7` is `code_tw1` unchanged).

  python experiments/NV7_nature_v7/run_nv7.py zero    # hard stops; writes zero.txt

Checks: v7's code with twins 0 and sex_ratio_birth 0 equals code_v6; v7 equals code_tw1's T arm (the arm TW1 tested);
v7 acts (differs from v6); reload is exact; the live package's defaults equal v7.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"v7": HERE / "code_v7", "v6": EXP / "NV6_nature_v6" / "code_v6",
         "tw1": EXP / "TW1_twins_sex_ratio" / "code_tw1", "live": EXP.parent}
WPY = 52
V2 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1}
V3 = {**V2, "parts_first": 1}
V4 = {**V3, "bodies_stay": 1}
V5 = {**V4, "digging": 1}
V6 = {**V5, "body_rot": 1}
V7 = {**V6, "twins": 1, "sex_ratio_birth": 1}


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
        w = make_world(seed, V7 if which == "v7" else V6)
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def reload_check(seed):
    setup("v7")
    from acl.world import World
    a = make_world(seed, V7)
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
        t = call("v7", "v6", seed, years) == call("v6", "v6", seed, years)
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_v7 with twins 0 and sex_ratio_birth 0 = code_v6: {'yes' if t else 'NO'}")
    for seed in (501, 601):
        v7 = call("v7", "v7", seed, 20)
        t = v7 == call("tw1", "v7", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: v7 = code_tw1's T arm: {'yes' if t else 'NO'}")
        t = v7 == call("live", "defaults", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: the live package with its own defaults = v7: {'yes' if t else 'NO'}")
    t = call("v7", "v7", 501, 20) != call("v7", "v6", 501, 20)
    ok &= t
    lines.append(f"seed 501, 20 years: twins and sex_ratio_birth change the world (they act): {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"v7, seed 501 (a pit held): saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
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
