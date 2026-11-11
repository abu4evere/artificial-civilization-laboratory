"""NB2: the neural brain connected to the world (experiments/NB2_connected_brain/questions.md, NB2-frozen).

On top of NB1's network (brain_nb.py, which this module reuses for genomes, inheritance and REINFORCE):
  nb_sight   the network sees the facts about each offered option (the place, the person, the action, the recipe) and
             about one's own stash, as raw numbers with masks; the instinct score is never an input
  nb_critic  an actor-critic: a critic network learns V(state); the step is the TD error
             delta = r + 0.95 V(next) - V(this), with the exact gradient of log pi, clipped to norm 1.0
  nb_social  learning from others into the network: a child under 14 with its carer in reach steps toward the carer's
             action; otherwise a step toward the action of the person nearby whose mood rose most last week
  nb_g_fixed  for the common gardens only: g is held at this value for everyone (-1 = off)
The options themselves (what the body can do, several targets per action) are built in mind.decide (nb_options).

This module is in code_nb2 only.
"""
from __future__ import annotations

import math

import numpy as np

from . import brain_nb as nb1
from .person import A, ACTIONS
from .util import distance
from . import weather

N_ACT = len(ACTIONS)
N_BODY = nb1.N_BODY + 1                    # NB1's body features, and one's own stash nearby
N_OPT = N_ACT + 4 + 5 + 8 + 2 + 3          # action, NB1's four; place 5; person 8; action 2; recipe 3
N_OTH = 2
N_IN = N_BODY + N_OPT + N_OTH
N_HID = 16
N_ACTOR = N_HID * N_IN + N_HID + N_HID + 1
N_CRITIC = N_HID * N_BODY + N_HID + N_HID + 1
N_W = N_ACTOR + N_CRITIC

# Chosen constants (questions.md; recorded as constants, never tuned on outcomes)
GAMMA = 0.95
ETA0_AC = 0.001          # founders' actor learning rate with the critic (evolvable)
ETA_SD_AC = 0.0002
ETA_V = 0.005            # critic learning rate (fixed)
CLIP = 1.0
SOC_CHILD = 0.5          # social step, a child toward its carer: 0.5 x eta
SOC_WATCH = 0.2          # social step toward someone whose mood rose: 0.2 x eta
CHILD_YEARS = 14

PLACE: dict = {}         # within one decision only: a place's facts (read-only computations, so caching changes nothing)
PERSON: dict = {}        # within one decision only: a person's facts
WATER: dict = {}         # (the map's seed and size, reach, tile) -> fresh water within reach (biomes never change)
LAST: dict = {}          # (id(world), pid) -> this week's decision record, until the week's learning; never saved
CHOSEN: dict = {}        # (id(world), pid) -> (tick, action, target) of this week's decision; never saved
OBS: dict = {}           # (id(world), pid) -> (tick, action, mood change) seen by others next week; never saved


def unpack_actor(w):
    w = np.asarray(w, dtype=float)
    k = N_HID * N_IN
    return w[:k].reshape(N_HID, N_IN), w[k:k + N_HID], w[k + N_HID:k + 2 * N_HID], w[N_ACTOR - 1]


def unpack_critic(w):
    v = np.asarray(w, dtype=float)[N_ACTOR:]
    k = N_HID * N_BODY
    return v[:k].reshape(N_HID, N_BODY), v[k:k + N_HID], v[k + N_HID:k + 2 * N_HID], v[-1]


def _genome(rng_np):
    w1 = rng_np.normal(0.0, 1.0 / math.sqrt(N_IN), (N_HID, N_IN))
    w2 = rng_np.normal(0.0, nb1.OUT_SD0, N_HID)
    c1 = rng_np.normal(0.0, 1.0 / math.sqrt(N_BODY), (N_HID, N_BODY))
    c2 = rng_np.normal(0.0, nb1.OUT_SD0, N_HID)
    return np.concatenate([w1.ravel(), np.zeros(N_HID), w2, [0.0], c1.ravel(), np.zeros(N_HID), c2, [0.0]])


def founder(world) -> dict:
    rng_np = np.random.default_rng(world.rng.getrandbits(32))
    g = _genome(rng_np)
    eta = ETA0_AC if world.cfg.nb_critic else nb1.ETA0
    out = {"g": 1.0, "eta": eta, "genome": g.tolist(), "w": g.tolist(), "base": 0.0}
    if world.cfg.nb3:                       # NB3: the feeling genes (founders: the start values)
        from . import brain_nb3
        brain_nb3.add_genes(out, None, rng_np)
    return out


def child(world, mother, father) -> dict:
    parents = [x for x in (mother, father) if x is not None and x.nb is not None]
    src = parents[world.rng.randrange(len(parents))] if parents else None
    rng_np = np.random.default_rng(world.rng.getrandbits(32))
    if src is None:
        g = _genome(rng_np)
        eta = ETA0_AC if world.cfg.nb_critic else nb1.ETA0
        out = {"g": 1.0, "eta": eta, "genome": g.tolist(), "w": g.tolist(), "base": 0.0}
        if world.cfg.nb3:
            from . import brain_nb3
            brain_nb3.add_genes(out, None, rng_np)
        return out
    s = src.nb
    genome = np.clip(np.asarray(s["genome"]) + rng_np.normal(0.0, nb1.W_SD, N_W), -nb1.CLAMP, nb1.CLAMP)
    g = min(nb1.G_MAX, max(0.0, s["g"] + float(rng_np.normal(0.0, nb1.G_SD))))
    eta_sd = ETA_SD_AC if world.cfg.nb_critic else nb1.ETA_SD
    eta = max(0.0, s["eta"] + float(rng_np.normal(0.0, eta_sd)))
    out = {"g": g, "eta": eta, "genome": genome.tolist(), "w": genome.tolist(), "base": 0.0}
    if world.cfg.nb3:                       # NB3: the feeling genes, from the same parent, mutated
        from . import brain_nb3
        brain_nb3.add_genes(out, s, rng_np)
    return out


def _own_stash(world, p) -> float:
    from .mind import own_stash
    need = p.need(world.cfg, world.tick)
    tot = sum(e[1] + e[2] for _, e in own_stash(world, p, world.cfg.reach))
    return min(tot / need, 3.0) / 3.0 if need > 0 else 0.0


def body(world, p, hunger: float, fatigue: float, company: bool) -> list:
    return nb1.body_features(world, p, hunger, fatigue, company) + [_own_stash(world, p)]


def _place(world, p, loc) -> list:
    from . import fauna
    c = world.cfg
    need = p.need(c, world.tick)
    tile = world.tile(loc)
    food = min((tile.plants + tile.crop) / need, 3.0) / 3.0 if need > 0 else 0.0
    prey = min(fauna.prey_here(world, loc), 3) / 3.0
    key = (c.seed, c.width, c.height, c.water_reach, loc)   # fresh water depends only on the map, which never changes
    water = WATER.get(key)
    if water is None:
        water = WATER[key] = 1.0 if weather.fresh_near(world, loc, c.water_reach) is not None else 0.0
    fire = 1.0 if tile.fire > 0 else 0.0
    return [food, prey, water, fire, 1.0]


def _person(world, p, q) -> list:
    from .mind import strength
    c = world.cfg
    tick = world.tick
    qn = q.need(c, tick)
    food = min(q.edible() / qn, 3.0) / 3.0 if qn > 0 else 0.0
    hunger = min(1.0, max(0.0, 1.0 - (q.edible() / qn) / 2.0)) if qn > 0 else 0.0
    r = p.rel.get(q.id)
    trust = r.trust if r is not None else 0.0
    grudge = r.grudge if r is not None else 0.0
    st = max(-1.0, min(1.0, strength(world, q) - strength(world, p)))
    young = 1.0 if q.stage(tick) in ("infant", "child") else 0.0
    return [food, hunger, q.health / 100.0, trust, grudge, st, young, 1.0]


def _loc_of(target):
    """The place an option is about, if any: a tile, (tile, kind) for gather, or (tile, owner) for take."""
    if isinstance(target, tuple) and len(target) == 2:
        a = target[0]
        if isinstance(a, tuple) and len(a) == 2 and isinstance(a[0], int):
            return a
        if isinstance(a, int) and isinstance(target[1], int):
            return target
    return None


def option(world, p, action: str, target) -> list:
    from .mind import COST
    f = nb1.option_features(world, p, action, target)
    loc = _loc_of(target)
    if loc is None:
        place = [0.0] * 5
    else:                                   # the same facts for every option about this place, within one decision
        place = PLACE.get(loc)
        if place is None:
            place = PLACE[loc] = _place(world, p, loc)
    q = world.people.get(target) if isinstance(target, str) else None
    if q is None:
        person = [0.0] * 8
    else:                                   # the same facts for every option about this person, within one decision
        person = PERSON.get(q.id)
        if person is None:
            person = PERSON[q.id] = _person(world, p, q)
    heard = 1.0 if loc is not None and f"g:{loc[0]},{loc[1]}" in p.heard else 0.0
    act = [COST[action] / 40.0, heard]
    if action == "make" and isinstance(target, str) and target in p.recipes:
        from .mind import _holding
        held = 1.0 if _holding(p, target, worn_ok=True) else 0.0
        recipe = [min(p.itemval.get(target, 0.0), 2.0) / 2.0, held, 1.0]
    else:
        recipe = [0.0, 0.0, 0.0]
    return f + place + person + act + recipe


def actor_scores(w, X):
    w1, b1, w2, b2 = unpack_actor(w)
    H = np.tanh(X @ w1.T + b1)
    return H @ w2 + b2, H


def value(w, s):
    c1, d1, c2, d2 = unpack_critic(w)
    h = np.tanh(c1 @ s + d1)
    return float(h @ c2 + d2), h


def rescore(world, p, options: list, near, hunger: float, fatigue: float, lw: float, base: int) -> list:
    nb = p.nb
    if nb is None or not options:
        return options
    S = np.array(body(world, p, hunger, fatigue, bool(near)))
    oth = nb1.others_features(near)
    PLACE.clear()
    PERSON.clear()
    X = np.array([list(S) + option(world, p, a, t) + oth.get(a, [0.0, 0.0]) for _, a, t in options])
    out, H = actor_scores(nb["w"], X)
    gf = world.cfg.nb_g_fixed
    g = gf if gf >= 0.0 else nb["g"]
    if world.cfg.nb3:                       # NB3: the inborn reluctance to harm (not scaled by g)
        from . import brain_nb3
        hb = [brain_nb3.harm_bias(world, p, a, t) for _, a, t in options]
    else:
        hb = [0.0] * len(options)
    new = [(g * (s - lw * p.q[base + A[a]]) + hb[k] + float(out[k]), a, t) for k, (s, a, t) in enumerate(options)]
    LAST[(id(world), p.id)] = [X, H, None, None, S, [(a, t) for _, a, t in options]]
    return new


def chosen(world, p, i: int, final_scores: list, temperature: float) -> None:
    rec = LAST.get((id(world), p.id))
    if rec is not None:
        rec[2] = np.asarray(final_scores, dtype=float)
        rec[3] = (i, temperature)
        a, t = rec[5][i]
        CHOSEN[(id(world), p.id)] = (world.tick, a, t)


def grad_logpi(w, X, H, final_scores, i: int, temperature: float):
    """The exact gradient of log pi(option i) with respect to the actor's numbers; zeros for the critic's."""
    s = final_scores / temperature
    pr = np.exp(s - s.max())
    pr /= pr.sum()
    coef = -pr
    coef[i] += 1.0
    coef /= temperature
    _, _, w2, _ = unpack_actor(w)
    dpre = (1.0 - H ** 2) * w2
    gw1 = (coef[:, None] * dpre).T @ X
    gb1 = coef @ dpre
    gw2 = coef @ H
    gb2 = coef.sum()
    return np.concatenate([gw1.ravel(), gb1, gw2, [gb2], np.zeros(N_CRITIC)])


def grad_value(w, s):
    """The gradient of V(s) with respect to the critic's numbers; zeros for the actor's."""
    c1, d1, c2, d2 = unpack_critic(w)
    h = np.tanh(c1 @ s + d1)
    dpre = (1.0 - h ** 2) * c2
    return np.concatenate([np.zeros(N_ACTOR), np.outer(dpre, s).ravel(), dpre, h, [1.0]])


def clip(v):
    n = float(np.linalg.norm(v))
    return v * (CLIP / n) if n > CLIP else v


def _state_now(world, p):
    from .mind import hunger_of
    c = world.cfg
    deps = world.dependents(p.id)
    hunger = hunger_of(world, p, sum(d.need(c, world.tick) for d in deps))
    near = world.people_near(p.loc, c.reach, exclude=p.id)
    return np.array(body(world, p, hunger, 1.0 - p.energy / 100.0, bool(near)))


def _match(acts, action, target):
    """The index of the observed (action, target) among one's own options: the same target if offered, else the first
    option of the same kind; None if that kind is not offered."""
    first = None
    for k, (a, t) in enumerate(acts):
        if a == action:
            if t == target:
                return k
            if first is None:
                first = k
    return first


def _social(world, p, rec, w, eta):
    c = world.cfg
    X, H, fs, (i, T), S, acts = rec
    key = id(world)
    tick = world.tick                          # the body phase runs before the tick moves on: this week
    j, step = None, 0.0
    if p.age(world.tick) < CHILD_YEARS * 52 and p.caregiver:
        carer = world.people.get(p.caregiver)
        ch = CHOSEN.get((key, p.caregiver))
        if (carer is not None and carer.alive and ch is not None and ch[0] == tick
                and distance(p.loc, carer.loc, c.width, c.height) <= c.reach):
            j = _match(acts, ch[1], ch[2])
            step = SOC_CHILD * eta
    if j is None:
        best = None
        for q in world.people_near(p.loc, c.reach, exclude=p.id):
            ob = OBS.get((key, q.id))
            if ob is None or ob[0] != tick - 1 or ob[2] <= 0.0:
                continue
            if best is None or ob[2] > best[2] or (ob[2] == best[2] and q.id < best[3]):
                best = (ob[1], None, ob[2], q.id)
        if best is not None:
            j = _match(acts, best[0], None)
            step = SOC_WATCH * eta
    if j is None or step <= 0.0:
        return w
    return np.clip(w + step * clip(grad_logpi(w, X, H, fs, j, T)), -nb1.CLAMP, nb1.CLAMP)


def learn(world, p, r: float, on: int) -> None:
    """The week's learning. Without the critic: NB1's REINFORCE (brain_nb.learn's rule). With it: the TD step for actor
    and critic. With nb_social: then one social step."""
    c = world.cfg
    key = (id(world), p.id)
    rec = LAST.pop(key, None)
    nb = p.nb
    if nb is not None:
        OBS[key] = (world.tick, p.last_action, p.mood - p.mood_before)
    if rec is None or nb is None or rec[3] is None:
        return
    X, H, fs, (i, T), S, acts = rec
    w = np.asarray(nb["w"], dtype=float)
    eta = nb["eta"]
    if on and eta > 0.0:
        if c.nb_critic:
            v, _ = value(w, S)
            v2, _ = value(w, _state_now(world, p))
            delta = r + GAMMA * v2 - v
            ga = clip(delta * grad_logpi(w, X, H, fs, i, T))
            gv = clip(delta * grad_value(w, S))
            w = np.clip(w + eta * ga + ETA_V * gv, -nb1.CLAMP, nb1.CLAMP)
        else:
            w = np.clip(w + eta * (r - nb["base"]) * grad_logpi(w, X, H, fs, i, T), -nb1.CLAMP, nb1.CLAMP)
        if c.nb_social:
            w = _social(world, p, rec, w, eta)
        nb["w"] = w.tolist()
    nb["base"] = nb["base"] + nb1.BASE_RATE * (r - nb["base"])


def forget(world, p) -> None:
    p.nb = None
    LAST.pop((id(world), p.id), None)
    CHOSEN.pop((id(world), p.id), None)
    OBS.pop((id(world), p.id), None)
