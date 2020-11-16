def get_key_byte(seed, a, b, c):
    a %= 25
    b %= 3
    if a % 2 == 0:
        keybyte = ((seed >> a) & 255) ^ ((seed >> b) | c)
    else:
        keybyte = ((seed >> a) & 255) ^ ((seed >> b) & c)
    return keybyte % 255


def get_checksum(s):
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
