from itertools import count

import util

DAY = 25
YEAR = 2021


def step(cucumbers):
    L = len(cucumbers)
    l = len(cucumbers[0])
    moved = False
    for symbol, di, dj in (">", 0, 1), ("v", 1, 0):
        new_state = [[x if x != symbol else "." for x in line]
                     for line in cucumbers]
        for i, row in enumerate(cucumbers):
            for j, x in enumerate(row):
                if x == symbol:
                    ni, nj = (i + di) % L, (j + dj) % l
                    if cucumbers[ni][nj] == ".":
                        new_state[ni][nj] = symbol
                        moved = True
                    else:
                        new_state[i][j] = symbol
        cucumbers = new_state
    return new_state, moved


@util.timing
def part1(cucumbers):
    for i in count(1):
        cucumbers, moved = step(cucumbers)
        if not moved:
            return i


if __name__ == "__main__":
    raw_data = util.get_data(DAY, year=YEAR, raw=True)
    data = [[*row] for row in raw_data.split("\n")]
    print(data)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
