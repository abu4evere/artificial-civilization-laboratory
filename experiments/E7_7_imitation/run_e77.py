"""E7.7: exposure and reproduction audit. Read-only replays of the E7 worlds (E7 code), first 300 years.

Usage:
  python experiments/E7_7_imitation/run_e77.py <seed> [years]     -> output/seed_<n>.json
  python experiments/E7_7_imitation/run_e77.py verify <seed>      # probe is read-only: same state hash
  python experiments/E7_7_imitation/run_e77.py all                # verify, then seeds 301-308

The probe reads events and people each week. It also wraps knowhow.watch to count watching: the wrapper calls
the original unchanged and draws no random numbers, and the verify step proves the world is unchanged.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
E7 = HERE.parent / "E7_passive"
CODE = E7 / "code_e7"
SEEDS = list(range(301, 309))
YEARS = 300
WPY = 52

sys.path.insert(0, str(CODE))
sys.path.insert(1, str(E7))
from acl import knowhow  # noqa: E402
from acl.config import Config  # noqa: E402
from acl.historian import classify  # noqa: E402
from acl.world import World  # noqa: E402
from run_e7 import code_hash  # noqa: E402

FAMILIES = ("blade", "spear", "club", "carrier", "wrap", "boat", "fired clay", "watertight")


def families(sig: str, props: dict | None) -> list[str]:
    if not props:
        return []
    out = classify(props)
    if "clay" in sig and "^" in sig:
        out.append("fired clay")
    if props.get("tight", 0) >= 50 and props.get("contain", 0) >= 40:
        out.append("watertight")
    return out


class Probe:
    def __init__(self, world):
        self.world = world
        self.st = defaultdict(dict)          # (pid, fam) -> facts
        self.objects = defaultdict(set)      # fam -> ids of things ever seen
        self._keep = {}                      # id -> thing, so ids are never reused while we watch
        self.prev_items = {}                 # pid -> set of ids
        self.prev_recipes = {}               # pid -> set of sigs
        self.watch = defaultdict(Counter)    # fam -> counts
        self.pops = []
        self.sig_fams = defaultdict(set)     # sig -> every family a thing made from it has fallen in
        self.learned = defaultdict(list)     # pid -> [tick, sig, how] for every recipe they came to know
        self.kept = Counter()                # ('simple'|'composite', 'kept'|'forgotten') for things made in play
        self._real_watch = knowhow.watch
        knowhow.watch = self._watch

    def _sig_fams(self, sig):
        rec = self.world.knowledge.get(sig) or {}
        return set(families(sig, rec.get("props"))) | self.sig_fams[sig]

    def _watch(self, world, watcher, maker, sig, outcome):
        fams = families(sig, next((it for it in maker.items if it["sig"] == sig), None))
        before = len(watcher.recipes)
        self._real_watch(world, watcher, maker, sig, outcome)
        for f in fams:
            c = self.watch[f]
            c["watched"] += 1
            c["maker_knew"] += sig in maker.recipes
            c["good_outcome"] += outcome > 0
            c["copied"] += len(watcher.recipes) > before

    def __call__(self, world, events):
        tick = world.tick - 1
        how_by_person = defaultdict(set)     # pid -> ways things came to them this week
        learned_how = {}                     # (pid, sig) -> how
        made_now = defaultdict(set)          # pid -> families made this week
        for e in events:
            k, a = e["k"], e.get("a")
            if k in ("make", "play") and e.get("thing"):
                fams = families(e["thing"], {p: e[p] for p in ("edge", "reach", "hard", "contain", "warm", "float", "tight") if p in e})
                made_now[a].update(fams)
                self.sig_fams[e["thing"]].update(fams)
                how_by_person[a].add("made")
            elif k == "inherit":
                how_by_person[a].add("inherited")
            elif k == "consequence" and e.get("what") == "ceramic_passive":
                how_by_person[a].add("fire-hardened")
            elif k == "learn" and e.get("thing"):
                learned_how[(a, e["thing"])] = e.get("how")
        for e in events:
            if e["k"] == "play" and e.get("thing") and e.get("a") in world.people:
                kind = "composite" if e["thing"].startswith("(") else "simple"
                self.kept[(kind, "kept" if e["thing"] in world.people[e["a"]].recipes else "forgotten")] += 1
        living = world.living()
        by_tile = defaultdict(list)
        for p in living:
            by_tile[p.loc].append(p)
            # things carried
            cur = {}
            for it in p.items:
                self._keep[id(it)] = it
                self.sig_fams[it["sig"]].update(families(it["sig"], it))
                for f in families(it["sig"], it):
                    cur.setdefault(id(it), []).append(f)
                    self.objects[f].add(id(it))
            prev = self.prev_items.get(p.id, set())
            for oid, fams in cur.items():
                if oid in prev:
                    continue
                how = ("inherited" if "inherited" in how_by_person[p.id] else
                       "fire-hardened" if "fire-hardened" in how_by_person[p.id] else
                       "made" if "made" in how_by_person[p.id] else "other")
                for f in fams:
                    s = self.st[(p.id, f)]
                    s.setdefault("first_carried", tick)
                    s.setdefault("first_carried_how", how)
                    s.setdefault("first_exposed", tick)
                    s.setdefault("first_exposure_how", how)
            self.prev_items[p.id] = set(cur)
            # recipes known
            prev_r = self.prev_recipes.get(p.id, set())
            for sig in sorted(set(p.recipes) - prev_r):
                self.learned[p.id].append((tick, sig, learned_how.get((p.id, sig), "found in play")))
            self.prev_recipes[p.id] = set(p.recipes)
            for f in made_now.get(p.id, ()):
                s = self.st[(p.id, f)]
                s.setdefault("first_made", tick)
                s["made"] = s.get("made", 0) + 1
        # living beside a thing someone else carries
        for loc, people in by_tile.items():
            if len(people) < 2:
                continue
            fams_here = defaultdict(set)
            for p in people:
                for it in p.items:
                    for f in families(it["sig"], it):
                        fams_here[f].add(p.id)
            for f, holders in fams_here.items():
                for p in people:
                    if p.id not in holders:
                        s = self.st[(p.id, f)]
                        s.setdefault("first_beside", tick)
                        if "first_exposed" not in s:
                            s["first_exposed"] = tick
                            s["first_exposure_how"] = "beside"
        if tick % 520 == 519:
            self.pops.append(len(living))

    def results(self):
        # Families of recipes are settled now, when every recipe's makings are known.
        for pid, rows in self.learned.items():
            for tick, sig, how in rows:
                for f in self._sig_fams(sig):
                    s = self.st[(pid, f)]
                    if "first_recipe" not in s:
                        s["first_recipe"] = tick
                        s["first_recipe_how"] = how
        out = {}
        for f in FAMILIES:
            rows = [s for (pid, fam), s in self.st.items() if fam == f]
            carried = [s for s in rows if "first_carried" in s]
            # exposed before knowing any recipe of the family (first exposure strictly before first recipe, or never a recipe)
            naive = [s for s in rows if "first_exposed" in s and s.get("first_recipe", 10 ** 9) > s["first_exposed"]]
            learned = [s for s in naive if "first_recipe" in s]
            made_after = [s for s in naive if s.get("first_made", -1) > s["first_exposed"]]
            inherited_first = [s for s in rows if s.get("first_exposure_how") == "inherited"]
            beside_only = [s for s in rows if "first_beside" in s and "first_carried" not in s]
            knew = [s for s in rows if "first_recipe" in s]
            out[f] = {
                "objects": len(self.objects[f]),
                "people_carried": len(carried),
                "carried_first_how": dict(Counter(s["first_carried_how"] for s in carried)),
                "people_beside_only": len(beside_only),
                "beside_only_later_knew": sum(1 for s in beside_only if "first_recipe" in s),
                "exposed_before_knowing": len(naive),
                "exposure_how": dict(Counter(s["first_exposure_how"] for s in naive)),
                "later_learned": len(learned),
                "learned_how": dict(Counter(s["first_recipe_how"] for s in learned)),
                "later_made": len(made_after),
                "never_learned": len(naive) - len(learned),
                "inherited_first": len(inherited_first),
                "inherited_first_later_made": sum(1 for s in inherited_first if s.get("first_made", -1) > s["first_exposed"]),
                "ever_knew": len(knew),
                "knew_and_made": sum(1 for s in knew if s.get("made", 0) > 0),
                "recipe_first_how_all": dict(Counter(s["first_recipe_how"] for s in knew)),
                "watching": dict(self.watch[f]),
            }
        return out


def run(seed: int, years: int = YEARS):
    fp = code_hash(CODE / "acl")
    saved = json.loads((E7 / "output" / "e7" / f"seed_{seed}.json").read_text(encoding="utf-8"))
    w = World(Config(seed=seed))
    probe = Probe(w)
    w.observers.append(probe)
    t0 = time.time()
    for _ in range(min(years, saved["years_run"]) * WPY):
        w.step()
        if not w.living():
            break
    saved_pops = [s["population"] for s in saved["samples"]]
    n = min(len(saved_pops), len(probe.pops))
    out = {"seed": seed, "years": w.year, "code_hash": fp, "code_hash_after": code_hash(CODE / "acl"),
           "replay_matches_saved": n > 0 and probe.pops[:n] == saved_pops[:n],
           "families": probe.results(),
           "kept_after_play": {f"{a}/{b}": n for (a, b), n in probe.kept.items()}, "seconds": round(time.time() - t0)}
    (HERE / "output").mkdir(exist_ok=True)
    (HERE / "output" / f"seed_{seed}.json").write_text(json.dumps(out), encoding="utf-8")
    print(f"seed {seed}: {w.year} years, replay matches: {out['replay_matches_saved']}, {out['seconds']}s", flush=True)


def verify(seed: int, years: int = 20) -> bool:
    hashes = []
    for with_probe in (False, True):
        w = World(Config(seed=seed))
        if with_probe:
            w.observers.append(Probe(w))
        for _ in range(years * WPY):
            w.step()
        hashes.append(w.state_hash())
    ok = hashes[0] == hashes[1]
    line = f"e7 seed {seed}, {years} years: {hashes[0][:16]} / {hashes[1][:16]} -> {'READ-ONLY' if ok else 'CHANGES THE WORLD'}"
    print(line, flush=True)
    (HERE / "output").mkdir(exist_ok=True)
    with open(HERE / "output" / "verify.txt", "a", encoding="utf-8") as f:
        f.write(line + "\n")
    return ok


def run_all():
    me = [sys.executable, str(Path(__file__).resolve())]
    if subprocess.call(me + ["verify", "304"]) != 0:
        print("ABORT: probe changes the world", flush=True)
        return
    for seed in SEEDS:
        if not (HERE / "output" / f"seed_{seed}.json").exists():
            if subprocess.call(me + [str(seed)]) != 0:
                print(f"seed {seed}: CRASHED", flush=True)
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "all":
        run_all()
    elif sys.argv[1] == "verify":
        sys.exit(0 if verify(int(sys.argv[2])) else 1)
    else:
        run(int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else YEARS)
