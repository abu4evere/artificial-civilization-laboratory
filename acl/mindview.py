"""What is going on in someone's head, in words, for us to read.

The people have no words. This module turns what is really there into
sentences: what holds their attention this week and how strongly, the choices
they weighed and the one they took, what puzzles them, what they were told but
have not checked, and what the marks they know have come to go with for them.
It only reads.
"""
from __future__ import annotations

from . import thought
from .config import SEASONS
from .historian import CLASSES, classify, describe

ACTION_WORDS = {
    "rest": "rest", "forage": "gather plants to eat", "hunt": "hunt", "gather": "pick up",
    "put": "set down", "take": "fetch food left earlier", "make": "make", "play": "fiddle with things",
    "explore": "wander off and look around", "give": "give food to", "care": "look after", "talk": "talk with",
    "court": "court", "steal": "steal from", "attack": "attack", "flee": "get away from danger",
    "join": "go to",
}


def _name(world, pid) -> str:
    q = world.people.get(pid) if pid else None
    return q.name if q else "someone"


def _thing(world, sig: str) -> str:
    rec = world.knowledge.get(sig, {})
    cls = classify(rec.get("props"))
    if cls:
        return CLASSES[cls[0]][0]
    recipe = rec.get("recipe")
    return "the thing made by " + describe(recipe, world) if recipe else "a thing of their own"


def _memory(world, p, eid) -> str:
    for m in p.memories:
        if str(m.eid) == str(eid):
            a, b = _name(world, m.actor) if m.actor and not m.actor.startswith("animal:") else \
                {"animal:wolf": "the wolves", "animal:bear": "the bear"}.get(m.actor or "", "it"), _name(world, m.target)
            return {"killed": f"{a} killing {b}", "attacked": f"{a} attacking {b}", "stole": f"{a} stealing from {b}",
                    "died": f"{b} dying", "mauled": f"{a} going for {b}", "storm": "the storm",
                    "flood": "the flood"}.get(m.kind, "what happened")
    return "something that happened"


def _source(world, src) -> str:
    if src and src.startswith("mark:"):
        return f"the mark <{src[5:]}>"
    return _name(world, src)


def puzzle_words(world, p, key: str) -> str:
    kind, what = key[:2], key[2:]
    if kind == "f:":
        target, _, tool = what.partition("/")
        return f"what happens when {target} is struck with {tool}"
    if kind == "m:":
        return f"why {_thing(world, what)} turned out the way it did"
    if kind == "b:":
        thing, season = what.split("@")
        return f"what became of the {thing} left in {SEASONS[int(season)]}"
    if kind == "k:":
        return f"the mark <{what}>"
    return what


def thought_words(world, p, kind: str, about) -> str:
    n = _name(world, about) if isinstance(about, str) and about.startswith("p") else ""
    words = {
        "hunger": lambda: "hungry; where is food?",
        "thirst": lambda: "thirsty; where is water?",
        "cold": lambda: "cold; needs warmth",
        "tired": lambda: "tired",
        "sick": lambda: "feels ill",
        "grief": lambda: f"grieving for {n}" if n else "grieving",
        "memory": lambda: f"can't stop going over {_memory(world, p, about)}",
        "grudge": lambda: f"wants {n} to pay for what they did",
        "fear": lambda: f"afraid of {n}",
        "dread": lambda: f"afraid of {'wolves' if about == 'wolf' else 'bears' if about == 'bear' else about}",
        "love": lambda: f"glad to be near {n}",
        "missing": lambda: f"misses {n}",
        "worry": lambda: f"worried about {n}",
        "curiosity": lambda: "curious about the things in their hands",
        "craft": lambda: f"wants to make {_thing(world, about)} again" if about else "wants to make something",
        "puzzle": lambda: f"puzzling over {puzzle_words(world, p, about)}" if isinstance(about, str) and about
                  else "puzzled",
        "mate": lambda: "wishes for someone to be with",
        "shore": lambda: "wonders what is across the water",
        "lonely": lambda: "lonely",
    }.get(kind)
    return words() if words else kind


def _place_words(world, p, aim: str) -> str:
    """Where a choice was headed, as the chooser could see it."""
    from .weather import fresh_near
    try:
        x, y = (int(v) for v in aim.split(","))
    except ValueError:
        return "somewhere else"
    if p.home() == (x, y):
        return "home"
    if world.tile((x, y)).fire > 0:
        return "the fire"
    if fresh_near(world, (x, y), 1) is not None:
        return "the water"
    if world.people_near((x, y), 0, exclude=p.id):
        return "the others"
    return "somewhere else"


def choice_words(world, p, action: str, aim: str) -> str:
    verb = ACTION_WORDS.get(action, action)
    if aim and aim in world.people:
        return f"{verb} {_name(world, aim)}"
    if action in ("join", "explore", "flee") and aim and "," in aim:
        return ("go to " if action == "join" else verb + " toward ") + _place_words(world, p, aim)
    if action == "make" and aim:
        return f"make {_thing(world, aim)} again"
    if action == "put" and aim:
        return f"set down {aim} here"
    return verb


def mind(world, p) -> dict:
    """Everything going on in p's head this week, in words."""
    tick = world.tick
    state = thought.state(p)
    thoughts = [{"text": thought_words(world, p, k, a), "pull": s} for k, a, s in p.thoughts]
    weighed = [{"text": choice_words(world, p, act, aim), "score": sc, "chosen": bool(ch)}
               for act, aim, sc, ch in p.considered]
    puzzles = [{"text": puzzle_words(world, p, k), "pull": v[0], "tests": v[2]}
               for k, v in sorted(p.puzzles.items(), key=lambda kv: -kv[1][0])]
    heard = []
    for key, h in sorted(p.heard.items(), key=lambda kv: -abs(kv[1][0])):
        who = " and ".join(_source(world, x) for x in h[1])
        if key.startswith("b:"):
            thing, season = key[2:].split("@")
            heard.append(f"{who} said leaving {thing} somewhere in {SEASONS[int(season)]} is worth it (not tried yet)")
        elif key.startswith("g:"):
            heard.append(f"{who} said there were animals at {key[2:]} (not checked yet)")
        elif key.startswith("w:"):
            heard.append(f"{who} said there is water at {key[2:]} (not checked yet)")
        else:
            heard.append(f"{who} said {_thing(world, key[2:])} is worth making (not tried yet)")
    words = []
    for src, (hd, fl) in sorted(p.records.items(), key=lambda kv: -(kv[1][0] + kv[1][1]))[:6]:
        n = hd + fl
        est = (hd + 1.0) / (n + 2.0)
        verdict = "usually right" if est >= 0.7 else "often wrong" if est <= 0.4 else "sometimes right"
        words.append(f"{_source(world, src)}: {verdict} ({hd:.0f} held, {fl:.0f} failed in what they know of)")
    from .marks import meaning
    known = []
    for shape, (seen, _) in sorted(p.marks.items(), key=lambda kv: -kv[1][0])[:6]:
        means = meaning(p, shape)
        if means:
            top = sorted(means.items(), key=lambda kv: -kv[1])[:2]
            words = ", ".join(_name(world, k[2:]) if k.startswith("p:") else k for k, _ in top)
            known.append({"shape": shape, "seen": seen, "goes_with": words})
        else:
            known.append({"shape": shape, "seen": seen, "goes_with": ""})
    return {
        "state": state, "weeks": p.focus_weeks if state else 0,
        "thoughts": thoughts, "weighed": weighed, "puzzles": puzzles, "heard": heard, "marks": known,
        "records": words,
        "feelings": {"mood": round(p.mood, 2), "fear": round(p.fear, 2), "anger": round(p.anger, 2),
                     "grief": round(p.grief, 2), "loneliness": round(p.loneliness, 2),
                     "thirst": round(p.thirst, 2)},
        "age": round(p.years(tick), 1),
    }


def headline(world, p) -> str:
    """The one thing on their mind, short enough to float over their head."""
    if not p.thoughts:
        return ""
    k, a, _ = p.thoughts[0]
    return thought_words(world, p, k, a)
