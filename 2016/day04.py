import re
from collections import Counter

from util import *

DAY = 4
YEAR = 2016


def split(row):
    room_regex = r"([a-z]+)([0-9]+)\[([a-z]+)\]"
    return re.match(room_regex, row.replace("-", "")).groups()


def is_real(name, checksum):
    top_scores = sorted(
        (-n, letter) for letter, n in Counter(name).items())[:5]
    actual_checksum = "".join(letter for _, letter in top_scores)
    return actual_checksum == checksum


def part1(data):
    return sum(
        int(sector) for name, sector, checksum in map(split, data)
        if is_real(name, checksum))


def rotate(text, n):
    return "".join(chr(ord('a') + (ord(x) - ord('a') + n) % 26) for x in text)


def part2(data):
    for name, sector, checksum in map(split, data):
        rotated = rotate(name, int(sector))
        if "north" in rotated:
            return sector


if __name__ == "__main__":
    my_input = get_data(DAY, year=YEAR)
    # print(my_input)

    # res = part1(my_input)
    # res = part2(my_input)
    # submit(DAY, 1, res)
    # submit(DAY, 2, res)
