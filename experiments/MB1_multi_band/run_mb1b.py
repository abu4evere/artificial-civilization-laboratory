"""MB1b — same 80 people, divided differently (questions_mb1b.md, frozen as `MB1b-frozen`). `code_mb1b` = `code_v2`
(nature v2) + `founding_bands`, one commit. Observers, read-only: F1's probe and MB1a's lineage observer (unchanged),
and the founding placement read at week one.

  python experiments/MB1_multi_band/run_mb1b.py zero    # hard stops: setting 0 = code_v2; b8, b16 act; observers read-only
  python experiments/MB1_multi_band/run_mb1b.py run     # p4, b8, b16, sham on seeds 5301-5556, 120 years (skips saved)
  python experiments/MB1_multi_band/run_mb1b.py smoke   # throwaway: seeds 9701-9702, 8 years, every arm (code check only)
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
CODES = {"mb1b": HERE / "code_mb1b", "v2": EXP / "NV2_nature_v2" / "code_v2"}
OUT = HERE / "output_mb1b"
WPY, YEARS = 52, 120
SEEDS = tuple(range(5301, 5557))
SMOKE_SEEDS = (9701, 9702)
V2 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1}
ARMS = {"p4": {}, "b8": {"founding_bands": 8}, "b16": {"founding_bands": 16}, "sham": {"sham_draw": 1}}
EXPECT = {"p4": (4, 20), "b8": (8, 10), "b16": (16, 5), "sham": (4, 20)}


def setup(code="mb1b"):
    sys.path.insert(0, str(CODES[code]))
    for d in ("E7_passive", "F1_baseline_fragility", "MB1_multi_band"):
        sys.path.insert(1, str(EXP / d))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, kw, founders=80):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, founders=founders, **V2, **kw))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")              # the settings list itself is left out, as every zero check has done
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["mb1b"] / "acl")


def placement(w, lin):
    """Founding bands at week one: size, island and centre of each, from MB1a's lineage map (read-only)."""
    from acl.util import distance, torus_delta
    c = w.cfg
    bands = {}
    for p in w.people.values():
        k = lin.of.get(p.id)
        if k is not None:
            bands.setdefault(k, []).append(p.loc)
    out = []
    for k, locs in sorted(bands.items()):
        x0, y0 = locs[0]          # mean on the torus: offsets from the first founder, so a band on the edge is not split
        cx = round(x0 + sum(torus_delta(x0, x, c.width) for x, _ in locs) / len(locs)) % c.width
        cy = round(y0 + sum(torus_delta(y0, y, c.height) for _, y in locs) / len(locs)) % c.height
        out.append({"band": k, "size": len(locs), "island": w.island_of(locs[0]), "centre": [cx, cy]})
    cs = [tuple(b["centre"]) for b in out]
    gaps = [distance(a, b, c.width, c.height) for i, a in enumerate(cs) for b in cs[i + 1:]]
    per_island = Counter(b["island"] for b in out)
    return {"bands": out, "n_bands": len(out), "sizes": sorted({b["size"] for b in out}),
            "max_bands_per_island": max(per_island.values()) if per_island else 0,
            "min_centre_gap": min(gaps) if gaps else None}


def observers(w):
    from run_f1 import Probe
    from run_mb1a import Lineages
    return Probe(), Lineages(w)


def hashrun(code, seed, years, kw, observe, founders):
    setup(code)
    w = make_world(seed, kw, founders)
    if observe:
        w.observers += list(observers(w))
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for founders in (20, 80):
        for seed, years in ((11, 5), (501, 5), (501, 20), (601, 20)):
            t = call("mb1b", seed, years, "{}", 0, founders) == call("v2", seed, years, "{}", 0, founders)
            ok &= t
            lines.append(f"{founders} founders, seed {seed}, {years} years: founding_bands 0 = code_v2: {'yes' if t else 'NO'}")
    base = call("mb1b", 501, 20, "{}", 0, 80)
    for arm in ("b8", "b16"):
        t = call("mb1b", 501, 20, json.dumps(ARMS[arm]), 0, 80) != base
        ok &= t
        lines.append(f"arm {arm}, seed 501, 20 years: the setting changes the world (it acts): {'yes' if t else 'NO'}")
    for arm in ("p4", "b16"):
        t = call("mb1b", 501, 20, json.dumps(ARMS[arm]), 1, 80) == call("mb1b", 501, 20, json.dumps(ARMS[arm]), 0, 80)
        ok &= t
        lines.append(f"arm {arm}, seed 501, 20 years: identical with and without the observers: {'yes' if t else 'NO'}")
    setup("mb1b")
    lines.append(f"code_mb1b fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup("mb1b")
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    probe, lin = observers(w)
    place = placement(w, lin)
    w.observers += [probe, lin]
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    nb, size = EXPECT[arm]
    res = {"arm": arm, "seed": seed, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "world_hash": world_hash(w), **probe.results(), "mb1a": lin.results(), "placement": place,
           "manipulation_ok": place["n_bands"] == nb and place["sizes"] == [size]}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: bands {place['n_bands']}x{place['sizes']}, alive {len(w.living())}, pops {probe.pops}",
          flush=True)


def batch(seeds=SEEDS, years=YEARS, out=OUT):
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: the zero checks have not passed (run 'zero')")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [(a, s) for s in seeds for a in ARMS if not (out / f"{a}_seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["one", j[0], str(j[1]), str(years), str(out)]), todo))
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), json.loads(sys.argv[5]), sys.argv[6] == "1",
                      int(sys.argv[7])))
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "run":
        batch()
    elif cmd == "smoke":
        batch(SMOKE_SEEDS, years=8, out=HERE / "output_mb1b_smoke")
