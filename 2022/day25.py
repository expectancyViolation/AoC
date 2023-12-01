from util import *

DAY = 25
YEAR = 2022


def from_snafu(num: str):
    res = 0
    curr = 1
    for s in num[::-1]:
        dig = "=-012".index(s) - 2
        res += dig * curr
        curr *= 5
    return res


def to_snafu(num: int):
    res = []
    carry = 0
    while num:
        last_dig = (num % 5 + carry)
        res.append("012=-"[last_dig % 5])
        carry = last_dig > 2
        num //= 5
    if res[-1] in "=-":
        res.append("1")
    return "".join(res[::-1])


def part1(data):
    res = sum(from_snafu(line) for line in data)
    return to_snafu(res)


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True).split("\n")
    res = part1(data)
    print(res)
