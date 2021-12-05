from util import *

DAY = 4
YEAR = 2021

DRAWN = -1


def parse_grid(grid):
    return [[*map(int, x.split())] for x in grid.split("\n")]


def unmarked_grid_sum(grid):
    return sum(sum(y for y in x if y != DRAWN) for x in grid)


def is_won(grid):
    row_win = any(
        all(x == DRAWN for x in grid[i]) for i in range(len(grid)))
    column_win = any(
        all(grid[j][i] == DRAWN for j in range(len(grid)))
        for i in range(len(grid[0])))
    return row_win or column_win


def mark(grid, num):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == num:
                grid[i][j] = DRAWN


def gen_win_order(data):
    nums = [*map(int, data[0].split(","))]
    grids = {i: parse_grid(grid) for i, grid in enumerate(data[1:])}
    for num in nums:
        for grid_num, grid in [*grids.items()]:
            mark(grid, num)
            if is_won(grid):
                yield unmarked_grid_sum(grid) * num
                grids.pop(grid_num)


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True).split("\n\n")
    part1, *_, part2 = gen_win_order(data)
    print("part1", part1)
    print("part2", part2)
    # submit(DAY, 1, part1, year=YEAR)
    # submit(DAY, 2, part2, year=YEAR)
