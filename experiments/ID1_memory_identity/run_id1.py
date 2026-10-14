"""ID1 — what makes an ACL person who they are? (questions.md, frozen as `ID1-frozen`; correction of 12 October appended.)
Works on copies of control worlds, never on ACL's own worlds; the copies are discarded. Control code (`code_e13r`).

  python experiments/ID1_memory_identity/run_id1.py discovery   # worlds 501-516, 601-616
  python experiments/ID1_memory_identity/run_id1.py holdout     # worlds 811-818, 1101-1124 (after the discovery reading)
  python experiments/ID1_memory_identity/run_id1.py smoke       # throwaway: seed 9401, snapshot at year 2, 8 weeks (code check only)

Per world: run the control world to the start of year 20 (week 1040) and take a snapshot (the world's own to_dict, through
JSON, as a saved world). From it, run 52 weeks each: the **original** (nothing touched); the **sham** (one extra random
draw at the moment of the swap); and, for each of the two focal people, the **eight swap arms**. The uncopied world is
also run on for 52 weeks: the original copy must reproduce it exactly (hard stop).

Operational notes written before any data (the frozen text leaves these open; each is the most literal reading):
- The original and the sham do not depend on which person is focal, so each is run once per world and serves both focal
  people (running it twice would give the identical world).
- Parts, by the frozen table: temperament = genes; habits = q; memories = memories; relationships = rel; know-how =
  recipes, itemval, skills; beliefs = beliefs, expect, heard, records; places = places, springs, sightings, shores;
  "all but temperament" = all of these except genes. Fields not in the table (puzzles, marks, placements, voyage, the
  week's thoughts and feelings, body, family) stay the focal person's own.
- A swap gives the focal person deep copies of the donor's values at the moment of the swap. At week 26 (before the 27th
  week is lived) the swapped fields are set back to deep copies of the focal person's own values at the moment of the
  swap; if the focal person has died by then, nothing is restored.
- Choosing focal people (`random.Random(seed)`): living people aged 20-45 at the snapshot, sorted by id, then shuffled.
  Each in turn becomes a focal person if a donor exists: same sex, within 10 years of age, kinship 0, not their partner,
  not already a focal person or a donor. The donor is drawn from those (sorted by id). Stop at two focal people. A world
  with none is skipped and reported; a world with one keeps its one (reported).
- Behaviour: the focal person's chosen action each week, from the world's read-only record of decisions. The donor's
  actions are read in the original copy (for "pull toward the donor").
"""
from __future__ import annotations

import copy
import hashlib
import json
import random
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODE = EXP / "E13R_replication" / "code_e13r"
OUT = HERE / "output"
WPY = 52
SNAP_YEAR, WEEKS, RESTORE = 20, 52, 26
DISCOVERY = tuple(range(501, 517)) + tuple(range(601, 617))
HOLDOUT = tuple(range(811, 819)) + tuple(range(1101, 1125))
SMOKE_SEED = 9401
PARTS = {"temperament": ("genes",), "habits": ("q",), "memories": ("memories",), "relationships": ("rel",),
         "knowhow": ("recipes", "itemval", "skills"), "beliefs": ("beliefs", "expect", "heard", "records"),
         "places": ("places", "springs", "sightings", "shores")}
PARTS["all_but_temperament"] = tuple(f for k, fs in PARTS.items() if k != "temperament" for f in fs)


def setup():
    sys.path.insert(0, str(CODE))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODE / "acl")


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def choose(w, seed):
    """Two (focal, donor) pairs, as the operational notes say."""
    rng = random.Random(seed)
    t = w.tick
    adults = sorted((p for p in w.living() if 20 <= p.years(t) <= 45), key=lambda p: p.id)
    order = adults[:]
    rng.shuffle(order)
    pairs, used = [], set()
    for f in order:
        if f.id in used:
            continue
        donors = [d for d in adults if d.id != f.id and d.id not in used and d.sex == f.sex
                  and abs(d.years(t) - f.years(t)) <= 10 and w.kinship(f, d) == 0 and w.kinship(d, f) == 0
                  and f.partner != d.id]
        if not donors:
            continue
        d = donors[rng.randrange(len(donors))]
        pairs.append((f.id, d.id))
        used |= {f.id, d.id}
        if len(pairs) == 2:
            break
    return pairs


def run_copy(snap, weeks, watch, sham=False, swap=None, restore_at=RESTORE):
    """Run a copy of the snapshot. watch: ids whose chosen actions are recorded each week.
    swap: (focal, donor, part). Returns {id: [action or None per week]}, the final hash, and the population at the end."""
    from acl.world import World
    w = World.from_dict(json.loads(snap))
    if sham:
        w.rng.random()
    back = None
    if swap:
        f, d, part = swap
        fp, dp = w.people[f], w.people[d]
        back = {k: copy.deepcopy(getattr(fp, k)) for k in PARTS[part]}
        for k in PARTS[part]:
            setattr(fp, k, copy.deepcopy(getattr(dp, k)))
    acts = {pid: [] for pid in watch}
    for wk in range(weeks):
        if swap and wk == restore_at and w.people[swap[0]].alive:
            for k, v in back.items():
                setattr(w.people[swap[0]], k, copy.deepcopy(v))
        w.step()
        chosen = {d.agent_id: d.chosen[0] for d in w.week_decisions if d.agent_id in acts and d.chosen}
        for pid in acts:
            acts[pid].append(chosen.get(pid) if w.people[pid].alive else None)
        if not w.living():
            break
    return acts, world_hash(w), len(w.living())


def run_world(seed, snap_week=SNAP_YEAR * WPY, weeks=WEEKS, restore_at=RESTORE, out=None):
    setup()
    from acl.config import Config
    from acl.world import World
    f0 = fingerprint()
    w = World(Config(seed=seed, anticipation_weight=1.0))
    for _ in range(snap_week):
        w.step()
        if not w.living():
            break
    res = {"seed": seed, "code_hash": f0, "snap_week": w.tick, "pop_at_snapshot": len(w.living())}
    pairs = choose(w, seed) if w.living() else []
    res["pairs"] = [{"focal": f, "donor": d, "sex": w.people[f].sex, "focal_age": round(w.people[f].years(w.tick), 1),
                     "donor_age": round(w.people[d].years(w.tick), 1), "focal_partnered": w.people[f].partner is not None}
                    for f, d in pairs]
    if not pairs:
        res["skipped"] = "no eligible focal person" if w.living() else "world died out before the snapshot"
    else:
        snap = json.dumps(w.to_dict(), separators=(",", ":"))
        for _ in range(weeks):                            # the uncopied world, run on: the reference
            w.step()
            if not w.living():
                break
        res["reference_hash"] = world_hash(w)
        watch = sorted({x for fd in pairs for x in fd})
        o_acts, o_hash, o_pop = run_copy(snap, weeks, watch, restore_at=restore_at)
        s_acts, s_hash, s_pop = run_copy(snap, weeks, watch, sham=True, restore_at=restore_at)
        res["original"] = {"acts": o_acts, "hash": o_hash, "pop_end": o_pop}
        res["sham"] = {"acts": s_acts, "hash": s_hash, "pop_end": s_pop}
        res["swaps"] = {}
        for f, d in pairs:
            for part in PARTS:
                acts, h, pop = run_copy(snap, weeks, [f], swap=(f, d, part), restore_at=restore_at)
                res["swaps"][f"{f}:{part}"] = {"acts": acts[f], "hash": h, "pop_end": pop}
        res["original_reproduces"] = o_hash == res["reference_hash"]
        res["all_differ"] = s_hash != o_hash and all(v["hash"] != o_hash for v in res["swaps"].values())
    res["code_hash_after"] = fingerprint()
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    flag = "" if res.get("original_reproduces", True) else "  HARD STOP: the original copy does not reproduce the world"
    print(f"seed {seed}: {len(pairs)} focal people, pop {res['pop_at_snapshot']}{flag}", flush=True)


def batch(seeds):
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [s for s in seeds if not (OUT / f"seed_{s}.json").exists()]
    stop = []

    def go(s):
        if stop:
            return
        subprocess.call(me + ["one", str(s)])
        f = OUT / f"seed_{s}.json"
        if not f.exists() or not json.loads(f.read_text(encoding="utf-8")).get("original_reproduces", True):
            stop.append(s)

    with ThreadPoolExecutor(4) as pool:
        list(pool.map(go, todo))
    print(f"HARD STOP at seed {stop[0]}" if stop else "ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "one":
        run_world(int(sys.argv[2]))
    elif cmd == "smoke":
        run_world(SMOKE_SEED, snap_week=2 * WPY, weeks=8, restore_at=4, out=HERE / "output_smoke")
    elif cmd == "discovery":
        batch(DISCOVERY)
    elif cmd == "holdout":
        if not (HERE / "findings_discovery.md").exists():
            sys.exit("ABORT: the discovery reading has not been written down")
        batch(HOLDOUT)
