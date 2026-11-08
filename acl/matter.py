"""The physics of things: what materials are like, and what happens when you
strike one against another, tie them together, press them into a shape, hold
them in a fire, wet them, set them down or burn them.

Every material and every made thing has ten lasting properties, each a whole
number from 0 to 100 (World Bible v8.1, first-stage rule: discrete core state;
0-100 keeps the fine differences the older physics depends on, such as a stick
barely sharpened on a stone):

    edge     how well it cuts
    reach    how long it is
    hard     how hard and heavy it is
    contain  how well it holds other things
    warm     how well it keeps cold out
    float    how well it floats
    tight    how well it keeps liquid in
    plastic  how readily it takes and keeps a shape when wet
    fuel     how well it burns, and how hot
    flex     how well it bends

and passing states on a 0-10 scale: how wet a thing is, and how hot a fire
burns; and, for something that holds things, what it holds.

Striking a brittle material with a harder one can flake it to an edge.
Binding two things with something flexible joins them: the longer reach adds
up, the sharper edge and harder body carry over. Flexible things joined to
flexible things cover more, so they hold and wrap better, though each extra
layer adds less than the one before. Where two coverings meet, the seam keeps
liquid in only as well as the binding does.

Heat follows the same few rules for everything: it dries what is wet; what
burns well catches and burns away; what was shaped while soft sets hard and
tight, harder and tighter the hotter the fire. Food is changed by heat too
(biology): it keeps longer and goes further.

Nobody in the world knows any of this. They find it out by trying, and they
judge what they make by what it does for them. How useful something is comes
only from its properties. There is no list of tools anywhere in the code, and
no step is named after anything people would later call it.
"""
from __future__ import annotations

from .util import clamp

MATERIALS = ("stone", "flint", "bone", "wood", "fiber", "hide", "clay", "char")
PROPS = ("edge", "reach", "hard", "contain", "warm", "float", "tight", "plastic", "fuel", "flex")

RAW = {
    #        edge reach hard contain warm float tight plastic fuel flex
    "stone": (10,  10,   80,  0,      0,   0,    0,    0,      0,   0),
    "flint": (25,  10,   70,  0,      0,   0,    0,    0,      0,   0),
    "bone":  (20,  30,   50,  0,      0,   3,    0,    0,      10,  10),
    "wood":  (5,   60,   35,  0,      0,   50,   40,   0,      60,  20),
    "fiber": (0,   10,   0,   25,     15,  15,   0,    0,      50,  90),
    "hide":  (0,   10,   0,   30,     45,  25,   60,   0,      20,  60),
    "clay":  (0,   10,   10,  0,      0,   0,    30,   80,     0,   30),   # wet ground by rivers and lakes
    "char":  (0,   10,   10,  0,      0,   0,    0,    0,      80,  0),    # what a burnt-out fire leaves
}
BRITTLE = {"stone": 35, "flint": 90, "bone": 55, "wood": 15, "fiber": 0, "hide": 0, "clay": 0, "char": 10}
SHARPEST = {"stone": 45, "flint": 95, "bone": 70, "wood": 30, "fiber": 0, "hide": 0, "clay": 0, "char": 0}
FLEXIBLE = tuple(m for m in MATERIALS if RAW[m][9] >= 50)      # what can tie things together
FORMS = ("hollow", "long", "point")                             # what soft stuff can be pressed into
SOFT_WHEN_WET = 4        # wetness at which plastic stuff can be shaped
DRY = 2                  # wetness at or below which a thing counts as dry


def item_from(sig: str, props: dict, wet: int = 0) -> dict:
    p = {k: int(max(0, min(100, props[k]))) for k in PROPS}
    uses = 15 + (30 * p["hard"] + 25 * p["warm"] + 20 * p["contain"]) // 100
    return {"sig": sig, **p, "uses": uses, "wet": wet, "holds": None}


def raw_props(kind: str) -> dict:
    d = dict(zip(PROPS, RAW[kind]))
    d["sig"] = kind
    return d


def strike(target: str, hammer: str, skill: float, rng, hammer_props: dict | None = None) -> dict | None:
    """Hit a raw material with another. Brittle things flake to an edge if the hammer is hard enough.
    OD1 (D4): the hammer may be a made thing; its own hardness sets the force."""
    t = raw_props(target)
    hm = hammer_props if hammer_props is not None else raw_props(hammer)
    force = min(100, (hm["hard"] * 100) // max(t["hard"], 1))
    skill100 = int(skill * 100)
    roll = rng.randrange(80, 101)
    quality = min(1000, BRITTLE[target] * force * (55 + (45 * skill100) // 100) * roll // 100_000)
    edge = t["edge"] + ((SHARPEST[target] - t["edge"]) * quality + 500) // 1000      # to the nearest step
    if edge <= t["edge"] + 2:
        return None
    t["edge"] = edge
    return item_from(f"{target}/{hammer}", t)


def sparks(target: str, hammer: str, hammer_props: dict | None = None) -> bool:
    """Flint struck against something hard throws sparks. OD1 (D4): a made hammer's hardness is its own."""
    hh = hammer_props["hard"] if hammer_props is not None else RAW[hammer][2]
    return "flint" in (target, hammer) and min(RAW[target][2], hh) >= 50


def _layer(x: int, y: int, binder: int) -> int:
    """Joining coverings: the bigger counts fully, the smaller half, the binding a little."""
    return max(x, y) + min(x, y) // 2 + (15 * binder) // 100


def bind(a: dict, b: dict, binder: str, binder_props: dict | None = None) -> dict:
    """Tie two things together with something flexible. OD1 (D3): the binder may be a made thing; its own properties
    enter where a raw binder's do."""
    bd = binder_props if binder_props is not None else raw_props(binder)
    flexible = int(a["flex"] >= 50) + int(b["flex"] >= 50) + 1
    p = {
        "edge": max(a["edge"], b["edge"]),
        "reach": min(100, a["reach"] + b["reach"]),
        "hard": max(a["hard"], b["hard"]),
        "contain": min(100, _layer(a["contain"], b["contain"], bd["contain"]) + 10 * flexible),
        "warm": min(100, _layer(a["warm"], b["warm"], bd["warm"])),
        "float": min(100, max(a["float"], b["float"]) + min(a["float"], b["float"]) // 2),
        "plastic": 0,
        "fuel": max(a["fuel"], b["fuel"], bd["fuel"]),
        "flex": (a["flex"] + b["flex"]) // 2,
    }
    # What holds liquid is whichever part holds things; where two holding parts meet, the seam is only
    # as tight as what binds them.
    holder = a if a["contain"] >= b["contain"] else b
    p["tight"] = holder["tight"]
    if a["contain"] > 0 and b["contain"] > 0:
        p["tight"] = min(max(a["tight"], b["tight"]), bd["tight"])
    parts = sorted((a["sig"], b["sig"]))
    return item_from(f"({parts[0]}+{parts[1]})#{binder}", p)


def shape(material: str, form: str, wet: int) -> dict | None:
    """Press a soft lump into a form. Only what is plastic, and wet enough, takes a shape."""
    p = raw_props(material)
    if p["plastic"] < 50 or wet < SOFT_WHEN_WET:
        return None
    if form == "hollow":
        p["contain"] = p["plastic"] - 20
    elif form == "long":
        p["reach"] = 20 + p["plastic"] // 2
    else:
        p["edge"] = 20
    return item_from(f"{material}~{form}", p, wet=wet)


def heat(thing: dict, level: int) -> tuple[dict | None, bool]:
    """Hold a thing in a fire of the given heat (0-10). Returns (what is left, whether it burned).

    The same rules for everything: heat dries; what burns well and is dry enough catches and is gone;
    what is plastic and dry sets hard and tight, the more so the hotter the fire, but if it goes into a
    hot fire still wet it cracks apart. A thing whose lasting properties changed gets a new name for
    what it now is (the old name, marked as heated)."""
    t = dict(thing)
    wet = t.get("wet", 0)
    if level >= 2:
        t["wet"] = 0
    if t["fuel"] >= 40 and level >= 4 and wet <= 3:
        return None, True
    if t["plastic"] >= 50 and level >= 5:
        if wet > DRY:
            return None, False           # cracked
        t["plastic"] = 0
        t["hard"] = max(t["hard"], 40 + 5 * level)
        t["tight"] = max(t["tight"], min(90, 10 * level))
        out = item_from(f"{thing['sig']}^{level}", t)
        out["uses"] += 10
        return out, False
    return t, False


def can_hold(item: dict, substance: str) -> int:
    """How much of a substance a thing can hold (0 if none): water needs it tight; embers need it
    not to burn, and hard enough to take the heat."""
    if substance == "water":
        return item["contain"] // 10 if item["contain"] >= 40 and item["tight"] >= 50 else 0
    if substance == "embers":
        return 6 if item["contain"] >= 30 and item["fuel"] <= 20 and item["hard"] >= 40 else 0
    return 0


def fire_heat(kind: str) -> int:
    """How hot a fire burns on this fuel, 0-10."""
    return RAW[kind][8] // 10


def fuel_of(kind: str) -> float:
    """How long a unit of this keeps a fire going, in weeks."""
    return RAW[kind][8] * 0.025


# --- what a thing does for you ------------------------------------------------

def factor(item: dict, use: str) -> float:
    """How much an item multiplies an effort. 1.0 means no help. (Properties on the 0-100 scale are
    read as fractions here, where they meet the efforts of the body.)"""
    e, r, h, c, w = (item["edge"] / 100, item["reach"] / 100, item["hard"] / 100, item["contain"] / 100,
                     item["warm"] / 100)
    if use == "forage":
        return 1.0 + 0.25 * e + 0.3 * c
    if use == "hunt":
        return 1.0 + 1.5 * e * r + 0.3 * h * r
    if use == "wood":
        return 1.0 + 1.2 * e * h
    if use in ("stone", "flint", "clay", "char"):
        return 1.0 + 0.5 * h
    if use == "fiber":
        return 1.0 + 0.6 * e
    if use == "fight":
        return 1.0 + 0.8 * e * r + 0.4 * h * r
    if use == "carry":
        return 1.0 + c
    if use == "cold":
        return 1.0 + w * (1.0 - item.get("wet", 0) / 20)      # wet things keep out less cold
    return 1.0


def best_item(p, use: str) -> tuple[int, float]:
    """The item p would reach for, and how much it helps."""
    best, best_f = -1, 1.0
    for i, it in enumerate(p.items):
        f = factor(it, use)
        if f > best_f + 1e-9:
            best, best_f = i, f
    return best, best_f


def best_float(p) -> tuple[int, float]:
    """The item p would use to cross water, and how well it floats (as a fraction). (-1, 0) if none."""
    best, best_f = -1, 0.0
    for i, it in enumerate(p.items):
        f = it.get("float", 0) / 100
        if f > best_f:
            best, best_f = i, f
    return best, best_f


def best_holder(p, substance: str) -> int:
    """The thing p would put a substance in: empty, and holding the most. -1 if none."""
    best, best_n = -1, 0
    for i, it in enumerate(p.items):
        n = can_hold(it, substance)
        if n > best_n and not it.get("holds"):
            best, best_n = i, n
    return best


def holding(p, substance: str) -> int:
    """Index of a thing p carries that holds some of this substance, or -1."""
    for i, it in enumerate(p.items):
        h = it.get("holds")
        if h and h[0] == substance and h[1] > 0:
            return i
    return -1


def wear(p, index: int) -> None:
    if index < 0:
        return
    it = p.items[index]
    it["uses"] -= 1
    if it["uses"] <= 0:
        p.items.pop(index)


def receive(world, p, kind: str, amount: float, loc: tuple, how: str) -> None:
    """Raw material coming to p at loc (spoils of a kill, an inheritance). FF2 (F4): with fix_mat_limit, what goes past
    the material limit is left on that tile's pile, kept and not deleted; 0 = v12 (p keeps it all). The runner's log
    (read by nothing here) counts the units past the limit either way."""
    over = min(amount, max(0.0, p.mat_total() + amount - material_cap(world, p)))          # OD1 (D2)
    log = getattr(world, "ff2log", None)
    if log is not None and over > 0:
        log.append(("mat_over", how, over))
    if world.cfg.fix_mat_limit and over > 0:
        tile = world.tile(loc)
        tile.pile[kind] = tile.pile.get(kind, 0.0) + over
        amount -= over
    p.mats[kind] += amount


def layered(p, use: str) -> float:
    """OD1 (D5): what several things do together for warmth worn or for carrying, by the law for joining coverings
    (`_layer`, as `bind` uses it): the best counts fully, each next one half, in order from the best down; capped at 100
    on the property scale (1.0 here), as `bind` caps it."""
    v = 0.0
    for e in sorted((factor(it, use) - 1.0 for it in p.items), reverse=True):
        if e <= 0:
            break
        v = min(1.0, max(v, e) + min(v, e) / 2)
    return 1.0 + v


def use_factor(world, p, use: str) -> float:
    """How much p's things help with this use: the single best thing (v16), or for warmth worn and carrying the layered
    whole (OD1, D5)."""
    if world is not None and world.cfg.layers_add and use in ("carry", "cold"):
        return layered(p, use)
    return best_item(p, use)[1]


def carry_capacity(world, p) -> float:
    return world.cfg.carry_limit * use_factor(world, p, "carry")


def item_cap(world, p) -> int:
    """How many made things p can carry. OD1 (D2, AF1's K): multiplied by the carry factor, as food is; the container
    counts toward its own limit."""
    if not world.cfg.containers_carry:
        return world.cfg.item_limit
    return int(world.cfg.item_limit * use_factor(world, p, "carry"))


def material_cap(world, p) -> float:
    """How much raw material p can carry. OD1 (D2, AF1's K): multiplied by the carry factor."""
    if not world.cfg.containers_carry:
        return world.cfg.material_limit
    return world.cfg.material_limit * use_factor(world, p, "carry")


def worn_warmth(p, world=None) -> float:
    """Share of cold kept out by what p wears."""
    return clamp(0.7 * (use_factor(world, p, "cold") - 1.0))


# --- piles of things on the ground ---------------------------------------------

def pile_shape(pile: dict) -> tuple[float, float]:
    """(enclosure, cover) of a heap of placed materials. Walls need long or heavy things; a roof needs flat ones."""
    enclosure = clamp(0.06 * pile.get("wood", 0) + 0.04 * pile.get("stone", 0) + 0.03 * pile.get("bone", 0))
    cover = clamp(0.12 * pile.get("hide", 0) + 0.05 * pile.get("fiber", 0) + 0.02 * pile.get("wood", 0))
    return enclosure, cover


def pile_warmth(pile: dict) -> float:
    enclosure, cover = pile_shape(pile)
    return enclosure * cover


def pile_room(pile: dict) -> int:
    enclosure, _ = pile_shape(pile)
    return 2 + int(8 * enclosure)
