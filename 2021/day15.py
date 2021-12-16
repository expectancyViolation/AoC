import numpy as np

from util import *

DAY = 15
YEAR = 2021


def part1(data):
    L = len(data)
    l = len(data[0])

    def get_neighbors(pos):
        x, y = pos
        for dx, dy in (-1, 0), (1, 0), (0, 1), (0, -1):
            nx, ny = x + dx, y + dy
            if 0 <= nx < L and 0 <= ny < l:
                yield (nx, ny), data[nx][ny]

    def heur(state):
        x, y = state
        return 0

    res, came_from = a_star_search(get_neighbors, (0, 0),
                                   lambda x: x == (L - 1, l - 1),
                                   heur)

    visited = {(L - 1, l - 1)}
    curr = (L - 1, l - 1)
    while curr != (0, 0):
        curr = came_from[curr]
        visited.add(curr)
    A=np.zeros([L,l],dtype=np.uint8)
    for x,y in visited:
        A[x,y]=1
    for line in A:
        print("".join("x" if x else " " for x in line))

    return res


@timing
def part2(data):
    return part1(data)


if __name__ == "__main__":
    raw_data = get_data(DAY, year=YEAR, raw=True)
    # raw_data = datata
    data = [[int(x) for x in line] for line in raw_data.split("\n")]
    L = len(data)
    l = len(data[0])
    data2 = [[((data[x % L][y % L] + y // l + x // L - 1) % 9) + 1 for y in
              range(5 * l)] for x in range(5 * L)]
    res = part1(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    res = part2(data2)
    # print(res)
    # submit(DAY, 2, res, year=YEAR)
