"""E6 follow-up (read-only, from saved snapshots): was the new physics used, and what killed the worlds?"""
import gzip, json, sys
from collections import Counter
from pathlib import Path
HERE = Path(__file__).parent
for arm in ('e6', 'baseline'):
    print('=====', arm)
    for s in range(301, 309):
        snaps = sorted((HERE / 'output' / arm).glob(f'seed_{s}_*.json.gz'), key=lambda f: f.stat().st_mtime)
        if not snaps:
            continue
        d = json.loads(gzip.open(snaps[-1]).read())
        W = d['world']
        know = W['knowledge']
        shaped = [k for k in know if '~' in k]
        heated = [k for k in know if '^' in k]
        def holds_water(pr, scale):
            return pr and pr.get('contain', 0) >= 0.4 * scale and pr.get('tight', 0) >= 0.5 * scale
        water = [k for k, r in know.items() if holds_water(r.get('props'), 100)] if arm == 'e6' else []
        people = W['people']
        plist = people.values() if isinstance(people, dict) else people
        causes = Counter(p['death_cause'] for p in plist if not p['alive'] and p.get('death_cause'))
        tot = sum(causes.values())
        kept = sum(p.get('kept', 0) for p in plist if p['alive'])
        print(f"seed {s}: ever made {len(know)} kinds | shaped {len(shaped)} | heated {len(heated)} {heated[:3]} | "
              f"could hold water {len(water)} {water[:2]} | kept food now {kept:.0f}")
        print('     deaths:', tot, [(k, round(100 * v / tot)) for k, v in causes.most_common(5)])
