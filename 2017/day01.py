from util import *

DAY = 1
YEAR = 2017


def part1(data):
    return 0


def part2(data):
    n = len(data)
    return 2 * sum(
        int(data[i]) for i in range(n // 2) if data[i] == data[i + n // 2])


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True)
    print(data)
    # res = part1(data)
    res = part2(data)
    # res = part2("12131415")
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    submit(DAY, 2, res, year=YEAR)

    # too high 80325
    # too low 754
