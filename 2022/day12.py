from util import *

DAY = 12
YEAR = 2022


def get_elevation(letter):
    if letter in "SE":
        letter = "az"["SE".index(letter)]
    return ord(letter) - ord("a") + 1


def bfs(data, start_set):
    L = len(data)
    l = len(data[0])
    frontier = {*start_set}
    distances = {x: 0 for x in start_set}
    while frontier:
        new_frontier = set()
        for (x, y) in frontier:
            current_elevation = get_elevation(data[x][y])
            for dx, dy in (-1, 0), (1, 0), (0, 1), (0, -1):
                nx, ny = x + dx, y + dy
                if not ((0 <= nx < L) and (0 <= ny < l)):
                    continue
                new_elevation = get_elevation(data[nx][ny])
                if new_elevation - current_elevation > 1:
                    continue
                if (nx, ny) not in distances:
                    distances[(nx, ny)] = distances[(x, y)] + 1
                    new_frontier.add((nx, ny))
        frontier = new_frontier

    target_pos = next(
        (i, j) for i, row in enumerate(data) if (j := row.find("E")) != -1)
    return distances[target_pos]


def part1(data):
    curr_pos = next(
        (i, j) for i, row in enumerate(data) if (j := row.find("S")) != -1)
    return bfs(data, {curr_pos})


def part2(data):
    start_pos = {
        (i, j) for i, row in enumerate(data) for j, letter in enumerate(row) if
        letter in "Sa"}
    return bfs(data, start_pos)


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR,filename="input/2022/onHk.txt")
    #print(data)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
