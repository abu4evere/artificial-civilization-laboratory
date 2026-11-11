"""NB3: feelings (experiments/NB3_feelings/questions.md, NB3-frozen, "THE FROZEN DESIGN").

Each feeling changes the weekly feeling number r that NB2's brain learns from; nothing forbids any act. Genes E, G, L,
A, C, H (range 0-2, mutation sd 0.08) are inherited with the network genome; founders take the start values.
  nb3_no_attack_joy  no +0.1 per attack and no kill bonus (in actions._attack)
  nb3_E  empathy: r -= E x weighted mean over people in reach of (rise in distress + 0.25 x distress)
  nb3_G  guilt for harm one starts to people (attack +0.3, kill +1.0, x2 kin; noticed theft +0.15); r -= G x guilt;
         guilt x 0.9 a week; an attack on someone who attacked one in the last 4 weeks is defence (no guilt)
  nb3_L  love of one's own child: r += L x (mean well of own children under 6 - 0.5 x mean distress of own children
         under 12) + 0.1 L for a week caring for or giving to one's own child
  nb3_A  approval and shame: r += A x (affection others gave one this week - grudges they took against one)
  nb3_C  curiosity: r += C x 0.1 / (1 + times this action was done in this situation), never for attack or steal
  nb3_H  inborn reluctance: attack and steal options' instinct score - H, except an attack in defence
This module is in code_nb3 only.
"""
from __future__ import annotations

from .util import distance

GENES = {"E": 0.5, "G": 0.5, "L": 1.0, "A": 0.5, "C": 0.5, "H": 1.0}
GENE_SD, GENE_MAX = 0.08, 2.0
DEFENCE_WEEKS = 4
APPR: dict = {}            # (id(world), pid) -> this week's approval from others' relation updates; checkpointed
CUR = [0]                  # id of the world now stepping (set by world.step), so social.bump can file approval


def add_genes(nb, src, rng_np):
    """Founders (src None) take the start values; a child inherits the parent's (the network's source) with mutation."""
    for k, v in GENES.items():
        if src is None or k not in src:
            nb[k] = v
        else:
            nb[k] = min(GENE_MAX, max(0.0, src[k] + float(rng_np.normal(0.0, GENE_SD))))
    nb["guilt"] = 0.0
    nb["att"] = {}         # attacker id -> the week they last attacked this person
    nb["cnt"] = {}
    return nb


def on_bump(other: str, affection: float, grudge: float) -> None:
    v = affection - max(0.0, grudge)
    if v:
        key = (CUR[0], other)
        APPR[key] = APPR.get(key, 0.0) + v


def defence(world, p, q) -> bool:
    """p attacking q is defence if q attacked p in the last 4 weeks."""
    if p.nb is None:
        return False
    t = p.nb.get("att", {}).get(q.id)
    return t is not None and world.tick - t <= DEFENCE_WEEKS


def on_attack(world, p, q, killed: bool) -> None:
    """After p attacked q (p started it): q remembers the attack (for its defence); p's guilt unless it was defence."""
    was_defence = defence_before.pop((id(world), p.id, q.id), False)
    if q.nb is not None:
        att = q.nb.setdefault("att", {})
        for k in [k for k, t in att.items() if world.tick - t > DEFENCE_WEEKS]:
            del att[k]
        att[p.id] = world.tick
    if p.nb is None or not world.cfg.nb3_G or was_defence:
        return
    add = 0.3
    if killed:
        add += 1.0 * (2.0 if world.kinship(p, q) > 0 else 1.0)
    p.nb["guilt"] = p.nb.get("guilt", 0.0) + add


defence_before: dict = {}  # (id(world), attacker, target) -> was it defence (read before the attack changes anything)


def before_attack(world, p, q) -> None:
    defence_before[(id(world), p.id, q.id)] = defence(world, p, q)


def on_theft(world, p) -> None:
    if p.nb is not None and world.cfg.nb3_G:
        p.nb["guilt"] = p.nb.get("guilt", 0.0) + 0.15


def harm_bias(world, p, action, target) -> float:
    """The inborn reluctance: -H for attack and steal options, except an attack in defence."""
    if not world.cfg.nb3_H or p.nb is None or action not in ("attack", "steal"):
        return 0.0
    if action == "attack" and isinstance(target, str) and target in world.people and defence(world, p, world.people[target]):
        return 0.0
    return -p.nb.get("H", GENES["H"])


def distress(world, q) -> float:
    need = q.need(world.cfg, world.tick) or 1.0
    hunger = min(1.0, max(0.0, 1.0 - (q.edible() / need) / 2.0))
    return (hunger + 1.0 - q.health / 100.0) / 2.0


def _dist_last(world, q) -> float:
    """q's distress at the end of last week (q's own snapshot), or now if there is none."""
    if q.nb is None:
        return distress(world, q)
    if q.nb.get("d_week") == world.tick:          # q already took this week's snapshot: use the one before
        return q.nb.get("d_last", q.nb.get("d_now", 0.0))
    return q.nb.get("d_now", distress(world, q))


def feel(world, p) -> float:
    """The week's feelings, added to r before learning. Also takes p's own distress snapshot for others' empathy."""
    c = world.cfg
    nb = p.nb
    if nb is None or not c.nb3:
        return 0.0
    tick = world.tick
    add = 0.0
    if c.nb3_E:
        num = den = 0.0
        for q in world.people_near(p.loc, c.reach, exclude=p.id):
            kin = world.kinship(p, q) > 0 or p.partner == q.id
            r = p.rel.get(q.id)
            wt = 1.0 if kin else (0.5 if r is not None and r.affection > 0.3 else 0.2)
            d = distress(world, q)
            num += wt * (max(0.0, d - _dist_last(world, q)) + 0.25 * d)
            den += wt
        if den > 0:
            add -= nb["E"] * num / den
    if c.nb3_G:
        add -= nb["G"] * nb.get("guilt", 0.0)
        nb["guilt"] = nb.get("guilt", 0.0) * 0.9
    if c.nb3_L:
        young = [world.people[k] for k in p.children if world.people[k].alive and world.people[k].age(tick) < 12 * 52]
        if young:
            small = [k for k in young if k.age(tick) < 6 * 52]
            well = 0.0
            if small:
                def ok(k):
                    carer = world.people.get(k.caregiver)
                    return (k.edible() >= 0.5 * k.need(c, tick) and k.health >= 50 and carer is not None
                            and carer.loc == k.loc)
                well = sum(1.0 for k in small if ok(k)) / len(small)
            concern = sum(distress(world, k) for k in young) / len(young)
            add += nb["L"] * (well - 0.5 * concern)
        from . import brain_nb2
        ch = brain_nb2.CHOSEN.get((id(world), p.id))
        if ch is not None and ch[0] == tick and ch[1] in ("care", "give") and ch[2] in p.children:
            add += 0.1 * nb["L"]
    if c.nb3_A:
        add += nb["A"] * APPR.pop((id(world), p.id), 0.0)
    else:
        APPR.pop((id(world), p.id), None)
    if c.nb3_C and p.last_action not in ("attack", "steal"):
        key = f"{p.last_ctx}:{p.last_action}"
        n = nb["cnt"].get(key, 0)
        add += nb["C"] * 0.1 / (1 + n)
        nb["cnt"][key] = n + 1
    # p's own distress snapshot, for the empathy of others
    nb["d_last"] = nb.get("d_now", distress(world, p))
    nb["d_now"] = distress(world, p)
    nb["d_week"] = tick
    return add
