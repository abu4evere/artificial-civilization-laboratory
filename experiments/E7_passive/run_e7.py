"""E7: one world for 1000 years with the E7 recorder, under the E6 code (baseline arm) or E6 + passive physics.

Usage:
  python experiments/E7_passive/run_e7.py e7 <seed> [years]          # E6 + passive physics (code_e7/)
  python experiments/E7_passive/run_e7.py baseline <seed> [years]    # the verified E6 code (../E6_novelty/code_e6/)
  python experiments/E7_passive/run_e7.py verify <arm> <seed> [years]  # recorder is read-only: same state hash
  python experiments/E7_passive/run_e7.py all                        # verify both arms, then every seed, E7 first
Writes output/<arm>/seed_<n>.json and a snapshot every 100 years. Each result records the code fingerprint
it ran under, so the analysis can check nothing changed during the runs.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
CODE = {"e7": HERE / "code_e7", "baseline": HERE.parent / "E6_novelty" / "code_e6"}
SEEDS = list(range(301, 309))


def code_hash(acl_folder: Path) -> str:
    """The E6 convention: sha256 over the package's .py files, by relative path."""
    h = hashlib.sha256()
    for f in sorted(acl_folder.rglob("*.py"), key=lambda f: f.relative_to(acl_folder).as_posix()):
        h.update(f.relative_to(acl_folder).as_posix().encode())
        h.update(f.read_bytes())
    return h.hexdigest()


def setup(arm: str) -> str:
    code = CODE[arm]
    sys.path.insert(0, str(code))
    sys.path.insert(1, str(HERE))
    import acl
    assert Path(acl.__file__).resolve().parent == (code / "acl").resolve(), acl.__file__
    return code_hash(code / "acl")


def run(arm: str, seed: int, years: int):
    fingerprint = setup(arm)
    from acl.config import VERSIONS, WEEKS_PER_YEAR, Config
    from acl.historian import Historian
    from acl.matter import MATERIALS
    from acl.runner import save_snapshot
    from acl.world import World
    from novelty_e7 import NoveltyE7

    out = HERE / "output" / arm
    out.mkdir(parents=True, exist_ok=True)
    w = World(Config(seed=seed))
    h = Historian()
    rec = NoveltyE7(100, MATERIALS)
    w.observers += [h, rec]
    t0 = time.time()
    for y in range(years):
        for _ in range(WEEKS_PER_YEAR):
            w.step()
        if (y + 1) % 100 == 0:
            save_snapshot(w, h, out / f"seed_{seed}_year{y + 1}.json.gz")
            print(f"  {arm} seed {seed}: year {y + 1}, {len(w.living())} alive, {time.time() - t0:.0f}s", flush=True)
        if not w.living():
            save_snapshot(w, h, out / f"seed_{seed}_end.json.gz")
            break
    res = rec.results(w)
    res.update({"arm": arm, "seed": seed, "years_run": w.year, "extinct": not w.living(), "versions": VERSIONS,
                "seconds": round(time.time() - t0), "code_hash": fingerprint,
                "code_hash_after": code_hash(CODE[arm] / "acl")})
    (out / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: done, {w.year} years, LFA {res['LFA']}, FEC {res['fec']}, {res['seconds']}s",
          flush=True)


def verify(arm: str, seed: int, years: int) -> bool:
    setup(arm)
    from acl.config import WEEKS_PER_YEAR, Config
    from acl.matter import MATERIALS
    from acl.world import World
    from novelty_e7 import NoveltyE7

    hashes = []
    for with_rec in (False, True):
        w = World(Config(seed=seed))
        if with_rec:
            w.observers.append(NoveltyE7(100, MATERIALS))
        for _ in range(years * WEEKS_PER_YEAR):
            w.step()
        hashes.append(w.state_hash())
    ok = hashes[0] == hashes[1]
    line = (f"{arm} seed {seed}, {years} years: without {hashes[0][:16]}  with {hashes[1][:16]}  -> "
            + ("READ-ONLY" if ok else "CHANGES THE WORLD"))
    print(line, flush=True)
    (HERE / "output").mkdir(exist_ok=True)
    with open(HERE / "output" / "verify.txt", "a", encoding="utf-8") as f:
        f.write(line + "\n")
    return ok


def run_all():
    """Each world in its own process, so one crash is recorded and the rest still run."""
    me = [sys.executable, str(Path(__file__).resolve())]
    for arm in ("e7", "baseline"):
        if subprocess.call(me + ["verify", arm, "304", "20"]) != 0:
            print(f"ABORT: recorder changes the world under {arm}", flush=True)
            return
    for arm in ("e7", "baseline"):
        for seed in SEEDS:
            if (HERE / "output" / arm / f"seed_{seed}.json").exists():
                print(f"{arm} seed {seed}: already done, skipped", flush=True)
                continue
            if subprocess.call(me + [arm, str(seed)]) != 0:
                print(f"{arm} seed {seed}: CRASHED", flush=True)
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "all":
        run_all()
    elif sys.argv[1] == "verify":
        ok = verify(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 20)
        sys.exit(0 if ok else 1)
    else:
        run(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 1000)
