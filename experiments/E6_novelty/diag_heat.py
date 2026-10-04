"""Development check on a development seed: how often people are at a fire, and what they do there."""
import sys
from collections import Counter
sys.path.insert(0, 'code_e6')
from acl.config import Config
from acl.world import World
seed, years = int(sys.argv[1]), int(sys.argv[2])
w = World(Config(seed=seed))
c = Counter()
def spy(world, events):
    for p in world.living():
        if p.age(world.tick) < 16 * 52:
            continue
        if world.tile(p.loc).fire > 0:
            c['adult-weeks at a fire'] += 1
            c[f'  doing there: {p.last_action}'] += 1
            for opt in p.considered:
                if opt[0] in ('heat', 'fill'):
                    c[f'  considered {opt[0]} {opt[1]}'] += 1
    for e in events:
        if e['k'] in ('heat', 'fill') or (e['k'] in ('play', 'make') and e.get('thing') and '^' in e['thing']):
            c[f"EVENT {e['k']} {e.get('thing') or e.get('substance')}"] += 1
        if e['k'] == 'fire':
            c[f"fire {e.get('how')}"] += 1
w.observers.append(spy)
for _ in range(years * 52):
    w.step()
print(len(w.living()), 'alive')
for k, v in sorted(c.items(), key=lambda kv: -kv[1])[:30]:
    print(f'{v:6d}  {k}')
