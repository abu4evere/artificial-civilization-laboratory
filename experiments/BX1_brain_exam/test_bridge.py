"""Prove the BX1 bridge works: load a real ACL world, run the new brain's worth map on one person, show where it points.
Exploratory, labelled; nothing frozen. Run from the experiment root."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "code_bx1"))
sys.path.insert(0, str(HERE / "code_bx1" / "acl"))

import numpy as np
from acl.runner import new_world
from acl import brain_bx1 as BX

MBB = HERE / "mbb_seed1.npz"


def main():
    world, hist = new_world(42)
    for _ in range(20):                      # let the world settle so people have moved and seen things
        world.step()
    net = BX.load(str(MBB), seed=1)
    p = next(iter(world.living()))
    v = BX.worth_map(p, world, net)
    m = BX.window(p, world)
    print(f"agent {p.name} at {p.loc}, energy {p.energy:.0f}, curiosity {p.genes.get('curiosity', 1):.2f}")
    print(f"drives (hunger, tired, curiosity) = {BX._levels(p).round(3).tolist()}")
    print(f"window: {int(m[BX.CH_FOOD].sum())} food cells, {int(m[BX.CH_WALL].sum())} wall cells, "
          f"{int(m[BX.CH_UNSEEN].sum())} unseen cells, shelter {int(m[BX.CH_SHELTER].sum())}")
    print(f"worth map: min {v.min():.3f}, max {v.max():.3f}, at the agent (centre) {v[BX.HALF, BX.HALF]:.3f}")
    # where the worth points: the best neighbour move from the centre
    best, ba = v[BX.HALF, BX.HALF], "stay"
    for dx, dy, name in [(-1, 0, "west"), (1, 0, "east"), (0, -1, "north"), (0, 1, "south")]:
        val = v[BX.HALF + dy, BX.HALF + dx]
        if val > best:
            best, ba = val, name
    print(f"the brain's worth is highest toward: {ba} ({best:.3f})")
    # sanity: a food cell should usually be worth more than empty ground
    food = [v[y, x] for y in range(BX.N) for x in range(BX.N) if m[BX.CH_FOOD, y, x] > 0]
    empty = [v[y, x] for y in range(BX.N) for x in range(BX.N)
             if m[BX.CH_FOOD, y, x] == 0 and m[BX.CH_WALL, y, x] == 0]
    if food:
        print(f"mean worth: food cells {np.mean(food):.3f} vs empty ground {np.mean(empty):.3f}")
    print("BRIDGE OK: the new brain read an ACL agent and produced a worth map.")


if __name__ == "__main__":
    main()
