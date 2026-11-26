"""Check actual host-slot locations in an AP 0.6.8 generated test archive.

Pass an AP source checkout and a generated ZIP from a mixed test room. This
asserts presence/absence of AP locations, not gameplay reachability.
"""
import argparse
import sys
import zlib
from pathlib import Path
from zipfile import ZipFile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("ap_source", type=Path)
parser.add_argument("archives", nargs="+", type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.ap_source.resolve()))
from Utils import restricted_loads

names = dict(enumerate(("Cap", "Cascade", "Sand", "Wooded", "Lake", "Cloud", "Lost",
                        "Metro", "Seaside", "Snow", "Luncheon", "Ruined", "Bowser", "Moon")))
examples_always_omitted = {1088, 417, 40, 524, 2500}
counts = set()
archives = 0
for path in args.archives:
    with ZipFile(path) as archive:
        multidata = archive.read(next(n for n in archive.namelist() if n.endswith(".archipelago")))
    data = restricted_loads(zlib.decompress(multidata[1:]))
    package = data["datapackage"]["Super Mario Odyssey"]["location_name_to_id"]
    by_id = {id_: name for name, id_ in package.items()}
    short_slots = 0
    for player, slot in data["slot_info"].items():
        if slot.game != "Super Mario Odyssey" or not data["slot_data"].get(player, {}).get("short_kingdom_route"):
            continue
        route = data["slot_data"][player]["short_kingdom_route"]
        counts.add(len(route))
        short_slots += 1
        active = {"Cap", "Bowser", "Moon", *(names[id_] for id_ in route)}
        locations = data["locations"][player]  # Keys are HOST location IDs, independent of recipient.
        assert 2499 in locations, (path, player, "missing Moon goal")
        assert not examples_always_omitted & set(locations), (path, player, "disabled check was generated")
        present = set()
        for id_ in locations:
            name = by_id[id_]
            prefix = name.partition(" - ")[0].removesuffix(" Kingdom")
            if prefix in names.values():
                assert prefix in active, (path, player, name, route)
                present.add(prefix)
        assert {names[id_] for id_ in route} <= present, (path, player, "selected kingdom absent")
    assert short_slots >= 2, (path, "use a mixed test room with two short slots")
    assert any(slot.game != "Super Mario Odyssey" for slot in data["slot_info"].values())
    assert any(slot.game == "Super Mario Odyssey" and
               not data["slot_data"].get(pid, {}).get("short_kingdom_route")
               for pid, slot in data["slot_info"].items()), (path, "vanilla control missing")
    archives += 1

print(f"Validated {archives} actual multiworld location tables (short counts: {sorted(counts)}).")
