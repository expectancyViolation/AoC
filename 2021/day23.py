from collections import defaultdict
from copy import deepcopy
from itertools import combinations
from math import inf

import networkx as nx

import util

DAY = 23
YEAR = 2021

goal_positions = {
    "A": tuple((i, 3) for i in range(2, 6)),
    "B": tuple((i, 5) for i in range(2, 6)),
    "C": tuple((i, 7) for i in range(2, 6)),
    "D": tuple((i, 9) for i in range(2, 6)),
}

cost_factor = {"A": 1, "B": 10, "C": 100, "D": 1000}


def get_draw(input):
    empty = [[x if x in ("#", " ") else "." for x in l] for l in input]

    def draw_position(positions):
        lul = deepcopy(empty)
        for (i, j), letter in positions:
            lul[i][j] = letter
        for line in lul:
            print("".join(line))

    return draw_position


def get_gen_neighbors(G):
    def gen_neighbors(positions):
        letter = positions[0][1]
        letter_count = sum(1 for x in positions if x[1] == letter)
        positions = {x: y for x, y in positions}
        for pos, letter in positions.items():
            distances = defaultdict(lambda: inf, {pos: 0})
            frontier = {pos}
            while frontier:
                curr = frontier.pop()
                for nb in G.neighbors(curr):
                    if nb not in positions and nb not in distances:
                        distances[nb] = distances[curr] + G[curr][nb]["weight"]
                        frontier.add(nb)
            for x, d in distances.items():
                i, j = x
                u, v = pos
                # cannot move in hall after stopping
                if u == i == 1:
                    continue
                if i >= 2:
                    # can only move into own goal
                    goals = goal_positions[letter]
                    if x not in goals:
                        continue
                    # and only if no "wrong" amphipods are in goal
                    if any(positions[x] != letter for x in goals
                           if x in positions):
                        continue
                    # # speedup: always scoot all the way back
                    if any(y not in positions for y in goals[goals.index(x) + 1:letter_count]):
                        # print("skipping move to", letter, x, goals[goals.index(x) + 1:], positions)
                        continue
                if x == pos:
                    continue
                new_positions = {
                    p: l
                    for p, l in positions.items() if p != pos
                }
                new_positions[x] = letter
                nt = tuple(sorted(
                    new_positions.items()))
                yield nt, d * cost_factor[letter]

    return gen_neighbors


def to_graph(input):
    G = nx.Graph()
    L = len(input)
    l = len(input[0])
    positions = {}
    neighbors = defaultdict(lambda: 0)
    for i, line in enumerate(input):
        for j, x in enumerate(line):
            if x in ("#", " "):
                continue
            if x != ".":
                positions[(i, j)] = x
            for di, dj in (-1, 0), (1, 0), (0, 1), (0, -1):
                ni, nj = i + di, j + dj
                if 0 <= ni < L and 0 <= nj < l and input[ni][nj] != "#":
                    G.add_edge((i, j), (ni, nj), weight=1)
                    neighbors[(i, j)] += 1
    for (i, j), count in neighbors.items():
        if count >= 3:
            for x, y in combinations(G.neighbors((i, j)), 2):
                G.add_edge(x, y, weight=2)
            G.remove_node((i, j))
    return G, positions


@util.timing
def solve(data):
    G, positions = to_graph(data)
    gen_neighbors = get_gen_neighbors(G)

    draw = get_draw(data)

    def is_final(positions):
        for pos, letter in positions:
            if pos not in goal_positions[letter]:
                return False
        return True

    def heur(positions):
        positions = {x: y for x, y in positions}
        open_goals = {
            letter: {x for x in g if (x not in positions) or (positions[x] != letter)}
            for letter, g in goal_positions.items()
        }
        cost = 0
        for (i, j), letter in positions.items():
            if (i, j) not in goal_positions[letter]:
                k, l = open_goals[letter].pop()
                curr_cost = abs(k - i) + abs(l - j)
                curr_cost += (l != j) * (min(k, i) - 1) * 2
                cost += curr_cost * cost_factor[letter]

        return cost

    cost, came_from, current = util.a_star_search(
        gen_neighbors, tuple(sorted(positions.items())), is_final, heur)
    chain = [current]
    while current in came_from:
        current = came_from[current]
        if current:
            chain += [current]
    for x in chain[::-1]:
        print("")
        draw(x)
    return cost


inset = """  #D#C#B#A#
  #D#B#A#C#"""

if __name__ == "__main__":
    raw_data = util.get_data(DAY, year=YEAR, raw=True)
    data = raw_data.split("\n")
    inset_split = inset.split("\n")
    res = solve(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    data2 = data[:3] + inset_split + data[3:]
    res = solve(data2)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
