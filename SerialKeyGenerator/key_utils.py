import string
import math

characters = list("_" + string.ascii_uppercase + string.digits)


def str_to_int(input_str: str) -> int:
    input_bytes_list = []
    for character in input_str:
        input_bytes_list.append(characters.index(character))
    input_bytes = bytes(input_bytes_list)
    return int.from_bytes(input_bytes, byteorder="big", signed=False)


def int_to_str(input_int: int, length=100) -> str:
    output_bytes = input_int.to_bytes(length, byteorder="big", signed=False)
    result = []
    for byte in output_bytes:
        if byte % len(characters) == 0x00:
            continue
        result.append(characters[byte % len(characters)])
    return "".join(result)


def get_key_byte(seed_str: str, a: int, b: int, c: int) -> str:
    seed = str_to_int(seed_str) << a % 8615323
    seed += a
    pow_ = math.pow(seed % 78651, b % 55)
    sqrt_ = math.sqrt(pow_)
    key = int(sqrt_) * c
    return int_to_str(int(key))[:2].zfill(2)


def get_checksum(s: str) -> str:
    i = hash(str_to_int(s))
    checksum = int_to_str(i)
    return checksum[:4].zfill(4)
