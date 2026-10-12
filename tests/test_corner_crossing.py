"""A1 fixed (AA1, the creator's decision of 12 October 2026): water touching only at a corner blocks a diagonal step.

Each test sets a 2 x 2 patch of tiles by hand: from `here`, a diagonal step to `there`, squeezing between two side tiles.
"""
from __future__ import annotations

from acl import Config, World


def _patch(sides_water: tuple[bool, bool]):
    w = World(Config(seed=11))
    p = next(iter(w.living()))
    x, y = 10, 10
    here, there = (x, y), (x + 1, y + 1)
    for loc in (here, there):
        w.tile(loc).water = False
    w.tile((x + 1, y)).water = sides_water[0]
    w.tile((x, y + 1)).water = sides_water[1]
    p.items = []
    return w, p, here, there


def test_corner_contact_cannot_bypass_water():
    w, p, here, there = _patch((True, True))
    got, crossed = w.walk(p, here, there)
    assert got == here and not crossed


def test_diagonal_step_on_land_still_works():
    for sides in ((False, False), (True, False), (False, True)):
        w, p, here, there = _patch(sides)
        got, _ = w.walk(p, here, there)
        assert got == there, sides


def test_a_boat_still_crosses_at_a_corner():
    w, p, here, there = _patch((True, True))
    p.items = [{"sig": "raft", "float": 1.0, "uses": 5}]
    got, _ = w.walk(p, here, there)
    assert got == there


def test_animals_are_blocked_too():
    w, _, here, there = _patch((True, True))
    got, _ = w.walk(None, here, there)
    assert got == here
