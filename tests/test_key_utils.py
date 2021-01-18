import unittest

from ddt import ddt

from serial_key_generator.key_utils import KeyUtils


@ddt
class TestKeyUtils(unittest.TestCase):
    def test_get_key_byte(self):
        seed = "test"
        key_bytes = KeyUtils.get_key_bytes(seed, 1, 2, 3)
        self.assertEqual("C0", key_bytes)

    def test_get_checksum(self):
        checksum = KeyUtils.get_checksum("test1234")
        self.assertEqual("Z32G", checksum)
