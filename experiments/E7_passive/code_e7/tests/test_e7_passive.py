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


def test_food_by_fire_is_only_counted():
    # Spec 3.2.3: smoke slows rot (smoke_keep, already nature). Food is not made "kept" for free.
    w, p = _world_and_person()
    _light(w, p.loc)
    p.food = 20.0
    p.kept = 0.0
    w.events = []
    biology._wet_and_dry(w, p)
    assert p.kept == 0.0
    assert any(e["k"] == "consequence" and e["what"] == "food_by_fire" for e in w.events)


def test_baked_thing_can_be_remade_and_world_runs_on():
    # The passive recipe must use the same shape as an active one, or the next decision crashes.
    w, p = _world_and_person()
    _light(w, p.loc)
    soft = matter.item_from("clay~hollow", {**matter.raw_props("clay"), "contain": 60, "tight": 30, "plastic": 80, "hard": 10}, wet=0)
    p.items = [soft]
    biology._wet_and_dry(w, p)
    assert p.recipes["clay~hollow^6"] == {"verb": "heat", "part": "clay~hollow", "level": 6}
    for _ in range(52):
        w.step()


def test_carried_raw_clay_bakes_by_a_hot_fire():
    w, p = _world_and_person()
    _light(w, p.loc)
    p.items = []
    p.mats["clay"] = 2.0
    p.damp.pop("clay", None)
    w.events = []
    biology._wet_and_dry(w, p)
    assert p.mats["clay"] == 1.0
    assert [it["sig"] for it in p.items] == ["clay^6"]
    assert p.recipes["clay^6"]["part"] == "clay"
    assert any(e["k"] == "consequence" and e["what"] == "ceramic_passive" for e in w.events)


def test_a_cool_fire_bakes_nothing():
    w, p = _world_and_person()
    _light(w, p.loc, kind="fiber")                     # heat 5, under the spec's 6
    p.items = []
    p.mats["clay"] = 1.0
    p.damp.pop("clay", None)
    biology._wet_and_dry(w, p)
    assert p.items == [] and p.mats["clay"] == 1.0


def test_wading_a_river_fills_open_vessel():
    w, p = _world_and_person()
    pot = matter.item_from("x", {**matter.raw_props("clay"), "contain": 60, "tight": 60, "plastic": 0, "hard": 70})
    p.items = [pot]
    t = w.tile(p.loc)
    t.water, t.biome = False, "river"
    w.sky["rain"] = 0
    biology._wet_and_dry(w, p)
    assert pot.get("holds") == ["water", 6]


def test_covered_heap_keeps_rain_out():
    w, p = _world_and_person()
    pot = matter.item_from("x", {**matter.raw_props("clay"), "contain": 60, "tight": 60, "plastic": 0, "hard": 70})
    p.items = [pot]
    w.tile(p.loc).pile = {"hide": 40.0, "wood": 40.0}
    assert biology.pile_shape(w.tile(p.loc).pile)[1] > 0.5
    w.sky["rain"] = 1
    biology._wet_and_dry(w, p)
    assert pot.get("holds") is None
