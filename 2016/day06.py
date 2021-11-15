from collections import Counter

from util import *

DAY = 6


def part1(data):
    cols = [sorted((-n, letter) for letter, n in Counter(x).items())[0][1] for x in zip(*data)]
    return "".join(cols)


def part2(data):
    cols = [sorted((n, letter) for letter, n in Counter(x).items())[0][1] for x in zip(*data)]
    return "".join(cols)


if __name__ == "__main__":
    data = get_data(DAY)
    print(data)
    # res = part1(data)
    res = part2(data)
    # print(res)
    # submit(DAY, 1, res)
    submit(DAY, 2, res)
