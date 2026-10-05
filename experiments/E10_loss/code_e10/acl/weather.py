"""Weather and water.

Every year is wetter or drier, and its winter milder or harder. Every week it
rains or it does not. Now and then a storm crosses part of the land, and in a
wet spring the rivers flood. None of this aims at anyone (Rules 8 and 10).

How cold a place feels depends on where it is (the north and high ground are
colder), the season, the year, and whether it is raining.

Bodies need fresh water. Rivers and lakes have it. Water in sight is walked to
every day, at a cost in energy. After rain, there are pools everywhere for a
while (less so in desert). Sea water is salty: drinking it does
not help, and makes you ill. Nobody knows that until they try it or see it.
"""
from __future__ import annotations

from .util import clamp

SEASON_TEMP = (0.0, 0.2, 0.0, -0.3)    # spring, summer, autumn, winter
RAIN = (0.55, 0.3, 0.5, 0.45)          # chance of rain in a week of each season, in an ordinary year
FRESH = ("river", "lake")


def new_year(world) -> None:
    """How wet the year will be, and how hard its winter."""
    rng = world.rng
    sky = world.sky
    sky["wet"] = round(0.45 + 0.9 * rng.random(), 3)
    sky["hard"] = round(-0.1 + 0.25 * rng.random(), 3)
    if sky["wet"] < 0.65:
        world.emit("drought", None, None, None, wet=sky["wet"])
    if sky["hard"] > 0.1:
        world.emit("hard_winter", None, None, None, hard=sky["hard"])


def new_week(world) -> None:
    """This week's rain, and any storm or flood. Their effects land on whatever is there."""
    rng = world.rng
    sky = world.sky
    s = world.season
    sky["rained"] = sky.get("rain", 0)
    roll = rng.random()
    sky["roll"] = round(roll, 4)
    sky["rain"] = 1 if roll < RAIN[s] * sky["wet"] else 0
    sky["storm"] = None
    sky["flood"] = 0
    if s in (1, 2) and rng.random() < 0.06:
        _storm(world)
    if s == 0 and sky["rain"] and sky["wet"] > 1.0 and sky.get("flooded") != world.year and rng.random() < 0.1:
        sky["flooded"] = world.year          # the rivers rise at most once a spring
        _flood(world)


def raining(world, loc) -> bool:
    """Whether it rained here this week. Desert gets rain only in the wettest weeks."""
    sky = world.sky
    if not sky.get("rain"):
        return False
    if world.tile(loc).biome == "desert":
        return sky["roll"] < 0.3 * RAIN[world.season] * sky["wet"]
    return True


def coldness(world, loc) -> float:
    """How cold it is here this week: 0 is comfortable, 1 is a hard winter week, up to 1.5."""
    t = world.tile(loc)
    s = world.season
    felt = t.temp + SEASON_TEMP[s]
    if s == 3:
        felt -= world.sky.get("hard", 0.0)
    if world.sky.get("rain") and s in (2, 3):
        felt -= 0.05
    return clamp((0.45 - felt) / 0.3, 0.0, 1.5)


def fresh_near(world, loc, radius: int):
    """The nearest fresh water within `radius` tiles (a river, or a lake shore), or None."""
    c = world.cfg
    best, best_d = None, 99
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            d = max(abs(dx), abs(dy))
            if d >= best_d:
                continue
            n = ((loc[0] + dx) % c.width, (loc[1] + dy) % c.height)
            if world.tile(n).biome in FRESH:
                best, best_d = n, d
    return best


def reachable_fresh(world, p, here, radius: int):
    """The nearest fresh water within `radius` that p can walk to (to a river, or to a lake's shore)."""
    from .util import distance
    c = world.cfg
    spots = []
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            n = ((here[0] + dx) % c.width, (here[1] + dy) % c.height)
            if world.tile(n).biome in FRESH:
                spots.append((max(abs(dx), abs(dy)), n))
    for d, spot in sorted(spots):
        end, _ = world.walk(p, here, spot)
        if distance(end, spot, c.width, c.height) <= (0 if world.tile(spot).biome == "river" else 1):
            return spot
    return None


def salt_near(world, loc) -> bool:
    c = world.cfg
    for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
        if world.tile(((loc[0] + dx) % c.width, (loc[1] + dy) % c.height)).biome in ("sea", "deep"):
            return True
    return False


def drink(world, p) -> float:
    """p drinks what they can find this week. Returns how short of water they went, 0 .. 1.

    Water close by is drunk every day. Water they can see but further off means walking there and
    back every day, which costs energy; something that holds water saves some of the walking.
    Beyond that, only rain helps."""
    from .matter import best_item
    from .util import distance
    c = world.cfg
    if raining(world, p.loc):
        return 0.0
    if world.sky.get("rained") and world.tile(p.loc).biome != "desert":
        return 0.0                         # last week's rain still stands in pools
    start = world.plan.get(p.id, (p.loc, ""))[0]
    best = None
    for here in (p.loc, start):
        spot = reachable_fresh(world, p, here, c.perception)
        if spot is not None:
            d = distance(here, spot, c.width, c.height)
            best = d if best is None else min(best, d)
    if best is not None:
        if best > c.water_reach:
            _, f = best_item(p, "carry")
            walk = 6.0 * (best - c.water_reach) * (1.0 - 0.6 * min(1.0, f - 1.0))
            p.energy = max(0.0, p.energy - walk)
        return 0.0
    from .matter import holding
    idx = holding(p, "water")
    if idx >= 0:
        # Water carried from somewhere else: drunk where there is none to be had.
        from .knowhow import judge_item
        it = p.items[idx]
        it["holds"][1] -= 1
        if it["holds"][1] <= 0:
            it["holds"] = None
        before = p.expect.get("fill:water", 0.0)
        p.expect["fill:water"] = round(before + 0.3 * (1.0 - before), 3)
        judge_item(world, p, it["sig"], 0.5)
        world.emit("consequence", p.id, None, p.loc, what="water_carried", thing=it["sig"])
        return 0.0
    if salt_near(world, p.loc):
        # Water is water, as far as anyone knows, until they drink the sea. It does not help.
        expected = p.expect.get("salt", 1.0)
        if expected > 0.4:
            p.expect["salt"] = round(expected * 0.5, 3)
            p.health -= 3.0
            if world.rng.random() < 0.3:
                p.sick = True
            world.emit("drank_sea", p.id, None, p.loc, first=1 if expected >= 1.0 else 0)
    return 1.0


def _storm(world) -> None:
    rng = world.rng
    c = world.cfg
    x, y = rng.randrange(c.width), rng.randrange(c.height)
    r = rng.randint(2, 5)
    world.sky["storm"] = [x, y, r]
    eid = world.emit("storm", None, None, (x, y), r=r)
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            t = world.tiles[(y + dy) % c.height][(x + dx) % c.width]
            if t.water:
                continue
            t.fire = 0.0
            t.plants *= 0.9
            t.wood = min(c.wood_cap * max(t.forest, 0.05), t.wood + 0.5 * t.forest)
            if t.pile:
                for k in ("hide", "fiber"):
                    if k in t.pile:
                        t.pile[k] *= 0.7
            if t.stash:
                from .matter import pile_shape
                _, cover = pile_shape(t.pile)
                for st in t.stash:
                    st[1] *= 1.0 - 0.3 * (1.0 - cover)
            if t.marks:
                t.marks = [m for m in t.marks if m[4] != "ground"]
            t.traces.pop("ash", None)
    _caught(world, (x, y), r, eid, "storm", 6.0)


def _flood(world) -> None:
    c = world.cfg
    flooded = []
    for row in world.tiles:
        for t in row:
            if t.biome != "river":
                continue
            for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                n = world.tiles[(t.y + dy) % c.height][(t.x + dx) % c.width]
                if not n.water and (n.x, n.y) not in flooded:
                    flooded.append((n.x, n.y))
    if not flooded:
        return
    world.sky["flood"] = 1
    eid = world.emit("flood", None, None, None, tiles=len(flooded))
    for x, y in flooded:
        t = world.tiles[y][x]
        t.sown *= 0.2
        t.crop *= 0.3
        t.plants *= 0.7
        t.fire = 0.0
        t.fertility = round(min(1.0, t.fertility + 0.03), 4)       # the water leaves silt behind
        for st in t.stash:
            st[1] *= 0.3
            st[2] *= 0.5
        if t.pile:
            for k in list(t.pile):
                t.pile[k] *= 0.6
        if t.marks:
            t.marks = [m for m in t.marks if m[4] != "ground"]
        for kind in list(t.traces):
            if kind.startswith(("sown", "ash", "bones")):
                del t.traces[kind]
    for x, y in flooded:
        if world.tile((x, y)).biome == "river":
            _caught(world, (x, y), 0, eid, "flood", 8.0)


def _caught(world, centre, r: int, eid: int, kind: str, harm: float) -> None:
    """Everyone out in it is hurt by how exposed they are, and remembers it."""
    from .matter import pile_warmth
    from .social import remember
    for q in world.people_near(centre, r):
        tile = world.tile(q.loc)
        shelter = pile_warmth(tile.pile) if tile.pile else 0.0
        exposure = 1.0 - clamp(2.0 * shelter)
        if exposure <= 0.05:
            continue
        q.health -= harm * exposure
        q.fear = clamp(q.fear + 0.15 * exposure * (0.5 + q.genes["anxiety"]))
        q.hurt_by = q.hurt_by or kind
        if q.age(world.tick) >= 52 * 3:
            remember(world, q, eid, kind, None, None, q.loc, 0.25 + 0.3 * exposure, -0.5 * exposure)
