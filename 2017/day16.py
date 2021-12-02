from itertools import count
from typing import List

from util import *

DAY = 16
YEAR = 2017


def handle_move(state, move):
    instruction = move[0]
    # we need a switch statement :(
    if instruction == "s":
        spin_length = (-int(move[1:])) % len(state)
        state = state[spin_length:] + state[:spin_length]
    elif instruction == "x":
        p1, p2 = map(int, move[1:].split("/"))
        state[p1], state[p2] = state[p2], state[p1]
    elif instruction == "p":
        v1, v2 = move[1:].split("/")
        p1, p2 = state.index(v1), state.index(v2)
        state[p1], state[p2] = state[p2], state[p1]
    return state


def get_default_initial_state():
    return [chr(ord("a") + i) for i in range(16)]


def gen_steps(data, initial_state: Optional[List[str]] = None):
    if initial_state is None:
        initial_state = get_default_initial_state()
    state = [*initial_state]
    for move in data:
        state = handle_move(state, move)
        yield state


def part1(data, initial_state: Optional[str] = None):
    steps = gen_steps(data, initial_state)
    state = None
    while True:
        try:
            state = next(steps)
        except StopIteration:
            break
    return "".join(state)


def part2(data, initial_state: Optional[str] = None):
    first_seen = {}
    if initial_state is None:
        initial_state = get_default_initial_state()
    state = "".join(initial_state)
    loop_size = None
    for i in count():
        print(state)
        if state in first_seen:
            loop_size = i
            break
        first_seen[state] = i
        state = part1(data, state)
    steps = (10 ** 9) % loop_size
    return next(val for val, i in first_seen.items() if i == steps)


if __name__ == "__main__":
    instructions = get_data(DAY, year=YEAR, raw=True).split(",")
    # data = ["s1", "x3/4", "pe/b"]
    # # res = part1(data)
    res = part2(instructions)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    # submit(DAY, 2, res, year=YEAR)
