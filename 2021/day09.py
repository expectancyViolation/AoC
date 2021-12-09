from math import prod

from disjoint_set import DisjointSet

from util import *

DAY = 9
YEAR = 2021


@timing
def get_risks(lines):
    L = len(lines)
    l = len(lines[0])
    indices = [[int(z) for z in line] for line in lines]
    ds = DisjointSet()
    for x, line in enumerate(indices):
        for y, z in enumerate(line):
            if z == 9:
                continue
            for (dx, dy) in (1, 0), (-1, 0), (0, 1), (0, -1), (0, 0):
                nx, ny = x + dx, y + dy
                if 0 <= nx < L and 0 <= ny < l:
                    val = indices[nx][ny]
                    if val <= z:
                        ds.union((x, y), (nx, ny))
    # sinks = {(x, y) for _, (x, y) in ds}
    sinks = {min((indices[x][y], (x,y)) for x,y in basin) for basin in ds.itersets()}
    sinks = {pos for _, pos in sinks}
    sizes = sorted(
        [sum(1 for x in basin) for basin in ds.itersets()])
    p1 = sum(1 + indices[x][y] for x, y in sinks)
    p2 = prod(sizes[-3:])
    return p1, p2


if __name__ == "__main__":
    raw_data = get_data(DAY, year=YEAR,
                        raw=True)
    # raw_data = get_data(DAY, filename="input/2021/09_bigboi.txt", year=YEAR,
    #                     raw=True)
    data = raw_data.split("\n")
    part1, part2 = get_risks(data)
    print(part1)
    # submit(DAY, 1, part1,year=YEAR)
    print(part2)
    # submit(DAY, 2, part2, year=YEAR)
