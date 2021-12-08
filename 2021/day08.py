from collections import Counter
from itertools import permutations

from util import *

DAY = 8
YEAR = 2021

# TODO: really slow use non-string representations?


numbers = [
    "abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf",
    "abcdefg", "abcdfg"
]

sorted_nums = sorted(numbers)

numbers_lookup = {segments: num for num, segments in enumerate(numbers)}


def map_parts(parts, mapping):
    return ["".join(mapping[x] for x in part) for part in parts]


def check_mapping(parts, mapping):
    mapped_parts = map_parts(parts, mapping)
    sorted_mapped_parts = sorted(
        ["".join(sorted(part)) for part in mapped_parts])
    return sorted_mapped_parts == sorted_nums


def solve_pattern(patterns, output):
    for mapping_order in permutations("abcdefg"):
        mapping = {x: y for x, y in zip("abcdefg", mapping_order)}
        if not check_mapping(patterns, mapping):
            continue
        mapped_output = map_parts(output, mapping)
        return [numbers_lookup["".join(sorted(x))] for x in mapped_output]


def solve(data):
    res = []
    for patters, output in data:
        res += [solve_pattern(patters, output)]
    return res


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
