import importlib
import itertools
from pathlib import Path
import random
import sys
import types
import unittest

# Run without importing Archipelago's world registry.
root = Path(__file__).resolve().parents[1] / "World" / "smo"
for name, path in (("_smo_test", root), ("_smo_test.Connector", root / "Connector")):
    package = types.ModuleType(name)
    package.__path__ = [str(path)]
    sys.modules[name] = package
route = importlib.import_module("_smo_test.KingdomOrder")
packets = importlib.import_module("_smo_test.Connector.Packets")


class EarlyKingdomTest(unittest.TestCase):
    def test_rng_is_seeded_and_spans_all_permutations(self):
        orders = set()
        for seed in range(100):
            order = route.roll_order(random.Random(seed))
            self.assertEqual(order, route.roll_order(random.Random(seed)))
            orders.add(order)
        self.assertEqual(orders, set(itertools.permutations(route.EARLY_KINGDOMS)))

    def test_slot_wire_format(self):
        values = [5, 16, 16, 8, 10, 20, 10, 10, 18, 3, 8, 250, 500, False, True]
        guid = bytes(16)
        def packet(order):
            return packets.Packet(guid=guid, packet_type=packets.PacketType.SlotData,
                                  packet_data=values + list(order))
        old = packet([]).serialize()
        self.assertEqual(len(old), 20 + 28)
        self.assertEqual(packets.SlotDataPacket(packet_bytes=old[20:]).early_order, ())
        for order in itertools.permutations(route.EARLY_KINGDOMS):
            encoded = packet([order]).serialize()
            self.assertEqual(len(encoded), 20 + 31)
            self.assertEqual(encoded[20:48], old[20:])
            self.assertEqual(encoded[48:], bytes(order))
            decoded = packets.SlotDataPacket(packet_bytes=encoded[20:])
            self.assertEqual(decoded.early_order, order)
            self.assertEqual(decoded.serialize(), encoded[20:])

    def test_short_orders_and_wire_compatibility(self):
        values = [5, 16, 16, 8, 10, 20, 10, 10, 18, 3, 8, 250, 500, False, False]
        for count in range(1, 10):
            for seed in range(20):
                order = route.roll_short_route(random.Random(seed), count)
                self.assertEqual(len(order), count)
                self.assertEqual(order, route.roll_short_route(random.Random(seed), count))
                packet = packets.Packet(guid=bytes(16), packet_type=packets.PacketType.SlotData,
                                        packet_data=[*values, (), order]).serialize()
                self.assertEqual(packet[48:], bytes((255, *order)))
                decoded = packets.SlotDataPacket(packet_bytes=packet[20:])
                self.assertEqual(decoded.short_route, order)
                self.assertEqual(decoded.early_order, ())
                self.assertEqual(decoded.serialize(), packet[20:])
        for invalid in ([1, 1], [5], [11], [12], [True], None):
            with self.assertRaises(ValueError):
                route.validate_short_route(invalid)

    def test_invalid_order_fails(self):
        for order in (None, [1], [1, 1, 4], [1, 2, 3], [True, 2, 4], "124"):
            with self.assertRaises(ValueError):
                route.validate_order(order)


if __name__ == "__main__":
    unittest.main()

