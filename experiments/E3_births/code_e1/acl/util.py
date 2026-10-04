"""Small helpers: clamping, distance on a world that wraps at the edges, names."""
from __future__ import annotations

import math


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if v < lo else hi if v > hi else v


def torus_delta(a: int, b: int, size: int) -> int:
    """Shortest signed step from a to b on a ring of the given size."""
    d = (b - a) % size
    if d > size // 2:
        d -= size
    return d


def distance(p: tuple, q: tuple, w: int, h: int) -> int:
    """Chebyshev distance on the torus: diagonal steps count as one."""
    return max(abs(torus_delta(p[0], q[0], w)), abs(torus_delta(p[1], q[1], h)))


def step_toward(p: tuple, q: tuple, steps: int, w: int, h: int) -> tuple:
    dx = torus_delta(p[0], q[0], w)
    dy = torus_delta(p[1], q[1], h)
    mx = max(-steps, min(steps, dx))
    my = max(-steps, min(steps, dy))
    return ((p[0] + mx) % w, (p[1] + my) % h)


def step_away(p: tuple, q: tuple, steps: int, w: int, h: int) -> tuple:
    dx = torus_delta(p[0], q[0], w)
    dy = torus_delta(p[1], q[1], h)
    sx = -1 if dx > 0 else 1 if dx < 0 else 0
    sy = -1 if dy > 0 else 1 if dy < 0 else 0
    if sx == 0 and sy == 0:
        sx = 1
    return ((p[0] + sx * steps) % w, (p[1] + sy * steps) % h)


def softmax_pick(rng, scores: list, temperature: float) -> int:
    top = max(scores)
    weights = [math.exp((s - top) / temperature) for s in scores]
    r = rng.random() * sum(weights)
    for i, w in enumerate(weights):
        r -= w
        if r <= 0:
            return i
    return len(weights) - 1


_ONSETS = ("b", "d", "g", "h", "k", "l", "m", "n", "r", "s", "t", "v", "y", "z", "sh", "th")
_VOWELS = ("a", "e", "i", "o", "u", "ai", "ei", "ou")
_CODAS = ("", "", "", "n", "l", "r", "m", "k", "s")


def make_name(rng) -> str:
    parts = []
    for _ in range(rng.choice((2, 2, 3))):
        parts.append(rng.choice(_ONSETS) + rng.choice(_VOWELS))
    parts.append(rng.choice(_CODAS))
    return "".join(parts).capitalize()
