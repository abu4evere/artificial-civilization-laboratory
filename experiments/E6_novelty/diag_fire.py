"""Development check: where fire-making stops (not part of the experiment)."""
import sys
from collections import Counter
code = sys.argv[1]; seed = int(sys.argv[2]); years = int(sys.argv[3])
sys.path.insert(0, code)
from acl import actions, matter
from acl.config import Config
from acl.world import World
c = Counter()
orig_spark = actions._spark
def spy_spark(world, p):
    tile = world.tile(p.loc)
    c['spark_check'] += 1
    if tile.fire > 0: c['already_fire'] += 1
    c['pile_tinder' if tile.pile.get('fiber', 0) + tile.pile.get('wood', 0) >= 0.5 else 'no_pile_tinder'] += 1
    c['carry_fiber' if p.mats['fiber'] >= 1 else 'no_fiber'] += 1
    if hasattr(p, 'damp') and p.damp.get('fiber', 0) > 3: c['fiber_wet'] += 1
    r = orig_spark(world, p)
    c['lit' if r else 'not_lit'] += 1
    return r
actions._spark = spy_spark
orig_strike = matter.strike
def spy_strike(target, hammer, skill, rng):
    out = orig_strike(target, hammer, skill, rng)
    c[f'strike {target}/{hammer} ' + ('ok' if out else 'none')] += 1
    return out
matter.strike = spy_strike
w = World(Config(seed=seed))
for y in range(years):
    for _ in range(52): w.step()
for k, v in sorted(c.items()): print(f'  {k}: {v}')
