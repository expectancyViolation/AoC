import re
from timeit import timeit

from util import *

DAY = 1
YEAR = 2023

written_letter_regex = "(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine)"
letter_regex = "[0-9]"

combined_regex = f"(?=({letter_regex})|{written_letter_regex})"


# (non-regular) lookahead matching to allow for word overlap
# regex match is a 10-tuple with exactly one non-trivial element
# its index is the number it represents
#   except for the element at 0 which is just a regular digit

def solve(regex):
    def get_match_val(match):
        if match[0] != '':
            return match[0]
        return next(i for i, x in enumerate(match) if x != "")

    def get_val(line):
        found = re.findall(regex, str(line))
        found_vals = [get_match_val(m) for m in found]
        return int(f"{found_vals[0]}{found_vals[-1]}")

    return sum(get_val(line) for line in data)


def part1(data):
    return solve(letter_regex)


def part2(data):
    return solve(combined_regex)


if __name__ == "__main__":
    data = get_data(DAY, filename="input/2023/day01_bigboy",year=YEAR)

    res = part1(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)

    res = part2(data)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
