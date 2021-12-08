from collections import Counter

import networkx as nx
from networkx.algorithms import isomorphism

from util import *

# import solution

DAY = 8
YEAR = 2021

numbers = [
    "abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf",
    "abcdefg", "abcdfg"
]

numbers_lookup = {segments: num for num, segments in enumerate(numbers)}


def generate_graph(segment_lists):
    return nx.Graph((i, segment) for i, segments in enumerate(segment_lists)
                    for segment in segments)


def solve_pattern(patterns, outpus):
    G_base = generate_graph(numbers)
    G_pat = generate_graph(patterns)
    GM = isomorphism.GraphMatcher(G_pat, G_base)
    GM.is_isomorphic()
    output_segments = [
        "".join(sorted(GM.mapping[x] for x in part))
        for part in outpus
    ]
    return [numbers_lookup[seg] for seg in output_segments]


def solve(data):
    return [solve_pattern(patters, output) for patters, output in data]


@timing
def part1(data):
    solutions = solve(data)
    all_digs = [x for sol in solutions for x in sol]
    dig_counts = Counter(all_digs)
    return sum(dig_counts[x] for x in [1, 4, 7, 8])


def from_base(arr, base):
    res = 0
    for x in arr:
        res = res * base + x
    return res


@timing
def part2(data):
    solutions = solve(data)
    return sum(from_base(sol, 10) for sol in solutions)


def parse_subpart(part):
    return [x for x in part.strip().split()]


def parse_line(line):
    sub1, sub2 = line.split("|")
    return [*map(parse_subpart, (sub1, sub2))]


if __name__ == "__main__":
    data = [*map(parse_line, get_data(DAY, year=YEAR, raw=True).split("\n"))]
    print(data)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
