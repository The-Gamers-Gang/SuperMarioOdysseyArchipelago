"""Universal Tracker regen must not read passthrough when Odyssey slot data is absent."""

import importlib.util
import sys
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMO_ROOT = ROOT / "World" / "smo"


def _ensure_options():
    existing = sys.modules.get("Options")
    if existing is not None and hasattr(existing, "Choice") and hasattr(existing, "DeathLink"):
        return
    sys.path.insert(0, str(ROOT / "tests"))
    import test_extra_moons
    if test_extra_moons._real_archipelago_options() is None:
        test_extra_moons._install_choice_stub()


def _stub(name, **attrs):
    module = sys.modules.get(name)
    if module is None:
        module = types.ModuleType(name)
        sys.modules[name] = module
    for key, value in attrs.items():
        setattr(module, key, value)
    return module


def _install_archipelago_stubs():
    class Item:
        pass

    class Location:
        pass

    class Region:
        def __init__(self, *args, **kwargs):
            pass

    class CollectionState:
        pass

    class ItemClassification:
        filler = 0
        progression = 1
        progression_skip_balancing = 2

    _stub("BaseClasses", Item=Item, Location=Location, Region=Region,
          CollectionState=CollectionState, ItemClassification=ItemClassification)

    worlds = _stub("worlds")
    worlds.__path__ = []
    auto = _stub("worlds.AutoWorld")

    class World:
        pass

    auto.World = World
    generic = _stub("worlds.generic")
    generic.__path__ = []
    _stub("worlds.generic.Rules", set_rule=lambda *args, **kwargs: None)

    class Component:
        def __init__(self, *args, **kwargs):
            pass

    class ComponentType:
        CLIENT = "client"

    _stub("worlds.LauncherComponents", Component=Component, components=[],
          Type=ComponentType, SuffixIdentifier=object(), launch=lambda *args, **kwargs: None)
    _stub("settings", Group=type("Group", (), {}), UserFolderPath=type("UserFolderPath", (), {}))
    utils = _stub("Utils")
    if not hasattr(utils, "output_path"):
        utils.output_path = lambda *args, **kwargs: ""


def _load_world():
    _ensure_options()
    _install_archipelago_stubs()
    name = "_smo_tracker_world"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(
        name, SMO_ROOT / "__init__.py", submodule_search_locations=[str(SMO_ROOT)])
    module = importlib.util.module_from_spec(spec)
    module.__package__ = name
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class TrackerRegenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world_module = _load_world()
        cls.calls = []

        def record_regions(world, multiworld, player):
            cls.calls.append((world, multiworld, player))

        cls.world_module.create_regions = record_regions

    def setUp(self):
        self.calls = type(self).calls
        self.calls.clear()

    def _world(self, passthrough=None, has_passthrough=True):
        multiworld = types.SimpleNamespace(generation_is_fake=True, regions=[])
        if has_passthrough:
            multiworld.re_gen_passthrough = {} if passthrough is None else passthrough
        world = self.world_module.SMOWorld.__new__(self.world_module.SMOWorld)
        world.multiworld = multiworld
        world.player = 1
        world.moon_counts = {"cascade": 123}
        world.early_kingdom_order = ("keep-early",)
        world.short_route = ("keep-short",)
        world.options = types.SimpleNamespace(
            counts=0,
            goal=types.SimpleNamespace(value=2, option_moon=13),
        )
        return world

    def test_missing_odyssey_slot_data_does_not_read_passthrough(self):
        world = self._world({"Other Game": {}})
        self.world_module.SMOWorld.create_regions(world)
        self.assertEqual(world.moon_counts, {"cascade": 123})
        self.assertEqual(world.early_kingdom_order, ("keep-early",))
        self.assertEqual(world.short_route, ("keep-short",))
        self.assertEqual(world.options.goal.value, 2)
        self.assertEqual(self.calls, [(world, world.multiworld, 1)])

    def test_missing_passthrough_attribute_still_builds_regions(self):
        world = self._world(has_passthrough=False)
        self.world_module.SMOWorld.create_regions(world)
        self.assertEqual(world.short_route, ("keep-short",))
        self.assertEqual(self.calls, [(world, world.multiworld, 1)])

    def test_odyssey_slot_data_still_restores_short_route(self):
        passthrough = {
            "Super Mario Odyssey": {
                "MoonCounts": {"cascade": 9, "sand": 16},
                "EarlyKingdomOrder": [4, 1, 2],
                "ShortKingdomRoute": [10, 6],
            }
        }
        world = self._world(passthrough)
        self.world_module.SMOWorld.create_regions(world)
        self.assertEqual(world.moon_counts, {"cascade": 9, "sand": 16})
        self.assertEqual(world.early_kingdom_order, (4, 1, 2))
        self.assertEqual(world.short_route, (10, 6))
        self.assertEqual(world.options.goal.value, 13)
        self.assertEqual(self.calls, [(world, world.multiworld, 1)])


if __name__ == "__main__":
    unittest.main()
