import re
from itertools import combinations, permutations

from util import *

DAY = 21
YEAR = 2016


def apply_instruction(state, instruction):
    if m := re.match(r"^swap position (\d+) with position (\d+)$",
                     instruction):
        p1, p2 = map(int, m.groups())
        state[p1], state[p2] = state[p2], state[p1]
    elif m := re.match(r"^swap letter (\w+) with letter (\w+)$", instruction):
        p1, p2 = [state.index(x) for x in m.groups()]
        state[p1], state[p2] = state[p2], state[p1]
    elif m := re.match(r"^rotate (\w+) (\d+) steps?$", instruction):
        dir, num = m.groups()
        num = int(num) * (1 if dir == "left" else -1)
        assert dir in ("left", "right")
        state = state[num:] + state[:num]
    elif m := re.match(r"^rotate based on position of letter (\w+)$",
                       instruction):
        letter = m.group(1)
        n = (state.index(letter))
        n = (1 + n + (n >= 4)) % len(state)
        state = state[-n:] + state[:-n]
    elif m := re.match(r"^reverse positions (\d+) through (\d+)$",
                       instruction):
        p1, p2 = map(int, m.groups())
        state[p1:p2 + 1] = state[p1:p2 + 1][::-1]
    elif m := re.match(r"^move position (\d+) to position (\d+)$",
                       instruction):
        p1, p2 = map(int, m.groups())
        letter = state[p1]
        state = state[:p1] + state[p1 + 1:]
        state = state[:p2] + [letter] + state[p2:]
    else:
        print(f"unparsable:{instruction}")
    return state


def part1(data, initial_state=None):
    if initial_state is None:
        initial_state = [*"abcdefgh"]
    state = initial_state
    for instruction in data:
        state = apply_instruction(state, instruction)
    return "".join(state)


def part2(data):
    # force of the brute
    for initial_state in permutations("abcdefgh"):
        res = part1(data, [*initial_state])
        if res == "fbgdceah":
            return "".join(initial_state)


instruction_sequence = [
    "swap position 4 with position 0", "swap letter d with letter b",
    "reverse positions 0 through 4", "rotate left 1 step",
    "move position 1 to position 4", "move position 3 to position 0",
    "rotate based on position of letter b",
    "rotate based on position of letter d"
]

state_sequence = [
    "ebcda", "edcba", "abcde", "bcdea", "bdeac", "abdec", "ecabd", "decab"
]

state = [*"abcde"]
for instruction, expected_state in zip(instruction_sequence, state_sequence):
    print(f"applying {instruction} to {state} expecting {expected_state}")
    state = apply_instruction(state, instruction)
    print(f"got state: {state}")
    assert state == [*expected_state]

if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True).split("\n")
    print(data)
    # res = part1(data)
    res = part2(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    submit(DAY, 2, res, year=YEAR)
