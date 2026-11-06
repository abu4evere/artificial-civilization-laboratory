"""NV14 zero checks. `code_v14` = `code_v13` + FF3's fault fix (`fix_name_ties` F9, default 1), i.e. FF3's `code_ff3`
with the default switched on. Adopted 6 November 2026 by the assistant under the creator's permission to edit world rules
(2 November) and FF3's frozen plan (no harm -> nature v14; council rounds 66 and 67).

  python experiments/NV14_nature_v14/run_nv14.py zero    # hard stops; writes zero.txt

Checks: v14's code with the fix 0 equals code_v13; v14 equals FF3's arm f (code_ff3 with the fix 1); v14 acts (differs
from v13); reload is exact; the live package's defaults equal v14.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"v14": HERE / "code_v14", "v13": EXP / "NV13_nature_v13" / "code_v13",
         "ff3": EXP / "FF3_name_ties" / "code_ff3", "live": EXP.parent}
WPY = 52
V11 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
       "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1,
       "ground_items": 1, "curiosity_pull": 1}
V13 = dict(V11)                                            # v13: its own defaults
V14 = dict(V11)                                            # v14: the fix is its default (1)
V14_OFF = {**V11, "fix_name_ties": 0}                      # v14's code with the fix off
FF3_F = {**V11, "fix_name_ties": 1}                        # FF3's arm f on code_ff3


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
        w = make_world(seed, {"v14": V14, "v13": V13, "v14off": V14_OFF, "ff3f": FF3_F}[which])
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def reload_check(seed):
    setup("v14")
    from acl.world import World
    a = make_world(seed, V14)
    for _ in range(10 * WPY):
        a.step()
    if a.cfg.fix_name_ties != 1:
        return False
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
        t = call("v14", "v14off", seed, years) == call("v13", "v13", seed, years)
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_v14 with the fix 0 = code_v13: {'yes' if t else 'NO'}")
    for seed in (501, 601):
        v14 = call("v14", "v14", seed, 20)
        t = v14 == call("ff3", "ff3f", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: v14 = FF3's arm f (code_ff3 with the fix 1): {'yes' if t else 'NO'}")
        t = v14 == call("live", "defaults", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: the live package with its own defaults = v14: {'yes' if t else 'NO'}")
    t = call("v14", "v14", 501, 20) != call("v14", "v14off", 501, 20)
    ok &= t
    lines.append(f"seed 501, 20 years: the fix changes the world (it acts): {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"v14, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
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
