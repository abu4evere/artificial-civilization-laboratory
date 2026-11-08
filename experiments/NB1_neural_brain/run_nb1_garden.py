"""NB1 phase 2 — the common garden (questions.md, NB1-frozen, amendment 2). Written before phase 1's data.

Genomes saved in phase 1's n worlds (the first births of generations 1, 9 and 18; amendment 3) become all the founders of a fresh
v17 world with the neural brain (code_nb1, LP), one fresh world per source world (seeds 25501-25516, paired with the
source seeds 25401-25416), run twice: learning on (L) and off (N). 60 years. Founders take the source genomes in a
fixed order (founder i gets sample i mod n); their genes, ages and places are the fresh world's own, so only the
networks differ between generations.

Measured per world: the founders' living-weeks (their survival), births in the world, the survival to 16 of the
children born by year 44 (so every outcome is known by year 60), population at year 60, and extinction.

  python experiments/NB1_neural_brain/run_nb1_garden.py pack <phase-1 output dir>    # writes garden/samples.json.gz
  python experiments/NB1_neural_brain/run_nb1_garden.py one <arm> <seed> <years> <out>
Arms: "g1L", "g1N", "g9L", "g9N", "g18L", "g18N" (generation, learning on or off).
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
import run_nb1 as P  # noqa: E402

base = P.base
WPY, YEARS = P.WPY, 60
GENS = (1, 9, 18)                                # amendment 3
PER_GEN = 30                                      # genomes packed per generation and source world
SOURCES = P.SEEDS
GARDEN = {s: 25501 + (s - SOURCES[0]) for s in SOURCES}
ARMS = {f"g{g}{l}": {**base.LP, "nb_brain": 1, "nb_learn": 1 if l == "L" else 0} for g in GENS for l in "LN"}
JOBS = [f"{a}:{GARDEN[s]}" for s in SOURCES for a in ARMS]
PACK = HERE / "garden" / "samples.json.gz"
OUT = HERE / "output_garden"
BORN_BY = 44 * WPY


def pack(src_dir):
    data = {}
    for f in sorted(glob.glob(str(Path(src_dir) / "n_seed_*.json"))):
        r = json.load(open(f))
        data[str(r["seed"])] = {str(g): [{"g": round(x["g"], 6), "eta": round(x["eta"], 6),
                                          "genome": [round(v, 6) for v in x["genome"]]}
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
    res = {"arm": arm, "seed": seed, "source_seed": src, "generation": int(gen), "learn": arm.endswith("L"),
           "n_samples": len(samples), "nature": "code_nb1", "code_hash": f0}
    if not samples:
        res.update({"skipped": "no genomes of this generation in the source world"})
    else:
        for i, p in enumerate(founders):
            x = samples[i % len(samples)]
            p.nb = {"g": x["g"], "eta": x["eta"], "genome": list(x["genome"]), "w": list(x["genome"]), "base": 0.0}
        ids = {p.id for p in founders}
        fweeks = 0
        for _ in range(years * WPY):
            w.step()
            fweeks += sum(1 for p in w.living() if p.id in ids)
            if not w.living():
                break
        kids = [p for p in w.people.values() if p.birth >= 0]
        known = [p for p in kids if p.birth < BORN_BY]
        reached = sum(1 for p in known if ((p.death_tick if not p.alive else w.tick) - p.birth) >= 16 * WPY)
        res.update({"founder_weeks": fweeks, "births": len(kids), "known": len(known), "reached16": reached,
                    "pop_end": len(w.living()), "extinct": not w.living(), "final_tick": w.tick,
                    "world_hash": base.world_hash(w)})
    res["code_hash_after"] = base.fingerprint(P.CODE)
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "pack":
        pack(sys.argv[2])
    elif cmd == "fp":                     # the same code_nb1 as phase 1, so phase 1's zero record applies
        base.setup(P.CODE)
        print(base.fingerprint(P.CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
