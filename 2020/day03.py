from util import get_data, submit
from functools import reduce
from operator import mul

DAY = 3


def tree_hits(data, dx, dy):
    h = len(data)
    w = len(data[0])
    return sum(data[dx * i][(dy * i) % w] == "#" for i in range(0, h // dx))


def part1(data):
    return tree_hits(data, dx=1, dy=3)


def part2(data):
    directions = ((1, 1), (1, 3), (1, 5), (1, 7), (2, 1))
    return reduce(mul, (tree_hits(data, dx, dy) for dx, dy in directions))


if __name__ == "__main__":
    data = get_data(DAY)
    #print(data)
    result1 = part1(data)
    print(f"result for part 1: {result1}")
    #submit(DAY, 1, result1)
    result2 = part2(data)
    print(f"result for part 2: {result2}")
    #submit(DAY, 2, result2)
