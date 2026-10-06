"""W1 only: counts food where it moves inside the body phase and the stash update. Writes to world.ledger when an
observer has set it, and nothing else; the world never reads it."""


def add(world, key: str, amount: float) -> None:
    led = getattr(world, "ledger", None)
    if led is not None and amount:
        led[key] = led.get(key, 0.0) + amount
