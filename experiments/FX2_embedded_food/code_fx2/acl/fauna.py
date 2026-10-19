"""Animals: whole species with one mind each.

People each have their own temperament, memories and ideas. Animals do not:
every rabbit wants what every other rabbit wants. Each species has a fixed set
of instincts, the same for all its members. Eat. Run from what hunts you. Hunt
what you can catch. Breed in the warm seasons. Survive the winter.

Animals live in groups (a warren of rabbits, a herd of deer or bison, a pack of
wolves, a bear, a school of fish). Each group is one moving thing with a size.
Together they make a food chain. Plants feed the grazers. Grazers feed wolves,
bears and people. Fish feed bears and people.

Wolves near starving may go for a person on their own, but they keep away
from fire and from people standing together. Bears attack when surprised. Bison
fight back. Being hurt by an animal, seeing it happen or being told about it
teaches a person to fear that kind of animal. The animals know none of this;
they only follow their instincts.
"""
from __future__ import annotations

from .util import clamp, distance

SPECIES = {
    # size: group size range; speed: tiles a week; breed: young per adult per warm week
    # need: plant food per animal per week; meat/hide/bone: what one animal gives a hunter
    # flee: how quickly they run from people; danger: how hard they fight back
    "rabbit": {"eats": "plants", "lives": ("plains", "forest", "hills", "tundra", "beach", "river"),
               "size": (4, 16), "speed": 1, "breed": 0.03, "need": 0.12, "meat": 3.0, "hide": 0.0, "bone": 0.0,
               "flee": 0.85, "danger": 0.0, "catch": 0.40},
    "deer": {"eats": "plants", "lives": ("forest", "woods", "plains", "hills", "river"),
             "size": (3, 10), "speed": 2, "breed": 0.008, "need": 1.0, "meat": 22.0, "hide": 1.0, "bone": 2.0,
             "flee": 0.6, "danger": 0.03, "catch": 0.16},
    "bison": {"eats": "plants", "lives": ("plains", "tundra"),
              "size": (6, 20), "speed": 2, "breed": 0.006, "need": 2.2, "meat": 55.0, "hide": 2.0, "bone": 3.0,
              "flee": 0.35, "danger": 0.22, "catch": 0.10},
    "wolf": {"eats": "meat", "prey": ("rabbit", "deer"), "lives": ("forest", "woods", "plains", "hills", "tundra"),
             "size": (3, 7), "speed": 3, "breed": 0.02, "danger": 0.5},
    "bear": {"eats": "both", "prey": ("fish", "deer"), "lives": ("woods", "forest", "hills", "mountain", "river"),
             "size": (1, 2), "speed": 1, "breed": 0.012, "need": 1.5, "danger": 0.75},
    "fish": {"eats": "water", "lives": ("sea", "lake", "river"),
             "size": (10, 40), "speed": 0, "breed": 0.025, "meat": 1.5, "hide": 0.0, "bone": 0.0,
             "flee": 0.3, "danger": 0.0, "catch": 0.25},
}
PREY = ("rabbit", "deer", "bison", "fish")
DENSITY = {"rabbit": 45, "deer": 55, "bison": 110, "wolf": 180, "bear": 240, "fish": 35}   # habitat tiles per group


def populate(world) -> None:
    """The first animals: groups spread over the land each species likes."""
    rng = world.rng
    world.animals = []
    for sp in SPECIES:
        home = [t for row in world.tiles for t in row if t.biome in SPECIES[sp]["lives"]]
        if sp == "fish":
            home = [t for t in home if t.biome != "sea" or _by_land(world, t)]
        for _ in range(max(1, len(home) // DENSITY[sp])):
            t = home[rng.randrange(len(home))]
            lo, hi = SPECIES[sp]["size"]
            _spawn(world, sp, rng.randint(lo, (lo + hi) // 2), (t.x, t.y))
    index(world)


def _by_land(world, t) -> bool:
    c = world.cfg
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if not world.tiles[(t.y + dy) % c.height][(t.x + dx) % c.width].water:
            return True
    return False


def _spawn(world, sp: str, n: int, loc: tuple) -> dict:
    g = {"id": world.next_aid, "sp": sp, "n": n, "x": loc[0], "y": loc[1], "fx": loc[0], "fy": loc[1],
         "hunger": 0.2, "do": "graze"}
    world.next_aid += 1
    world.animals.append(g)
    return g


def index(world) -> None:
    world.herds = {}
    for g in world.animals:
        world.herds.setdefault((g["x"], g["y"]), []).append(g)


def near(world, loc: tuple, radius: int) -> list:
    c = world.cfg
    out = []
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            out.extend(world.herds.get(((loc[0] + dx) % c.width, (loc[1] + dy) % c.height), ()))
    return out


def fish_by(world, loc: tuple) -> dict | None:
    """The biggest school a person could fish from here: on this tile (a river) or in water beside it."""
    c = world.cfg
    best = None
    for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
        for g in world.herds.get(((loc[0] + dx) % c.width, (loc[1] + dy) % c.height), ()):
            if g["sp"] == "fish" and (best is None or g["n"] > best["n"]):
                best = g
    return best


def prey_here(world, loc: tuple) -> int:
    """How many huntable animals a person would find here: prey on the tile, plus fish in reach of it."""
    n = sum(g["n"] for g in near(world, loc, 0) if g["sp"] in PREY and g["n"] > 0)
    fish = fish_by(world, loc)
    if fish is not None and fish["n"] > 0:
        n += fish["n"]
    return n


def take_prey(world, loc: tuple) -> tuple:
    """A successful hunt: remove animals from one herd here and return (meat, hide, bone, species)."""
    prey = [g for g in near(world, loc, 0) if g["sp"] in PREY and g["n"] > 0]
    fish = fish_by(world, loc)
    if fish is not None and fish["n"] > 0:
        prey.append(fish)
    if not prey:
        return (0.0, 0.0, 0.0, "")
    g = prey[world.rng.randrange(len(prey))]
    sp = g["sp"]
    info = SPECIES[sp]
    taken = min(g["n"], 1 if info["meat"] >= 10 else max(1, round(10.0 / info["meat"])))
    g["n"] -= taken
    return (info["meat"] * taken, info["hide"] * taken, info["bone"] * taken, sp)


def _lives_on(world, sp: str, loc: tuple) -> bool:
    return world.tile(loc).biome in SPECIES[sp]["lives"]


def _move(world, g: dict, dest: tuple) -> None:
    g["x"], g["y"] = dest


def step(world) -> None:
    """One week of animal life, in a fixed order."""
    c = world.cfg
    rng = world.rng
    warm = world.season in (0, 1)
    index(world)
    # The land can only feed so many animals; beyond that, no young are raised.
    cap = max(60, (c.width * c.height) // 2)
    total = sum(g["n"] for g in world.animals)
    for g in list(world.animals):
        g["fx"], g["fy"] = g["x"], g["y"]
        if g["n"] <= 0:
            continue
        sp = SPECIES[g["sp"]]
        here = (g["x"], g["y"])
        speed = sp["speed"]
        if g["sp"] == "fish":
            g["do"] = "swim"
        elif sp["eats"] == "plants" or g["sp"] == "bear":
            _graze(world, g, sp)
        if sp["eats"] in ("meat", "both"):
            _hunt(world, g, sp)
        # Moving: away from danger, toward food, and toward shelter from the cold in winter.
        if speed and g["n"] > 0:
            threat = _threatened(world, g, sp)
            if threat or g["hunger"] > 0.35 or rng.random() < 0.15:
                best, best_v = here, -9.0
                for _ in range(8):
                    dest = ((here[0] + rng.randint(-speed, speed)) % c.width,
                            (here[1] + rng.randint(-speed, speed)) % c.height)
                    if not _lives_on(world, g["sp"], dest):
                        continue
                    if g["sp"] != "fish" and world.walk(None, here, dest)[0] != dest:
                        continue           # water in the way
                    t = world.tile(dest)
                    v = ((t.plants + t.embedded) / 40.0 if sp["eats"] in ("plants", "both") else 0.0)
                    if sp["eats"] in ("meat", "both"):
                        v += 0.5 * sum(1 for o in world.herds.get(dest, ()) if o["sp"] in sp["prey"])
                    if threat:
                        v += 0.4 * distance(dest, threat, c.width, c.height)
                    if world.season == 3:
                        v += 0.5 * t.temp
                    if t.fire > 0:
                        v -= 2.0        # every animal keeps away from fire
                    if v > best_v:
                        best, best_v = dest, v
                if best != here:
                    _move(world, g, best)
                    g["do"] = "flee" if threat else "roam"
        # Life and death.
        if warm and g["hunger"] < 0.5 and total < cap:
            births = int(g["n"] * sp["breed"] + rng.random())
            g["n"] += births
            total += births
        if g["hunger"] > 0.8:
            g["n"] -= max(1, g["n"] // 8)
        elif rng.random() < 0.01:
            g["n"] -= 1
        lo, hi = sp["size"]
        if g["n"] > hi:
            half = g["n"] // 2
            g["n"] -= half
            child = _spawn(world, g["sp"], half, (g["x"], g["y"]))
            child["hunger"] = g["hunger"]
    world.animals = [g for g in world.animals if g["n"] > 0]
    index(world)


def _graze(world, g: dict, sp: dict) -> None:
    t = world.tile((g["x"], g["y"]))
    need = g["n"] * sp.get("need", 0.5)
    if t.embedded > 0:                 # FX2: grazing takes from both stands in proportion
        tot = t.plants + t.embedded
        eaten = min(tot * 0.25, need)
        open_share = t.plants / tot
        t.plants -= eaten * open_share
        t.embedded -= eaten * (1.0 - open_share)
    else:
        eaten = min(t.plants * 0.25, need)
        t.plants -= eaten
    fed = eaten / need if need else 1.0
    if g["sp"] == "bear":
        fish = fish_by(world, (g["x"], g["y"]))
        if fish and fish["n"] > 2 and world.rng.random() < 0.4:
            fish["n"] -= 2
            fed = min(1.0, fed + 0.6)
    g["hunger"] = clamp(0.5 * g["hunger"] + 0.5 * (1.0 - fed))
    g["do"] = "graze"


def _threatened(world, g: dict, sp: dict):
    """The nearest thing this animal runs from: people (for prey) or a hunting pack."""
    if g["sp"] in ("wolf", "bear"):
        for q in world.people_near((g["x"], g["y"]), 1):
            if world.tile(q.loc).fire > 0:
                return q.loc
        return None
    rng = world.rng
    for q in world.people_near((g["x"], g["y"]), 1):
        if q.age(world.tick) >= 52 * 6 and rng.random() < sp["flee"]:
            return q.loc
    for o in near(world, (g["x"], g["y"]), 1):
        if o["sp"] == "wolf" and g["sp"] in SPECIES["wolf"]["prey"]:
            return (o["x"], o["y"])
    return None


def _hunt(world, g: dict, sp: dict) -> None:
    """Predators: hunt prey when hungry; a starving pack may go for a person alone."""
    rng = world.rng
    if g["sp"] == "wolf":
        g["hunger"] = clamp(g["hunger"] + 0.25)
    if g["hunger"] < 0.3:
        return
    c = world.cfg
    targets = [o for o in near(world, (g["x"], g["y"]), sp["speed"]) if o["sp"] in sp["prey"] and o["n"] > 0]
    if targets:
        o = min(targets, key=lambda o: (distance((g["x"], g["y"]), (o["x"], o["y"]), c.width, c.height), o["id"]))
        if world.tile((o["x"], o["y"])).fire <= 0:
            _move(world, g, (o["x"], o["y"]))
            g["do"] = "hunt"
            if rng.random() < min(0.85, 0.3 + 0.08 * g["n"]):
                o["n"] -= 3 if o["sp"] == "rabbit" else 1
                g["hunger"] = clamp(g["hunger"] - 0.7)
                return
    if g["hunger"] > 0.7:
        _go_for_people(world, g, sp)


def _go_for_people(world, g: dict, sp: dict) -> None:
    from .biology import die
    from .social import remember, witness
    rng = world.rng
    tick = world.tick
    for q in world.people_near((g["x"], g["y"]), 1):
        tile = world.tile(q.loc)
        if tile.fire > 0:
            continue
        company = [o for o in world.people_near(q.loc, 0, exclude=q.id) if o.age(tick) >= 52 * 14]
        if len(company) >= 2:
            continue                     # they keep away from people standing together
        if rng.random() >= 0.2 * g["hunger"] * sp["danger"] * (1.5 if q.age(tick) < 52 * 12 else 1.0):
            continue
        g["x"], g["y"] = q.loc
        q.health -= 20.0 + 30.0 * rng.random()
        killed = q.health <= 0
        eid = world.emit("mauled", None, q.id, q.loc, animal=g["sp"], killed=killed)
        if killed:
            q.hurt_by = g["sp"]
            die(world, q, "wolves" if g["sp"] == "wolf" else "a bear", None)
            g["hunger"] = 0.0
        else:
            remember(world, q, eid, "mauled", f"animal:{g['sp']}", q.id, q.loc, 0.9, -0.9)
            learn_fear(q, g["sp"], 0.5)
            q.fear = clamp(q.fear + 0.5)
        witness(world, eid, "mauled", f"animal:{g['sp']}", q.id, q.loc, chance=0.9)
        g["do"] = "attack"
        return


def surprised(world, p, loc: tuple) -> None:
    """A bear surprised while someone forages or hunts close by may attack."""
    from .biology import die
    from .social import remember, witness
    rng = world.rng
    for g in world.herds.get(loc, ()):
        if g["sp"] != "bear" or g["n"] <= 0 or world.tile(loc).fire > 0:
            continue
        if rng.random() < 0.06:
            p.health -= 25.0 + 30.0 * rng.random()
            killed = p.health <= 0
            eid = world.emit("mauled", None, p.id, loc, animal="bear", killed=killed)
            if killed:
                p.hurt_by = "bear"
                die(world, p, "a bear", None)
            else:
                remember(world, p, eid, "mauled", "animal:bear", p.id, loc, 0.9, -0.9)
                learn_fear(p, "bear", 0.5)
                p.fear = clamp(p.fear + 0.5)
            witness(world, eid, "mauled", "animal:bear", p.id, loc, chance=0.9)
            return


def learn_fear(p, sp: str, amount: float) -> None:
    key = f"fear:{sp}"
    p.expect[key] = clamp(p.expect.get(key, 0.0) + amount)


def fear_of(p, sp: str) -> float:
    return p.expect.get(f"fear:{sp}", 0.0)
