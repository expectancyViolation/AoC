from collections import defaultdict

from util import *

DAY = 9
YEAR = 2022

DIR_VECS = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, 1),
    'D': (0, -1)
}


def sign(x):
    return (x > 0) - (x < 0)


def simulate(data, tail_len=1):
    hx, hy = 0, 0
    tail = [(0, 0) for _ in range(tail_len)]
    visited = {(0, 0)}
    for dir, cnt in data:
        dx, dy = DIR_VECS[dir]
        for _ in range(cnt):
            hx, hy = hx + dx, hy + dy
            prev_x, prev_y = hx, hy
            for i, (tx, ty) in enumerate(tail):
                dtx, dty = prev_x - tx, prev_y - ty
                touching = max(abs(dtx), abs(dty)) <= 1
                if not touching:
                    dtx, dty = sign(dtx), sign(dty)
                    tx, ty = tx + dtx, ty + dty
                    tail[i] = (tx, ty)
                prev_x, prev_y = tx, ty
            visited.add(tail[-1])

    return len(visited)


def part1(data):
    return simulate(data, 1)


def part2(data):
    return simulate(data, 9)


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
