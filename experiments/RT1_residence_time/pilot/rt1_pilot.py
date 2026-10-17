import sys, statistics
code, rw, seed, years = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
sys.path.insert(0, code)
from acl import Config, World
from acl.util import distance
kw = dict(seed=seed, anticipation_weight=1.0, loved_location='last_seen', corner_block=1, ashore_if_float_breaks=1, knowledge_copy=1)
if rw: kw['residence_weeks'] = rw
w = World(Config(**kw)); c = w.cfg
hist = {}; moved = n = 0
for t in range(years * 52):
    w.step()
    for p in w.living():
        if p.age(w.tick) >= 16 * 52:
            h = hist.setdefault(p.id, [])
            if h: n += 1; moved += h[-1] != p.loc
            h.append(p.loc)
month = [distance(h[i], h[i + 4], c.width, c.height) for h in hist.values() for i in range(0, len(h) - 4, 4)]
print(f"rw={rw} seed={seed}: moved share {moved / n:.3f}; distance a month mean {statistics.fmean(month):.2f} tiles (n={len(month)}); alive {len(w.living())}")
