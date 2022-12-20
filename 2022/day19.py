import re
from collections import defaultdict
from functools import cache
from math import prod

from util import *

DAY = 19
YEAR = 2022

ressource_names = ["ore", "clay", "obsidian", "geode"]


# slow, but all pruning should be safe (i.e. optimality of result is guaranteed)
def solve(rule_set, duration=24):
    def could_buy(resources, rule):
        return all(x >= y for x, y in zip(resources, rule))

    # keep track of first occurrence of state
    # later occurrences can be pruned
    earliest = {}

    ore_max = max(rule[0] for rule in rule_set)
    clay_max = max(rule[1] for rule in rule_set)
    obs_max = max(rule[2] for rule in rule_set)

    best_so_far = 0

    earliest_fill = defaultdict(lambda: 1000000000)

    @cache
    def sol(robots, resources, time):
        nonlocal best_so_far

        can_afford_geode = could_buy(resources, rule_set[-1])

        # assuming buying a geode robot each turn is possible
        best_possible = resources[-1] + robots[-1] * time + (
                time - 1 + can_afford_geode) * (time - 2 + can_afford_geode) // 2

        # prune if better score is impossible
        if best_possible <= best_so_far:
            return 0

        if all(x >= y for x, y in zip(robots, rule_set[-1])):
            if all(x >= y for x, y in zip(resources, rule_set[-1])):
                stute = (robots[-1], resources[-1])
                if earliest_fill[stute] > time:
                    offset = resources[-1] + robots[-1] * time + time * (time - 1) // 2
                    if offset > best_so_far:
                        print(offset)
                    best_so_far = offset
                    return offset


        if time == 1:
            new_best = max(best_so_far, resources[-1] + robots[-1])
            if new_best > best_so_far:
                print(new_best)
            best_so_far = new_best
            return resources[-1] + robots[-1]

        if (robots, resources) in earliest and earliest[(robots,
                                                         resources)] >= time:
            return 0
        earliest[(robots, resources)] = time
        res = 0

        # no buy (only if there is a non-affordable rule)
        # if all rules are affordable there cannot be a reason for "saving"

        for i, rule in enumerate(rule_set):
            if i == 0:
                # don't buy ore miner, when supply already guaranteed
                if robots[0] >= ore_max:
                    continue
                # don't buy ore miner late,since not worth
                if time <= rule[0]:
                    continue
            # don't buy clay miner, when supply already guaranteed
            if i == 1 and robots[1] >= clay_max:
                continue

            if i == 2 and robots[2] >= obs_max:
                continue

            if could_buy(resources, rule):
                new_robots = [*robots]
                new_robots[i] += 1
                new_robots = tuple(new_robots)
                new_resources = [
                    x - y + z for x, y, z in zip(resources, rule, robots)
                ]
                # if supply is guaranteed enforce cap
                if new_robots[0] >= ore_max:
                    new_resources[0] = min(ore_max, new_resources[0])
                if new_robots[1] >= clay_max:
                    new_resources[1] = min(clay_max, new_resources[1])
                if new_robots[2] >= obs_max:
                    new_resources[2] = min(obs_max, new_resources[1])
                new_resources = tuple(new_resources)
                res = max(res, sol(new_robots, new_resources, time - 1))

        if not all(could_buy(resources, rule) for rule in rule_set):
            new_resources = tuple([x + y for x, y in zip(robots, resources)])
            res = max(res, sol(robots, new_resources, time - 1))

        return res

    return sol((1, 0, 0, 0), (0, 0, 0, 0), duration)


def gen_parse_rulesets(data):
    for line in data:
        rules = []
        for rule in line.split(":")[1].split(".")[:-1]:
            cost = re.findall("([0-9]+ [a-z]+)", rule)
            in_rule = [0] * len(ressource_names)
            for x in cost:
                amount, ressource = x.split()
                amount = int(amount)
                in_rule[ressource_names.index(ressource)] = amount
            rules.append(tuple(in_rule))
        yield rules


@timing
def part1(data):
    sols = pool.map(solve, [*gen_parse_rulesets(data)])
    return sum(x * y for x, y in enumerate(sols, start=1))


@timing
def part2(data):
    sols = pool.starmap(solve, [(x, 32) for x in gen_parse_rulesets(data[:3])])
    return prod(sols)


import multiprocessing as mp

if __name__ == "__main__":
    pool = mp.Pool(mp.cpu_count())
    # data = get_data(DAY, year=YEAR, raw=True,filename="input/2022/19_test.txt").strip().split("\n")
    data = get_data(DAY, year=YEAR, raw=True).strip().split("\n")
    res = part1(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
    pool.close()
