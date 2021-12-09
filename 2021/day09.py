from math import prod

from disjoint_set import DisjointSet

from util import *

DAY = 9
YEAR = 2021

@timing
def get_risks(lines):
    indices = {(int(x), int(y)): int(z)
               for x, line in enumerate(lines) for y, z in enumerate(line)}
    ds = DisjointSet()
    for i, ((x, y), z) in enumerate(indices.items()):
        val, nx, ny = min((indices[(nx, ny)], nx, ny)
                          for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1))
                          if (nx := (x + dx), ny := (y + dy)) in indices
                          if not (dx == 0 == dy))
        if val < z:
            ds.union((x, y), (nx, ny))
    sinks = {(x, y) for _, (x, y) in ds}
    sizes = sorted(
        [sum(1 for x in basin if indices[x] != 9) for basin in ds.itersets()])
    p1 = sum(1 + indices[(x, y)] for x, y in sinks)
    p2 = prod(sizes[-3:])
    return p1, p2


if __name__ == "__main__":
    raw_data = get_data(DAY, year=YEAR, raw=True)
    data = raw_data.split("\n")
    part1,part2 = get_risks(data)
    print(part1)
    # submit(DAY, 1, part1,year=YEAR)
    print(part2)
    # submit(DAY, 2, part2, year=YEAR)
