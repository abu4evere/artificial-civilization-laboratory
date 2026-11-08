"""code_nb1 = code_v17 + NB1's neural brain (questions.md, frozen as `NB1-frozen`); nb_brain 0 = v17 exactly.

  python experiments/NB1_neural_brain/patch_nb1.py <acl folder>      # patches the copy in place (line endings kept)
"""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent


def patch(p, reps):
    s = p.read_bytes().decode("utf-8")
    crlf = "\r\n" in s
    s = s.replace("\r\n", "\n")
    for old, new in reps:
        assert s.count(old) == 1, (p.name, old[:80])
        s = s.replace(old, new)
    p.write_bytes((s.replace("\n", "\r\n") if crlf else s).encode("utf-8"))


root = Path(sys.argv[1])
shutil.copyfile(HERE / "brain_nb.py", root / "brain_nb.py")

patch(root / "config.py", [(
    "    layers_add: int = 1 ",
    "    nb_brain: int = 0                  # NB1: 1 = a small inherited, evolving network scores each option, added to the\n"
    "                                       # hand-written score times an inherited gene g; the habit table is not used\n"
    "    nb_learn: int = 1                  # NB1: with nb_brain, 1 = the network also learns within a life (REINFORCE)\n"
    "    layers_add: int = 1 ")])

patch(root / "person.py", [
    ('''        "kept", "damp", "seen_at", "tried",
    )''',
     '''        "kept", "damp", "seen_at", "tried", "nb",
    )'''),
    ('''        self.tried = None              # CU1: how often p has learned from each action in each situation (only with curiosity_pull)
''',
     '''        self.tried = None              # CU1: how often p has learned from each action in each situation (only with curiosity_pull)
        self.nb = None                 # NB1: the network (genome, working weights, g, learning rate, baseline), with nb_brain
'''),
    ('''            elif k == "tried" and v is None:
                continue                 # CU1: saved only when held, so v8's world is unchanged
''',
     '''            elif k == "tried" and v is None:
                continue                 # CU1: saved only when held, so v8's world is unchanged
            elif k == "nb" and v is None:
                continue                 # NB1: saved only when held, so v17's world is unchanged
'''),
])

patch(root / "mind.py", [(
    '''    options = thought.steer(p, options)
    i = softmax_pick(rng, [o[0] for o in options], c.choice_temperature)
''',
    '''    options = thought.steer(p, options)
    if c.nb_brain:                      # NB1: g x the hand-written score + the network's score
        from . import brain_nb
        options = brain_nb.rescore(world, p, options, near, hunger, fatigue, lw, base)
    i = softmax_pick(rng, [o[0] for o in options], c.choice_temperature)
    if c.nb_brain:
        brain_nb.chosen(world, p, i, [o[0] for o in options], c.choice_temperature)
''')])

patch(root / "biology.py", [
    ('''    r = p.reward + 2.0 * (p.mood - p.mood_before)
    i = p.last_ctx * N_ACTIONS + A[p.last_action]
''',
     '''    r = p.reward + 2.0 * (p.mood - p.mood_before)
    if c.nb_brain:                      # NB1: the network's own learning, from the same feeling
        from . import brain_nb
        brain_nb.learn(world, p, r, c.nb_learn)
    i = p.last_ctx * N_ACTIONS + A[p.last_action]
'''),
    ('''    child.caregiver = mother.id
''',
     '''    child.caregiver = mother.id
    if world.cfg.nb_brain:              # NB1: one parent's network genome, mutated a little
        from . import brain_nb
        child.nb = brain_nb.child(world, mother, father)
'''),
    ('''def die(world, p: Person, cause: str, killer) -> None:
    tick = world.tick
    p.alive = False
''',
     '''def die(world, p: Person, cause: str, killer) -> None:
    tick = world.tick
    p.alive = False
    if world.cfg.nb_brain:              # NB1: the network is dropped at death (nothing reads it again)
        from . import brain_nb
        brain_nb.forget(world, p)
'''),
])

patch(root / "world.py", [(
    '''            p.food = c.founder_food
            self.people[p.id] = p
''',
    '''            p.food = c.founder_food
            if c.nb_brain:              # NB1: a founder's network, random from the world's generator
                from . import brain_nb
                p.nb = brain_nb.founder(self)
            self.people[p.id] = p
''')])
print("patched", root)
