from enum import Enum, auto

from key_utils import get_checksum, get_key_byte

KEY00 = 1
KEY01 = 1
KEY02 = 0
KEY03 = 0
KEY04 = 0
BL = [
    # 'QZ4JN2AMVXY',
    # 'CZDI6H4K2IL',
    # 'TCK4BKX0PHA',
    # 'ZA0PLET272K'
]


class Key(Enum):
    GOOD = auto()
    INVALID = auto()
    BLACKLISTED = auto()
    FORGED = auto()


def check_key_checksum(key: str) -> bool:
    key = key.replace('-', '')
    if len(key) != 25:
        return False
    checksum = f"{key[0:1]}{key[6:7]}{key[19:20]}{key[24:25]}"
    return checksum == get_checksum(f"{key[1:6]}{key[7:19]}{key[20:24]}")


def check_key(key: str) -> Key:
    if not check_key_checksum(key):
        return Key.INVALID
    key = key.replace('-', '')
    seed = f"{key[3:6]}{key[9:12]}{key[14:16]}{key[18:19]}{key[22:24]}"
    for bl in BL:
        if seed == bl:
            return Key.BLACKLISTED
    if KEY00:
        kb0 = f"{key[1:2]}{key[21:22]}"
        if kb0 != get_key_byte(seed, 9871654, 98713654, 98713657):
            return Key.FORGED
    if KEY01:
        kb1 = f"{key[2:3]}{key[7:8]}"
        if kb1 != get_key_byte(seed, 189364, 153499, 98172563):
            return Key.FORGED
    if KEY02:
        kb2 = f"{key[8:9]}{key[12:13]}"
        if kb2 != get_key_byte(seed, 9861523849, 8761534, 67514985):
            return Key.FORGED
    if KEY03:
        kb3 = f"{key[13:14]}{key[16:17]}"
        if kb3 != get_key_byte(seed, 786153786615, 91876458615, 81359712):
            return Key.FORGED
    if KEY04:
        kb4 = f"{key[17:18]}{key[20:21]}"
        if kb4 != get_key_byte(seed, 987145, 6487961023, 581640):
            return Key.FORGED
    return Key.GOOD


def _main() -> None:
    x = input('Key to validate: ')
    print(check_key(x))


if __name__ == '__main__':
    _main()
