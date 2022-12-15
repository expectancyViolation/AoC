import re
from collections import defaultdict
from itertools import product

from util import *

DAY = 15
YEAR = 2022


def manhattan(x, y, a, b):
    return abs(x - a) + abs(y - b)


def parse_input(data):
    stations = []
    beacons = []
    for row in data:
        res = map(int, re.findall("(-?[0-9]+)", row))
        sx, sy, bx, by = res
        d = manhattan(bx, by, sx, sy)
        stations += [(sx, sy, d)]
        beacons += [(bx, by)]
    return stations, beacons

# interval union using 1-d line scan
@timing
def part1(data):
    line_y = 2000000
    stations, beacons = parse_input(data)
    beacons = {x for x, y in beacons if y == line_y}
    spots_of_interest = [(x, 0) for x in beacons]
    for sx, sy, d in stations:
        dy = abs(sy - line_y)
        dx = d - dy
        if dx > 0:
            spots_of_interest += [(sx - dx, 1)]
            spots_of_interest += [(sx + dx + 1, -1)]

    total = 0
    depth = 0
    last_x = None
    for x, d in sorted(spots_of_interest):
        if depth > 0:
            total += (x - last_x)
            if d == 0:
                total -= 1
        depth += d
        last_x = x

    return res


# since we know there is a unique solution
#   at least 4 scan areas have to border the distress beacon
#   to cover all surrounding squares
# consider lines that pass along the "outside" border of the scan areas
#   the two diagonal lines containing the distress beacon both have to
#   occur at least twice to cover the 4 "diagonal" neighbors of the beacon
# so the only candidates are intersections of such "multi-occurrence" diagonals
# since there are only 4*n_scanner border lines this is a fast solution
@timing
def part2(data):
    stations, _beacons = parse_input(data)
    line_counts = defaultdict(lambda: 0)
    for sx, sy, d in stations:
        for a, b in product([-1, 1], repeat=2):
            # identify line by its parameters m,b (f(x)=m*x+b)
            line = (a, sy + b * (d + 1) - a * sx)
            line_counts[line] += 1
    multi_lines = {
        lines
        for lines, counts in line_counts.items() if counts >= 2
    }

    up_lines, down_lines = ({y
                             for x, y in multi_lines if x == k}
                            for k in (1, -1))

    coord_limit = 4_000_000
    for y1, y2 in product(up_lines, down_lines):
        y = (y1 + y2) // 2
        x = (y2 - y1) // 2
        if (0 <= x <= coord_limit) and (0 <= y <= coord_limit):
            if all(manhattan(x, y, sx, sy) > d for sx, sy, d in stations):
                return x * coord_limit + y


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True).split("\n")
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    # p2_loop(data)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
