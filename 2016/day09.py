import re

from util import *

DAY = 9


def decompress(compressed, recurse=False):
    bracket_regex = r"\(([0-9]+)x([0-9]+)\)"
    curr_pos = 0
    res = 0
    while True:
        if m := re.search(bracket_regex, compressed[curr_pos:]):
            x, y = map(int, m.groups())
            start, end = m.span()
            string_start = curr_pos + end
            string_end = string_start + x
            res += start
            if recurse:
                res += y * decompress(compressed[string_start:string_end], recurse)
            else:
                res += y * x
            curr_pos = string_end
        else:
            break
    res += len(compressed) - curr_pos
    return res


def part1(data):
    return decompress(data[0])


def part2(data):
    return decompress(data[0], recurse=True)


if __name__ == "__main__":
    data = get_data(DAY)
    # res = part1(data)

    # print(res)
    # submit(DAY, 1, res)
    # print(decompress("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN",True))
    res = part2(data)
    submit(DAY, 2, res)
