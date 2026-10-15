"""NV2 zero-check follow-up (read-only): find control worlds where a stranding happens (ST1's definition: an adult or
unaccompanied person ends a week on water with nothing that floats), then check that the ST1 switch alone changes them.
  python experiments/NV2_nature_v2/st1_probe.py SEED [SEED ...]
"""
import json, sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_nv2 as R

def strandings(seed, years, kw):
    R.setup("v2")
    w = R.make_world(seed, kw)
    first = None
    for wk in range(years * 52):
        w.step()
        for p in w.living():
            if w.tile(p.loc).water and not w.passable(p, p.loc):
                carer = w.people.get(p.caregiver) if p.caregiver else None
                if carer and carer.alive and carer.loc == p.loc and w.passable(carer, carer.loc):
                    continue                     # a child in the carer's boat (intended)
                first = first if first is not None else wk + 1
        if not w.living():
            break
    return first, R.world_hash(w)

if __name__ == "__main__":
    for s in map(int, sys.argv[1:]):
        f1, h1 = strandings(s, 30, {})
        if f1 is None:
            print(s, "no stranding in 30 years under v1", flush=True)
            continue
        f2, h2 = strandings(s, 30, {"ashore_if_float_breaks": 1})
        print(s, f"v1: first stranding in week {f1}; ST1 alone: strandings {'none' if f2 is None else 'from week ' + str(f2)}; "
                 f"world differs from v1: {h1 != h2}", flush=True)
