""" TODO: Finish docstring """
import os
import random
import sys
import string

from key_utils import get_key_byte, get_checksum


def seed_generator(size=11, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def make_key(seed: str) -> str:
    """ TODO: Finish docstring

    :param seed:
    :return:
    """
    # C01SS-SC12S-SS23S-S34SC-40SSC
    kb0 = get_key_byte(seed, 9871654, 98713654, 98713657)
    kb1 = get_key_byte(seed, 189364, 153499, 98172563)
    kb2 = get_key_byte(seed, 9861523849, 8761534, 67514985)
    kb3 = get_key_byte(seed, 786153786615, 91876458615, 81359712)
    kb4 = get_key_byte(seed, 987145, 6487961023, 581640)
    checksum = get_checksum(seed + kb0 + kb1 + kb2 + kb3 + kb4)
    key = f"{checksum[0:1]}{kb0[:1]}{kb1[:1]}{seed[0:2]}"
    key += f"-{seed[2:3]}{checksum[1:2]}{kb1[1:]}{kb2[:1]}{seed[3:4]}"
    key += f"-{seed[4:6]}{kb2[1:]}{kb3[:1]}{seed[6:7]}"
    key += f"-{seed[7:8]}{kb3[1:]}{kb4[:1]}{seed[8:9]}{checksum[2:3]}"
    key += f"-{kb4[1:]}{kb0[:1]}{seed[9:11]}{checksum[3:4]}"
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
        seed = seed_generator()

        for b in burned_seeds:
            if b == seed:
                already_used = True
                break

        if already_used:
            continue

        for u in used_seeds:
            if u == seed:
                already_used = True
                break

        if already_used:
            continue

        print(make_key(seed))
        used_seeds.append(seed)
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
