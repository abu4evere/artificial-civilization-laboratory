"""BX1 Phase A (exploratory, labelled): the Mind Lab brain (MoveVIN, MBb) as the "where" for ONE ACL agent.

Not a frozen study and not nature. A quick adapter that lets one tagged person's "where" come from the new brain, so
we can watch it live among old-mind people. The brain was raised in Mind Lab's 15x15 world, so this TRANSLATES ACL into
what it expects (an approximation, named in questions.md):

  - a 15x15 window centred on the agent, 5 channels in Mind Lab's order
    (wall, unseen, food, shelter, staleness), built from what the agent sees and remembers;
  - the agent's body as the brain's 3 drives (hunger, tiredness, curiosity), scaled to Mind Lab's ranges.

The brain plans over the window and gives a worth for every nearby cell; `where_worth` reads the worth at a target tile,
for `mind.decide` to use in place of the hand-written distance pull (for the tagged agent only).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))              # so brain_mv/brains3 import as in Mind Lab
import brain_mv as M                        # noqa: E402

N = M.N                                      # 15
HALF = N // 2                                # 7: the agent sits at the centre
CH_WALL, CH_UNSEEN, CH_FOOD, CH_SHELTER, CH_UNC = range(5)
FOOD_SEEN = 1.0                              # a tile shows "food" when its wild plants are at least this
_BRAINS: dict = {}                           # seed -> loaded MoveVIN (one per agent lineage)


def load(path, seed=1):
    if seed not in _BRAINS:
        import brains3 as B                   # noqa: F401  (registers the numerical settings)
        d = np.load(path)
        net = M.MoveVIN(seed)
        for k in net.p:
            net.p[k] = d[k].copy()
        _BRAINS[seed] = net
    return _BRAINS[seed]


def _levels(p):
    """The agent's body as Mind Lab's 3 drives, scaled to its ranges [0, 1] (approximate; questions.md)."""
    hunger = min(1.0, max(0.0, (100.0 - p.energy) / 100.0))     # low energy -> hungry (E_SET is 150 in Mind Lab)
    tired = 0.0                                                 # ACL has no step-fatigue; the sleep drive is left off
    curiosity = min(1.0, max(0.0, p.genes.get("curiosity", 1.0) / 2.0))
    return np.array([hunger, tired, curiosity], float)


def window(p, world):
    """The 5-channel 15x15 window centred on the agent, in Mind Lab's channel order."""
    c = world.cfg
    m = np.zeros((5, N, N))
    cx, cy = p.loc
    home = p.home()
    for wy in range(N):
        for wx in range(N):
            tx, ty = (cx + wx - HALF) % c.width, (cy + wy - HALF) % c.height
            t = world.tile((tx, ty))
            cheb = max(abs(wx - HALF), abs(wy - HALF))
            seen = cheb <= c.perception
            wall = bool(t.water)                                # a land agent cannot cross water: a "wall"
            m[CH_WALL, wy, wx] = 1.0 if wall else 0.0
            m[CH_UNSEEN, wy, wx] = 0.0 if seen else 1.0
            food = seen and not wall and (t.plants >= FOOD_SEEN or t.crop > 0.0
                                          or any(st[1] > 0 for st in t.stash))
            m[CH_FOOD, wy, wx] = 1.0 if food else 0.0
            m[CH_SHELTER, wy, wx] = 1.0 if (home is not None and (tx, ty) == tuple(home)) else 0.0
            m[CH_UNC, wy, wx] = 0.0 if wall else (1.0 if not seen else 0.0)   # unseen = uncertain; seen = fresh
    return m


def worth_map(p, world, net):
    """The brain's worth for every cell of the window (agent at the centre). 15x15."""
    m = window(p, world)
    fw = net.plan(m[None], _levels(p)[None])
    q = fw[8].reshape(5, -1).T                 # (225, 5): the value of each of the 5 moves at each cell
    return q.reshape(N, N, -1).max(2)          # the best move's value = the cell's worth


def where_worth(p, world, net, target):
    """The brain's worth at an ACL target tile (for mind.decide). None if the tile is outside the window."""
    c = world.cfg
    cx, cy = p.loc
    dx = ((target[0] - cx + c.width // 2) % c.width) - c.width // 2
    dy = ((target[1] - cy + c.height // 2) % c.height) - c.height // 2
    wx, wy = dx + HALF, dy + HALF
    if not (0 <= wx < N and 0 <= wy < N):
        return None
    return float(worth_map(p, world, net)[wy, wx])
