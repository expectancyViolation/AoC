from copy import deepcopy
from functools import reduce
from itertools import combinations

from util import *

DAY = 18
YEAR = 2021


def add_leftmost(num, val):
    if isinstance(num[0], int):
        num[0] += val
    else:
        add_leftmost(num[0], val)


def add_rightmost(num, val):
    if isinstance(num[1], int):
        num[1] += val
    else:
        add_rightmost(num[1], val)


def step(num):
    stepped, *_ = check_explode(num)
    if not stepped:
        stepped = check_split(num)
    return stepped


def reduce_num(num):
    while step(num):
        # print(num)
        pass
    return num


def add(num1, num2):
    return reduce_num([deepcopy(num1), deepcopy(num2)])


def check_explode(num, depth=0):
    if isinstance(num, int):
        return False, None, None
    if isinstance(num[0], int) and isinstance(num[1], int):
        if depth >= 4:
            return True, *num
        return False, None, None
    # check left explode
    exploded, left_push, right_push = check_explode(num[0], depth + 1)
    if exploded:
        # direct explosion
        if left_push is not None and right_push is not None:
            num[0] = 0
        if right_push is not None:
            if isinstance(num[1], int):
                num[1] += right_push
            else:
                add_leftmost(num[1], right_push)
        return exploded, left_push, None
    # check right explode
    exploded, left_push, right_push = check_explode(num[1], depth + 1)
    if exploded:
        if left_push is not None and right_push is not None:
            num[1] = 0
        if left_push is not None:
            if isinstance(num[0], int):
                num[0] += left_push
            else:
                add_rightmost(num[0], left_push)
        return exploded, None, right_push
    return False, None, None


def check_split(num):
    if isinstance(num, int):
        return False
    split = False
    if isinstance(num[0], int):
        if num[0] >= 10:
            num[0] = [num[0] // 2, num[0] - num[0] // 2]
            split = True
    else:
        split = check_split(num[0])
    if split:
        return True
    if isinstance(num[1], int):
        if num[1] >= 10:
            num[1] = [num[1] // 2, num[1] - num[1] // 2]
            split = True
    else:
        split = check_split(num[1])
    return split


def magnitude(num):
    if isinstance(num, int):
        return num
    return 3 * magnitude(num[0]) + 2 * magnitude(num[1])


def part1(data):
    res = reduce(add, data)
    return magnitude(res)


def part2(data):
    res = max(magnitude(add(a, b))
              for x, y in combinations(data, 2)
              for a, b in ((x, y), (y, x)))
    return res


if __name__ == "__main__":
    data_raw = get_data(DAY, year=YEAR, raw=True)
    data = [eval(x) for x in data_raw.split("\n")]
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
