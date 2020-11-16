""" TODO: Finish docstring """


def get_key_byte(seed: int, a: int, b: int, c: int) -> int:
    """ TODO: Finish docstring

    :param seed:
    :param a:
    :param b:
    :param c:
    :return:
    """

    a %= 25
    b %= 3
    if a % 2 == 0:
        key_byte = ((seed >> a) & 255) ^ ((seed >> b) | c)
    else:
        key_byte = ((seed >> a) & 255) ^ ((seed >> b) & c)
    return key_byte % 255


def get_checksum(s: str) -> int:
    """ TODO: Finish docstring

    :param s:
    :return:
    """

    left = 86
    right = 175
    if len(s) > 0:
        for x in s:
            right += int(x, 16)
            if right > 255:
                right -= 255
            left += right
            if left > 255:
                left -= 255
    checksum = (left << 8) + right

    return checksum
