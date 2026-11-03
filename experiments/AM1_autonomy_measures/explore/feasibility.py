import sys
sys.path.insert(0, r"D:\acl\experiments\AM1_autonomy_measures")
import run_am1 as R
R.base.setup(R.CODE)
temp, seed = float(sys.argv[1]), int(sys.argv[2])
kw = {**R.base.LP} if temp == 0.2 else {**R.base.LP, "choice_temperature": temp}
w = R.base.make_world(seed, kw)
lw = 0
for _ in range(int(sys.argv[3]) * R.WPY):
    w.step()
    lw += len(w.living())
    if not w.living():
        break
print(temp, seed, lw, len(w.living()), w.tick)
