from collections import defaultdict
from functools import cache

from util import *

DAY = 24
YEAR = 2022

dirs = [(0, 1), (-1, 0), (0, -1), (1, 0)]


@timing
def solve(data):
    blizzards = defaultdict(set)

    L = len(data)
    l = len(data[0])

    for i, row in enumerate(data):
        for j, x in enumerate(row):
            try:
                facing = ">^<v".index(x)
                blizzards[(i, j)].add(facing)
            except Exception as e:
                pass

    @cache
    def get_blizzard_state(time: int):
        # print("get", time)
        if time == 0:
            return blizzards
        prev_blizzards = get_blizzard_state(time - 1)
        new_blizzards = defaultdict(set)
        for (x, y), facings in prev_blizzards.items():
            for facing in facings:
                dx, dy = dirs[facing]
                nx, ny = ((x + dx - 1) % (L - 2)) + 1, (
                        (y + dy - 1) % (l - 2)) + 1
                new_blizzards[(nx, ny)].add(facing)
        return new_blizzards

    def get_neighbors(state):
        x, y, time = state
        assert len(get_blizzard_state(time)[(x, y)]) == 0
        next_blizzard_state = get_blizzard_state(time + 1)
        for dx, dy in dirs + [(0, 0)]:
            nx, ny = x + dx, y + dy
            if not ((0 <= nx < L) and (0 <= ny < l)):
                continue
            if data[nx][ny] == "#":
                continue
            if len(next_blizzard_state[(nx, ny)]):
                # print("cannot move", nx, ny)
                continue
            yield (nx, ny, time + 1), 1

    goal_x = L - 1
    goal_y = data[L - 1].index(".")

    start_x = 0
    start_y = data[0].index(".")

    def get_check_coord_same(check_x, check_y):
        def check(state):
            x, y, time = state
            return x == check_x and y == check_y

        return check

    def get_dist_heuristic(check_x, check_y):
        def heuristic(state):
            x, y, time = state
            return abs(x - check_x) + abs(y - check_y)

        return heuristic

    is_final_goal = get_check_coord_same(goal_x, goal_y)
    heuristic_goal = get_dist_heuristic(goal_x, goal_y)
    is_final_start = get_check_coord_same(start_x, start_y)
    heuristic_start = get_dist_heuristic(start_x, start_y)

    search = a_star_search

    cost_to, _came_from, current_to = search(get_neighbors,
                                             (start_x, start_y, 0),
                                             is_final_goal,
                                             heuristic_goal)

    cost_fro, _came_from, current_fro = search(get_neighbors,
                                               current_to,
                                               is_final_start,
                                               heuristic_start)

    cost_to_again, _came_from, current_to_again = search(get_neighbors,
                                                         current_fro,
                                                         is_final_goal,
                                                         heuristic_goal)

    return current_to[-1], current_to_again[-1]


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    part1, part2 = solve(data)
    print(part1)
    # submit(DAY, 1, part1,year=YEAR)
    print(part2)
    # submit(DAY, 2, part2,year=YEAR)
