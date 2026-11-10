"""NB1: a small neural network that helps a person decide (experiments/NB1_neural_brain/questions.md, NB1-frozen).

The body stays as it is: hunger, cold, pain, loneliness and the rest still make the feeling r that every week leaves
behind (reward + 2 x mood change). What changes is the deciding. Each candidate option keeps its hand-written score
(the instinct utility and the pulls of what is on the person's mind), multiplied by an inherited gene g; a small
network adds its own score, computed from raw features only. The habit table is not used. Children inherit one
parent's whole network genome with small mutations; nothing learned in a life is inherited. With nb_learn the network
also learns within a life, by REINFORCE with a baseline. Only survival and children decide what spreads.

This module is in code_nb1 only; nb_brain 0 is nature v17 exactly.
"""
from __future__ import annotations

import math

import numpy as np

from .person import A, ACTIONS
from .util import distance
from . import weather

STAGES = ("infant", "child", "teen", "adult", "elder")
N_ACT = len(ACTIONS)
N_BODY = 10 + len(STAGES) + 4 + 1          # body state, life stage, season, company
N_OPT = N_ACT + 4                          # action kind, distance, a person or not, kinship, affection
N_OTH = 2                                  # what others nearby did lately, and how it went for them
N_IN = N_BODY + N_OPT + N_OTH
N_HID = 16
N_W = N_HID * N_IN + N_HID + N_HID + 1

# Chosen constants, recorded as such in questions.md (never tuned on outcomes)
W_SD = 0.02          # mutation of each weight
G_SD = 0.08          # mutation of g (as the temperament genes' mutation)
ETA_SD = 0.002       # mutation of the learning rate
ETA0 = 0.01          # founders' learning rate
OUT_SD0 = 0.05       # founders' output weights: small, so the old scores dominate at first
BASE_RATE = 0.05     # how fast the baseline follows the feeling
CLAMP = 5.0          # weights stay within +-5
G_MAX = 2.0          # amendment 1 (before data): g in [0, 2], so mutation from 1 is not pushed down by a wall at 1

LAST: dict = {}      # (id(world), person id) -> this week's decision, until the week's learning; never saved


def unpack(w):
    w = np.asarray(w, dtype=float)
    k = N_HID * N_IN
    return w[:k].reshape(N_HID, N_IN), w[k:k + N_HID], w[k + N_HID:k + 2 * N_HID], w[-1]


def _new(rng_np, src=None, world_rng=None):
    if src is None:
        w1 = rng_np.normal(0.0, 1.0 / math.sqrt(N_IN), (N_HID, N_IN))
        b1 = np.zeros(N_HID)
        w2 = rng_np.normal(0.0, OUT_SD0, N_HID)
        genome = np.concatenate([w1.ravel(), b1, w2, [0.0]])
        return {"g": 1.0, "eta": ETA0, "genome": genome.tolist(), "w": genome.tolist(), "base": 0.0}
    genome = np.clip(np.asarray(src["genome"]) + rng_np.normal(0.0, W_SD, N_W), -CLAMP, CLAMP)
    g = min(G_MAX, max(0.0, src["g"] + float(rng_np.normal(0.0, G_SD))))   # amendment 1: [0, 2], not [0, 1]
    eta = max(0.0, src["eta"] + float(rng_np.normal(0.0, ETA_SD)))
    return {"g": g, "eta": eta, "genome": genome.tolist(), "w": genome.tolist(), "base": 0.0}


def founder(world) -> dict:
    """A founder's network: random, from the world's own generator."""
    return _new(np.random.default_rng(world.rng.getrandbits(32)))


def child(world, mother, father) -> dict:
    """One parent's whole network genome (chosen by the world's draw), mutated a little."""
    parents = [x for x in (mother, father) if x is not None and x.nb is not None]
    src = parents[world.rng.randrange(len(parents))] if parents else None
    return _new(np.random.default_rng(world.rng.getrandbits(32)), src.nb if src is not None else None)


def body_features(world, p, hunger: float, fatigue: float, company: bool) -> list:
    c = world.cfg
    tick = world.tick
    need = p.need(c, tick)
    st = p.stage(tick)
    cold = min(1.0, max(0.0, weather.coldness(world, p.loc)))
    deps = len(world.dependents(p.id))
    f = [p.energy / 100.0, p.health / 100.0, (min(p.edible() / need, 3.0) / 3.0) if need > 0 else 1.0, p.thirst,
         cold, hunger, fatigue, p.loneliness, p.mood, min(deps, 3) / 3.0]
    f += [1.0 if st == s else 0.0 for s in STAGES]
    f += [1.0 if world.season == k else 0.0 for k in range(4)]
    f.append(1.0 if company else 0.0)
    return f


def option_features(world, p, action: str, target) -> list:
    c = world.cfg
    one = [0.0] * N_ACT
    one[A[action]] = 1.0
    dist, person, kin, aff = 0.0, 0.0, 0.0, 0.0
    if isinstance(target, str) and target in world.people:
        q = world.people[target]
        person = 1.0
        dist = distance(p.loc, q.loc, c.width, c.height) / 10.0
        kin = world.kinship(p, q)
        r = p.rel.get(target)
        aff = r.affection if r is not None else 0.0
    else:
        t = target[0] if action == "gather" and isinstance(target, tuple) else target
        if isinstance(t, tuple) and len(t) == 2 and isinstance(t[0], int) and isinstance(t[1], int):
            dist = distance(p.loc, t, c.width, c.height) / 10.0
    return one + [min(dist, 3.0), person, kin, aff]


def others_features(near) -> dict:
    """For each action: the share of people nearby whose latest action it was, and their mean mood change."""
    out: dict = {}
    if not near:
        return out
    by: dict = {}
    for q in near:
        if q.last_action:
            by.setdefault(q.last_action, []).append(q.mood - q.mood_before)
    for a, ch in by.items():
        out[a] = [len(ch) / len(near), sum(ch) / len(ch)]
    return out


def scores(w, X):
    w1, b1, w2, b2 = unpack(w)
    H = np.tanh(X @ w1.T + b1)
    return H @ w2 + b2, H


def rescore(world, p, options: list, near, hunger: float, fatigue: float, lw: float, base: int) -> list:
    """g x (the hand-written score without the habit table) + the network's score, for each option."""
    nb = p.nb
    if nb is None or not options:
        return options
    body = body_features(world, p, hunger, fatigue, bool(near))
    oth = others_features(near)
    X = np.array([body + option_features(world, p, a, t) + oth.get(a, [0.0, 0.0]) for _, a, t in options])
    out, H = scores(nb["w"], X)
    g = nb["g"]
    new = [(g * (s - lw * p.q[base + A[a]]) + float(out[k]), a, t) for k, (s, a, t) in enumerate(options)]
    LAST[(id(world), p.id)] = [X, H, None, None]
    return new


def chosen(world, p, i: int, final_scores: list, temperature: float) -> None:
    rec = LAST.get((id(world), p.id))
    if rec is not None:
        rec[2] = np.asarray(final_scores, dtype=float)
        rec[3] = (i, temperature)


def grad_logpi(w, X, H, final_scores, i: int, temperature: float):
    """The gradient of log pi(chosen) with respect to the network's numbers (the hand-written part has none)."""
    s = final_scores / temperature
    pr = np.exp(s - s.max())
    pr /= pr.sum()
    coef = -pr
    coef[i] += 1.0
    coef /= temperature
    _, _, w2, _ = unpack(w)
    dpre = (1.0 - H ** 2) * w2
    gw1 = (coef[:, None] * dpre).T @ X
    gb1 = coef @ dpre
    gw2 = coef @ H
    gb2 = coef.sum()
    return np.concatenate([gw1.ravel(), gb1, gw2, [gb2]])


def learn(world, p, r: float, on: int) -> None:
    """The week's learning: w <- w + eta (r - b) grad log pi(chosen); b <- b + 0.05 (r - b)."""
    rec = LAST.pop((id(world), p.id), None)
    nb = p.nb
    if rec is None or nb is None or rec[3] is None:
        return
    if on and nb["eta"] > 0.0:
        X, H, fs, (i, T) = rec
        grad = grad_logpi(nb["w"], X, H, fs, i, T)
        w = np.clip(np.asarray(nb["w"]) + nb["eta"] * (r - nb["base"]) * grad, -CLAMP, CLAMP)
        nb["w"] = w.tolist()
    nb["base"] = nb["base"] + BASE_RATE * (r - nb["base"])


def forget(world, p) -> None:
    """At death the network is dropped: nothing reads it again."""
    p.nb = None
    LAST.pop((id(world), p.id), None)


# NB2: with nb2, the entry points are brain_nb2's (questions.md, NB2-frozen)
_nb1 = {"rescore": rescore, "chosen": chosen, "learn": learn, "founder": founder, "child": child, "forget": forget}


def _two(world):
    return world.cfg.nb2


def rescore(world, p, options, near, hunger, fatigue, lw, base):    # noqa: F811
    if _two(world):
        from . import brain_nb2
        return brain_nb2.rescore(world, p, options, near, hunger, fatigue, lw, base)
    return _nb1["rescore"](world, p, options, near, hunger, fatigue, lw, base)


def chosen(world, p, i, final_scores, temperature):    # noqa: F811
    if _two(world):
        from . import brain_nb2
        return brain_nb2.chosen(world, p, i, final_scores, temperature)
    return _nb1["chosen"](world, p, i, final_scores, temperature)


def learn(world, p, r, on):    # noqa: F811
    if _two(world):
        from . import brain_nb2
        return brain_nb2.learn(world, p, r, on)
    return _nb1["learn"](world, p, r, on)


def founder(world):    # noqa: F811
    if _two(world):
        from . import brain_nb2
        return brain_nb2.founder(world)
    return _nb1["founder"](world)


def child(world, mother, father):    # noqa: F811
    if _two(world):
        from . import brain_nb2
        return brain_nb2.child(world, mother, father)
    return _nb1["child"](world, mother, father)


def forget(world, p):    # noqa: F811
    if _two(world):
        from . import brain_nb2
        return brain_nb2.forget(world, p)
    return _nb1["forget"](world, p)
