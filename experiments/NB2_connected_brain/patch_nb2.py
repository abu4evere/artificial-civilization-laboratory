"""code_nb2 = code_nb1 + NB2 (questions.md, frozen as `NB2-frozen`); with nb2 0 and nb_options 0 it is code_nb1 exactly.

  python experiments/NB2_connected_brain/patch_nb2.py          # rebuilds code_nb2 from code_nb1 (line endings kept)
"""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent / "NB1_neural_brain" / "code_nb1"
DST = HERE / "code_nb2"


def patch(p, reps):
    s = p.read_bytes().decode("utf-8")
    crlf = "\r\n" in s
    s = s.replace("\r\n", "\n")
    for old, new in reps:
        assert s.count(old) == 1, (p.name, old[:90])
        s = s.replace(old, new)
    p.write_bytes((s.replace("\n", "\r\n") if crlf else s).encode("utf-8"))


if DST.exists():
    shutil.rmtree(DST)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))
root = DST / "acl"
shutil.copyfile(HERE / "brain_nb2.py", root / "brain_nb2.py")

patch(root / "config.py", [(
    "    nb_learn: int = 1 ",
    "    nb2: int = 0                       # NB2: with nb_brain, the network sees the facts (brain_nb2.py)\n"
    "    nb_options: int = 0                # NB2: options are what the body can do (several targets; no old thresholds)\n"
    "    nb_critic: int = 0                 # NB2: actor-critic learning (a learned state value; TD error)\n"
    "    nb_social: int = 0                 # NB2: learning from others into the network\n"
    "    nb_g_fixed: float = -1.0           # NB2 gardens only: g held at this value for everyone (-1 = off)\n"
    "    nb_learn: int = 1 ")])

# brain_nb: with nb2, every entry point is brain_nb2's
s = (root / "brain_nb.py").read_bytes().decode("utf-8")
crlf = "\r\n" in s
s = s.replace("\r\n", "\n") + '''

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
'''
(root / "brain_nb.py").write_bytes((s.replace("\n", "\r\n") if crlf else s).encode("utf-8"))

patch(root / "mind.py", [
    # the helpers
    ('''    lw = c.learned_weight

    options: list = []   # (score, action, target)
''',
     '''    lw = c.learned_weight
    nbo = c.nb_options              # NB2: options are what the body can do (several targets; no old thresholds)

    def spread(cands):
        """NB2: up to 4 of the candidate places (target, u, d): the 2 nearest, 1 from farther out, 1 at random."""
        seen, uniq = set(), []
        for x in sorted(cands, key=lambda x: (x[2], str(x[0]))):
            if str(x[0]) not in seen:
                seen.add(str(x[0]))
                uniq.append(x)
        out, rest = uniq[:2], uniq[2:]
        far = [x for x in rest if out and x[2] > out[-1][2]]
        if far:
            pick = far[rng.randrange(len(far))]
            out.append(pick)
            rest.remove(pick)
        if rest:
            out.append(rest[rng.randrange(len(rest))])
        return out

    def some(cands):
        """NB2: up to 4 of the candidates (people, prey, recipes), drawn at random."""
        cands, out = list(cands), []
        while cands and len(out) < 4:
            out.append(cands.pop(rng.randrange(len(cands))))
        return out

    options: list = []   # (score, action, target)
'''),
    # forage
    ('''        aff, aff_u, aff_d = None, -1.0, 0       # NV16 (FF4): the best target this person can afford
        for t in tiles:
            d = distance(p.loc, t, w, h)
            tile = world.tile(t)
            got = min(tile.plants + tile.crop, rate) * (1.0 - 0.1 * d)
            u = (0.25 + 1.6 * food_hunger) * min(1.0, got / (need * 1.5)) + 0.08 * g["diligence"]
''',
     '''        aff, aff_u, aff_d = None, -1.0, 0       # NV16 (FF4): the best target this person can afford
        fcands = []
        for t in tiles:
            d = distance(p.loc, t, w, h)
            tile = world.tile(t)
            got = min(tile.plants + tile.crop, rate) * (1.0 - 0.1 * d)
            u = (0.25 + 1.6 * food_hunger) * min(1.0, got / (need * 1.5)) + 0.08 * g["diligence"]
            fcands.append((t, u, d))
'''),
    ('''        if c.fix_affordable_target and p.energy < COST["forage"] + MOVE_COST * best_d:
            if aff is not None:
                add("forage", aff, aff_u, aff_d)
''',
     '''        if nbo:
            for t, u, d in spread(fcands):
                add("forage", t, u, d)
        elif c.fix_affordable_target and p.energy < COST["forage"] + MOVE_COST * best_d:
            if aff is not None:
                add("forage", aff, aff_u, aff_d)
'''),
    # hunt
    ('''        aff, aff_u, aff_d, aff_n = None, -1.0, 0, 1.0       # NV16 (FF4): the best target this person can afford
        for t in tiles:
''',
     '''        aff, aff_u, aff_d, aff_n = None, -1.0, 0, 1.0       # NV16 (FF4): the best target this person can afford
        hcands = []
        for t in tiles:
'''),
    ('''            u -= 0.5 * dread * (1.0 - 0.5 * g["boldness"])
''',
     '''            u -= 0.5 * dread * (1.0 - 0.5 * g["boldness"])
            if t not in [x[0] for x in hcands]:
                hcands.append((t, u, d))
'''),
    ('''        if best is not None:
            add("hunt", best, best_u, best_d)
''',
     '''        if nbo:
            for t, u, d in some(hcands):
                add("hunt", t, u, d)
        elif best is not None:
            add("hunt", best, best_u, best_d)
'''),
    # gather
    ('''            aff, aff_u, aff_d = None, 0.0, 0     # NV16 (FF4): the best target this person can afford
            for kind in GATHERABLE + (("earth",) if c.digging else ()):
''',
     '''            aff, aff_u, aff_d = None, 0.0, 0     # NV16 (FF4): the best target this person can afford
            gcands = []
            for kind in GATHERABLE + (("earth",) if c.digging else ()):
'''),
    ('''                    u = wk * (1.0 - 0.7 * hunger) * min(1.0, stock / 3.0) * (1.0 - 0.1 * d)
''',
     '''                    u = wk * (1.0 - 0.7 * hunger) * min(1.0, stock / 3.0) * (1.0 - 0.1 * d)
                    gcands.append(((t, kind), u, d))
'''),
    ('''            if best is not None:
                add("gather", best, best_u, best_d)
''',
     '''            if nbo:
                for t, u, d in spread(gcands):
                    add("gather", t, u, d)
            elif best is not None:
                add("gather", best, best_u, best_d)
'''),
    # make: only the body's limit (the parts and the fire); up to 4 recipes at random
    ('''            if v <= 0.05 or (_holding(p, sig) and v == p.itemval.get(sig, 0.0)) or resolve_recipe(world, p, recipe) is None:     # OD1 (D1)
''',
     '''            if ((not nbo and (v <= 0.05 or (_holding(p, sig) and v == p.itemval.get(sig, 0.0))))
                    or resolve_recipe(world, p, recipe) is None):     # OD1 (D1); NB2: only the body's limit
'''),
    ('''        if best is not None:
            add("make", best, best_u)
''',
     '''        if nbo:
            for sig, v, u in some(cands):
                add("make", sig, u)
        elif best is not None:
            add("make", best, best_u)
'''),
    # put: not for the grown only
    ('''    if grown:
        # Set something down here, if leaving such things has gone well before.
''',
     '''    if grown or (nbo and not toddler):
        # Set something down here, if leaving such things has gone well before.
'''),
    ('''            add("put", put[0], put[1])

        # Hold food in the fire here''',
     '''            add("put", put[0], put[1])

    if grown:
        # Hold food in the fire here'''),
    # take: one's own stashes (up to 4); others' without the hunger threshold
    ('''            add("take", (loc, p.id), u, distance(p.loc, loc, w, h))
            break
''',
     '''            add("take", (loc, p.id), u, distance(p.loc, loc, w, h))
            if not nbo or sum(1 for o in options if o[1] == "take") >= 4:
                break
'''),
    ('''        if hunger > 0.4 and grown:
''',
     '''        if grown and (hunger > 0.4 or nbo):
'''),
    # explore: not for the grown only; more places to set out for
    ('''    if grown:
        # Explore: curiosity, or hunger when nothing nearby is worth eating.
''',
     '''    if grown or (nbo and not toddler):
        # Explore: curiosity, or hunger when nothing nearby is worth eating.
'''),
    ('''        add("explore", dest, explore_u, c.reach)
        if world.tile(p.loc).water:
''',
     '''        add("explore", dest, explore_u, c.reach)
        if nbo and dest_random:         # NB2: more places to set out for, drawn the same way
            for _ in range(3):
                more = world.nearest_land(((p.loc[0] + rng.choice((-c.reach, 0, c.reach))) % w,
                                           (p.loc[1] + rng.choice((-c.reach, c.reach))) % h), p)
                add("explore", more, explore_u, c.reach)
        if world.tile(p.loc).water:
'''),
    # people: up to 4 at random; the old thresholds go
    ('''    for q in near:
        r = p.rel.get(q.id)
''',
     '''    for q in (some(near) if nbo else near):
        r = p.rel.get(q.id)
'''),
    ('''        if surplus > 1.0 and not (q.caregiver == p.id and q_st in ("infant", "child")):
''',
     '''        if (surplus > 1.0 or (nbo and p.edible() > 0.0)) and not (q.caregiver == p.id and q_st in ("infant", "child")):
'''),
    ('''        if q_trouble > 0.2 and (kin > 0 or is_partner or aff > 0.3) and st != "child":
''',
     '''        if q_trouble > (0.0 if nbo else 0.2) and (nbo or kin > 0 or is_partner or aff > 0.3) and st != "child":
'''),
    ('''            elif p.partner is None and q.partner is None and aff > -0.2:
''',
     '''            elif p.partner is None and q.partner is None and (aff > -0.2 or nbo):
'''),
    ('''        if q.food > 4.0 and hunger > 0.3 and kin < 0.5 and not is_partner and st != "child":
''',
     '''        if q.food > 4.0 and (hunger > 0.3 or nbo) and kin < 0.5 and not is_partner and st != "child":
'''),
    ('''        if grudge > 0.15 and st != "child":
''',
     '''        if (grudge > 0.15 or nbo) and st != "child":
'''),
    # join, home, water and fire: not for the grown only
    ('''    if grown:
        # Single adults with no one to court nearby go looking, beyond their own band if need be.
''',
     '''    if grown or (nbo and not toddler):
        # Single adults with no one to court nearby go looking, beyond their own band if need be.
'''),
])
print("built", DST)
