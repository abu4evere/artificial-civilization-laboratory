"""The world: land that grows and runs out, fire, the passage of weeks, and the people in it.

All randomness comes from one seeded generator owned by the world, and its state
is saved in every snapshot. People act in a seeded shuffled order each week, so
nobody always goes first. Nothing iterates over a set. Together these make a run
fully repeatable: the same seed always produces the same history.
"""
from __future__ import annotations

import hashlib
import json
import random

from . import actions, biology, decision, fauna, geo, marks, weather
from .config import CHILD_END, INFANT_END, SEASONS, WEEKS_PER_SEASON, WEEKS_PER_YEAR, Config
from .matter import best_float, pile_shape
from .person import GENES, SKILLS, Person, Relation
from .util import distance, make_name, step_away, step_toward


class Tile:
    __slots__ = ("x", "y", "biome", "water", "temp", "height", "cost",
                 "fertility", "rock", "forest", "wildness", "flinty",
                 "plants", "wood", "stone", "flint", "fiber",
                 "sown", "crop", "fire", "pile", "builders", "stash", "marks", "traces")

    def __init__(self, x, y, biome, water, temp, height, cost,
                 fertility, rock, forest, wildness, flinty):
        self.x = x
        self.y = y
        self.biome = biome
        self.water = water
        self.temp = temp
        self.height = height
        self.cost = cost
        self.fertility = fertility
        self.rock = rock
        self.forest = forest
        self.wildness = wildness
        self.flinty = flinty
        self.plants = 0.0      # wild plant food
        self.wood = 0.0
        self.stone = 0.0
        self.flint = 0.0
        self.fiber = 0.0
        self.sown = 0.0        # seed lying in the ground
        self.crop = 0.0        # food growing from it
        self.fire = 0.0        # fuel left in a fire burning here
        self.pile: dict[str, float] = {}       # materials people have set down here
        self.builders: dict[str, float] = {}   # who set them down, and how much
        self.stash: list[list] = []            # [owner, food, seeds, tick] food people have set down here
        self.marks: list[list] = []            # [shape, maker, tick, depth, surface] scratched here
        # What doing things here has left behind: turned earth, stone flakes, ash, bones.
        # kind -> [how plain it still is, week it was last added to]
        self.traces: dict[str, list] = {}

    _SAVED = ("biome", "water", "temp", "height", "cost",
              "fertility", "rock", "forest", "wildness", "flinty",
              "plants", "wood", "stone", "flint", "fiber", "sown", "crop", "fire",
              "pile", "builders", "stash", "marks", "traces")

    def to_list(self) -> list:
        return [getattr(self, k) for k in self._SAVED]

    @classmethod
    def from_list(cls, x, y, v: list) -> "Tile":
        t = cls(x, y, *v[:10])
        for k, val in zip(cls._SAVED[10:], v[10:]):
            setattr(t, k, val)
        return t

    def material(self, kind: str) -> float:
        return getattr(self, kind) if kind in ("wood", "stone", "flint", "fiber") else 0.0


# How much of each kind of trace is still plain to see after a week.
TRACE_KEEP = {"sown": 0.97, "struck": 0.995, "ash": 0.95, "bones": 0.97}


def leave_traces_fading(tile) -> None:
    for kind in list(tile.traces):
        rec = tile.traces[kind]
        rec[0] = round(rec[0] * TRACE_KEEP.get(kind.split("@")[0].split(":")[0], 0.95), 4)
        if rec[0] < 0.1:
            del tile.traces[kind]


class World:
    def __init__(self, cfg: Config | None = None, _empty: bool = False):
        self.cfg = cfg or Config()
        self.rng = random.Random(self.cfg.seed)
        self.tick = 0
        self.next_pid = 1
        self.next_eid = 1
        self.next_aid = 1
        self.people: dict[str, Person] = {}
        self.knowledge: dict[str, dict] = {}   # every kind of thing anyone has ever made
        self.animals: list[dict] = []          # each group of animals: {"id", "sp", "n", "x", "y", ...}
        self.herds: dict[tuple, list] = {}     # (x, y) -> the groups standing there
        self.event_chain = "0" * 64
        self.weather = 1.0                    # this year's growing conditions
        # The sky: this year's wetness and winter, and this week's rain, storm and flood.
        self.sky: dict = {"wet": 1.0, "hard": 0.0, "rain": 0, "rained": 0, "roll": 1.0, "storm": None, "flood": 0}
        self.graves: dict[str, int] = {}      # "x,y" -> the week someone last died there
        self.events: list[dict] = []          # this week's events
        self.observers: list = []             # called with (world, events) after each week
        self.hunts: dict[tuple, list] = {}
        self.courting: list = []
        self.plan: dict[str, tuple] = {}      # this week: person -> (where they set out from, their target)
        self.occ: dict[tuple, list] = {}
        self.week_decisions: list = []        # every decision made this week, for read-only observers
        self._island: dict | None = None      # (x, y) -> which landmass; the map never changes
        self._living: list[Person] | None = None
        if not _empty:
            self._make_land()
            fauna.populate(self)
            self._make_founders()

    # --- time -------------------------------------------------------------

    @property
    def year(self) -> int:
        return self.tick // WEEKS_PER_YEAR

    @property
    def week(self) -> int:
        return self.tick % WEEKS_PER_YEAR

    @property
    def season(self) -> int:
        return self.week // WEEKS_PER_SEASON

    @property
    def season_name(self) -> str:
        return SEASONS[self.season]

    # --- creation ---------------------------------------------------------

    def _make_land(self) -> None:
        """Raise the land from seeded noise: oceans, coasts, rivers, lakes and biomes."""
        c = self.cfg
        cells = geo.generate(self.rng, c.width, c.height)
        self.tiles = []
        for y in range(c.height):
            row = []
            for x in range(c.width):
                cell = cells[y][x]
                biome = cell["biome"]
                t = Tile(x, y, biome, biome in geo.WATER, cell["temp"], cell["height"], cell["cost"],
                         cell["fertility"], cell["rock"], cell["forest"], cell["wildness"], cell["flinty"])
                t.plants = c.plant_cap * t.fertility * 0.6
                t.wood = c.wood_cap * t.forest * 0.6
                t.stone = c.stone_cap * t.rock * 0.6
                t.flint = c.flint_cap * 0.6 if t.flinty else 0.0
                t.fiber = c.fiber_cap * t.fertility * 0.6
                row.append(t)
            self.tiles.append(row)

    def _make_founders(self) -> None:
        c = self.cfg
        rng = self.rng
        sexes = ["F", "M"] * (c.founders // 2) + (["F"] if c.founders % 2 else [])
        rng.shuffle(sexes)
        n_groups = max(1, min(4, c.founders // 4))
        # Each band starts on its own island, so they cannot meet until someone
        # works out how to cross the water. If there are not enough islands,
        # later bands settle far apart on the largest one.
        masses = self.landmasses()
        centres = []
        for k in range(n_groups):
            mass = masses[k] if k < len(masses) else masses[0]
            # People come from somewhere livable: fertile ground, near fresh water if the island has any.
            fertile = [t for t in mass if self.tile(t).fertility > 0.4] or mass
            pool = [t for t in fertile if weather.fresh_near(self, t, 3)] or fertile
            for _ in range(200):
                cx, cy = pool[rng.randrange(len(pool))]
                apart = all(max(abs(cx - x), abs(cy - y)) > 6 for x, y in centres)
                if apart:
                    break
            centres.append((cx, cy))
        groups: list[list[Person]] = [[] for _ in range(n_groups)]
        names_taken = []
        for i in range(c.founders):
            g = i % n_groups
            cx, cy = centres[g]
            loc = ((cx + rng.randint(-1, 1)) % c.width, (cy + rng.randint(-1, 1)) % c.height)
            if self.tile(loc).water:
                loc = (cx, cy)
            age_weeks = rng.randint(c.founder_min_age * WEEKS_PER_YEAR, c.founder_max_age * WEEKS_PER_YEAR)
            genes = {gname: round(0.1 + 0.8 * rng.random(), 4) for gname in GENES}
            name = make_name(rng)
            while name in names_taken:
                name = make_name(rng)
            names_taken.append(name)
            p = Person(self._new_pid(), name, sexes[i], -age_weeks, 0, genes, loc)
            p.skills = {s: round(0.2 + 0.2 * rng.random(), 4) for s in SKILLS}
            p.food = c.founder_food
            self.people[p.id] = p
            groups[g].append(p)
        # People who start together grew up together.
        for members in groups:
            for a in members:
                for b in members:
                    if a is not b:
                        a.rel[b.id] = Relation(affection=0.3, trust=0.3, familiarity=0.5)
        self.reindex()

    def _new_pid(self) -> str:
        pid = f"p{self.next_pid:05d}"
        self.next_pid += 1
        return pid

    # --- lookups ----------------------------------------------------------

    def tile(self, loc: tuple) -> Tile:
        return self.tiles[loc[1]][loc[0]]

    def walkable(self, loc: tuple) -> bool:
        """Whether a person can stand here. Sea and lakes cannot be crossed; rivers can be waded."""
        return not self.tile(loc).water

    def boat(self, p) -> float:
        """How well the best thing p carries floats. 0.0 if they have nothing that floats."""
        return best_float(p)[1]

    def passable(self, p, loc: tuple) -> bool:
        """Whether `p` can stand here: land, or water if they carry something that floats."""
        if not self.tile(loc).water:
            return True
        return self.boat(p) >= 0.65

    def island_of(self, loc: tuple):
        """Which stretch of land a tile belongs to (0 is the largest), or None for water."""
        if self._island is None:
            self._island = {}
            for i, comp in enumerate(self.landmasses()):
                for xy in comp:
                    self._island[xy] = i
        return self._island.get(tuple(loc))

    def walk(self, p, src: tuple, dst: tuple) -> tuple:
        """Go from src toward dst one tile at a time. Water stops anyone (or any animal, p=None) with
        nothing that floats. Returns (where they get to, whether they went over water)."""
        c = self.cfg
        here, crossed = tuple(src), self.tile(src).water
        dst = tuple(dst)
        for _ in range(c.width + c.height):
            if here == dst:
                break
            nxt = step_toward(here, dst, 1, c.width, c.height)
            if self.tile(nxt).water:
                if not self._standable(p, nxt):
                    break
                crossed = True
            here = nxt
        return here, crossed

    def landmasses(self) -> list:
        """The walkable land as connected islands (8-adjacency), largest first. Each is a list of (x, y)."""
        c = self.cfg
        seen = set()
        masses = []
        for y in range(c.height):
            for x in range(c.width):
                if (x, y) in seen or not self.walkable((x, y)):
                    continue
                comp, stack = [], [(x, y)]
                seen.add((x, y))
                while stack:
                    cx, cy = stack.pop()
                    comp.append((cx, cy))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            if not (dx or dy):
                                continue
                            n = ((cx + dx) % c.width, (cy + dy) % c.height)
                            if n not in seen and self.walkable(n):
                                seen.add(n)
                                stack.append(n)
                masses.append(comp)
        masses.sort(key=len, reverse=True)
        return masses

    def _standable(self, p, loc: tuple) -> bool:
        return self.passable(p, loc) if p is not None else self.walkable(loc)

    def nearest_land(self, loc: tuple, p=None) -> tuple:
        """The nearest tile `p` can stand on, searching outward in rings."""
        if self._standable(p, loc):
            return loc
        c = self.cfg
        for r in range(1, max(c.width, c.height) + 1):
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    if max(abs(dx), abs(dy)) != r:
                        continue
                    cand = ((loc[0] + dx) % c.width, (loc[1] + dy) % c.height)
                    if self._standable(p, cand):
                        return cand
        return loc

    def step_toward_land(self, src: tuple, dst: tuple, reach: int, p=None) -> tuple:
        """Step up to `reach` tiles toward dst, never ending on water `p` cannot cross."""
        c = self.cfg
        direct = step_toward(src, dst, reach, c.width, c.height)
        if self._standable(p, direct):
            return direct
        best, best_d = None, None
        for dy in range(-reach, reach + 1):
            for dx in range(-reach, reach + 1):
                cand = ((src[0] + dx) % c.width, (src[1] + dy) % c.height)
                if not self._standable(p, cand):
                    continue
                d = distance(cand, dst, c.width, c.height)
                if best is None or d < best_d:
                    best, best_d = cand, d
        return best if best is not None else src

    def step_away_land(self, src: tuple, dst: tuple, reach: int, p=None) -> tuple:
        """Step up to `reach` tiles away from a threat, without ending on water `p` cannot cross."""
        c = self.cfg
        direct = step_away(src, dst, reach, c.width, c.height)
        if self._standable(p, direct):
            return direct
        best, best_d = None, None
        for dy in range(-reach, reach + 1):
            for dx in range(-reach, reach + 1):
                cand = ((src[0] + dx) % c.width, (src[1] + dy) % c.height)
                if not self._standable(p, cand):
                    continue
                d = distance(cand, dst, c.width, c.height)
                if best is None or d > best_d:
                    best, best_d = cand, d
        return best if best is not None else src

    def living(self) -> list[Person]:
        if self._living is None:
            self._living = [p for p in self.people.values() if p.alive]
        return self._living

    def reindex(self) -> None:
        self.occ = {}
        for p in self.living():
            self.occ.setdefault(p.loc, []).append(p.id)

    def move(self, p: Person, dest: tuple) -> None:
        if dest == p.loc:
            return
        here = self.occ.get(p.loc)
        if here and p.id in here:
            here.remove(p.id)
        p.loc = dest
        self.occ.setdefault(dest, []).append(p.id)

    def people_near(self, loc: tuple, radius: int, exclude: str | None = None) -> list[Person]:
        w, h = self.cfg.width, self.cfg.height
        out = []
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                ids = self.occ.get(((loc[0] + dx) % w, (loc[1] + dy) % h))
                if ids:
                    for pid in ids:
                        if pid != exclude:
                            q = self.people[pid]
                            if q.alive:
                                out.append(q)
        return out

    def dependents(self, pid: str) -> list[Person]:
        p = self.people[pid]
        out = []
        for cid in p.children + p.wards:
            c = self.people[cid]
            if c.alive and c.caregiver == pid:
                out.append(c)
        return out

    def kinship(self, a: Person, b: Person) -> float:
        """How closely related two people are: 1 parent/child, 0.8 sibling, 0.5 grandparent, 0.4 aunt/uncle."""
        if a.id == b.id:
            return 1.0
        if b.id in (a.mother, a.father) or a.id in (b.mother, b.father):
            return 1.0
        ap = [x for x in (a.mother, a.father) if x]
        bp = [x for x in (b.mother, b.father) if x]
        if any(x in bp for x in ap):
            return 0.8
        for x in ap:
            par = self.people[x]
            if b.id in (par.mother, par.father):
                return 0.5
            pp = [y for y in (par.mother, par.father) if y]
            if pp and any(y in pp for y in (b.mother, b.father) if y):
                return 0.4
        for x in bp:
            par = self.people[x]
            if a.id in (par.mother, par.father):
                return 0.5
            pp = [y for y in (par.mother, par.father) if y]
            if pp and any(y in pp for y in (a.mother, a.father) if y):
                return 0.4
        return 0.0

    # --- events -----------------------------------------------------------

    def emit(self, etype: str, actor: str | None, target: str | None, place: tuple | None, **data) -> int:
        eid = self.next_eid
        self.next_eid += 1
        ev = {"id": eid, "t": self.tick, "k": etype}
        if actor:
            ev["a"] = actor
        if target:
            ev["b"] = target
        if place is not None:
            ev["at"] = [place[0], place[1]]
        if data:
            ev.update(data)
        self.events.append(ev)
        return eid

    # --- the week ---------------------------------------------------------

    def step(self) -> list[dict]:
        self.events = []
        self.hunts = {}
        self.courting = []
        self.plan = {}
        self.week_decisions = []
        self._living = None
        self._grow_land()
        weather.new_week(self)
        self.reindex()
        fauna.step(self)

        for p in self.living():
            p.reward = 0.0
            p.mood_before = p.mood
            p.contact = False
            p.cared = False
            p.doing = ""

        order = sorted(p.id for p in self.living() if p.age(self.tick) >= INFANT_END)
        self.rng.shuffle(order)
        for pid in order:
            p = self.people[pid]
            if not p.alive:
                continue
            option = decision.decide(self, p).chosen
            actions.perform(self, p, option)
        actions.resolve_hunts(self)

        # Infants and children go where their caregiver goes.
        for p in self.living():
            if p.alive and p.caregiver and p.age(self.tick) < CHILD_END:
                carer = self.people[p.caregiver]
                if carer.alive:
                    self.move(p, carer.loc)

        biology.body_phase(self)

        line = json.dumps(self.events, sort_keys=True, separators=(",", ":"))
        self.event_chain = hashlib.sha256((self.event_chain + line).encode()).hexdigest()
        events = self.events
        self.tick += 1
        self._living = None
        for obs in self.observers:
            obs(self, events)
        return events

    def run(self, weeks: int) -> None:
        for _ in range(weeks):
            self.step()
            if not self.living():
                break

    def _grow_land(self) -> None:
        c = self.cfg
        rng = self.rng
        if self.week == 0 and self.tick > 0:
            self.weather = round(c.weather_low + (c.weather_high - c.weather_low) * rng.random(), 4)
            weather.new_year(self)
            self.emit("year", None, None, None, year=self.year, weather=self.weather, wet=self.sky["wet"])
            self.graves = {k: v for k, v in self.graves.items() if self.tick - v < 20 * WEEKS_PER_YEAR}
        s = self.season
        # A dry year grows less; a wet one a little more.
        g = c.season_growth[s] * self.weather * (0.6 + 0.4 * min(1.2, self.sky["wet"]))
        growing = s in (0, 1)
        winter = s == 3
        dieback = c.winter_dieback * (1.0 + 2.0 * max(0.0, self.sky["hard"]))
        decay = dict(c.pile_decay)
        for row in self.tiles:
            for t in row:
                cap = c.plant_cap * t.fertility
                t.plants = min(cap, t.plants + c.plant_regrow * t.fertility * g)
                if winter:
                    t.plants *= 1.0 - dieback
                t.wood = min(c.wood_cap * t.forest, t.wood + c.wood_regrow * t.forest)
                t.stone = min(c.stone_cap * t.rock, t.stone + c.stone_regrow * t.rock)
                if t.flinty:
                    t.flint = min(c.flint_cap, t.flint + c.flint_regrow)
                if s != 3:
                    t.fiber = min(c.fiber_cap * t.fertility, t.fiber + c.fiber_regrow * t.fertility * g)

                # Seed in the ground grows in the warm seasons; otherwise animals dig some up.
                if t.sown > 0.01:
                    if growing:
                        sprouted = t.sown * c.sprout_rate * self.weather
                        t.sown -= sprouted
                        t.crop += sprouted * c.seed_multiplier * (0.4 + 0.6 * t.fertility)
                    else:
                        t.sown *= 1.0 - c.seed_loss
                else:
                    t.sown = 0.0
                if t.crop > 0.01:
                    if winter:
                        t.crop *= 1.0 - c.crop_rot
                else:
                    t.crop = 0.0

                # Fire burns its fuel down; set-down things slowly rot.
                if t.fire > 0:
                    t.fire = max(0.0, t.fire - c.wood_burn)
                    if t.fire == 0:
                        self.emit("fire_out", None, None, (t.x, t.y))
                if t.pile:
                    for kind in list(t.pile):
                        t.pile[kind] *= 1.0 - decay.get(kind, 0.0)
                        if t.pile[kind] < 0.05:
                            del t.pile[kind]
                    if not t.pile:
                        t.builders = {}
                if t.stash:
                    _, cover = pile_shape(t.pile)
                    rate = c.spoil_rate * (1.0 - 0.6 * cover) * (c.smoke_keep if t.fire > 0 else 1.0)
                    for st in t.stash:
                        st[1] *= 1.0 - rate
                        st[2] *= 1.0 - c.seed_spoil
                    t.stash = [st for st in t.stash if st[1] + st[2] >= 0.2]
                if t.marks:
                    marks.weather_away(self, t)
                if t.fire > 0:
                    t.traces["ash"] = [1.0, self.tick]
                if t.traces:
                    leave_traces_fading(t)

        # Lightning in the dry months.
        if s in (1, 2) and rng.random() < c.lightning and not self.sky.get("rain"):
            x, y = rng.randrange(c.width), rng.randrange(c.height)
            t = self.tiles[y][x]
            if t.forest > 0.4 and t.fire <= 0:
                t.fire = 3.0
                t.wood *= 0.7
                t.plants *= 0.5
                self.emit("fire", None, None, (x, y), how="lightning")

    # --- persistence ------------------------------------------------------

    def to_dict(self) -> dict:
        v, internal, gauss = self.rng.getstate()
        return {
            "cfg": self.cfg.to_dict(),
            "tick": self.tick,
            "rng": [v, list(internal), gauss],
            "next_pid": self.next_pid,
            "next_eid": self.next_eid,
            "next_aid": self.next_aid,
            "tiles": [[t.to_list() for t in row] for row in self.tiles],
            "people": [p.to_dict() for p in self.people.values()],
            "animals": self.animals,
            "knowledge": self.knowledge,
            "event_chain": self.event_chain,
            "weather": self.weather,
            "sky": self.sky,
            "graves": self.graves,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "World":
        w = cls(Config.from_dict(d["cfg"]), _empty=True)
        v, internal, gauss = d["rng"]
        w.rng.setstate((v, tuple(internal), gauss))
        w.tick = d["tick"]
        w.next_pid = d["next_pid"]
        w.next_eid = d["next_eid"]
        w.next_aid = d.get("next_aid", 1)
        w.tiles = [[Tile.from_list(x, y, vals) for x, vals in enumerate(row)] for y, row in enumerate(d["tiles"])]
        for pd in d["people"]:
            p = Person.from_dict(pd)
            w.people[p.id] = p
        w.animals = d.get("animals", [])
        w.knowledge = d["knowledge"]
        w.event_chain = d["event_chain"]
        w.weather = d["weather"]
        w.sky = d.get("sky", w.sky)
        w.graves = d.get("graves", {})
        w.reindex()
        fauna.index(w)
        return w

    def save(self, path) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, separators=(",", ":"))

    @classmethod
    def load(cls, path) -> "World":
        with open(path, encoding="utf-8") as f:
            return cls.from_dict(json.load(f))

    def state_hash(self) -> str:
        blob = json.dumps(self.to_dict(), separators=(",", ":"))
        return hashlib.sha256(blob.encode()).hexdigest()
