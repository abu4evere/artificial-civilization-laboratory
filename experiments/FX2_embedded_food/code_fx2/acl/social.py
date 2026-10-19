"""Memories, witnesses, news and feelings toward others.

Harm creates grudges in the victim and in everyone who loves the victim, once
they find out. They find out by seeing it happen or by being told. Being told
is gossip, and gossip is how reputation and old stories travel, including
from grandparents to grandchildren.
"""
from __future__ import annotations

from .person import Memory, Person
from .util import clamp

HARM = ("killed", "attacked", "stole")


def bump(p: Person, other: str, tick: int, affection=0.0, trust=0.0, familiarity=0.0,
         grudge=0.0, respect=0.0, balance=0.0) -> None:
    r = p.relation(other)
    r.affection = clamp(r.affection + affection, -1.0, 1.0)
    r.trust = clamp(r.trust + trust, -1.0, 1.0)
    r.familiarity = clamp(r.familiarity + familiarity)
    r.grudge = clamp(r.grudge + grudge)
    r.respect = clamp(r.respect + respect)
    r.balance += balance
    r.last = tick


def remember(world, p: Person, eid: int, kind: str, actor, target, place, salience: float,
             valence: float, strength: float = 1.0, source: str = "", hops: int = 0) -> bool:
    """Store a memory. Returns False if p already knew it (it is refreshed instead)."""
    for m in p.memories:
        if m.eid == eid:
            m.strength = min(1.0, m.strength + 0.15)
            return False
    p.memories.append(Memory(eid, world.tick, kind, actor, target, tuple(place) if place else (), salience,
                             valence, strength, source, hops))
    if len(p.memories) > world.cfg.memory_capacity:
        weakest = min(range(len(p.memories)), key=lambda i: p.memories[i].salience * p.memories[i].strength)
        p.memories.pop(weakest)
    return True


def closeness(world, p: Person, other_id: str) -> float:
    """How much p cares about another person: love, family or partnership."""
    if other_id == p.id:
        return 1.0
    if other_id == p.partner:
        return 1.0
    other = world.people.get(other_id)
    r = p.rel.get(other_id)
    aff = r.affection if r else 0.0
    kin = world.kinship(p, other) if other else 0.0
    return max(aff, kin)


def react(world, p: Person, kind: str, actor, target, credibility: float, fresh: bool) -> None:
    """How p feels on learning that `actor` did `kind` to `target`."""
    if actor == p.id:
        return
    tick = world.tick
    g = p.genes
    if kind in HARM and actor:
        weight = {"killed": 1.0, "attacked": 0.5, "stole": 0.25}[kind]
        bump(p, actor, tick, trust=-0.4 * weight * credibility, affection=-0.2 * weight * credibility)
        close = closeness(world, p, target) if target else 0.0
        if close > 0.15:
            bump(p, actor, tick, grudge=weight * credibility * close * (0.5 + g["temper"]))
            p.anger = clamp(p.anger + 0.5 * weight * close * credibility)
        if kind == "killed" and fresh and close > 0.3:
            p.grief = clamp(p.grief + 0.7 * close)
        if kind == "killed" and target != p.id:
            p.fear = clamp(p.fear + 0.2 * credibility * g["anxiety"])
    elif kind == "gave" and actor:
        bump(p, actor, tick, trust=0.05 * credibility, respect=0.02 * credibility)
    elif kind == "died" and fresh and target:
        close = closeness(world, p, target)
        if close > 0.3:
            p.grief = clamp(p.grief + 0.6 * close)
    elif kind == "mauled" and actor and actor.startswith("animal:"):
        # Seeing or hearing of an attack teaches fear of that kind of animal.
        from .fauna import learn_fear
        close = closeness(world, p, target) if target else 0.0
        learn_fear(p, actor[7:], (0.15 + 0.25 * close) * credibility)
        p.fear = clamp(p.fear + 0.15 * credibility * (0.5 + g["anxiety"]))


def salience_for(world, p: Person, kind: str, actor, target) -> float:
    base = {"killed": 0.6, "attacked": 0.35, "stole": 0.25, "died": 0.3, "born": 0.2,
            "gave": 0.15, "paired": 0.2, "discovered": 0.3, "mauled": 0.5,
            "storm": 0.3, "flood": 0.35}.get(kind, 0.1)
    involved = max(closeness(world, p, target) if target else 0.0,
                   closeness(world, p, actor) if actor else 0.0)
    return clamp(base + 0.4 * involved)


def witness(world, eid: int, kind: str, actor, target, place, chance: float = 0.7) -> None:
    """Everyone close enough may see it happen."""
    for q in world.people_near(place, world.cfg.perception):
        if q.id in (actor, target) or q.age(world.tick) < 52 * 3:
            continue
        if world.rng.random() < chance:
            sal = salience_for(world, q, kind, actor, target)
            fresh = remember(world, q, eid, kind, actor, target, place, sal, -0.5 if kind in HARM else 0.2)
            react(world, q, kind, actor, target, 1.0, fresh)


def gossip(world, speaker: Person, listener: Person) -> str:
    """The speaker tells a story; the listener decides what to make of it. See information.py."""
    from .information import tell_story
    return tell_story(world, speaker, listener)
