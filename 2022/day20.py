from fractions import Fraction

from util import *

from sortedcontainers import SortedDict

DAY = 20
YEAR = 2022


@timing
def simulate(data, rounds=1):
    n = len(data)
    indices = {(x, i): Fraction(i, 1) for i, x in enumerate(data)}
    sorted_ring = SortedDict({i: x for x, i in indices.items()})
    for _round in range(rounds):
        for i, x in enumerate(data):
            ind = indices[(x, i)]
            curr_pos = sorted_ring.index(ind)
            del (sorted_ring[ind])
            new_pos = (curr_pos + x - 1) % (n - 1)
            left = sorted_ring.keys()[new_pos]
            if new_pos + 1 < n - 1:
                right = sorted_ring.keys()[(new_pos + 1)]
            else:
                right = Fraction(n, 1)
            new_ind = (left + right) / 2
            assert new_ind not in sorted_ring
            indices[(x, i)] = new_ind
            sorted_ring[new_ind] = x
    zero_ind = indices[next((x, i) for i, x in enumerate(data) if x == 0)]
    zero_pos = sorted_ring.index(zero_ind)
    res = 0
    for k in range(1, 4):
        mix_pos = (zero_pos + 1000 * k) % n
        mix_ind = sorted_ring.keys()[mix_pos]
        res += sorted_ring[mix_ind]
    return res


def part1(data):
    return simulate(data, 1)


def part2(data):
    data = [x * 811589153 for x in data]
    return simulate(data, 10)


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)

