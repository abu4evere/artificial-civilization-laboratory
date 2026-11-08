"""NV17 zero checks. `code_v17` = `code_v16` + OD1's doors, the arm the frozen rule let go live (make_v17.py). Written
before OD1's data; run only after OD1's findings are final.

  python experiments/NV17_nature_v17/run_nv17.py zero <o|p>    # hard stops; writes zero.txt

Checks: v17's code with the five doors at 0 equals code_v16; v17 equals OD1's adopted arm (code_od1 with that arm's
doors, OD1's set-up: v11's laws and 80 founders on 80 x 80), world and random stream; v17 acts (differs from the doors
off); reload is exact; the live package's defaults equal v17.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"v17": HERE / "code_v17", "v16": EXP / "NV16_nature_v16" / "code_v16",
         "od1": EXP / "OD1_open_doors" / "code_od1", "live": EXP.parent}
WPY = 52
V11 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
       "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1,
       "ground_items": 1, "curiosity_pull": 1}
LP = {"founders": 80, "width": 80, "height": 80}
DOORS = ("similar_parts", "containers_carry", "made_binders", "made_hammers", "layers_add")
OFF = {d: 0 for d in DOORS}


def arm_doors(arm):
    return {**{d: 1 for d in DOORS}, **({"similar_parts": 0} if arm == "p" else {})}


def sets(arm):
    return {"v17": dict(V11), "v17off": {**V11, **OFF}, "v16": dict(V11), "v17lp": {**V11, **LP},
            "od1arm": {**V11, **LP, **arm_doors(arm)}}


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


def hashrun(code, which, arm, seed, years):
    setup(code)
    if which == "defaults":                       # the live package as it runs: its own defaults
        from acl.config import Config
        from acl.world import World
        w = World(Config(seed=seed, anticipation_weight=1.0))
    else:
        w = make_world(seed, sets(arm)[which])
    for _ in range(years * WPY):
        w.step()
    return world_hash(w) + ":" + rng_state(w)


def reload_check(arm, seed):
    setup("v17")
    from acl.world import World
    a = make_world(seed, sets(arm)["v17"])
    for _ in range(10 * WPY):
        a.step()
    want = arm_doors(arm)
    if any(getattr(a.cfg, d) != v for d, v in want.items()):
        return False
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for w in (a, b):
        for _ in range(5 * WPY):
            w.step()
    return world_hash(a) == world_hash(b) and all(getattr(b.cfg, d) == v for d, v in want.items())


def zero(arm):
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [f"adopted arm: {arm} ({', '.join(d for d, v in arm_doors(arm).items() if v)})"], True
    for seed, years in ((11, 5), (501, 5), (501, 20), (601, 20)):
        t = call("v17", "v17off", arm, seed, years) == call("v16", "v16", arm, seed, years)
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_v17 with the five doors at 0 = code_v16 (world and random "
                     f"stream): {'yes' if t else 'NO'}")
    for seed in (501, 601):
        t = call("v17", "v17lp", arm, seed, 20) == call("od1", "od1arm", arm, seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years, OD1's set-up: v17 = OD1's arm {arm} (code_od1), world and random stream: "
                     f"{'yes' if t else 'NO'}")
        v17 = call("v17", "v17", arm, seed, 20)
        t = v17 == call("live", "defaults", arm, seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: the live package with its own defaults = v17: {'yes' if t else 'NO'}")
    t = call("v17", "v17", arm, 501, 20) != call("v17", "v17off", arm, 501, 20)
    ok &= t
    lines.append(f"seed 501, 20 years: the doors change the world (they act): {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", arm, "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"v17, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (HERE / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero(sys.argv[2]) else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]), int(sys.argv[6])))
    elif cmd == "reload":
        print(reload_check(sys.argv[2], int(sys.argv[3])))
