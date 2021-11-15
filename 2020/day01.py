from itertools import combinations

from util import get_data, submit, timing


@timing
def part1(nums):
    opposites = {2020 - num for num in nums}
    x = next(x for x in nums if x in opposites)
    return (2020 - x) * x


@timing
def part2(nums):
    opposites = {2020 - x - y: (x, y) for x, y in combinations(nums, 2)}
    z = next(z for z in nums if z in opposites)
    x, y = opposites[z]
    return x * y * z


if __name__ == "__main__":
    data = get_data(1)
    # sol = part1(data)
    # submit(1, 1, sol)
    sol = part2(data)
    submit(1, 2, sol)
