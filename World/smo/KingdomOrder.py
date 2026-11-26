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


# Cloud and Ruined have special transitions; keep them outside this first mode.
SHORT_KINGDOMS = {1: "Cascade", 2: "Sand", 3: "Wooded", 4: "Lake", 6: "Lost",
                  7: "Metro", 8: "Seaside", 9: "Snow", 10: "Luncheon"}
SHORT_KEY = "short_kingdom_route"
SHORT_MARKER = 255


def validate_short_route(route):
    if not isinstance(route, (tuple, list)):
        raise ValueError("Short kingdom route must be a sequence.")
    if (len(route) > len(SHORT_KINGDOMS)
            or any(type(x) is not int or x not in SHORT_KINGDOMS for x in route)
            or len(set(route)) != len(route)):
        raise ValueError("Invalid short kingdom route.")
    return tuple(route)


def roll_short_route(rng, count):
    if not 1 <= count <= len(SHORT_KINGDOMS):
        raise ValueError("Select 1 to 9 intermediate kingdoms.")
    return tuple(rng.sample(tuple(SHORT_KINGDOMS), count))
