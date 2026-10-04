"""The physics of things: what materials are like, and what happens when you
strike one against another, tie them together, set them down or burn them.

Every raw material has five physical properties:

    edge     how well it cuts
    reach    how long it is
    hard     how hard and heavy it is
    contain  how well it holds other things
    warm     how well it keeps cold out

Striking a brittle material with a harder one can flake it to an edge.
Binding two things with something flexible joins them: the longer reach adds
up, the sharper edge and harder body carry over. Flexible things joined to
flexible things cover more, so they hold and wrap better, though each extra
layer adds less than the one before. Nobody in the world knows any of this. They find
it out by trying, and they judge what they make by what it does for them.

How useful something is comes only from its properties. There is no list of
tools anywhere in the code.
"""
from __future__ import annotations

from .util import clamp

MATERIALS = ("stone", "flint", "bone", "wood", "fiber", "hide")
PROPS = ("edge", "reach", "hard", "contain", "warm", "float")

RAW = {
    #         edge   reach  hard  contain warm  float
    "stone": (0.10, 0.10, 0.80, 0.00, 0.00, 0.00),
    "flint": (0.25, 0.10, 0.70, 0.00, 0.00, 0.00),
    "bone":  (0.20, 0.30, 0.50, 0.00, 0.00, 0.03),
    "wood":  (0.05, 0.60, 0.35, 0.00, 0.00, 0.50),
    "fiber": (0.00, 0.10, 0.00, 0.25, 0.15, 0.15),
    "hide":  (0.00, 0.10, 0.00, 0.30, 0.45, 0.25),
}
BRITTLE = {"stone": 0.35, "flint": 0.9, "bone": 0.55, "wood": 0.15, "fiber": 0.0, "hide": 0.0}
SHARPEST = {"stone": 0.45, "flint": 0.95, "bone": 0.7, "wood": 0.3, "fiber": 0.0, "hide": 0.0}
FLEXIBLE = ("fiber", "hide")


def item_from(sig: str, edge, reach, hard, contain, warm, float_) -> dict:
    uses = int(15 + 30 * hard + 25 * warm + 20 * contain)
    return {"sig": sig, "edge": round(edge, 3), "reach": round(reach, 3), "hard": round(hard, 3),
            "contain": round(contain, 3), "warm": round(warm, 3), "float": round(float_, 3), "uses": uses}


def raw_props(kind: str) -> dict:
    e, r, h, c, w, fl = RAW[kind]
    return {"sig": kind, "edge": e, "reach": r, "hard": h, "contain": c, "warm": w, "float": fl,
            "flex": kind in FLEXIBLE}


def strike(target: str, hammer: str, skill: float, rng) -> dict | None:
    """Hit a raw material with another. Brittle things flake to an edge if the hammer is hard enough."""
    t, hm = RAW[target], RAW[hammer]
    force = clamp(hm[2] / max(t[2], 0.1))
    quality = BRITTLE[target] * force * (0.55 + 0.45 * skill) * (0.8 + 0.2 * rng.random())
    edge = t[0] + (SHARPEST[target] - t[0]) * clamp(quality)
    if edge <= t[0] + 0.02:
        return None
    return item_from(f"{target}/{hammer}", edge, t[1], t[2] * 0.95, t[3], t[4], t[5])


def sparks(target: str, hammer: str) -> bool:
    """Flint struck against something hard throws sparks."""
    return "flint" in (target, hammer) and min(RAW[target][2], RAW[hammer][2]) >= 0.5


def bind(a: dict, b: dict, binder: str) -> dict:
    """Tie two things together with something flexible."""
    bd = raw_props(binder)
    flex = int(a.get("flex", False)) + int(b.get("flex", False)) + 1
    edge = max(a["edge"], b["edge"])
    reach = clamp(a["reach"] + b["reach"])
    hard = max(a["hard"], b["hard"])
    contain = clamp(_layer(a["contain"], b["contain"], bd["contain"]) + 0.1 * flex)
    warm = clamp(_layer(a["warm"], b["warm"], bd["warm"]))
    fa, fb = a.get("float", 0.0), b.get("float", 0.0)
    float_ = clamp(max(fa, fb) + 0.5 * min(fa, fb))   # two buoyant parts together float far better
    parts = sorted((a["sig"], b["sig"]))
    return item_from(f"({parts[0]}+{parts[1]})#{binder}", edge, reach, hard, contain, warm, float_)


def _layer(x: float, y: float, binder: float) -> float:
    """Joining coverings: the bigger counts fully, the smaller half, the binding a little."""
    return max(x, y) + 0.5 * min(x, y) + 0.15 * binder


# --- what a thing does for you ------------------------------------------------

def factor(item: dict, use: str) -> float:
    """How much an item multiplies an effort. 1.0 means no help."""
    e, r, h, c, w = item["edge"], item["reach"], item["hard"], item["contain"], item["warm"]
    if use == "forage":
        return 1.0 + 0.25 * e + 0.3 * c
    if use == "hunt":
        return 1.0 + 1.5 * e * r + 0.3 * h * r
    if use == "wood":
        return 1.0 + 1.2 * e * h
    if use in ("stone", "flint"):
        return 1.0 + 0.5 * h
    if use == "fiber":
        return 1.0 + 0.6 * e
    if use == "fight":
        return 1.0 + 0.8 * e * r + 0.4 * h * r
    if use == "carry":
        return 1.0 + c
    if use == "cold":
        return 1.0 + w
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
    """The item p would use to cross water, and how well it floats. (-1, 0) if none."""
    best, best_f = -1, 0.0
    for i, it in enumerate(p.items):
        f = it.get("float", 0.0)
        if f > best_f:
            best, best_f = i, f
    return best, best_f


def wear(p, index: int) -> None:
    if index < 0:
        return
    it = p.items[index]
    it["uses"] -= 1
    if it["uses"] <= 0:
        p.items.pop(index)


def carry_capacity(world, p) -> float:
    _, f = best_item(p, "carry")
    return world.cfg.carry_limit * f


def worn_warmth(p) -> float:
    """Share of cold kept out by what p wears."""
    _, f = best_item(p, "cold")
    return clamp(0.7 * (f - 1.0))


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
