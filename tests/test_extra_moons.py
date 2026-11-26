"""ExtraMoons choice ids are ints. Pool sizes keep the old float multipliers."""

import ast
import importlib.util
import os
import sys
import types
import unittest
from dataclasses import dataclass
from math import floor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMO_OPTIONS = ROOT / "World" / "smo" / "Options.py"
SMO_INIT = ROOT / "World" / "smo" / "__init__.py"

# Multipliers previously stored as the Choice values themselves.
OLD_MULTIPLIERS = {
    "none": 1.0,
    "some": 1.2,
    "more": 1.5,
    "many": 1.75,
    "double": 2.0,
}
POOL_KINGDOMS = (
    "cascade", "sand", "wooded", "lake", "lost", "metro",
    "seaside", "snow", "luncheon", "ruined", "bowser",
)


def _install_choice_stub():
    """Choice.from_any as Generate.handle_option calls it.

    An omitted YAML key is resolved with from_any(option.default). An int is
    accepted only when it is a defined choice id; anything else is the option
    name. This mirrors Archipelago's Choice, so the suite runs without an
    Archipelago checkout. Set PYTHONPATH to a checkout to exercise the real class.
    """

    class AssembleOptions(type):
        def __new__(mcs, name, bases, attrs):
            options = {}
            name_lookup = {}
            for base in bases:
                if getattr(base, "options", None):
                    options.update(base.options)
                    name_lookup.update(base.name_lookup)
            new_options = {
                attr[7:].lower(): option_id
                for attr, option_id in attrs.items()
                if attr.startswith("option_")
            }
            assert "random" not in new_options
            assert len(new_options) == len(set(new_options.values())), "same ID cannot be used twice"
            name_lookup.update({option_id: option_name for option_name, option_id in new_options.items()})
            options.update(new_options)
            aliases = {
                attr[6:].lower(): option_id
                for attr, option_id in attrs.items()
                if attr.startswith("alias_")
            }
            options.update(aliases)
            attrs["options"] = options
            attrs["name_lookup"] = name_lookup
            attrs["aliases"] = aliases
            return super().__new__(mcs, name, bases, attrs)

    class Option(metaclass=AssembleOptions):
        default = 0

    class NumericOption(Option):
        pass

    class Choice(NumericOption):
        def __init__(self, value: int):
            self.value = value

        @classmethod
        def from_text(cls, text: str):
            text = text.lower()
            for option_name, value in cls.options.items():
                if option_name == text:
                    return cls(value)
            raise KeyError(
                f'Could not find option "{text}" for "{cls.__name__}", '
                f'known options are {", ".join(cls.name_lookup.values())}'
            )

        @classmethod
        def from_any(cls, data):
            if type(data) == int and data in cls.options.values():
                return cls(data)
            return cls.from_text(str(data))

    class Toggle(Choice):
        option_false = 0
        option_true = 1
        default = 0

    class Range(NumericOption):
        def __init__(self, value):
            self.value = value

    class FreeText(Option):
        default = ""

    @dataclass
    class PerGameCommonOptions:
        pass

    class DeathLink(Toggle):
        """Death Link"""

    module = types.ModuleType("Options")
    for obj in (Toggle, Choice, Range, FreeText, PerGameCommonOptions, DeathLink, Option):
        setattr(module, obj.__name__, obj)
    sys.modules["Options"] = module
    return module


def _allow_options_import():
    """Archipelago's Options.py imports Utils at module level. A full checkout
    provides it. A lone Options.py (used to exercise the real Choice) does not."""
    if "Utils" in sys.modules:
        return
    try:
        import Utils  # noqa: F401
    except Exception:
        utils = types.ModuleType("Utils")
        utils.get_file_safe_name = lambda name: name
        utils.get_fuzzy_results = lambda *a, **k: []
        utils.is_iterable_except_str = lambda obj: isinstance(obj, (list, tuple, set, dict))
        utils.output_path = lambda *a, **k: ""
        sys.modules["Utils"] = utils


def _real_archipelago_options():
    if "Options" in sys.modules:
        module = sys.modules["Options"]
    else:
        spec = importlib.util.find_spec("Options")
        origin = getattr(spec, "origin", None) or ""
        if spec is None or not origin or "SuperMarioOdysseyArchipelago" in origin.replace("\\", "/"):
            return None
        _allow_options_import()
        try:
            import Options as module
        except Exception:
            sys.modules.pop("Options", None)
            return None
    if (
        getattr(module, "Choice", None) is not None
        and hasattr(module.Choice, "from_any")
        and hasattr(module, "DeathLink")
        and hasattr(module, "PerGameCommonOptions")
        and getattr(module, "__file__", "")
        and "SuperMarioOdysseyArchipelago" not in module.__file__.replace("\\", "/")
    ):
        return module
    sys.modules.pop("Options", None)
    return None


def _load_extra_moons():
    real = _real_archipelago_options()
    if real is None:
        _install_choice_stub()
    spec = importlib.util.spec_from_file_location("smo_options_under_test", SMO_OPTIONS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ExtraMoons, real is not None


def _class_dict(source: str, class_name: str, attr: str):
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for stmt in node.body:
                if isinstance(stmt, ast.Assign):
                    for target in stmt.targets:
                        if isinstance(target, ast.Name) and target.id == attr:
                            return ast.literal_eval(stmt.value)
    raise AssertionError(f"{class_name}.{attr} not found")


def resolve_extra_moons(option_cls, weights):
    """Generate.handle_option for extra_moons, without world verify."""
    if "extra_moons" in weights:
        return option_cls.from_any(weights["extra_moons"])
    return option_cls.from_any(option_cls.default)


class ExtraMoonsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ExtraMoons, cls.used_real_choice = _load_extra_moons()

    def test_backend_matches_request(self):
        if os.environ.get("EXPECT_REAL_ARCHIPELAGO") == "1":
            self.assertTrue(self.used_real_choice)

    def test_ids_are_ints_and_default_is_some(self):
        expected = {"none": 0, "some": 1, "more": 2, "many": 3, "double": 4}
        for name, option_id in expected.items():
            value = getattr(self.ExtraMoons, f"option_{name}")
            self.assertIs(type(value), int)
            self.assertEqual(value, option_id)
            self.assertEqual(self.ExtraMoons.multipliers[option_id], OLD_MULTIPLIERS[name])
        self.assertIs(type(self.ExtraMoons.default), int)
        self.assertEqual(self.ExtraMoons.default, 1)
        self.assertEqual(self.ExtraMoons.default, self.ExtraMoons.option_some)

    def test_from_any_names_default_and_omitted_yaml(self):
        for name in ("none", "some", "more", "many", "double", "None", "SOME", "Double"):
            option = self.ExtraMoons.from_any(name)
            self.assertEqual(option.value, getattr(self.ExtraMoons, f"option_{name.lower()}"))
            self.assertEqual(option.multiplier, OLD_MULTIPLIERS[name.lower()])

        for option_id, name in enumerate(("none", "some", "more", "many", "double")):
            option = self.ExtraMoons.from_any(option_id)
            self.assertEqual(option.value, option_id)
            self.assertEqual(option.multiplier, OLD_MULTIPLIERS[name])

        by_default = self.ExtraMoons.from_any(self.ExtraMoons.default)
        self.assertEqual((by_default.value, by_default.multiplier), (1, 1.2))

        omitted = resolve_extra_moons(self.ExtraMoons, {"goal": "moon"})
        self.assertEqual((omitted.value, omitted.multiplier), (1, 1.2))

        named = resolve_extra_moons(self.ExtraMoons, {"extra_moons": "many"})
        self.assertEqual((named.value, named.multiplier), (3, 1.75))

        with self.assertRaises(KeyError):
            self.ExtraMoons.from_any(1.2)

    def test_pool_counts_match_old_multiplier_math(self):
        source = SMO_INIT.read_text()
        moon_counts = _class_dict(source, "SMOWorld", "moon_counts")
        max_counts = _class_dict(source, "SMOWorld", "max_counts")
        self.assertNotIn("extra_moons.value", source)
        self.assertGreaterEqual(source.count("extra_moons.multiplier"), len(POOL_KINGDOMS))

        for name, old_multiplier in OLD_MULTIPLIERS.items():
            option = self.ExtraMoons.from_any(name)
            for kingdom in POOL_KINGDOMS:
                expected = min(floor(moon_counts[kingdom] * old_multiplier), max_counts[kingdom])
                actual = min(floor(moon_counts[kingdom] * option.multiplier), max_counts[kingdom])
                self.assertEqual(actual, expected)
                self.assertIs(type(actual), int)


if __name__ == "__main__":
    unittest.main()
