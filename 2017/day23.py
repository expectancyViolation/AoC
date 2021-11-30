from collections import defaultdict
from math import gcd

from util import *
import sympy as sp

DAY = 23
YEAR = 2017


inst_lookup=["set","sub","mul","jnz"]

def run(data, debug_switch=True):
    for d in data:
        d[0]=inst_lookup.index(d[0])
    registers = defaultdict(lambda: 0)
    if not debug_switch:
        registers["a"] = 1

    def get_value(arg):
        if isinstance(arg, str):
            return registers[arg]
        return arg

    call_count = defaultdict(lambda: 0)

    pointer = 0

    while 0 <= pointer < len(data):
        inst, x, y = data[pointer]

        call_count[inst] += 1
        pointer += 1
        if inst == 0:
            registers[x] = get_value(y)
        elif inst == 1:
            registers[x] -= get_value(y)
        elif inst == 2:
            registers[x] *= get_value(y)
        elif inst == 3:
            if get_value(x) != 0:
                pointer += get_value(y) - 1
    return registers, call_count


def part1(data):
    _regs, call_count = run(data)
    return call_count["mul"]


def part2(data):
    res = 0
    for i in range(109900, 126901, 17):
        res += not sp.isprime(i)
    return res


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    print(data)
    # res = part1(data)
    res = part2(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    # submit(DAY, 2, res,year=YEAR)
