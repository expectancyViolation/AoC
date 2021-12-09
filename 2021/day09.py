from collections import Counter
from math import prod

from util import *

DAY = 9
YEAR = 2021


@timing
def get_risks(lines):
    indices = {(int(x), int(y)): int(z)
               for x, line in enumerate(lines) for y, z in enumerate(line)}
    sink_target = {}
    low_to_high = sorted(indices.items(), key=lambda tup: tup[1])
    for i, ((x, y), z) in enumerate(low_to_high):
        if z == 9:
            break
        for dx, dy in (-1, 0), (1, 0), (0, 1), (0, -1):
            nb = (x + dx, y + dy)
            if nb in sink_target:
                sink_target[(x, y)] = sink_target[nb]
                break
        else:
            sink_target[(x, y)] = (x, y)

    sinks = {*sink_target.values()}
    sizes = sorted(Counter(sink_target.values()).values())
    p1 = sum(1 + indices[(x, y)] for x, y in sinks)
    p2 = prod(sizes[-3:])
    return p1, p2


if __name__ == "__main__":
    raw_data = get_data(DAY, year=YEAR, raw=True)
    data = raw_data.split("\n")
    part1, part2 = get_risks(data)
    print(part1)
    # submit(DAY, 1, part1,year=YEAR)
    print(part2)
    # submit(DAY, 2, part2, year=YEAR)
