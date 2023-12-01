from collections import Counter

from util import *

DAY = 3
YEAR = 2022


def get_priority(letter):
    upper = letter.isupper()
    reference_letter = 'A' if upper else 'a'
    return ord(letter) - ord(reference_letter) + 1 + 26 * upper


def get_line_score1(line):
    assert len(line) % 2 == 0
    l = len(line) // 2
    intersection = set(line[:l]) & set(line[l:])
    common_letter = intersection.pop()
    return get_priority(common_letter)


def part1(data):
    return sum(get_line_score1(line) for line in data)


def part2(data):
    bags = [set(row) for row in data]
    res = 0
    for chunk_start in range(0, len(bags), 3):
        common_letter = set.intersection(
            *bags[chunk_start:chunk_start + 3]).pop()
        res += get_priority(common_letter)
    return res


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
