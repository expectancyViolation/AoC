from functools import reduce
from itertools import repeat, cycle, islice
from operator import xor

from util import *

DAY = 10
YEAR = 2017


def round(data, pos=0, skip=0, N=256):
    state = [*range(N)]
    pos %= N
    state = state[pos:] + state[:pos]
    for length in data:
        state[:length] = state[:length][::-1]
        move = (length + skip) % N
        state = state[move:] + state[:move]
        pos -= move
        skip += 1
    pos %= N
    state = state[pos:] + state[:pos]
    return state[0] * state[1], state


def part1(data):
    return round(data)[0]


def knot_hash(data: str):
    start = [ord(x) for x in data] + [17, 31, 73, 47, 23]
    sparse_hash = round(islice(cycle(start), 64 * len(start)))[1]
    dense_hash = [reduce(xor, sparse_hash[i:i + 16]) for i in range(0, 256, 16)]
    return "".join(f"{x:02x}" for x in dense_hash)


def part2(data):
    return knot_hash(data)


if __name__ == "__main__":
    data = [int(x) for x in get_data(DAY, year=YEAR, raw=True).split(",")]
    # res = part1(data)

    data = get_data(DAY, year=YEAR, raw=True)
    res = part2(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    # submit(DAY, 2, res,year=YEAR)
