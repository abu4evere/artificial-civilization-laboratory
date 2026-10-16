"""Tests for determinism, revenge, family life, knowledge and the land."""
from __future__ import annotations

import json

from acl import Config, World
from acl import actions, biology, knowhow, matter, social
from acl.historian import Historian, classify
from acl.person import Relation
from acl.runner import load_snapshot, new_world, save_snapshot, simulate
from acl.util import distance, step_toward


# --- determinism ---------------------------------------------------------------

def test_same_seed_same_history():
    a, _ = new_world(7)
    b, _ = new_world(7)
    a.run(52 * 5)
    b.run(52 * 5)
    assert a.state_hash() == b.state_hash()
    assert a.event_chain == b.event_chain


def test_different_seed_different_history():
    a, _ = new_world(7)
    b, _ = new_world(8)
    a.run(52)
    b.run(52)
    assert a.state_hash() != b.state_hash()


def test_snapshot_resume_matches_straight_run(tmp_path):
    w1, h1 = new_world(11)
    straight = simulate(w1, h1, 6)
    w2, h2 = new_world(11)
    simulate(w2, h2, 3)
    save_snapshot(w2, h2, tmp_path / "snap.json.gz")
    w3, h3 = load_snapshot(tmp_path / "snap.json.gz")
    resumed = simulate(w3, h3, 3)
    assert straight["state_hash"] == resumed["state_hash"]
    assert straight["event_chain"] == resumed["event_chain"]
    assert straight["metrics"] == resumed["metrics"]


def test_a_world_saved_under_other_laws_is_not_continued(tmp_path):
    """A save from before nature v2 has no version; it is refused, not loaded into the wrong laws, and left on disk."""
    import gzip
    import json
    import pytest
    w, h = new_world(11)
    save_snapshot(w, h, tmp_path / "snap.json.gz")
    with gzip.open(tmp_path / "snap.json.gz", "rt", encoding="utf-8") as f:
        blob = json.load(f)
    del blob["versions"]
    with gzip.open(tmp_path / "old.json.gz", "wt", encoding="utf-8") as f:
        json.dump(blob, f)
    with pytest.raises(ValueError, match="nature-v1"):
        load_snapshot(tmp_path / "old.json.gz")
    assert (tmp_path / "old.json.gz").exists()


def test_serialisation_round_trip():
    w, _ = new_world(3)
    w.run(52 * 2)
    d = w.to_dict()
    again = World.from_dict(json.loads(json.dumps(d))).to_dict()
    assert again == d


def test_historian_never_changes_the_world():
    with_h, _ = new_world(5)
    without = World(Config(seed=5))
    with_h.run(52 * 4)
    without.run(52 * 4)
    assert with_h.state_hash() == without.state_hash()


# --- a small controlled world --------------------------------------------------

def _trio(seed=1):
    """Three adults on one tile: A, B, and C, B's partner. Everyone else removed."""
    w = World(Config(seed=seed, founders=4))
    a, b, c, d = list(w.people.values())
    for p in (a, b, c, d):
        p.loc = (5, 5)
        p.food = 60.0
        p.rel = {}
    d.alive = False
    w._living = None
    b.partner, c.partner = c.id, b.id
    c.rel[b.id] = Relation(affection=0.9, trust=0.8, familiarity=1.0)
    c.genes.update(temper=0.9, boldness=0.9, kindness=0.1, anxiety=0.1)
    a.genes.update(temper=0.1, boldness=0.1, kindness=0.5)
    w.reindex()
    return w, a, b, c


def test_witnessing_a_killing_creates_a_grudge():
    w, a, b, c = _trio()
    b.health = 1.0
    a.health = 100.0
    for _ in range(20):
        if not b.alive:
            break
        actions._attack(w, a, b.id, 1.0)
        b.health = min(b.health, 1.0)
    assert not b.alive and b.death_cause == "killed"
    assert any(m.kind == "killed" and m.actor == a.id for m in c.memories)
    assert c.rel[a.id].grudge > 0.3
    assert c.grief > 0.3


def test_revenge_follows_a_killing():
    w, a, b, c = _trio()
    b.health = 1.0
    while b.alive:
        actions._attack(w, a, b.id, 1.0)
        b.health = min(b.health, 1.0)
    avenged = False
    for _ in range(52):
        for p in (a, c):
            p.food = max(p.food, 60.0)
        events = w.step()
        if any(e["k"] in ("attack", "kill") and e.get("a") == c.id and e.get("b") == a.id for e in events):
            avenged = True
            break
        if not a.alive or not c.alive:
            break
    assert avenged


def test_news_of_a_killing_travels_by_gossip():
    w, a, b, c = _trio()
    friend = w.people[[pid for pid in w.people if pid not in (a.id, b.id, c.id)][0]]
    friend.alive = True
    friend.rel = {b.id: Relation(affection=0.8, trust=0.5, familiarity=0.8),
                  c.id: Relation(affection=0.5, trust=0.8, familiarity=0.8)}
    friend.loc = (15, 15)          # far away: cannot witness
    w._living = None
    w.reindex()
    b.health = 1.0
    while b.alive:
        actions._attack(w, a, b.id, 1.0)
        b.health = min(b.health, 1.0)
    assert not any(m.kind == "killed" for m in friend.memories)
    for _ in range(20):            # the listener may doubt it at first
        social.gossip(w, c, friend)
        if any(m.kind == "killed" for m in friend.memories):
            break
    heard = [m for m in friend.memories if m.kind == "killed"]
    assert heard and heard[0].source == c.id
    assert friend.rel[a.id].grudge > 0


# --- family --------------------------------------------------------------------

def _couple(seed=2):
    w = World(Config(seed=seed, founders=2))
    mother, father = sorted(w.people.values(), key=lambda p: p.sex)  # F first
    assert mother.sex == "F" and father.sex == "M"
    father.loc = mother.loc
    mother.partner, father.partner = father.id, mother.id
    mother.pregnant, mother.conceived = father.id, w.tick - 40
    w.reindex()
    return w, mother, father


def test_birth_inherits_from_both_parents():
    w, mother, father = _couple()
    biology.give_birth(w, mother)
    child = w.people[mother.children[-1]]
    assert child.caregiver == mother.id and child.father == father.id
    assert child.generation == 1
    for g, v in child.genes.items():
        lo, hi = sorted((mother.genes[g], father.genes[g]))
        assert lo - 0.4 <= v <= hi + 0.4
    assert mother.rel[child.id].affection >= 0.5
    assert any(m.kind == "born" for m in mother.memories)


def test_caring_parents_feed_children_before_themselves():
    fed = {}
    for care in (0.05, 0.95):
        w, mother, father = _couple()
        biology.give_birth(w, mother)
        child = w.people[mother.children[-1]]
        mother.genes["care"] = care
        mother.food, father.food, child.food = 4.0, 30.0, 0.0
        before = child.health
        biology.body_phase(w)
        fed[care] = child.health - before
    assert fed[0.95] > fed[0.05]


def test_orphans_go_to_family():
    w, mother, father = _couple()
    biology.give_birth(w, mother)
    child = w.people[mother.children[-1]]
    biology.die(w, mother, "illness", None)
    assert child.caregiver == father.id


# --- knowledge -----------------------------------------------------------------

FLAKE = {"verb": "strike", "target": "flint", "tool": "stone"}


def test_knowledge_dies_with_its_last_holder():
    w, mother, father = _couple()
    knowhow.remember_recipe(w, mother, "flint/stone", FLAKE, "made")
    biology.die(w, mother, "illness", None)
    knowhow.check_lost(w)
    assert w.knowledge["flint/stone"]["alive"] is False
    assert any(e["k"] == "knowledge_lost" for e in w.events)


def test_teaching_passes_knowledge_on():
    w, mother, father = _couple()
    knowhow.remember_recipe(w, mother, "flint/stone", FLAKE, "made")
    mother.itemval["flint/stone"] = 0.8
    father.genes["curiosity"] = 0.98
    father.rel[mother.id] = Relation(affection=0.8, trust=0.8, familiarity=1.0)
    for _ in range(60):
        knowhow.teach(w, mother, father)
    # He took something from her, as he understood it (maybe with a step wrong), and it is still hearsay.
    learned = [sig for sig in father.recipes if f"m:{sig}" in father.heard]
    assert learned
    assert all(father.heard[f"m:{sig}"][1] == [mother.id] for sig in learned)
    assert father.itemval[learned[0]] > 0


# --- physics of things ---------------------------------------------------------

class _Fixed:
    """The luckiest strike: the highest roll (nature v2 draws whole numbers, and keeps properties on a 0-100 scale)."""
    def random(self):
        return 1.0

    def randrange(self, lo, hi):
        return hi - 1


def test_struck_flint_takes_an_edge():
    flake = matter.strike("flint", "stone", skill=0.5, rng=_Fixed())
    assert flake["edge"] > 55
    assert classify(flake) == ["blade"]
    stick = matter.strike("wood", "wood", skill=0.5, rng=_Fixed())
    assert stick is None or stick["edge"] < 15


def test_a_blade_on_a_shaft_reaches_and_cuts():
    flake = matter.strike("flint", "stone", skill=0.5, rng=_Fixed())
    spear = matter.bind(flake, matter.raw_props("wood"), "fiber")
    assert "spear" in classify(spear)
    assert spear["warm"] < 30
    assert matter.factor(spear, "hunt") > 1.5


def test_hides_together_keep_warm():
    wrap = matter.bind(matter.raw_props("hide"), matter.raw_props("hide"), "hide")
    assert "wrap" in classify(wrap)
    basket = matter.bind(matter.raw_props("fiber"), matter.raw_props("fiber"), "fiber")
    assert "carrier" in classify(basket) and "wrap" not in classify(basket)


def test_seeds_in_the_ground_grow_in_spring():
    w = World(Config(seed=6))
    t = next(t for row in w.tiles for t in row if not t.water and t.fertility > 0.3)
    t.sown = 20.0
    w.tick = 0                       # spring
    for _ in range(8):
        w._grow_land()
    assert t.crop > 20.0 and t.sown < 20.0


def test_fire_burns_out_unless_fed():
    w = World(Config(seed=6))
    t = w.tiles[4][4]
    t.fire = 2.0
    w._grow_land()
    w._grow_land()
    assert t.fire == 0.0
    p = next(iter(w.people.values()))
    w.move(p, (4, 4))
    t.fire = 1.5
    p.mats["wood"] = 4.0
    actions._put(w, p, "wood", 1.0)
    assert t.fire > 1.5 and "wood" not in t.pile


def test_a_heap_shelters_its_builders_first():
    w = World(Config(seed=6, founders=8))
    people = list(w.people.values())
    for q in people:
        w.move(q, (2, 2))
    t = w.tiles[2][2]
    t.pile = {"wood": 5.0, "hide": 8.0}
    builder = people[-1]
    t.builders = {builder.id: 13.0}
    inside = biology._who_is_inside(w, people)
    assert matter.pile_room(t.pile) < len(people)
    assert builder.id in inside
    assert len(inside) == matter.pile_room(t.pile)


def test_people_link_buried_seeds_to_a_richer_patch():
    w = World(Config(seed=6))
    p = next(iter(w.people.values()))
    w.move(p, (5, 5))
    knowhow.placed(w, p, "seeds", (5, 5))
    w.tick += 6
    w.tiles[5][5].crop = 60.0
    knowhow.look_around(w, p)
    assert p.beliefs[f"seeds@{p.placements[0][3].split('@')[1]}"] > 0


# --- land ----------------------------------------------------------------------

def test_world_wraps_at_the_edges():
    assert distance((0, 0), (19, 19), 20, 20) == 1
    assert step_toward((0, 0), (18, 0), 3, 20, 20) == (18, 0)


def test_land_never_exceeds_its_capacity():
    w = World(Config(seed=4))
    w.run(52 * 3)
    c = w.cfg
    for row in w.tiles:
        for t in row:
            assert t.plants <= c.plant_cap * t.fertility + 1e-6
            assert t.wood <= c.wood_cap * t.forest + 1e-6
    assert c.weather_low <= w.weather <= c.weather_high


def test_historian_round_trip():
    w, h = new_world(9)
    w.run(52 * 6)
    d = h.to_dict()
    assert Historian.from_dict(json.loads(json.dumps(d))).to_dict() == json.loads(json.dumps(d))
