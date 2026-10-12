"""Diagnostic: replay one world and print a state hash after every week, plus which code was imported.

  python tools/ci/replay_trace.py <code dir> <seed> <weeks> [anticipation] [dump week]

Run on two machines and compare the outputs line by line: the first differing week locates where they part.
"""
import hashlib
import json
import sys

sys.path.insert(0, sys.argv[1])
import acl  # noqa: E402
from acl import Config, World  # noqa: E402

print("acl imported from", acl.__file__)
kw = {"seed": int(sys.argv[2])}
if len(sys.argv) > 4:
    kw["anticipation_weight"] = float(sys.argv[4])
w = World(Config(**kw))
print("cfg", hashlib.sha256(json.dumps(w.cfg.to_dict(), sort_keys=True).encode()).hexdigest()[:16])
print("week 0", w.state_hash()[:16])
for wk in range(1, int(sys.argv[3]) + 1):
    w.step()
    print("week", wk, w.state_hash()[:16])
    if len(sys.argv) > 5 and wk in (int(sys.argv[5]) - 1, int(sys.argv[5])):
        with open(f"state_week_{wk}.json", "w", encoding="utf-8") as f:
            json.dump(w.to_dict(), f, sort_keys=True)
