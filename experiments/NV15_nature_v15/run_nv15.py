"""NV15 zero checks. `code_v15` = `code_v14` + CI1/CI1-C's LG law (`child_make`, default 1: children aged 3 and over are
offered the make option). Adopted 6 November 2026 by the assistant by CLAUDE.md's safe path: CI1 supported LG, CI1-C
confirmed it on new seeds, blind recomputes by GPT and Gemini matched both, council round 71 (GPT 99%, Gemini 100%,
DeepSeek about 94%; the assistant 92%).

  python experiments/NV15_nature_v15/run_nv15.py zero    # hard stops; writes zero.txt

Checks: v15's code with child_make 0 equals code_v14; v15 equals CI1-C's arm g (code_ci1 with child_make 1, held_aim 0,
CI1-C's set-up: v11's laws and 80 founders on 80 x 80), world and random stream; v15 acts (differs from child_make 0);
reload is exact; the live package's defaults equal v15.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"v15": HERE / "code_v15", "v14": EXP / "NV14_nature_v14" / "code_v14",
         "ci1": EXP / "CI1_children_and_aims" / "code_ci1", "live": EXP.parent}
WPY = 52
V11 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
       "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1,
       "ground_items": 1, "curiosity_pull": 1}
LP = {"founders": 80, "width": 80, "height": 80}           # CI1-C's set-up (run_es2.LP)
SETS = {"v15": dict(V11), "v15off": {**V11, "child_make": 0}, "v14": dict(V11),
        "v15lp": {**V11, **LP}, "ci1g": {**V11, **LP, "child_make": 1, "held_aim": 0}}


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


def hashrun(code, which, seed, years):
    setup(code)
    if which == "defaults":                       # the live package as it runs: its own defaults
        from acl.config import Config
        from acl.world import World
        w = World(Config(seed=seed, anticipation_weight=1.0))
    else:
        w = make_world(seed, SETS[which])
    for _ in range(years * WPY):
        w.step()
    return world_hash(w) + ":" + rng_state(w)


def reload_check(seed):
    setup("v15")
    from acl.world import World
    a = make_world(seed, SETS["v15"])
    for _ in range(10 * WPY):
        a.step()
    if a.cfg.child_make != 1:
        return False
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for w in (a, b):
        for _ in range(5 * WPY):
            w.step()
    return world_hash(a) == world_hash(b) and b.cfg.child_make == 1


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for seed, years in ((11, 5), (501, 5), (501, 20), (601, 20)):
        t = call("v15", "v15off", seed, years) == call("v14", "v14", seed, years)
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_v15 with child_make 0 = code_v14 (world and random stream): "
                     f"{'yes' if t else 'NO'}")
    for seed in (501, 601):
        t = call("v15", "v15lp", seed, 20) == call("ci1", "ci1g", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years, CI1-C's set-up: v15 = CI1-C's arm g (code_ci1, child_make 1, held_aim 0), "
                     f"world and random stream: {'yes' if t else 'NO'}")
        v15 = call("v15", "v15", seed, 20)
        t = v15 == call("live", "defaults", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: the live package with its own defaults = v15: {'yes' if t else 'NO'}")
    t = call("v15", "v15", 501, 20) != call("v15", "v15off", 501, 20)
    ok &= t
    lines.append(f"seed 501, 20 years: the law changes the world (it acts): {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"v15, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
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
