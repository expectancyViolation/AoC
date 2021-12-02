from util import *

DAY = 2
YEAR = 2021


def part1(data):
    x, y = 0, 0
    for inst, dist in data:
        if inst == "forward":
            x += int(dist)
        elif inst == "down":
            y += int(dist)
        elif inst == "up":
            y -= int(dist)
        else:
            raise
    return x * y


def part2(data):
    x, y, aim = 0, 0, 0
    for inst, dist in data:
        if inst == "forward":
            x += int(dist)
            y += aim * int(dist)
        elif inst == "down":
            aim += int(dist)
        elif inst == "up":
            aim -= int(dist)
        else:
            raise
    return x * y


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    print(data)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
