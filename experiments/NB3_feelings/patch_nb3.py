"""code_nb3 = code_nb2 + NB3's feelings (questions.md, NB3-frozen); with nb3 0 it is code_nb2 exactly.

  python experiments/NB3_feelings/patch_nb3.py          # rebuilds code_nb3 from code_nb2 (line endings kept)
"""
import shutil
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent / "NB2_connected_brain" / "code_nb2"
DST = HERE / "code_nb3"


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
shutil.copyfile(HERE / "brain_nb3.py", root / "brain_nb3.py")

patch(root / "config.py", [(
    "    nb2: int = 0 ",
    "    nb3: int = 0                       # NB3: feelings (brain_nb3.py); the switches below act only with nb3\n"
    "    nb3_no_attack_joy: int = 0         # NB3: no +0.1 per attack and no kill bonus\n"
    "    nb3_E: int = 0                     # NB3: empathy\n"
    "    nb3_G: int = 0                     # NB3: guilt\n"
    "    nb3_L: int = 0                     # NB3: love of one's own child\n"
    "    nb3_A: int = 0                     # NB3: approval and shame\n"
    "    nb3_C: int = 0                     # NB3: curiosity\n"
    "    nb3_H: int = 0                     # NB3: an inborn reluctance to harm\n"
    "    nb2: int = 0 ")])

patch(root / "world.py", [(
    '''    def step(self) -> list[dict]:
        self.events = []
''',
    '''    def step(self) -> list[dict]:
        if self.cfg.nb3:                    # NB3: social.bump files approval under the world now stepping
            from . import brain_nb3
            brain_nb3.CUR[0] = id(self)
        self.events = []
''')])

patch(root / "social.py", [(
    '''    r.balance += balance
    r.last = tick
''',
    '''    r.balance += balance
    r.last = tick
    if affection or grudge:                 # NB3: approval and shame (filed only while an NB3 world steps)
        from . import brain_nb3
        brain_nb3.on_bump(other, affection, grudge)
''')])

patch(root / "actions.py", [
    ('''    sp, sq = strength(world, p), strength(world, q)
    if sp + sq <= 0:
        return
''',
     '''    sp, sq = strength(world, p), strength(world, q)
    if sp + sq <= 0:
        return
    if world.cfg.nb3:                       # NB3: was it defence? (read before the attack changes anything)
        from . import brain_nb3
        brain_nb3.before_attack(world, p, q)
'''),
    ('''    killed = q.health <= 0
    kind = "killed" if killed else "attacked"
''',
     '''    killed = q.health <= 0
    kind = "killed" if killed else "attacked"
    if world.cfg.nb3:                       # NB3: the target remembers; guilt for an attack one started
        from . import brain_nb3
        brain_nb3.on_attack(world, p, q, killed)
'''),
    ('''        p.reward += 0.3 * p.genes["temper"] - 0.2 * p.genes["kindness"]
''',
     '''        if not world.cfg.nb3_no_attack_joy:  # NB3: no joy in killing
            p.reward += 0.3 * p.genes["temper"] - 0.2 * p.genes["kindness"]
'''),
    ('''        remember(world, q, eid, "attacked", p.id, q.id, p.loc, 0.8, -0.9)
        p.reward += 0.1
''',
     '''        remember(world, q, eid, "attacked", p.id, q.id, p.loc, 0.8, -0.9)
        if not world.cfg.nb3_no_attack_joy:  # NB3: no joy in attacking
            p.reward += 0.1
'''),
    ('''        bump(q, p.id, world.tick, trust=-0.4, affection=-0.3, grudge=0.3 + 0.2 * q.genes["temper"])
''',
     '''        bump(q, p.id, world.tick, trust=-0.4, affection=-0.3, grudge=0.3 + 0.2 * q.genes["temper"])
        if world.cfg.nb3:                   # NB3: guilt for a noticed theft
            from . import brain_nb3
            brain_nb3.on_theft(world, p)
'''),
    ('''        bump(o, p.id, world.tick, trust=-0.4, affection=-0.3, grudge=0.25 + 0.2 * o.genes["temper"])
''',
     '''        bump(o, p.id, world.tick, trust=-0.4, affection=-0.3, grudge=0.25 + 0.2 * o.genes["temper"])
        if world.cfg.nb3:                   # NB3: guilt for a noticed theft
            from . import brain_nb3
            brain_nb3.on_theft(world, p)
'''),
])

patch(root / "brain_nb2.py", [
    ('''    eta = ETA0_AC if world.cfg.nb_critic else nb1.ETA0
    return {"g": 1.0, "eta": eta, "genome": g.tolist(), "w": g.tolist(), "base": 0.0}


def child(''',
     '''    eta = ETA0_AC if world.cfg.nb_critic else nb1.ETA0
    out = {"g": 1.0, "eta": eta, "genome": g.tolist(), "w": g.tolist(), "base": 0.0}
    if world.cfg.nb3:                       # NB3: the feeling genes (founders: the start values)
        from . import brain_nb3
        brain_nb3.add_genes(out, None, rng_np)
    return out


def child('''),
    ('''        eta = ETA0_AC if world.cfg.nb_critic else nb1.ETA0
        return {"g": 1.0, "eta": eta, "genome": g.tolist(), "w": g.tolist(), "base": 0.0}
''',
     '''        eta = ETA0_AC if world.cfg.nb_critic else nb1.ETA0
        out = {"g": 1.0, "eta": eta, "genome": g.tolist(), "w": g.tolist(), "base": 0.0}
        if world.cfg.nb3:
            from . import brain_nb3
            brain_nb3.add_genes(out, None, rng_np)
        return out
'''),
    ('''    return {"g": g, "eta": eta, "genome": genome.tolist(), "w": genome.tolist(), "base": 0.0}
''',
     '''    out = {"g": g, "eta": eta, "genome": genome.tolist(), "w": genome.tolist(), "base": 0.0}
    if world.cfg.nb3:                       # NB3: the feeling genes, from the same parent, mutated
        from . import brain_nb3
        brain_nb3.add_genes(out, s, rng_np)
    return out
'''),
    ('''    new = [(g * (s - lw * p.q[base + A[a]]) + float(out[k]), a, t) for k, (s, a, t) in enumerate(options)]
''',
     '''    if world.cfg.nb3:                       # NB3: the inborn reluctance to harm (not scaled by g)
        from . import brain_nb3
        hb = [brain_nb3.harm_bias(world, p, a, t) for _, a, t in options]
    else:
        hb = [0.0] * len(options)
    new = [(g * (s - lw * p.q[base + A[a]]) + hb[k] + float(out[k]), a, t) for k, (s, a, t) in enumerate(options)]
'''),
])

patch(root / "brain_nb.py", [(
    '''def learn(world, p, r, on):    # noqa: F811
    if _two(world):
        from . import brain_nb2
        return brain_nb2.learn(world, p, r, on)''',
    '''def learn(world, p, r, on):    # noqa: F811
    if _two(world):
        from . import brain_nb2
        if world.cfg.nb3:                   # NB3: the week's feelings join the feeling the brain learns from
            from . import brain_nb3
            r = r + brain_nb3.feel(world, p)
        return brain_nb2.learn(world, p, r, on)''')])
print("built", DST)
