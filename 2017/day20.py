import re
from math import isqrt

import numpy as np

from util import *

DAY = 20
YEAR = 2017


def parse_line(line):
    m = re.findall(r"(\w)\=\<(\-?\d+)\,(\-?\d+)\,(\-?\d+)\>", line)
    return {att: np.array([*map(int, rest)]) for att, *rest in m}


def part1(data):
    particles = [*map(parse_line, data)]
    a_min, i_min = min(
        (sorted(map(abs, p["a"])), i) for i, p in enumerate(particles))
    return i_min


NN = "NN"


def solve_quadratic_integer(a, b, c):
    if a == 0:
        if b == 0:
            return NN if c == 0 else None
        if c % b != 0:
            return None
        return {2 * (-c) // b}
    d_sq = b**2 - 4 * a * c
    if d_sq < 0:
        return None
    d = isqrt(d_sq)
    if d**2 != d_sq:
        return None
    t = -b + d
    if t % a != 0:
        return None
    return {t // a, (-b - d) // a}


def simulate(particle, t):
    res = []
    for a, v, p in zip(*[particle[x] for x in "avp"]):
        for _ in range(t):
            v += a
            p += v
        res += [2 * p]
    return tuple(res)


def get_quadratic_coefficients(a, v, p):
    return a, 3 * a + 2 * v, 2 * (a + p + v)


def calculate(particle, t):
    t = t - 1
    res = []
    for a, v, p in zip(*[particle[x] for x in "avp"]):
        a, b, c = get_quadratic_coefficients(a, v, p)
        res += [a * t**2 + b * t + c]
    return tuple(res)


@timing
def part2(data):
    particles = [*map(parse_line, data)]
    A = np.array([p['a'] for p in particles])
    V = np.array([p['v'] for p in particles])
    P = np.array([p['p'] for p in particles])
    for _ in range(1000):
        V += A
        P += V
        _, indices, cnts = np.unique(P,
                                     return_index=True,
                                     return_counts=True,
                                     axis=0)
        remaining_indices = indices[cnts == 1]
        A = A[remaining_indices]
        V = V[remaining_indices]
        P = P[remaining_indices]
    return len(P)


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True).split("\n")
    print(data)
    # res = part1(data)
    res = part2(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    # submit(DAY, 2, res, year=YEAR)
