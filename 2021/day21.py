from collections import defaultdict
from functools import lru_cache
from itertools import islice, count, cycle, product
from util import *

DAY = 21
YEAR = 2021


def gen_rolls():
    for i, roll_count in zip(cycle(range(1, 101)), count(1)):
        yield i, roll_count


def gen_sum(dice):
    while True:
        rolls = [*islice(dice, 3)]
        res = sum(v for v, _c in rolls)
        yield res, rolls[-1][-1]


def part1(data):
    data = [*data]
    die = gen_rolls()
    rolls = gen_sum(die)
    values = [0, 0]
    for i in count():
        index = i % 2
        rolled, roll_count = next(rolls)
        data[index] = ((data[index] + rolled - 1) % 10) + 1
        values[index] += data[index]
        if values[index] >= 1000:
            return values[1 - index] * roll_count


@lru_cache()
def get_die_poss(die_size=3):
    res = defaultdict(lambda: 0)
    for rolls in product(range(1, die_size + 1), repeat=3):
        res[sum(rolls)] += 1
    print(res)
    return res


@timing
def part2(data, score_limit=21, die_size=3):
    states = defaultdict(lambda: 0, {(tuple(data), (0, 0), 0): 1})
    wins = [0, 0]
    # visited = {*states}
    while states:
        new_states = defaultdict(lambda: 0)
        for rolled, poss in get_die_poss(die_size).items():
            for (positions, scores, next_player), count in states.items():
                pos_ = [*positions]
                sco_ = [*scores]
                pos_[next_player] = ((pos_[next_player] + rolled - 1) % 10) + 1
                sco_[next_player] += pos_[next_player]
                if sco_[next_player] >= score_limit:
                    wins[next_player] += count * poss
                else:
                    new_states[(tuple(pos_), tuple(sco_),
                                1 - next_player)] += count * poss
        states = new_states
        # visited |= {*states}
    # state_space_size = (10 * score_limit) ** 2 * 2
    # print(f"visited {len(visited)} out of {state_space_size}")
    return max(wins)


if __name__ == "__main__":
    data = [int(line[-1]) for line in get_data(DAY, year=YEAR)]
    # data = [4, 8]
    print(data)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
