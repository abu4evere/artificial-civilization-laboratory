"""The shape of the land: oceans, coasts, rivers, lakes, plains, forests, hills,
mountains, deserts and tundra.

The land is raised from smoothed seeded noise and sinks into ocean toward the
edges, so it is a stretch of continent and islands with sea all round. The
north is colder and the south warmer, and high ground is colder still. Rivers
run downhill from wet high ground to the sea or into lakes.

Each kind of land has its own physics:
- how fertile it is;
- how much wood and stone it holds;
- how many animals it can feed;
- how hard it is to cross;
- how cold it gets.

Nobody can walk on sea or lake water. Rivers can be waded.
"""
from __future__ import annotations

from .util import clamp

BIOMES = ("deep", "sea", "lake", "beach", "plains", "forest", "woods", "hills",
          "mountain", "snow", "desert", "tundra", "river")
WATER = ("deep", "sea", "lake")

#            fertility forest rock wildness cost
PHYSICS = {
    "deep":     (0.00, 0.00, 0.0, 0.2, 99),
    "sea":      (0.00, 0.00, 0.0, 0.6, 99),
    "lake":     (0.00, 0.00, 0.0, 0.6, 99),
    "beach":    (0.15, 0.03, 0.3, 0.2, 1.0),
    "plains":   (0.70, 0.12, 0.12, 0.75, 1.0),
    "forest":   (0.50, 0.75, 0.15, 0.80, 1.2),
    "woods":    (0.40, 1.00, 0.15, 0.70, 1.5),
    "hills":    (0.40, 0.30, 0.65, 0.55, 1.6),
    "mountain": (0.08, 0.10, 1.00, 0.30, 2.5),
    "snow":     (0.02, 0.00, 0.80, 0.10, 3.0),
    "desert":   (0.08, 0.02, 0.40, 0.15, 1.4),
    "tundra":   (0.22, 0.10, 0.30, 0.45, 1.2),
    "river":    (0.90, 0.30, 0.20, 0.65, 1.3),
}


def _smooth(rng, w: int, h: int, passes: int) -> list:
    g = [[rng.random() for _ in range(w)] for _ in range(h)]
    for _ in range(passes):
        n = [[0.0] * w for _ in range(h)]
        for y in range(h):
            for x in range(w):
                s = 0.0
                for dy in (-1, 0, 1):
                    row = g[(y + dy) % h]
                    for dx in (-1, 0, 1):
                        s += row[(x + dx) % w]
                n[y][x] = s / 9.0
        g = n
    flat = [v for row in g for v in row]
    lo, hi = min(flat), max(flat)
    return [[(v - lo) / (hi - lo) for v in row] for row in g]


def _islands(cells, w: int, h: int) -> list:
    """Connected stretches of not-yet-water land (8-adjacency), each a list of (x, y)."""
    seen = set()
    out = []
    for y in range(h):
        for x in range(w):
            if (x, y) in seen or cells[y][x]["biome"] in WATER:
                continue
            comp, stack = [], [(x, y)]
            seen.add((x, y))
            while stack:
                cx, cy = stack.pop()
                comp.append((cx, cy))
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        n = ((cx + dx) % w, (cy + dy) % h)
                        if n not in seen and cells[n[1]][n[0]]["biome"] not in WATER:
                            seen.add(n)
                            stack.append(n)
            out.append(sorted(comp))
    return out


def generate(rng, w: int, h: int) -> list:
    """A grid of land descriptions: [[{biome, height, temp, moisture, fertility, forest, rock, wildness, cost, flinty}]]."""
    big, mid, small = _smooth(rng, w, h, 9), _smooth(rng, w, h, 4), _smooth(rng, w, h, 1)
    wet, warm = _smooth(rng, w, h, 5), _smooth(rng, w, h, 3)
    # An archipelago: land rises around a handful of island centres and sinks
    # between them, so bands can begin far apart and meet only by crossing sea.
    n_islands = max(4, (w * h) // 300)
    centres = []
    for _ in range(400):
        if len(centres) >= n_islands:
            break
        cx, cy = rng.uniform(0, w), rng.uniform(0, h)
        far = all(min(abs(cx - x), w - abs(cx - x)) ** 2 + min(abs(cy - y), h - abs(cy - y)) ** 2
                  > (max(w, h) / 3.0) ** 2 for x, y in centres)
        if far:
            centres.append((cx, cy))
    while len(centres) < n_islands:
        centres.append((rng.uniform(0, w), rng.uniform(0, h)))

    radius = max(w, h) / 6.0
    height = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            best = 1e9
            for cx, cy in centres:
                dx = min(abs(x - cx), w - abs(x - cx))
                dy = min(abs(y - cy), h - abs(y - cy))
                best = min(best, (dx * dx + dy * dy) ** 0.5)
            island = max(0.0, 1.0 - best / radius)
            noise = 0.5 * big[y][x] + 0.3 * mid[y][x] + 0.2 * small[y][x]
            height[y][x] = island * (0.35 + 0.65 * noise) - 0.22 * (1.0 - island)
    flat = sorted(v for row in height for v in row)
    sea = flat[int(len(flat) * 0.60)]
    top = flat[-1]

    def elev(x, y):
        return (height[y][x] - sea) / max(1e-6, top - sea)

    cells = [[None] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            e = elev(x, y)
            temp = clamp(0.2 + 0.6 * (y + 0.5) / h + 0.2 * (warm[y][x] - 0.5) - 0.45 * max(0.0, e))
            cells[y][x] = {"height": round(height[y][x], 4), "elev": e, "temp": round(temp, 3),
                           "moisture": wet[y][x], "biome": None}
    # Water first.
    for y in range(h):
        for x in range(w):
            c = cells[y][x]
            if c["elev"] < -0.25:
                c["biome"] = "deep"
            elif c["elev"] < 0:
                c["biome"] = "sea"
    # Rivers run downhill from wet high ground until they reach water or a hollow, which becomes a lake.
    def run_river(sx, sy) -> bool:
        x, y, path = sx, sy, []
        for _ in range(w + h):
            path.append((x, y))
            best, best_h = None, height[y][x]
            for ddx in (-1, 0, 1):
                for ddy in (-1, 0, 1):
                    nx, ny = (x + ddx) % w, (y + ddy) % h
                    if (ddx or ddy) and height[ny][nx] < best_h:
                        best, best_h = (nx, ny), height[ny][nx]
            if best is None:                       # a hollow: the river pools into a lake
                cells[y][x]["biome"] = "lake"
                break
            x, y = best
            if cells[y][x]["biome"] in WATER:
                break
        if len(path) < 3:
            return False
        for px, py in path:
            if cells[py][px]["biome"] is None and cells[py][px]["elev"] < 0.8:
                cells[py][px]["biome"] = "river"
        return True

    sources = [(x, y) for y in range(h) for x in range(w)
               if 0.3 < cells[y][x]["elev"] < 0.85 and cells[y][x]["moisture"] > 0.45]
    rng.shuffle(sources)
    rivers = 0
    for sx, sy in sources:
        if rivers >= max(4, (w * h) // 100):
            break
        if cells[sy][sx]["biome"] is None and run_river(sx, sy):
            rivers += 1
    # Every island big enough to live on has some fresh water: a stream from its highest wet ground.
    for comp in _islands(cells, w, h):
        if len(comp) < 12 or any(cells[y][x]["biome"] in ("river", "lake") for x, y in comp):
            continue
        top = max(comp, key=lambda c: (cells[c[1]][c[0]]["elev"] + 0.3 * cells[c[1]][c[0]]["moisture"], c))
        if not run_river(*top):
            cells[top[1]][top[0]]["biome"] = "lake"     # a spring-fed pond
    # Land.
    for y in range(h):
        for x in range(w):
            c = cells[y][x]
            if c["biome"]:
                continue
            e, t, m = c["elev"], c["temp"], c["moisture"]
            near_sea = any(cells[(y + dy) % h][(x + dx) % w]["biome"] in ("sea", "deep")
                           for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if e > 0.8 or (e > 0.62 and t < 0.3):
                c["biome"] = "snow"
            elif e > 0.62:
                c["biome"] = "mountain"
            elif e > 0.45:
                c["biome"] = "hills"
            elif near_sea and e < 0.12:
                c["biome"] = "beach"
            elif t > 0.68 and m < 0.42:
                c["biome"] = "desert"
            elif t < 0.3:
                c["biome"] = "tundra"
            elif m > 0.66:
                c["biome"] = "woods"
            elif m > 0.5:
                c["biome"] = "forest"
            else:
                c["biome"] = "plains"
    # Physical properties, with a little variety within each kind of land.
    for y in range(h):
        for x in range(w):
            c = cells[y][x]
            fert, forest, rock, wild, cost = PHYSICS[c["biome"]]
            jitter = (rng.random() - 0.5) * 0.2
            c["fertility"] = round(clamp(fert + jitter * (fert > 0)), 4) if fert > 0 else 0.0
            c["forest"] = round(clamp(forest + (rng.random() - 0.5) * 0.2), 4) if forest > 0 else 0.0
            c["rock"] = round(clamp(rock + (rng.random() - 0.5) * 0.2), 4)
            c["wildness"] = round(clamp(wild + (rng.random() - 0.5) * 0.2), 4)
            c["cost"] = cost
            c["flinty"] = c["biome"] in ("hills", "mountain", "beach", "desert") and rng.random() < 0.45
            del c["elev"]
    return cells
