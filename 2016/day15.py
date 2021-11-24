import re
from sympy.ntheory.modular import crt

from util import *

DAY = 15
YEAR = 2016


def parse_line(line):
    m = re.findall(r"(\d+)", line)
    disk, n_position, _time, initial_state = map(int, m)
    # disk is the time offset
    return n_position, (-initial_state - disk) % n_position


def part1(data):
    disks = [*map(parse_line, data)]
    n, _ = crt(*zip(*disks))
    return int(n)


def part2(data):
    disks = [*map(parse_line, data)]
    disks += [(11, (-(len(disks) + 1)) % 11)]
    n, _ = crt(*zip(*disks))
    return int(n)


test_input = """Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1."""

if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True).split("\n")
    print(data)
    # res = part1(data)
    # res = part1(test_input.split("\n"))
    res = part2(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    # submit(DAY, 2, res, year=YEAR)
