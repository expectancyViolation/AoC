from collections import defaultdict
from itertools import combinations, product, count

import numpy as np

from util import *

DAY = 23
YEAR = 2022


def draw_positions(p):
    x_min, x_max = min(x for x, y in p), max(x for x, y in p)
    y_min, y_max = min(y for x, y in p), max(y for x, y in p)

    arr = np.zeros([x_max + 1 - x_min, y_max + 1 - y_min], dtype=int)
    for x, y in p:
        arr[x - x_min, y - y_min] = 1
    res = 0
    for row in arr:
        res += sum(i == 0 for i in row)
        print("".join(".#"[i] for i in row))
    return res


def gen_step(data):
    positions = {(i, j) for i, row in enumerate(data) for j, x in enumerate(row) if x == "#"}
    rules = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while True:
        new_positions = defaultdict(lambda: [])
        moved = False
        for x, y in positions:
            has_nb = False
            for dx, dy in product((-1, 0, 1), repeat=2):
                if dx == dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                has_nb |= ((nx, ny) in positions)
            if not has_nb:
                new_positions[(x, y)].append((x, y))
                continue
            proposed = False
            for dx, dy in rules:
                p1 = nx, ny = x + dx, y + dy
                d1 = nx + dy, ny + dx
                d2 = nx - dy, ny - dx
                if any(p in positions for p in (p1, d1, d2)):
                    continue
                # print(x, y, "move", nx, ny)
                new_positions[p1].append((x, y))
                proposed = True
                break
            if not proposed:
                new_positions[(x, y)].append((x, y))
        for p_new, p_olds in [*new_positions.items()]:
            if len(p_olds) > 1:
                del (new_positions[p_new])
                for p_old in p_olds:
                    new_positions[p_old] = [p_old]
        positions = {p for p, arr in new_positions.items() if len(arr) == 1}
        rules = rules[1:] + rules[:1]
        yield positions, any(x != y for x, [y] in new_positions.items())


def part1(data):
    simulate = gen_step(data)
    for _ in range(10):
        positions, changed = next(simulate)
    return draw_positions(positions)


def part2(data):
    simulate = gen_step(data)
    for i in count(1):
        _positions, changed = next(simulate)
        if not changed:
            return i


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    print(data)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
