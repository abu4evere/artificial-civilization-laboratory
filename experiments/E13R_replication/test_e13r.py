"""Tests for the E13R code: the guarantees the pre-registration depends on (part of L2).

    python -m pytest experiments/E13R_replication/test_e13r.py -q
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "code_e13r"))

from acl import biology  # noqa: E402
from acl.config import Config  # noqa: E402
from acl.person import A, N_ACTIONS  # noqa: E402
from acl.world import World  # noqa: E402


def _state(w):
    d = json.loads(json.dumps(w.to_dict()))
    d.pop("cfg")
    return d


def _scene(mode, model_food, write=True):
    """An observer with one model beside them who foraged this week; everyone else moved out of sight."""
    w = World(Config(seed=501, anticipation_weight=1.0, b2_mode=mode, b2_write=write))
    adults = sorted((p for p in w.living() if p.age(w.tick) >= 16 * 52), key=lambda q: q.id)
    p, m = adults[0], adults[1]
    far = ((p.loc[0] + w.cfg.width // 2) % w.cfg.width, (p.loc[1] + w.cfg.height // 2) % w.cfg.height)
    for q in w.living():
        if q.id not in (p.id, m.id):
            w.move(q, far)
    w.move(m, p.loc)
    p.food, p.seeds = 1.0, 0.0
    m.food, m.seeds = model_food, 0.0
    m.last_action, m.last_ctx = "forage", 3 * 8 + 2
    w.events = [{"k": "forage", "a": m.id, "got": 5.0}]
    return w, p, m


def _forage_entry(m):
    return m.last_ctx * N_ACTIONS + A["forage"]


def test_off_by_default():
    c = Config()
    assert c.b2_mode == 0 and c.b2_write is True


def test_copying_changes_only_the_observers_forage_entry():
    w, p, m = _scene(1, 40.0)
    before = _state(w)
    biology._follow(w, p)
    after = _state(w)
    idx = next(i for i, d in enumerate(before["people"]) if d["id"] == p.id)
    changed = [i for i, (x, y) in enumerate(zip(before["people"][idx]["q"], after["people"][idx]["q"])) if x != y]
    assert changed == [_forage_entry(m)]
    after["people"][idx]["q"] = before["people"][idx]["q"]
    assert after == before


def test_no_visible_better_fed_model_means_no_change():
    w, p, m = _scene(1, 40.0)
    p.food = 1000.0                       # nobody in sight is better fed
    before = _state(w)
    biology._follow(w, p)
    assert _state(w) == before


def test_model_not_foraging_means_no_change():
    w, p, m = _scene(1, 40.0)
    m.last_action = "rest"
    before = _state(w)
    biology._follow(w, p)
    assert _state(w) == before


def test_sham_writes_nothing():
    w, p, m = _scene(1, 40.0, write=False)
    before = _state(w)
    biology._follow(w, p)
    assert _state(w) == before


def test_arm_n_ignores_models_holding_80_or_more():
    for food, learns in ((79.0, True), (80.0, False)):
        w, p, m = _scene(3, food)
        before = list(p.q)
        biology._follow(w, p)
        assert (p.q != before) is learns


def test_arm_p_only_models_holding_80_or_more():
    for food, learns in ((79.0, False), (80.0, True)):
        w, p, m = _scene(4, food)
        before = list(p.q)
        biology._follow(w, p)
        assert (p.q != before) is learns


def test_sham_world_equals_control_world():
    """L1 in miniature: three years, the sham's world state equals the control's."""
    hs = []
    for kw in ({}, {"b2_mode": 1, "b2_write": False}):
        w = World(Config(seed=501, anticipation_weight=1.0, **kw))
        for _ in range(3 * 52):
            w.step()
        hs.append(hashlib.sha256(json.dumps(_state(w)).encode()).hexdigest())
    assert hs[0] == hs[1]
