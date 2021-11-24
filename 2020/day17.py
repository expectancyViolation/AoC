from collections import defaultdict
from itertools import product

from util import *

DAY = 17


def step(locations):
    neighbors = defaultdict(lambda: 0)
    # sample random location for the dimension:
    dim = len(next(x for x in locations))
    for d_vec in product([-1, 0, 1], repeat=dim):
        if not any(d_vec):
            continue
        for vec in locations:
            neighbors[tuple(x + dx for x, dx in zip(vec, d_vec))] += 1
    new_locations = set()
    for loc in locations:
        if 2 <= neighbors[loc] <= 3:
            new_locations.add(loc)
    for loc, nbs in neighbors.items():
        if nbs == 3 and loc not in locations:
            new_locations.add(loc)
    return new_locations


@timing
def simulate(locations, n_steps=6):
    for n in range(n_steps):
        locations = step(locations)
        print(len(locations))
    return len(locations)


if __name__ == "__main__":
    data = get_data(DAY)
    locations_3d = {(i, j, 0)
                    for i, line in enumerate(data)
                    for j, val in enumerate(line)
                    if val == "#"}
    res_1 = simulate(locations_3d)
    print(res_1)
    # submit(DAY, 1, res_1)
    locations_4d = {(*pos, 0) for pos in locations_3d}
    res_2 = simulate(locations_4d)
    print(res_2)

    locations_100d = {tuple([*pos] + [0] * 97) for pos in locations_3d}
    res_2 = simulate(locations_100d)
    print(res_2)
    # submit(DAY, 2, res_2)
