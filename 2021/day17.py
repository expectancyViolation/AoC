import re
from functools import lru_cache
from itertools import product
from math import sqrt, floor, ceil

# import sympy as sp
# from sympy import lambdify

from util import *

DAY = 17
YEAR = 2021


# unnecessarily complicated.
# solve for time range spent in target for each coordinate and find intersection
# sympy is slow...
# vx, vy, s, t = sp.symbols("vx,vy,s,t")
#
# py = sp.Sum(vy - s, (s, 0, t - 1)).doit()
#
# px = sp.Sum(vx - s, (s, 0, t - 1)).doit()
#
# b = sp.symbols("b")
#
# F = lambdify((vx, b), sp.solve(px - b, t)[0])
# G = lambdify((vx, b), sp.solve(px - b, t)[1])
# print(sp.solve(px - b, t)[0])
# print(sp.solve(px - b, t)[1])


def F(vx, b):
    return vx - sqrt(-8 * b + 4 * vx ** 2 + 4 * vx + 1) / 2 + 1 / 2


def G(vx, b):
    return vx + sqrt(-8 * b + 4 * vx ** 2 + 4 * vx + 1) / 2 + 1 / 2


@lru_cache(maxsize=10 ** 10)
def get_x_time_range(v_x, x_low, x_high):
    max_end = v_x * (v_x + 1) // 2
    t_low = ceil(F(v_x, (x_low - .5))) if max_end >= x_low else inf
    t_high = F(v_x, (x_high + .5)) if max_end >= x_high else inf
    return t_low, t_high

@lru_cache(maxsize=10 ** 10)
def get_y_time_range(v_y, y_low, y_high):
    return ceil(G(v_y, y_high)), floor(G(v_y, y_low))


def get_is_ok(x_low, x_high, y_low, y_high):
    def is_ok(v_x, v_y):
        t_y_low, t_y_high = get_y_time_range(v_y, y_low, y_high)
        t_x_low, t_x_high = get_x_time_range(v_x, x_low, x_high)
        low = max(t_y_low, t_x_low)
        high = min(t_y_high, t_x_high)
        return low <= high

    return is_ok


@timing
def part2(x_low, x_high, y_low, y_high):
    okay = get_is_ok(x_low, x_high, y_low, y_high)
    res = 0
    x_s = []
    for x in range(1, x_high + 1):
        a, b = get_x_time_range(x, x_low, x_high)
        if a <= b:
            x_s.append(x)
    y_s = []
    for y in range(y_low - 2, -y_low + 2):
        a, b = get_y_time_range(y, y_low, y_high)
        if a <= b:
            y_s.append(y)

    for x, y in product(x_s, y_s):
        res += okay(x, y)
    return res


# DANGER: only works since there is a v_x for any t>0
#   that gives a hit in the x coordinate
def part1(_x_low, _x_high, y_low, _y_high):
    v_y = -y_low - 1
    return v_y * (v_y + 1) // 2


if __name__ == "__main__":
    raw_data = get_data(DAY, year=YEAR, raw=True)
    data = re.match(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)",
                    raw_data).groups()
    data = [*map(int, data)]
    res = part1(*data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    res = part2(*data)
    # submit(DAY, 1, res,year=YEAR)
    # res = part2(data)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
