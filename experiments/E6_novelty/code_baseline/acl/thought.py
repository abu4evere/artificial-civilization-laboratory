"""What is on a person's mind, and what that does to them.

Every week, many things compete for a person's attention: hunger, thirst, cold,
a child who looks thin, someone they love who is far away, a grudge, a fear, a
loss, a memory that will not go away, curiosity about the stones in their hand,
something that surprised them and still does not make sense, loneliness, the
wish for a partner. Each pull has a strength, set by their body,
their feelings, what has happened to them, and their temperament. The
strongest wins their attention for the week.

Attention matters:

- **It steers what they do.** Whatever is on their mind makes the related
  choices more attractive. Someone thinking about a child goes to the child;
  someone gripped by fear stays close to others.
- **It has inertia.** Whatever held their attention last week pulls a little
  harder this week. Diligent people stay with a task; anxious people stay
  with a worry.
- **Staying with a goal is focus.** After a few weeks on the same goal (food,
  making things), they get better at it faster and feel a quiet satisfaction.
- **Staying with pain is overthinking.** After a few weeks on the same loss,
  fear or grudge, they are distracted, slower at their work, and sadder. Going
  over a memory again and again also keeps it sharp, so painful things are
  remembered longer.

Nobody is told to be focused or anxious. Both happen, or not, because of who
someone is and what they have lived through. "Focused" and "overthinking" are
only our names for what we see.
"""
from __future__ import annotations

from . import weather
from .config import WEEKS_PER_YEAR
from .util import clamp, distance

NEGATIVE = ("grief", "memory", "fear", "grudge", "dread")
GOALS = ("curiosity", "craft", "puzzle")   # chasing food for years is survival, not focus
STREAK = 3   # weeks of the same thing on one's mind before it becomes focus or overthinking

# Which choices a thought makes more attractive, and how much.
PULLS = {
    "hunger": {"forage": 0.25, "hunt": 0.25, "take": 0.2},
    "thirst": {"join": 0.3, "explore": 0.15},
    "cold": {"join": 0.2, "put": 0.2, "make": 0.15},
    "tired": {"rest": 0.3},
    "sick": {"rest": 0.35},
    "grief": {"rest": 0.15, "talk": 0.15, "join": 0.1},
    "memory": {"rest": 0.1, "talk": 0.15},
    "grudge": {"attack": 0.3, "talk": 0.1},
    "fear": {"flee": 0.3, "join": 0.15, "hunt": -0.2},
    "dread": {"join": 0.15, "hunt": -0.25, "explore": -0.2},
    "love": {"talk": 0.25, "give": 0.2, "care": 0.2, "court": 0.15, "join": 0.2},
    "missing": {"join": 0.35, "talk": 0.2},
    "worry": {"give": 0.25, "care": 0.3, "forage": 0.15},
    "curiosity": {"play": 0.25, "gather": 0.2, "make": 0.2, "explore": 0.1},
    "craft": {"make": 0.3, "gather": 0.15},
    "mate": {"court": 0.25, "explore": 0.1, "join": 0.1},
    "lonely": {"talk": 0.25, "join": 0.2},
    "puzzle": {"play": 0.15, "make": 0.1, "gather": 0.1},
    "shore": {"explore": 0.3, "gather": 0.05, "play": 0.05},
}


def candidates(world, p, hunger: float, fatigue: float) -> list:
    """Everything pulling at p's attention this week: [(key, kind, about, strength)]."""
    c = world.cfg
    tick = world.tick
    g = p.genes
    out = []

    def add(kind, about, strength):
        if strength > 0.05:
            out.append((f"{kind}:{about or ''}", kind, about, strength))

    add("hunger", None, 1.1 * hunger)
    add("thirst", None, 1.2 * p.thirst)
    cold = weather.coldness(world, p.loc)
    if cold > 0.1:
        add("cold", None, 0.7 * min(cold, 1.0) * (1.0 - p.expect.get("warm", 1.0)))
    add("tired", None, 0.9 * fatigue * fatigue)
    if p.sick or p.health < 50:
        add("sick", None, 0.5 + 0.5 * (1.0 - p.health / 100.0) if p.sick else 0.6 * (1.0 - p.health / 100.0))

    # Feelings toward particular people.
    best_grudge, best_fear, best_love = (None, 0.0), (None, 0.0), (None, 0.0)
    family = [x for x in (p.partner, p.mother, p.father) if x] + list(p.children)
    for pid, r in p.rel.items():
        q = world.people.get(pid)
        if q is None or not q.alive:
            continue
        gr = r.grudge * (0.5 + g["temper"])
        if gr > best_grudge[1]:
            best_grudge = (pid, gr)
        fe = max(0.0, -r.trust - 0.3) * (0.5 + g["anxiety"])
        if fe > best_fear[1]:
            best_fear = (pid, fe)
        if pid in family or r.affection > 0.5:
            lv = max(r.affection, 0.0)
            if lv > best_love[1]:
                best_love = (pid, lv)
    add("grudge", best_grudge[0], best_grudge[1])
    add("fear", best_fear[0], best_fear[1])
    if best_love[0]:
        q = world.people[best_love[0]]
        apart = distance(p.loc, q.loc, c.width, c.height) > c.reach
        add("missing" if apart else "love", q.id, best_love[1] * (0.8 if apart else 0.35) * (0.6 + 0.6 * g["sociability"]))

    # Fear of animals, learned from being hurt or from stories.
    worst, worst_v = None, 0.0
    for key, v in p.expect.items():
        if key.startswith("fear:") and v > worst_v:
            worst, worst_v = key[5:], v
    if worst:
        add("dread", worst, worst_v * (0.5 + g["anxiety"]))

    # Loss, and memories that will not let go.
    if p.grief > 0.1:
        lost = None
        for m in sorted(p.memories, key=lambda m: -(m.salience * m.strength)):
            if m.kind in ("died", "killed") and m.target and m.target != p.id:
                lost = m.target
                break
        add("grief", lost, 1.1 * p.grief)
    worst_m, worst_mv = None, 0.0
    for m in p.memories:
        if m.valence >= -0.3:
            continue
        years = (tick - m.tick) / WEEKS_PER_YEAR
        v = m.salience * m.strength * (0.3 + 0.9 * g["anxiety"]) / (1.0 + years)
        if v > worst_mv:
            worst_m, worst_mv = m.eid, v
    add("memory", worst_m, worst_mv)

    # The young in one's care.
    for d in world.dependents(p.id):
        need = d.need(c, tick)
        h = clamp(1.0 - d.edible() / (2.0 * need)) + (0.4 if d.starving or d.sick else 0.0)
        add("worry", d.id, h * (0.4 + 0.8 * g["care"]))

    # Curiosity, and the pull of things one knows how to make.
    stuff = sum(1 for v in p.mats.values() if v >= 1.0) + len(p.items)
    add("curiosity", None, g["curiosity"] * (1.0 - hunger) * (0.35 + 0.1 * min(stuff, 3)))
    best_sig = max(p.itemval.items(), key=lambda kv: kv[1], default=(None, 0.0))
    if best_sig[0] and best_sig[1] > 0.1:
        add("craft", best_sig[0], best_sig[1] * (0.4 + 0.6 * g["diligence"]) * (1.0 - hunger))

    # Things that turned out differently from what they expected. Hunger crowds them out.
    for key, pz in sorted(p.puzzles.items()):
        add("puzzle", key, pz[0] * (0.4 + 0.9 * g["curiosity"]) * (1.0 - 0.8 * hunger))

    # Land seen across the water, out of reach on foot.
    if p.shores:
        x, y = p.shores[-1]
        add("shore", f"{x},{y}", (0.2 + (0.3 if p.voyage else 0.0)) * g["curiosity"] * (1.0 - hunger)
            * (1.5 if world.boat(p) >= 0.65 else 1.0))

    # Wanting a partner, wanting company.
    if p.stage(tick) == "adult" and p.partner is None and p.years(tick) < 45:
        add("mate", None, 0.45 * (0.5 + g["sociability"]))
    add("lonely", None, p.loneliness * g["sociability"] * 0.9)
    return out


def attend(world, p, hunger: float, fatigue: float) -> list:
    """Choose what holds p's attention this week. Returns the leading thoughts, strongest first."""
    g = p.genes
    pulls = []
    for key, kind, about, strength in candidates(world, p, hunger, fatigue):
        if key == p.focus:
            # Whatever held the mind last week holds on: diligence keeps a task, anxiety keeps a worry.
            strength += 0.12 + (0.25 * g["anxiety"] if kind in NEGATIVE else 0.3 * g["diligence"])
        pulls.append((strength, key, kind, about))
    pulls.sort(key=lambda x: (-x[0], x[1]))
    if not pulls:
        p.focus, p.focus_weeks = "", 0
        p.thoughts = []
        return []
    top = pulls[0]
    if top[1] == p.focus:
        p.focus_weeks += 1
    else:
        p.focus, p.focus_weeks = top[1], 1
    p.thoughts = [[kind, about or "", round(s, 2)] for s, _, kind, about in pulls[:4]]
    return p.thoughts


def steer(p, options: list) -> list:
    """Whatever is on p's mind makes the related choices more attractive."""
    if not p.thoughts:
        return options
    kind, about, strength = p.thoughts[0]
    pulls = PULLS.get(kind, {})
    out = []
    for score, action, target in options:
        bonus = pulls.get(action, 0.0) * min(strength, 1.5)
        # Thoughts about a particular person pull toward that person.
        if about and target == about and action in ("talk", "give", "care", "court", "attack", "join"):
            bonus += 0.2 * min(strength, 1.5)
        # A puzzle pulls toward trying that very thing again.
        if kind == "puzzle" and about:
            if action == "make" and about[2:] == target and about[:2] in ("m:", "f:"):
                bonus += 0.35 * min(strength, 1.5)
            elif action == "put" and about.startswith(f"b:{target}@"):
                bonus += 0.35 * min(strength, 1.5)
            elif action == "play" and about.startswith("k:"):
                bonus += 0.2 * min(strength, 1.5)
        out.append((score + bonus, action, target))
    return out


def state(p) -> str:
    """'focused', 'overthinking' or '' from how long the same thing has held p's mind."""
    if not p.focus or p.focus_weeks < STREAK:
        return ""
    kind = p.focus.split(":")[0]
    if kind in NEGATIVE:
        return "overthinking"
    if kind in GOALS:
        return "focused"
    return ""
