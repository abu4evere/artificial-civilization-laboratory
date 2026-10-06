"""S1 only: records each person's options and choice for an observer that has set world.s1_log. The world never
reads it, and nothing here draws a random number or changes a person."""


def record(world, p, options, i, base, lw, total_need, hunger, season) -> None:
    log = getattr(world, "s1_log", None)
    if log is None:
        return
    from .person import A
    log.append({
        "pid": p.id, "season": season, "hunger": hunger,
        "food": p.food, "seeds": p.seeds, "line": 2.0 * total_need,
        "options": [(o[0], o[1], o[2] if isinstance(o[2], str) else None) for o in options],
        "chosen": i,
        "q_put": lw * p.q[base + A["put"]], "q_forage": lw * p.q[base + A["forage"]],
        "b_food": p.beliefs.get(f"food@{season}"), "b_seeds": p.beliefs.get(f"seeds@{season}"),
        "h_food": ("b:food@%d" % season) in p.heard, "h_seeds": ("b:seeds@%d" % season) in p.heard,
    })
