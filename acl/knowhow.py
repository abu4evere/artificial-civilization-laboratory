"""What people work out for themselves, and how it passes between them.

There is no list of discoveries. People learn three kinds of things:

1. **What things are worth.** When someone uses a thing they made and the
   result beats what they have come to expect, they value that kind of thing
   more. Things that don't help are valued less.
2. **How to make things.** Whatever someone makes, by accident or on purpose,
   they remember how. They remake the things they value, and forget how to
   make the things they don't.
3. **What to leave where.** People remember what they set down and where, and
   what they saw others set down. They notice when a spot later stands out from
   the land around it more than it did when the thing was left there, when a
   winter week there is warmer than they have come to expect, and when food
   left there kept better than food carried around. They link that to what was
   left there, and in which season. This is how leaving seeds in the ground, building up a heap of wood
   and hides, or keeping food by a fire could come to seem worthwhile. It is
   also how superstitions form: a stone left where the harvest happened to be
   good gets some of the credit.

All three pass on by teaching and by watching, imperfectly, and the learner
decides what to take (see information.py). What someone was told stays hearsay
until their own experience tests it. A result that contradicts what they
expected moves them more than one that confirms it (Law 66), and a big
surprise becomes a puzzle they may go back to (see inquiry.py).
"""
from __future__ import annotations

from . import inquiry
from .config import WEEKS_PER_YEAR
from .util import clamp

MAX_RECIPES = 12
MAX_PLACES = 8


def expectation(p, key: str, value: float, rate: float = 0.1) -> float:
    """Return what p expected for `key`, then update the expectation toward `value`."""
    before = p.expect.get(key)
    if before is None:
        p.expect[key] = value
        return value
    p.expect[key] = before + rate * (value - before)
    return before


# --- things and how to make them ------------------------------------------------

def judge_item(world, p, sig: str, felt: float) -> None:
    """Using a thing made the job this much easier, as far as the user could feel."""
    from .information import tested
    v = p.itemval.get(sig, 0.0)
    felt = clamp(felt, -1.0, 1.0)
    # Being proved wrong teaches more than being proved right (Law 66).
    rate = 0.3 if (abs(v) > 0.1 and (felt > 0.05) != (v > 0.05)) else 0.15
    p.itemval[sig] = clamp(v + rate * (felt - v), -1.0, 1.0)
    inquiry.surprised(world, p, "m:" + sig, v, felt)
    h = p.heard.get("m:" + sig)
    if h is not None:
        tested(world, p, "m:" + sig, felt - 0.5 * h[0])


def belief(p, key: str):
    """What p believes about leaving something somewhere ("seeds@0"): what they found out themselves,
    or failing that, what they were told and took on. None if neither."""
    v = p.beliefs.get(key)
    if v is not None:
        return v
    h = p.heard.get("b:" + key)
    return h[0] if h is not None else None


def remember_recipe(world, p, sig: str, recipe: dict, how: str, source=None, props=None, meant=None) -> None:
    fresh = sig not in p.recipes
    recipe = dict(recipe)
    if "parts" in recipe:
        recipe["parts"] = list(recipe["parts"])
    p.recipes[sig] = recipe
    p.itemval.setdefault(sig, 0.0)
    if len(p.recipes) > MAX_RECIPES:
        worst = min(p.recipes, key=lambda s: (p.itemval.get(s, 0.0), s))
        del p.recipes[worst]
    rec = world.knowledge.get(sig)
    if rec is None:
        world.knowledge[sig] = {"first_by": p.id, "first_tick": world.tick, "recipe": recipe,
                                "props": props, "lost": [], "alive": True}
    if fresh and how != "made":
        if meant and meant != sig:
            world.emit("learn", p.id, source, p.loc, thing=sig, how=how, meant=meant)
        else:
            world.emit("learn", p.id, source, p.loc, thing=sig, how=how)


def forget_useless(p) -> None:
    for sig in list(p.recipes):
        if p.itemval.get(sig, 0.0) < -0.15:
            del p.recipes[sig]
    for sig in list(p.itemval):
        if sig not in p.recipes and abs(p.itemval[sig]) < 0.05:
            del p.itemval[sig]


# --- what to leave where ------------------------------------------------------------

def placed(world, p, key: str, loc: tuple, season: int | None = None) -> None:
    """Remember leaving something here (or seeing it left), and how this spot compared with its surroundings."""
    season = world.season if season is None else season
    p.placements.append([world.tick, loc[0], loc[1], f"{key}@{season}", contrast(world, loc), world.tick])
    if len(p.placements) > 40:
        p.placements.pop(0)


def contrast(world, loc: tuple) -> float:
    """How much richer in plant food this spot is than the land around it, as anyone could see."""
    c = world.cfg
    t = world.tile(loc)
    around = 0.0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx or dy:
                n = world.tiles[(loc[1] + dy) % c.height][(loc[0] + dx) % c.width]
                around += n.plants + n.crop
    return (t.plants + t.crop) / (around / 8.0 + 5.0)


def look_around(world, p) -> None:
    """Back at a spot where something was left: does it stand out more than it did?"""
    if not p.placements:
        return
    loc = p.loc
    now = None
    for pl in p.placements:
        if pl[1] != loc[0] or pl[2] != loc[1] or world.tick - pl[5] < 4:
            continue
        if now is None:
            now = contrast(world, loc)
        surprise = now - pl[4]
        pl[5] = world.tick
        if abs(surprise) >= 0.1:
            _credit(world, p, pl[3], world.cfg.association_rate * clamp(surprise, -1.0, 1.0))


def look_at_traces(world, p) -> None:
    """Turned earth where someone sowed is as good as having watched them: p remembers it like a
    placement they saw, and later notices whether the spot came to stand out (Law 47, by observation)."""
    tile = world.tile(p.loc)
    for kind, (strength, tick) in list(tile.traces.items()):
        if not kind.startswith("sown@") or strength < 0.3:
            continue
        key = "seeds@" + kind[5:]
        if any(pl[1] == p.loc[0] and pl[2] == p.loc[1] and pl[3] == key and pl[0] >= tick for pl in p.placements):
            continue
        placed(world, p, "seeds", p.loc, int(kind[5:]))


def associate(world, p, loc: tuple, surprise: float, weight: float = 1.0) -> None:
    """Something went better or worse than expected here: credit what p left here this past year."""
    if abs(surprise) < 0.03 or not p.placements:
        return
    rate = world.cfg.association_rate * weight * clamp(surprise, -1.0, 1.0)
    cutoff = world.tick - WEEKS_PER_YEAR
    seen = []
    for t, x, y, key, _, _ in p.placements:
        if t >= cutoff and x == loc[0] and y == loc[1] and key not in seen:
            seen.append(key)
            _credit(world, p, key, rate)


def _credit(world, p, key: str, change: float) -> None:
    """p's own experience moves their belief about `key`. If they had only been told about it,
    this is the test of what they were told."""
    from .information import tested
    before = belief(p, key) or 0.0
    after = clamp(p.beliefs.get(key, 0.0) + change, -1.0, 1.0)
    p.beliefs[key] = after
    if "b:" + key in p.heard:
        tested(world, p, "b:" + key, change)
    # What they now expect a spot like this to do, against what it did.
    rate = max(world.cfg.association_rate, 1e-6)
    inquiry.surprised(world, p, "b:" + key, clamp(before / rate, -1.0, 1.0), clamp(change / rate, -1.0, 1.0))


def prune_placements(world, p) -> None:
    cutoff = world.tick - WEEKS_PER_YEAR
    p.placements = [pl for pl in p.placements if pl[0] >= cutoff]
    for key in list(p.beliefs):
        p.beliefs[key] *= 0.98
        if abs(p.beliefs[key]) < 0.01:
            del p.beliefs[key]
    # Hearsay nobody ever tested slowly stops seeming true.
    for key in list(p.heard):
        h = p.heard[key]
        h[0] = round(h[0] * 0.9, 3)
        if abs(h[0]) < 0.02:
            del p.heard[key]


def feel_place(p, loc: tuple, value: float) -> None:
    """How good this week was, remembered against where it was spent."""
    key = f"{loc[0]},{loc[1]}"
    v = p.places.get(key)
    p.places[key] = value if v is None else v + 0.1 * (value - v)
    for k in list(p.places):
        if k != key:
            p.places[k] *= 0.995
    if len(p.places) > MAX_PLACES:
        worst = min(p.places, key=lambda k: (p.places[k], k))
        del p.places[worst]


# --- passing it on ----------------------------------------------------------------------

def teach(world, teacher, learner, parent: bool = False) -> bool:
    """The teacher shows or tells something they value; the learner decides what to take. See information.py."""
    from .information import show_how
    return show_how(world, teacher, learner, parent)


def can_follow(learner, recipe: dict) -> bool:
    """A recipe that needs a made part can only be followed by someone who knows how to make that part."""
    for part in recipe.get("parts", ()):
        if part.startswith("(") or "/" in part:
            if part not in learner.recipes:
                return False
    return True


def watch(world, watcher, maker, sig: str, outcome: float) -> None:
    """Seeing someone do well with a thing can be enough to want one and work out how.
    Working it out from the outside goes wrong more often than being shown."""
    from .information import _recipe_as_shown, _sig_of
    if sig in watcher.recipes or sig not in maker.recipes or outcome <= 0:
        return
    if world.rng.random() >= 0.04 * (0.5 + watcher.genes["curiosity"]):
        return
    recipe = _recipe_as_shown(world, maker, watcher, maker.recipes[sig])
    if world.rng.random() < 0.15:
        recipe = _recipe_as_shown(world, maker, watcher, recipe)   # seen, not explained: twice the room for error
    copy = _sig_of(recipe)
    if copy in watcher.recipes or not can_follow(watcher, recipe):
        return
    remember_recipe(world, watcher, copy, recipe, "copied", maker.id, meant=sig)
    watcher.itemval[copy] = max(watcher.itemval.get(copy, 0.0), 0.3 * clamp(outcome))


def check_lost(world) -> None:
    """When nobody alive knows how to make something any more, it is lost."""
    known = set()
    for q in world.living():
        known.update(q.recipes)
    for sig, rec in world.knowledge.items():
        alive = sig in known
        if rec["alive"] and not alive:
            rec["alive"] = False
            rec["lost"].append(world.tick)
            world.emit("knowledge_lost", None, None, None, thing=sig)
        elif alive and not rec["alive"]:
            rec["alive"] = True
