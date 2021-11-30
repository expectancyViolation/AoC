from collections import defaultdict

from matplotlib import pyplot as plt

from util import *
import networkx as nx

DAY = 24
YEAR = 2017


def solve(data, score_adder, initial_score):
    neighbors = defaultdict(lambda: [])
    for i, (x, y) in enumerate(data):
        neighbors[x].append(i)
        neighbors[y].append(i)

    states = {(0, tuple()): initial_score}
    best = initial_score
    while states:
        ns = {}
        for (curr_val, visited), score in states.items():
            for nb_i in neighbors[curr_val]:
                if nb_i in visited:
                    continue
                x, y = data[nb_i]
                new_val = y if x == curr_val else x
                new_visited = tuple(sorted((*visited, nb_i)))
                new_score = score_adder(score, x, y)
                ns[(new_val, new_visited)] = new_score
                best = max(best, new_score)
        states = ns
    return best


def part1(data):
    def adder(old_val, x, y):
        return old_val + x + y

    return solve(data, adder, 0)


def part2(data):
    def adder(old_val, x, y):
        l, score = old_val
        return l + 1, score + x + y

    return solve(data, adder, (0, 0))[1]


if __name__ == "__main__":
    data = [[*map(int, x.split("/"))] for x in get_data(DAY, year=YEAR)]
    print(data)
    print(len(data))
    # res = part1(data)
    res = part2(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    submit(DAY, 2, res, year=YEAR)
