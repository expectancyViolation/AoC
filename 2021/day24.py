from operator import lt, gt

from util import *

DAY = 24
YEAR = 2021


def get_transform_values(instructions):
    sublists = []
    curr = []
    for instr in instructions:
        if instr[0] == "inp":
            sublists += [curr]
            curr = []
        curr += [instr]
    parts = sublists[1:] + [curr]
    return [[int(x) for x in (part[4][-1], part[5][-1], part[15][-1])]
            for part in parts]


@timing
def solve(values):
    def apply_forward(all_nums, z, w):
        a, b, c = all_nums
        if z % 26 + b == w:
            return z // a
        return z // a * 26 + w + c

    def apply_reverse(all_nums, x, w):
        a, b, c = all_nums
        if a == 1:
            candidates = [(x - w - c) // 26] + [x]
        else:
            candidates = [((x - w - c) // 26) * 26 + v
                          for v in range(26) if v + b != w] + [x * a + w - b]
        return [z for z in candidates if apply_forward(all_nums, z, w) == x]

    backstates = {0}
    successors = [{}, {}]
    for i, nums in [*enumerate(values)][::-1]:
        new_backstates = set()
        for state in backstates:
            for w in range(9, 0, -1):
                reverse_states = apply_reverse(nums, state, w)
                for s in reverse_states:
                    for succs, op in zip(successors, (gt, lt)):
                        if (i, s) not in succs or op(w, succs[(i, s)][1]):
                            succs[(i, s)] = (state, w)
                new_backstates |= {*reverse_states}
        backstates = new_backstates
    for succs in successors:
        solution = []
        curr = 0
        for i in range(len(values)):
            succ, w = succs[(i, curr)]
            solution += [w]
            curr = succ
        print("".join(str(x) for x in solution))


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    values = get_transform_values(data)
    solve(values)
