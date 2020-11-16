""" Finish docstring """
from enum import Enum, auto

from key_utils import get_checksum, get_key_byte

KEY00 = 1
KEY01 = 1
KEY02 = 0
KEY03 = 0
BL = [
    # '88bb121d'
]


class Key(Enum):
    """ TODO: Finish docstring """

    GOOD = auto()
    INVALID = auto()
    BLACKLISTED = auto()
    FORGED = auto()


def check_key_checksum(key: str) -> bool:
    """ TODO: Finish docstring

    :param key:
    :return:
    """

    key = key.replace('-', '')
    if len(key) != 20:
        return False
    checksum = key[16:]
    return checksum == '{0:0{1}x}'.format(get_checksum(key[:16]), 4)


def check_key(key: str) -> Key:
    """ TODO: Finish docstring

    :param key:
    :return:
    """

    hex_format = '{0:0{1}x}'

    if not check_key_checksum(key):
        return Key.INVALID

    key = key.replace('-', '')
    seed = key[:8]

    for bl in BL:
        if seed == bl:
            return Key.BLACKLISTED
    if KEY00:
        kb0 = key[8:10]
        if kb0 != hex_format.format(get_key_byte(int(seed, 16), 9871654, 98713654, 98713657), 2):
            return Key.FORGED

    if KEY01:
        kb1 = key[10:12]
        if kb1 != hex_format.format(get_key_byte(int(seed, 16), 189364, 153499, 98172563), 2):
            return Key.FORGED

    if KEY02:
        kb2 = key[12:14]
        if kb2 != hex_format.format(get_key_byte(int(seed, 16), 9861523849, 8761534, 67514985), 2):
            return Key.FORGED

    if KEY03:
        kb3 = key[14:16]
        if kb3 != hex_format.format(get_key_byte(int(seed, 16), 786153786615, 91876458615, 81359712), 2):
            return Key.FORGED

    return Key.GOOD


def _main() -> None:
    """ Main function """

    x = input('Key to validate: ')
    print(check_key(x))


if __name__ == '__main__':
    _main()
