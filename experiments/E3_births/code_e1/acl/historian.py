"""The historian watches and writes things down. It never tells anyone what to do.

It reads each week's events and, once a year, looks at the whole world to spot
patterns nobody programmed: bands of people who live and stay together,
leaders whom others look up to, pairs who keep trading gifts, revenge and
feuds, settlements, famines, and know-how spreading or dying out.

It also recognises inventions. The people only ever make "flint struck with
stone" or "two fibers tied with a third"; the historian looks at what the thing
can do (its edge, reach, hardness, how it holds and how it warms) and calls it
a blade, a spear, a carrier. In the same way it recognises the first fire made
by hand, the first heap of things big enough to live in, the first harvest from
seeds left in the ground. These names are for us. The people never see them.

It keeps the truth of what happened, so it can see how stories drift as they
are retold (Laws 26, 80): which versions people now believe, and when many share
a version that is false. It notices people going back to test something again
and again (Law 75), claims that turned out right or wrong, and marks that come
to mean the same thing to many people, or drift (Laws 22, 23). It only ever
reads.
"""
from __future__ import annotations

import math
from collections import Counter

from . import marks as marks_
from .config import CHILD_END, TEEN_END, WEEKS_PER_YEAR
from .matter import MATERIALS, pile_warmth
from .person import ACTIONS
from .util import distance

# What the historian calls a made thing, judged only by its properties.
CLASSES = {
    "spear": ("a spear", "a sharp point on a long shaft"),
    "blade": ("a blade", "a sharp edge"),
    "club": ("a club", "something heavy on a handle"),
    "carrier": ("a carrier", "something to carry things in"),
    "wrap": ("a wrap", "something warm to wear"),
    "boat": ("a raft", "something that floats and carries someone across water"),
}
PRACTICES = {
    "sowing": ("seeds",),
    "building": ("wood", "stone", "fiber", "hide", "bone"),
    "storing": ("food",),
}


def classify(props: dict | None) -> list[str]:
    if not props:
        return []
    e, r, h, c, w = props["edge"], props["reach"], props["hard"], props["contain"], props["warm"]
    out = []
    if e >= 0.5 and r >= 0.6:
        out.append("spear")
    elif e >= 0.55:
        out.append("blade")
    if h >= 0.6 and r >= 0.55 and e < 0.5:
        out.append("club")
    if c >= 0.6:
        out.append("carrier")
    if w >= 0.6:
        out.append("wrap")
    if props.get("float", 0.0) >= 0.65:
        out.append("boat")
    return out


def describe(recipe: dict, world) -> str:
    if recipe["verb"] == "strike":
        return f"struck {recipe['target']} with {recipe['tool']}"
    parts = []
    for part in recipe["parts"]:
        if part in MATERIALS:
            parts.append(part)
        else:
            cls = classify(world.knowledge.get(part, {}).get("props"))
            if cls:
                parts.append(CLASSES[cls[0]][0])
            elif "/" in part and not part.startswith("("):
                parts.append(f"a {part.split('/')[0]} flake")
            else:
                parts.append("a bundle they had tied")
    return f"tied {parts[0]} and {parts[1]} together with {recipe['binder']}"

ERA_YEARS = 25


class Historian:
    def __init__(self):
        self.chronicle: list[dict] = []       # {"t", "year", "kind", "text"}
        self.years: list[dict] = []           # one row of statistics per year
        self.year_counts: Counter = Counter()
        self.action_counts: Counter = Counter()
        self.harms: list[list] = []           # [tick, actor, victim, kind, depth, eid]
        self.revenge_acts = 0
        self.feuds: list[dict] = []
        self.gifts: dict[str, list] = {}      # "a|b" -> [a->b count, b->a count, last tick]
        self.partnerships: list[str] = []
        self.bands: list[dict] = []           # current bands: {"id", "members", "leader", "name"}
        self.next_band = 1
        self.bands_formed = 0
        self.band_history: list[dict] = []
        self.settlements: dict[str, dict] = {}
        self.firsts: dict[str, int] = {}
        self.lost_classes: dict[str, int] = {}
        self.milestones: list[int] = []
        self.max_generation = 0
        self.notable: dict[int, str] = {}     # event id -> one-line description, for oral history
        self.births = 0
        self.deaths: Counter = Counter()
        self.truth: dict[str, list] = {}      # event id -> [story kind, true actor, target]
        self.myths: list[str] = []            # event ids whose false version many share, already written up
        self.tests: dict[str, int] = {}       # "person|what" -> times tested
        self.symbols: dict[str, str] = {}     # mark shape -> the thing it is shared as meaning
        self.symbol_watch: dict[str, list] = {}   # shape -> [thing, years running] not yet written down

    # --- weekly ---------------------------------------------------------------

    def __call__(self, world, events: list[dict]) -> None:
        tick = world.tick - 1          # the week these events happened in
        for p in world.living():
            if p.age(tick) >= 52:
                self.action_counts[p.last_action] += 1
        for e in events:
            handler = getattr(self, "_on_" + e["k"], None)
            if handler:
                handler(world, e)
            self.year_counts[e["k"]] += 1
        if tick % WEEKS_PER_YEAR == WEEKS_PER_YEAR - 1:
            self._year_end(world, tick)

    def _write(self, world, t: int, kind: str, text: str) -> None:
        self.chronicle.append({"t": t, "year": t // WEEKS_PER_YEAR, "kind": kind, "text": text})

    def _name(self, world, pid) -> str:
        q = world.people.get(pid) if pid else None
        return q.name if q else "someone"

    def _first(self, world, key: str, t: int, text: str) -> None:
        if key not in self.firsts:
            self.firsts[key] = t
            self._write(world, t, "first", text)

    # --- event handlers ---------------------------------------------------------

    def _on_play(self, world, e):
        if e.get("thing"):
            self._new_thing(world, e)

    def _on_make(self, world, e):
        self._new_thing(world, e)

    def _new_thing(self, world, e):
        props = {k: e[k] for k in ("edge", "reach", "hard", "contain", "warm", "float") if k in e}
        rec = world.knowledge.get(e["thing"])
        for cls in classify(props):
            name, phrase = CLASSES[cls]
            how = describe(rec["recipe"], world) if rec else "made something"
            who = self._name(world, e["a"])
            if cls not in self.firsts:
                self.firsts[cls] = e["t"]
                self._write(world, e["t"], "invention",
                            f"{who} {how} and was left with {phrase}: the first {name[2:]}.")
            elif cls in self.lost_classes:
                lost_at = self.lost_classes.pop(cls)
                self._write(world, e["t"], "invention",
                            f"{who} {how}: {name} again, a skill lost since year {lost_at // WEEKS_PER_YEAR}.")

    def _on_knowledge_lost(self, world, e):
        rec = world.knowledge.get(e["thing"], {})
        for cls in classify(rec.get("props")):
            if cls in self.lost_classes:
                continue
            # Only a skill that had spread counts as lost; one person's half-remembered trick does not.
            if not self.years or self.years[-1]["know"].get(cls, 0) < 2:
                continue
            still = any(cls in classify(world.knowledge.get(sig, {}).get("props"))
                        for q in world.living() for sig in q.recipes)
            if not still:
                self.lost_classes[cls] = e["t"]
                self._write(world, e["t"], "loss",
                            f"Nobody alive remembers how to make {CLASSES[cls][0]} any more. The skill was lost.")

    def _on_fire(self, world, e):
        if e.get("how") == "sparks":
            self._first(world, "fire", e["t"],
                        f"{self._name(world, e['a'])} struck flint where dry things lay, and they caught: "
                        f"the first fire made by people.")

    def _on_put(self, world, e):
        who = self._name(world, e["a"])
        on_purpose = e.get("belief", 0) >= 0.2
        if on_purpose and e["thing"] == "seeds" and e.get("into") == "ground":
            self._first(world, "farming", e["t"],
                        f"{who} buried seed on purpose, having seen it come back as food: the beginning of farming.")
        if on_purpose and e["thing"] == "food":
            self._first(world, "storing", e["t"],
                        f"{who} set food aside on purpose, having found it there when it was needed before: "
                        f"the beginning of keeping stores.")
        if e.get("into") == "fire":
            self._first(world, "kept_fire", e["t"], f"{who} fed wood to a fire to keep it going: the first kept fire.")
        if e.get("warmth", 0) >= 0.2 and "dwelling" not in self.firsts:
            t = world.tile(tuple(e["at"]))
            top = max(t.builders, key=lambda pid: (t.builders[pid], pid)) if t.builders else e["a"]
            self._first(world, "dwelling", e["t"],
                        f"At ({e['at'][0]}, {e['at'][1]}) the heap of things people had left grew big enough to "
                        f"keep out a fifth of the winter cold: the first dwelling. "
                        f"{self._name(world, top)} had put in the most.")

    def _on_harvest(self, world, e):
        self._first(world, "field", e["t"],
                    f"{self._name(world, e['a'])} gathered food that had grown where seeds had been dropped: "
                    f"the first harvest from seed left in the ground.")

    def _on_take(self, world, e):
        if e.get("own") and e.get("weeks", 0) >= 4:
            self._first(world, "store", e["t"],
                        f"{self._name(world, e['a'])} came back for food left {e['weeks']} weeks before, "
                        f"and it was still there.")

    def _on_birth(self, world, e):
        self.births += 1
        gen = e["generation"]
        if gen > self.max_generation:
            self.max_generation = gen
            if gen >= 2:
                mother = self._name(world, e["a"])
                child = "daughter" if world.people[e["b"]].sex == "F" else "son"
                self._write(world, e["t"], "generation",
                            f"{e['name']}, {child} of {mother}, was the first of generation {gen}.")

    def _true(self, e, kind, actor, target) -> None:
        self.truth[str(e["id"])] = [kind, actor or "", target or ""]

    def _on_told(self, world, e):
        self.year_counts["heard_" + str(e.get("heard") or "")] += 1

    def _on_mauled(self, world, e):
        self._true(e, "mauled", "animal:" + e.get("animal", ""), e.get("b"))
        if not e.get("killed"):
            beast = "a bear" if e.get("animal") == "bear" else "wolves"
            self._first(world, "mauled", e["t"], f"{self._name(world, e.get('b'))} survived an attack by {beast}.")

    def _on_drought(self, world, e):
        self._write(world, e["t"], "weather", "A dry year began: little rain, thin growth.")

    def _on_hard_winter(self, world, e):
        self._write(world, e["t"], "weather", "A hard winter set in.")

    def _on_flood(self, world, e):
        self._write(world, e["t"], "weather", "The rivers flooded their banks.")

    def _on_drank_sea(self, world, e):
        if e.get("first"):
            self._first(world, "salt", e["t"], f"{self._name(world, e.get('a'))} drank from the sea "
                        "and it did not quench their thirst.")

    def _on_puzzled(self, world, e):
        about = e.get("about", "")
        if about.startswith("f:"):
            self._first(world, "puzzled_fire", e["t"], f"{self._name(world, e.get('a'))} struck "
                        f"{_strike_words(about[2:])} and stared at what happened.")

    def _on_tested(self, world, e):
        key = f"{e.get('a')}|{e.get('about')}"
        n = self.tests.get(key, 0) + 1
        self.tests[key] = n
        if n == 3:
            about = e.get("about", "")
            if about.startswith("f:"):
                what = f"striking {_strike_words(about[2:])}"
            elif about.startswith("m:"):
                what = "a thing they had made"
            elif about.startswith("k:"):
                what = "a mark they had seen"
            else:
                what = "what they had left in one spot"
            self._first(world, "testing", e["t"], f"{self._name(world, e.get('a'))} went back to {what} "
                        "a third time, to see it happen again: the first deliberate testing.")

    def _on_refuted(self, world, e):
        by = (e.get("by") or [None])[0]
        if by and by.startswith("mark:"):
            self._first(world, "refuted_mark", e["t"], f"{self._name(world, e.get('a'))} found that what the "
                        f"mark <{by[5:]}> seemed to say was wrong, and put less faith in that mark.")
            return
        self._first(world, "refuted", e["t"], f"{self._name(world, e.get('a'))} found that what "
                    f"{self._name(world, by)} had told them was wrong, and trusted them less for it.")

    def _on_crossed(self, world, e):
        self._first(world, f"crossed:{min(e['from'], e['to'])}-{max(e['from'], e['to'])}", e["t"],
                    f"{self._name(world, e.get('a'))} crossed open water on something that floats and came ashore "
                    f"on land nobody could walk to from where they set out.")

    def _on_read(self, world, e):
        self._first(world, "read", e["t"], f"{self._name(world, e.get('a'))} came on the mark <{e.get('shape')}> "
                    f"and took it to mean {self._thing_words(world, e.get('means', ''))}: the first mark read as a message.")

    def _on_learn(self, world, e):
        if e.get("how") != "read" or not e.get("thing"):
            return
        rec = world.knowledge.get(e["thing"])
        if rec is not None and not rec.get("alive", True):
            self._write(world, e["t"], "record",
                        f"{self._name(world, e.get('a'))} learned to strike {_strike_words(e['thing'])} "
                        "from a mark, though nobody alive knew how: a skill recovered from a record.")
        self._first(world, "learned_from_mark", e["t"], f"{self._name(world, e.get('a'))} took up "
                    f"striking {_strike_words(e['thing'])} from a mark: the first thing learned from a record.")

    def _on_vouched(self, world, e):
        if e.get("good"):
            self._first(world, "vouched", e["t"], f"{self._name(world, e.get('a'))} told {self._name(world, e.get('b'))} "
                        f"that {self._source(world, e.get('about'))} could be believed: reputation passed on by word.")

    def _source(self, world, src) -> str:
        if src and src.startswith("mark:"):
            return f"the mark <{src[5:]}>"
        return self._name(world, src) if src in world.people else "someone"

    def _on_mark(self, world, e):
        on = {"rock": "rock", "wood": "wood"}.get(e.get("on"), "the ground")
        self._first(world, "mark", e["t"], f"{self._name(world, e.get('a'))} scratched a mark "
                    f"<{e.get('shape')}> into {on}.")

    def _on_death(self, world, e):
        self.deaths[e["cause"]] += 1
        if e["cause"] != "killed":
            self._true(e, "died", None, e.get("a"))
        p = world.people[e["a"]]
        if e["cause"] == "killed":
            return  # described by the kill event
        if p.generation == 0 and e["cause"] == "old age":
            living_founders = sum(1 for q in world.living() if q.generation == 0)
            if living_founders == 0:
                self._write(world, e["t"], "death",
                            f"{p.name}, the last of the founders, died at {e['age']:.0f}.")

    def _on_taken_in(self, world, e):
        if e.get("by") == "adoption":
            self._first(world, "adoption", e["t"],
                        f"{self._name(world, e['a'])} took in the orphan {self._name(world, e['b'])}, "
                        f"no relation, the first time a stranger raised another's child.")

    def _on_give(self, world, e):
        a, b = e["a"], e["b"]
        key, flip = (f"{a}|{b}", False) if a < b else (f"{b}|{a}", True)
        rec = self.gifts.setdefault(key, [0, 0, e["t"]])
        if e["t"] - rec[2] > 3 * WEEKS_PER_YEAR:
            rec[0] = rec[1] = 0
        rec[1 if flip else 0] += 1
        rec[2] = e["t"]
        if key in self.partnerships or rec[0] < 3 or rec[1] < 3:
            return
        pa, pb = world.people[a], world.people[b]
        if world.kinship(pa, pb) > 0 or pa.partner == b:
            return
        self.partnerships.append(key)
        n = len(self.partnerships)
        if n <= 5 or n in (10, 25, 50, 100, 250):
            what = "the first lasting exchange" if n == 1 else f"exchange partnership number {n}"
            self._write(world, e["t"], "exchange",
                        f"{pa.name} and {pb.name}, not related, had been trading food back and forth "
                        f"for years: {what} between unrelated people.")

    def _on_steal(self, world, e):
        if e.get("noticed"):
            self._true(e, "stole", e.get("a"), e.get("b"))
        self._note_steal(world, e)

    def _note_steal(self, world, e):
        if e.get("stash"):
            self._first(world, "store_theft", e["t"],
                        f"{self._name(world, e['a'])} took food that {self._name(world, e.get('b'))} had left, "
                        f"and was seen: the first theft from a store.")
        if e.get("noticed"):
            self.harms.append([e["t"], e["a"], e["b"], "stole", self._depth(world, e), e["id"]])

    def _on_attack(self, world, e):
        self._true(e, "attacked", e.get("a"), e.get("b"))
        self._note_attack(world, e)

    def _note_attack(self, world, e):
        depth = self._depth(world, e)
        self.harms.append([e["t"], e["a"], e["b"], "attacked", depth, e["id"]])
        if depth > 0:
            self.revenge_acts += 1
        self._first(world, "violence", e["t"],
                    f"{self._name(world, e['a'])} attacked {self._name(world, e['b'])}: the first violence.")

    def _on_kill(self, world, e):
        self._true(e, "killed", e.get("a"), e.get("b"))
        self._note_kill(world, e)

    def _note_kill(self, world, e):
        depth = self._depth(world, e)
        self.harms.append([e["t"], e["a"], e["b"], "killed", depth, e["id"]])
        killer, victim = self._name(world, e["a"]), self._name(world, e["b"])
        self.notable[e["id"]] = f"the killing of {victim} by {killer} in year {e['t'] // 52}"
        if depth > 0:
            self.revenge_acts += 1
            reason = self._reason
            self._write(world, e["t"], "revenge", f"{killer} killed {victim} {reason}.")
            if depth >= 2:
                self._note_feud(world, e)
        else:
            self._write(world, e["t"], "killing", f"{killer} killed {victim}.")

    def _depth(self, world, e) -> int:
        """Was this harm payback for an earlier one against the attacker or their family?"""
        a, b = world.people[e["a"]], world.people[e["b"]]
        self._reason = ""
        for h in reversed(self.harms):
            if e["t"] - h[0] > 30 * WEEKS_PER_YEAR:
                break
            past_actor, past_victim = world.people[h[1]], world.people[h[2]]
            actor_matches = past_actor.id == b.id or world.kinship(past_actor, b) >= 0.8
            victim_close = (past_victim.id == a.id or world.kinship(past_victim, a) >= 0.8
                            or a.partner == past_victim.id)
            if actor_matches and victim_close:
                did = {"killed": "killed", "attacked": "attacked", "stole": "robbed"}[h[3]]
                if past_victim.id == a.id:
                    self._reason = f"after being {did} by {past_actor.name} in year {h[0] // 52}"
                else:
                    self._reason = (f"in revenge for {past_victim.name}, {did} by {past_actor.name} "
                                    f"in year {h[0] // 52}")
                return h[4] + 1
        return 0

    def _note_feud(self, world, e):
        a, b = world.people[e["a"]], world.people[e["b"]]
        for f in self.feuds:
            if {a.id, b.id} & set(f["people"]):
                f["people"] = sorted(set(f["people"]) | {a.id, b.id})
                f["acts"] += 1
                f["last"] = e["t"]
                return
        self.feuds.append({"start": e["t"], "last": e["t"], "people": sorted({a.id, b.id}), "acts": 1,
                           "name": f"the feud between the kin of {a.name} and the kin of {b.name}"})
        self._write(world, e["t"], "feud",
                    f"Revenge answered revenge: {self.feuds[-1]['name']} had begun.")

    # --- yearly -------------------------------------------------------------------

    def _year_end(self, world, tick: int) -> None:
        year = tick // WEEKS_PER_YEAR
        living = world.living()
        n = len(living)
        c = world.cfg
        counts = self.year_counts
        self.year_counts = Counter()
        deaths_by_cause = Counter()
        for p in world.people.values():
            if not p.alive and p.death_tick is not None and p.death_tick // WEEKS_PER_YEAR == year:
                deaths_by_cause[p.death_cause] += 1
        dwellings = fields = fires = stores = 0
        for row_ in world.tiles:
            for t in row_:
                if t.pile and pile_warmth(t.pile) >= 0.2:
                    dwellings += 1
                if t.crop >= 5:
                    fields += 1
                if t.fire > 0:
                    fires += 1
                stores += len(t.stash)
        know = {cls: 0 for cls in CLASSES}
        practice = {k: 0 for k in PRACTICES}
        for p in living:
            have = []
            for sig in p.recipes:
                for cls in classify(world.knowledge.get(sig, {}).get("props")):
                    if cls not in have:
                        have.append(cls)
            for cls in have:
                know[cls] += 1
            for k, things in PRACTICES.items():
                if any(p.beliefs.get(f"{thing}@{s_}", 0.0) >= 0.1 for thing in things for s_ in range(4)):
                    practice[k] += 1
        row = {
            "year": year,
            "population": n,
            "births": counts["birth"],
            "deaths": sum(deaths_by_cause.values()),
            "deaths_by_cause": dict(deaths_by_cause),
            "mood": round(sum(p.mood for p in living) / n, 3) if n else 0.0,
            "health": round(sum(p.health for p in living) / n, 1) if n else 0.0,
            "generation": max((p.generation for p in living), default=0),
            "pairs": sum(1 for p in living if p.partner) // 2,
            "children": sum(1 for p in living if p.age(tick) < TEEN_END),
            "know": know,
            "practice": practice,
            "dwellings": dwellings,
            "fields": fields,
            "fires": fires,
            "stores": stores,
            "gifts": counts["give"],
            "thefts": counts["steal"],
            "attacks": counts["attack"] + counts["kill"],
            "killings": counts["kill"],
            "stories_told": counts["told"],
            "weather": world.weather,
            "wet": world.sky.get("wet", 1.0),
            "stories": self._story_drift(world),
            "heard": {k[6:]: v for k, v in counts.items() if k.startswith("heard_")},
            "verified": counts["verified"],
            "refuted": counts["refuted"],
            "puzzles": counts["puzzled"],
            "tests": counts["tested"],
            "marks_made": counts["mark"],
            "symbols": len(marks_.shared(world)),
        }
        self.years.append(row)
        self._find_myths(world, tick)
        self._find_symbols(world, tick)
        remembered = {str(m.eid) for p in living for m in p.memories}
        self.truth = {k: v for k, v in self.truth.items() if k in remembered}
        thirst = deaths_by_cause.get("thirst", 0)
        if thirst >= max(3, 0.06 * (n + thirst)):
            self._write(world, tick, "drought", f"A thirsty year: {thirst} people died for want of water.")

        starved = deaths_by_cause.get("starvation", 0)
        if starved >= max(3, 0.06 * (n + starved)):
            self._write(world, tick, "famine",
                        f"A hungry year: {starved} people starved"
                        + (" after a poor growing season." if world.weather < 0.85 else "."))
        for m in (50, 100, 200, 500, 1000):
            if n >= m and m not in self.milestones:
                self.milestones.append(m)
                self._write(world, tick, "population", f"The population reached {m}.")
        self._find_bands(world, tick)
        self._find_settlements(world, tick)
        if (year + 1) % ERA_YEARS == 0:
            self._write(world, tick, "era", self.era_summary(world, year + 1 - ERA_YEARS, year))

    def _story_drift(self, world) -> dict:
        """How faithful the stories people now hold are, by how many tellings they passed through."""
        held = wrong = 0
        by_hops: dict = {}
        for p in world.living():
            for m in p.memories:
                t = self.truth.get(str(m.eid))
                if t is None or not m.source or t[1] == "":
                    continue
                held += 1
                bad = (m.actor or "") != t[1]
                wrong += bad
                b = by_hops.setdefault(str(min(m.hops, 4)), [0, 0])
                b[0] += 1
                b[1] += bad
        return {"heard": held, "wrong": wrong, "by_hops": by_hops}

    def _find_myths(self, world, tick: int) -> None:
        """A false version of an event that several living people now share."""
        versions: dict = {}
        for p in world.living():
            for m in p.memories:
                t = self.truth.get(str(m.eid))
                if t is None or not t[1] or (m.actor or "") == t[1]:
                    continue
                versions.setdefault((m.eid, m.actor or ""), []).append(p.id)
        for (eid, actor), holders in sorted(versions.items()):
            if len(holders) < 3 or str(eid) in self.myths:
                continue
            self.myths.append(str(eid))
            kind, true_actor, target = self.truth[str(eid)]
            verb = {"killed": "killed", "attacked": "attacked", "stole": "stole from",
                    "mauled": "mauled"}.get(kind, kind)
            self._write(world, tick, "myth",
                        f"{len(holders)} people now tell that {self._who(world, actor)} {verb} "
                        f"{self._name(world, target)}. It was {self._who(world, true_actor)}. "
                        "The story changed as it was passed on.")

    def _who(self, world, actor: str) -> str:
        if actor.startswith("animal:"):
            return {"wolf": "wolves", "bear": "a bear"}.get(actor[7:], actor[7:])
        return self._name(world, actor) if actor in world.people else "someone"

    def _find_symbols(self, world, tick: int) -> None:
        """Marks that many people take to go with the same thing, and marks whose sense has moved.
        Only what has held for two years running is written down; a sense is only called changed
        once the old one has all but gone."""
        loose = {(s_, k) for s_, k, _ in marks_.shared(world, min_people=2)}
        best: dict = {}
        for shape, thing, n in marks_.shared(world):
            if shape not in best or n > best[shape][1]:
                best[shape] = (thing, n)
        watch = {}
        for shape, (thing, n) in sorted(best.items()):
            prev = self.symbol_watch.get(shape)
            years = prev[1] + 1 if prev and prev[0] == thing else 1
            watch[shape] = [thing, years]
            if years < 2:
                continue
            before = self.symbols.get(shape)
            words = self._thing_words(world, thing)
            if before is None:
                self._write(world, tick, "symbol",
                            f"{n} people now take the mark <{shape}> to go with {words}, and have for two years. "
                            "Nobody decided this; it grew from where the mark was made and seen.")
                self.symbols[shape] = thing
            elif before != thing and (shape, before) not in loose:
                self._write(world, tick, "symbol",
                            f"The mark <{shape}> has drifted: it went with {self._thing_words(world, before)}, "
                            f"and now, for {n} people, with {words}.")
                self.symbols[shape] = thing
        self.symbol_watch = watch

    def _thing_words(self, world, thing: str) -> str:
        if thing.startswith("p:"):
            return self._name(world, thing[2:]) if thing[2:] in world.people else "someone long gone"
        if thing.startswith("sown@"):
            return "seed sown in " + ("spring", "summer", "autumn", "winter")[int(thing[5:])]
        if thing.startswith("struck:"):
            return f"{thing[7:]} being struck"
        if thing.startswith("bones:"):
            return f"{thing[6:]} killed"
        return {"food": "food set down", "plants": "growing food", "fire": "fire", "water": "water",
                "shelter": "shelter", "grave": "a grave", "rabbit": "rabbits", "deer": "deer",
                "bison": "bison", "wolf": "wolves", "bear": "bears", "ash": "the ashes of a fire"}.get(thing, thing)

    def _find_bands(self, world, tick: int) -> None:
        """Bands: people who like each other and live near each other."""
        c = world.cfg
        grown = [p for p in world.living() if p.age(tick) >= CHILD_END]
        index = {p.id: i for i, p in enumerate(grown)}
        parent = list(range(len(grown)))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        for p in grown:
            for qid, r in p.rel.items():
                j = index.get(qid)
                if j is None or r.affection < 0.25:
                    continue
                q = grown[j]
                back = q.rel.get(p.id)
                if back and back.affection >= 0.25 and distance(p.loc, q.loc, c.width, c.height) <= 2 * c.camp_radius:
                    a, b = find(index[p.id]), find(j)
                    if a != b:
                        parent[max(a, b)] = min(a, b)
        groups: dict[int, list] = {}
        for p in grown:
            groups.setdefault(find(index[p.id]), []).append(p.id)
        found = [sorted(m) for m in groups.values() if len(m) >= 3]
        found.sort(key=lambda m: m[0])

        # Match this year's groups to last year's. A band is announced only once it
        # has lasted two years, and declared gone only after two years missing, so
        # the chronicle records lasting bands rather than week-to-week shuffling.
        new_bands = []
        used_prev = Counter()
        for members in found:
            best, best_overlap = None, 0.0
            for b in self.bands:
                inter = len(set(members) & set(b["members"]))
                overlap = inter / len(set(members) | set(b["members"]))
                if overlap > best_overlap:
                    best, best_overlap = b, overlap
            leader = _leader(world, members)
            if best is not None and best_overlap >= 0.3:
                used_prev[best["id"]] += 1
                if used_prev[best["id"]] == 1:
                    band = dict(best, members=members, leader=leader, missing=0, age=best["age"] + 1)
                    if band["age"] == 1 and not band["announced"]:
                        band["announced"] = True
                        self.bands_formed += 1
                        self._write(world, tick, "band",
                                    f"{_cap(band['name'])} had formed: {len(members)} grown people who "
                                    f"lived near each other and cared for one another.")
                    elif (band["announced"] and leader != best["leader"]
                          and world.people[leader].name not in band["name"]
                          and _respect_for(world, leader, members) >= 1.0):
                        self._write(world, tick, "leader",
                                    f"{world.people[leader].name} became the most respected person in {band['name']}.")
                else:
                    band = {"id": self._new_band_id(), "members": members, "leader": leader,
                            "name": f"the band of {world.people[leader].name}", "founded": tick,
                            "age": 0, "missing": 0, "announced": best["announced"]}
                    if best["announced"]:
                        self.bands_formed += 1
                        self._write(world, tick, "band",
                                    f"{_cap(best['name'])} split; {band['name']} went its own way "
                                    f"with {len(members)} grown members.")
            else:
                band = {"id": self._new_band_id(), "members": members, "leader": leader,
                        "name": f"the band of {world.people[leader].name}", "founded": tick,
                        "age": 0, "missing": 0, "announced": False}
            new_bands.append(band)
        for b in self.bands:
            if b["id"] in used_prev:
                continue
            b = dict(b, missing=b["missing"] + 1)
            alive = [m for m in b["members"] if world.people[m].alive]
            if b["missing"] < 2 and alive:
                new_bands.append(b)
            elif b["announced"]:
                why = "its people scattered" if alive else "its last members died"
                self._write(world, tick, "band", f"{_cap(b['name'])} was no more: {why}.")
        self.bands = new_bands
        self.band_history.append({"year": tick // WEEKS_PER_YEAR, "bands": [
            {"name": b["name"], "size": len(b["members"]), "leader": world.people[b["leader"]].name}
            for b in new_bands if b["missing"] == 0 and b["announced"]]})

    def _new_band_id(self) -> int:
        self.next_band += 1
        return self.next_band - 1

    def _find_settlements(self, world, tick: int) -> None:
        c = world.cfg
        for row in world.tiles:
            for t in row:
                if not t.pile or pile_warmth(t.pile) < 0.2:
                    continue
                key = f"{t.x},{t.y}"
                residents = len(world.people_near((t.x, t.y), c.camp_radius))
                near_known = any(distance((t.x, t.y), (s["x"], s["y"]), c.width, c.height) <= 3
                                 for s in self.settlements.values())
                if residents >= 4 and not near_known:
                    top = max(t.builders, key=lambda pid: (t.builders[pid], pid)) if t.builders else None
                    sown = any(world.tiles[(t.y + dy) % c.height][(t.x + dx) % c.width].crop >= 5
                               for dy in (-1, 0, 1) for dx in (-1, 0, 1))
                    self.settlements[key] = {"founded": tick, "x": t.x, "y": t.y,
                                             "founder": world.people[top].name if top else None}
                    if len(self.settlements) <= 5:
                        self._write(world, tick, "settlement",
                                    f"A settlement took shape at ({t.x}, {t.y}): a dwelling"
                                    + (", sown ground beside it" if sown else "")
                                    + f", and {residents} people living around it.")

    # --- summaries ------------------------------------------------------------------

    def era_summary(self, world, y0: int, y1: int) -> str:
        rows = [r for r in self.years if y0 <= r["year"] <= y1]
        if not rows:
            return ""
        start = self.years[y0 - 1]["population"] if y0 > 0 and len(self.years) >= y0 else world.cfg.founders
        end = rows[-1]["population"]
        births = sum(r["births"] for r in rows)
        causes = Counter()
        for r in rows:
            causes.update(r["deaths_by_cause"])
        top = ", ".join(f"{k} ({v})" for k, v in causes.most_common(3)) or "none"
        events = [e for e in self.chronicle if y0 <= e["year"] <= y1 and e["kind"] != "era"]
        kinds = Counter(e["kind"] for e in events)
        bits = []
        for k, label in (("invention", "inventions"), ("first", "firsts"), ("loss", "lost skills"),
                         ("revenge", "revenge killings"),
                         ("killing", "killings"), ("famine", "famines"), ("band", "band changes"),
                         ("exchange", "new exchange partnerships"), ("settlement", "new settlements")):
            if kinds.get(k):
                bits.append(f"{kinds[k]} {label}")
        mood = sum(r["mood"] for r in rows) / len(rows)
        return (f"Years {y0}-{y1}: population {start} to {end}, {births} births. "
                f"Deaths mostly from {top}. Average happiness {mood:.2f}. "
                + (("Recorded: " + ", ".join(bits) + ".") if bits else "A quiet age."))

    def oral_history(self, world, top: int = 8) -> list[dict]:
        """Which remembered events are still known by the living, and how long ago they happened."""
        holders: Counter = Counter()
        for p in world.living():
            for m in p.memories:
                if m.eid in self.notable:
                    holders[m.eid] += 1
        out = []
        for eid, count in holders.most_common(top):
            out.append({"event": self.notable[eid], "remembered_by": count})
        return out

    def metrics(self, world) -> dict:
        tick = world.tick
        people = list(world.people.values())
        old_enough = [p for p in people if p.generation > 0 and tick - p.birth >= TEEN_END]
        survived = [p for p in old_enough if p.alive or (p.death_tick - p.birth) >= TEEN_END]
        total_actions = sum(self.action_counts.values())
        entropy = 0.0
        for a in ACTIONS:
            n = self.action_counts.get(a, 0)
            if n:
                f = n / total_actions
                entropy -= f * math.log(f)
        living = world.living()
        last = self.years[-1] if self.years else {"know": {}, "practice": {}}
        n = max(1, len(living))
        know = {k: round(v / n, 3) for k, v in last.get("know", {}).items()}
        practice = {k: round(v / n, 3) for k, v in last.get("practice", {}).items()}
        return {
            "years": tick // WEEKS_PER_YEAR,
            "population_end": len(living),
            "population_peak": max((r["population"] for r in self.years), default=len(living)),
            "births": self.births,
            "max_generation": self.max_generation,
            "child_survival_to_16": round(len(survived) / len(old_enough), 3) if old_enough else None,
            "action_entropy": round(entropy / math.log(len(ACTIONS)), 3),
            "action_counts": dict(self.action_counts.most_common()),
            "deaths_by_cause": dict(self.deaths.most_common()),
            "exchange_partnerships": len(self.partnerships),
            "bands_now": sum(1 for b in self.bands if b["missing"] == 0 and b["announced"]),
            "bands_ever": self.bands_formed,
            "revenge_acts": self.revenge_acts,
            "killings": sum(1 for h in self.harms if h[3] == "killed"),
            "feuds": len(self.feuds),
            "settlements": len(self.settlements),
            "know_spread": know,
            "practice_spread": practice,
            "firsts": {k: v // WEEKS_PER_YEAR for k, v in self.firsts.items()},
            "skills_lost": len(self.lost_classes),
            "kinds_of_things_made": len(world.knowledge),
            "mean_mood": round(sum(r["mood"] for r in self.years) / len(self.years), 3) if self.years else None,
        }

    # --- persistence ------------------------------------------------------------------

    def to_dict(self) -> dict:
        out = {}
        for k, v in self.__dict__.items():
            if k.startswith("_"):
                continue
            if isinstance(v, Counter):
                v = dict(v)
            elif k == "notable":
                v = {str(kk): vv for kk, vv in v.items()}
            out[k] = v
        return out

    @classmethod
    def from_dict(cls, d: dict) -> "Historian":
        h = cls()
        for k, v in d.items():
            if isinstance(getattr(h, k, None), Counter):
                v = Counter(v)
            elif k == "notable":
                v = {int(kk): vv for kk, vv in v.items()}
            setattr(h, k, v)
        return h


def _strike_words(sig: str) -> str:
    target, _, tool = sig.partition("/")
    return f"{target} with {tool}" if tool else sig


def _cap(s: str) -> str:
    return s[:1].upper() + s[1:]


def _respect_for(world, pid: str, members: list) -> float:
    total = 0.0
    for m in members:
        if m != pid:
            r = world.people[m].rel.get(pid)
            if r:
                total += r.respect
    return total


def _leader(world, members: list) -> str:
    return max(members, key=lambda pid: (_respect_for(world, pid, members), pid))
