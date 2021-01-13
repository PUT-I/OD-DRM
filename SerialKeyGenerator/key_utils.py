""" TODO: Finish docstring """
import string
import math

characters = list("_" + string.ascii_uppercase + string.digits)


def str_to_int(input_str: str) -> int:
    """

    :param input_str:
    :return:
    """
    input_bytes_list = []
    for character in input_str:
        input_bytes_list.append(characters.index(character))
    input_bytes = bytes(input_bytes_list)
    return int.from_bytes(input_bytes, byteorder="big", signed=False)


def int_to_str(input_int: int, length: int = 100) -> str:
    """

    :param input_int:
    :param length:
    :return:
    """
    output_bytes = input_int.to_bytes(length, byteorder="big", signed=False)
    result = []
    for byte in output_bytes:
        if byte == 0x00:
            continue
        result.append(characters[byte % len(characters)])
    return "".join(result)


def get_key_byte(seed_str: str, a: int, b: int, c: int) -> str:
    """ TODO: Finish docstring

    :param seed_str:
    :param a:
    :param b:
    :param c:
    :return:
    """
    seed = str_to_int(seed_str) << a
    seed += a
    pow_ = math.pow(seed % 78651, b % 55)
    sqrt_ = math.sqrt(pow_)
    key = int(sqrt_) * c
    return int_to_str(int(key))[:2].zfill(2)


def get_checksum(s: str) -> str:
    """ TODO: Finish docstring

    :param s:
    :return:
    """
    i = hash(str_to_int(s))
    checksum = int_to_str(i)
    return checksum[:4].zfill(4)
