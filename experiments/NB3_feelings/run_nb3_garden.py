"""NB3 phase 2: the garden (questions.md, NB3-frozen). Written before phase 1's data, from NB2's.

Genomes saved in phase 1's f worlds (the first births of generations 1 and 18), with their feeling genes, become all the
founders of a fresh world with all the feelings (code_nb3, arm f's switches), one fresh world per source world (seeds
25901-25916, paired with the sources 25801-25816). 60 years. Founder i gets sample i mod k; ages, places and the old
genes are the fresh world's own.
  g1Z, g18Z: g held at 0 for everyone (the old instincts silent), learning off, the feeling genes (H too) as inherited
Measured: the share of founders alive after one year ("does a feeling brain alone live a year?"), NB2's founders'
living-weeks, births, and the survival to 16 of children born by year 44.

  python experiments/NB3_feelings/run_nb3_garden.py pack <phase-1 output dir>    # writes garden/samples.json.gz
  python experiments/NB3_feelings/run_nb3_garden.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import glob  # noqa: E402
import gzip  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_nb3 as P  # noqa: E402

base = P.base
WPY, YEARS = P.WPY, 60
GENS = (1, 18)
PER_GEN = 30
FEEL = ("E", "G", "L", "A", "C", "H")
SOURCES = P.SEEDS
GARDEN = {s: 25901 + (s - SOURCES[0]) for s in SOURCES}
F = {**P.FULL, **P.ALLF}
ARMS = {"g1Z": {**F, "nb_learn": 0, "nb_g_fixed": 0.0}, "g18Z": {**F, "nb_learn": 0, "nb_g_fixed": 0.0}}
JOBS = [f"{a}:{GARDEN[s]}" for s in SOURCES for a in ARMS]
PACK = HERE / "garden" / "samples.json.gz"
OUT = HERE / "output_garden"
BORN_BY = 44 * WPY


def pack(src_dir):
    data = {}
    for f in sorted(glob.glob(str(Path(src_dir) / "f_seed_*.json"))):
        r = json.load(open(f))
        data[str(r["seed"])] = {str(g): [{"g": round(x["g"], 6), "eta": round(x["eta"], 6),
                                          "genome": [round(v, 6) for v in x["genome"]],
                                          **{k: round(x[k], 6) for k in FEEL}}
                                         for x in r["samples"].get(str(g), [])[:PER_GEN]] for g in GENS}
    PACK.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(PACK, "wt", encoding="utf-8") as fh:
        json.dump(data, fh, separators=(",", ":"))
    print("packed", len(data), "source worlds:", {s: {g: len(v) for g, v in d.items()} for s, d in data.items()})


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(P.CODE)
    f0 = base.fingerprint(P.CODE)
    src = next(s for s, g in GARDEN.items() if g == seed)
    gen = arm[1:-1]
    with gzip.open(PACK, "rt", encoding="utf-8") as fh:
        samples = json.load(fh)[str(src)][gen]
    w = base.make_world(seed, dict(ARMS[arm]))
    founders = sorted((p for p in w.people.values()), key=lambda p: p.id)
    res = {"arm": arm, "seed": seed, "source_seed": src, "generation": int(gen), "learn": False, "g_fixed": True,
           "n_samples": len(samples), "nature": "code_nb3", "code_hash": f0}
    if not samples:
        res.update({"skipped": "no genomes of this generation in the source world"})
    else:
        for i, p in enumerate(founders):
            x = samples[i % len(samples)]
            p.nb = {"g": x["g"], "eta": x["eta"], "genome": list(x["genome"]), "w": list(x["genome"]), "base": 0.0,
                    **{k: x[k] for k in FEEL}, "guilt": 0.0, "att": {}, "cnt": {}}
        ids = {p.id for p in founders}
        fweeks = alive1 = 0
        for _ in range(years * WPY):
            w.step()
            fweeks += sum(1 for p in w.living() if p.id in ids)
            if w.tick == WPY:
                alive1 = sum(1 for p in w.living() if p.id in ids)
            if not w.living():
                break
        kids = [p for p in w.people.values() if p.birth >= 0]
        known = [p for p in kids if p.birth < BORN_BY]
        reached = sum(1 for p in known if ((p.death_tick if not p.alive else w.tick) - p.birth) >= 16 * WPY)
        res.update({"founders": len(ids), "alive_1y": alive1, "founder_weeks": fweeks, "births": len(kids),
                    "known": len(known), "reached16": reached, "pop_end": len(w.living()), "extinct": not w.living(),
                    "final_tick": w.tick, "world_hash": base.world_hash(w)})
    res["code_hash_after"] = base.fingerprint(P.CODE)
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "pack":
        pack(sys.argv[2])
    elif cmd == "fp":
        base.setup(P.CODE)
        print(base.fingerprint(P.CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
