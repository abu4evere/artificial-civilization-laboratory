"""D2 only: records placements of seed, every change to a belief about sowing, and what the spot held, for an observer
that has set world.d2_log. The world never reads it; nothing here draws a random number or changes anything."""


def spot(world, loc):
    """The spot's plant food and crop, and the mean of its eight neighbours'."""
    c = world.cfg
    t = world.tile(loc)
    nb = 0.0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx or dy:
                n = world.tiles[(loc[1] + dy) % c.height][(loc[0] + dx) % c.width]
                nb += n.plants + n.crop
    return round(t.plants, 2), round(t.crop, 2), round(nb / 8.0, 2)


def log(world, rec: dict) -> None:
    lst = getattr(world, "d2_log", None)
    if lst is not None:
        lst.append(rec)
