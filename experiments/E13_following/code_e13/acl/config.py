"""The laws of nature. Every number the simulation uses lives here.

One tick is one week, and a year is 52 weeks. Seasons are 13 weeks each, and
the world starts in spring.

These numbers describe physics and bodies: how land grows, how materials
behave, how fire burns, what people need. None of them describe a tool, a
building, a farm or a custom. Those are left for the people to work out.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, fields

WEEKS_PER_YEAR = 52
WEEKS_PER_SEASON = 13
SEASONS = ("spring", "summer", "autumn", "winter")

# Life stages, as ages in weeks.
INFANT_END = 1 * WEEKS_PER_YEAR
CHILD_END = 12 * WEEKS_PER_YEAR
TEEN_END = 16 * WEEKS_PER_YEAR
ADULT_END = 50 * WEEKS_PER_YEAR

# Experiment 0 feature stages: which actions are available at each stage.
# None means "every action" (the full current world). Each stage only adds
# actions on top of the previous one, so we can see what each layer contributes.
STAGE_ACTIONS = {
    "E0-A": ("rest", "forage", "hunt", "gather", "explore"),
    "E0-B": ("rest", "forage", "hunt", "gather", "explore",
             "talk", "give", "care", "court", "attack", "steal", "flee", "join"),
    "E0-C": ("rest", "forage", "hunt", "gather", "explore",
             "talk", "give", "care", "court", "attack", "steal", "flee", "join",
             "put", "take"),
    "E0-D": None,
}

# Frozen version labels, recorded with every experiment run so results are
# reproducible and comparable across future revisions.
VERSIONS = {"world_bible": "8.1", "world": "0.4", "agent": "0.4"}


@dataclass
class Config:
    seed: int = 42
    width: int = 40
    height: int = 40
    founders: int = 20
    stage: str = "E0-D"                 # which E0 feature stage to run (E0-A..E0-D)
    founder_min_age: int = 16          # years
    founder_max_age: int = 28
    founder_food: float = 21.0         # three weeks of food each

    # --- land -------------------------------------------------------------
    plant_cap: float = 64.0            # most wild plant food a tile holds, at fertility 1
    plant_regrow: float = 14.0         # weekly regrowth, at fertility 1
    season_growth: tuple = (1.3, 1.0, 0.5, 0.15)  # spring, summer, autumn, winter
    winter_dieback: float = 0.03       # share of wild plant food that rots each winter week
    weather_low: float = 0.65          # each year's growing conditions: a random factor
    weather_high: float = 1.25         # between these two
    seed_share: tuple = (0.0, 0.12, 0.35, 0.05)   # share of a plant harvest that is seed, by season
    wood_cap: float = 20.0
    wood_regrow: float = 0.3
    stone_cap: float = 15.0
    stone_regrow: float = 0.05
    clay_cap: float = 6.0              # soft wet earth, only by rivers and lakes
    clay_regrow: float = 0.02
    char_cap: float = 5.0              # what a fire that burned for a while leaves
    char_per_week: float = 0.15
    flint_cap: float = 4.0             # only on some rocky tiles
    flint_regrow: float = 0.02
    fiber_cap: float = 12.0
    fiber_regrow: float = 0.8          # in the growing seasons

    # --- seeds in the ground ----------------------------------------------
    sprout_rate: float = 0.08          # share of buried seed that grows each spring/summer week
    seed_multiplier: float = 5.0       # food grown per unit of seed that sprouts
    seed_loss: float = 0.03            # buried seed eaten by animals each week outside the growing season
    crop_rot: float = 0.05             # standing plants rot each winter week

    # --- fire -------------------------------------------------------------
    lightning: float = 0.03            # chance per summer/autumn week that lightning starts a fire somewhere
    spark_chance: float = 0.3          # flint struck hard makes a spark this often
    wood_burn: float = 1.0             # fuel a fire uses per week
    wood_fuel: float = 1.5             # fuel one unit of wood adds
    fire_warmth: float = 0.6           # share of cold a fire keeps off
    heated_food_saving: float = 0.15       # food that has been in a fire goes further
    kept_keep: float = 0.25            # food that has been in a fire rots this much as fast
    smoke_keep: float = 0.25           # food near smoke rots this much as fast

    # --- piles of things on the ground ------------------------------------
    pile_decay: tuple = (("fiber", 0.02), ("hide", 0.01), ("wood", 0.004), ("bone", 0.002))

    # --- bodies -----------------------------------------------------------
    need_infant: float = 2.0           # food per week
    need_child: float = 4.0
    need_teen: float = 6.0
    need_adult: float = 7.0
    need_elder: float = 6.0
    carry_limit: float = 100.0         # food and seed one person can carry
    material_limit: float = 20.0       # raw materials one person can carry
    item_limit: int = 3                # made things one person can carry
    spoil_rate: float = 0.04           # share of loose food that rots each week
    seed_spoil: float = 0.005          # seeds keep
    starvation_damage: float = 14.0    # health lost in a week with no food at all
    fed_recovery: float = 1.5          # health regained in a fed week
    cold_damage: float = 1.2           # a hard-winter week fully exposed (see weather.coldness)
    thirst_damage: float = 20.0        # health lost in a week with no water at all
    water_reach: int = 2               # fresh water this close is drunk from every day
    illness_chance: float = 0.003      # per week, before risk factors
    illness_damage: float = 3.5
    illness_recovery: float = 0.15
    mortality_base: float = 1.5e-5     # Gompertz: weekly death risk = base * e^(rate * age_years)
    mortality_rate: float = 0.0866     # risk doubles about every 8 years
    energy_recovery: float = 25.0

    # --- reproduction -----------------------------------------------------
    fertile_from: int = 16             # years
    fertile_until: int = 45
    conception_chance: float = 0.04    # per week a couple spends together
    pregnancy_weeks: int = 39
    nursing_weeks: int = 78            # no new pregnancy while nursing
    birth_death_chance: float = 0.01
    mutation: float = 0.08             # how far a child's temperament drifts from its parents'
    camp_radius: int = 2               # partners this close count as living together

    # --- work -------------------------------------------------------------
    reach: int = 3                     # tiles a person can travel and still act that week
    perception: int = 4                # tiles a person can see
    forage_base: float = 12.0
    forage_skill: float = 14.0
    hunt_base_chance: float = 0.10
    hunt_prey_base: float = 25.0
    hunt_prey_per_hunter: float = 12.0
    hunt_injury: float = 0.03
    gather_base: float = 3.0
    gather_skill: float = 4.0
    skill_gain: float = 0.012
    anticipation_weight: float = 0.0   # E9 (A2): how strongly next season's expected shortage is felt now
    b2_mode: int = 0                   # E13 (B2): 0 off; 1 follow the best-fed visible adult; 2 the same, among those whose children all live

    # --- minds ------------------------------------------------------------
    choice_temperature: float = 0.2    # how much chance there is in a decision
    learning_rate: float = 0.05
    discount: float = 0.8              # how much next week's prospects count toward this week's choice
    learned_weight: float = 0.6        # how much experience counts against instinct
    association_rate: float = 0.25     # how fast people link what they left somewhere to what happened there
    worth_weight: float = 2.0          # how strongly a proven thing or practice pulls on choices
    novelty: float = 0.15              # extra pull of a material or combination never tried
    memory_capacity: int = 60
    mark_chance: float = 0.2           # how often fiddling with something hard turns to scratching a surface
    imitation_rate: float = 0.05

    def allowed_actions(self):
        """The set of actions this stage allows, or None for every action."""
        allowed = STAGE_ACTIONS.get(self.stage, None)
        return set(allowed) if allowed is not None else None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Config":
        known = {f.name: f for f in fields(cls)}
        out = {}
        for k, v in d.items():
            if k in known:
                if isinstance(v, list):
                    v = tuple(tuple(x) if isinstance(x, list) else x for x in v)
                out[k] = v
        return cls(**out)
