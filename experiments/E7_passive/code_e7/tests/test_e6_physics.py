"""E6 physics: each new process works as the design note says, from properties alone.

Run: python -m pytest experiments/E6_novelty/code_e6/tests -q   (from D:/acl)
"""
import re
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CODE))

from acl import actions, biology, matter, weather  # noqa: E402
from acl.config import Config  # noqa: E402
from acl.world import World  # noqa: E402


def _world_and_person():
    w = World(Config(seed=301))
    p = sorted(w.living(), key=lambda q: q.id)[0]
    p.birth = w.tick - 30 * 52             # an adult
    return w, p


def _light(w, loc, kind="wood"):
    t = w.tile(loc)
    t.fire = 5.0
    t.fire_heat = matter.fire_heat(kind)
    return t


def test_P1_no_human_invention_named_in_code():
    """Properties, never products: no name in the code (identifier or key) is something people would
    later invent. Comments and prose are not code paths."""
    import io
    import tokenize
    banned = {"pot", "pots", "pottery", "oven", "kiln", "bow", "house", "bridge", "cook", "cooking", "boil",
              "boiling", "kettle", "jar", "cooked", "fired", "smoked"}
    for f in (CODE / "acl").glob("*.py"):
        for tok in tokenize.generate_tokens(io.StringIO(f.read_text(encoding="utf-8")).readline):
            if tok.type == tokenize.NAME:
                words = tok.string.lower().split("_")
            elif tok.type == tokenize.STRING and " " not in tok.string and len(tok.string) < 40:
                words = tok.string.strip("\"'fr").lower().replace(":", "_").split("_")
            else:
                continue
            assert not banned & set(words), f"{f.name}: {tok.string}"


def test_shaping_needs_soft_wet_stuff():
    assert matter.shape("clay", "hollow", wet=8)["contain"] == 60
    assert matter.shape("clay", "hollow", wet=2) is None          # dry clay does not take a shape
    assert matter.shape("stone", "hollow", wet=10) is None        # stone is not plastic


def test_heat_one_rule_many_consequences():
    """P2: the same heat rule dries, burns, cracks and sets, depending only on properties."""
    soft = matter.shape("clay", "hollow", wet=8)
    cracked, burned = matter.heat(soft, 6)
    assert cracked is None and not burned                          # wet into a hot fire: it cracks
    soft["wet"] = 0
    fired, burned = matter.heat(soft, 6)
    assert fired["plastic"] == 0 and fired["hard"] == 70 and fired["tight"] == 60 and not burned
    hotter, _ = matter.heat(dict(soft), 8)
    assert hotter["hard"] > fired["hard"] and hotter["tight"] > fired["tight"]   # a hotter fire, a better result
    wood = matter.item_from("wood", matter.raw_props("wood"))
    gone, burned = matter.heat(wood, 6)
    assert gone is None and burned                                  # what burns well burns away
    stone = matter.item_from("stone", matter.raw_props("stone"), wet=5)
    dried, burned = matter.heat(stone, 6)
    assert dried["wet"] == 0 and dried["sig"] == "stone" and not burned   # only dried
    assert matter.can_hold(fired, "water") == 6 and matter.can_hold(fired, "embers") == 6
    assert matter.can_hold(soft, "water") == 0                        # unfired clay leaks


def test_seams_leak_unless_tightly_bound():
    hide = matter.raw_props("hide")
    tied_with_fibre = matter.bind(hide, hide, "fiber")
    tied_with_hide = matter.bind(hide, hide, "hide")
    assert matter.can_hold(tied_with_fibre, "water") == 0
    assert matter.can_hold(tied_with_hide, "water") > 0


def test_food_held_in_fire_keeps_and_goes_further():
    """Two people with the same food, one has held it in a fire: after a week away from any fire, hers
    has rotted less and fed her as well on less, so she has more left, and she felt the difference."""
    w, p = _world_and_person()
    q = sorted(w.living(), key=lambda r: r.id)[1]
    q.birth = p.birth
    q.sex = p.sex
    w.move(q, p.loc)
    _light(w, p.loc)
    p.food = q.food = 20.0
    p.seeds = q.seeds = 0.0
    actions._heat_food(w, p, "food", 1.0)
    assert p.kept == 15.0 and q.kept == 0.0
    w.tile(p.loc).fire = 0.0
    biology.body_phase(w)
    assert p.food > q.food + 0.5
    assert p.expect.get("heat:food", 0.0) > 0


def test_carried_water_is_drunk_where_there_is_none():
    w, p = _world_and_person()
    pot = matter.item_from("x", {**matter.raw_props("clay"), "contain": 60, "tight": 60, "plastic": 0, "hard": 70})
    pot["holds"] = ["water", 6]
    p.items = [pot]
    dry = next(((t.x, t.y) for row in w.tiles for t in row
                if not t.water and weather.fresh_near(w, (t.x, t.y), w.cfg.perception) is None
                and not weather.salt_near(w, (t.x, t.y))), None)
    assert dry is not None
    w.move(p, dry)
    w.sky["rain"] = w.sky["rained"] = 0
    w.events = []
    assert weather.drink(w, p) == 0.0
    assert pot["holds"] == ["water", 5]
    assert any(e["k"] == "consequence" and e["what"] == "water_carried" for e in w.events)


def test_embers_carried_light_a_fire_elsewhere():
    w, p = _world_and_person()
    t = _light(w, p.loc)
    pot = matter.item_from("x", {**matter.raw_props("clay"), "contain": 60, "tight": 60, "plastic": 0, "hard": 70})
    p.items = [pot]
    p.mats["fiber"] = 2.0
    p.damp = {}
    actions._fill(w, p, "embers", 1.0)
    assert pot["holds"] == ["embers", 6]
    t.fire = 0.0
    w.events = []
    actions._fill(w, p, "pour", 1.0)
    assert w.tile(p.loc).fire > 0 and pot["holds"] is None
    assert any(e["k"] == "consequence" and e["what"] == "fire_carried" for e in w.events)


def test_making_a_hardened_container_end_to_end():
    w, p = _world_and_person()
    p.mats["clay"] = 2.0
    p.damp = {"clay": 8}
    soft = actions._craft(w, p, {"verb": "shape", "material": "clay", "form": "hollow"})
    assert soft["sig"] == "clay~hollow" and soft["wet"] == 8
    soft["wet"] = 0                                                  # left to dry
    _light(w, p.loc)
    fired = actions._craft(w, p, {"verb": "heat", "part": "clay~hollow", "level": 6})
    assert fired is not None and fired["sig"] == "clay~hollow^6" and matter.can_hold(fired, "water") > 0
