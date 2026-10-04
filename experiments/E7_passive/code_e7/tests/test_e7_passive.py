"""Tests for E7 passive environmental physics:
1. Rain catchment into open watertight vessels
2. Wading / submersion filling open vessels
3. Passive radiant heat baking dry clay on fire tiles
4. Passive food heating on fire tiles
"""
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CODE))

from acl import biology, matter, weather
from acl.config import Config
from acl.world import World


def _world_and_person():
    w = World(Config(seed=301))
    p = sorted(w.living(), key=lambda q: q.id)[0]
    p.birth = w.tick - 30 * 52
    return w, p


def _light(w, loc, kind="wood"):
    t = w.tile(loc)
    t.fire = 5.0
    t.fire_heat = matter.fire_heat(kind)
    return t


def test_passive_rain_fills_open_vessel():
    w, p = _world_and_person()
    pot = matter.item_from("x", {**matter.raw_props("clay"), "contain": 60, "tight": 60, "plastic": 0, "hard": 70})
    p.items = [pot]
    w.tile(p.loc).pile = {}
    w.sky["rain"] = 1
    w.events = []
    biology._wet_and_dry(w, p)
    assert pot.get("holds") == ["water", 6]
    assert any(e["k"] == "consequence" and e["what"] == "water_passive" for e in w.events)


def test_passive_wading_fills_open_vessel():
    w, p = _world_and_person()
    pot = matter.item_from("x", {**matter.raw_props("clay"), "contain": 60, "tight": 60, "plastic": 0, "hard": 70})
    p.items = [pot]
    w.tile(p.loc).water = True
    w.events = []
    biology._wet_and_dry(w, p)
    assert pot.get("holds") == ["water", 6]
    assert any(e["k"] == "consequence" and e["what"] == "water_passive" for e in w.events)


def test_passive_hearth_bakes_dry_clay():
    w, p = _world_and_person()
    _light(w, p.loc)
    soft = matter.item_from("clay~hollow", {**matter.raw_props("clay"), "contain": 60, "tight": 30, "plastic": 80, "hard": 10}, wet=0)
    p.items = [soft]
    w.events = []
    biology._wet_and_dry(w, p)
    baked = p.items[0]
    assert baked["sig"] == "clay~hollow^6"
    assert baked["plastic"] == 0
    assert baked["hard"] >= 70
    assert baked["tight"] >= 60
    assert any(e["k"] == "consequence" and e["what"] == "ceramic_passive" for e in w.events)


def test_passive_food_heating():
    w, p = _world_and_person()
    _light(w, p.loc)
    p.food = 20.0
    p.kept = 0.0
    w.events = []
    biology._wet_and_dry(w, p)
    assert p.kept == 20.0
    assert any(e["k"] == "consequence" and e["what"] == "food_heated" for e in w.events)
