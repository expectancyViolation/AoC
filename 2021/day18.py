import json
from functools import reduce
from itertools import combinations

from llist import dllist

from util import *

DAY = 18
YEAR = 2021


def gen_inorder(num, d=0):
    if isinstance(num, int):
        yield [num, d]
    else:
        yield from gen_inorder(num[0], d + 1)
        yield from gen_inorder(num[1], d + 1)


def to_list(num):
    return dllist([*gen_inorder(num)])


def explode(l: dllist):
    node = l.first
    while node:
        if node.next:
            val, depth = node.value
            next_val, next_depth = node.next.value
            if depth > 4 and depth == next_depth:
                if node.prev:
                    node.prev.value[0] += node.value[0]
                node.value[0] = 0
                node.value[1] -= 1
                l.remove(node.next)
                if node.next:
                    node.next.value[0] += next_val
                return True
        node = node.next
    return False


def split(l: dllist):
    node = l.first
    while node:
        val, depth = node.value
        if val >= 10:
            lval, rval = val // 2, val - val // 2
            l.insertafter([rval, depth + 1], node)
            node.value = [lval, depth + 1]
            return True
        node = node.next
    return False


def reduce_number(l):
    while explode(l) or split(l):
        pass


def add(l1, l2):
    res = dllist([[x, d + 1] for x, d in (*l1, *l2)])
    reduce_number(res)
    return res


# calculating magnitude in list representation is a bit more involved
# keep track of left (3) and right (2) "tree-factors"
def magnitude(l):
    stack = []
    prod = 1
    res = 0
    for val, depth in l:
        while depth > len(stack):
            stack.append(3)
            prod *= 3
        res += prod * val
        while stack and stack[-1] == 2:
            prod //= 2
            stack.pop()
        if stack and stack[-1] == 3:
            stack[-1] = 2
            prod = prod // 3 * 2
    return res


@timing
def part1(data):
    return magnitude(reduce(add, data))


@timing
def part2(data):
    return max(
        magnitude(add(l1, l2)) for x, y in combinations(data, 2)
        for l1, l2 in ((x, y), (y, x)))


if __name__ == "__main__":
    data_raw = get_data(DAY, year=YEAR, raw=True)
    data = [to_list(json.loads(x)) for x in data_raw.split("\n")]
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
