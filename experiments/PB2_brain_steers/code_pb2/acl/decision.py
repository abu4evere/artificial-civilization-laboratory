"""The standard decision interface for Experiment 0.

Every action choice passes through one door::

    Agent State Snapshot -> Candidate Actions -> Decision -> Chosen Action
                                                              |
                                                   World Execution
                                                              v
                                                    Observed Outcome

The decision module can later be replaced (MCTS, an LLM, reinforcement
learning, ...) without rewriting the world. For now it wraps the existing
instinct + habit logic in :mod:`acl.mind` unchanged, and only records what
that logic already considered and chose, plus a minimal prediction.

Nothing in this module draws from the world's random generator, so wrapping
the existing logic here leaves the simulation fully deterministic.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

from . import mind
from .util import clamp

# Rough alignment between decision scores (~0..3) and immediate rewards
# (~0..0.6). The exact scale is itself an open question the experiment is
# meant to surface, so this is only a comparable-enough normalisation.
REWARD_SCALE = 5.0

_EMOTIONS = ("mood", "fear", "anger", "grief", "loneliness", "wellbeing")
_NEEDS = ("health", "energy", "food", "sick", "starving")


@dataclass
class Decision:
    agent_id: str
    tick: int
    state: dict
    candidates: list          # each [action, aim, score, is_chosen]
    chosen: tuple             # (action, target)
    prediction: dict


def state_snapshot(world, p) -> dict:
    """Everything about the agent and its immediate world a decision could read.

    Read-only. This is the observable state at the moment of decision, used both
    by the interface and later by the SurpriseLog to measure before/after change.
    """
    c = world.cfg
    near = world.people_near(p.loc, c.reach, exclude=p.id)
    snap = {
        "agent_id": p.id,
        "tick": world.tick,
        "loc": list(p.loc),
        "season": world.season,
        "age_weeks": p.age(world.tick),
        "stage": p.stage(world.tick),
        "health": round(p.health, 2),
        "energy": round(p.energy, 2),
        "food": round(p.food + p.seeds, 2),
        "mood": round(p.mood, 3),
        "fear": round(p.fear, 3),
        "anger": round(p.anger, 3),
        "grief": round(p.grief, 3),
        "loneliness": round(p.loneliness, 3),
        "wellbeing": round(p.wellbeing, 3),
        "sick": p.sick,
        "starving": p.starving,
        "partner": p.partner,
        "thoughts": [list(t) for t in p.thoughts],
        "focus": p.focus,
        "nearby_people": [q.id for q in near[:8]],
        "relationships": {k: r.to_list() for k, r in p.rel.items()},
        "memories": [m.eid for m in p.memories],
        "recipes": list(p.recipes.keys()),
        "beliefs": {k: round(v, 3) for k, v in p.beliefs.items()},
        "items": [it["sig"] for it in p.items],
        "materials": {k: round(v, 2) for k, v in p.mats.items() if v > 0},
    }
    snap["ref"] = _ref(snap)
    return snap


def _ref(snap: dict) -> str:
    """A stable short reference to a state snapshot (not the full state inline)."""
    blob = json.dumps(snap, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha1(blob.encode()).hexdigest()[:12]


def decide(world, p) -> Decision:
    """Choose p's action for this week through the standard interface.

    Wraps the existing decision logic unchanged; it only records what that
    logic already considered and chose, plus a minimal prediction of the
    chosen action's value.
    """
    state = state_snapshot(world, p)
    chosen = mind.decide(world, p)                     # (action, target)
    candidates = [list(c) for c in p.considered]
    score = next((c[2] for c in candidates if c[3]), 0.0)
    d = Decision(p.id, world.tick, state, candidates, chosen,
                 {"expected_value": round(score, 3)})
    world.week_decisions.append(d)
    return d


def prediction_error(decision: Decision, reward: float) -> float:
    """Distance between the agent's predicted value and the reward it got.

    The simplest sensible measure available: the decision score is the agent's
    internal expectation, and ``reward`` is what the action handlers actually
    returned (the same signal its temporal-difference learner trains on).
    """
    predicted = decision.prediction["expected_value"]
    return round(abs(predicted - reward * REWARD_SCALE), 3)
