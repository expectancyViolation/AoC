from enum import Enum

from util import *

DAY = 19
YEAR = 2017


class DIR(Enum):
    up = (-1, 0)
    right = (0, 1)
    down = (1, 0)
    left = (0, -1)


def solve(data):
    curr_dir = DIR.down
    x, y = 0, data[0].index("|")
    res = []
    n_steps = 1
    while True:
        n_steps += 1
        dx, dy = curr_dir.value
        opposite_dir = DIR((-dx, -dy))
        x, y = x + dx, y + dy
        direction_candidates = set()
        curr_symbol = data[x][y]
        if curr_symbol.isalpha():
            res.append(curr_symbol)
        for next_direction in DIR:
            dx, dy = next_direction.value
            nx, ny = x + dx, y + dy
            if data[nx][ny] != " ":
                direction_candidates.add(next_direction)
        direction_candidates.remove(opposite_dir)
        if curr_dir in direction_candidates:
            continue
        # reached a dead end
        if not direction_candidates:
            return "".join(res), n_steps
        curr_dir = direction_candidates.pop()


def part1(data):
    return solve(data)[0]


def part2(data):
    return solve(data)[1]


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True).split("\n")
    # for line in data:
    #     print(line)
    res = part1(data)
    print(res)
    res = part2(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    # submit(DAY, 2, res,year=YEAR)
