from key_utils import get_key_byte, get_checksum
import sys, random, os


def make_key(seed):
    hexformat = '{0:0{1}x}'
    hexseed = hexformat.format(seed % int('ffffffff', 16), 8)
    kb0 = hexformat.format(get_key_byte(int(hexseed, 16), 9871654, 98713654, 98713657), 2)
    kb1 = hexformat.format(get_key_byte(int(hexseed, 16), 189364, 153499, 98172563), 2)
    kb2 = hexformat.format(get_key_byte(int(hexseed, 16), 9861523849, 8761534, 67514985), 2)
    kb3 = hexformat.format(get_key_byte(int(hexseed, 16), 786153786615, 91876458615, 81359712), 2)
    checksum = hexformat.format(get_checksum(hexseed + kb0 + kb1 + kb2 + kb3), 4)
    key = hexseed[0:4] + "-" + hexseed[4:8] + "-" + kb0 + kb1 + "-" + kb2 + kb3 + "-" + checksum
    return key


if __name__ == '__main__':
    nb = input('Keys to generate:')
    # try:
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
        rand = random.randrange(int('ffffffff', 16))
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
    # except ValueError:
    #     print("Invalid number")
