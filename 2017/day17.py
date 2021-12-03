from util import *
from collections import deque

DAY = 17
YEAR = 2017


# dequee has O(k) for k shift
# O(1) shift should be possible
# but still quick enough
def apply_lock(rot, n):
    data = deque([0])
    for i in range(1, n + 1):
        if i % 100000 == 0:
            print(i / n)
        data.rotate(-rot - 1)
        data.appendleft(i)
    return data


def part1(rot):
    return apply_lock(rot, 2017)[1]


def part2(rot):
    data = apply_lock(rot, 50000000)
    arr = [*data]
    return arr[arr.index(0) + 1]


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)[0]
    print(data)
    # res = part1(data)
    res = part2(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    submit(DAY, 2, res, year=YEAR)
