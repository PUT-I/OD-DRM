""" TODO: Finish docstring """
import os
import random
import sys

from key_utils import get_key_byte, get_checksum


def make_key(seed: int) -> str:
    """ TODO: Finish docstring

    :param seed:
    :return:
    """

    hex_format = '{0:0{1}x}'
    hex_seed = hex_format.format(seed % int('ffffffff', 16), 8)
    print(type(hex_seed))

    kb0 = hex_format.format(get_key_byte(int(hex_seed, 16), 9871654, 98713654, 98713657), 2)
    kb1 = hex_format.format(get_key_byte(int(hex_seed, 16), 189364, 153499, 98172563), 2)
    kb2 = hex_format.format(get_key_byte(int(hex_seed, 16), 9861523849, 8761534, 67514985), 2)
    kb3 = hex_format.format(get_key_byte(int(hex_seed, 16), 786153786615, 91876458615, 81359712), 2)

    checksum = hex_format.format(get_checksum(hex_seed + kb0 + kb1 + kb2 + kb3), 4)
    key = f"{hex_seed[0:4]}-{hex_seed[4:8]}-{kb0}{kb1}-{kb2}{kb3}-{checksum}"

    return key


def _main() -> None:
    """ Main function """

    nb = input('Keys to generate: ')

    keys = int(nb)
    generated = 0
    burned_seeds = []
    used_seeds = []
    original_stdout = sys.stdout

    if os.path.exists('used_seeds.txt'):
        print('Loading used seeds...')
        with open('used_seeds.txt', 'r') as ur:
            lines = ur.readlines()
            for line in lines:
                burned_seeds.append(line[:-1])
            ur.close()

    print('Printing keys...')
    sys.stdout = open("valid_keys.txt", "w")
    while generated < keys:
        already_used = False
        rand: int = random.randrange(int('ffffffff', 16))

        for b in burned_seeds:
            if int(b, 16) == rand:
                already_used = True
                break

        if already_used:
            continue

        for u in used_seeds:
            if int(u, 16) == rand:
                already_used = True
                break

        if already_used:
            continue

        print(make_key(rand))
        used_seeds.append('{0:0{1}x}'.format(rand, 8))
        generated += 1
    sys.stdout = original_stdout

    print('Printing seeds...')
    sys.stdout = open("used_seeds.txt", "a")
    for u in used_seeds:
        print(u)
    sys.stdout = original_stdout

    print('Done!')


if __name__ == '__main__':
    _main()
