""" This script contains unit tests for class KeyUtils """
import unittest

from ddt import ddt

from serial_key_generator.key_utils import KeyUtils


@ddt
class TestKeyUtils(unittest.TestCase):
    """ TestKeyUtils unit tests """

    def test_get_key_byte_same_arguments(self):
        """ Checks if get_key_bytes gives repeatable results for same arguments """

        seed = "test"
        key_bytes_1 = KeyUtils.get_key_bytes(seed, 1, 2, 3)
        key_bytes_2 = KeyUtils.get_key_bytes(seed, 1, 2, 3)
        self.assertEqual(key_bytes_1, key_bytes_2)

    def test_get_key_byte_different_arguments(self):
        """ Checks if get_key_bytes gives different results for different arguments """

        key_bytes_1 = KeyUtils.get_key_bytes("test1", 1, 2, 3)
        key_bytes_2 = KeyUtils.get_key_bytes("test2", 3, 2, 1)
        self.assertNotEqual(key_bytes_1, key_bytes_2)

    def test_get_checksum_same_arguments(self):
        """ Checks if get_checksum gives repeatable results for same arguments """

        input_str = "test1234"
        checksum_1 = KeyUtils.get_checksum(input_str)
        checksum_2 = KeyUtils.get_checksum(input_str)
        self.assertEqual(checksum_1, checksum_2)

    def test_get_checksum_different_arguments(self):
        """ Checks if get_checksum gives different results for different arguments """

        checksum_1 = KeyUtils.get_checksum("test1234")
        checksum_2 = KeyUtils.get_checksum("test5678")
        self.assertNotEqual(checksum_1, checksum_2)
