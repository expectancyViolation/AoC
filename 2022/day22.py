import numpy as np
import matplotlib

matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

from util import *

DAY = 22
YEAR = 2022

facings = [(0, 1), (1, 0), (0, -1), (-1, 0)]


@timing
def part1(map_, path):
    L = len(map_)
    l = len(map_[0])
    x = 0
    y = map_[x].index(".")
    facing = 0
    for step in path:
        cnt = int(step[:-1])
        turn = "LNR".index(step[-1]) - 1
        fx, fy = facings[facing]
        for _ in range(int(cnt)):
            nx, ny = x, y
            while True:
                nx, ny = (nx + fx) % L, (ny + fy) % l
                if map_[nx][ny] != " ":
                    break
            if map_[nx][ny] == ".":
                x, y = nx, ny
            else:
                break
        facing = (facing + turn) % 4

    return 1000 * (x + 1) + 4 * (y + 1) + facing


base_vecs = {(1, 0, 0), (0, 1, 0), (0, 0, 1)}


def cross(v1, v2):
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    return y1 * z2 - z1 * y2, z1 * x2 - x1 * z2, x1 * y2 - x2 * y1


def add(v1, v2):
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    return x1 + x2, y1 + y2, z1 + z2


def scale(a, v):
    x, y, z = v
    return a * x, a * y, a * z


# floodfill map_ keeping track of the 3d cube positions and axis orientations
#  during crossings of "folds" (cube-edges; position only dependent on cube size)
# 3d point coordinates are centered on the faces of the cube (start position is at origin)
# 3d surface normals point "inwards" into the cube
def floodfill_fold_3d(map_, start_pos, cube_size=50):
    three_d_map_ = {}
    x_dir = {}
    y_dir = {}
    L = len(map_)
    l = len(map_[0])
    x, y = start_pos
    frontier = {(x, y)}
    three_d_map_[(x, y)] = (0, 0, 0)
    distances = {(x, y): 0}
    x_dir[(x, y)] = (1, 0, 0)
    y_dir[(x, y)] = (0, 1, 0)
    while frontier:
        new_frontier = set()
        for x, y in frontier:
            t_pos = three_d_map_[(x, y)]
            for dx, dy in (1, 0), (-1, 0), (0, 1), (0, -1):
                nx, ny = x + dx, y + dy
                if (nx, ny) in three_d_map_:
                    continue
                if not ((0 <= nx < L) and (0 <= ny < l)):
                    continue
                if map_[nx][ny] != ".":
                    continue
                if dx:
                    x_step = x_dir[(x, y)]
                    if {x % cube_size, nx % cube_size} == {0, cube_size - 1}:
                        # crossed fold
                        x_dir[(nx, ny)] = cross(scale(dx, x_step), y_dir[(x, y)])
                        x_step = add(x_step, x_dir[(nx, ny)])
                    else:
                        x_dir[(nx, ny)] = x_dir[(x, y)]
                    three_d_map_[(nx, ny)] = add(t_pos, scale(dx, x_step))
                    y_dir[(nx, ny)] = y_dir[(x, y)]

                elif dy:
                    y_step = y_dir[(x, y)]
                    if {y % cube_size, ny % cube_size} == {0, cube_size - 1}:
                        # crossed fold
                        y_dir[(nx, ny)] = cross(x_dir[(x, y)], scale(dy, y_step))
                        y_step = add(y_step, y_dir[(nx, ny)])
                    else:
                        y_dir[(nx, ny)] = y_dir[(x, y)]
                    three_d_map_[(nx, ny)] = add(t_pos, scale(dy, y_step))
                    x_dir[(nx, ny)] = x_dir[(x, y)]
                new_frontier.add((nx, ny))
                distances[(nx, ny)] = distances[(x, y)] + 1
        frontier = new_frontier

    return three_d_map_, x_dir, y_dir


def draw_cube(three_d_map_, x_dir, y_dir):
    z_dir = {(x, y): cross(x_dir[(x, y)], y_dir[(x, y)]) for x, y in three_d_map_}
    p = [(x, y) for x, y in three_d_map_.keys()]
    points = np.array([three_d_map_[x] for x in p])
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


@timing
def part2(map_, path, cube_size=50):
    start_pos = (0, map_[0].index("."))
    three_d_map_, x_dir, y_dir = floodfill_fold_3d(map_, start_pos, cube_size)

    z_dir = {(x, y): cross(x_dir[(x, y)], y_dir[(x, y)]) for x, y in three_d_map_}
    reverse_three_d_map_ = {p3: p2 for p2, p3 in three_d_map_.items()}

    curr_pos = (0, 0, 0)
    facing = (0, 1, 0)
    for step in path:
        cnt = int(step[:-1])
        turn = step[-1]
        for _ in range(int(cnt)):
            new_pos = add(curr_pos, facing)
            if new_pos in reverse_three_d_map_:
                curr_pos = new_pos
            else:
                # try crossing a fold (by additionally stepping "inwards" in surface normal direction)
                new_facing = z_dir[reverse_three_d_map_[curr_pos]]
                new_pos = add(new_pos, new_facing)
                if new_pos in reverse_three_d_map_:
                    curr_pos = new_pos
                    facing = new_facing
        if turn == "R":
            facing = cross(facing, z_dir[reverse_three_d_map_[curr_pos]])
        elif turn == "L":
            dx, dy, dz = facing
            facing = cross((-dx, -dy, -dz), z_dir[reverse_three_d_map_[curr_pos]])

    sol_x, sol_y = reverse_three_d_map_[curr_pos]
    draw_cube(three_d_map_,x_dir,y_dir)
    # generate 3d facing lookup by rotating the 3d y-direction (corresponding to 2d (0,1)) clockwise
    facing_lookup = []
    q = y_dir[(sol_x, sol_y)]
    for _ in range(4):
        facing_lookup.append(q)
        q = cross(q, z_dir[(sol_x, sol_y)])
    sol_face = facing_lookup.index(facing)
    return 1000 * (sol_x + 1) + 4 * (sol_y + 1) + sol_face


def parse_input(data):
    *map_, my_path = data
    map_ = [line.rstrip() for line in map_]
    l_fill = max(len(line) for line in map_)
    map_ = [line.ljust(l_fill) for line in map_]
    path = (my_path + "N").replace("L", "L,").replace("R", "R,").split(",")
    return map_, path


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR,filename="input/2022/22_test.txt")
    my_map, my_path = parse_input(data)
    res = part1(my_map, my_path)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(my_map, my_path, cube_size=4)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
