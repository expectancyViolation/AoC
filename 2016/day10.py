import re
from collections import defaultdict
from math import prod

from util import *

DAY = 10


def gen_simulate(data):
    bot_holding = defaultdict(lambda: set())
    bot_rules = {}
    outputs = {}
    for line in data:
        if m := re.match("value (\d+) goes to bot (\d+)", line):
            val, bot = map(int, m.groups())
            bot_holding[bot].add(val)
        elif m := re.match("bot (\d+) gives low to ((?:bot)|(?:output)) (\d+) and high to ((?:bot)|(?:output)) (\d+)",
                           line):
            bot, target_low, low, target_high, high = m.groups()
            bot, low, high = map(int, (bot, low, high))
            target_low_is_bot, target_high_is_bot = [x == "bot" for x in (target_low, target_high)]
            bot_rules[bot] = ((target_low_is_bot, low), (target_high_is_bot, high))
    multi_holding_bots = (bot for bot, holding in bot_holding.items() if len(holding) > 1)
    current_bots = set(multi_holding_bots)
    print(bot_holding)
    while current_bots:
        current_bot = current_bots.pop()
        if not current_bot in bot_rules:
            continue
        low_val, high_val = sorted(bot_holding[current_bot])
        bot_holding.pop(current_bot)
        if {low_val, high_val} == {61, 17}:
            yield current_bot
        (target_low_is_bot, low_bot), (target_high_is_bot, high_bot) = bot_rules[current_bot]
        if target_low_is_bot:
            bot_holding[low_bot].add(low_val)
        else:
            outputs[low_bot] = low_val
        if target_high_is_bot:
            bot_holding[high_bot].add(high_val)
        else:
            outputs[high_bot] = high_val
        for bot in low_bot, high_bot:
            if len(bot_holding[bot]) >= 2:
                current_bots.add(bot)
    yield prod(outputs[i] for i in range(3))



if __name__ == "__main__":
    data = get_data(DAY, raw=True).split("\n")
    simulate=gen_simulate(data)
    # part 1:
    res = next(simulate)
    print(res)
    # submit(DAY, 1, res)
    res = next(simulate)
    print(res)
    submit(DAY, 2, res)
