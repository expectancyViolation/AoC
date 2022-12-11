from math import prod
from typing import List, Callable, Tuple
import re

from util import *

DAY = 11
YEAR = 2022


@dataclass
class Monkey:
    held_items: List[int]
    throw_op: Callable[[int], Tuple[int, int]]
    test: int
    activity: int = 0


throw_template = """global throw_op
def throw_op(old):
    {op}
    {reduce}
    if new%{test}==0:
        return {true},new
    else:
        return {false},new
    
"""


def parse_monkey(monkey_txt: str, part2=False) -> Monkey:
    num_line, start_line, op_line, test_line, true_line, false_line = monkey_txt.split(
        "\n")
    monkey_num = int(re.match("Monkey ([0-9]+)", num_line).groups()[0])
    start_items = [int(x) for x in re.findall("[0-9]+", start_line)]
    operation = re.match(r".*Operation:\ (.*)", op_line).groups()[0]
    test_crit = int(re.match(".*divisible.*?([0-9]+)", test_line).groups()[0])
    true_target = re.match(".*true.*?([0-9]+)", true_line).groups()[0]
    false_target = re.match(".*false.*?([0-9]+)", false_line).groups()[0]
    reduce = "pass" if part2 else "new//=3"
    throw = throw_template.format(op=operation, test=test_crit,
                                  true=true_target, false=false_target,
                                  reduce=reduce)
    exec(throw)
    return Monkey(held_items=start_items, throw_op=throw_op, test=test_crit)


def simulate_monkeys(monkeys, steps=20, modular_arithmetic=False):
    max_factor = prod((monkey.test for monkey in monkeys))
    for _round in range(steps):
        for monkey in monkeys:
            for item in monkey.held_items:
                monkey.activity += 1
                target, item = monkey.throw_op(item)
                # print("item", item, target)
                monkeys[target].held_items.append(item)
                monkey.held_items = []
        if modular_arithmetic:
            for monkey in monkeys:
                monkey.held_items = [item % max_factor for item in
                                     monkey.held_items]
    activities = [monkey.activity for monkey in monkeys]
    activities.sort()
    return activities[-1] * activities[-2]


def part1(data):
    monkeys = [parse_monkey(monkey_txt)
               for monkey_txt in data.split("\n\n")]
    return simulate_monkeys(monkeys, steps=20)


def part2(data):
    monkeys = [parse_monkey(monkey_txt, part2=True)
               for monkey_txt in data.split("\n\n")]
    return simulate_monkeys(monkeys, steps=10000, modular_arithmetic=True)


if __name__ == "__main__":
    # data = get_data(DAY, year=YEAR, raw=True, filename="input/2022/11_test.txt")

    data = get_data(DAY, year=YEAR, raw=True)
    # print(data)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
