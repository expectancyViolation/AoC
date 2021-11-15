from collections import Counter, defaultdict

import numpy as np

from util import get_data, submit, timing

DAY = 10


def sort_jolt(data):
    in_order = sorted(data)
    device = in_order[-1] + 3
    return [0] + in_order + [device]


@timing
def part1(data):
    in_order = sort_jolt(data)
    diffs = np.diff(in_order)
    diff_counts = Counter(diffs)
    return diff_counts[1] * (diff_counts[3])


@timing
def part2(data):
    in_order = sort_jolt(data)
    poss = defaultdict(lambda: 0, {0: 1})
    for x in in_order[1:]:
        poss[x] = sum(poss[y] for y in range(max(0, x - 3), x))
    return poss[in_order[-1]]


if __name__ == "__main__":
    my_data = get_data(DAY)
    #print(my_data)

    res = part1(my_data)
    print(res)
    #submit(DAY, 1, res)

    res = part2(my_data)
    print(res)
    #submit(DAY, 2, res)
