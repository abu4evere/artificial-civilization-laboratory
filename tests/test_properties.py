"""Property tests: laws that must hold in every world, checked on many randomly chosen worlds (Hypothesis).

Each test builds worlds from random seeds (and sizes), runs them for a random number of weeks, and checks, every
week, things the World Bible and the code's own rules say can never happen. These tests only read the worlds; they
cannot change any experiment. A failure is a finding, to be examined before anything is changed.
"""
from __future__ import annotations

import json

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from acl import Config, World

EPS = 1e-9
WPY = 52

seeds = st.integers(min_value=0, max_value=10**6)
weeks = st.integers(min_value=1, max_value=2 * WPY)
founders = st.sampled_from([4, 8, 12, 20])
SETTINGS = dict(max_examples=10, deadline=None, suppress_health_check=[HealthCheck.too_slow])


def _check_laws(w: World) -> None:
    c, tick = w.cfg, w.tick
    living = w.living()
    for p in w.people.values():
        # Things carried can never be negative.
        assert p.food >= -EPS, (p.id, p.food)
        assert p.seeds >= -EPS, (p.id, p.seeds)
        assert all(v >= -EPS for v in p.mats.values()), (p.id, p.mats)
        if not p.alive:
            assert p.death_tick is not None and p not in living, p.id
            continue
        # Bodies stay within their limits.
        assert -EPS <= p.energy <= 100.0 + EPS, (p.id, p.energy)
        assert p.health <= p.max_health(tick) + EPS, (p.id, p.health)
        assert p.birth <= tick, (p.id, p.birth, tick)
        # Everyone alive is on the map, and on land unless they carry something that floats (Rule 3).
        x, y = p.loc
        assert 0 <= x < c.width and 0 <= y < c.height, (p.id, p.loc)
        assert w.passable(p, p.loc) or not w.tile(p.loc).water, (p.id, p.loc)
        # Partnership is mutual, between living people who are not kin.
        if p.partner is not None:
            q = w.people[p.partner]
            assert q.alive, (p.id, q.id)
            assert q.partner == p.id, (p.id, q.id, q.partner)
            assert w.kinship(p, q) == 0, (p.id, q.id, w.kinship(p, q))
    for row in w.tiles:
        for t in row:
            # The land's stocks can never be negative.
            assert t.plants >= -EPS and t.crop >= -EPS, (t.x, t.y, t.plants, t.crop)
            assert t.wood >= -EPS and t.stone >= -EPS and t.fiber >= -EPS, (t.x, t.y)


@settings(**SETTINGS)
@given(seed=seeds, n=weeks, f=founders)
def test_laws_hold_every_week(seed, n, f):
    w = World(Config(seed=seed, founders=f))
    _check_laws(w)
    for _ in range(n):
        if not w.living():
            break
        w.step()
        _check_laws(w)


@settings(**SETTINGS)
@given(seed=seeds, n=st.integers(min_value=1, max_value=WPY))
def test_same_seed_same_world(seed, n):
    """Determinism: two worlds from the same seed stay identical, week for week."""
    a, b = World(Config(seed=seed)), World(Config(seed=seed))
    for _ in range(n):
        a.step()
        b.step()
    assert a.state_hash() == b.state_hash()


@settings(**SETTINGS)
@given(seed=seeds, before=st.integers(min_value=1, max_value=WPY), after=st.integers(min_value=1, max_value=WPY))
def test_saved_and_restored_world_continues_identically(seed, before, after):
    """A world saved and restored mid-run goes on exactly as the unsaved one (the live world depends on this).

    The copy goes through JSON, as the live world's saves do. Passing `to_dict()` straight to `from_dict()` would share
    lists between the two worlds, so stepping one would disturb the other: a restore must always use a saved copy."""
    a = World(Config(seed=seed))
    for _ in range(before):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for _ in range(after):
        a.step()
        b.step()
    assert a.state_hash() == b.state_hash()
