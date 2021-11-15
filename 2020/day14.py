from util import *
from collections import defaultdict
import re
from itertools import product
DAY = 14


@timing
def part1(data):
    MEM = defaultdict(lambda: 0)
    set_mask = 0
    unset_mask = (1 << 36) - 1
    for op, _, val in data:
        if m := re.match(r"^mem\[([0-9]+)\]$", op):
            val = (val | set_mask) & unset_mask
            loc = int(m[1])
            MEM[loc] = val
        else:
            set_mask = 0
            unset_mask = (1 << 36) - 1
            for i, ch in enumerate(val[::-1]):
                if ch == "1":
                    set_mask += 1 << i
                elif ch == "0":
                    unset_mask -= 1 << i
    return sum(MEM.values())


def gen_float_nums(float_bits):
    for bits in product([0, 1], repeat=len(float_bits)):
        curr = 0
        for val, i in zip(bits, float_bits):
            curr += val << i
        yield curr


@timing
def part2(data):
    MEM = defaultdict(lambda: 0)
    set_mask = 0
    float_bits = []
    for op, _, val in data:
        if m := re.match(r"^mem\[([0-9]+)\]$", op):
            loc = int(m[1])
            loc = (loc | set_mask)
            for floats in gen_float_nums(float_bits):
                float_loc = loc ^ floats
                MEM[float_loc] = val
        else:
            set_mask = 0
            float_bits = []
            for i, ch in enumerate(val[::-1]):
                if ch == "1":
                    set_mask += 1 << i
                elif ch == "X":
                    float_bits += [i]
    return sum(MEM.values())


if __name__ == "__main__":
    data = get_data(DAY)
    print(data)
    res = part1(data)
    print(res)
    #submit(DAY, 1, res)
    res = part2(data)
    print(res)
    #submit(DAY, 2, res)
