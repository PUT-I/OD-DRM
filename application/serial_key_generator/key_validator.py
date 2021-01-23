from enum import Enum, auto

from serial_key_generator.key_utils import KeyUtils


class KeyStatus(Enum):
    VALID = auto()
    INVALID = auto()
    BLACKLISTED = auto()
    FORGED = auto()


class KeyValidator:
    _KEY_00 = 1
    _KEY_01 = 1
    _KEY_02 = 0
    _KEY_03 = 0
    _KEY_04 = 0
    _seed_blacklist = [
        # 'QZ4JN2AMVXY',
        # 'CZDI6H4K2IL',
        # 'TCK4BKX0PHA',
        # 'ZA0PLET272K'
    ]

    @staticmethod
    def check_key(key: str) -> KeyStatus:
        key = KeyValidator._reformat_key(key)

        if not KeyValidator._check_key_checksum(key):
            return KeyStatus.INVALID

        seed = f"{key[3:6]}{key[9:12]}{key[14:16]}{key[18:19]}{key[22:24]}"

        for blacklisted_seed in KeyValidator._seed_blacklist:
            if seed == blacklisted_seed:
                return KeyStatus.BLACKLISTED

        if KeyValidator._KEY_00:
            key_bytes_0 = f"{key[1]}{key[21]}"
            if key_bytes_0 != KeyUtils.get_key_bytes(seed, 9871654, 98713654, 98713657):
                return KeyStatus.FORGED

        if KeyValidator._KEY_01:
            key_bytes_1 = f"{key[2]}{key[7]}"
            if key_bytes_1 != KeyUtils.get_key_bytes(seed, 189364, 153499, 98172563):
                return KeyStatus.FORGED

        if KeyValidator._KEY_02:
            key_bytes_2 = f"{key[8]}{key[12]}"
            if key_bytes_2 != KeyUtils.get_key_bytes(seed, 9861523849, 8761534, 67514985):
                return KeyStatus.FORGED

        if KeyValidator._KEY_03:
            key_bytes_3 = f"{key[13]}{key[16]}"
            if key_bytes_3 != KeyUtils.get_key_bytes(seed, 786153786615, 91876458615, 81359712):
                return KeyStatus.FORGED

        if KeyValidator._KEY_04:
            key_bytes_4 = f"{key[17]}{key[20]}"
            if key_bytes_4 != KeyUtils.get_key_bytes(seed, 987145, 6487961023, 581640):
                return KeyStatus.FORGED

        return KeyStatus.VALID

    @staticmethod
    def add_key_to_blacklist(key):
        key = KeyValidator._reformat_key(key)
        seed = f"{key[3:6]}{key[9:12]}{key[14:16]}{key[18:19]}{key[22:24]}"

        KeyValidator._seed_blacklist.append(seed)

    @staticmethod
    def _reformat_key(key) -> str:
        return key.upper().strip().replace('-', '')

    @staticmethod
    def _check_key_checksum(key: str) -> bool:
        if len(key) != 25:
            return False

        checksum = f"{key[0]}{key[6]}{key[19]}{key[24]}"
        try:
            return checksum == KeyUtils.get_checksum(f"{key[1:6]}{key[7:19]}{key[20:24]}")
        except ValueError:
            return False


if __name__ == '__main__':
    x = input('Enter key to validate: ')
    print(KeyValidator.check_key(x))
