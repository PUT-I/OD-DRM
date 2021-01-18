import math
import string


class KeyUtils:
    characters = list("_" + string.ascii_uppercase + string.digits)

    @staticmethod
    def get_key_bytes(seed_str: str, a: int, b: int, c: int) -> str:
        seed_str = seed_str.upper()

        seed = KeyUtils._str_to_int(seed_str) << a % 8615323
        seed += a
        pow_ = math.pow(seed % 78651, b % 55)
        sqrt_ = math.sqrt(pow_)
        key = int(sqrt_) * c

        return KeyUtils._int_to_str(int(key))[:2].zfill(2)

    @staticmethod
    def get_checksum(input_str: str) -> str:
        input_str = input_str.upper()

        import hashlib
        hash_bytes: bytes = hashlib.md5(input_str.encode("ascii")).digest()
        hash_number: int = int.from_bytes(hash_bytes, byteorder="big", signed=False)
        checksum = KeyUtils._int_to_str(hash_number)

        return checksum[:4].zfill(4)

    @staticmethod
    def _str_to_int(input_str: str) -> int:
        input_bytes_list = []
        for character in input_str:
            input_bytes_list.append(KeyUtils.characters.index(character))
        input_bytes = bytes(input_bytes_list)

        return int.from_bytes(input_bytes, byteorder="big", signed=False)

    @staticmethod
    def _int_to_str(input_int: int, length=100) -> str:
        output_bytes = input_int.to_bytes(length, byteorder="big", signed=False)
        result = []
        for byte in output_bytes:
            if byte % len(KeyUtils.characters) == 0x00:
                continue
            result.append(KeyUtils.characters[byte % len(KeyUtils.characters)])

        return "".join(result)
