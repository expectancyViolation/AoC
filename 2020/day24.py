import re
import numpy as np
from collections import Counter, defaultdict
from util import get_data, submit, timing

DAY = 24

A = np.array

DIRECTIONS = {
    "e": A((1, 0)),
    "nw": A((0, 1)),
    "ne": A((1, 1)),
    "w": A((-1, 0)),
    "sw": A((-1, -1)),
    "se": A((0, -1))
}


def get_start_tiles(data):
    pattern = re.compile("|".join(DIRECTIONS))
    end_positions = [
        tuple(sum(DIRECTIONS[step] for step in pattern.findall(tile)))
        for tile in data
    ]
    tile_counts = Counter(end_positions)
    return [x for x, c in tile_counts.items() if c % 2 == 1]


@timing
def part1(data):
    black_tiles = get_start_tiles(data)
    return len(black_tiles)


def step(locations):
    neighbors = defaultdict(lambda: 0)
    for dx, dy in DIRECTIONS.values():
        for x, y in locations:
            neighbors[(x + dx, y + dy)] += 1
    new_locations = set()
    for loc in locations:
        if 1 <= neighbors[loc] <= 2:
            new_locations.add(loc)
    for loc, nbs in neighbors.items():
        if nbs == 2 and loc not in locations:
            new_locations.add(loc)
    return new_locations


@timing
def part2(data):
    black_tiles = get_start_tiles(data)
    for i in range(100):
        black_tiles = step(black_tiles)
        #print(len(black_tiles))
    return len(black_tiles)


if __name__ == "__main__":
    data = get_data(DAY)
    #print(data)

    res = part1(data)
    print(res)
    #submit(DAY, 1, res)

    res = part2(data)
    print(res)
    #submit(DAY, 2, res)
