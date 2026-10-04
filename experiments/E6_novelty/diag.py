"""Quick look at whether the new physics is used (development check, not part of the experiment)."""
import sys, time
from collections import Counter
sys.path.insert(0, 'code_e6'); sys.path.insert(1, '.')
from acl.config import Config
from acl.world import World
from acl.historian import Historian
from acl.measure import Lab
from acl.matter import MATERIALS
from novelty import Novelty
seed = int(sys.argv[1]); years = int(sys.argv[2])
w = World(Config(seed=seed)); h = Historian(); lab = Lab(h); rec = Novelty(10, MATERIALS)
ev = Counter(); made = Counter()
def spy(world, events):
    for e in events:
        k = e['k']
        if k in ('heat', 'fill', 'consequence', 'fire'):
            ev[(k, e.get('substance') or e.get('what') or e.get('how') or e.get('thing'))] += 1
        if k in ('play', 'make') and e.get('thing') and ('~' in e['thing'] or '^' in e['thing']):
            made[(k, e['thing'])] += 1
        if k == 'gather' and e.get('kind') in ('clay', 'char'):
            ev[('gather', e['kind'])] += 1
w.observers += [h, lab, rec, spy]
t0 = time.time()
for y in range(years):
    for _ in range(52): w.step()
    if (y+1) % 25 == 0:
        print(f'year {y+1}: {len(w.living())} alive', flush=True)
    if not w.living(): break
print('seconds', round(time.time()-t0))
for k, v in sorted(ev.items(), key=lambda kv: -kv[1]): print(' ', k, v)
for k, v in made.most_common(15): print('  made', k, v)
res = rec.results(w)
print('lasting', res['lasting'], 'LFA', res['LFA'], 'share>100', res['share_after_100'])
print('kept food now', round(sum(p.kept for p in w.living()),1), 'food', round(sum(p.food for p in w.living()),1))
print('holders', [(it['sig'], it['holds']) for p in w.living() for it in p.items if it.get('holds')][:8])
