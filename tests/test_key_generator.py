import unittest

from serial_key_generator.key_generator import KeyGenerator
from serial_key_generator.key_validator import KeyValidator, KeyStatus


class TestKeyGenerator(unittest.TestCase):
    def test_generate_key(self):
        seed = "testtesttes"
        key = KeyGenerator.generate_key(seed)

        self.assertEqual(KeyStatus.VALID, KeyValidator.check_key(key))

    def test_generate_key_short_seed(self):
        seed = "test"

        error_message = ""
        try:
            KeyGenerator.generate_key(seed)
        except ValueError as error:
            error_message = str(error)

        self.assertEqual(error_message, "Seed is shorter than 11 bytes")

    def test_generate_seed(self):
        seed = KeyGenerator.generate_seed()
        key = KeyGenerator.generate_key(seed)

        self.assertEqual(KeyStatus.VALID, KeyValidator.check_key(key))
