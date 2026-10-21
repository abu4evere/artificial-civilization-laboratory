"""NV3 zero checks (questions.md, frozen as `NV3-frozen`). `code_v3` = `code_v2` + `parts_first` (v2_to_v3.diff).

  python experiments/NV3_nature_v3/run_nv3.py zero    # hard stops; writes zero.txt

Checks: v3's code with parts_first 0 equals code_v2; v3 equals code_lm1's L arm; v3 acts (differs from v2);
reload is exact.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"v3": HERE / "code_v3", "v2": EXP / "NV2_nature_v2" / "code_v2",
         "lm1": EXP / "LM1_memory_and_parts" / "code_lm1"}
WPY = 52
V2 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1}
V3 = {**V2, "parts_first": 1}


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


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
    w = make_world(seed, V3 if which == "v3" else V2)
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def reload_check(seed):
    setup("v3")
    from acl.world import World
    a = make_world(seed, V3)
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
        t = call("v3", "v2", seed, years) == call("v2", "v2", seed, years)
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_v3 with parts_first 0 = code_v2: {'yes' if t else 'NO'}")
    for seed in (501, 601):
        t = call("v3", "v3", seed, 20) == call("lm1", "v3", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: v3 = code_lm1's L arm: {'yes' if t else 'NO'}")
    t = call("v3", "v3", 501, 20) != call("v3", "v2", 501, 20)
    ok &= t
    lines.append(f"seed 501, 20 years: parts_first changes the world (it acts): {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"v3, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
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
