import os
import random
import string

from serial_key_generator.key_utils import KeyUtils
from serial_key_generator.key_validator import KeyValidator, KeyStatus


class KeyGenerator:
    @staticmethod
    def generate_seed(size: int = 11, chars: str = string.ascii_uppercase + string.digits) -> str:
        return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

    @staticmethod
    def generate_key(seed: str) -> str:
        if len(seed) < 11:
            raise ValueError("Seed is shorter than 11 bytes")

        seed = seed.upper()

        kb0 = KeyUtils.get_key_bytes(seed, 9871654, 98713654, 98713657)
        kb1 = KeyUtils.get_key_bytes(seed, 189364, 153499, 98172563)
        kb2 = KeyUtils.get_key_bytes(seed, 9861523849, 8761534, 67514985)
        kb3 = KeyUtils.get_key_bytes(seed, 786153786615, 91876458615, 81359712)
        kb4 = KeyUtils.get_key_bytes(seed, 987145, 6487961023, 581640)

        incomplete = f"{kb0[:1]}{kb1[:1]}{seed[0:2]}"
        incomplete += f"{seed[2]}{kb1[1:]}{kb2[:1]}{seed[3]}"
        incomplete += f"{seed[4:6]}{kb2[1:]}{kb3[:1]}{seed[6]}"
        incomplete += f"{seed[7]}{kb3[1:]}{kb4[:1]}{seed[8]}"
        incomplete += f"{kb4[1:]}{kb0[1:]}{seed[9:11]}"
        checksum = KeyUtils.get_checksum(incomplete)

        key = f"{checksum[0:1]}{kb0[:1]}{kb1[:1]}{seed[0:2]}"
        key += f"-{seed[2:3]}{checksum[1:2]}{kb1[1:]}{kb2[:1]}{seed[3]}"
        key += f"-{seed[4:6]}{kb2[1:]}{kb3[:1]}{seed[6]}"
        key += f"-{seed[7:8]}{kb3[1:]}{kb4[:1]}{seed[8]}{checksum[2]}"
        key += f"-{kb4[1:]}{kb0[1:]}{seed[9:11]}{checksum[3]}"

        return key


def _main() -> None:
    number_of_keys_str = input('Number of keys to generate: ')
    number_of_keys = int(number_of_keys_str)
    generated = 0
    burned_seeds = []
    used_seeds = []

    if os.path.exists('used_seeds.txt'):
        print('Loading used seeds...')
        with open('used_seeds.txt', 'r') as used_seeds_file:
            lines = used_seeds_file.readlines()
            for line in lines:
                burned_seeds.append(line[:-1])
            used_seeds_file.close()
    print('Printing keys...')

    with open('valid_keys.txt', 'w') as valid_keys_file, open("used_seeds.txt", "a") as used_seeds_file:
        while generated < number_of_keys:
            already_used = False
            random_seed = KeyGenerator.generate_seed()
            for b in burned_seeds:
                if b == random_seed:
                    already_used = True
                    break
            if already_used:
                continue
            for seed in used_seeds:
                if seed == random_seed:
                    already_used = True
                    break
            if already_used:
                continue

            key = KeyGenerator.generate_key(random_seed)
            valid_keys_file.write(key + "\n")
            used_seeds.append(random_seed)
            generated += 1

        print('Printing seeds...')

        for seed in used_seeds:
            used_seeds_file.write(seed + "\n")
        print('Done!')


def _generate_forged_key(position: int = 1) -> None:
    burned_seeds: set = {""}
    finish = False
    while not finish:
        if len(burned_seeds) > 20000:
            print("Generation takes too long, exiting...")
            break

        random_seed = KeyGenerator.generate_seed()

        if random_seed in burned_seeds:
            continue

        burned_seeds.add(random_seed)

        valid_key = KeyGenerator.generate_key(random_seed)

        for character in KeyUtils.characters:
            temp = list(valid_key)
            temp[position] = character
            valid_key = "".join(temp)

            if KeyValidator.check_key(valid_key) == KeyStatus.FORGED:
                print(f"Pos {position} : {valid_key}")
                finish = True
                break


if __name__ == '__main__':
    # Uncomment if you need to generate forged key
    # with wrong byte at given position
    _generate_forged_key(7)

    # _main()
