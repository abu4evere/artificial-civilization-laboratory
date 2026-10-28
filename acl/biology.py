"""The body and the life cycle: eating, cold, sickness, ageing, birth and death,
plus how feelings fade and what people learn at the end of each week.

Parents feed their young before themselves, how far they go set by the
inherited `care` trait. Love for a newborn is built in. Grief, anger and fear
fade, each at its own speed.

Cold is physics: being exposed when it is cold hurts. How cold it is depends
on the place, the season and the year (see weather.py). A fire on the same
tile keeps some of it off, and so does a heap of set-down things that encloses
and covers, for as many people as it has room for. So does wearing something
warm. None of these is a "house" or "clothing" to the people. They only notice
that some cold weeks, in some places, with some things, hurt less.

Bodies need water as well as food. A week without it hurts badly.
"""
from __future__ import annotations

import copy
import math

from . import inquiry, knowhow, matter, thought, weather
from .config import CHILD_END, INFANT_END, WEEKS_PER_YEAR
from .matter import best_item, pile_room, pile_shape, pile_warmth, worn_warmth
from .mind import context_index
from .person import A, GENES, N_ACTIONS, Person, Relation
from .social import remember, react
from .util import clamp, distance, make_name


def body_phase(world) -> None:
    c = world.cfg
    tick = world.tick
    rng = world.rng
    living = list(world.living())
    cold_at = {}
    for p in living:
        if p.loc not in cold_at:
            cold_at[p.loc] = weather.coldness(world, p.loc)

    # Loose food rots, slower in smoke, and slower if it has been in a fire; seeds keep.
    for p in living:
        rate = c.spoil_rate * (c.smoke_keep if world.tile(p.loc).fire > 0 else 1.0)
        kept = min(p.kept, p.food)
        p.food = (p.food - kept) * (1.0 - rate) + kept * (1.0 - rate * c.kept_keep)
        p.kept = kept * (1.0 - rate * c.kept_keep)
        p.seeds -= p.seeds * c.seed_spoil
        _wet_and_dry(world, p)

    # HF4 logging copy: a ledger outside the world's state (set by the runner); nothing below reads it.
    ledger = getattr(world, "ledger", None)
    fed_out = {}
    # Parents feed the young first, as far as their nature takes them.
    for p in living:
        deps = world.dependents(p.id)
        if not deps:
            continue
        own = p.need(c, tick)
        wants = [max(0.0, d.need(c, tick) - d.edible()) for d in deps]
        total = sum(wants)
        if total <= 0:
            continue
        if p.edible() >= own + total:
            portion = 1.0
        else:
            dep_weight = total * (0.4 + 1.2 * p.genes["care"])
            portion = min(1.0, p.edible() * dep_weight / (dep_weight + own) / total)
        for d, want in zip(deps, wants):
            amount = min(want * portion, p.edible())
            from_food = min(p.food, amount)
            p.food -= from_food
            p.seeds -= amount - from_food
            d.food += amount
            fed_out[p.id] = fed_out.get(p.id, 0.0) + amount
        p.contact = True
        for d in deps:
            d.contact = True

    # Who is out of the wind tonight: a heap with room shelters those who built it first.
    inside = _who_is_inside(world, [p for p in living if cold_at[p.loc] > 0])

    crowd = {loc: len(ids) for loc, ids in world.occ.items()}
    felt_warmth: dict = {}
    dying = []
    for p in living:
        st = p.stage(tick)
        tile = world.tile(p.loc)
        fire = tile.fire > 0
        need = p.need(c, tick) * (1.0 - c.heated_food_saving if fire else 1.0)
        held_before = p.food + p.seeds
        p.kept = min(p.kept, p.food)
        # Food that has been in a fire goes further, wherever it is eaten.
        from_kept = 0.0 if fire else min(p.kept, need * (1.0 - c.heated_food_saving))
        covered = from_kept / (1.0 - c.heated_food_saving)
        eat_food = from_kept + min(p.food - from_kept, need - covered)
        p.food -= eat_food
        p.kept = min(p.kept - from_kept, p.food)
        eat_seeds = min(p.seeds, need - covered - (eat_food - from_kept))
        p.seeds -= eat_seeds
        deficit = 1.0 - (covered + eat_food - from_kept + eat_seeds) / need
        if ledger is not None:
            ledger.append((p.id, p.age(tick) >= 16 * WEEKS_PER_YEAR, need, held_before, deficit, fed_out.get(p.id, 0.0)))
        if from_kept > 0 and st != "infant":
            # It filled them more than raw food would have: that is something they can feel.
            felt = min(1.0, (covered - from_kept) / (0.15 * need))
            before = p.expect.get("heat:food", 0.0)
            p.expect["heat:food"] = round(before + 0.2 * (felt - before), 3)
        if deficit > 0.05:
            p.health -= c.starvation_damage * deficit
            p.starving += 1
            p.hurt_by = "starvation"
        else:
            p.starving = 0
            if not p.sick:
                p.health += c.fed_recovery

        # Water. Infants drink at the breast; everyone else finds their own.
        if st != "infant":
            p.thirst = weather.drink(world, p)
            p.expect["dry"] = round(p.expect.get("dry", 0.0) + 0.1 * (p.thirst - p.expect.get("dry", 0.0)), 3)
            # E9 (A2): what going short of food in this season has been like, learned the way thirst is.
            short_key = f"short@{world.season}"
            p.expect[short_key] = round(p.expect.get(short_key, 0.0)
                                        + 0.1 * ((1.0 if p.starving else 0.0) - p.expect.get(short_key, 0.0)), 3)
            if p.thirst > 0.05:
                p.health -= c.thirst_damage * p.thirst
                p.hurt_by = "thirst"

        frail = st in ("infant", "elder")
        cold = cold_at[p.loc]
        if cold > 0:
            place_warm = 1.0 - (1.0 - inside.get(p.id, 0.0)) * (1.0 - (c.fire_warmth if fire else 0.0))
            worn = worn_warmth(p)
            exposure = (1.0 - place_warm) * (1.0 - worn) * min(cold, 1.0)
            felt_warmth[p.id] = 1.0 - exposure
            p.health -= c.cold_damage * exposure * max(cold, 1.0) * (2.0 if frail else 1.0)
            if exposure > 0.5 and p.health < 60:
                p.hurt_by = p.hurt_by or "cold"
            if st != "infant":
                expected = knowhow.expectation(p, "warm", place_warm)
                if p.age(tick) >= 6 * WEEKS_PER_YEAR:
                    knowhow.associate(world, p, p.loc, place_warm - expected)
                if worn > 0:
                    idx, _ = best_item(p, "cold")
                    knowhow.judge_item(world, p, p.items[idx]["sig"], worn)
                    p.items[idx]["uses"] -= 1
                    if p.items[idx]["uses"] <= 0:
                        p.items.pop(idx)

        # Orphaned little ones suffer without someone to look after them.
        if st in ("infant", "child") and p.age(tick) < 6 * WEEKS_PER_YEAR and not p.caregiver:
            p.health -= 10.0 if st == "infant" else 4.0
            p.hurt_by = "neglect"

        if p.sick:
            p.health -= c.illness_damage
            if rng.random() < c.illness_recovery + (0.25 if p.cared else 0.0) + (0.1 if deficit < 0.05 else 0.0):
                p.sick = False
            else:
                p.hurt_by = "illness"
        else:
            chance = c.illness_chance * (1.0 + 2.0 * deficit) * (2.0 if frail else 1.0) * (0.8 if fire else 1.0)
            chance *= 1.0 + 0.15 * max(0, crowd.get(p.loc, 1) - 4)
            if rng.random() < chance:
                p.sick = True
                world.emit("ill", p.id, None, p.loc)

        p.health = min(p.health, p.max_health(tick))
        p.energy = min(100.0, p.energy + c.energy_recovery * (1.0 - 0.5 * deficit))

        if p.health <= 0:
            dying.append((p, p.hurt_by or "illness"))
        elif rng.random() < c.mortality_base * math.exp(c.mortality_rate * p.years(tick)):
            dying.append((p, "old age" if st == "elder" else "illness"))

    for p, cause in dying:
        if p.alive:
            die(world, p, cause, None)

    # Births and conceptions.
    courting = {a for pair in world.courting for a in pair}
    for p in list(world.living()):
        if p.sex != "F":
            continue
        if p.pregnant is not None:
            if tick - p.conceived >= c.pregnancy_weeks:
                give_birth(world, p)
            continue
        if p.partner is None or not (c.fertile_from <= p.years(tick) < c.fertile_until):
            continue
        mate = world.people[p.partner]
        apart = distance(p.loc, mate.loc, c.width, c.height) > c.camp_radius
        if not mate.alive or apart or p.health < 50 or p.starving or mate.age(tick) < CHILD_END:
            continue
        if tick - p.last_birth < c.nursing_weeks and _youngest_alive(world, p):
            continue
        chance = c.conception_chance * (2.0 if p.id in courting else 1.0)
        if rng.random() < chance:
            p.pregnant = mate.id
            p.conceived = tick
            world.emit("pregnant", p.id, mate.id, p.loc)

    # Orphans look for someone to take them in; at twelve, children fend for themselves.
    for p in world.living():
        if p.caregiver is None and p.age(tick) < CHILD_END:
            assign_caregiver(world, p)
        elif p.caregiver is not None and p.age(tick) >= CHILD_END:
            p.caregiver = None

    # Feelings, places, and what the week taught.
    for p in world.living():
        inquiry.fade(p)
        _feelings(world, p, felt_warmth.get(p.id, 1.0))
        if p.age(tick) >= INFANT_END:
            knowhow.feel_place(p, p.loc, p.wellbeing)
            _learn(world, p)
            if world.cfg.b2_mode and p.age(tick) >= 16 * WEEKS_PER_YEAR:
                _follow(world, p)

    if tick % 4 == 0:
        for p in world.living():
            _upbringing(world, p)
            _fade_memories(p, 4)
    if tick % 13 == 0:
        for p in world.living():
            _upkeep_relations(world, p, 13)
            knowhow.prune_placements(world, p)
            knowhow.forget_useless(p)
        knowhow.check_lost(world)


def _wet_and_dry(world, p) -> None:
    """A week of weather on what p carries. Rain soaks what is in the open (to 5 of 10); going into
    water soaks everything through (10); a dry week dries things out (by 4, by 6 in summer), and a fire
    dries them completely. Embers carried in something die down, and go out if it is soaked."""
    tile = world.tile(p.loc)
    if tile.water:
        soak, dry = 10, 0
    elif weather.raining(world, p.loc) and pile_shape(tile.pile)[1] < 0.3:
        soak, dry = 5, 0
    else:
        soak, dry = 0, 10 if tile.fire > 0 else (6 if world.season == 1 else 4)
    for k, v in p.mats.items():
        if v < 0.5:
            p.damp.pop(k, None)
            continue
        w = max(p.damp.get(k, 0), soak) - dry
        if w > 0:
            p.damp[k] = min(10, w)
        else:
            p.damp.pop(k, None)
    for it in p.items:
        it["wet"] = max(0, min(10, max(it.get("wet", 0), soak) - dry))
        h = it.get("holds")
        if h and h[0] == "embers":
            h[1] -= 1
            if h[1] <= 0 or it["wet"] >= 8:
                it["holds"] = None

    _passive_water(world, p, tile)
    _passive_heat(world, p, tile)


def _passive_water(world, p, tile) -> None:
    """E7 (spec 3.1). Rain falls into any open watertight hollow thing carried outside a covered heap,
    and going into a river or lake fills it. A week of rain is the only measure of rain there is, so
    it fills the thing."""
    submerged = tile.water or tile.biome == "river"
    if not (submerged or (weather.raining(world, p.loc) and pile_shape(tile.pile)[1] <= 0.5)):
        return
    for it in p.items:
        cap = matter.can_hold(it, "water")
        h = it.get("holds")
        if cap > 0 and (h is None or h[0] == "water") and (h[1] if h else 0) < cap:
            it["holds"] = ["water", cap]
            world.emit("consequence", p.id, None, p.loc, what="water_passive", thing=it["sig"],
                       how="submerged" if submerged else "rain")


def _passive_heat(world, p, tile) -> None:
    """E7 (spec 3.2). A fire hot enough (6+) sets whatever dry plastic stuff is carried by it, a
    shaped thing or a lump of raw clay, the same way holding it in the fire would. Food by a fire
    already rots slower in the smoke; that is only counted here."""
    if tile.fire <= 0:
        return
    if p.food > 0:
        world.emit("consequence", p.id, None, p.loc, what="food_by_fire")
    level = tile.fire_heat
    if level < 6:
        return
    for i, it in enumerate(list(p.items)):
        if it.get("plastic", 0) >= 50 and it.get("wet", 0) <= matter.DRY:
            out, _ = matter.heat(it, level)
            if out is not None and out["sig"] != it["sig"]:
                p.items[i] = out
                _baked(world, p, it["sig"], out, level)
    for m in matter.MATERIALS:
        if matter.RAW[m][7] >= 50 and p.mats.get(m, 0.0) >= 1.0 and p.damp.get(m, 0) <= matter.DRY:
            thing = matter.raw_props(m)
            thing["wet"] = 0
            out, _ = matter.heat(thing, level)
            if out is not None and out["sig"] != thing["sig"]:
                from .actions import _keep
                p.mats[m] -= 1.0
                _keep(p, out, world.cfg.item_limit, world)
                _baked(world, p, m, out, level)


def _baked(world, p, part: str, out: dict, level: int) -> None:
    knowhow.remember_recipe(world, p, out["sig"], {"verb": "heat", "part": part, "level": level}, "heated",
                            props=copy.deepcopy(out) if world.cfg.knowledge_copy else out)   # NV2: a copy, not the item itself
    world.emit("consequence", p.id, None, p.loc, what="ceramic_passive", thing=out["sig"])


def _who_is_inside(world, living: list) -> dict:
    """Warmth each person gets from a heap on their tile. Builders first, by how much they put in."""
    out = {}
    by_tile: dict = {}
    for p in living:
        by_tile.setdefault(p.loc, []).append(p)
    for loc, people in by_tile.items():
        tile = world.tile(loc)
        if not tile.pile:
            continue
        warmth = pile_warmth(tile.pile)
        if warmth <= 0.01:
            continue
        room = pile_room(tile.pile)
        people.sort(key=lambda q: (-tile.builders.get(q.id, 0.0), q.id))
        for q in people[:room]:
            out[q.id] = warmth
    return out


def _youngest_alive(world, p: Person) -> bool:
    """TW1: whether any child of her latest delivery lives (with one child per delivery, v6's rule exactly)."""
    for cid in reversed(p.children):
        child = world.people[cid]
        if child.mother == p.id:
            if child.birth != p.last_birth:
                return False
            if child.alive:
                return True
    return False


def _feelings(world, p: Person, warm: float) -> None:
    tick = world.tick
    g = p.genes
    if not p.contact:
        for pid in (p.partner, p.caregiver):
            if pid and world.people[pid].loc == p.loc:
                p.contact = True
    if p.contact:
        p.loneliness = clamp(p.loneliness - 0.15)
    else:
        p.loneliness = clamp(p.loneliness + 0.04 * (0.5 + g["sociability"]))
    p.anger *= 0.8 + 0.15 * g["temper"]
    p.fear *= 0.75 + 0.15 * g["anxiety"]
    p.grief *= 0.985

    fed = 0.0 if p.starving else 1.0
    family = []
    if p.partner:
        family.append(world.people[p.partner])
    for cid in p.children:
        ch = world.people[cid]
        if ch.alive and ch.age(tick) < CHILD_END:
            family.append(ch)
    fam = sum(f.health / 100.0 for f in family) / len(family) if family else 0.5
    p.wellbeing = clamp(0.3 * fed + 0.2 * p.health / 100.0 + 0.2 * (1.0 - p.loneliness) + 0.15 * fam
                        + 0.15 * warm - 0.5 * p.grief - 0.25 * p.fear - 0.15 * p.anger)
    # Going over the same pain again and again weighs on a person; staying with a goal steadies them.
    mind = thought.state(p)
    if mind == "overthinking":
        p.wellbeing = clamp(p.wellbeing - 0.08)
        p.grief *= 1.01      # grief that is dwelt on fades more slowly
        kind, _, about = p.focus.partition(":")
        if kind == "memory" and about.isdigit():
            for m in p.memories:
                if m.eid == int(about):
                    m.strength = min(1.0, m.strength + 0.05)   # rehearsed, so remembered
    elif mind == "focused":
        p.wellbeing = clamp(p.wellbeing + 0.04)
    p.mood += 0.25 * (p.wellbeing - p.mood)


def _learn(world, p: Person) -> None:
    """Habits: how well this kind of action went here, counting what it led to next week."""
    c = world.cfg
    near = world.people_near(p.loc, c.reach, exclude=p.id)
    nxt = context_index(world, p, bool(near))
    future = max(p.q[nxt * N_ACTIONS:(nxt + 1) * N_ACTIONS])
    r = p.reward + 2.0 * (p.mood - p.mood_before)
    i = p.last_ctx * N_ACTIONS + A[p.last_action]
    p.q[i] = clamp(p.q[i] + c.learning_rate * (r + c.discount * future - p.q[i]), -1.5, 1.5)


def _follow(world, p: Person) -> None:
    """E13 (B2): seeing someone who visibly does better forage, and what they got, teaches p what foraging in their
    situation would be worth to p. Only what is seen is used: the model's action, situation and harvest."""
    c = world.cfg
    cands = [q for q in world.people_near(p.loc, c.perception, exclude=p.id)
             if q.alive and q.age(world.tick) >= 16 * WEEKS_PER_YEAR and q.edible() > p.edible()]
    if c.b2_mode == 2:
        cands = [q for q in cands if q.children and all(world.people[k].alive for k in q.children)]
    elif c.b2_mode == 3:
        cands = [q for q in cands if q.edible() < c.b2_planner_food]
    elif c.b2_mode == 4:
        cands = [q for q in cands if q.edible() >= c.b2_planner_food]
    if not cands:
        return
    m = min(cands, key=lambda q: (-q.edible(), q.id))
    if m.last_action != "forage":
        return
    got = next((e.get("got", 0.0) for e in world.events if e["k"] == "forage" and e.get("a") == m.id), None)
    if got is None:
        return
    from .mind import hunger_of
    r = 0.3 * min(1.0, got / p.need(c, world.tick)) * (0.3 + 0.7 * hunger_of(world, p))
    ctx = m.last_ctx
    future = max(p.q[ctx * N_ACTIONS:(ctx + 1) * N_ACTIONS])
    i = ctx * N_ACTIONS + A["forage"]
    new = clamp(p.q[i] + c.learning_rate * (r + c.discount * future - p.q[i]), -1.5, 1.5)
    if not c.b2_write:
        return
    p.q[i] = new


def _upbringing(world, p: Person) -> None:
    """Children absorb the ways of whoever raises them."""
    if p.age(world.tick) >= CHILD_END or not p.caregiver:
        return
    carer = world.people[p.caregiver]
    if not carer.alive or carer.loc != p.loc:
        return
    rate = 0.08
    pq, cq = p.q, carer.q
    for i in range(len(pq)):
        pq[i] += rate * (cq[i] - pq[i])


def _fade_memories(p: Person, weeks: int) -> None:
    keep = []
    for m in p.memories:
        m.strength *= (1.0 - 0.015 * (1.0 - m.salience) ** 2 - 0.0002) ** weeks
        if m.strength >= 0.05:
            keep.append(m)
    p.memories = keep


def _upkeep_relations(world, p: Person, weeks: int) -> None:
    temper = p.genes["temper"]
    grudge_keep = (1.0 - 0.003 * (1.5 - temper)) ** weeks
    respect_keep = 0.998 ** weeks
    drop = []
    best, best_aff = None, 0.4
    for pid, r in p.rel.items():
        r.grudge *= grudge_keep
        r.respect *= respect_keep
        other = world.people.get(pid)
        if other is None or not other.alive:
            if r.grudge < 0.3:
                drop.append(pid)
            continue
        if world.tick - r.last > WEEKS_PER_YEAR:
            r.affection *= 0.995 ** weeks
            r.familiarity *= 0.99 ** weeks
            r.trust *= 0.995 ** weeks     # distrust of someone never seen again slowly fades
        if (r.familiarity < 0.03 and abs(r.affection) < 0.05 and r.grudge < 0.05
                and abs(r.trust) < 0.05 and abs(r.balance) < 1.0):
            drop.append(pid)
            continue
        if r.affection > best_aff and pid not in (p.partner, p.mother, p.father) and pid not in p.children:
            best, best_aff = pid, r.affection
    for pid in drop:
        del p.rel[pid]
    p.friend = best


# --- birth and death ---------------------------------------------------------


def give_birth(world, mother: Person) -> None:
    c = world.cfg
    rng = world.rng
    tick = world.tick
    father = world.people.get(mother.pregnant)
    mother.pregnant = None
    mother.last_birth = tick
    log = getattr(world, "tw1log", None)                 # TW1 logging (read-only; runner sets it)
    if log is not None:
        parity = len({world.people[x].birth for x in mother.children if world.people[x].mother == mother.id})
        n_alive = len(world.living())
    gen = max(mother.generation, father.generation if father else 0) + 1
    genes = _draw_genes(world, mother, father)

    def sex_draw():
        if c.sex_ratio_birth:                             # TW1: boys 105 to girls 100
            return "M" if rng.random() < 105.0 / 205.0 else "F"
        return rng.choice(("F", "M"))
    first = _born(world, mother, father, genes, make_name(rng), sex_draw(), gen)
    kind = None
    if c.twins:                                           # TW1: one draw per delivery that reads nothing else
        u = rng.random()
        kind = "identical" if u < 0.004 else "fraternal" if u < 0.014 else None
        if kind == "identical":
            second = _born(world, mother, father, dict(genes), make_name(rng), first.sex, gen)
        elif kind == "fraternal":
            g2 = _draw_genes(world, mother, father)
            second = _born(world, mother, father, g2, make_name(rng), sex_draw(), gen)
    if log is not None:
        sexes = [first.sex] + ([second.sex] if kind else [])
        log.append((tick, mother.id, round(mother.years(tick), 2), parity, n_alive, kind or "single", sexes,
                    first.id, second.id if kind else None))
    if rng.random() < c.birth_death_chance:
        mother.hurt_by = "childbirth"
        die(world, mother, "childbirth", None)


def _draw_genes(world, mother, father) -> dict:
    c = world.cfg
    rng = world.rng
    genes = {}
    for gname in GENES:
        mid = (mother.genes[gname] + (father.genes[gname] if father else mother.genes[gname])) / 2.0
        genes[gname] = round(clamp(mid + rng.gauss(0.0, c.mutation), 0.02, 0.98), 4)
    return genes


def _born(world, mother, father, genes, name, sex, gen):
    """One child of a delivery (TW1: called twice for twins; v6's steps, unchanged)."""
    tick = world.tick
    child = Person(world._new_pid(), name, sex, tick, gen, genes, mother.loc)
    child.health = 70.0
    child.mother = mother.id
    child.father = father.id if father else None
    child.caregiver = mother.id
    parents = [mother] + ([father] if father else [])
    for par in parents:
        par.children.append(child.id)
        love = 0.5 + 0.5 * par.genes["care"]
        if par is father:
            love *= 0.8
        par.rel[child.id] = Relation(affection=love, trust=0.5, familiarity=1.0, last=tick)
        child.rel[par.id] = Relation(affection=0.7, trust=0.7, familiarity=1.0, last=tick)
    # Habits start as a softened blend of the parents'.
    fq = father.q if father and father.alive else mother.q
    child.q = [0.25 * (a + b) for a, b in zip(mother.q, fq)]
    world.people[child.id] = child
    world._living = None
    world.occ.setdefault(child.loc, []).append(child.id)
    eid = world.emit("birth", mother.id, child.id, mother.loc,
                     father=child.father, name=child.name, generation=gen)
    for par in parents:
        if par.alive:
            remember(world, par, eid, "born", par.id, child.id, mother.loc, 0.8, 0.9)
            par.mood = clamp(par.mood + 0.2)
    return child


def die(world, p: Person, cause: str, killer) -> None:
    tick = world.tick
    p.alive = False
    p.death_tick = tick
    p.death_cause = cause
    world._living = None
    here = world.occ.get(p.loc)
    if here and p.id in here:
        here.remove(p.id)
    eid = world.emit("death", p.id, killer, p.loc, cause=cause, age=round(p.years(tick), 1),
                     generation=p.generation)
    world.graves[f"{p.loc[0]},{p.loc[1]}"] = tick

    # Those nearby see it; family elsewhere hears later, if someone tells them.
    kind = "killed" if killer else "died"
    for q in world.people_near(p.loc, world.cfg.perception):
        if q.age(tick) < 52 * 3:
            continue
        sal = clamp(0.3 + 0.6 * max(_close(world, q, p.id), 0.0))
        fresh = remember(world, q, eid, kind, killer, p.id, p.loc, sal, -0.8)
        if killer is None:
            react(world, q, "died", None, p.id, 1.0, fresh)
        elif q.id != killer:
            react(world, q, "killed", killer, p.id, 1.0, fresh)

    # Partner is free; belongings go to family on the spot or are left where they fell.
    heir = None
    if p.partner:
        mate = world.people[p.partner]
        mate.partner = None
        if mate.alive and mate.loc == p.loc:
            heir = mate
    if heir is None:
        for cid in p.children:
            ch = world.people[cid]
            if ch.alive and ch.loc == p.loc and ch.age(tick) >= CHILD_END:
                heir = ch
                break
    tile = world.tile(p.loc)
    if heir is not None:
        heir.food += p.food
        heir.seeds += p.seeds
        for k, v in p.mats.items():
            heir.mats[k] += v
        for it in p.items:
            heir.items.append(it)
        while len(heir.items) > world.cfg.item_limit:
            heir.items.pop(0)
        world.emit("inherit", heir.id, p.id, p.loc, food=round(p.food + p.seeds, 2), things=len(p.items))
    else:
        if not world.cfg.bodies_stay:
            tile.plants += p.food + p.seeds
        for k, v in p.mats.items():
            if v > 0:
                tile.pile[k] = tile.pile.get(k, 0.0) + v
    if world.cfg.bodies_stay:
        _leave_body(world, p, tile, heir, eid, kind, killer)
    p.food = p.seeds = 0.0
    p.mats = {k: 0.0 for k in p.mats}
    p.items = []

    for cid in p.children + p.wards:
        ch = world.people[cid]
        if ch.alive and ch.caregiver == p.id:
            ch.caregiver = None
            assign_caregiver(world, ch)

    # A person's memories, habits and know-how end with them.
    p.memories = []
    p.q = []
    p.recipes = {}
    p.itemval = {}
    p.beliefs = {}
    p.placements = []
    p.places = {}
    p.expect = {}
    p.heard = {}
    p.puzzles = {}
    p.marks = {}
    p.springs = []
    p.records = {}
    p.sightings = []
    p.shores = []
    p.voyage = None
    p.rel = {k: r for k, r in p.rel.items() if k in (p.mother, p.father, p.partner)}


BODY_MEAT = 18.0          # BD1: food in an adult body (a deer gives 22); an assumption, not a measurement
ROT_SHARE = 0.4           # BD1: rotten once this share would have rotted at v3's rate for loose food


def _leave_body(world, p: Person, tile, heir, eid: int, kind: str, killer) -> None:
    """BD1: the body stays where they fell. Its meat, and the food they carried if no relative took it, lie there as
    food that is still theirs (v3's store, owned by the dead). Their tools stay with the body for kin to take."""
    years = p.years(world.tick)
    meat = BODY_MEAT * (1.0 if years >= 16 else max(0.2, years / 16.0))
    food = meat + (p.food if heir is None else 0.0)
    seeds = p.seeds if heir is None else 0.0
    tile.stash.append([p.id, food, seeds, world.tick])
    world.bodies.append({"id": p.id, "x": p.loc[0], "y": p.loc[1], "tick": world.tick, "eid": eid,
                         "kind": kind, "killer": killer, "start": food,
                         "items": [] if heir is not None else list(p.items), "flesh": True})
    if world.cfg.body_rot:                  # BD2: the flesh apart from what they carried, and warmth so far
        world.bodies[-1]["meat0"] = meat
        world.bodies[-1]["add"] = 0.0
    log = getattr(world, "bd1log", None)    # BD1 logging (runner sets it; not saved; read by nothing here)
    if log is not None:
        log.append(("body", world.tick, p.id, round(meat, 2), round(food, 2), len(p.items) if heir is None else 0))


BONES_ADD = 1300.0        # BD2: degree-days (deg C x days above 0) until only bones are left; an assumption anchored
                          # to forensic work showing decay follows accumulated temperature (Megyesi et al. 2005)


def celsius(world, loc) -> float:
    """BD2: this week's warmth here in degrees C, from ACL's felt temperature (0.45 felt = 15 C, 0.15 = 0 C)."""
    t = world.tile(loc)
    felt = t.temp + weather.SEASON_TEMP[world.season]
    if world.season == 3:
        felt -= world.sky.get("hard", 0.0)
    return 50.0 * felt - 7.5


def _rot_by_warmth(world, b, tile) -> None:
    """BD2: a week of rot. The flesh loses its share of the degree-days that passed; what they carried rots as stored
    food does (v5's rate). Eating takes from both alike."""
    entry = next((st for st in tile.stash if st[0] == b["id"]), None)
    if entry is None:
        return
    dd = 7.0 * max(0.0, celsius(world, (b["x"], b["y"])))
    meat_left = max(0.0, b["meat0"] * (1.0 - b["add"] / BONES_ADD))
    carried = max(0.0, entry[1] - meat_left)
    flesh = entry[1] - carried
    b["add"] += dd
    flesh = max(0.0, flesh - b["meat0"] * dd / BONES_ADD)
    entry[1] = carried * (1.0 - world.cfg.spoil_rate) + flesh
    if b["add"] >= BONES_ADD:
        b["bones_now"] = True


def rot_weeks(world) -> int:
    """Weeks until a body counts as rotten: when ROT_SHARE of loose food would have rotted at v3's rate."""
    return math.ceil(math.log(1.0 - ROT_SHARE) / math.log(1.0 - world.cfg.spoil_rate))


def bodies_week(world) -> None:
    """BD1: each week, what the bodies of the dead do among the living. Rot follows v3's rate for loose food (it is
    v3's store). The living near a rotten body find the place foul; those who were close to the dead and had not
    known of the death learn it from the sight; a partner or grown child who stands there takes the tools."""
    tick = world.tick
    log = getattr(world, "bd1log", None)
    rotten_after = rot_weeks(world)
    keep = []
    for b in world.bodies:
        loc = (b["x"], b["y"])
        tile = world.tile(loc)
        if b["flesh"] and world.cfg.body_rot:
            _rot_by_warmth(world, b, tile)
        if b["flesh"]:
            entry = next((st for st in tile.stash if st[0] == b["id"]), None)
            if entry is None or b.get("bones_now"):
                b["flesh"] = False
                from .world_traces import leave_trace
                leave_trace(tile, "bones:person", tick)
                if log is not None:
                    log.append(("bones", tick, b["id"], tick - b["tick"]))
        rotten = b["flesh"] and (b["add"] >= ROT_SHARE * BONES_ADD if world.cfg.body_rot
                                  else tick - b["tick"] >= rotten_after)
        dead = world.people[b["id"]]
        for q in world.people_near(loc, world.cfg.perception):
            if q.age(tick) < 52 * 3:
                continue
            near = distance(q.loc, loc, world.cfg.width, world.cfg.height) <= 1
            if rotten and near:
                knowhow.associate(world, q, q.loc, -0.3)        # the smell of rot: the place feels foul
                if log is not None:
                    log.append(("foul", tick, q.id, b["id"]))
            if b["flesh"] and not any(m.eid == b["eid"] for m in q.memories):
                close = _close(world, q, b["id"])
                if close > 0:                                   # they see who it is
                    sal = clamp(0.3 + 0.6 * max(close, 0.0))
                    fresh = remember(world, q, b["eid"], b["kind"], b["killer"], b["id"], loc, sal, -0.8)
                    react(world, q, "died" if b["killer"] is None else "killed", b["killer"], b["id"], 1.0, fresh)
                    if log is not None:
                        log.append(("seen", tick, q.id, b["id"]))
            if b["items"] and q.loc == loc and (q.id == dead.partner or (q.id in dead.children
                                                                           and q.age(tick) >= CHILD_END)):
                for it in b["items"]:
                    q.items.append(it)
                while len(q.items) > world.cfg.item_limit:
                    gone = q.items.pop(0)
                    if world.cfg.ground_items:              # OP1: left on the ground, not deleted
                        from .actions import drop_on_ground
                        drop_on_ground(world, q, gone)
                world.emit("inherit", q.id, b["id"], loc, food=0.0, things=len(b["items"]))
                if log is not None:
                    log.append(("tools", tick, q.id, b["id"], len(b["items"])))
                b["items"] = []
        if b["flesh"] or b["items"]:
            keep.append(b)
    world.bodies = keep


def _close(world, q: Person, other: str) -> float:
    r = q.rel.get(other)
    aff = r.affection if r else 0.0
    o = world.people.get(other)
    return max(aff, world.kinship(q, o) if o else 0.0, 1.0 if q.partner == other else 0.0)


def assign_caregiver(world, child: Person) -> None:
    """Family first: the other parent, grown siblings, grandparents. Then a kind stranger nearby."""
    tick = world.tick
    candidates = []
    for pid in (child.mother, child.father):
        if pid:
            candidates.append(pid)
    for pid in (child.mother, child.father):
        if pid:
            par = world.people[pid]
            candidates.extend(par.children)
    for pid in (child.mother, child.father):
        if pid:
            par = world.people[pid]
            for gp in (par.mother, par.father):
                if gp:
                    candidates.append(gp)
    for pid in candidates:
        q = world.people.get(pid)
        if q and q.alive and q.id != child.id and q.age(tick) >= 14 * WEEKS_PER_YEAR:
            child.caregiver = q.id
            if child.id not in q.children and child.id not in q.wards:
                q.wards.append(child.id)
                q.rel.setdefault(child.id, Relation(affection=0.5, trust=0.4, familiarity=0.5, last=tick))
            world.emit("taken_in", q.id, child.id, q.loc, by="family")
            return
    best, best_score = None, 0.35
    for q in world.people_near(child.loc, world.cfg.reach):
        if q.age(tick) < 16 * WEEKS_PER_YEAR or q.id == child.id:
            continue
        score = q.genes["care"] * q.genes["kindness"]
        for pid in (child.mother, child.father):
            r = q.rel.get(pid) if pid else None
            if r:
                score += 0.5 * max(r.affection, 0.0)
        if score > best_score:
            best, best_score = q, score
    if best is not None:
        child.caregiver = best.id
        if child.id not in best.wards:
            best.wards.append(child.id)
        best.rel[child.id] = Relation(affection=0.4, trust=0.3, familiarity=0.3, last=tick)
        child.rel[best.id] = Relation(affection=0.4, trust=0.4, familiarity=0.3, last=tick)
        world.emit("taken_in", best.id, child.id, best.loc, by="adoption")
