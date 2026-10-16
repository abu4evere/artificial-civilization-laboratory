"""Experiment 1 measurements. Read-only.

A Lab watches a world week by week, next to the historian, and once a year
records what the long experiments ask about:

- shared symbols: marks that several people take to go with the same thing,
  how long each lasts, and whether it reaches people born after it formed;
- false beliefs: wrong versions of stories, superstitions (beliefs about
  leaving things where no physical effect exists), hearsay, and water
  believed in where there is none;
- inventions: kinds of things ever made, and the historian's named classes;
- technique survival: how long each way of making something stays known, by
  how many people, across how many generations;
- knowledge loss: techniques lost, and found again;
- trust networks: how trust is spread, its strong ties and clusters, ties
  across islands, and whether people who turn out right are trusted more;
- surprise loops: puzzles opened, tested, settled or dropped, and what they
  led to.

It never changes the world (a test checks that). Nothing in it is used by
the people.
"""
from __future__ import annotations

import math
from collections import Counter

from . import marks
from .config import WEEKS_PER_YEAR
from .historian import CLASSES, classify
from .weather import fresh_near

# Leaving these somewhere has a physical effect: seed grows, food keeps,
# materials heaped up enclose or cover. Flint left lying does nothing, and
# striking two things without flint makes no sparks.
WORKS = ("seeds", "food", "wood", "hide", "fiber", "stone", "bone")


def superstitious(key: str) -> bool:
    """True if a belief about `key` ("thing@season") credits something that has no physical way to matter."""
    thing = key.split("@")[0]
    if "/" in thing:
        return "flint" not in thing.split("/")
    return thing not in WORKS


def _pearson(xs: list, ys: list):
    n = len(xs)
    if n < 5:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return None
    return round(sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy), 3)


class Lab:
    def __init__(self, historian):
        self.h = historian
        self.years: list[dict] = []
        self.counts: Counter = Counter()              # this year's events
        self.techniques: dict[str, dict] = {}         # sig -> its life
        self.puzzles: dict[str, dict] = {}            # "pid|key" -> an open puzzle
        self.puzzle_ends: Counter = Counter()         # how puzzles ended, all time
        self.puzzle_tests: list[int] = []             # tests per ended puzzle
        self.sources: dict[str, list] = {}            # pid -> [claims that held, claims that failed]
        self.symbols: dict[str, dict] = {}            # "shape|thing" -> its life
        self.fire_puzzles: dict[str, int] = {}        # pid -> week their last sparks/fire puzzle opened
        self._island: dict | None = None
        self.accuracy_pairs: list = []                # [how often right as a source, how trusted] this year
        self.record_pairs: list = []                  # [how often right as a source, how others' records rate them]
        self.seq: dict[str, list] = {}                # person -> outcomes of their tested claims, in order

    # --- weekly --------------------------------------------------------------------------------

    def __call__(self, world, events: list) -> None:
        tick = world.tick - 1
        for e in events:
            k = e["k"]
            self.counts[k] += 1
            a = e.get("a")
            if k == "puzzled":
                key = f"{a}|{e.get('about')}"
                if key not in self.puzzles:
                    self.puzzles[key] = {"start": tick, "tests": 0, "last_gap": None}
                if str(e.get("about", "")).startswith("f:"):
                    self.fire_puzzles[a] = tick
            elif k == "tested":
                pz = self.puzzles.get(f"{a}|{e.get('about')}")
                if pz is not None:
                    pz["tests"] += 1
                    pz["last_gap"] = abs(e.get("gap", 0.0))
            elif k in ("verified", "refuted"):
                self.counts[f"{k}_{str(e.get('claim', ''))[:2]}"] += 1
                for src in e.get("by") or []:
                    rec = self.sources.setdefault(src, [0, 0])
                    rec[0 if k == "verified" else 1] += 1
                    if src.startswith("mark:"):
                        self.counts["mark_" + k] += 1
                    else:
                        self.seq.setdefault(src, []).append(1 if k == "verified" else 0)
            elif k in ("play", "make") and e.get("thing"):
                self._made(world, e, tick)
            elif k == "learn" and e.get("thing"):
                self.counts["learn_how_" + str(e.get("how"))] += 1
                if e.get("meant"):
                    self.counts["learned_wrong"] += 1
            elif k == "learn" and e.get("belief"):
                self.counts["learn_belief"] += 1
            elif k == "fire" and e.get("how") == "sparks":
                started = self.fire_puzzles.get(a)
                if started is not None and tick - started <= WEEKS_PER_YEAR:
                    self.counts["fire_after_puzzle"] += 1
            elif k == "knowledge_lost":
                rec = self.techniques.get(e.get("thing"))
                if rec is not None:
                    rec["lost"].append(tick)
            elif k == "told":
                self.counts["heard_" + str(e.get("heard"))] += 1
                if e.get("changed"):
                    self.counts["told_changed"] += 1
        self._close_puzzles(world)
        if tick % WEEKS_PER_YEAR == WEEKS_PER_YEAR - 1:
            self._year(world, tick)

    def _made(self, world, e, tick) -> None:
        sig = e["thing"]
        rec = self.techniques.get(sig)
        p = world.people.get(e.get("a"))
        if rec is None:
            puzzled = bool(p and p.thoughts and p.thoughts[0][0] == "puzzle")
            props = {k: e[k] for k in ("edge", "reach", "hard", "contain", "warm", "float") if k in e} or None
            self.techniques[sig] = {
                "first": tick, "inventor": e.get("a"), "gen": p.generation if p else 0,
                "classes": classify(props), "puzzled": puzzled, "lost": [], "found_again": [],
                "holders_max": 1, "last_known": tick, "gen_span": 0, "years_known": 0,
            }
            self.counts["new_technique"] += 1
            if puzzled:
                self.counts["new_technique_while_puzzled"] += 1
        elif rec["lost"] and (not rec["found_again"] or rec["found_again"][-1] < rec["lost"][-1]):
            rec["found_again"].append(tick)

    def _close_puzzles(self, world) -> None:
        for key in list(self.puzzles):
            pid, _, about = key.partition("|")
            p = world.people.get(pid)
            if p is not None and p.alive and about in p.puzzles:
                continue
            pz = self.puzzles.pop(key)
            if p is None or not p.alive:
                end = "died"
            elif pz["tests"] == 0:
                end = "faded untested"
            elif pz["last_gap"] is not None and pz["last_gap"] < 0.1:
                end = "settled by testing"
            else:
                end = "dropped after testing"
            self.puzzle_ends[end] += 1
            self.counts["puzzle_" + end] += 1
            if end != "died":
                self.puzzle_tests.append(pz["tests"])

    # --- yearly -------------------------------------------------------------------------------

    def _islands(self, world) -> dict:
        if self._island is None:
            self._island = {}
            for i, comp in enumerate(world.landmasses()):
                for loc in comp:
                    self._island[loc] = i
        return self._island

    def _year(self, world, tick: int) -> None:
        year = tick // WEEKS_PER_YEAR
        living = world.living()
        n = len(living)
        hrow = self.h.years[-1] if self.h.years and self.h.years[-1]["year"] == year else {}
        row = {"year": year, "population": n,
               "generation": max((p.generation for p in living), default=0),
               "births": hrow.get("births", 0), "deaths": hrow.get("deaths", 0),
               "deaths_by_cause": hrow.get("deaths_by_cause", {})}
        row["symbols"] = self._symbols(world, year, living)
        row["false_beliefs"] = self._false_beliefs(world, living)
        row["inventions"] = self._inventions(world)
        row["techniques"] = self._technique_survival(world, tick, living)
        row["trust"] = self._trust(world, living)
        row["surprise"] = self._surprise(living)
        row["events"] = {k: v for k, v in self.counts.items()}
        self.counts = Counter()
        self.years.append(row)

    def _symbols(self, world, year: int, living: list) -> dict:
        shared = marks.shared(world)
        island = self._islands(world)
        on_land = sum(len(t.marks) for r in world.tiles for t in r)
        shapes = set()
        for q in living:
            shapes.update(q.marks)
        for shape, thing, k in shared:
            key = f"{shape}|{thing}"
            sharers = [q for q in living if marks.meaning(q, shape).get(thing, 0.0) >= 0.3]
            rec = self.symbols.get(key)
            if rec is None:
                rec = {"first": year, "last": year, "max": k, "years": 0, "younger": False, "islands": 1}
                self.symbols[key] = rec
            rec["last"] = year
            rec["years"] += 1
            rec["max"] = max(rec["max"], k)
            born_after = rec["first"] * WEEKS_PER_YEAR
            if any(q.birth > born_after for q in sharers):
                rec["younger"] = True
            rec["islands"] = max(rec["islands"], len({island.get(q.loc, -1) for q in sharers}))
        return {"shared_pairs": len(shared), "shapes_on_land": on_land,
                "shapes_known": len(shapes),
                "most_sharers": max((k for _, _, k in shared), default=0),
                "things": dict(Counter(t for _, t, _ in shared))}

    def _false_beliefs(self, world, living: list) -> dict:
        stories = self.h._story_drift(world)
        beliefs = superstitions = 0
        heard = heard_super = 0
        believers: Counter = Counter()
        false_springs = springs = 0
        for q in living:
            for key, v in q.beliefs.items():
                if v >= 0.15:
                    beliefs += 1
                    if superstitious(key):
                        superstitions += 1
                        believers[key] += 1
            for hkey, hv in q.heard.items():
                if hkey.startswith("b:") and hv[0] >= 0.15:
                    heard += 1
                    if superstitious(hkey[2:]):
                        heard_super += 1
            for spot in q.springs:
                springs += 1
                if fresh_near(world, tuple(spot), 1) is None:
                    false_springs += 1
        top = believers.most_common(1)
        return {"stories_heard": stories["heard"], "stories_wrong": stories["wrong"],
                "stories_by_hops": stories["by_hops"], "myths_ever": len(self.h.myths),
                "beliefs": beliefs, "superstitions": superstitions,
                "widest_superstition": [top[0][0], top[0][1]] if top else None,
                "hearsay": heard, "hearsay_superstitions": heard_super,
                "water_believed": springs, "water_believed_wrongly": false_springs}

    def _inventions(self, world) -> dict:
        classes = sorted({c for rec in self.techniques.values() for c in rec["classes"]})
        return {"techniques_ever": len(world.knowledge), "classes_ever": classes,
                "named_firsts": sorted(k for k in self.h.firsts if k in CLASSES)}

    def _technique_survival(self, world, tick: int, living: list) -> dict:
        holders: dict = {}
        gens: dict = {}
        for q in living:
            for sig in q.recipes:
                holders[sig] = holders.get(sig, 0) + 1
                gens[sig] = max(gens.get(sig, 0), q.generation)
        for sig, k in holders.items():
            rec = self.techniques.get(sig)
            if rec is None:          # learned as a variant before anyone made it
                continue
            rec["holders_max"] = max(rec["holders_max"], k)
            rec["last_known"] = tick
            rec["years_known"] += 1
            rec["gen_span"] = max(rec["gen_span"], gens[sig] - rec["gen"])
        alive = [s for s in holders if s in self.techniques]
        lost_now = sum(1 for s, r in self.techniques.items() if s not in holders)
        classes_known = sorted({c for s in holders for c in classify(world.knowledge.get(s, {}).get("props"))})
        return {"known_now": len(holders), "known_by_2plus": sum(1 for k in holders.values() if k >= 2),
                "widest": max(holders.values(), default=0), "not_known_now": lost_now,
                "lost_events_ever": sum(len(r["lost"]) for r in self.techniques.values()),
                "found_again_ever": sum(len(r["found_again"]) for r in self.techniques.values()),
                "crossed_2_generations": sum(1 for s in alive if self.techniques[s]["gen_span"] >= 2),
                "classes_known": classes_known}

    def _trust(self, world, living: list) -> dict:
        ids = {q.id for q in living}
        island = self._islands(world)
        vals = []
        strong = []
        weak_neg = 0
        in_trust: dict = {}
        for q in living:
            for pid, r in q.rel.items():
                if pid not in ids:
                    continue
                vals.append(r.trust)
                in_trust.setdefault(pid, []).append(r.trust)
                if r.trust >= 0.5:
                    strong.append((q.id, pid))
                if r.trust <= -0.2:
                    weak_neg += 1
        strong_set = set(strong)
        mutual = sum(1 for a, b in strong if (b, a) in strong_set) // 2
        # clusters of mutual-or-one-way strong trust
        parent = {q.id: q.id for q in living}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for a, b in strong:
            parent[find(a)] = find(b)
        sizes = Counter(find(q.id) for q in living)
        loc = {q.id: q.loc for q in living}
        cross = sum(1 for a, b in strong if island.get(loc[a], -1) != island.get(loc[b], -2))
        hubs = sum(1 for pid, ts in in_trust.items() if sum(1 for t in ts if t >= 0.5) >= 5)
        # Are people who turned out right trusted more?
        xs, ys = [], []
        for q in living:
            rec = self.sources.get(q.id)
            if rec and rec[0] + rec[1] >= 2 and q.id in in_trust:
                xs.append(rec[0] / (rec[0] + rec[1]))
                ys.append(sum(in_trust[q.id]) / len(in_trust[q.id]))
        self.accuracy_pairs = [[round(x, 3), round(y, 3)] for x, y in zip(xs, ys)]
        # Do others' records of a person track how often that person is really right?
        rx, ry = [], []
        experts = 0
        for q in living:
            rec = self.sources.get(q.id)
            ests = []
            for o in living:
                r_ = o.records.get(q.id) if o is not q else None
                if r_ and r_[0] + r_[1] >= 1:
                    ests.append((r_[0] + 1.0) / (r_[0] + r_[1] + 2.0))
            if sum(1 for e_ in ests if e_ >= 0.75) >= 5:
                experts += 1
            if rec and rec[0] + rec[1] >= 4 and ests:
                rx.append(rec[0] / (rec[0] + rec[1]))
                ry.append(sum(ests) / len(ests))
        self.record_pairs = [[round(x, 3), round(y, 3)] for x, y in zip(rx, ry)]
        n = len(living)
        return {"ties": len(vals), "mean_trust": round(sum(vals) / len(vals), 3) if vals else None,
                "distrust_ties": weak_neg, "strong_ties": len(strong), "mutual_strong": mutual,
                "strong_per_person": round(len(strong) / n, 2) if n else 0,
                "largest_cluster_share": round(max(sizes.values()) / n, 3) if n else 0,
                "clusters": sum(1 for s in sizes.values() if s >= 3),
                "cross_island_strong": cross, "trusted_hubs": hubs,
                "accuracy_vs_trust_r": _pearson(xs, ys), "sources_measured": len(xs),
                "accuracy_vs_record_r": _pearson(rx, ry), "record_measured": len(rx), "experts": experts,
                "rafts_known": sum(1 for q in living if any(
                    (world.knowledge.get(sig, {}).get("props") or {}).get("float", 0) >= 65 for sig in q.recipes)),
                "rafts_carried": sum(1 for q in living if any(it.get("float", 0) >= 65 for it in q.items))}

    def _surprise(self, living: list) -> dict:
        open_now = sum(len(q.puzzles) for q in living)
        focused = sum(1 for q in living if q.thoughts and q.thoughts[0][0] == "puzzle")
        return {"open_puzzles": open_now, "minds_on_a_puzzle": focused,
                "ended_all_time": dict(self.puzzle_ends)}

    # --- the end ---------------------------------------------------------------------------------

    def summary(self, world) -> dict:
        tests = self.puzzle_tests
        techs = self.techniques
        life = [(r["last_known"] - r["first"]) / WEEKS_PER_YEAR for r in techs.values()]
        widely = [r for r in techs.values() if r["holders_max"] >= 3]
        syms = self.symbols.values()
        return {
            "techniques": len(techs),
            "techniques_from_puzzles": sum(1 for r in techs.values() if r["puzzled"]),
            "technique_life_years": {
                "median": round(sorted(life)[len(life) // 2], 1) if life else 0,
                "max": round(max(life), 1) if life else 0,
                "over_10": sum(1 for x in life if x >= 10), "over_50": sum(1 for x in life if x >= 50)},
            "techniques_ever_held_by_3plus": len(widely),
            "techniques_crossing_2_generations": sum(1 for r in techs.values() if r["gen_span"] >= 2),
            "techniques_lost_ever": sum(1 for r in techs.values() if r["lost"]),
            "techniques_found_again": sum(1 for r in techs.values() if r["found_again"]),
            "classes_invented": sorted({c for r in techs.values() for c in r["classes"]}),
            "puzzles_ended": dict(self.puzzle_ends),
            "puzzle_tests": {"mean": round(sum(tests) / len(tests), 2) if tests else 0,
                             "share_tested": round(sum(1 for t in tests if t) / len(tests), 3) if tests else 0,
                             "share_3plus": round(sum(1 for t in tests if t >= 3) / len(tests), 3) if tests else 0},
            "symbols_ever": len(self.symbols),
            "symbols_lasting_5y": sum(1 for s in syms if s["years"] >= 5),
            "symbols_lasting_20y": sum(1 for s in syms if s["years"] >= 20),
            "symbols_reaching_younger": sum(1 for s in syms if s["younger"]),
            "symbols_across_islands": sum(1 for s in syms if s["islands"] >= 2),
            "longest_symbol": max(([k, s["years"]] for k, s in self.symbols.items()), key=lambda x: x[1], default=None),
            "sources_tracked": len(self.sources),
            "accuracy_trust_pairs": self.accuracy_pairs,
            "accuracy_record_pairs": self.record_pairs,
            "accuracy_sequences": {k: v for k, v in self.seq.items() if len(v) >= 4},
        }
