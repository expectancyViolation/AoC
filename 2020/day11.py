from util import *
from copy import deepcopy
import numpy as np
from collections import defaultdict
from scipy.signal import convolve2d
from itertools import product, count

DAY = 11

NB_STENCIL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

AND = np.logical_and
NOT = np.logical_not
OR = np.logical_or


@timing
def simulate(seats, nb_count, nb_limit):
    occupied = np.zeros(seats.shape, dtype=np.bool)
    for i in count():
        print(i)
        last_occupied = occupied.copy()
        neighbor_count = nb_count(occupied)
        potentially_occupied = AND(OR(neighbor_count == 0, occupied),
                                   NOT(neighbor_count >= nb_limit))
        occupied = AND(seats, potentially_occupied)
        if np.array_equal(occupied, last_occupied):
            return np.sum(occupied)


@timing
def part1(seats):
    neighbor_count = lambda occupied: convolve2d(
        occupied, NB_STENCIL, mode="same")
    return simulate(seats, neighbor_count, 4)


@timing
def part2(seats):
    seat_x, seat_y = seats.nonzero()
    neighbors = defaultdict(lambda: [])
    for _, (dx, dy) in enumerate(product([-1, 0, 1], repeat=2)):
        if dx == 0 == dy:
            continue
        directional_neighbors = defaultdict(lambda: [])
        for sx, sy in zip(seat_x, seat_y):
            directional_neighbors[sx * dx + sy * dy] += [(sx, sy)]
        for line in directional_neighbors.values():
            line.sort(key=lambda tup: tup[0] * dy - tup[1] * dx)
            for j in range(1, len(line)):
                neighbors[line[j - 1]] += [line[j]]
    # this is insanely slow
    # dict lookups and unnecessary tuple/list/array instances
    def neighbor_count(occupied):
        return np.array([[
            sum(occupied[x, y] for x, y in neighbors[(X, Y)])
            for Y in range(len(seats[0]))
        ] for X in range(len(seats))])

    return simulate(seats, neighbor_count, 5)


if __name__ == "__main__":
    data = get_data(DAY)
    seats = np.array([[x == 'L' for x in line] for line in data])
    res = part1(seats)
    print(res)
    #print(seats.shape)
    res = part2(seats)
    print(res)
    #submit(DAY, 1, res)
    #submit(DAY, 2, res)
