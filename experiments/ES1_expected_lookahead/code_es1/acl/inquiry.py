"""Surprise, and going back to look again (Laws 63-66).

People carry expectations: what a thing they made will do for them, how a spot
where they left something will turn out, what happens when they strike one
stone against another. When the world answers very differently from what they
expected, the gap stays with them. That gap is a puzzle.

A puzzle is only a pull on attention (see thought.py). Whether anyone acts on it
depends on how curious they are and on what else is on their mind; hunger
crowds it out. If they do act, it pulls them back toward the same thing: make
the thing again, leave the same thing in the same season, gather what trying
again needs, fiddle with things like it. Each new try is a test. A test that
comes out as expected starts to settle the puzzle. One that surprises again
keeps it alive.

Nothing here knows the answer. The world's physics decides every test.
"""
from __future__ import annotations

from .util import clamp

THRESHOLD = 0.25   # a gap this big between expectation and outcome is noticed
SETTLED = 0.1      # a gap this small means it came out as expected
MAX_PUZZLES = 5


def surprised(world, p, key: str, expected: float, got: float) -> None:
    """p expected `expected` for `key` and got `got`. A big gap becomes a puzzle; a test of an
    existing puzzle either settles it or keeps it alive."""
    gap = got - expected
    pz = p.puzzles.get(key)
    if pz is not None:
        pz[2] += 1
        pz[3] = world.tick
        if abs(gap) < SETTLED:
            pz[0] = round(pz[0] * 0.5, 3)          # it came out as they now expect
        else:
            pz[0] = round(clamp(max(pz[0], abs(gap))), 3)
        pz[1] = round(got, 3)
        world.emit("tested", p.id, None, p.loc, about=key, gap=round(gap, 2), n=pz[2])
        if pz[0] < 0.05:
            del p.puzzles[key]
        return
    if abs(gap) < THRESHOLD:
        return
    notice(world, p, key, abs(gap), expected)


def notice(world, p, key: str, size: float, expected: float = 0.0) -> None:
    """Something new or odd caught p's eye."""
    pz = p.puzzles.get(key)
    if pz is not None:
        pz[0] = round(clamp(max(pz[0], size)), 3)
        return
    p.puzzles[key] = [round(clamp(size), 3), round(expected, 3), 0, world.tick]
    world.emit("puzzled", p.id, None, p.loc, about=key, size=round(size, 2))
    while len(p.puzzles) > MAX_PUZZLES:
        weakest = min(p.puzzles, key=lambda k: (p.puzzles[k][0], k))
        del p.puzzles[weakest]


def pull(p, key: str) -> float:
    pz = p.puzzles.get(key)
    return pz[0] if pz else 0.0


def fade(p) -> None:
    """Unresolved puzzles slowly let go."""
    for key in list(p.puzzles):
        pz = p.puzzles[key]
        pz[0] = round(pz[0] * 0.93, 3)
        if pz[0] < 0.05:
            del p.puzzles[key]
