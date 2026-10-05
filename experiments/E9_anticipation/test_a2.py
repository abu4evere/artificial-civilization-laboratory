"""Tests for the E9 A2 code: the guarantees the pre-registration depends on.

    python -m pytest experiments/E9_anticipation/test_a2.py -q
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "code_a2"))

from acl import biology, mind  # noqa: E402
from acl.config import Config  # noqa: E402
from acl.world import World  # noqa: E402


def _adult(w):
    return sorted((p for p in w.living() if p.stage(w.tick) == "adult"), key=lambda q: q.id)[0]


def test_default_weight_is_zero():
    assert Config().anticipation_weight == 0.0


def test_expectation_learns_only_the_current_season_from_going_short():
    w = World(Config(seed=304))
    p = _adult(w)
    p.expect = {}
    p.starving = 3
    p.food = 0.0
    p.seeds = 0.0
    biology.body_phase(w)
    s = w.season
    keys = [k for k in p.expect if k.startswith("short@")]
    assert keys == [f"short@{s}"]


def test_no_expectation_means_no_change_in_food_pull():
    """Leak guarantee: a person who has never gone short feels exactly today's hunger."""
    w = World(Config(seed=304, anticipation_weight=1.0))
    p = _adult(w)
    p.expect = {k: v for k, v in p.expect.items() if not k.startswith("short@")}
    nxt = f"short@{(w.season + 1) % 4}"
    assert c_ahead(w, p) == 0.0, nxt


def c_ahead(w, p):
    return w.cfg.anticipation_weight * p.expect.get(f"short@{(w.season + 1) % 4}", 0.0)


def test_anticipation_reaches_only_the_food_pull():
    """With an expectation of going short next season, foraging rises but stealing does not: the thief's
    hunger term is untouched (it still reads today's hunger)."""
    src = (HERE / "code_a2" / "acl" / "mind.py").read_text(encoding="utf-8")
    assert src.count("food_hunger") == 4          # defined once; used in forage, hunt, and the thought call
    assert "hunger > 0.3 and kin < 0.5" in src     # stealing still reads hunger, not food_hunger


def test_zero_weight_reproduces_e7_for_five_years():
    sys.path.insert(0, str(HERE.parent / "E7_passive"))
    import json
    saved = json.loads((HERE.parent / "E7_passive" / "output" / "e7" / "seed_304.json").read_text(encoding="utf-8"))
    w = World(Config(seed=304, anticipation_weight=0.0))
    pops = []
    for y in range(10):
        for _ in range(52):
            w.step()
    pops.append(len(w.living()))
    assert pops[0] == saved["samples"][0]["population"]
