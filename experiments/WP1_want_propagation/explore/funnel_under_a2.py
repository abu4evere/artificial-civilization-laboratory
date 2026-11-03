"""WP1 follow-up, exploratory (outside any frozen plan): where do new kinds stop under A2? Runs one world of the copy
(code_wp1, want_propagation 2, seed 22201) to year 130 with UP1's make-choice funnel observer and compares the shares
for kinds invented from year 100 with UP1's v11 result. Read-only on a copy; live nature is untouched. Under A2 the
make choice uses `_wanted_parts_deep` and never calls `_wanted_parts`, so the observer's reproduction is pointed at
the deep version (its mismatch counter must stay 0).

  python experiments/WP1_want_propagation/explore/funnel_under_a2.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "UP1_uptake_of_new_kinds"))
import run_up1 as U  # noqa: E402

U.base.CODES["wp1"] = HERE.parent / "code_wp1"
U.base.setup("wp1")
import acl.mind as mind  # noqa: E402
mind._wanted_parts = mind._wanted_parts_deep        # A2 never calls the one-level version; the observer imports it
U.LATE[0], U.LATE[1] = 100 * 52, 130 * 52
w = U.base.make_world(22201, {**U.base.LP, "want_propagation": 2})
obs = U.UP1Obs(w)
U.install(w, obs)
w.observers.append(obs)
for _ in range(130 * 52):
    w.step()
r = obs.results()
tot = {}
for k, v in r["steps"].items():
    c = k.split("|")[0]
    tot[c] = [a + b for a, b in zip(tot.get(c, [0] * 7), v)]
out = {"mismatch": r["mismatch"], "new_kinds": len(r["per_kind"]),
       "shares": {c: {s: round(x / sum(v), 4) for s, x in zip(U.STEPS, v)} for c, v in tot.items() if sum(v)},
       "counts": tot, "p5": r["p5"], "winner": r["winner"]}
(HERE / "funnel_under_a2.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out))
