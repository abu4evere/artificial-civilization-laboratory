"""Marks: scratches people leave on rock, wood and bare ground.

A mark is only a physical thing: three strokes cut into a surface, as deep as
the tool and the surface allow, slowly wearing away. Ground marks wash out in
weeks, wood marks in a few years, and rock marks last generations. A mark means
nothing. There is no list of meanings anywhere in the code (Law 22).

People make marks while fiddling with things in their hands, the same way
they strike and tie things together. Their hand draws partly by chance and
partly by copying marks they have seen, with slips (Law 23). It is also pulled
toward whichever known shape they already link, in their own mind, with what is
here and what is on their mind. That pull is the only bias built in, and it
points at nothing in particular. It only reinforces whatever links a person
already has.

People see the marks where they stop. Each person links each shape they see
with whatever is around it at that moment: food set down, a fire, water, a
shelter, a grave, animals, the person they saw make it. Links that keep holding
grow. Links that fail fade. People also carry a sense of how often each of those
things is around wherever they stop. A shape only tells them something when it
goes with a thing more often than that thing is around anyway: a mark always
seen by the river says nothing about water to people who live by the river.
When a shape does tell them something, meeting it where the thing is absent
makes them half expect the thing anyway.

Doing things leaves traces on the land: turned earth where seed went in, flakes
where stone was struck, ash, bones. Those can be noticed like anything else, so a
mark can come to go with what is done in a place, not only what is there.

Reading. A person who takes a shape to go with something, and meets the shape
where that thing is not, half expects it. If what the shape goes with is
something that can be checked or tried (water here, animals hunted here, seed
sown in some season, a kind of stone struck), the mark tells them so the way a
person would: as a claim, from the mark itself as its source. They weigh it by
how strongly the shape goes with that thing for them and by how marks of that
shape have turned out before, check it or try it, and remember whether the
mark was right (Laws 52, 56, 81, 115). A mark on rock can outlast everyone who
knew what it was about. That is all: single marks pointing at things and
practices. Nothing composes them into sentences.

If many people come to link the same shape with the same thing, that is shared
meaning, and the historian notes it. Or it never happens. Or it happens in one
band and not another, or it drifts over generations.
"""
from __future__ import annotations

from . import fauna, inquiry
from .matter import pile_warmth
from .util import clamp

STROKES = "|-/\\o^v."
SURFACES = {"rock": (0.75, 0.998), "wood": (0.35, 0.985), "ground": (0.05, 0.8)}   # hardness, share left each week
MARKERS = {"stone": 0.8, "flint": 0.7, "bone": 0.5}
MAX_ON_TILE = 6
MAX_KNOWN = 16
LINK_RATE = 0.2
SLIP = 0.06


def surfaces_at(tile) -> list:
    out = []
    if tile.rock > 0.3 or tile.pile.get("stone", 0.0) >= 2.0:
        out.append("rock")
    if tile.forest > 0.25 or tile.pile.get("wood", 0.0) >= 2.0:
        out.append("wood")
    if not tile.water:
        out.append("ground")
    return out


def tool_of(p) -> tuple[float, float]:
    """(hardness, edge) of the hardest thing in p's hands, or (0, 0)."""
    best = (0.0, 0.0)
    for m, hard in MARKERS.items():
        if p.mats.get(m, 0.0) >= 1.0 and hard > best[0]:
            best = (hard, 0.1)
    for it in p.items:
        if it["hard"] >= best[0] and (it["hard"], it["edge"]) > best:
            best = (it["hard"], it["edge"])
    return best


def can_mark(p, tile) -> bool:
    return tool_of(p)[0] > 0.0 and bool(surfaces_at(tile))


def around(world, loc) -> list:
    """What anyone stopping here could notice right now."""
    from .weather import fresh_near
    t = world.tile(loc)
    out = []
    if t.stash:
        out.append("food")
    if t.crop > 4.0:
        out.append("plants")
    if t.fire > 0:
        out.append("fire")
    if fresh_near(world, loc, 1):
        out.append("water")
    if t.pile and pile_warmth(t.pile) > 0.05:
        out.append("shelter")
    g = world.graves.get(f"{loc[0]},{loc[1]}")
    if g is not None and world.tick - g < 52 * 20:
        out.append("grave")
    for herd in fauna.near(world, loc, 1):
        if herd["sp"] not in out and herd["sp"] != "fish":
            out.append(herd["sp"])
    for kind, (strength, _) in t.traces.items():
        if strength >= 0.3:
            out.append(kind)
    return out


def _on_mind(p) -> list:
    """What p's own mind brings to the moment: the person or animal they are thinking about."""
    if not p.thoughts:
        return []
    kind, about, _ = p.thoughts[0]
    if kind == "dread" and about:
        return [about]
    if kind in ("grief", "missing", "love", "worry", "grudge", "fear") and about and about.startswith("p"):
        return ["p:" + about]
    return []


def make(world, p) -> bool:
    """p scratches a mark into something here. Returns False if nothing shows."""
    rng = world.rng
    tile = world.tile(p.loc)
    hard, edge = tool_of(p)
    surfaces = surfaces_at(tile)
    if hard <= 0 or not surfaces:
        return False
    surface = surfaces[rng.randrange(len(surfaces))]
    depth = clamp(hard - SURFACES[surface][0] + 0.4) * (0.6 + 0.4 * edge)
    if depth < 0.1:
        return False
    here = around(world, p.loc)
    shape, copied = _hand(world, p, here + _on_mind(p))
    tile.marks.append([shape, p.id, world.tick, round(depth, 3), surface])
    if len(tile.marks) > MAX_ON_TILE:
        tile.marks.pop(min(range(len(tile.marks)), key=lambda i: (tile.marks[i][3], i)))
    # The maker and anyone close by watching see it and what is around it, and who made it.
    _link(world, p, shape, here)
    for q in world.people_near(p.loc, 1, exclude=p.id):
        if q.age(world.tick) >= 52 * 3 and rng.random() < 0.5:
            _link(world, q, shape, here + ["p:" + p.id])
    world.emit("mark", p.id, None, p.loc, shape=shape, on=surface, copied=copied)
    return True


def _hand(world, p, cues: list) -> tuple[str, str]:
    """The shape p's hand draws: something new, or a known shape (with slips), pulled toward the
    shapes p already links with what is here and on their mind."""
    rng = world.rng
    shapes, weights = [], []
    for shape, (seen, _) in sorted(p.marks.items()):
        told = meaning(p, shape)
        primed = sum(told.get(k, 0.0) for k in cues)
        shapes.append(shape)
        weights.append((seen ** 0.5) * (1.0 + 3.0 * primed))
    shapes.append("")
    weights.append(1.0 + 1.5 * p.genes["curiosity"])
    pick = rng.random() * sum(weights)
    choice = shapes[-1]
    for s, w in zip(shapes, weights):
        pick -= w
        if pick <= 0:
            choice = s
            break
    if not choice:
        return "".join(STROKES[rng.randrange(len(STROKES))] for _ in range(3)), ""
    out = "".join(STROKES[rng.randrange(len(STROKES))] if rng.random() < SLIP else ch for ch in choice)
    return out, choice


def weather_away(world, tile) -> None:
    """Marks wear: ground marks fast, rock marks slowly."""
    keep = []
    for m in tile.marks:
        m[3] = round(m[3] * SURFACES[m[4]][1], 4)
        if m[3] >= 0.05:
            keep.append(m)
    tile.marks = keep


def see(world, p) -> None:
    """p looks at the marks where they stopped, and links each shape to what is around it."""
    if p.age(world.tick) < 52 * 3:
        return
    tile = world.tile(p.loc)
    here = around(world, p.loc)
    _usual(p, here)
    if not tile.marks:
        return
    for m in tile.marks:
        shape = m[0]
        if shape not in p.marks:
            inquiry.notice(world, p, "k:" + shape, 0.15 + 0.35 * p.genes["curiosity"])
        _link(world, p, shape, here)
        _expect(world, p, shape, here)


def _link(world, p, shape: str, here: list) -> None:
    e = p.marks.get(shape)
    if e is None:
        e = [0, {}]
        p.marks[shape] = e
    e[0] += 1
    links = e[1]
    for k in here:
        links[k] = round(links.get(k, 0.0) + LINK_RATE * (1.0 - links.get(k, 0.0)), 3)
    for k in list(links):
        if k not in here:
            links[k] = round(links[k] * 0.9, 3)
            if links[k] < 0.03:
                del links[k]
    if len(links) > 6:
        for k in sorted(links, key=lambda k: (links[k], k))[:len(links) - 6]:
            del links[k]
    if len(p.marks) > MAX_KNOWN:
        least = min(p.marks, key=lambda s: (p.marks[s][0], s))
        if least != shape:
            del p.marks[least]


def _usual(p, here: list) -> None:
    """How often each thing is around wherever p stops: the background a mark has to stand out from."""
    for k in BACKGROUND:
        key = "near:" + k
        v = p.expect.get(key, 0.0)
        p.expect[key] = round(v + 0.05 * ((1.0 if k in here else 0.0) - v), 4)


BACKGROUND = ("food", "plants", "fire", "water", "shelter", "grave",
              "rabbit", "deer", "bison", "wolf", "bear",
              "ash", "sown@0", "sown@1", "sown@2", "sown@3",
              "struck:stone", "struck:flint", "struck:bone", "struck:wood",
              "bones:rabbit", "bones:deer", "bones:bison")


def meaning(p, shape: str) -> dict:
    """What a shape tells p: how much more often each thing goes with it than is around anyway."""
    e = p.marks.get(shape)
    if e is None:
        return {}
    out = {}
    for k, w in e[1].items():
        base = p.expect.get("near:" + k, 0.0) if not k.startswith("p:") else 0.0
        if w - base > 0.0:
            out[k] = round(w - base, 3)
    return out


def _expect(world, p, shape: str, here: list) -> None:
    """A shape that tells p of something not here makes them half expect it anyway."""
    for k, w in meaning(p, shape).items():
        if w < 0.35 or k in here:
            continue
        if k in ("wolf", "bear"):
            fauna.learn_fear(p, k, 0.03 * w)
            p.fear = clamp(p.fear + 0.05 * w)
        elif k == "grave":
            p.fear = clamp(p.fear + 0.03 * w)
        elif k in ("food", "plants", "fire", "shelter", "ash"):
            key = f"{p.loc[0]},{p.loc[1]}"
            p.places[key] = p.places.get(key, 0.0) + 0.02 * w
        else:
            read(world, p, shape, k, w)


def read(world, p, shape: str, k: str, w: float) -> None:
    """A mark tells p something that can be checked or tried. p takes it as a claim from the mark."""
    from .information import _wonder, record
    source = "mark:" + shape
    if k == "water" or k.startswith("bones:"):
        key = ("w:" if k == "water" else "g:") + f"{p.loc[0]},{p.loc[1]}"
    elif k.startswith("sown@"):
        key = "b:seeds@" + k[5:]
        if key[2:] in p.beliefs:
            return                                    # they know for themselves
    elif k.startswith("struck:"):
        target = k[7:]
        if any(r_.get("verb") == "strike" and r_.get("target") == target for r_ in p.recipes.values()):
            return
        key = None
    else:
        return
    if key is not None and key in p.heard:
        return
    est, n = record(p, source)
    weight = n / (n + 3.0)
    c = clamp((1.0 - weight) * (0.2 + 0.6 * w) + weight * (0.05 + 0.95 * est))
    if world.rng.random() >= c:
        return
    if key is None:
        # A kind of stone struck here: try striking it with the hardest thing in hand.
        from .knowhow import remember_recipe
        tool = max(("stone", "flint", "bone"), key=lambda m: (p.mats.get(m, 0.0) >= 1.0, MARKERS[m]))
        if tool == target and p.mats.get(tool, 0.0) < 2.0:
            tool = "stone" if target != "stone" else "flint"
        sig = f"{target}/{tool}"
        remember_recipe(world, p, sig, {"verb": "strike", "target": target, "tool": tool}, "read", source)
        key = "m:" + sig
    p.heard[key] = [round(0.5 * c, 3), [source], world.tick]
    _wonder(world, p, key, 0.5 * c)
    world.emit("read", p.id, None, p.loc, shape=shape, means=k, claim=key)


def shared(world, min_people: int = 3, min_meaning: float = 0.3) -> list:
    """[(shape, thing, people)] for every shape that has been made in more than one place and that
    tells at least `min_people` living people the same thing (see `meaning`). A shape found in one
    spot only is that spot's mark, not yet a symbol. Read-only."""
    spots: dict = {}
    for row in world.tiles:
        for t in row:
            for m in t.marks:
                spots.setdefault(m[0], set()).add((t.x, t.y))
    count: dict = {}
    for q in world.living():
        for shape in q.marks:
            if len(spots.get(shape, ())) < 2:
                continue
            for k, w in meaning(q, shape).items():
                if w >= min_meaning:
                    count[(shape, k)] = count.get((shape, k), 0) + 1
    return sorted([(s, k, n) for (s, k), n in count.items() if n >= min_people],
                  key=lambda x: (-x[2], x[0], x[1]))
