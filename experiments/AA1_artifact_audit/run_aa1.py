"""AA1 — artifact audit (questions.md, frozen as `AA1-frozen`; code review appended before this file was written).
A logging copy of the control code (`code_aa1`: code_e13r plus log lines that write outside the world's state) and a
read-only observer that turns the log into AA1's measures.

  python experiments/AA1_artifact_audit/run_aa1.py zero        # the logging copy reproduces the control world exactly
  python experiments/AA1_artifact_audit/run_aa1.py discovery   # seeds 501-516, 120 years
  python experiments/AA1_artifact_audit/run_aa1.py holdout     # seeds 601-616 (after the discovery reading is written)

Operational details written before any data:
- A water crossing = a walk that ends on a different landmass than it started on, where landmasses are land joined
  along edges (4-connected, computed once from the map). The world's own `landmasses()` joins land that touches only at
  a corner (8-connected); that definition would hide A1 by construction, so A1 uses the 4-connected one. (Fixed after a
  smoke test on throwaway seeds and before any data.) Every walk containing a corner step is also counted. Each crossing is classed: with a boat (water crossed while carrying something that floats), corner (a
  diagonal step between two water tiles that touch at a corner, no water tile entered), wrapping edge, or other.
- Food of the dead (A3): each tile keeps an estimate of how much of its wild plants came from the dead; it rises by
  what is dropped, is capped each week at the tile's plants, and when someone forages there the food taken is
  attributed to the dead in proportion (estimate ÷ plants before taking).
- A5 / A6c: a chosen "go to" move is tagged by the branch that offered it (toward an absent loved one; toward an eligible
  single in partner search) and the distance to that person; "beyond sight" = farther than `perception`.
- A6a / A6b: gifts and thefts are counted from the world's own events; their food is compared with the food taken from
  the wild by foraging (the denominator for "all food" is food foraged from the wild, the bulk of what people eat).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"aa1": HERE / "code_aa1", "e13r": EXP / "E13R_replication" / "code_e13r"}
OUT = HERE / "output"
WPY, YEARS = 52, 120
DISCOVERY, HOLDOUT = tuple(range(501, 517)), tuple(range(601, 617))


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


class Audit:
    """Reads the logging copy's log after each week, and the world's events; writes nothing to the world."""

    def __init__(self):
        self.buf, self.n, self.mass, self.dead = [], Counter(), None, {}

    def _masses(self, world):
        c, seen, k = world.cfg, {}, 0
        for y in range(c.height):
            for x in range(c.width):
                if world.tiles[y][x].water or (x, y) in seen:
                    continue
                stack = [(x, y)]
                seen[(x, y)] = k
                while stack:
                    a, b = stack.pop()
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):   # joined along edges only
                        q = ((a + dx) % c.width, (b + dy) % c.height)
                        if q not in seen and not world.tiles[q[1]][q[0]].water:
                            seen[q] = k
                            stack.append(q)
                k += 1
        return seen

    def __call__(self, world, events):
        n = self.n
        if self.mass is None:
            self.mass = self._masses(world)
        n["person_weeks"] += len(world.living())
        for e in events:
            if e["k"] == "give":
                n["gifts"] += 1
                n["gift_food"] += e.get("amount", 0.0) or 0.0
            elif e["k"] == "steal":
                n["thefts"] += 1
                n["steal_food"] += e.get("amount", 0.0) or 0.0
        for rec in self.buf:
            kind = rec[0]
            if kind == "walk":
                _, pid, src, end, corner, wrap, crossed, boat = rec
                n["walks"] += 1
                n["walks_wrap"] += wrap
                n["walks_corner"] += corner
                a, b = self.mass.get(tuple(src)), self.mass.get(tuple(end))
                if a is not None and b is not None and a != b:
                    n["crossings"] += 1
                    how = "boat" if crossed and boat else "corner" if corner else "wrap" if wrap else "other"
                    n["crossings_" + how] += 1
            elif kind == "dropped":
                _, loc, amt = rec
                self.dead[tuple(loc)] = self.dead.get(tuple(loc), 0.0) + amt
                n["dropped_food"] += amt
            elif kind == "forage":
                _, loc, before, taken = rec
                n["foraged_wild"] += taken
                stock = self.dead.get(tuple(loc), 0.0)
                if stock > 0 and before > 0 and taken > 0:
                    got = taken * min(1.0, stock / before)
                    self.dead[tuple(loc)] = stock - got
                    n["foraged_from_dead"] += got
            elif kind == "dry":
                n["dry_judgements"] += 1
                n["dry_beyond_sight"] += rec[1]
            elif kind == "chose":
                _, pid, act, tag, dist = rec
                n["choices"] += 1
                if act == "join":
                    n["joins"] += 1
                    if tag:
                        beyond = dist > world.cfg.perception
                        n[f"joins_{tag}"] += 1
                        n[f"joins_{tag}_beyond_sight"] += beyond
                        if beyond:
                            n[f"dist_{tag}_beyond_sum"] += dist
                elif act in ("give", "steal"):
                    n[f"chose_{act}"] += 1
        self.buf.clear()
        for loc in list(self.dead):   # the estimate cannot exceed the tile's plants
            t = world.tiles[loc[1]][loc[0]]
            if self.dead[loc] > t.plants:
                self.dead[loc] = t.plants
            if self.dead[loc] <= 1e-9:
                del self.dead[loc]

    def results(self):
        return {k: round(v, 3) if isinstance(v, float) else v for k, v in self.n.items()}


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["aa1"] / "acl")


def hash_run(code, seed, years, log):
    setup(code)
    w = make_world(seed)
    if log:
        a = Audit()
        w.aa1log = a.buf
        w.observers.append(a)
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]
    call = lambda code, seed, log: subprocess.run(me + ["hashrun", code, str(seed), "1" if log else "0"],  # noqa: E731
                                                  capture_output=True, text=True).stdout.strip().splitlines()[-1]
    lines, ok = [], True
    for seed in (501, 601):
        t = call("e13r", seed, False) == call("aa1", seed, True)
        ok &= t
        lines.append(f"logging copy with log and observer on, seed {seed}, 20 years: reproduces the control world: {'yes' if t else 'NO'}")
    setup("aa1")
    lines.append(f"code_aa1 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "zero.txt").write_text("\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n", encoding="utf-8")
    print("\n".join(lines), f"\nAll: {'PASS' if ok else 'FAIL'}", flush=True)
    return ok


def run_one(seed, years=YEARS, out=None):
    setup("aa1")
    f0 = fingerprint()
    w = make_world(seed)
    a = Audit()
    w.aa1log = a.buf
    w.observers.append(a)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"seed": seed, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "world_hash": world_hash(w), "audit": a.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: ended week {w.tick}", flush=True)


def batch(seeds):
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: the logging copy has not been shown to leave the world unchanged")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [s for s in seeds if not (OUT / f"seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda s: subprocess.call(me + ["one", str(s)]), todo))
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hash_run(sys.argv[2], int(sys.argv[3]), 20, sys.argv[4] == "1"))
    elif cmd == "one":
        run_one(int(sys.argv[2]))
    elif cmd == "discovery":
        batch(DISCOVERY)
    elif cmd == "holdout":
        if not (HERE / "findings_discovery.md").exists():
            sys.exit("ABORT: the discovery reading has not been written down")
        batch(HOLDOUT)
