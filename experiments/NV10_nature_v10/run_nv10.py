"""NV10 zero checks. `code_v10` = `code_v9` with one default changed: `mortality_base` from 1.5e-5 to
1.5e-5 * 0.0072 / 0.0249 (AG1's arm b, the !Kung step; v9_to_v10.diff). Adopted by the creator's decision, 31 October 2026.

  python experiments/NV10_nature_v10/run_nv10.py zero    # hard stops; writes zero.txt

Checks: v10's code with the old mortality_base equals code_v9; v10 equals AG1's arm b (code_v9 with b's base, the arm
AG1 tested); v10 acts (differs from v9); reload is exact; the live package's defaults equal v10.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"v10": HERE / "code_v10", "v9": EXP / "NV9_nature_v9" / "code_v9", "live": EXP.parent}
WPY = 52
V2 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1}
V3 = {**V2, "parts_first": 1}
V4 = {**V3, "bodies_stay": 1}
V5 = {**V4, "digging": 1}
V6 = {**V5, "body_rot": 1}
V7 = {**V6, "twins": 1, "sex_ratio_birth": 1}
V8 = {**V7, "ground_items": 1}
V9 = {**V8, "curiosity_pull": 1}
B_BASE = 1.5e-5 * 0.0072 / 0.0249          # AG1's arm b (run_ag1.py), the same expression
V10 = dict(V9)                              # v10's mortality_base is its default
V9_OLD = {**V9, "mortality_base": 1.5e-5}   # v10's code with v9's base
AG1_B = {**V9, "mortality_base": B_BASE}    # AG1's arm b on code_v9


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
        w = make_world(seed, {"v10": V10, "v9": V9, "v9old": V9_OLD, "ag1b": AG1_B}[which])
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def reload_check(seed):
    setup("v10")
    from acl.world import World
    a = make_world(seed, V10)
    for _ in range(10 * WPY):
        a.step()
    if abs(a.cfg.mortality_base - B_BASE) > 1e-18:
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
        t = call("v10", "v9old", seed, years) == call("v9", "v9", seed, years)
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_v10 with v9's mortality_base = code_v9: {'yes' if t else 'NO'}")
    for seed in (501, 601):
        v10 = call("v10", "v10", seed, 20)
        t = v10 == call("v9", "ag1b", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: v10 = AG1's arm b (code_v9 with b's base): {'yes' if t else 'NO'}")
        t = v10 == call("live", "defaults", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: the live package with its own defaults = v10: {'yes' if t else 'NO'}")
    t = call("v10", "v10", 501, 20) != call("v10", "v9old", 501, 20)
    ok &= t
    lines.append(f"seed 501, 20 years: the new mortality_base changes the world (it acts): {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"v10, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
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
