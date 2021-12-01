from util import *
from itertools import islice

DAY = 15
YEAR = 2017

MOD = (1 << 31) - 1
GEN_MOD = (1 << 16)
print(MOD, GEN_MOD)

STEPS = [16807, 48271]


def gen_vals(start, step, judge=1):
    val = start
    while True:
        val = (val * step) % MOD
        if val % judge == 0:
            yield val % GEN_MOD


def part1(data):
    gen_a, gen_b = (gen_vals(start, step) for step, start in zip(STEPS, data))
    return sum(a == b for a, b in islice(zip(gen_a, gen_b), 40_000_000))


def part2(data):
    gen_a, gen_b = (gen_vals(start, step, judge) for step, start, judge in zip(STEPS, data, (4, 8)))
    return sum(a == b for a, b in islice(zip(gen_a, gen_b), 5_000_000))


if __name__ == "__main__":
    data = [int(x[-1]) for x in get_data(DAY, year=YEAR)]
    print(data)
    # res = part1(data)
    # res = part1([65, 8921])
    res = part2(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    submit(DAY, 2, res, year=YEAR)
