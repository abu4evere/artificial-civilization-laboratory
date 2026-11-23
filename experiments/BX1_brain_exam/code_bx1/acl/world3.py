"""W3's world (questions.md, W3-frozen): a 15 x 15 land with walls, 3 food patches that relocate twice per life,
1 shelter, a body (energy, fatigue), the 3 x 3 view, and the remembered map (a fixed writer, as W2).

Actions: 0 north (y-1), 1 south (y+1), 2 east (x+1), 3 west (x-1), 4 stay. Cells are (x, y); arrays are [y, x].
"""
from __future__ import annotations

import math
from collections import deque

import numpy as np

N = 15
MOVES = [(0, -1), (0, 1), (1, 0), (-1, 0), (0, 0)]
E0, EMAX, E_SET, MEAL = 150, 200, 150, 30
F_SHELTER, F_TIRED, F_CAP = 10, 100, 200
LIFE = 3000
TAU = 200.0
REL_LO, REL_HI, REL_GAP, REL_FAR = 500, 2700, 400, 5
FIND_WINDOW = 300
CAL_SEEDS = range(800001, 800051)
TEST_SEEDS = range(900001, 900051)
R_LIST = (400, 200, 100, 50, 25)
# the planner's channels
CH_WALL, CH_UNSEEN, CH_FOOD, CH_SHELTER, CH_UNC = range(5)
C = 5


def train_seed(run_seed, life):
    return 1000 * run_seed + life


def _connected(walls):
    open_cells = [(x, y) for y in range(N) for x in range(N) if not walls[y, x]]
    if not open_cells:
        return False
    seen = {open_cells[0]}
    q = deque([open_cells[0]])
    while q:
        x, y = q.popleft()
        for dx, dy in MOVES[:4]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N and not walls[ny, nx] and (nx, ny) not in seen:
                seen.add((nx, ny))
                q.append((nx, ny))
    return len(seen) == len(open_cells)


def _blocks(walls, taken):
    """All 2 x 2 blocks of open cells whose cells are not in `taken` (top-left corners)."""
    out = []
    for y in range(1, N - 2):
        for x in range(1, N - 2):
            cells = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
            if all(not walls[cy, cx] and (cx, cy) not in taken for cx, cy in cells):
                out.append((x, y))
    return out


def block_cells(corner):
    x, y = corner
    return [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]


def make_land(seed):
    """The land and its relocation schedule, from its seed alone."""
    rng = np.random.default_rng(seed)
    while True:
        walls = np.zeros((N, N), bool)
        walls[0, :] = walls[-1, :] = walls[:, 0] = walls[:, -1] = True
        for _ in range(4):
            length = int(rng.integers(3, 7))
            horiz = bool(rng.integers(0, 2))
            x, y = int(rng.integers(1, N - 1)), int(rng.integers(1, N - 1))
            for k in range(length):
                cx, cy = (x + k, y) if horiz else (x, y + k)
                if 1 <= cx < N - 1 and 1 <= cy < N - 1:
                    walls[cy, cx] = True
        if not _connected(walls):
            continue
        open_cells = [(x, y) for y in range(N) for x in range(N) if not walls[y, x]]
        shelter = open_cells[int(rng.integers(len(open_cells)))]
        patches, taken = [], {shelter}
        ok = True
        for _ in range(3):
            cand = _blocks(walls, taken)
            if not cand:
                ok = False
                break
            c = cand[int(rng.integers(len(cand)))]
            patches.append(c)
            taken |= set(block_cells(c))
        if not ok:
            continue
        free = [c for c in open_cells if c not in taken]
        start = free[int(rng.integers(len(free)))]
        # relocations: each patch twice, in [REL_LO, REL_HI], at least REL_GAP apart
        sched = []
        for i in range(3):
            while True:
                t1, t2 = sorted(int(t) for t in rng.integers(REL_LO, REL_HI + 1, size=2))
                if t2 - t1 >= REL_GAP:
                    break
            sched += [(t1, i), (t2, i)]
        sched.sort()
        reloc_rng_seed = int(rng.integers(0, 2**31 - 1))
        return {"walls": walls, "shelter": shelter, "patches": patches, "start": start, "sched": sched,
                "reloc_seed": reloc_rng_seed, "seed": seed}


class World:
    """One life on one land. The brain sees only obs() (the map memory and its body); the world keeps the truth."""

    def __init__(self, land, R):
        self.land, self.R = land, R
        self.walls = land["walls"]
        self.shelter = land["shelter"]
        self.patches = list(land["patches"])
        self.food = {}                                    # cell -> step at which it is full again (<= t: full)
        for c in self.patches:
            for cell in block_cells(c):
                self.food[cell] = 0
        self.pos = land["start"]
        self.E, self.F, self.t = float(E0), 0.0, 0
        self.dead = False
        self.sched = list(land["sched"])
        self.reloc_rng = np.random.default_rng(land["reloc_seed"])
        self.events = []                                  # [step, patch index, new corner, found step or None]
        # the map memory (the fixed writer)
        self.m_wall = np.zeros((N, N), bool)
        self.m_seen = np.zeros((N, N), bool)
        self.m_food = np.zeros((N, N), bool)
        self.m_shelter = np.zeros((N, N), bool)
        self.m_last = np.full((N, N), -1, int)
        self.write_view()

    # --- the truth ---------------------------------------------------------------------------------------------
    def food_full(self, cell):
        return cell in self.food and self.food[cell] <= self.t

    def view_cells(self):
        x, y = self.pos
        return [(x + dx, y + dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if 0 <= x + dx < N and 0 <= y + dy < N]

    def write_view(self):
        """The fixed writer: only cells in the 3 x 3 view are written."""
        for cx, cy in self.view_cells():
            self.m_seen[cy, cx] = True
            self.m_wall[cy, cx] = bool(self.walls[cy, cx])
            self.m_food[cy, cx] = self.food_full((cx, cy))
            self.m_shelter[cy, cx] = (cx, cy) == self.shelter
            self.m_last[cy, cx] = self.t
        for ev in self.events:                            # a relocation is found when any new cell is in view
            if ev[3] is None and self.t - ev[0] <= FIND_WINDOW:
                if any(c in set(self.view_cells()) for c in block_cells(ev[2])):
                    ev[3] = self.t

    def uncertainty(self):
        u = np.ones((N, N))
        seen = self.m_seen
        age = self.t - self.m_last
        u[seen] = 1.0 - np.exp(-age[seen] / TAU)
        u[self.m_wall] = 0.0
        return u

    def curiosity_level(self):
        u = self.uncertainty()
        return float(u[~self.m_wall].mean())

    def deficits(self):
        s = max(0.0, E_SET - self.E) / E_SET
        f = min(self.F, F_CAP) / F_CAP
        return s, f

    def drive(self):
        s, f = self.deficits()
        return s * s + f * f

    def obs_map(self):
        """The planner's 5 channels from the map memory only."""
        m = np.zeros((C, N, N))
        m[CH_WALL] = self.m_wall
        m[CH_UNSEEN] = ~self.m_seen
        m[CH_FOOD] = self.m_food
        m[CH_SHELTER] = self.m_shelter
        m[CH_UNC] = self.uncertainty()
        return m

    def relocate(self, i):
        old = self.patches[i]
        for cell in block_cells(old):
            self.food.pop(cell, None)
        taken = {self.shelter}
        for j, c in enumerate(self.patches):
            if j != i:
                taken |= set(block_cells(c))
        cand = [c for c in _blocks(self.walls, taken)
                if abs(c[0] - old[0]) + abs(c[1] - old[1]) >= REL_FAR and self.pos not in block_cells(c)]
        new = cand[int(self.reloc_rng.integers(len(cand)))]
        self.patches[i] = new
        for cell in block_cells(new):
            self.food[cell] = self.t
        self.events.append([self.t, i, new, None])

    def step(self, a):
        """One step. Returns (curiosity sum of u over the new view before the update, ate)."""
        dx, dy = MOVES[a]
        nx, ny = self.pos[0] + dx, self.pos[1] + dy
        moved = False
        if a != 4 and not self.walls[ny, nx]:
            self.pos, moved = (nx, ny), True
        self.E -= 2.0 if (moved and self.F > F_TIRED) else 1.0
        if self.pos == self.shelter:
            self.F = max(0.0, self.F - F_SHELTER)
        else:
            self.F += 1.0
        self.t += 1
        while self.sched and self.sched[0][0] == self.t:
            _, i = self.sched.pop(0)
            self.relocate(i)
        ate = False
        if self.food_full(self.pos) and self.E < EMAX:
            self.E = min(EMAX, self.E + MEAL)
            self.food[self.pos] = self.t + self.R
            ate = True
        u = self.uncertainty()
        cur = float(sum(u[cy, cx] for cx, cy in self.view_cells()))
        self.write_view()
        if self.E <= 0:
            self.dead = True
        return cur, ate

    def done(self):
        return self.dead or self.t >= LIFE

    def land_known(self):
        return float(self.m_seen[~self.walls].mean())


def bfs_path(passable, start, goals):
    """Shortest path on the map memory; passable(cell) -> bool; returns the first action, or None."""
    goals = set(goals)
    if not goals:
        return None
    if start in goals:
        return 4
    prev = {start: None}
    q = deque([start])
    while q:
        c = q.popleft()
        if c in goals:
            while prev[c] != start:
                c = prev[c]
            d = (c[0] - start[0], c[1] - start[1])
            return MOVES.index(d)
        for dx, dy in MOVES[:4]:
            n = (c[0] + dx, c[1] + dy)
            if 0 <= n[0] < N and 0 <= n[1] < N and n not in prev and passable(n):
                prev[n] = c
                q.append(n)
    return None


def reachable(passable, start):
    """Cells reachable from start on the map memory (unknown cells count as open)."""
    seen = {start}
    q = deque([start])
    while q:
        c = q.popleft()
        for dx, dy in MOVES[:4]:
            n = (c[0] + dx, c[1] + dy)
            if 0 <= n[0] < N and 0 <= n[1] < N and n not in seen and passable(n):
                seen.add(n)
                q.append(n)
    return seen


class Script:
    """The ceiling: reads only the map memory and its own body (questions.md)."""

    def __init__(self):
        self.resting = False

    def act(self, mem):
        """mem: a MapView (map memory, body and position only)."""
        pos = mem.pos

        def passable(c):
            return not mem.m_wall[c[1], c[0]]

        reach = reachable(passable, pos)
        if mem.F == 0:
            self.resting = False
        if self.resting and pos == mem.shelter_known:
            return 4
        if mem.E < 120:
            foods = [(x, y) for y in range(N) for x in range(N) if mem.m_food[y, x]]
            a = bfs_path(passable, pos, foods)
            if a is not None:
                return a
            # pre-data correction 1 (IMPLEMENTATION.md): hungry with no food remembered -> search the stalest open cell
            u = mem.u
            cand = [(x, y) for y in range(N) for x in range(N)
                    if (x, y) in reach and (x, y) != pos and u[y, x] > 0]
            if cand:
                best = max(u[y, x] for x, y in cand)
                a = bfs_path(passable, pos, [(x, y) for x, y in cand if u[y, x] >= best - 1e-9])
                if a is not None:
                    return a
        if mem.F > 80 and mem.shelter_known is not None:
            self.resting = True
            a = bfs_path(passable, pos, [mem.shelter_known])
            if a is not None:
                return a
        unseen = [(x, y) for y in range(N) for x in range(N) if not mem.m_seen[y, x] and (x, y) in reach]
        a = bfs_path(passable, pos, unseen) if unseen else None
        if a is not None and a != 4:
            return a
        u = mem.u
        stale = [(x, y) for y in range(N) for x in range(N) if u[y, x] >= 0.5 and (x, y) != pos and (x, y) in reach]
        if stale:
            best = max(u[y, x] for x, y in stale)
            a = bfs_path(passable, pos, [(x, y) for x, y in stale if u[y, x] >= best - 1e-9])
            if a is not None:
                return a
        return 4


class MapView:
    """What Script may read: the map memory, its own body and position, nothing of the world's truth."""

    def __init__(self, w: World):
        self.pos, self.E, self.F = w.pos, w.E, w.F
        self.m_wall, self.m_seen, self.m_food = w.m_wall.copy(), w.m_seen.copy(), w.m_food.copy()
        ys, xs = np.nonzero(w.m_shelter)
        self.shelter_known = (int(xs[0]), int(ys[0])) if len(xs) else None
        self.u = w.uncertainty()


def life_measures(w: World):
    """The per-life measures (questions.md, Test)."""
    events = w.events
    found = [1.0 if (ev[3] is not None and ev[3] - ev[0] <= FIND_WINDOW) else 0.0 for ev in events]
    return {"survived": float(w.t >= LIFE and not w.dead), "lifespan": w.t,
            "events": len(events), "found_share": (sum(found) / len(found)) if found else math.nan}
