"""A person: a body, a temperament, feelings, memories, ties to others, habits,
and whatever they have worked out about the world.

Temperament ("genes") is inherited from both parents with small random drift.
Everything else a person knows is culture. Habits, the things they know how to
make, and their beliefs about what is worth leaving where all come from
experience, upbringing and other people. All of it dies with them unless they
pass it on.
"""
from __future__ import annotations

from .config import ADULT_END, CHILD_END, INFANT_END, TEEN_END, WEEKS_PER_YEAR
from .matter import MATERIALS

GENES = ("curiosity", "diligence", "sociability", "kindness", "temper", "anxiety", "care", "boldness")
SKILLS = ("foraging", "hunting", "crafting")

ACTIONS = (
    "rest", "forage", "hunt", "gather", "put", "take", "make", "play", "explore",
    "give", "care", "talk", "court", "steal", "attack", "flee", "join",
    "heat", "fill",
)
A = {name: i for i, name in enumerate(ACTIONS)}
N_ACTIONS = len(ACTIONS)
N_CONTEXTS = 32  # food on hand (4) x company (2) x season (4)

# Things a person can set down somewhere.
PLACEABLE = ("seeds", "food") + MATERIALS


class Relation:
    """How one person feels about another. Not symmetric."""

    __slots__ = ("affection", "trust", "familiarity", "grudge", "respect", "balance", "last")

    def __init__(self, affection=0.0, trust=0.0, familiarity=0.0, grudge=0.0,
                 respect=0.0, balance=0.0, last=-1):
        self.affection = affection    # -1 hate .. 1 love
        self.trust = trust            # -1 .. 1
        self.familiarity = familiarity
        self.grudge = grudge          # 0 .. 1, the wish to pay someone back for harm
        self.respect = respect        # 0 .. 1
        self.balance = balance        # food they gave me minus food I gave them
        self.last = last              # tick of last contact

    def to_list(self) -> list:
        return [self.affection, self.trust, self.familiarity, self.grudge,
                self.respect, self.balance, self.last]

    @classmethod
    def from_list(cls, v: list) -> "Relation":
        return cls(*v)


class Memory:
    """Something a person saw, did, suffered, or was told."""

    __slots__ = ("eid", "tick", "kind", "actor", "target", "place", "salience",
                 "valence", "strength", "source", "hops")

    def __init__(self, eid, tick, kind, actor, target, place, salience, valence,
                 strength=1.0, source="", hops=0):
        self.eid = eid
        self.tick = tick
        self.kind = kind
        self.actor = actor
        self.target = target
        self.place = place
        self.salience = salience      # how much it matters to this person, 0 .. 1
        self.valence = valence        # how it felt, -1 .. 1
        self.strength = strength      # fades over time; forgotten near zero
        self.source = source          # "" if lived through, else who told them
        self.hops = hops              # how many tellings it passed through to reach them

    def to_list(self) -> list:
        return [self.eid, self.tick, self.kind, self.actor, self.target, list(self.place),
                self.salience, self.valence, self.strength, self.source, self.hops]

    @classmethod
    def from_list(cls, v: list) -> "Memory":
        m = cls(*v)
        m.place = tuple(m.place)
        return m


class Person:
    __slots__ = (
        "id", "name", "sex", "birth", "generation", "genes", "skills",
        "health", "energy", "food", "seeds", "mats", "items", "sick",
        "pregnant", "conceived", "last_birth", "loc",
        "mood", "fear", "anger", "grief", "loneliness",
        "rel", "memories", "q",
        "recipes", "itemval", "beliefs", "placements", "places", "expect",
        "partner", "mother", "father", "children", "wards", "caregiver", "friend",
        "alive", "death_tick", "death_cause",
        "last_action", "last_ctx", "reward", "mood_before", "doing",
        "contact", "starving", "cared", "hurt_by", "wellbeing",
        "focus", "focus_weeks", "thoughts", "considered",
        "heard", "puzzles", "marks", "thirst", "springs",
        "records", "sightings", "shores", "voyage",
        "kept", "damp", "seen_at", "recipe_got",
    )

    def __init__(self, pid: str, name: str, sex: str, birth: int, generation: int,
                 genes: dict, loc: tuple):
        self.id = pid
        self.name = name
        self.sex = sex
        self.birth = birth
        self.generation = generation
        self.genes = genes
        self.skills = {s: 0.0 for s in SKILLS}
        self.health = 100.0
        self.energy = 100.0
        self.food = 0.0                # loose food: plants and meat
        self.seeds = 0.0               # seeds: edible, and they keep
        self.mats = {m: 0.0 for m in MATERIALS}
        self.items: list[dict] = []    # things they have made
        self.sick = False
        self.pregnant = None           # father's id while pregnant
        self.conceived = -1
        self.last_birth = -10_000
        self.loc = loc
        self.mood = 0.5                # happiness, 0 .. 1
        self.fear = 0.0
        self.anger = 0.0
        self.grief = 0.0
        self.loneliness = 0.3
        self.rel: dict[str, Relation] = {}
        self.memories: list[Memory] = []
        self.q = [0.0] * (N_CONTEXTS * N_ACTIONS)
        # What they have worked out:
        self.recipes: dict[str, dict] = {}    # how to make a thing they once made or were shown
        self.itemval: dict[str, float] = {}   # how much each kind of thing has helped them
        self.beliefs: dict[str, float] = {}   # "seeds@0": how well leaving seeds somewhere in spring has gone
        self.placements: list[list] = []      # [tick, x, y, key] what they left where, for the past year
        self.places: dict[str, float] = {}    # "x,y": how good life has been there
        self.expect: dict[str, float] = {}    # what they have come to expect from foraging, from a week
        self.partner = None
        self.mother = None
        self.father = None
        self.children: list[str] = []
        self.wards: list[str] = []     # other people's children they took in
        self.caregiver = None
        self.friend = None             # closest non-family friend, refreshed each season
        self.alive = True
        self.death_tick = None
        self.death_cause = None
        self.last_action = "rest"
        self.last_ctx = 0
        self.reward = 0.0
        self.mood_before = 0.5
        self.doing = ""                # short description of this week's action, for watching
        self.contact = False
        self.starving = 0
        self.cared = False
        self.hurt_by = None
        self.wellbeing = 0.5
        self.focus = ""                # what held their attention last week ("kind:about")
        self.focus_weeks = 0           # for how many weeks running
        self.thoughts: list = []       # what is on their mind this week, strongest first
        self.considered: list = []     # the choices they weighed this week
        # Claims other people made that they accepted but have not tested themselves:
        # key -> [value, [who said it], tick]. "b:seeds@0" a belief, "m:<sig>" what a made thing is worth.
        self.heard: dict[str, list] = {}
        # Things that turned out very differently from what they expected:
        # key -> [pull, what they expected, times tested since, tick]
        self.puzzles: dict[str, list] = {}
        # Marks they have seen: shape -> [times seen, {what was around it: how strongly they link the two}]
        self.marks: dict[str, list] = {}
        self.thirst = 0.0              # how short of water last week went, 0 .. 1
        self.springs: list = []        # fresh water they have seen: [[x, y], ...], most recent last
        # Whose word has turned out right: source (a person's id, or "mark:<shape>") -> [held, failed].
        # Counted from their own tests, plus what people they believe said about the source.
        self.records: dict[str, list] = {}
        self.sightings: list = []      # animals they have seen lately: [[x, y, tick, species], ...]
        self.shores: list = []         # land they have seen across water and cannot walk to: [[x, y], ...]
        self.voyage = None             # [x, y, tick] a far shore they have set out for over water
        self.kept = 0.0                # of their food, how much has been held in a fire: it keeps longer
        self.damp: dict = {}           # how wet each material they carry is, 0 .. 10
        self.recipe_got = {}           # G1: recipe -> the week first held, while under 13 weeks (only with grace)
        self.seen_at = {}              # NV2 (LK1): loved one's id -> [x, y, tick] where last in sight (only when last_seen)

    # --- life stage -------------------------------------------------------

    def age(self, tick: int) -> int:
        return tick - self.birth

    def years(self, tick: int) -> float:
        return (tick - self.birth) / WEEKS_PER_YEAR

    def stage(self, tick: int) -> str:
        a = tick - self.birth
        if a < INFANT_END:
            return "infant"
        if a < CHILD_END:
            return "child"
        if a < TEEN_END:
            return "teen"
        if a < ADULT_END:
            return "adult"
        return "elder"

    def need(self, cfg, tick: int) -> float:
        st = self.stage(tick)
        n = {"infant": cfg.need_infant, "child": cfg.need_child, "teen": cfg.need_teen,
             "adult": cfg.need_adult, "elder": cfg.need_elder}[st]
        if self.pregnant is not None:
            n += 1.5
        return n

    def max_health(self, tick: int) -> float:
        y = self.years(tick)
        if y <= 50:
            return 100.0
        return max(30.0, 100.0 - (y - 50) * 1.5)

    def edible(self) -> float:
        return self.food + self.seeds

    def mat_total(self) -> float:
        return sum(self.mats.values())

    def home(self):
        """The place life has been best, if any place stands out."""
        best, best_v = None, 0.0
        for key, v in self.places.items():
            if v > best_v + 1e-9:
                best, best_v = key, v
        if best is None:
            return None
        x, y = best.split(",")
        return (int(x), int(y))

    # --- ties -------------------------------------------------------------

    def relation(self, other: str) -> Relation:
        r = self.rel.get(other)
        if r is None:
            r = Relation()
            self.rel[other] = r
        return r

    # --- persistence ------------------------------------------------------

    def to_dict(self) -> dict:
        d = {}
        for k in self.__slots__:
            v = getattr(self, k)
            if k == "rel":
                v = {kk: r.to_list() for kk, r in v.items()}
            elif k == "memories":
                v = [m.to_list() for m in v]
            elif k == "recipe_got" and not v:
                continue                 # G1: saved only when held, so v3's world is unchanged
            elif k == "seen_at" and not v:
                continue                 # NV2 (LK1): saved only when held, so v1's world is unchanged
            elif k == "loc":
                v = list(v)
            d[k] = v
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Person":
        p = cls(d["id"], d["name"], d["sex"], d["birth"], d["generation"], d["genes"], tuple(d["loc"]))
        for k, v in d.items():
            if k in ("id", "name", "sex", "birth", "generation", "genes", "loc"):
                continue
            if k == "rel":
                v = {kk: Relation.from_list(vv) for kk, vv in v.items()}
            elif k == "memories":
                v = [Memory.from_list(m) for m in v]
            setattr(p, k, v)
        return p
