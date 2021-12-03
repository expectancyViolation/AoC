from util import *

DAY = 19
YEAR = 2016


def step(arr):
    is_odd = len(arr) % 2
    arr = arr[::2]
    if is_odd:
        arr = arr[1:]
    return arr


def solve(n):
    still_in = [*range(1, n + 1)]
    while len(still_in) > 1:
        still_in = step(still_in)
    return still_in[0]


def part1(data):
    return solve(data)


@timing
def part2(n):
    number_to_left = {x: (x + 1) % n for x in range(n)}
    before_opposite = n // 2 - 1
    step = n % 2
    while before_opposite != number_to_left[before_opposite]:
        number_to_left[before_opposite] = number_to_left[
            number_to_left[before_opposite]]
        if step:
            before_opposite = number_to_left[before_opposite]
        step = 1 - step
        # print(number_to_left, before_opposite)
    return before_opposite + 1


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)[0]
    print(data)
    res = part1(data)
    res = part2(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    # submit(DAY, 2, res, year=YEAR)
    # too low 1420278
