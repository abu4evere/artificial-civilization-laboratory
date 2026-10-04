"""Development check: survival and fire under the baseline code and the E6 code, on development seeds."""
import subprocess, sys
CODE = r'''
import sys
sys.path.insert(0, CODEDIR)
from acl.config import Config
from acl.world import World
w = World(Config(seed=SEED)); pops = []; fires = 0; at_fire = 0
for y in range(150):
    for _ in range(52):
        w.step()
        fires += sum(1 for e in w.events if e["k"] == "fire")
        at_fire += sum(1 for p in w.living() if w.tile(p.loc).fire > 0)
    if (y + 1) % 50 == 0: pops.append(len(w.living()))
    if not w.living(): pops.append(0); break
print(CODEDIR.split("/")[-1], SEED, "pop at 50/100/150:", pops, "fires:", fires, "person-weeks at a fire:", at_fire, flush=True)
'''
for seed in (901, 902, 903, 904):
    for code in ("code_baseline", "code_e6"):
        src = CODE.replace("CODEDIR", repr(code)).replace("SEED", str(seed))
        subprocess.run([sys.executable, "-c", src])
