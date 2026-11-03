"""NV12 zero checks. `code_v12` = `code_v11` + FF1's two fault fixes (`fix_make_choice`, `fix_overflow`, both default 1;
v11_to_v12.diff), i.e. FF1's `code_fx1` (folder FX1_fault_fixes) with both defaults switched on. Adopted 3 November 2026
by the assistant under the creator's permission to edit world rules (2 November) and FF1's frozen plan (no harm ->
nature v12; council round 51: GPT 97%, Gemini 99%, DeepSeek ~95%).

  python experiments/NV12_nature_v12/run_nv12.py zero    # hard stops; writes zero.txt

Checks: v12's code with both fixes 0 equals code_v11; v12 equals FF1's arm f (code_fx1 with both 1); v12 acts (differs
from v11); reload is exact; the live package's defaults equal v12.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"v12": HERE / "code_v12", "v11": EXP / "NV11_nature_v11" / "code_v11",
         "fx1": EXP / "FX1_fault_fixes" / "code_fx1", "live": EXP.parent}
WPY = 52
V11 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
       "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1,
       "ground_items": 1, "curiosity_pull": 1}
V12 = dict(V11)                                            # v12: both fixes are its defaults (1)
V12_OFF = {**V11, "fix_make_choice": 0, "fix_overflow": 0}  # v12's code with the fixes off
FF1_F = {**V11, "fix_make_choice": 1, "fix_overflow": 1}    # FF1's arm f on code_fx1


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
        w = make_world(seed, {"v12": V12, "v11": V11, "v12off": V12_OFF, "ff1f": FF1_F}[which])
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def reload_check(seed):
    setup("v12")
    from acl.world import World
    a = make_world(seed, V12)
    for _ in range(10 * WPY):
        a.step()
    if a.cfg.fix_make_choice != 1 or a.cfg.fix_overflow != 1:
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
        t = call("v12", "v12off", seed, years) == call("v11", "v11", seed, years)
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_v12 with both fixes 0 = code_v11: {'yes' if t else 'NO'}")
    for seed in (501, 601):
        v12 = call("v12", "v12", seed, 20)
        t = v12 == call("fx1", "ff1f", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: v12 = FF1's arm f (code_fx1 with both fixes 1): {'yes' if t else 'NO'}")
        t = v12 == call("live", "defaults", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: the live package with its own defaults = v12: {'yes' if t else 'NO'}")
    t = call("v12", "v12", 501, 20) != call("v12", "v12off", 501, 20)
    ok &= t
    lines.append(f"seed 501, 20 years: the fixes change the world (they act): {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"v12, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
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
