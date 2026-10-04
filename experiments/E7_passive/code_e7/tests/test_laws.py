"""Tests that pin the code to particular laws of the World Bible.

Each test names the law it holds the code to.
"""
from __future__ import annotations

import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CODE))

from acl import Config, World
from acl import inquiry, information, knowhow, marks, matter, weather
from acl.historian import Historian
from acl.person import Memory, Relation
from acl.runner import load_snapshot, save_snapshot


def _pair(seed=3):
    """A speaker and a listener on one tile, everyone else gone."""
    w = World(Config(seed=seed, founders=4))
    people = list(w.people.values())
    a, b = people[0], people[1]
    for p in people[2:]:
        p.alive = False
    w._living = None
    for p in (a, b):
        p.loc = a.loc
        p.rel = {}
        p.food = 60.0
    w.reindex()
    return w, a, b


# --- Law 91: nobody writes into another person's mind ------------------------------------

def test_a_claim_is_hearsay_until_tested():
    w, a, b = _pair()
    a.beliefs["seeds@0"] = 0.9
    b.genes["curiosity"] = 0.98
    b.rel[a.id] = Relation(affection=0.8, trust=0.9, familiarity=1.0)
    for _ in range(80):
        information.show_how(w, a, b, parent=False)
        if b.heard:
            break
    told = [k for k in b.heard if k.startswith("b:")]
    assert told, "the listener should have taken the claim on"
    assert not b.beliefs, "a claim never becomes the listener's own tested belief by being told"
    key = told[0][2:]
    assert knowhow.belief(b, key) is not None      # but it does steer them until tested
    trust_before = b.rel[a.id].trust
    knowhow._credit(w, b, key, -0.3)               # their own experience says otherwise
    assert told[0] not in b.heard
    assert b.rel[a.id].trust < trust_before          # Law 66: being proved wrong costs the teller
    assert any(e["k"] == "refuted" for e in w.events)


def test_the_listener_weighs_the_speaker():
    w, a, b = _pair()
    trusted, distrusted = 0, 0
    for i in range(300):
        for trust in (0.9, -0.9):
            b.memories = []
            b.rel[a.id] = Relation(trust=trust, familiarity=0.5)
            msg = {"eid": 10_000 + i, "kind": "stole", "actor": a.id, "target": None, "place": a.loc,
                   "valence": -0.5, "strength": 1.0, "hops": 1}
            if information.hear_story(w, b, a, msg) == "accepted":
                if trust > 0:
                    trusted += 1
                else:
                    distrusted += 1
    assert trusted > 2 * distrusted


def test_a_witness_rejects_a_wrong_version():
    w, a, b = _pair()
    third = sorted(w.people)[2]
    b.memories = [Memory(500, 0, "stole", third, b.id, a.loc, 0.6, -0.6)]   # b saw it themselves
    msg = {"eid": 500, "kind": "stole", "actor": a.id, "target": b.id, "place": a.loc,
           "valence": -0.6, "strength": 1.0, "hops": 1}
    assert information.hear_story(w, b, a, msg) == "rejected"
    assert b.memories[0].actor == third


# --- Laws 51 and 80: telling is never exact ----------------------------------------------

def test_faded_stories_drift_toward_whoever_the_teller_dislikes():
    w, a, b = _pair()
    culprit, enemy = "p09998", "p09999"
    a.rel[enemy] = Relation(affection=-0.8, grudge=0.9, familiarity=0.5)
    m = Memory(700, 0, "stole", culprit, b.id, a.loc, 0.6, -0.6, strength=0.2)
    actors = [information._recall(w, a, m)["actor"] for _ in range(400)]
    changed = [x for x in actors if x != culprit]
    assert changed and all(x == enemy for x in changed)
    fresh = Memory(701, 0, "stole", culprit, b.id, a.loc, 0.6, -0.6, strength=1.0)
    still = sum(information._recall(w, a, fresh)["actor"] != culprit for _ in range(400))
    assert still < len(changed)                       # a fresh memory drifts less than a faded one


def test_methods_are_copied_with_mistakes():
    w, a, b = _pair()
    a.skills["crafting"] = b.skills["crafting"] = 0.0
    recipe = {"verb": "bind", "parts": ["stone", "wood"], "binder": "fiber"}
    seen = {information._sig_of(information._recipe_as_shown(w, a, b, recipe)) for _ in range(300)}
    assert "(stone+wood)#fiber" in seen and len(seen) > 1
    assert recipe == {"verb": "bind", "parts": ["stone", "wood"], "binder": "fiber"}   # the teacher's own is untouched


# --- Laws 63-66: surprise opens a question; tests settle it -------------------------------

def test_surprise_becomes_a_puzzle_and_testing_settles_it():
    w, a, _ = _pair()
    inquiry.surprised(w, a, "m:flint/stone", 0.0, 0.9)
    assert inquiry.pull(a, "m:flint/stone") > 0.5
    for _ in range(6):
        inquiry.surprised(w, a, "m:flint/stone", 0.85, 0.9)     # it does it again, as now expected
    assert inquiry.pull(a, "m:flint/stone") < 0.1
    inquiry.surprised(w, a, "m:wood/stone", 0.0, 0.05)          # small gaps are not noticed
    assert "m:wood/stone" not in a.puzzles


# --- Law 22: marks mean nothing; links have to stand out from the background ------------

def test_a_mark_that_is_everywhere_water_is_tells_nothing_about_water():
    w, a, _ = _pair()
    a.expect["near:water"] = 0.95              # they always stop by water
    a.marks["|o^"] = [10, {"water": 0.95}]
    assert marks.meaning(a, "|o^").get("water", 0.0) < 0.05
    a.expect["near:grave"] = 0.02              # graves are rare where they stop
    a.marks["v.v"] = [10, {"grave": 0.7}]
    assert marks.meaning(a, "v.v")["grave"] > 0.6


def test_shapes_carry_no_built_in_meaning():
    w, a, _ = _pair()
    w.tile(a.loc).marks = [["/-o", "p00999", 0, 0.8, "rock"]]
    for k in list(a.expect):
        if k.startswith("near:"):
            del a.expect[k]
    marks.see(w, a)
    links = a.marks["/-o"][1]
    assert set(links) == set(marks.around(w, a.loc))   # whatever was around, and nothing else


# --- Rules 8 and 14: weather, water and thirst ----------------------------------------------

def test_no_water_hurts_and_sea_water_does_not_help():
    w, a, _ = _pair()
    sight = w.cfg.perception
    w.sky.update(rain=0, rained=0)

    def put(loc):
        a.loc = loc
        w.plan[a.id] = (loc, "")

    dry = next((t.x, t.y) for row in w.tiles for t in row
               if not t.water and weather.fresh_near(w, (t.x, t.y), sight) is None
               and not weather.salt_near(w, (t.x, t.y)) and t.biome != "desert")
    put(dry)
    assert weather.drink(w, a) == 1.0
    shore = next((t.x, t.y) for row in w.tiles for t in row
                 if not t.water and weather.salt_near(w, (t.x, t.y))
                 and weather.fresh_near(w, (t.x, t.y), sight) is None)
    put(shore)
    health = a.health
    assert weather.drink(w, a) == 1.0 and a.health < health
    assert a.expect["salt"] < 1.0          # they have learned something about the sea
    river = next((t.x, t.y) for row in w.tiles for t in row if t.biome == "river")
    put(river)
    a.energy = 100.0
    assert weather.drink(w, a) == 0.0 and a.energy == 100.0
    walk = next((t.x, t.y) for row in w.tiles for t in row
                if not t.water and weather.fresh_near(w, (t.x, t.y), w.cfg.water_reach) is None
                and weather.fresh_near(w, (t.x, t.y), sight) is not None)
    put(walk)
    assert weather.drink(w, a) == 0.0 and a.energy < 100.0      # water in sight, but a walk every day


def test_the_north_and_winter_are_colder():
    w, a, _ = _pair()
    land = [t for row in w.tiles for t in row if not t.water]
    cold = min(land, key=lambda t: t.temp)
    warm = max(land, key=lambda t: t.temp)
    w.tick = 3 * 13                        # winter
    assert weather.coldness(w, (cold.x, cold.y)) > weather.coldness(w, (warm.x, warm.y))
    w.tick = 13                            # summer
    assert weather.coldness(w, (warm.x, warm.y)) == 0.0


def test_new_state_survives_a_snapshot(tmp_path):
    w = World(Config(seed=7))
    for _ in range(60):
        w.step()
    p = next(iter(w.living()))
    p.heard["b:seeds@0"] = [0.3, ["p00001"], 1]
    p.puzzles["m:flint/stone"] = [0.6, 0.0, 1, 2]
    p.marks["|o^"] = [2, {"fire": 0.4}]
    w.tile(p.loc).marks.append(["|o^", p.id, w.tick, 0.5, "rock"])
    path = tmp_path / "w.json.gz"
    save_snapshot(w, Historian(), path)
    v, _ = load_snapshot(path)
    q = v.people[p.id]
    assert q.heard == p.heard and q.puzzles == p.puzzles and q.marks == p.marks
    assert v.tile(p.loc).marks == w.tile(p.loc).marks and v.sky == w.sky
    assert v.state_hash() == w.state_hash()


# --- the Lab only watches -------------------------------------------------------------------

def test_the_lab_never_changes_the_world():
    from acl.measure import Lab
    plain = World(Config(seed=11))
    watched = World(Config(seed=11))
    h = Historian()
    lab = Lab(h)
    watched.observers += [h, lab]
    for _ in range(52 * 3):
        plain.step()
        watched.step()
    assert plain.state_hash() == watched.state_hash()
    assert len(lab.years) == 3 and "trust" in lab.years[-1] and lab.summary(watched)["techniques"] >= 0


# --- reputation from tested accuracy (Laws 36, 56, 92) --------------------------------------------

def test_whose_word_held_is_believed_more():
    w, a, b = _pair()
    third = next(p for p in w.people.values() if p.id not in (a.id, b.id))
    third.alive = True
    w._living = None
    for src, held in ((a, True), (third, False)):
        b.rel[src.id] = Relation(trust=0.3, familiarity=0.5)
        for _ in range(6):
            b.heard["g:1,1"] = [0.8, [src.id], w.tick]
            information.tested(w, b, "g:1,1", 1.0 if held else -1.0)
    assert b.records[a.id][0] == 6 and b.records[third.id][1] == 6
    assert information.credence(w, b, a) > information.credence(w, b, third) + 0.3


def test_reputation_passes_by_word_and_the_listener_decides():
    w, a, b = _pair()
    a.records["p09999"] = [5.0, 0.0]
    b.rel[a.id] = Relation(trust=0.8, familiarity=0.8)
    assert information.share_reputation(w, a, b)
    held, failed = b.records["p09999"]
    assert 0 < held <= 0.5 and failed < held          # half an observation at most, weighted by belief in a


# --- more testing (Laws 47, 64, 65) -------------------------------------------------------------------

def test_reports_of_water_are_checked_on_sight():
    w, a, b = _pair()
    river = next((t.x, t.y) for row in w.tiles for t in row if t.biome == "river")
    dry = next((t.x, t.y) for row in w.tiles for t in row
               if not t.water and weather.fresh_near(w, (t.x, t.y), 2) is None)
    for spot, expect in ((river, "verified"), (dry, "refuted")):
        b.loc = spot
        b.heard[f"w:{spot[0]},{spot[1]}"] = [0.6, [a.id], w.tick]
        w.events = []
        information.check_places(w, b)
        assert any(e["k"] == expect for e in w.events)


def test_turned_earth_counts_as_having_watched_someone_sow():
    w, a, _ = _pair()
    t = w.tile(a.loc)
    t.traces["sown@1"] = [1.0, w.tick]
    a.placements = []
    knowhow.look_at_traces(w, a)
    assert any(pl[3] == "seeds@1" for pl in a.placements)


def test_an_accepted_claim_becomes_something_to_check():
    w, a, b = _pair()
    a.beliefs["food@2"] = 0.9
    b.rel[a.id] = Relation(trust=0.9, familiarity=1.0)
    b.genes["curiosity"] = 0.98
    for _ in range(80):
        information.show_how(w, a, b, parent=False)
        if "b:food@2" in b.heard:
            break
    assert "b:food@2" in b.heard and "b:food@2" in b.puzzles


# --- external records (Laws 52, 81, 115) --------------------------------------------------------------

def test_a_mark_can_mean_what_was_done_and_be_read_as_a_technique():
    w, a, _ = _pair()
    a.recipes = {}
    a.expect["near:struck:flint"] = 0.02
    a.marks["o|o"] = [9, {"struck:flint": 0.8}]
    w.tile(a.loc).traces.clear()
    w.tile(a.loc).marks = [["o|o", "p09999", 0, 0.9, "rock"]]
    seen = False
    for _ in range(60):
        marks.see(w, a)
        if any(r.get("target") == "flint" for r in a.recipes.values()):
            seen = True
            break
    assert seen
    key = next(k for k in a.heard if k.startswith("m:flint/"))
    assert a.heard[key][1] == ["mark:o|o"]


# --- floating as something it lets you do (Rule 3, Law 109) ---------------------------------------------

def test_water_stops_walking_but_not_floating():
    w, a, _ = _pair()
    c = w.cfg
    pair = None
    for row in w.tiles:
        for t in row:
            if t.water:
                continue
            for dx, dy in [(dx, dy) for dx in range(-3, 4) for dy in range(-3, 4)]:
                n = ((t.x + dx) % c.width, (t.y + dy) % c.height)
                if not w.tile(n).water and w.island_of(n) is not None and w.island_of(n) != w.island_of((t.x, t.y)):
                    pair = ((t.x, t.y), n)
                    break
            if pair:
                break
        if pair:
            break
    assert pair, "this map has islands close enough to test"
    src, dst = pair
    a.items = []
    end, crossed = w.walk(a, src, dst)
    assert end != dst and not crossed
    a.items = [matter.bind(matter.raw_props("wood"), matter.raw_props("wood"), "fiber")]
    end, crossed = w.walk(a, src, dst)
    assert end == dst and crossed


def test_crossing_to_new_land_makes_a_raft_worth_having():
    from acl import actions
    w, a, _ = _pair()
    raft = matter.bind(matter.raw_props("wood"), matter.raw_props("wood"), "fiber")
    a.items = [raft]
    a.itemval = {}
    land = [(t.x, t.y) for row in w.tiles for t in row if not t.water]
    start = next(l for l in land if w.island_of(l) == 0)
    other = next(l for l in land if w.island_of(l) not in (None, 0))
    a.loc = other
    w.events = []
    actions._over_water(w, a, start)
    assert a.itemval[raft["sig"]] > 0.05
    assert any(e["k"] == "crossed" for e in w.events)
