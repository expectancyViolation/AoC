from collections import defaultdict
from functools import cache
from itertools import zip_longest, count
from operator import mul, add, mod
import sympy as sp

from util import *

DAY = 24
YEAR = 2021


def split_on_inp(instructions):
    sublists = []
    curr = []
    for instr in instructions:
        if instr[0] == "inp":
            sublists += [curr]
            curr = []
        curr += [instr]
    return sublists[1:] + [curr]


ORDER = "xyzw"

# hacky global state :/
LAST_CONDITION = None


def eql(x, y):
    global LAST_CONDITION
    LAST_CONDITION = sp.Eq(x, y)
    return sp.Piecewise((1, sp.Eq(x, y)), (0, True)).simplify()


INST = {
    "mul": mul,
    "add": add,
    "mod": lambda x, y: x % y,
    "div": lambda x, y: x // y,
    "eql": eql

    # "eql": lambda x, y: 0
}


def run(instructions, initial_state, input_stack, condition_override=None):
    state = {letter: val for letter, val in zip(ORDER, initial_state)}

    all_nums = []

    def get_val(arg):
        if isinstance(arg, int):
            all_nums.append(arg)
            return arg
        return state[arg]

    for inst, *args in instructions:
        if inst == "inp":
            pos, = args
            state[pos] = input_stack.pop()
        else:
            arg1, arg2 = args
            op = INST[inst]
            if inst == "eql" and condition_override is not None:
                state[arg1] = int(condition_override)
            else:
                state[arg1] = op(get_val(arg1), get_val(arg2))
    return tuple(state[letter] for letter in ORDER), all_nums


def part1(data):
    x, y, z, w = sp.symbols("x y z w", integer=True)

    all_all_nums = []
    for block in data:
        state = (x, y, z, 0)
        for override in None, True, False:
            res, all_nums = run(block, state, [w], condition_override=override)
        all_all_nums.append(all_nums)
    relevant_positions = []
    for i in range(9):
        diffs = set(all_nums[i] for all_nums in all_all_nums)
        if len(diffs) > 1:
            relevant_positions += [i]
    all_all_nums = [[x for i, x in enumerate(all_nums) if i in relevant_positions] for all_nums in all_all_nums]

    def apply_forward(all_nums, z, w):
        a, b, c = all_nums
        if z % 26 + b == w:
            if a == 1:
                print("woot")
            return z // a
        return z // a * 26 + w + c

    # def apply_reverse(all_nums, x, w):
    #     a, b, c = all_nums
    #     w_hypo = x % 26 - c
    #     # print("hypo",x-w-c)
    #     if a == 1:
    #         candies = [(x - w - c) // 26] + [x]
    #     else:
    #         candies = [((x - w - c) // 26) * 26 + v for v in range(26) if v + b != w] + [x * a + w - b]
    #     return [z for z in candies if apply_forward(all_nums, z, w) == x]

    @cache
    def best(z=0, i=0, worst=False):
        if i >= len(all_all_nums):
            if z == 0:
                return []
            return None
        all_nums = all_all_nums[i]
        order = range(1, 10) if worst else range(9, 0, -1)
        for w in order:
            new_z = apply_forward(all_nums, z, w)
            others = best(new_z, i + 1, worst)
            if others is not None:
                return [w] + others

    res = best(worst=False)
    print("".join(str(x) for x in res))

    res = best(worst=True)
    print("".join(str(x) for x in res))


def part2(data):
    return None


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    split = split_on_inp(data)
    for row in zip_longest(*split, fillvalue="    "):
        print("\t".join(" ".join(str(y) for y in x).rjust(10, " ") for x in row))
    res = part1(split)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    # res = part2(data)
    # print(res)
    # submit(DAY, 2, res,year=YEAR)
