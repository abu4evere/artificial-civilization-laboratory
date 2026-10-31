"""NV11 zero checks. `code_v11` = `code_v10` + the handing law (`hand_items`, default 1; v10_to_v11.diff), i.e. HD1's
`code_hd1` with the default switched on. Adopted 31 October 2026 by the assistant under the creator's safe-path rule
(HD1 and HD1-C final and recomputed; GPT 92%, Gemini 88%).

  python experiments/NV11_nature_v11/run_nv11.py zero    # hard stops; writes zero.txt

Checks: v11's code with hand_items 0 equals code_v10; v11 equals HD1's arm h (code_hd1 with hand_items 1, the arm HD1
and HD1-C tested); v11 acts (differs from v10); reload is exact; the live package's defaults equal v11.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"v11": HERE / "code_v11", "v10": EXP / "NV10_nature_v10" / "code_v10", "hd1": EXP / "HD1_handing" / "code_hd1",
         "live": EXP.parent}
WPY = 52
V2 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1}
V3 = {**V2, "parts_first": 1}
V4 = {**V3, "bodies_stay": 1}
V5 = {**V4, "digging": 1}
V6 = {**V5, "body_rot": 1}
V7 = {**V6, "twins": 1, "sex_ratio_birth": 1}
V8 = {**V7, "ground_items": 1}
V9 = {**V8, "curiosity_pull": 1}
V10 = dict(V9)                              # v10: code_v10's own defaults for mortality_base
V11 = dict(V10)                             # v11: hand_items is its default (1)
V11_OFF = {**V10, "hand_items": 0}          # v11's code with the law off
HD1_H = {**V10, "hand_items": 1}            # HD1's arm h on code_hd1


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
        w = make_world(seed, {"v11": V11, "v10": V10, "v11off": V11_OFF, "hd1h": HD1_H}[which])
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def reload_check(seed):
    setup("v11")
    from acl.world import World
    a = make_world(seed, V11)
    for _ in range(10 * WPY):
        a.step()
    if a.cfg.hand_items != 1:
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
        t = call("v11", "v11off", seed, years) == call("v10", "v10", seed, years)
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_v11 with hand_items 0 = code_v10: {'yes' if t else 'NO'}")
    for seed in (501, 601):
        v11 = call("v11", "v11", seed, 20)
        t = v11 == call("hd1", "hd1h", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: v11 = HD1's arm h (code_hd1 with hand_items 1): {'yes' if t else 'NO'}")
        t = v11 == call("live", "defaults", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: the live package with its own defaults = v11: {'yes' if t else 'NO'}")
    t = call("v11", "v11", 501, 20) != call("v11", "v11off", 501, 20)
    ok &= t
    lines.append(f"seed 501, 20 years: the handing law changes the world (it acts): {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"v11, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
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
