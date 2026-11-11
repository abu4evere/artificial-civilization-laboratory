"""Turning a week of the simulation into something you can watch.

The simulation decides once a week: each person picks one thing to do. To show
that as life, the page plays the week out day by day: people walk out in the
morning, do their work, meet whoever they meant to meet, come home at dusk and
sleep. This module tells the page what really happened that week and when to
show it:

- where everyone set out from, and where and toward whom they were headed;
- what was really said: news passed on, a skill taught, thanks for food, a
  courtship, a cry of "thief";
- the moments: hunts, fights, births, deaths, fires, harvests.

Each moment gets a day and a time of day, worked out from its event number, so
everyone watching sees the same week. Nothing here feeds back into the world.

The words in the speech bubbles are our rendering of what passed between
people, as English sentences. Small talk ("chat") fills the time between
conversations that carried real news or knowledge ("say"); it is drawn
differently on the page so the two are never confused.
"""
from __future__ import annotations

from . import fauna, mindview, thought
from .config import CHILD_END, INFANT_END, SEASONS
from .historian import CLASSES, classify, describe
from .matter import pile_warmth

STAGES = ("infant", "child", "teen", "adult", "elder")


def when(eid: int, lo: float = 0.22, hi: float = 0.62) -> tuple[int, float]:
    """The day of the week (0-6) and time of day (0-1) to show an event, fixed by its number."""
    h = (eid * 2654435761) & 0xFFFFFFFF
    return (h >> 8) % 7, round(lo + (h % 1000) / 1000.0 * (hi - lo), 3)


def people_rows(world, line_of) -> list:
    tick = world.tick
    rows = []
    for p in world.living():
        a = p.age(tick)
        stage = 0 if a < INFANT_END else 1 if a < CHILD_END else STAGES.index(p.stage(tick))
        doing = p.doing or ("" if a < INFANT_END else "rest")
        frm, aim = world.plan.get(p.id, (p.loc, ""))
        things = []
        for it in p.items:
            for c in classify(it):
                if c not in things:
                    things.append(c)
        rows.append([
            p.id, p.name, p.loc[0], p.loc[1], frm[0], frm[1], p.sex, stage, doing, aim,
            line_of(p), p.caregiver or "", ",".join(things), round(p.mood, 2),
            1 if p.sick else 0, 1 if p.starving else 0, 1 if p.grief > 0.3 else 0,
            1 if p.pregnant is not None else 0, round(p.health), p.partner or "", round(p.years(tick), 1),
            mindview.headline(world, p) if a >= INFANT_END else "", thought.state(p),
        ])
    return rows


def mark_rows(world) -> list:
    """Every mark on the land: [x, y, shape, depth, surface]."""
    return [[t.x, t.y, m[0], m[3], m[4]] for row in world.tiles for t in row for m in t.marks]


def sky(world) -> dict:
    """This week's weather, as it really is."""
    return {"rain": world.sky.get("rain", 0), "storm": world.sky.get("storm"), "flood": world.sky.get("flood", 0),
            "wet": world.sky.get("wet", 1.0), "hard": world.sky.get("hard", 0.0)}


def animal_rows(world) -> list:
    """One row per living animal group: [species, x, y, count], so the page can draw each kind."""
    return [[g["sp"], g["x"], g["y"], g["n"]] for g in world.animals if g["n"] > 0]


def tile_rows(world) -> list:
    c = world.cfg
    rows = []
    for row in world.tiles:
        for t in row:
            warmth = pile_warmth(t.pile) if t.pile else 0.0
            size = sum(t.pile.values()) if t.pile else 0.0
            pile = t.pile or {}
            rows.append([
                round(9 * t.plants / max(1.0, c.plant_cap * t.fertility)),
                min(3, int(t.crop // 8)),
                round(10 * warmth),
                min(3, int(size // 5)) if size >= 1 else 0,
                1 if t.fire > 0 else 0,
                1 if t.stash else 0,
                round(3 * t.wood / max(1.0, c.wood_cap)),
                round(3 * t.stone / max(1.0, c.stone_cap)),
                min(4, int(sum(g["n"] for g in world.herds.get((t.x, t.y), ())) / 4)),
                round(3 * t.fiber / max(1.0, c.fiber_cap)),
                min(3, int(pile.get("wood", 0) // 4)),
                min(3, int((pile.get("stone", 0) + pile.get("bone", 0)) // 4)),
                min(3, int((pile.get("hide", 0) + pile.get("fiber", 0)) // 3)),
            ])
    return rows


def _name(world, pid) -> str:
    q = world.people.get(pid) if pid else None
    return q.name if q else "someone"


_NEWS = {
    "killed": "{a} killed {b}!",
    "attacked": "{a} attacked {b}.",
    "stole": "{a} stole from {b}.",
    "died": "{b} is dead.",
    "born": "{b} was born!",
    "gave": "{a} shared food with {b}.",
    "paired": "{a} and {b} are together now.",
    "discovered": "{a} found something new.",
    "mauled": "{a} went for {b}!",
    "storm": "That storm! I thought it would never end.",
    "flood": "The river came up over everything.",
}

_MADE = {
    "blade": "Sharp!",
    "spear": "Look: a long point!",
    "club": "Heavy. Good.",
    "carrier": "This holds things.",
    "wrap": "So warm.",
    "boat": "It floats!",
}


def _told(world, kind, of, to, speaker, listener) -> str:
    """A story as the teller would put it: "I" for themselves, "you" for the listener."""
    def who(pid, subject):
        if pid and pid.startswith("animal:"):
            return {"animal:wolf": "wolves", "animal:bear": "a bear"}.get(pid, "an animal")
        if pid == speaker:
            return "I" if subject else "me"
        if pid == listener:
            return "you"
        return _name(world, pid)
    if kind == "paired" and speaker in (of, to):
        other = to if of == speaker else of
        return f"{who(other, True)} and I are together now."
    if kind == "paired" and listener in (of, to):
        return "So you two are together now!"
    template = _NEWS.get(kind)
    if template is None:
        return "Did you hear what happened?"
    text = template.format(a=who(of, True), b=who(to, False))
    text = text.replace("I is", "I am").replace("you is", "you are")
    news = speaker not in (of, to) and listener not in (of, to)
    return ("Did you hear? " if news else "") + text[:1].upper() + text[1:]


def _imperative(text: str) -> str:
    for past, now in (("struck", "strike"), ("tied", "tie"), ("pressed", "press"), ("held", "hold")):
        if text.startswith(past):
            return now + text[len(past):]
    return text


def _belief_said(key: str) -> str:
    thing, season = key.split("@")
    when_ = SEASONS[int(season)]
    if "/" in thing:
        a, b = thing.split("/")
        return f"In {when_}, strike {a} with {b} at home."
    if thing == "seeds":
        return f"Leave seeds in the ground in {when_}. They come back as food."
    if thing == "food":
        return f"Leave food somewhere in {when_}, and come back for it."
    return f"Heap up {thing} in {when_}. It keeps the cold out."


def _small_talk(world, p, q, eid: int) -> str:
    """Ordinary talk, from how the speaker is and what is around them."""
    if p.starving:
        return "I'm so hungry."
    if p.grief > 0.3:
        return "I keep thinking of the ones we lost."
    if q.id in p.children and q.age(world.tick) < CHILD_END:
        return "Stay close to me."
    if p.partner == q.id:
        return "❤"
    season = world.season
    tile = world.tile(p.loc)
    choices = ["Good to see you.", "Where have you been?", "Ha! Look at that."]
    if season == 3:
        choices += ["So cold today."] + (["Come closer to the fire."] if tile.fire > 0 else [])
    elif season == 0:
        choices += ["Everything is growing again."]
    elif season == 1:
        choices += ["Good berries this year." if world.weather > 1.0 else "Food is thin this year."]
    else:
        choices += ["The cold is coming."]
    if fauna.prey_here(world, p.loc) >= 2:
        choices.append("I saw deer this morning.")
    return choices[eid % len(choices)]


def script(world, events: list, line_of, historian=None) -> dict:
    """What happened this week, as moments to show: who says what to whom, hunts, births, deaths."""
    w = world
    says = []        # [kind, a, b, text, day, f]   kind: say | chat | think
    moments = []     # [kind, a, b, x, y, day, f]  kind: fight | kill | birth | death | fire | harvest | made | gift
    hunts = []       # [x, y, [ids], success, day, f]
    dead = []        # [id, name, x, y, sex, stage, line, cause, day, f]
    had_words = []
    kill_time = {}
    for e in events:
        k = e["k"]
        a, b = e.get("a"), e.get("b")
        eid = e["id"]
        day, f = when(eid)
        at = e.get("at")
        if k == "told":
            says.append(["say", a, b, _told(w, e.get("about"), e.get("of"), e.get("to"), a, b), day, f])
            heard = e.get("heard")
            if heard == "rejected":
                reply = "That's not what happened. I was there."
            elif heard == "doubted":
                reply = ["I don't believe that.", "Are you sure?", "Hm. Who told you that?"][eid % 3]
            else:
                reply = _reaction(w, w.people.get(b), e.get("about"), e.get("of"), e.get("to"), a)
            if reply:
                says.append(["chat", b, a, reply, day, round(f + 0.03, 3)])
            had_words.append((a, b))
        elif k == "puzzled" and a:
            p_ = w.people.get(a)
            if p_ is not None:
                says.append(["think", a, "", "Huh? " + mindview.puzzle_words(w, p_, e.get("about", "")) + "...", day, f])
        elif k in ("verified", "refuted") and a:
            who = _name(w, (e.get("by") or [None])[0])
            says.append(["think", a, "", f"{who} was right." if k == "verified" else f"{who} was wrong about that.",
                         day, f])
        elif k == "vouched" and a and b:
            src = e.get("about", "")
            who = f"the mark <{src[5:]}>" if src.startswith("mark:") else _name(w, src)
            says.append(["chat", a, b, f"You can believe {who}." if e.get("good") else f"Don't believe {who}.", day, f])
        elif k == "read" and a:
            says.append(["think", a, "", f"<{e.get('shape')}>... that means something here.", day, f])
        elif k == "crossed" and a:
            says.append(["say", a, "", "Land! We made it across.", day, f])
        elif k == "drank_sea" and a:
            says.append(["say", a, "", "Bitter! This water burns my throat.", day, f])
        elif k == "mark" and a:
            says.append(["think", a, "", f"<{e.get('shape')}>", day, f])
            moments.append(["mark", a, e.get("shape", ""), at[0], at[1], day, f])
        elif k in ("storm", "flood"):
            x, y = (at or [0, 0])
            moments.append([k, "", "", x, y, day, f])
        elif k == "learn":
            if e.get("how") == "taught" and e.get("thing"):
                recipe = w.knowledge.get(e["thing"], {}).get("recipe")
                if recipe:
                    says.append(["say", b, a, "Watch: " + _imperative(describe(recipe, w)) + ".", day, f])
                    says.append(["chat", a, b, "Show me again.", day, round(f + 0.03, 3)])
                    had_words.append((b, a))
            elif e.get("how") == "told" and e.get("belief"):
                says.append(["say", b, a, _belief_said(e["belief"]), day, f])
                had_words.append((b, a))
            elif e.get("how") == "copied" and a:
                says.append(["think", a, b, "I could make one of those.", day, f])
        elif k == "give" and a and b:
            says.append(["chat", a, b, "Here, eat.", day, f])
            says.append(["chat", b, a, "I won't forget this." if not e.get("returned") else "Now we're even.",
                         day, round(f + 0.03, 3)])
            moments.append(["gift", a, b, 0, 0, day, f])
            had_words.append((a, b))
        elif k == "care" and a and b:
            says.append(["chat", a, b, "Rest. I'm here.", day, f])
            q = w.people.get(b)
            says.append(["chat", b, a, "It hurts less with you here." if q is not None and q.sick else "Thank you.",
                         day, round(f + 0.03, 3)])
        elif k == "pair" and a and b:
            says.append(["say", a, b, "Stay with me?", day, f])
            says.append(["say", b, a, "Yes.", day, round(f + 0.03, 3)])
        elif k == "steal" and a and b and e.get("noticed"):
            says.append(["say", b, a, "Hey! Thief!", day, f])
            moments.append(["theft", a, b, 0, 0, day, f])
        elif k in ("attack", "kill") and a and b:
            revenge = _was_revenge(historian, eid) if historian else False
            says.append(["say", a, b, "This is for what you did!" if revenge else "Get away from me!", day, f])
            says.append(["say", b, a, "Help!", day, round(f + 0.02, 3)])
            moments.append(["kill" if k == "kill" else "fight", a, b, at[0], at[1], day, f])
            if k == "kill":
                kill_time[b] = (day, f)
        elif k == "birth" and a and b:
            moments.append(["birth", a, b, at[0], at[1], day, f])
            says.append(["say", a, b, "👶", day, f])
        elif k == "fire" and at:
            moments.append(["fire", a or "", "", at[0], at[1], day, f])
            if a:
                says.append(["say", a, "", "Fire! It caught!", day, f])
        elif k == "harvest" and a:
            says.append(["say", a, "", "Food grew where the seeds fell!", day, f])
        elif k == "put" and a and e.get("into") == "fire":
            says.append(["chat", a, "", "Keep it burning.", day, f])
        elif k in ("make", "play") and a and e.get("thing"):
            for c in classify(e):
                says.append(["say", a, "", _MADE[c], day, f])
                moments.append(["made", a, c, 0, 0, day, f])
                break
        elif k == "hunt":
            party = e.get("party", [])
            hunts.append([at[0], at[1], party, 1 if e.get("success") else 0, day, f])
            if party:
                says.append(["chat", party[0], "", "We got one!" if e.get("success") else "It got away...",
                             day, round(f + 0.02, 3)])
        elif k == "taken_in" and e.get("by") == "adoption" and a and b:
            says.append(["say", a, b, "Come. You'll live with me now.", day, f])
        elif k == "death" and a:
            p = w.people[a]
            day_, f_ = kill_time.get(a, (day, f))
            dead.append([a, p.name, at[0], at[1], p.sex,
                         STAGES.index(p.stage(p.death_tick)) if p.death_tick is not None else 3,
                         line_of(p), e.get("cause"), day_, f_])
            moments.append(["death", a, e.get("b") or "", at[0], at[1], day_, f_])
    for e in events:
        if e["k"] == "talk" and (e["a"], e["b"]) not in had_words:
            p, q = w.people[e["a"]], w.people[e["b"]]
            day, f = when(e["id"])
            says.append(["chat", p.id, q.id, _small_talk(w, p, q, e["id"]), day, f])
            says.append(["chat", q.id, p.id, _reply(w, q, p, e["id"]), day, round(f + 0.03, 3)])
    return {"says": says, "moments": moments, "hunts": hunts, "dead": dead,
            "talks": _dialogues(w, says), "evening": _evenings(w)}


# --- whole conversations ---------------------------------------------------------------------

def _close(world, q, pid) -> bool:
    if q is None or not pid:
        return False
    if pid == q.partner or pid in (q.mother, q.father) or pid in q.children:
        return True
    r = q.rel.get(pid)
    return r is not None and r.affection > 0.3


def _reaction(world, q, kind, of, to, speaker):
    """How the listener answers a piece of news, from what they feel about the people in it."""
    if q is None:
        return None

    def n(pid):
        return "you" if pid == speaker else _name(world, pid)

    if q.id in (of, to):
        return {"gave": "You'd have done the same for me." if q.id == of else "I won't forget it.",
                "paired": "Yes, we are."}.get(kind, "I know. I was there.")
    if kind == "killed":
        return f"No... not {n(to)}!" if _close(world, q, to) else f"We have to watch out for {n(of)}."
    if kind == "attacked":
        return f"Is {n(to)} hurt?" if _close(world, q, to) else f"{n(of)} has a temper."
    if kind == "stole":
        return f"{n(of)} can't be trusted."
    if kind == "died":
        return f"I'll miss {n(to)}." if _close(world, q, to) else "That's sad news."
    if kind == "born":
        return "A new little one! Wonderful."
    if kind == "gave":
        return f"{n(of)} has a good heart."
    if kind == "paired":
        return "I'm happy for you!" if speaker in (of, to) else "Good for them."
    return "Really?"


def _reply(world, q, p, eid: int) -> str:
    """An everyday answer, from how the listener is."""
    if q.starving:
        return "Me too. I'm hungry."
    if q.grief > 0.3:
        return "I keep thinking of them too."
    if q.partner == p.id:
        return "❤"
    if p.id in (q.mother, q.father):
        return "I will."
    choices = ["Good to see you too.", "Here and there.", "Ha!", "Mm."]
    if world.season == 3:
        choices.append("Stay close to the fire.")
    return choices[(eid >> 3) % len(choices)]


def _dialogues(world, says) -> list:
    """Everyone who spent the week with someone, and what passed between them, in order."""
    pairs: dict = {}
    for pid, (_, aim) in world.plan.items():
        p = world.people.get(pid)
        q = world.people.get(aim) if aim else None
        if p is None or q is None or not p.alive or not q.alive:
            continue
        if p.doing not in ("talk", "court", "care", "give"):
            continue
        key = tuple(sorted((pid, aim)))
        if key not in pairs:
            pairs[key] = {"a": pid, "b": aim, "lines": []}
            if p.doing == "court" and p.partner != aim:
                r = q.rel.get(pid)
                aff = r.affection if r else 0.0
                answer = "I'd like that." if aff > 0.3 else "Maybe." if aff > 0 else "Not today."
                pairs[key]["lines"] += [[pid, "Walk with me?", "chat"], [aim, answer, "chat"]]
    for kind, a, b, text, day, f in sorted(says, key=lambda s: (s[4], s[5])):
        key = tuple(sorted((a, b))) if b else None
        if key in pairs and kind != "think":
            pairs[key]["lines"].append([a, text, kind])
    out = []
    for d in pairs.values():
        lines = d["lines"]
        if len(lines) < 2:
            p, q = world.people[d["a"]], world.people[d["b"]]
            eid = len(out) + world.tick
            lines += [[p.id, _small_talk(world, p, q, eid), "chat"], [q.id, _reply(world, q, p, eid), "chat"]]
        out.append([d["a"], d["b"], lines[:6]])
    return out


def _evenings(world) -> list:
    """By the fire at night: couples talk over the day, and parents tell the young what they remember."""
    tick, out = world.tick, []
    for p in world.living():
        if p.stage(tick) not in ("teen", "adult", "elder"):
            continue
        if p.partner and p.partner > p.id:
            q = world.people[p.partner]
            if q.alive and max(abs(p.loc[0] - q.loc[0]), abs(p.loc[1] - q.loc[1])) <= world.cfg.camp_radius:
                out.append([p.id, q.id, _couple_talk(world, p, q)])
        for cid in p.children + p.wards:
            c = world.people[cid]
            if c.alive and c.caregiver == p.id and c.age(tick) >= 3 * 52 and c.loc == p.loc:
                story = _story(world, p, c)
                if story:
                    out.append([p.id, c.id, [[p.id, story, "say"], [c.id, "Tell me another!", "chat"]]])
                break
    return out


def _couple_talk(world, p, q) -> list:
    if p.starving or q.starving:
        hungry, other = (p, q) if p.starving else (q, p)
        return [[hungry.id, "We need more food.", "chat"], [other.id, "I'll go out early tomorrow.", "chat"]]
    if p.sick or q.sick:
        sick, other = (p, q) if p.sick else (q, p)
        return [[sick.id, "I feel so weak.", "chat"], [other.id, "Rest. I'm here.", "chat"]]
    if p.grief > 0.3 or q.grief > 0.3:
        sad, other = (p, q) if p.grief > 0.3 else (q, p)
        return [[sad.id, "I can't stop thinking about them.", "chat"], [other.id, "I know. Me too.", "chat"]]
    if p.pregnant is not None or q.pregnant is not None:
        mother, other = (p, q) if p.pregnant is not None else (q, p)
        return [[mother.id, "The baby moved today!", "chat"], [other.id, "❤", "chat"]]
    if world.season == 3:
        return [[p.id, "So cold tonight.", "chat"], [q.id, "Come closer.", "chat"]]
    return [[p.id, "Good night.", "chat"], [q.id, "Sleep well.", "chat"]]


def _story(world, teller, child):
    """A story from the teller's own memory: this is how old events reach the young."""
    worth = ("killed", "attacked", "stole", "died", "born", "paired", "gave", "discovered")
    best = None
    for m in teller.memories:
        if m.kind in worth and (best is None or m.salience * m.strength > best.salience * best.strength):
            best = m
    if best is None:
        return None

    def n(pid):
        return "I" if pid == teller.id else "you" if pid == child.id else _name(world, pid)

    def o(pid):
        return "me" if pid == teller.id else "you" if pid == child.id else _name(world, pid)

    k, a, b = best.kind, best.actor, best.target
    text = {
        "killed": f"Long ago, {n(a)} killed {o(b)}. Never forget it.",
        "attacked": f"{n(a)} once attacked {o(b)}. Be careful of {o(a)}.",
        "stole": f"{n(a)} once stole from {o(b)}. Don't trust {o(a)}.",
        "died": f"I remember when {n(b)} died. I still miss them.",
        "born": "I remember the day you were born!" if b == child.id else f"I remember when {n(b)} was born.",
        "paired": f"I remember when {n(a)} and {o(b)} first came together.",
        "gave": f"{n(a)} once shared food with {o(b)} when it was needed. Remember that.",
        "discovered": "I once found a new way to make things. Let me show you one day.",
    }[k]
    return text[:1].upper() + text[1:]


def _was_revenge(historian, eid: int) -> bool:
    """The historian has already judged whether this harm paid back an earlier one."""
    for h in reversed(historian.harms[-50:]):
        if h[5] == eid:
            return h[4] > 0
    return False
