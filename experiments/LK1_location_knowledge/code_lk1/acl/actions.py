"""What happens when someone acts. Each action changes the world, other people,
and how the actor feels about having done it. That feeling is what habits
learn from.
"""
from __future__ import annotations

from . import biology, fauna, information, inquiry, knowhow, marks, matter, social, thought
from .matter import MATERIALS, best_item, carry_capacity, pile_warmth
from .mind import COST, MOVE_COST, can_fill, can_make, forage_rate, hunger_of, hunt_chance, recipe_materials, strength
from .person import A, N_ACTIONS, Person
from .social import bump, remember, witness
from .util import clamp, distance
from .world_traces import leave_trace

STRIKABLE = ("stone", "flint", "bone", "wood")
HARD = ("stone", "flint", "bone")


def perform(world, p: Person, option: tuple) -> None:
    action, target = option
    c = world.cfg
    p.last_action = action
    dest = p.loc
    if action in ("forage", "hunt", "explore", "flee", "join"):
        dest = target
    elif action in ("gather", "take"):
        dest = target[0]
    elif action in ("give", "care", "talk", "court", "steal", "attack"):
        q = world.people[target]
        if not q.alive:
            return
        dest = q.loc
    d = distance(p.loc, dest, c.width, c.height)
    if d > c.reach:
        dest = world.step_toward_land(p.loc, dest, c.reach, p)
    # Walk there a tile at a time: water stops anyone with nothing that floats (Rule 3).
    start = p.loc
    dest, crossed = world.walk(p, p.loc, dest)
    d = distance(p.loc, dest, c.width, c.height)
    if action in ("give", "care", "talk", "court", "steal", "attack"):
        aim = target
    elif action in ("forage", "hunt", "explore", "flee", "join", "gather", "take"):
        aim = f"{dest[0]},{dest[1]}"
    else:
        aim = ""
    world.plan[p.id] = (p.loc, aim)
    world.move(p, dest)
    if action == "explore" and world.boat(p) >= 0.65 and p.voyage is None:
        there = world.island_of(target)
        if there is not None and there != world.island_of(start):
            p.voyage = [target[0], target[1], world.tick, world.island_of(start)]
    if crossed:
        _over_water(world, p, start)
    if p.age(world.tick) >= 6 * 52:
        knowhow.look_around(world, p)
        knowhow.look_at_traces(world, p)
    marks.see(world, p)
    p.energy = max(0.0, p.energy - COST[action] - MOVE_COST * d)
    eff = 1.0 - 0.1 * d
    if thought.state(p) == "overthinking":
        eff *= 0.85          # their mind is elsewhere
    p.doing = action
    if action in ("give", "care", "talk", "court", "steal", "attack") and \
            distance(p.loc, world.people[target].loc, c.width, c.height) > 1:
        return                 # they could not get there
    HANDLERS[action](world, p, target, eff)


def _over_water(world, p: Person, start: tuple) -> None:
    """p went over water on something that floats. Reaching land they could not walk to is what makes
    such a thing worth having, and whoever sees them come ashore sees it too (Law 109)."""
    idx, f = matter.best_float(p)
    if idx < 0 or f < 0.65:
        # Nothing floats under them any more: they struggle ashore, half drowned.
        world.move(p, world.nearest_land(p.loc))
        p.health -= 10.0
        p.hurt_by = p.hurt_by or "drowning"
        return
    sig = p.items[idx]["sig"]
    land = world.island_of(p.loc)
    origin = p.voyage[3] if p.voyage else world.island_of(start)
    if land is None:
        knowhow.judge_item(world, p, sig, 0.2)          # out on the water, not there yet
        return
    new = origin is not None and land != origin
    knowhow.judge_item(world, p, sig, 0.4 + (0.3 if new else 0.0))
    if new:
        world.emit("crossed", p.id, None, p.loc, **{"from": origin, "to": land, "thing": sig})
        p.voyage = None
        c = world.cfg
        for q in world.people_near(p.loc, c.perception, exclude=p.id):
            if q.age(world.tick) >= 6 * 52:
                knowhow.watch(world, q, p, sig, 0.6)


def _gain_skill(world, p: Person, skill: str) -> None:
    rate = world.cfg.skill_gain * (1.6 if thought.state(p) == "focused" else 1.0)
    p.skills[skill] = min(1.0, p.skills[skill] + rate * (1.0 - p.skills[skill]))


def _judge_use(world, p: Person, index: int, use: str) -> None:
    """Whatever was in hand made the job easier by however much its properties allow, and p feels it."""
    if index >= 0:
        it = p.items[index]
        knowhow.judge_item(world, p, it["sig"], matter.factor(it, use) - 1.0)


def _rest(world, p, target, eff):
    p.energy = min(100.0, p.energy + 40.0)
    p.health = min(p.max_health(world.tick), p.health + 2.0)
    p.reward += 0.05


def _forage(world, p, target, eff):
    c = world.cfg
    tile = world.tile(p.loc)
    hunger = hunger_of(world, p)
    idx, _ = best_item(p, "forage")
    room = max(0.0, carry_capacity(world, p) - p.edible())
    want = min(forage_rate(world, p) * eff, room)
    from_crop = min(tile.crop, want * 1.3)          # standing plants come away faster
    tile.crop -= from_crop
    from_wild = min(tile.plants, max(0.0, want - from_crop / 1.3))
    log = getattr(world, "aa1log", None)   # AA1 logging copy
    if log is not None:
        log.append(("forage", p.loc, tile.plants, from_wild))
    tile.plants -= from_wild
    got = from_crop + from_wild
    seed = got * c.seed_share[world.season] * (1.4 if from_crop > 0 else 1.0)
    p.seeds += seed
    p.food += got - seed
    _gain_skill(world, p, "foraging")
    _judge_use(world, p, idx, "forage")
    matter.wear(p, idx)
    _judge_carry(world, p)
    need = p.need(c, world.tick)
    p.reward += 0.3 * min(1.0, got / need) * (0.3 + 0.7 * hunger)
    if from_crop > 1.0:
        world.emit("harvest", p.id, None, p.loc, crop=round(from_crop, 2))
    world.emit("forage", p.id, None, p.loc, got=round(got, 2))
    fauna.surprised(world, p, p.loc)


def _judge_carry(world, p: Person) -> None:
    """A bag or basket proves itself when you are carrying more than bare hands could."""
    if p.edible() > world.cfg.carry_limit:
        idx, _ = best_item(p, "carry")
        if idx >= 0:
            knowhow.judge_item(world, p, p.items[idx]["sig"], 0.3)


def _hunt(world, p, target, eff):
    world.hunts.setdefault(p.loc, []).append(p.id)


def resolve_hunts(world) -> None:
    c = world.cfg
    rng = world.rng
    for loc, ids in world.hunts.items():
        hunters = [world.people[i] for i in ids if world.people[i].alive]
        if not hunters:
            continue
        n = len(hunters)
        skill = sum(h.skills["hunting"] for h in hunters) / n
        tools = [best_item(h, "hunt") for h in hunters]
        tool = sum(f for _, f in tools) / n
        chance = hunt_chance(world, n, skill, tool) if fauna.prey_here(world, loc) >= 1 else 0.0
        success = rng.random() < chance
        meat = hide = bone = 0.0
        sp = ""
        if success:
            meat, hide, bone, sp = fauna.take_prey(world, loc)
            if sp and sp != "fish":
                leave_trace(world.tile(loc), f"bones:{sp}", world.tick)
            if hide > 0:
                rng.choice(hunters).mats["hide"] += hide
            for _ in range(int(round(bone))):
                rng.choice(hunters).mats["bone"] += 1.0
            if sp == "fish":
                for h in hunters:
                    h.doing = "fish"     # fishing is its own quiet work
        share = meat / n
        for h, (idx, _) in zip(hunters, tools):
            got = min(share, max(0.0, carry_capacity(world, h) - h.edible()))
            h.food += got
            _gain_skill(world, h, "hunting")
            _judge_use(world, h, idx, "hunt")
            if idx >= 0:
                sig = h.items[idx]["sig"]
                for o in hunters:
                    if o is not h:
                        knowhow.watch(world, o, h, sig, h.itemval.get(sig, 0.0) if success else 0.0)
            matter.wear(h, idx)
            _judge_carry(world, h)
            need = h.need(c, world.tick)
            h.reward += 0.3 * min(1.0, got / need) if success else -0.05
            # Big animals fight back.
            danger = fauna.SPECIES[sp]["danger"] / n if sp else 0.0
            if rng.random() < c.hunt_injury * (1.0 - h.skills["hunting"]) + 0.3 * danger:
                h.health -= 15.0 + (20.0 * rng.random() if danger else 0.0)
                h.hurt_by = "hunting"
                world.emit("injured", h.id, None, loc, how="hunting", animal=sp)
                if danger:
                    fauna.learn_fear(h, sp, 0.3)
                    h.fear = clamp(h.fear + 0.2)
            if n > 1:
                h.contact = True
                for o in hunters:
                    if o is not h:
                        bump(h, o.id, world.tick, affection=0.04, familiarity=0.05,
                             trust=0.02, respect=0.02 if success else 0.0)
        world.emit("hunt", hunters[0].id, None, loc, party=[h.id for h in hunters],
                   success=success, meat=round(meat, 2), animal=sp)
        fauna.surprised(world, hunters[0], loc)


def _gather(world, p, target, eff):
    c = world.cfg
    loc, kind = target
    tile = world.tile(p.loc)
    idx, f = best_item(p, kind)
    rate = (c.gather_base + c.gather_skill * p.skills["crafting"]) * eff * f
    got = min(tile.material(kind), rate, max(0.0, c.material_limit - p.mat_total()))
    setattr(tile, kind, tile.material(kind) - got)
    if matter.RAW[kind][7] >= 50:          # soft earth comes up wet
        have = p.mats[kind]
        p.damp[kind] = (p.damp.get(kind, 0) * int(have) + 8 * int(got + 0.5)) // max(1, int(have) + int(got + 0.5))
    p.mats[kind] += got
    p.expect[f"handled:{kind}"] = 1.0
    _judge_use(world, p, idx, kind)
    matter.wear(p, idx)
    p.reward += 0.02
    p.doing = f"gather {kind}"
    world.emit("gather", p.id, None, p.loc, kind=kind, got=round(got, 2))


def _put(world, p, thing, eff):
    c = world.cfg
    tile = world.tile(p.loc)
    deps = sum(d.need(c, world.tick) for d in world.dependents(p.id))
    keep = 2.0 * (p.need(c, world.tick) + deps)
    if thing == "food":
        amount = min(p.food - keep, 60.0)
    elif thing == "seeds":
        amount = min(p.seeds - max(0.0, 0.5 * keep - p.food), 40.0)
    else:
        amount = min(p.mats[thing], 10.0)
    if amount < 1.0:
        return
    belief = p.beliefs.get(f"{thing}@{world.season}", 0.0)
    _, cover = matter.pile_shape(tile.pile)
    where = ""
    if thing == "food" or (thing == "seeds" and cover >= 0.3):
        kept = min(p.kept, p.food) * amount / p.food if thing == "food" and p.food > 0 else 0.0
        p.kept = max(0.0, p.kept - kept)
        p.food -= amount if thing == "food" else 0.0
        p.seeds -= amount if thing == "seeds" else 0.0
        for st in tile.stash:
            if st[0] == p.id:
                st[1] += amount if thing == "food" else 0.0
                st[2] += amount if thing == "seeds" else 0.0
                st[4] += amount
                if len(st) > 5:
                    st[5] += kept
                else:
                    st.append(kept)
                break
        else:
            tile.stash.append([p.id, amount if thing == "food" else 0.0, amount if thing == "seeds" else 0.0,
                               world.tick, amount, kept])
        where = "stash"
    elif thing == "seeds":
        p.seeds -= amount
        if tile.fire <= 0:
            tile.sown += amount * 0.85
            leave_trace(tile, f"sown@{world.season}", world.tick)
        where = "ground"
    else:
        p.mats[thing] -= amount
        if tile.fire > 0 and matter.RAW[thing][8] >= 40:
            wet = p.damp.get(thing, 0)
            tile.fire += amount * matter.fuel_of(thing) * (1.0 - wet / 12)
            if wet <= 3:
                tile.fire_heat = max(tile.fire_heat, matter.fire_heat(thing))
            where = "fire"
        else:
            tile.pile[thing] = tile.pile.get(thing, 0.0) + amount
            tile.builders[p.id] = tile.builders.get(p.id, 0.0) + amount
            where = "pile"
    knowhow.placed(world, p, thing, p.loc)
    for q in world.people_near(p.loc, 1, exclude=p.id):
        if q.age(world.tick) >= 6 * 52 and world.rng.random() < 0.5:
            knowhow.placed(world, q, thing, p.loc)
    p.doing = f"put {thing}"
    world.emit("put", p.id, None, p.loc, thing=thing, amount=round(amount, 2), into=where,
               warmth=round(pile_warmth(tile.pile), 3), belief=round(belief, 2))


def _take(world, p, target, eff):
    c = world.cfg
    loc, owner = target
    tile = world.tile(p.loc)
    entry = None
    for st in tile.stash:
        if st[0] == owner:
            entry = st
            break
    if entry is None:
        if owner == p.id:
            # It is gone. Someone took it, or it rotted away.
            knowhow.associate(world, p, p.loc, -0.6)
            p.anger = clamp(p.anger + 0.2)
            world.emit("found_gone", p.id, None, p.loc)
        return
    room = max(0.0, carry_capacity(world, p) - p.edible())
    food = min(entry[1], room)
    seeds = min(entry[2], max(0.0, room - food))
    if len(entry) > 5 and entry[1] > 0:
        kept = min(entry[5], entry[1]) * food / entry[1]
        entry[5] -= kept
        p.kept += kept
    entry[1] -= food
    entry[2] -= seeds
    p.food += food
    p.seeds += seeds
    weeks = world.tick - entry[3]
    if entry[1] + entry[2] < 0.2:
        tile.stash.remove(entry)
    if owner == p.id:
        if weeks >= 2 and entry[4] > 0:
            kept = (food + seeds + entry[1] + entry[2]) / entry[4]
            loose = (1.0 - c.spoil_rate) ** weeks
            knowhow.associate(world, p, p.loc, kept - loose)
        entry[4] = entry[1] + entry[2]
        entry[3] = world.tick
        world.emit("take", p.id, None, p.loc, food=round(food + seeds, 2), weeks=weeks, own=True)
        p.reward += 0.1
        return
    o = world.people.get(owner)
    eid = world.emit("take", p.id, owner, p.loc, food=round(food + seeds, 2), weeks=weeks, own=False)
    p.reward += 0.3 * min(1.0, (food + seeds) / p.need(c, world.tick))
    if o is not None and o.alive and distance(o.loc, p.loc, c.width, c.height) <= c.perception \
            and world.rng.random() < 0.7:
        bump(o, p.id, world.tick, trust=-0.4, affection=-0.3, grudge=0.25 + 0.2 * o.genes["temper"])
        o.anger = clamp(o.anger + 0.3)
        remember(world, o, eid, "stole", p.id, o.id, p.loc, 0.6, -0.6)
        witness(world, eid, "stole", p.id, o.id, p.loc, chance=0.4)
        world.emit("steal", p.id, owner, p.loc, amount=round(food + seeds, 2), noticed=True, stash=True)


def _make(world, p, sig, eff):
    recipe = p.recipes.get(sig)
    if recipe is None:
        return
    item = _craft(world, p, recipe)
    if item is not None:
        p.reward += 0.1
        p.doing = "make"
        world.emit("make", p.id, None, p.loc, thing=item["sig"], **_props(item))


def _craft(world, p: Person, recipe: dict):
    """Carry out a recipe if the inputs are in hand. Returns the new item."""
    if not can_make(p, recipe):
        return None
    rng = world.rng
    _gain_skill(world, p, "crafting")
    if recipe["verb"] == "shape":
        m = recipe["material"]
        item = matter.shape(m, recipe["form"], p.damp.get(m, 0))
        if item is None:
            return None
        p.mats[m] -= 1.0
    elif recipe["verb"] == "heat":
        return _hold_in_fire(world, p, recipe["part"])
    elif recipe["verb"] == "strike":
        p.mats[recipe["target"]] -= 1.0
        item = matter.strike(recipe["target"], recipe["tool"], p.skills["crafting"], rng)
        sig = f"{recipe['target']}/{recipe['tool']}"
        knowhow.placed(world, p, sig, p.loc)
        leave_trace(world.tile(p.loc), f"struck:{recipe['target']}", world.tick, 0.5)
        if matter.sparks(recipe["target"], recipe["tool"]):
            # Sparks fly, and sometimes something catches. Either can be a surprise.
            got = 1.0 if _spark(world, p) else 0.5
            before = p.expect.get("fire:" + sig, 0.0)
            p.expect["fire:" + sig] = round(before + 0.3 * (got - before), 3)
            inquiry.surprised(world, p, "f:" + sig, before, got)
    else:
        parts = []
        for part in recipe["parts"]:
            if part in MATERIALS:
                p.mats[part] -= 1.0
                parts.append(matter.raw_props(part))
            else:
                for i, it in enumerate(p.items):
                    if it["sig"] == part:
                        parts.append(p.items.pop(i))
                        break
        p.mats[recipe["binder"]] -= 1.0
        item = matter.bind(parts[0], parts[1], recipe["binder"])
    if item is None:
        return None
    _keep(p, item, world.cfg.item_limit)
    return item


def _hold_in_fire(world, p: Person, part: str):
    """Hold a material or a made thing in the fire here. What comes out changed is a new thing; what
    burns feeds the fire; what was only wet comes out dry."""
    tile = world.tile(p.loc)
    if tile.fire <= 0:
        return None
    level = tile.fire_heat
    if part in MATERIALS:
        thing = matter.raw_props(part)
        thing["wet"] = p.damp.get(part, 0)
        p.mats[part] -= 1.0
        index = None
    else:
        index = next((i for i, it in enumerate(p.items) if it["sig"] == part), None)
        if index is None:
            return None
        thing = p.items.pop(index)
    out, burned = matter.heat(thing, level)
    if burned:
        tile.fire += thing["fuel"] * 0.025
        return None
    if out is None:
        leave_trace(tile, "shards", world.tick, 0.5)        # it cracked
        return None
    if out["sig"] == thing["sig"]:
        # Nothing lasting changed: it is only drier.
        if index is None:
            p.mats[part] += 1.0
            p.damp.pop(part, None)
        else:
            p.items.insert(index, out)
        return None
    _keep(p, out, world.cfg.item_limit)
    return out


def _keep(p: Person, item: dict, limit: int) -> None:
    p.items.append(item)
    while len(p.items) > limit:
        worst = min(range(len(p.items)), key=lambda i: (p.itemval.get(p.items[i]["sig"], 0.0), -i))
        p.items.pop(worst)


def _props(item: dict) -> dict:
    return {k: item[k] for k in matter.PROPS}


def _spark(world, p: Person) -> None:
    """A spark lands. If there is something dry to catch, it catches."""
    c = world.cfg
    tile = world.tile(p.loc)
    if tile.fire > 0 or world.rng.random() >= c.spark_chance:
        return False
    tinder = tile.pile.get("fiber", 0.0) + tile.pile.get("wood", 0.0)
    if tinder >= 0.5:
        burned = min(tile.pile.get("wood", 0.0), 3.0)
        tile.pile["wood"] = tile.pile.get("wood", 0.0) - burned
        tile.pile.pop("fiber", None)
        tile.fire = 1.0 + burned * c.wood_fuel
        tile.fire_heat = matter.fire_heat("wood" if burned > 0 else "fiber")
    elif p.mats["fiber"] >= 1.0 and p.damp.get("fiber", 0) <= 5:      # damp catches; soaked does not
        p.mats["fiber"] -= 1.0
        tile.fire = 1.0
        tile.fire_heat = matter.fire_heat("fiber")
    else:
        return False
    world.emit("fire", p.id, None, p.loc, how="sparks")
    return True


def _play(world, p, target, eff):
    """Fiddle with what is in hand: strike one thing with another, tie things together, or
    scratch at a surface."""
    rng = world.rng
    _gain_skill(world, p, "crafting")
    tile = world.tile(p.loc)
    if marks.can_mark(p, tile):
        drawn = max((pz[0] for k, pz in p.puzzles.items() if k.startswith("k:")), default=0.0)
        if rng.random() < world.cfg.mark_chance + 0.4 * drawn:
            if marks.make(world, p):
                p.reward += 0.03 * p.genes["curiosity"]
                return
    have = [m for m in MATERIALS if p.mats[m] >= 1.0]
    choices = []
    for t in have:
        if t in STRIKABLE:
            for h in HARD:
                if p.mats[h] >= (2.0 if h == t else 1.0):
                    choices.append({"verb": "strike", "target": t, "tool": h})
    for m in have:
        if matter.RAW[m][7] >= 50 and p.damp.get(m, 0) >= matter.SOFT_WHEN_WET:
            for form in matter.FORMS:
                choices.append({"verb": "shape", "material": m, "form": form})
    if tile.fire > 0:
        for part in have + [it["sig"] for it in p.items]:
            choices.append({"verb": "heat", "part": part, "level": tile.fire_heat})
    for substance in ("water", "embers", "pour"):
        if _can_fill(world, p, substance):
            choices.append({"verb": "fill", "substance": substance})
    binders = [b for b in matter.FLEXIBLE if p.mats[b] >= 1.0]
    if binders:
        parts = [m for m in MATERIALS] + [it["sig"] for it in p.items]
        for b in binders:
            for i, a in enumerate(parts):
                for bb in parts[i:]:
                    trial = {"verb": "bind", "parts": sorted([a, bb]), "binder": b}
                    if can_make(p, trial):
                        choices.append(trial)
    if not choices:
        p.reward -= 0.01
        return
    untried = [r for r in choices if _sig_of(r) not in p.recipes and _sig_of(r) not in p.expect]
    pool = untried if untried and rng.random() < 0.7 else choices
    # Puzzling over something they made: try things like it (deliberate variation).
    if p.thoughts and p.thoughts[0][0] == "puzzle" and p.thoughts[0][1][:2] in ("m:", "f:"):
        rec = p.recipes.get(p.thoughts[0][1][2:])
        if rec is not None:
            mats = set(recipe_materials(rec))
            near = [r for r in choices if mats & set(recipe_materials(r))]
            if near and rng.random() < 0.6:
                pool = near
    recipe = pool[rng.randrange(len(pool))]
    p.expect[_sig_of(recipe)] = 0.0
    if recipe["verb"] == "fill":
        _fill(world, p, recipe["substance"], 1.0)
        return
    item = _craft(world, p, recipe)
    if item is None:
        world.emit("play", p.id, None, p.loc, thing=None)
        return
    knowhow.remember_recipe(world, p, item["sig"], recipe, "made", props=_props(item))
    p.reward += 0.05
    world.emit("play", p.id, None, p.loc, thing=item["sig"], **_props(item))


def _sig_of(recipe: dict) -> str:
    from .information import _sig_of as sig_of
    return sig_of(recipe)


def _heat_food(world, p, target, eff):
    """Hold food in the fire here. It will keep longer and go further."""
    tile = world.tile(p.loc)
    p.expect["tried:heat:food"] = 1.0
    if tile.fire <= 0:
        return
    amount = min(p.food - min(p.kept, p.food), 15.0 * eff)
    if amount < 1.0:
        return
    p.kept += amount
    p.reward += 0.02
    p.doing = "heat food"
    world.emit("heat", p.id, None, p.loc, thing="food", amount=round(amount, 2))


def _can_fill(world, p, substance: str) -> bool:
    return can_fill(world, p, substance)


def _fill(world, p, substance, eff):
    """Fill something carried with water or embers, or tip embers out onto dry fuel."""
    p.expect["tried:fill:" + substance] = 1.0
    if not _can_fill(world, p, substance):
        return
    tile = world.tile(p.loc)
    if substance in ("water", "embers"):
        it = p.items[matter.best_holder(p, substance)]
        it["holds"] = [substance, matter.can_hold(it, substance)]
        if substance == "embers":
            tile.fire = max(0.0, tile.fire - 0.5)
        p.doing = f"fill with {substance}"
        world.emit("fill", p.id, None, p.loc, substance=substance, **{"with": it["sig"]})
        return
    # Tip the embers out onto something dry that burns.
    it = p.items[matter.holding(p, "embers")]
    it["holds"] = None
    kind = next(k for k in ("char", "wood", "fiber") if p.mats.get(k, 0.0) >= 1.0 and p.damp.get(k, 0) <= 5)
    p.mats[kind] -= 1.0
    tile.fire = 1.0 + matter.fuel_of(kind)
    tile.fire_heat = matter.fire_heat(kind)
    cold = weather_cold(world, p)
    got = 1.0 if cold > 0.3 else 0.5
    before = p.expect.get("fire:embers", 0.0)
    p.expect["fire:embers"] = round(before + 0.3 * (got - before), 3)
    inquiry.surprised(world, p, "f:embers", before, got)
    knowhow.judge_item(world, p, it["sig"], 0.3 * got)
    p.doing = "light a fire"
    world.emit("fire", p.id, None, p.loc, how="embers", **{"with": it["sig"]})
    world.emit("consequence", p.id, None, p.loc, what="fire_carried")


def weather_cold(world, p) -> float:
    from .weather import coldness
    return coldness(world, p.loc)


def _explore(world, p, target, eff):
    p.reward += 0.03 * p.genes["curiosity"]
    world.emit("explore", p.id, None, p.loc)


def _give(world, p, target, eff):
    c = world.cfg
    q = world.people[target]
    need = p.need(c, world.tick)
    q_need = q.need(c, world.tick)
    keep = need * 1.5
    amount = min(p.edible() - keep, q_need * 2.0, max(0.0, carry_capacity(world, q) - q.edible()))
    if amount <= 0.5:
        return
    from_food = min(p.food, amount)
    p.food -= from_food
    p.seeds -= amount - from_food
    q.food += from_food
    q.seeds += amount - from_food
    owed_before = q.rel[p.id].balance if p.id in q.rel else 0.0
    bump(q, p.id, world.tick, affection=0.08 * min(1.0, amount / q_need), trust=0.05,
         respect=0.04, familiarity=0.05, balance=amount)
    bump(p, q.id, world.tick, affection=0.03, familiarity=0.05, balance=-amount)
    p.contact = q.contact = True
    kin = world.kinship(p, q)
    p.reward += 0.1 + 0.2 * p.genes["kindness"] + 0.2 * kin
    if owed_before < 0:
        # p is paying back an earlier gift: q's habit of giving just paid off.
        i = q.last_ctx * N_ACTIONS + A["give"]
        q.q[i] = clamp(q.q[i] + world.cfg.learning_rate * 0.5, -1.5, 1.5)
    eid = world.emit("give", p.id, q.id, p.loc, amount=round(amount, 2), returned=owed_before < 0)
    remember(world, q, eid, "gave", p.id, q.id, p.loc, 0.15 + 0.3 * clamp(1.0 - q.edible() / (2 * q_need)), 0.6)


def _care(world, p, target, eff):
    q = world.people[target]
    q.health = min(q.max_health(world.tick), q.health + 4.0)
    q.cared = True
    p.contact = q.contact = True
    bump(p, q.id, world.tick, affection=0.05, familiarity=0.05)
    bump(q, p.id, world.tick, affection=0.05, familiarity=0.05, trust=0.03, respect=0.02)
    p.reward += 0.1 + 0.3 * p.genes["care"] * world.kinship(p, q)
    world.emit("care", p.id, q.id, p.loc)


def _talk(world, p, target, eff):
    q = world.people[target]
    g, h = p.genes, q.genes
    compat = 1.0 - abs(g["sociability"] - h["sociability"]) - 0.5 * abs(g["kindness"] - h["kindness"]) \
        - 0.5 * abs(g["temper"] - h["temper"])
    bump(p, q.id, world.tick, affection=0.05 * compat, familiarity=0.08)
    bump(q, p.id, world.tick, affection=0.05 * compat, familiarity=0.08)
    p.contact = q.contact = True
    p.loneliness = clamp(p.loneliness - 0.3)
    q.loneliness = clamp(q.loneliness - 0.3)
    # Each tells the other something; each listener decides what to make of it.
    social.gossip(world, p, q)
    if q.age(world.tick) >= 52 * 3 and world.rng.random() < 0.3 + 0.4 * h["sociability"]:
        social.gossip(world, q, p)
    # Who has turned out right, and who wrong; and where there is water, or game.
    if q.age(world.tick) >= 52 * 6:
        information.share_reputation(world, p, q)
        if world.rng.random() < 0.5:
            information.tell_place(world, p, q)
    if q.age(world.tick) >= 52 * 4:
        parent = p.id in (q.mother, q.father, q.caregiver)
        if knowhow.teach(world, p, q, parent):
            bump(q, p.id, world.tick, respect=0.1)
            p.reward += 0.1
    _imitate(world, q, p)
    p.reward += 0.1 + 0.1 * g["sociability"]
    world.emit("talk", p.id, q.id, p.loc)


def _imitate(world, learner: Person, model: Person) -> None:
    """People pick up the habits of those they look up to, or who seem to be doing well."""
    r = learner.rel.get(model.id)
    respect = r.respect if r else 0.0
    if respect < 0.2 and model.mood <= learner.mood + 0.1:
        return
    rate = world.cfg.imitation_rate * (0.5 + learner.genes["curiosity"]) * (0.5 + respect)
    lq, mq = learner.q, model.q
    for i in range(len(lq)):
        lq[i] += rate * (mq[i] - lq[i])


def _court(world, p, target, eff):
    q = world.people[target]
    p.contact = q.contact = True
    if p.partner == q.id:
        bump(p, q.id, world.tick, affection=0.05, familiarity=0.03)
        bump(q, p.id, world.tick, affection=0.05, familiarity=0.03)
        world.courting.append((p.id, q.id))
        p.reward += 0.2
        return
    if p.partner is not None or q.partner is not None:
        return
    r = q.rel.get(p.id)
    attraction = (0.25 + 0.2 * q.genes["sociability"] + (r.affection if r else 0.0)
                  + 0.2 * (r.respect if r else 0.0) + 0.1 * min(p.health, 100.0) / 100.0)
    if attraction > 0.55 and world.rng.random() < 0.6:
        p.partner, q.partner = q.id, p.id
        bump(p, q.id, world.tick, affection=0.2, trust=0.1)
        bump(q, p.id, world.tick, affection=0.2, trust=0.1)
        eid = world.emit("pair", p.id, q.id, p.loc)
        remember(world, p, eid, "paired", p.id, q.id, p.loc, 0.7, 0.9)
        remember(world, q, eid, "paired", p.id, q.id, p.loc, 0.7, 0.9)
        p.reward += 0.5
    else:
        bump(q, p.id, world.tick, affection=0.04 * q.genes["sociability"], familiarity=0.03)
        bump(p, q.id, world.tick, affection=0.03, familiarity=0.03)
        p.reward += 0.03


def _steal(world, p, target, eff):
    c = world.cfg
    rng = world.rng
    q = world.people[target]
    need = p.need(c, world.tick)
    amount = min(q.food * 0.5, need * 2.0, max(0.0, carry_capacity(world, p) - p.edible()))
    if amount <= 0:
        return
    q.food -= amount
    p.food += amount
    noticed = rng.random() < 0.4 + 0.4 * q.genes["anxiety"]
    p.reward += 0.3 * min(1.0, amount / need) - (0.2 if noticed else 0.0)
    eid = world.emit("steal", p.id, q.id, p.loc, amount=round(amount, 2), noticed=noticed)
    if noticed:
        bump(q, p.id, world.tick, trust=-0.4, affection=-0.3, grudge=0.3 + 0.2 * q.genes["temper"])
        q.anger = clamp(q.anger + 0.3)
        remember(world, q, eid, "stole", p.id, q.id, p.loc, 0.6, -0.6)
        witness(world, eid, "stole", p.id, q.id, p.loc, chance=0.4)
        if (q.age(world.tick) >= 52 * 14 and q.energy >= 20
                and rng.random() < 0.6 * q.genes["temper"] * q.genes["boldness"] + 0.1 * q.anger):
            q.energy -= 20
            _attack(world, q, p.id, 1.0)


def _attack(world, p, target, eff):
    rng = world.rng
    q = world.people[target]
    tick = world.tick
    sp, sq = strength(world, p), strength(world, q)
    if sp + sq <= 0:
        return
    idx, _ = best_item(p, "fight")
    if rng.random() < sp / (sp + sq):
        q.health -= 25.0 + 30.0 * rng.random()
        p.health -= 5.0 * rng.random()
    else:
        p.health -= 15.0 + 20.0 * rng.random()
        q.health -= 5.0 * rng.random()
    matter.wear(p, idx)
    p.anger = clamp(p.anger - 0.3)
    bump(p, q.id, tick, grudge=-0.4)
    killed = q.health <= 0
    kind = "killed" if killed else "attacked"
    eid = world.emit("kill" if killed else "attack", p.id, q.id, p.loc)
    if killed:
        q.hurt_by = "violence"
        bump(p, q.id, tick, grudge=-1.0)
        biology.die(world, q, "killed", p.id)
        p.reward += 0.3 * p.genes["temper"] - 0.2 * p.genes["kindness"]
    else:
        bump(q, p.id, tick, grudge=0.5, trust=-0.6, affection=-0.5)
        q.anger = clamp(q.anger + 0.5)
        q.fear = clamp(q.fear + 0.3 * (1.0 - q.genes["boldness"]))
        remember(world, q, eid, "attacked", p.id, q.id, p.loc, 0.8, -0.9)
        p.reward += 0.1
    if p.health <= 0:
        p.hurt_by = "violence"
        biology.die(world, p, "killed", q.id if q.alive else None)
    witness(world, eid, kind, p.id, q.id, p.loc)


def _flee(world, p, target, eff):
    p.fear = clamp(p.fear - 0.2)
    p.reward += 0.05
    world.emit("flee", p.id, None, p.loc)


def _join(world, p, target, eff):
    for q in world.people_near(p.loc, 0, exclude=p.id):
        r = p.rel.get(q.id)
        if q.id == p.partner or (r and r.affection > 0.3):
            p.contact = True
            break
    p.reward += 0.03


HANDLERS = {
    "rest": _rest, "forage": _forage, "hunt": _hunt, "gather": _gather, "put": _put,
    "take": _take, "make": _make, "play": _play, "explore": _explore, "give": _give,
    "heat": _heat_food, "fill": _fill,
    "care": _care, "talk": _talk, "court": _court, "steal": _steal, "attack": _attack,
    "flee": _flee, "join": _join,
}
