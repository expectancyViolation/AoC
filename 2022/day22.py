import numpy as np
import matplotlib

matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

from util import *

DAY = 22
YEAR = 2022

facings = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def part1(map, path):
    L = len(map)
    l = len(map[0])
    x = 0
    y = map[x].index(".")
    facing = 0
    for step in path:
        cnt = int(step[:-1])
        turn = "LNR".index(step[-1]) - 1
        fx, fy = facings[facing]
        for _ in range(int(cnt)):
            nx, ny = x, y
            while True:
                nx, ny = (nx + fx) % L, (ny + fy) % l
                if map[nx][ny] != " ":
                    break
            if map[nx][ny] == ".":
                x, y = nx, ny
            else:
                break
        facing = (facing + turn) % 4

    print(x, y, facing)
    return 1000 * (x + 1) + 4 * (y + 1) + facing


base_vecs = {(1, 0, 0), (0, 1, 0), (0, 0, 1)}


def cross(v1, v2):
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    return y1 * z2 - z1 * y2, z1 * x2 - x1 * z2, x1 * y2 - x2 * y1


def part2(map, block_size=50):
    three_d_map = {}
    x_dir = {}
    y_dir = {}
    L = len(map)
    l = len(map[0])
    x = 0
    y = map[x].index(".")
    frontier = {(x, y)}
    three_d_map[(x, y)] = (0, 0, 0)
    distances = {(x, y): 0}
    x_dir[(x, y)] = (1, 0, 0)
    y_dir[(x, y)] = (0, 1, 0)
    while frontier:
        new_frontier = set()
        for x, y in frontier:
            tx, ty, tz = three_d_map[(x, y)]
            for dx, dy in (1, 0), (-1, 0), (0, 1), (0, -1):
                nx, ny = x + dx, y + dy
                if (nx, ny) in three_d_map:
                    continue
                if not ((0 <= nx < L) and (0 <= ny < l)):
                    continue
                if map[nx][ny] != ".":
                    continue
                if dx:
                    # crossed fold
                    xdx, xdy, xdz = x_dir[(x, y)]
                    if {x % block_size, nx % block_size} == {0, block_size - 1}:
                        ntx, nty, ntz = new_x_dir = cross((dx * xdx, dx * xdy, dx * xdz), y_dir[(x, y)])
                        assert sum(abs(a) for a in (ntx, nty, ntz)) == 1
                    else:
                        ntx, nty, ntz = 0, 0, 0
                        new_x_dir = x_dir[(x, y)]
                    three_d_map[(nx, ny)] = tx + dx * (ntx + xdx), ty + dx * (nty + xdy), tz + dx * (ntz + xdz)
                    x_dir[(nx, ny)] = new_x_dir
                    y_dir[(nx, ny)] = y_dir[(x, y)]

                elif dy:
                    # crossed fold
                    ydx, ydy, ydz = y_dir[(x, y)]
                    if {y % block_size, ny % block_size} == {0, block_size - 1}:
                        ntx, nty, ntz = new_y_dir = cross(x_dir[(x, y)], (dy * ydx, dy * ydy, dy * ydz))
                        print(ntx, nty, ntz)
                        assert sum(abs(a) for a in (ntx, nty, ntz)) == 1
                    else:
                        ntx, nty, ntz = 0, 0, 0
                        new_y_dir = y_dir[(x, y)]

                    three_d_map[(nx, ny)] = tx + dy * (ntx + ydx), ty + dy * (nty + ydy), tz + dy * (ntz + ydz)
                    y_dir[(nx, ny)] = new_y_dir
                    x_dir[(nx, ny)] = x_dir[(x, y)]
                new_frontier.add((nx, ny))
                distances[(nx, ny)] = distances[(x, y)] + 1
        frontier = new_frontier
    print(three_d_map)
    reverse_three_d_map = {p3: p2 for p2, p3 in three_d_map.items()}

    z_dir = {(x, y): cross(x_dir[(x, y)], y_dir[(x, y)]) for x, y in three_d_map}

    p = [(x, y) for x, y in three_d_map.keys() if distances[(x, y)] < 10**10]
    points = np.array([three_d_map[x] for x in p])
    nx = np.array([x_dir[x] for x in p])
    ny = np.array([y_dir[x] for x in p])
    nz = np.array([z_dir[x] for x in p])
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2])
    ax.quiver(points[:, 0], points[:, 1], points[:, 2], .3 * nx[:, 0], .3 * nx[:, 1], .3 * nx[:, 2], color="red")
    ax.quiver(points[:, 0], points[:, 1], points[:, 2], .3 * ny[:, 0], .3 * ny[:, 1], .3 * ny[:, 2], color="green")
    ax.quiver(points[:, 0], points[:, 1], points[:, 2], .3 * nz[:, 0], .3 * nz[:, 1], .3 * nz[:, 2], color="blue")
    plt.show()

    x = 0
    y = 0
    z = 0
    facing = (0, 1, 0)
    for step in path:
        cnt = int(step[:-1])
        turn = step[-1]
        for _ in range(int(cnt)):
            dx, dy, dz = facing
            nx, ny, nz = x + dx, y + dy, z + dz
            if (nx, ny, nz) in reverse_three_d_map:
                x, y, z = nx, ny, nz
            else:
                new_facing = z_dir[reverse_three_d_map[(x, y, z)]]
                dx, dy, dz = new_facing
                nx, ny, nz = nx + dx, ny + dy, nz + dz
                if (nx, ny, nz) in reverse_three_d_map:
                    x, y, z = nx, ny, nz
                    facing = new_facing
        if turn == "R":
            facing = cross(facing, z_dir[reverse_three_d_map[(x, y, z)]])
        elif turn == "L":
            dx, dy, dz = facing
            facing = cross((-dx, -dy, -dz), z_dir[reverse_three_d_map[(x, y, z)]])

    sol_x, sol_y = reverse_three_d_map[(x, y, z)]
    facing_lookup = []
    q = y_dir[(sol_x, sol_y)]
    for _ in range(4):
        facing_lookup.append(q)
        q = cross(q, z_dir[(sol_x, sol_y)])
    sol_face = facing_lookup.index(facing)
    return 1000 * (sol_x + 1) + 4 * (sol_y + 1) + sol_face


if __name__ == "__main__":
    *map, path = get_data(DAY, year=YEAR)
    # *map, path = get_data(DAY, year=YEAR, filename="input/2022/22_test.txt")
    map = [line.rstrip() for line in map]
    l_fill = max(len(line) for line in map)
    map = [line.ljust(l_fill) for line in map]
    for line in map:
        print(line)
    path = (path + "N").replace("L", "L,").replace("R", "R,").split(",")
    print(path)
    # res = part1(map, path)
    # print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(map, 50)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
