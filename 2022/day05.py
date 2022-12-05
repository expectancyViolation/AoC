from collections import deque, defaultdict

from util import *

DAY = 5
YEAR = 2022


def parse_initial_state(inital_state_str):
    lines = inital_state_str.split("\n")
    stacks = defaultdict(deque)
    for line in lines[:-1][::-1]:
        for i, val in enumerate(line[1::4]):
            if val.isalpha():
                stacks[i].append(val)
    return stacks


def gen_parse_moves(move_str):
    moves = move_str.split("\n")
    for line in moves:
        amount, from_stack, to_stack = [int(x) for x in line.split()[1::2]]
        yield amount, from_stack, to_stack


def part1(data):
    inital_state, moves = data.split("\n\n")
    stacks = parse_initial_state(inital_state)
    for amount, from_stack, to_stack in gen_parse_moves(moves):
        for _ in range(amount):
            stacks[to_stack - 1].append(stacks[from_stack - 1].pop())
    result = "".join(stack.pop() for stack in stacks.values())
    return result


def part2(data):
    inital_state, moves = data.split("\n\n")
    stacks = [[*stack] for stack in parse_initial_state(inital_state)]
    for amount, from_stack, to_stack in gen_parse_moves(moves):
        stacks[to_stack - 1].extend(stacks[from_stack - 1][-amount:])
        stacks[from_stack - 1] = stacks[from_stack - 1][:-amount]
    result = "".join(stack.pop() for stack in stacks)
    return result


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
