from collections import defaultdict
from enum import Enum

from util import *

DAY = 22
YEAR = 2017

# "clean" but slow
# Enums and dict lookups :/


class DIR(Enum):
    up = (-1, 0)
    right = (0, 1)
    down = (1, 0)
    left = (0, -1)


DIR_ORDER = [*DIR]


class States(Enum):
    clean = 0
    infected = 1
    weakened = 2
    flagged = 3


def simulate(area_map, n_steps, state_map=None, turn_delta_map=None):
    if state_map is None:
        state_map = {
            States.infected: States.clean,
            States.clean: States.infected
        }
    if turn_delta_map is None:

        def turn_delta_map(state):
            return 1 if state == States.infected else -1

    x, y = 0, 0
    dir_index = 0
    infectious_bursts = 0
    for _ in range(n_steps):
        state = area_map[(x, y)]
        dir_index = (dir_index + turn_delta_map(state)) % 4
        new_state = state_map[state]
        infectious_bursts += new_state == States.infected
        area_map[(x, y)] = new_state
        dx, dy = DIR_ORDER[dir_index].value
        x, y = x + dx, y + dy
    return infectious_bursts


def part1(data):
    return simulate(data, 10000)


@timing
def part2(data):
    state_map = {
        States.clean: States.weakened,
        States.weakened: States.infected,
        States.infected: States.flagged,
        States.flagged: States.clean
    }

    def turn_delta_map(state):
        if state == States.clean:
            return -1
        elif state == States.weakened:
            return 0
        elif state == States.infected:
            return 1
        else:
            return 2

    return simulate(data,
                    10000000,
                    state_map=state_map,
                    turn_delta_map=turn_delta_map)


TEST_DATA = """..#
#..
..."""

if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True)
    # data=TEST_DATA
    data = data.split("\n")
    L, l = len(data), len(data[0])
    print(L, l)
    data = defaultdict(
        lambda: States.clean, {(i - L // 2, j - l // 2):
                               States.infected if y == "#" else States.clean
                               for i, x in enumerate(data)
                               for j, y in enumerate(x)})
    print(data)
    # res = part1(data)
    res = part2(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    # submit(DAY, 2, res, year=YEAR)
