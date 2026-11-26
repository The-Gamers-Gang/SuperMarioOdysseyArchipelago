"""Shared APWorld/connector contract for a seed-selected early kingdom route."""

# Odyssey's world IDs (same IDs as the mod's moon quota table).
EARLY_KINGDOMS = {1: "Cascade", 2: "Sand", 4: "Lake"}
SLOT_KEY = "early_kingdom_order"


def validate_order(order):
    """An empty sequence means vanilla/old slot data; otherwise require the entire pool."""
    if not isinstance(order, (tuple, list)):
        raise ValueError("Early kingdom order must be a sequence.")
    if not order:
        return ()
    if len(order) != len(EARLY_KINGDOMS) or any(type(x) is not int for x in order):
        raise ValueError("Invalid early kingdom order.")
    if set(order) != set(EARLY_KINGDOMS):
        raise ValueError("Early kingdom order must contain Cascade, Sand, and Lake exactly once.")
    return tuple(order)


def roll_order(rng):
    order = list(EARLY_KINGDOMS)
    rng.shuffle(order)
    return tuple(order)
