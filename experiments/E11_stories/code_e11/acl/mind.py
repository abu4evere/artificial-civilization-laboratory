"""How a person decides what to do this week.

Each option gets a score from two sources:

1. Instinct: built-in human nature. Hunger pulls toward food, tiredness toward
   rest, cold toward warmth, loneliness toward company, love toward caring for
   one's own, a grudge toward revenge, fear toward running away, and curiosity
   toward picking things up and fiddling with them. Temperament sets how
   strongly each pull is felt.
2. What they have learned: habits (how well each kind of action has gone in
   situations like this, looking a few weeks ahead), what the things they have
   made are worth to them, and what they believe about leaving things in
   places.

A person then picks with some randomness, so similar people still lead
different lives. Nothing here knows about tools, houses, farming, trade,
marriage or law. Any of those has to show up as a pattern in what people
actually do.
"""
from __future__ import annotations

from . import fauna, inquiry, thought, weather
from .knowhow import belief
from .config import WEEKS_PER_YEAR
from .matter import MATERIALS, SOFT_WHEN_WET, best_holder, best_item, holding
from .person import A, N_ACTIONS, PLACEABLE, Person
from .util import clamp, distance, softmax_pick

COST = {
    "rest": 0, "forage": 25, "hunt": 40, "gather": 25, "put": 10, "take": 10, "make": 25,
    "play": 15, "explore": 30, "give": 5, "care": 15, "talk": 10, "court": 10,
    "steal": 15, "attack": 35, "flee": 25, "join": 20, "heat": 10, "fill": 10,
}
MOVE_COST = 4
GATHERABLE = ("stone", "flint", "wood", "fiber", "clay", "char")


def own_stash(world, p: Person, radius: int | None = None) -> list:
    """Food p remembers setting down, that is still there: [(tile, entry)]."""
    out = []
    seen = []
    for pl in p.placements:
        loc = (pl[1], pl[2])
        if loc in seen or not (pl[3].startswith("food") or pl[3].startswith("seeds")):
            continue
        seen.append(loc)
        if radius is not None and distance(p.loc, loc, world.cfg.width, world.cfg.height) > radius:
            continue
        for st in world.tile(loc).stash:
            if st[0] == p.id:
                out.append((loc, st))
    return out


def hunger_of(world, p: Person, extra_need: float = 0.0) -> float:
    """0 = well stocked, 1 = desperate. Food left nearby counts too."""
    need = p.need(world.cfg, world.tick) + extra_need
    stored = sum(st[1] + st[2] for _, st in own_stash(world, p, world.cfg.reach))
    weeks = (p.edible() + stored) / need
    h = clamp(1.0 - weeks / 2.0)
    if p.starving:
        h = min(1.0, h + 0.3)
    return h


def context_index(world, p: Person, company: bool) -> int:
    need = p.need(world.cfg, world.tick)
    weeks = p.edible() / need
    if p.health < 40 or weeks < 0.5:
        f = 0
    elif weeks < 2:
        f = 1
    elif weeks < 6:
        f = 2
    else:
        f = 3
    return f * 8 + (4 if company else 0) + world.season


def forage_rate(world, p: Person) -> float:
    c = world.cfg
    st = p.stage(world.tick)
    f = {"child": 0.4, "teen": 0.8, "adult": 1.0, "elder": 0.7}.get(st, 0.0)
    _, tool = best_item(p, "forage")
    return (c.forage_base + c.forage_skill * p.skills["foraging"]) * f * tool


def hunt_chance(world, n: float, skill: float, tool: float) -> float:
    c = world.cfg
    return min(0.92, c.hunt_base_chance * (n ** 1.5) * (0.5 + skill) * tool)


def strength(world, p: Person) -> float:
    """Fighting strength: health, nerve, age, and whatever is in hand."""
    st = p.stage(world.tick)
    age_factor = {"infant": 0.0, "child": 0.2, "teen": 0.7, "adult": 1.0, "elder": 0.6}[st]
    _, f = best_item(p, "fight")
    return (p.health / 100.0) * (0.5 + p.genes["boldness"]) * age_factor * f


def decide(world, p: Person) -> tuple:
    c = world.cfg
    rng = world.rng
    tick = world.tick
    g = p.genes
    st = p.stage(tick)
    season = world.season
    w, h = c.width, c.height

    deps = world.dependents(p.id)
    dep_need = sum(d.need(c, tick) for d in deps)
    need = p.need(c, tick)
    hunger = hunger_of(world, p, dep_need)
    # E10: a season in which they lost someone to hunger is felt a season early, only in the pull to get food.
    ahead = c.loss_weight * p.expect.get(f"loss@{(world.season + 1) % 4}", 0.0)
    food_hunger = max(hunger, ahead)
    fatigue = 1.0 - p.energy / 100.0
    maxh = p.max_health(tick)
    water_here = weather.reachable_fresh(world, p, p.loc, c.water_reach) is not None
    if p.voyage and (world.tick - p.voyage[2] > 12
                     or world.island_of(p.loc) == world.island_of((p.voyage[0], p.voyage[1]))):
        p.voyage = None
    _look_for_water(world, p)
    thought.attend(world, p, hunger, fatigue, food_hunger)

    near = world.people_near(p.loc, c.reach, exclude=p.id)
    near.sort(key=lambda q: (distance(p.loc, q.loc, w, h), q.id))
    near = near[:12]
    company = bool(near)
    ctx = context_index(world, p, company)
    p.last_ctx = ctx
    base = ctx * N_ACTIONS
    lw = c.learned_weight

    options: list = []   # (score, action, target)

    # Places with no water in sight are where thirst comes. The more it has hurt, the more that weighs.
    dry_cost = 0.0 if world.sky.get("rain") else 0.1 + 0.8 * p.thirst + 0.3 * p.expect.get("dry", 0.0)
    dry_seen: dict = {}

    def dry(t) -> bool:
        if t not in dry_seen:
            dry_seen[t] = weather.fresh_near(world, t, c.perception) is None
        return dry_seen[t]

    def add(action: str, target, u: float, dist: int = 0) -> None:
        if p.energy < COST[action] + MOVE_COST * dist:
            return
        if dry_cost and action in ("forage", "hunt", "gather", "explore", "flee", "join"):
            t = target[0] if action == "gather" else target
            if isinstance(t, tuple) and len(t) == 2 and isinstance(t[0], int) and dry(t):
                u -= dry_cost
        options.append((u + lw * p.q[base + A[action]], action, target))

    age_years = p.years(tick)
    toddler = st == "child" and age_years < 3
    small = st == "child" and age_years < 6
    grown = st in ("teen", "adult", "elder")

    # Rest
    rest_u = 0.15 + 1.2 * fatigue * fatigue + 0.6 * (1.0 - p.health / maxh)
    if p.sick:
        rest_u += 0.5
    if st == "elder":
        rest_u += 0.2
    add("rest", None, rest_u)

    # Look at nearby land. People stay off the sea and the lakes.
    tiles = [p.loc]
    home = p.home()
    if home and home != p.loc and distance(p.loc, home, w, h) <= c.reach:
        tiles.append(home)
    if not small:
        span = c.reach if st != "child" else 1
        for _ in range(6):
            tiles.append(((p.loc[0] + rng.randint(-span, span)) % w,
                          (p.loc[1] + rng.randint(-span, span)) % h))
    # Animals someone said they saw nearby are worth a look.
    for key in p.heard:
        if key[:2] == "g:":
            spot = tuple(int(v) for v in key[2:].split(","))
            if distance(p.loc, spot, w, h) <= c.reach and spot not in tiles:
                tiles.append(spot)
    tiles = [t for t in tiles if world.passable(p, t) and world.walk(p, p.loc, t)[0] == t] or [p.loc]

    # Forage
    best_forage = 0.0
    if not small:
        rate = forage_rate(world, p)
        best, best_u, best_d = None, -1.0, 0
        for t in tiles:
            d = distance(p.loc, t, w, h)
            tile = world.tile(t)
            got = min(tile.plants + tile.crop, rate) * (1.0 - 0.1 * d)
            u = (0.25 + 1.6 * food_hunger) * min(1.0, got / (need * 1.5)) + 0.08 * g["diligence"]
            if u > best_u:
                best, best_u, best_d = t, u, d
        add("forage", best, best_u, best_d)
        best_forage = best_u

    if grown:
        # Hunt: better with others.
        _, tool = best_item(p, "hunt")
        best, best_u, best_d = None, -1.0, 0
        for t in tiles:
            tile = world.tile(t)
            if fauna.prey_here(world, t) < 1 or tile.fire > 0:
                continue
            d = distance(p.loc, t, w, h)
            committed = len(world.hunts.get(t, ()))
            others = len(world.occ.get(t, ())) - (1 if t == p.loc else 0)
            n = 1 + committed + 0.25 * max(0, others - committed)
            chance = hunt_chance(world, n, p.skills["hunting"], tool)
            share = (c.hunt_prey_base + c.hunt_prey_per_hunter * min(n, 5)) / n
            ev = chance * share * (1.0 - 0.1 * d)
            u = (0.25 + 1.6 * food_hunger) * min(1.0, ev / (need * 1.5)) * (0.7 + 0.6 * g["boldness"]) + 0.05
            # What they have learned to fear holds them back.
            dread = max((fauna.fear_of(p, h["sp"]) for h in fauna.near(world, t, 0)), default=0.0)
            u -= 0.5 * dread * (1.0 - 0.5 * g["boldness"])
            if u > best_u:
                best, best_u, best_d = t, u, d
        if best is not None:
            add("hunt", best, best_u, best_d)

    if not toddler:
        # Gather: picking things up, out of curiosity or because you have found a use for them.
        if p.mat_total() < c.material_limit:
            want = _material_wants(p, season)
            best, best_u, best_d = None, 0.0, 0
            for kind in GATHERABLE:
                wk = c.worth_weight * want[kind] + 0.03 + 0.08 * g["curiosity"]
                if f"handled:{kind}" not in p.expect:
                    wk += c.novelty * g["curiosity"] * 2.0
                for t in tiles:
                    stock = world.tile(t).material(kind)
                    if stock < 1.0:
                        continue
                    d = distance(p.loc, t, w, h)
                    u = wk * (1.0 - 0.7 * hunger) * min(1.0, stock / 3.0) * (1.0 - 0.1 * d)
                    if u > best_u:
                        best, best_u, best_d = (t, kind), u, d
            if best is not None:
                add("gather", best, best_u, best_d)

        # Play: fiddle with what you have. Children do this most.
        stuff = sum(1 for v in p.mats.values() if v >= 1.0) + len(p.items)
        if stuff >= 1:
            u = (0.04 + 0.3 * g["curiosity"] * (1.0 - hunger)) * (1.6 if st == "child" else 1.0)
            add("play", None, u)

    if grown:
        # Make again something that has proved its worth.
        best, best_u = None, 0.05
        fire_here = world.tile(p.loc).fire > 0
        part_of = _wanted_parts(p)
        for sig, recipe in p.recipes.items():
            if recipe["verb"] == "heat" and not fire_here:
                continue
            # Valued for what the thing does, for what it goes into, or for what happened last time
            # it was made here.
            v = max(p.itemval.get(sig, 0.0), part_of.get(sig, 0.0))
            if recipe["verb"] == "strike":
                v = max(v, belief(p, f"{recipe['target']}/{recipe['tool']}@{season}") or 0.0)
            # Something about it surprised them: they want to try it again and see.
            v = max(v, 0.5 * max(inquiry.pull(p, "m:" + sig), inquiry.pull(p, "f:" + sig)))
            if v <= best_u or (_holding(p, sig) and v == p.itemval.get(sig, 0.0)) or not can_make(p, recipe):
                continue
            u = c.worth_weight * v * (0.6 + 0.4 * g["diligence"]) * (1.0 - 0.5 * hunger)
            if u > best_u:
                best, best_u = sig, u
        if best is not None:
            add("make", best, best_u)

        # Set something down here, if leaving such things has gone well before.
        put = _best_put(world, p, need + dep_need, hunger, season, c)
        if put is not None:
            add("put", put[0], put[1])

        # Hold food in the fire here; fill something carried with water or embers; tip embers out.
        if world.tile(p.loc).fire > 0 and p.food - min(p.kept, p.food) >= 2.0:
            add("heat", "food", _worth_trying(p, "heat:food", c) * (1.0 - 0.5 * hunger))
        for substance in ("water", "embers", "pour"):
            if can_fill(world, p, substance):
                if substance == "water":
                    u = _worth_trying(p, "fill:water", c) * (0.5 + p.expect.get("dry", 0.0) + p.thirst)
                elif substance == "embers":
                    u = _worth_trying(p, "fill:embers", c, "fire:embers")
                else:
                    u = _worth_trying(p, "fill:pour", c, "fire:embers") * (0.3 + weather.coldness(world, p.loc))
                add("fill", substance, u)

    # Take back food you left, or someone else's if hunger outweighs scruples.
    if not small:
        for loc, st_entry in own_stash(world, p, c.reach):
            u = (0.2 + 1.4 * hunger) * min(1.0, (st_entry[1] + st_entry[2]) / need)
            add("take", (loc, p.id), u, distance(p.loc, loc, w, h))
            break
        if hunger > 0.4 and grown:
            for t in tiles[:4]:
                tile = world.tile(t)
                for entry in tile.stash:
                    owner = entry[0]
                    if owner == p.id:
                        continue
                    o = world.people.get(owner)
                    family = o is not None and (world.kinship(p, o) > 0 or p.partner == owner)
                    r = p.rel.get(owner)
                    aff = r.affection if r else 0.0
                    if o is None or not o.alive:
                        scruple = 0.05
                    elif family:
                        scruple = 0.2
                    else:
                        scruple = (0.4 + 0.6 * g["kindness"]) * (0.5 + max(aff, 0.0))
                    watched = o is not None and o.alive and distance(o.loc, t, w, h) <= 1
                    u = hunger * (1.0 - 0.5 * scruple) * min(1.0, entry[1] / need) - 0.3 * scruple \
                        - (0.4 if watched else 0.0)
                    add("take", (t, owner), u, distance(p.loc, t, w, h))
                    break

    if grown:
        # Explore: curiosity, or hunger when nothing nearby is worth eating.
        explore_u = 0.04 + 0.25 * g["curiosity"] * (1.0 - hunger)
        if best_forage < 0.5 * (0.25 + 1.6 * hunger):
            explore_u += 0.6 * hunger
        if not company:
            explore_u += 0.3 * p.loneliness * g["sociability"]
        boat = world.boat(p) >= 0.65
        if boat and (p.voyage or p.shores):
            # Land they have seen across the water, and something that floats.
            if p.voyage:
                dest = (p.voyage[0], p.voyage[1])
            else:
                dest = min((tuple(s) for s in p.shores), key=lambda s: (distance(p.loc, s, w, h), s))
            explore_u += 0.1 + 0.3 * g["curiosity"]
        elif boat and rng.random() < 0.15:
            # Something that floats and nowhere in mind: a curious person may just set out.
            for _ in range(20):
                fx, fy = rng.randrange(w), rng.randrange(h)
                if not world.tile((fx, fy)).water and (fx, fy) != p.loc:
                    dest = (fx, fy)
                    break
            else:
                dest = world.nearest_land(p.loc, p)
        else:
            dest = world.nearest_land(((p.loc[0] + rng.choice((-c.reach, 0, c.reach))) % w,
                                       (p.loc[1] + rng.choice((-c.reach, c.reach))) % h), p)
        add("explore", dest, explore_u, c.reach)
        if world.tile(p.loc).water:
            # Out on the water: getting to land comes before anything else.
            ashore = (p.voyage[0], p.voyage[1]) if p.voyage else world.nearest_land(p.loc)
            add("explore", ashore, 1.5, c.reach)

    # People within reach.
    my_str = strength(world, p)
    fear_total, threat = 0.0, None
    seeking = (st == "adult" and p.partner is None and age_years < 45)
    mates_in_reach = 0
    for q in near:
        r = p.rel.get(q.id)
        aff = r.affection if r else 0.0
        trust = r.trust if r else 0.0
        grudge = r.grudge if r else 0.0
        bal = r.balance if r else 0.0
        kin = world.kinship(p, q)
        is_partner = p.partner == q.id
        d = distance(p.loc, q.loc, w, h)
        q_st = q.stage(tick)
        q_need = q.need(c, tick)
        q_hunger = clamp(1.0 - (q.edible() / q_need) / 2.0) + (0.3 if q.starving else 0.0)
        their_str = strength(world, q)
        fear_q = clamp(their_str - my_str) * 0.5 * (1.0 - g["boldness"])

        # Give food.
        surplus = p.edible() - need * 2.0 - dep_need
        if surplus > 1.0 and not (q.caregiver == p.id and q_st in ("infant", "child")):
            motive = q_hunger * (0.25 * g["kindness"] + 0.6 * max(aff, 0.0) + 0.6 * kin
                                 + (0.6 if is_partner else 0.0))
            motive += 0.35 * clamp(bal / need) * (0.5 + g["kindness"])    # paying back
            add("give", q.id, motive * min(1.0, surplus / need), d)

        # Care for the sick, the hurt and the very young.
        q_trouble = (0.6 if q.sick else 0.0) + (1.0 - q.health / 100.0) + (0.3 if q_st == "infant" else 0.0)
        if q_trouble > 0.2 and (kin > 0 or is_partner or aff > 0.3) and st != "child":
            u = q_trouble * (0.3 * g["kindness"] + 0.7 * g["care"] * (kin + (0.5 if q.caregiver == p.id else 0.0))
                             + 0.4 * max(aff, 0.0)) * (1.0 - 0.6 * hunger)
            add("care", q.id, u, d)

        # Talk: company, news, and showing the young what you know.
        u = (0.15 + 0.5 * g["sociability"] * (0.3 + p.loneliness)) * (0.6 + 0.4 * max(aff, 0.0) + 0.3 * kin)
        u -= 0.4 * hunger
        if aff < -0.3:
            u *= 0.3
        if kin > 0 and q_st in ("child", "teen") and (p.recipes or p.beliefs):
            u += 0.25 * g["care"]
        if p.memories and p.memories[-1].salience > 0.5 and p.memories[-1].tick > tick - WEEKS_PER_YEAR:
            u += 0.15
        add("talk", q.id, u, d)

        # Court.
        if (st == "adult" and q_st == "adult" and q.sex != p.sex and kin == 0
                and q.id not in p.wards and p.id not in q.wards
                and abs(p.birth - q.birth) <= 15 * WEEKS_PER_YEAR):
            if is_partner:
                add("court", q.id, 0.2 + 0.3 * (1.0 - max(aff, 0.0)) - 0.3 * hunger, d)
            elif p.partner is None and q.partner is None and aff > -0.2:
                mates_in_reach += 1
                u = (0.35 + 0.4 * g["sociability"]) * (0.5 + 0.5 * max(aff, 0.0)) * (1.0 - 0.5 * hunger)
                add("court", q.id, u, d)

        # Steal: hunger, without kindness or love to hold you back.
        if q.food > 4.0 and hunger > 0.3 and kin < 0.5 and not is_partner and st != "child":
            u = (hunger * (1.0 - g["kindness"]) * (0.3 + 0.7 * g["temper"])
                 * min(1.0, q.food / (2.0 * need)) * (1.0 - max(aff, 0.0)))
            u -= 0.25 + 0.4 * fear_q
            add("steal", q.id, u, d)

        # Attack: a grudge, a temper, and the nerve to act on them.
        if grudge > 0.15 and st != "child":
            u = (grudge * (0.4 + 0.8 * g["temper"]) * (0.6 + 0.8 * g["boldness"]) * (0.5 + p.anger)
                 - 0.35 * g["kindness"] - fear_q - 0.15 - 0.5 * max(aff, 0.0))
            add("attack", q.id, u, d)

        if trust < -0.4 and their_str > 0.8 * my_str:
            if -trust > fear_total:
                fear_total, threat = -trust, q

    # Flee someone you fear.
    if threat is not None and st != "child":
        u = fear_total * (0.5 + g["anxiety"]) * (1.0 - g["boldness"]) * 0.9
        add("flee", world.step_away_land(p.loc, threat.loc, c.reach, p), u, c.reach)

    if grown:
        # Single adults with no one to court nearby go looking, beyond their own band if need be.
        if seeking and mates_in_reach == 0:
            for q in world.people_near(p.loc, c.perception + 2, exclude=p.id):
                if (q.stage(tick) == "adult" and q.sex != p.sex and q.partner is None
                        and world.kinship(p, q) == 0 and abs(p.birth - q.birth) <= 15 * WEEKS_PER_YEAR):
                    add("join", world.step_toward_land(p.loc, q.loc, c.reach, p), 0.3 + 0.3 * g["sociability"], c.reach)
                    break
            else:
                add("explore", dest, 0.15 + 0.25 * g["sociability"] + 0.15 * g["boldness"], c.reach)

        # Animals someone said they saw further off: worth the walk when hungry.
        if hunger > 0.3:
            for key, hv in p.heard.items():
                if key[:2] == "g:":
                    spot = tuple(int(v) for v in key[2:].split(","))
                    d = distance(p.loc, spot, w, h)
                    if c.reach < d <= 3 * c.reach:
                        add("join", world.step_toward_land(p.loc, spot, c.reach, p), 0.1 + 0.9 * hunger * hv[0], c.reach)
                        break

        # Go back to family and friends when they are out of reach.
        for q, aff, kin in _far_people(world, p):
            u = (0.2 + 0.6 * p.loneliness * g["sociability"] + 0.5 * kin
                 + (0.6 if p.partner == q.id else 0.0)) * max(aff, 0.2) * (1.0 - 0.5 * hunger)
            add("join", world.step_toward_land(p.loc, q.loc, c.reach, p), u, c.reach)

        # Go back to the place where life has been best.
        if home and distance(p.loc, home, w, h) > 0:
            here_v = p.places.get(f"{p.loc[0]},{p.loc[1]}", 0.0)
            home_v = p.places.get(f"{home[0]},{home[1]}", 0.0)
            u = 0.05 + 1.5 * max(0.0, home_v - here_v)
            add("join", world.step_toward_land(p.loc, home, c.reach, p), u, min(c.reach, distance(p.loc, home, w, h)))

        # Thirst pulls toward water they know of; with none known, they go looking.
        if not water_here:
            # Thirst is the most urgent of the body's pulls: it kills faster than hunger.
            pull = 0.3 + 2.5 * p.thirst + (0.0 if world.sky.get("rain") else 0.2)
            spring = _nearest_spring(world, p)
            if spring is not None:
                add("join", world.step_toward_land(p.loc, spring, c.reach, p), pull,
                    min(c.reach, distance(p.loc, spring, w, h)))
            else:
                add("explore", dest, 0.1 + 0.8 * p.thirst, c.reach)

        # The cold pulls people toward any fire they can see.
        if weather.coldness(world, p.loc) > 0.3:
            fire = _nearest_fire(world, p)
            if fire is not None and fire != p.loc:
                add("join", world.step_toward_land(p.loc, fire, c.reach, p), 0.5 + 0.3 * (1.0 - p.health / 100.0),
                    min(c.reach, distance(p.loc, fire, w, h)))

    allowed = c.allowed_actions()
    if allowed is not None:
        options = [o for o in options if o[1] in allowed]
    if not options:
        p.considered = []
        return ("rest", None)
    options = thought.steer(p, options)
    i = softmax_pick(rng, [o[0] for o in options], c.choice_temperature)
    ranked = sorted(range(len(options)), key=lambda k: -options[k][0])[:4]
    p.considered = [[options[k][1], _aim(options[k][2]), round(options[k][0], 2), 1 if k == i else 0] for k in ranked]
    if i not in ranked:
        p.considered.append([options[i][1], _aim(options[i][2]), round(options[i][0], 2), 1])
    return (options[i][1], options[i][2])


def _worth_trying(p: Person, key: str, c, learned: str | None = None) -> float:
    """What doing this has been worth to them, or, if they have never tried it, the pull of the new."""
    if "tried:" + key not in p.expect:
        return 0.02 + c.novelty * p.genes["curiosity"]
    return c.worth_weight * p.expect.get(learned or key, 0.0) * (0.5 + 0.5 * p.genes["diligence"])


def _wanted_parts(p: Person) -> dict:
    """Made things that go into something they value and do not have: worth making for that."""
    out: dict = {}
    for sig, recipe in p.recipes.items():
        v = p.itemval.get(sig, 0.0)
        if v <= 0 or _holding(p, sig):
            continue
        parts = list(recipe.get("parts", ())) + ([recipe["part"]] if recipe["verb"] == "heat" else [])
        for part in parts:
            if part not in MATERIALS and not _holding(p, part, worn_ok=True):
                out[part] = max(out.get(part, 0.0), 0.8 * v)
    return out


def can_fill(world, p: Person, substance: str) -> bool:
    """Can p fill something with water or embers here, or tip embers out onto something dry that burns?"""
    tile = world.tile(p.loc)
    if substance == "water":
        return best_holder(p, "water") >= 0 and \
            weather.reachable_fresh(world, p, p.loc, world.cfg.water_reach) is not None
    if substance == "embers":
        return tile.fire > 0 and best_holder(p, "embers") >= 0
    return (holding(p, "embers") >= 0 and tile.fire <= 0 and not tile.water
            and any(p.mats.get(k, 0.0) >= 1.0 and p.damp.get(k, 0) <= 5 for k in ("fiber", "wood", "char")))


def _aim(target) -> str:
    """A choice's target, as something a watcher can read: a person's id, a thing, or a place."""
    if target is None:
        return ""
    if isinstance(target, str):
        return target
    if isinstance(target, tuple) and len(target) == 2 and isinstance(target[1], str):
        return target[1] if target[1].startswith("p") else f"{target[1]}"
    if isinstance(target, tuple) and len(target) == 2 and isinstance(target[0], int):
        return f"{target[0]},{target[1]}"
    return ""


def _material_wants(p: Person, season: int) -> dict:
    """How much each material is wanted for the things p knows how to make, or likes to leave places."""
    want = {k: 0.0 for k in GATHERABLE}
    for sig, recipe in p.recipes.items():
        v = p.itemval.get(sig, 0.0)
        if v <= 0 or _holding(p, sig):
            continue
        for kind in recipe_materials(recipe):
            if kind in want and p.mats.get(kind, 0.0) < 1.0:
                want[kind] = max(want[kind], v)
    for kind in GATHERABLE:
        b = max(belief(p, f"{kind}@{season}") or 0.0, belief(p, f"{kind}@{(season + 1) % 4}") or 0.0)
        if b > 0:
            want[kind] = max(want[kind], b)
    # What a puzzle needs to try again.
    for key, pz in p.puzzles.items():
        recipe = p.recipes.get(key[2:]) if key[:2] in ("m:", "f:") else None
        if recipe is not None:
            for kind in recipe_materials(recipe):
                if kind in want and p.mats.get(kind, 0.0) < 2.0:
                    want[kind] = max(want[kind], 0.5 * pz[0])
    return want


def _best_put(world, p: Person, total_need: float, hunger: float, season: int, c):
    """Which thing p most wants to set down here, if any. Untried things get tried now and then."""
    g = p.genes
    best, best_u = None, 0.0
    for thing in PLACEABLE:
        if thing == "food":
            have = p.food - 2.0 * total_need
        elif thing == "seeds":
            have = p.seeds - (2.0 * total_need - p.food if p.food < 2.0 * total_need else 0.0)
        else:
            have = p.mats.get(thing, 0.0)
        if have < 1.0:
            continue
        key = f"{thing}@{season}"
        b = belief(p, key)
        if b is not None:
            u = c.worth_weight * b * (0.5 + 0.5 * g["diligence"])
        else:
            u = 0.02 + c.novelty * g["curiosity"]
        u = max(u, 0.6 * inquiry.pull(p, "b:" + key))
        if thing in ("food", "seeds"):
            u *= 1.0 - hunger
        if u > best_u:
            best, best_u = thing, u
    if best is None:
        return None
    return best, best_u


def recipe_materials(recipe: dict) -> list:
    if recipe["verb"] == "strike":
        return [recipe["target"], recipe["tool"]]
    if recipe["verb"] == "shape":
        return [recipe["material"]]
    if recipe["verb"] == "heat":
        return [recipe["part"]] if recipe["part"] in MATERIALS else []
    if recipe["verb"] == "fill":
        return []
    out = [part for part in recipe["parts"] if part in MATERIALS]
    out.append(recipe["binder"])
    return out


def can_make(p: Person, recipe: dict) -> bool:
    """Are the materials and parts for this recipe in hand?"""
    if recipe["verb"] == "shape":
        m = recipe["material"]
        return p.mats.get(m, 0.0) >= 1.0 and p.damp.get(m, 0) >= SOFT_WHEN_WET
    if recipe["verb"] == "heat":
        part = recipe["part"]
        if part in MATERIALS:
            return p.mats.get(part, 0.0) >= 1.0
        return any(it["sig"] == part for it in p.items)
    if recipe["verb"] == "fill":
        return False
    need: dict = {}
    if recipe["verb"] == "strike":
        need[recipe["target"]] = 1
        need[recipe["tool"]] = need.get(recipe["tool"], 0) + 1
        # The hammer is not used up, but striking a thing with its own kind needs two of them.
        if recipe["tool"] != recipe["target"]:
            need[recipe["tool"]] = 1
    else:
        made: dict = {}
        for part in recipe["parts"]:
            if part in p.mats:
                need[part] = need.get(part, 0) + 1
            else:
                made[part] = made.get(part, 0) + 1
        for sig, n in made.items():
            if sum(1 for it in p.items if it["sig"] == sig) < n:
                return False
        need[recipe["binder"]] = need.get(recipe["binder"], 0) + 1
    return all(p.mats.get(k, 0.0) >= n for k, n in need.items())


def _holding(p: Person, sig: str, worn_ok: bool = False) -> bool:
    for it in p.items:
        if it["sig"] == sig and (worn_ok or it["uses"] > 5):
            return True
    return False


def _nearest_fire(world, p: Person):
    c = world.cfg
    best, best_d = None, 99
    for dy in range(-c.perception, c.perception + 1):
        for dx in range(-c.perception, c.perception + 1):
            loc = ((p.loc[0] + dx) % c.width, (p.loc[1] + dy) % c.height)
            if world.tile(loc).fire > 0:
                d = max(abs(dx), abs(dy))
                if d < best_d:
                    best, best_d = loc, d
    return best


def _look_for_water(world, p: Person) -> None:
    """Fresh water p can see from here is remembered; a remembered spring found dry is forgotten.
    Animals in view are remembered too, and anything p was told about places in view is checked."""
    from .information import check_places
    c = world.cfg
    herd = max((g for g in fauna.near(world, p.loc, c.perception) if g["sp"] in fauna.PREY and g["sp"] != "fish"
                and g["n"] > 0), key=lambda g: (g["n"], -g["id"]), default=None)
    if herd is not None:
        p.sightings = [s for s in p.sightings if (s[0], s[1]) != (herd["x"], herd["y"])][-2:]
        p.sightings.append([herd["x"], herd["y"], world.tick, herd["sp"]])
    check_places(world, p)
    # Land across water that cannot be walked to: seen, and remembered.
    mine = world.island_of(p.loc)
    if mine is not None:
        best, best_d = None, 99
        for dy in range(-c.perception, c.perception + 1):
            for dx in range(-c.perception, c.perception + 1):
                n = ((p.loc[0] + dx) % c.width, (p.loc[1] + dy) % c.height)
                other = world.island_of(n)
                if other is not None and other != mine and max(abs(dx), abs(dy)) < best_d:
                    best, best_d = n, max(abs(dx), abs(dy))
        if best is not None:
            spot = [best[0], best[1]]
            p.shores = [s for s in p.shores if s != spot][-2:] + [spot]
    seen = weather.reachable_fresh(world, p, p.loc, c.perception)
    if seen is not None:
        spot = [seen[0], seen[1]]
        if spot in p.springs:
            p.springs.remove(spot)
        p.springs.append(spot)
        p.springs = p.springs[-4:]
    for spot in list(p.springs):
        if distance(p.loc, tuple(spot), c.width, c.height) <= 1 and weather.fresh_near(world, tuple(spot), 1) is None:
            p.springs.remove(spot)     # nothing here after all


def _nearest_spring(world, p: Person):
    """Water p knows of, or failing that, water they were told of."""
    c = world.cfg
    best, best_d = None, 999
    for spot in p.springs:
        d = distance(p.loc, tuple(spot), c.width, c.height)
        if d < best_d:
            best, best_d = tuple(spot), d
    if best is None:
        for key in p.heard:
            if key[:2] == "w:":
                spot = tuple(int(v) for v in key[2:].split(","))
                d = distance(p.loc, spot, c.width, c.height)
                if d < best_d:
                    best, best_d = spot, d
    return best


def _far_people(world, p: Person) -> list:
    """Loved ones beyond reach that p might travel toward: partner, parents, children, best friend."""
    c = world.cfg
    out = []
    seen = []
    for pid in (p.partner, p.mother, p.father, *p.children):
        if pid and pid not in seen:
            seen.append(pid)
    if p.friend and p.friend not in seen:
        seen.append(p.friend)
    for pid in seen:
        q = world.people[pid]
        if not q.alive:
            continue
        if distance(p.loc, q.loc, c.width, c.height) <= c.reach:
            continue
        r = p.rel.get(pid)
        aff = r.affection if r else 0.0
        out.append((q, aff, world.kinship(p, q)))
    return out[:3]

