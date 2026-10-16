"""SA1-F Part B: ACL's side of the sight and range ratios, measured on the control code (as SA1). Read-only: an observer
that reads the world after each week, draws no random numbers and writes nothing (checked: final state hash identical
with and without it, on the first seed).

For every adult or elder each week (pooled over worlds and weeks):
  - how far they are from where they were the week before (Chebyshev tiles, as ACL measures distance);
  - how many other living people are within sight (`perception`, 4) and within reach (`reach`, 3).

  python experiments/SA1_sensitivity/acl_ratios.py          # 16 of F1's seeds, 60 years; writes acl_ratios.json
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_sa1 as S  # noqa: E402

SEEDS = tuple(range(501, 517))
YEARS = 60


class Obs:
    def __init__(self):
        self.last = {}
        self.move, self.see, self.near = [], [], []

    def __call__(self, world, events):
        from acl.util import distance
        c = world.cfg
        now = {}
        for p in world.living():
            if p.stage(world.tick) not in ("adult", "elder"):
                continue
            now[p.id] = p.loc
            if p.id in self.last:
                self.move.append(distance(self.last[p.id], p.loc, c.width, c.height))
            self.see.append(len(world.people_near(p.loc, c.perception, exclude=p.id)))
            self.near.append(len(world.people_near(p.loc, c.reach, exclude=p.id)))
        self.last = now


def run(seed, observe=True):
    w = S.make_world(seed)
    o = Obs()
    if observe:
        w.observers.append(o)
    for _ in range(YEARS * S.WPY):
        w.step()
        if not w.living():
            break
    return o, w


def summary(xs):
    xs = sorted(xs)
    qs = statistics.quantiles(xs, n=4)
    return {"mean": round(statistics.fmean(xs), 3), "median": statistics.median(xs), "q1": qs[0], "q3": qs[2], "n": len(xs)}


def main():
    S.setup()
    o0, w0 = run(SEEDS[0], observe=True)
    _, w1 = run(SEEDS[0], observe=False)
    assert S.world_hash(w0) == S.world_hash(w1), "the observer changed the world"
    move, see, near = list(o0.move), list(o0.see), list(o0.near)
    for s in SEEDS[1:]:
        o, _ = run(s)
        move += o.move
        see += o.see
        near += o.near
        print(f"seed {s} done", flush=True)
    res = {"seeds": list(SEEDS), "years": YEARS, "code": "code_e13r (control, anticipation_weight 1.0)",
           "observer_read_only": True,
           "weekly_move_tiles": summary(move), "share_weeks_not_moved": round(sum(1 for m in move if m == 0) / len(move), 3),
           "share_weeks_moved_full_reach": round(sum(1 for m in move if m >= 3) / len(move), 3),
           "others_within_sight": summary(see), "others_within_reach": summary(near)}
    (HERE / "acl_ratios.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
