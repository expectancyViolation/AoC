import re
from itertools import product

import sympy as sp
from sympy import lambdify

from util import *

DAY = 17
YEAR = 2021

# unnecessarily complicated.
# solve for time range spent in target for each coordinate and find intersection
# sympy is slow...
vx, vy, s, t = sp.symbols("vx,vy,s,t")

py = sp.Sum(vy - s, (s, 0, t - 1)).doit()

px = sp.Sum(vx - s, (s, 0, t - 1)).doit()

b = sp.symbols("b")

F = lambdify((vx, b), sp.solve(px - b, t)[0])
G = lambdify((vx, b), sp.solve(px - b, t)[1])


def get_x_time_range(v_x, x_low, x_high):
    p = px.subs(vx, v_x)
    max_end = v_x * (v_x + 1) // 2
    if max_end >= x_low:
        t_low = F(v_x, (x_low - .5))
    else:
        t_low = inf
    if max_end >= x_high:
        t_high = F(v_x, (x_high + .5))
    else:
        t_high = inf

    return sp.ceiling(t_low), sp.floor(t_high)


def get_y_time_range(v_y, y_low, y_high):
    return sp.ceiling(G(v_y, y_high)), sp.floor(G(v_y, y_low))


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
    for x, y in product(range(1, x_high + 1), range(y_low - 2, -y_low + 2)):
        if okay(x, y):
            res += 1
    return res


def part1(_x_low, _x_high, y_low, _y_high):
    v_y = -y_low - 1
    return v_y * (v_y + 1) // 2


if __name__ == "__main__":
    raw_data = get_data(DAY, year=YEAR, raw=True)
    print(raw_data)
    data = re.match(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", raw_data).groups()
    data = [*map(int, data)]
    res = part1(*data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    res = part2(*data)
    # submit(DAY, 1, res,year=YEAR)
    # res = part2(data)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
