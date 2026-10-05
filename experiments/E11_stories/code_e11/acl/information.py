"""Information: what leaves one person and reaches another.

Knowledge lives inside people. When one person tells another something, what
travels is not the knowledge itself but a telling of it, and a telling is never
exact (Laws 51, 77, 80):

- A story is retold from memory. A faded memory gets filled in: the wrong
  person takes the blame, the place shifts, and it grows worse in the telling.
  Someone who holds a grudge is quicker to put that person into a story.
- A way of making something is shown or described. A step can come across
  wrong: the wrong binding, the wrong stone. Sometimes the mistake works better.
- A belief about what to leave where is passed on as a claim. The season or the
  thing can slip.

The speaker does not know what the listener already knows. They talk about
what matters most to them.

The listener then decides (Law 91). Nothing the speaker does writes into the
listener's mind. Every update below is made by the listener, from the
listener's own state: their trust in the speaker, what they can see of how the
speaker is doing, whether the claim fits what they saw with their own eyes,
how many others have said the same, how much attention they have to spare, and
how they feel. They accept the claim, doubt it, or reject it (Laws 56, 84, 92).

What they accept is still only hearsay (Law 61). It stays marked as heard
until their own experience confirms or contradicts it. When that happens, their
trust in whoever told them moves with the result. A contradiction moves it
more than a confirmation (Law 66). People who turn out to be right are believed
more the next time.
"""
from __future__ import annotations

from . import thought
from .config import CHILD_END
from .matter import FLEXIBLE, FORMS, MATERIALS
from .person import PLACEABLE
from .social import HARM, bump, react, remember, salience_for
from .util import clamp

STRIKABLE = ("stone", "flint", "bone", "wood")
HARD = ("stone", "flint", "bone")


# --- the listener judges -------------------------------------------------------------

MAX_RECORDS = 40


def record(listener, source: str) -> tuple[float, float]:
    """What the listener has found out about a source's word: (how often it holds, how much they know).
    With nothing known the estimate is an even chance."""
    rec = listener.records.get(source)
    if rec is None:
        return 0.5, 0.0
    n = rec[0] + rec[1]
    return (rec[0] + 1.0) / (n + 2.0), n


def credence(world, listener, speaker, about: str = "", evidence: float = 0.0) -> float:
    """How far `listener` believes what `speaker` says, 0 .. 1. Reads only what the listener
    feels, knows and can see: never the speaker's mind.

    Two things decide it. General goodwill (trust and respect, built by gifts, help and harm) counts
    most when the listener knows little of how the speaker's word has held up. As the listener's
    record of the speaker grows, the record counts more (Laws 56, 84, 92)."""
    r = listener.rel.get(speaker.id)
    trust = r.trust if r else 0.0
    respect = r.respect if r else 0.0
    goodwill = 0.35 + 0.45 * max(trust, 0.0) - 0.6 * max(-trust, 0.0) + 0.2 * respect
    est, n = record(listener, speaker.id)
    weight = n / (n + 3.0)
    c = (1.0 - weight) * goodwill + weight * (0.05 + 0.95 * est)
    # The young believe the grown-ups around them.
    tick = world.tick
    if listener.age(tick) < CHILD_END and speaker.age(tick) >= CHILD_END:
        c += 0.2
    # Someone who visibly does well is easier to believe (demonstrated success).
    c += 0.25 * (speaker.health / 100.0 - 0.7) - (0.1 if speaker.starving else 0.0)
    c += evidence
    # Fear makes stories of harm and danger easier to believe.
    if about in HARM or about == "mauled":
        c += 0.25 * listener.fear
    # A mind full of something else takes in less.
    if thought.state(listener) == "overthinking":
        c *= 0.6
    return clamp(c)


def _note(listener, source: str, held: float, failed: float) -> None:
    rec = listener.records.get(source)
    if rec is None:
        rec = [0.0, 0.0]
        listener.records[source] = rec
    rec[0] = round(rec[0] + held, 3)
    rec[1] = round(rec[1] + failed, 3)
    if len(listener.records) > MAX_RECORDS:
        least = min(listener.records, key=lambda k: (sum(listener.records[k]), k))
        if least != source:
            del listener.records[least]


def tested(world, p, hkey: str, outcome: float) -> None:
    """p's own experience has now tested something they were told. They remember, for each source of
    the claim, whether its word held. A person who turned out right is also trusted and respected a
    little more; one who turned out wrong, trusted less, and more so (Law 66)."""
    h = p.heard.pop(hkey, None)
    if h is None:
        return
    claim = h[0]
    held = (outcome > 0.05 and claim > 0) or (outcome <= 0.05 and claim <= 0)
    for src in h[1]:
        if src == p.id:
            continue
        _note(p, src, 1.0 if held else 0.0, 0.0 if held else 1.0)
        if src in world.people:
            bump(p, src, world.tick, trust=0.06 if held else -0.1, respect=0.03 if held else 0.0)
    world.emit("verified" if held else "refuted", p.id, None, p.loc, claim=hkey, by=list(h[1]))


def share_reputation(world, speaker, listener) -> bool:
    """The speaker says what they have found about someone's word (Laws 36, 54). The listener
    weighs it like any claim and adds it to their own record as half an observation of their own."""
    best, best_v = None, 0.0
    for src, (hd, fl) in speaker.records.items():
        n = hd + fl
        if n < 2 or src == listener.id or src == speaker.id:
            continue
        v = abs((hd + 1.0) / (n + 2.0) - 0.5) * n
        if v > best_v:
            best, best_v = src, v
    if best is None:
        return False
    hd, fl = speaker.records[best]
    est = (hd + 1.0) / (hd + fl + 2.0)
    c = credence(world, listener, speaker)
    _note(listener, best, 0.5 * c * est, 0.5 * c * (1.0 - est))
    world.emit("vouched", speaker.id, listener.id, None, about=best, good=1 if est > 0.5 else 0,
               record=[round(hd, 1), round(fl, 1)])
    return True


# --- stories ----------------------------------------------------------------------------

def tell_story(world, speaker, listener) -> str:
    """The speaker tells one of the stories that matter most to them, as they now remember it.
    Returns what the listener made of it: accepted, doubted, rejected, known, or "" if nothing was told."""
    rng = world.rng
    stories = sorted((m for m in speaker.memories if m.salience * m.strength >= 0.15),
                     key=lambda m: (-(m.salience * m.strength), m.eid))[:4]
    if not stories:
        return ""
    weights = [m.salience * m.strength for m in stories]
    pick = rng.random() * sum(weights)
    m = stories[-1]
    for cand, wgt in zip(stories, weights):
        pick -= wgt
        if pick <= 0:
            m = cand
            break
    msg = _recall(world, speaker, m)
    m.strength = min(1.0, m.strength + 0.05)          # telling it keeps it alive for the teller
    result = hear_story(world, listener, speaker, msg)
    world.emit("told", speaker.id, listener.id, None, story=m.eid, about=m.kind,
               of=msg["actor"] or "", to=msg["target"] or "", hops=msg["hops"], heard=result,
               changed=1 if msg["actor"] != m.actor else 0)
    return result


def _recall(world, speaker, m) -> dict:
    """The speaker's telling of memory m. Never exact; less exact the more it has faded."""
    rng = world.rng
    c = world.cfg
    fade = 1.0 - m.strength
    actor = m.actor
    if actor and actor.startswith("animal:"):
        if rng.random() < 0.02 + 0.15 * fade:
            actor = "animal:" + ("bear" if actor == "animal:wolf" else "wolf")
    elif actor and rng.random() < 0.03 + 0.3 * fade:
        actor = _suspect(world, speaker, m) or actor
    place = m.place
    if place and len(place) == 2 and rng.random() < 0.1 + 0.4 * fade:
        place = ((place[0] + rng.randint(-1, 1)) % c.width, (place[1] + rng.randint(-1, 1)) % c.height)
    valence = clamp(m.valence * (1.0 + 0.2 * rng.random()), -1.0, 1.0)   # it grows in the telling
    return {"eid": m.eid, "kind": m.kind, "actor": actor, "target": m.target, "place": place,
            "valence": valence, "strength": m.strength, "hops": m.hops + 1}


def _suspect(world, speaker, m):
    """Who a fading memory gets pinned on instead: most likely someone the teller already dislikes."""
    rng = world.rng
    cands, weights = [], []
    for pid, r in speaker.rel.items():
        if pid in (m.actor, m.target, speaker.id):
            continue
        w = 0.05 * r.familiarity + 1.5 * r.grudge + 0.8 * max(-r.affection, 0.0)
        if w > 0.02:
            cands.append(pid)
            weights.append(w)
    if not cands:
        return None
    pick = rng.random() * sum(weights)
    for pid, w in zip(cands, weights):
        pick -= w
        if pick <= 0:
            return pid
    return cands[-1]


def hear_story(world, listener, speaker, msg: dict) -> str:
    """The listener weighs a story and decides what to make of it."""
    result = _hear_story(world, listener, speaker, msg)
    # E11 (S1): a story of a death from hunger, not doubted or rejected, leaves a lesson for its season.
    if world.cfg.story_value > 0 and result in ("accepted", "known"):
        info = getattr(world, "death_info", {}).get(msg["eid"])
        if info and info[0] == "starvation":
            key = f"loss@{info[1]}"
            lesson = world.cfg.story_value * credence(world, listener, speaker, msg["kind"]) * msg["strength"]
            listener.expect[key] = max(listener.expect.get(key, 0.0), round(lesson, 4))
    return result


def _hear_story(world, listener, speaker, msg: dict) -> str:
    tick = world.tick
    eid = msg["eid"]
    own = next((m for m in listener.memories if m.eid == eid), None)
    if own is not None:
        if own.source == "":
            # They were there.
            if msg["actor"] != own.actor:
                bump(listener, speaker.id, tick, trust=-0.08)        # "that's not what happened"
                world.emit("disputed", listener.id, speaker.id, None, story=eid,
                           said=msg["actor"] or "", saw=own.actor or "")
                return "rejected"
            own.strength = min(1.0, own.strength + 0.1)
            return "known"
        if msg["actor"] == own.actor:
            own.strength = min(1.0, own.strength + 0.1)              # others say so too
            return "known"
        # Two versions of the same story: keep the one from whoever is more believed.
        before = world.people.get(own.source)
        old_c = credence(world, listener, before, own.kind) if before is not None else 0.3
        new_c = credence(world, listener, speaker, own.kind)
        if new_c > old_c + 0.1 and world.rng.random() < new_c:
            own.actor, own.source, own.hops = msg["actor"], speaker.id, msg["hops"]
            react(world, listener, own.kind, own.actor, own.target, new_c, False)
            return "accepted"
        return "doubted"
    c = credence(world, listener, speaker, msg["kind"])
    if world.rng.random() >= c:
        return "doubted"
    sal = salience_for(world, listener, msg["kind"], msg["actor"], msg["target"])
    fresh = remember(world, listener, eid, msg["kind"], msg["actor"], msg["target"], msg["place"], sal,
                     msg["valence"], strength=0.7 * msg["strength"] * c, source=speaker.id, hops=msg["hops"])
    react(world, listener, msg["kind"], msg["actor"], msg["target"], c, fresh)
    return "accepted"


# --- ways of making things, and what to leave where -----------------------------------------

def show_how(world, teacher, learner, parent: bool) -> bool:
    """The teacher shows or tells one of the things they value most. Returns True if the learner took
    something new from it."""
    rng = world.rng
    offers = []
    for sig in teacher.recipes:
        v = teacher.itemval.get(sig, 0.0)
        if v > 0.15:
            offers.append((v, "m", sig))
    for key, v in _beliefs_of(teacher).items():
        if v > 0.15:
            offers.append((v, "b", key))
    if not offers:
        return False
    offers.sort(key=lambda o: (-o[0], o[2]))
    offers = offers[:3]
    v, kind, what = offers[rng.randrange(len(offers))]
    claim = v * (0.85 + 0.35 * rng.random())          # people talk up what works for them
    if kind == "m":
        recipe = _recipe_as_shown(world, teacher, learner, teacher.recipes[what])
        return hear_how(world, learner, teacher, what, recipe, claim, parent)
    key = _belief_as_told(world, what)
    return hear_belief(world, learner, teacher, key, claim, parent)


def _beliefs_of(p) -> dict:
    """What p would pass on about leaving things: what they found out, and what they were told."""
    out = {}
    for hkey, h in p.heard.items():
        if hkey.startswith("b:"):
            out[hkey[2:]] = h[0]
    out.update(p.beliefs)
    return out


def _recipe_as_shown(world, teacher, learner, recipe: dict) -> dict:
    """The recipe as the learner takes it in. Showing it with the things in hand helps; skill on
    both sides helps; a step can still come across wrong."""
    from .mind import can_make
    rng = world.rng
    err = 0.3 - 0.15 * teacher.skills["crafting"] - 0.1 * learner.skills["crafting"]
    if can_make(teacher, recipe):
        err -= 0.1
    out = dict(recipe)
    if "parts" in out:
        out["parts"] = list(out["parts"])
    if rng.random() >= max(0.04, err):
        return out
    if out["verb"] == "shape":
        out["form"] = rng.choice([f for f in FORMS if f != out["form"]])
        return out
    if out["verb"] == "heat":
        if out["part"] in MATERIALS:
            out["part"] = rng.choice([m for m in MATERIALS if m != out["part"]])
        return out
    if out["verb"] == "strike":
        roll = rng.random()
        if roll < 0.4:
            out["tool"] = rng.choice([h for h in HARD if h != out["tool"]])
        elif roll < 0.8:
            out["target"] = rng.choice([t for t in STRIKABLE if t != out["target"]])
        elif out["target"] in HARD:
            out["target"], out["tool"] = out["tool"], out["target"]
    else:
        raw = [i for i, part in enumerate(out["parts"]) if part in MATERIALS]
        if raw and rng.random() < 0.6:
            i = raw[rng.randrange(len(raw))]
            out["parts"][i] = rng.choice([m for m in MATERIALS if m != out["parts"][i]])
            out["parts"] = sorted(out["parts"])
        else:
            out["binder"] = [b for b in FLEXIBLE if b != out["binder"]][0]
    return out


def _belief_as_told(world, key: str) -> str:
    rng = world.rng
    thing, season = key.split("@")
    season = int(season)
    if rng.random() < 0.1:
        season = (season + rng.choice((-1, 1))) % 4
    if rng.random() < 0.04:
        thing = rng.choice([t for t in PLACEABLE if t != thing])
    return f"{thing}@{season}"


def _sig_of(recipe: dict) -> str:
    v = recipe["verb"]
    if v == "strike":
        return f"{recipe['target']}/{recipe['tool']}"
    if v == "shape":
        return f"{recipe['material']}~{recipe['form']}"
    if v == "heat":
        return f"{recipe['part']}^{recipe.get('level', 0)}"
    if v == "fill":
        return f"try:fill:{recipe['substance']}"
    return f"({recipe['parts'][0]}+{recipe['parts'][1]})#{recipe['binder']}"


def _openness(learner, parent: bool) -> float:
    return 0.35 * (0.5 + learner.genes["curiosity"]) * (2.0 if parent else 1.0)


def hear_how(world, learner, teacher, meant: str, recipe: dict, claim: float, parent: bool) -> bool:
    """The learner decides whether to take up a way of making something, as they understood it."""
    from .knowhow import can_follow, remember_recipe
    sig = _sig_of(recipe)
    if sig in learner.recipes:
        return False
    holds = any(it["sig"] == meant for it in teacher.items)
    c = credence(world, learner, teacher, evidence=0.15 if holds else 0.0)
    own = learner.itemval.get(sig)
    if own is not None and own < -0.1 and "m:" + sig not in learner.heard:
        bump(learner, teacher.id, world.tick, trust=-0.03)    # they tried that and it was no good
        return False
    if world.rng.random() >= c * _openness(learner, parent):
        return False
    if not can_follow(learner, recipe):
        return False                                        # it needs a part they cannot make
    remember_recipe(world, learner, sig, recipe, "taught", teacher.id, meant=meant)
    learner.itemval[sig] = max(learner.itemval.get(sig, 0.0), 0.5 * claim * c)
    learner.heard["m:" + sig] = [round(claim, 3), [teacher.id], world.tick]
    _wonder(world, learner, "m:" + sig, claim)
    return True


def _wonder(world, p, key: str, claim: float) -> None:
    """Something told that would matter, if true, is something to go and check (Law 64)."""
    from .inquiry import notice
    notice(world, p, key, 0.1 + 0.35 * p.genes["curiosity"] * min(1.0, abs(claim)))


def hear_belief(world, learner, teacher, key: str, claim: float, parent: bool) -> bool:
    """The learner weighs a claim about what is worth leaving where."""
    tick = world.tick
    own = learner.beliefs.get(key)
    if own is not None:
        if own * claim < 0 and abs(own) > 0.15:
            bump(learner, teacher.id, tick, trust=-0.03)     # their own experience says otherwise
        return False
    c = credence(world, learner, teacher)
    h = learner.heard.get("b:" + key)
    if h is not None:
        if teacher.id in h[1]:
            return False
        # Someone else says the same: more people, more belief (social proof).
        h[1].append(teacher.id)
        h[1] = h[1][-4:]
        h[0] = round(clamp(h[0] + 0.5 * (claim * c - h[0]) + 0.05, -1.0, 1.0), 3)
        world.emit("learn", learner.id, teacher.id, learner.loc, belief=key, how="told", again=len(h[1]))
        return True
    if world.rng.random() >= c * _openness(learner, parent):
        return False
    learner.heard["b:" + key] = [round(0.6 * claim * c, 3), [teacher.id], tick]
    world.emit("learn", learner.id, teacher.id, learner.loc, belief=key, how="told")
    _wonder(world, learner, "b:" + key, claim)
    return True


# --- where things are: water, and animals lately seen ------------------------------------------------

def tell_place(world, speaker, listener) -> bool:
    """The speaker says where they saw animals lately, or where there is water. Animals move on, so a
    sighting is only worth something while it is fresh; whoever is out and looking knows best. People
    also pass on what they were told, which is older, and a place can shift in the telling."""
    rng = world.rng
    tick = world.tick
    c = world.cfg
    offers = []
    for x, y, t, sp in speaker.sightings:
        offers.append((max(0.1, 1.0 - (tick - t) / 12.0), f"g:{x},{y}", False))
    for hkey, h in speaker.heard.items():
        if hkey[:2] in ("g:", "w:"):
            offers.append((0.7 * h[0], hkey, True))
    for x, y in speaker.springs[-2:]:
        offers.append((0.6, f"w:{x},{y}", False))
    if not offers:
        return False
    offers.sort(key=lambda o: (-o[0], o[1]))
    claim, key, relayed = offers[0]
    kind, xy = key[:2], key[2:]
    x, y = (int(v) for v in xy.split(","))
    if rng.random() < 0.1 + (0.2 if relayed else 0.0):
        x, y = (x + rng.randint(-1, 1)) % c.width, (y + rng.randint(-1, 1)) % c.height
    return hear_place(world, listener, speaker, f"{kind}{x},{y}", claim)


def hear_place(world, listener, speaker, key: str, claim: float) -> bool:
    if key in listener.heard:
        h = listener.heard[key]
        if speaker.id not in h[1]:
            h[1].append(speaker.id)
            h[1] = h[1][-4:]
        return False
    if key[:2] == "w:" and [int(v) for v in key[2:].split(",")] in listener.springs:
        return False
    c = credence(world, listener, speaker)
    if world.rng.random() >= c:
        return False
    listener.heard[key] = [round(claim * c, 3), [speaker.id], world.tick]
    world.emit("learn", listener.id, speaker.id, listener.loc, spot=key, how="told")
    return True


def check_places(world, p) -> None:
    """Told of water or animals somewhere, p checks as soon as the spot is in plain view."""
    from .fauna import PREY, near
    from .util import distance
    from .weather import fresh_near
    c = world.cfg
    for key in [k for k in p.heard if k[:2] in ("g:", "w:")]:
        h = p.heard[key]
        x, y = (int(v) for v in key[2:].split(","))
        if key[:2] == "g:" and world.tick - h[2] > 12:
            del p.heard[key]                 # too old to be worth checking
            continue
        if distance(p.loc, (x, y), c.width, c.height) > 2:
            continue
        if key[:2] == "w:":
            there = fresh_near(world, (x, y), 1) is not None
            if there and [x, y] not in p.springs:
                p.springs.append([x, y])
                p.springs = p.springs[-4:]
        else:
            there = any(g["sp"] in PREY and g["sp"] != "fish" and g["n"] > 0 for g in near(world, (x, y), 1))
        tested(world, p, key, 1.0 if there else -1.0)

