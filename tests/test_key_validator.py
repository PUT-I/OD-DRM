""" This script contains unit tests for class KeyValidator """

import unittest

from ddt import ddt, data

from serial_key_generator.key_validator import KeyValidator, KeyStatus


@ddt
class TestKeyValidator(unittest.TestCase):
    """ KeyValidator unit tests """

    @data("VLEJY-V4QB2-NL6YC-HDJPX-HTYNY",
          "VLEJYV4QB2NL6YCHDJPXHTYNY",
          "  VLEJY-V4QB2-NL6YC-HDJPX-HTYNY  ",
          "vlejy-v4qb2-nl6yc-hdjpx-htyny")
    def test_valid_key(self, key: str):
        """ Checks if check_key works for different scenarios with valid key """

        key_status = KeyValidator.check_key(key)
        self.assertEqual(KeyStatus.VALID, key_status)

    @data("1BZ1L-YAKI5-MWLBB-9BA1B-L3EAK-INVALID",
          "!@#$%-^&*()-[]{};-ĄĘŚÓŻ-L3EAK",
          "INALI-DINVA-LIDIN-VALID-INVAL")
    def test_invalid_key(self, key):
        """ Checks if check_key works for different scenarios with invalid key """

        key_status = KeyValidator.check_key(key)
        self.assertEqual(KeyStatus.INVALID, key_status)

    def test_blacklisted_key(self):
        """ Checks if check_key recognizes blacklisted key """

        key = "1QCC5-W30DP-FGFRG-K1JEF-QUDLP"
        KeyValidator.add_key_to_blacklist(key)
        key_status = KeyValidator.check_key(key)
        self.assertEqual(KeyStatus.BLACKLISTED, key_status)

    @data("NSMMV-DGAQW-PNUWB-BUA1C-KQKQ2")  # Forged byte 21
    def test_forged_key(self, key):
        """ Checks if check_key recognizes forged keys """

        key_status = KeyValidator.check_key(key)
        self.assertEqual(KeyStatus.FORGED, key_status)
