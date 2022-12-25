from util import *

DAY = 23
YEAR = 2015


def simulate(data, a_val):
    position = 0
    regs = {"a": a_val, "b": 0}
    while 0 <= position < len(data):
        inst, *args = data[position]
        if inst == "jio":
            reg, diff = args
            if regs[reg.strip(",")] == 1:
                position += diff
                continue
        if inst == "jie":
            reg, diff = args
            if regs[reg.strip(",")] % 2 == 0:
                position += diff
                continue
        elif inst == "jmp":
            offset, *_ = args
            position += offset
            continue
        elif inst == "inc":
            reg, *_ = args
            regs[reg] += 1
        elif inst == "tpl":
            reg, *_ = args
            regs[reg] *= 3
        elif inst == "hlf":
            reg, *_ = args
            regs[reg] //= 2
        position += 1
    return regs["b"]


def part1(data):
    return simulate(data, a_val=0)


def part2(data):
    return simulate(data, a_val=1)


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
