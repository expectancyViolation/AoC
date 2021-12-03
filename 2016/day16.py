from util import *

DAY = 16
YEAR = 2016


def inflate(data):
    return data + [0] + [1 - x for x in data[::-1]]


def checksum(data):
    while len(data) % 2 == 0:
        data = [
            1 if data[i] == data[i + 1] else 0 for i in range(0, len(data), 2)
        ]
    return "".join(map(str, data))


def solve(data, n=272):
    while len(data) < n:
        data = inflate(data)
    return checksum(data[:n])


def part1(data):
    return solve(data)


def part2(data):
    return solve(data, n=35651584)


assert checksum([*map(int, "110010110100")]) == "100"

if __name__ == "__main__":
    data = [*map(int, get_data(DAY, year=YEAR, raw=True))]
    print(data)
    # res = part1(data)
    res = part2(data)
    # print(res)
    # submit(DAY, 1, res,year=YEAR)
    submit(DAY, 2, res, year=YEAR)
