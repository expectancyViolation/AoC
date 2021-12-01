from util import *

DAY = 18
YEAR = 2016


def step(state):
    res = [0]
    for i in range(1, len(state) - 1):
        left, center, right = state[i - 1:i + 2]
        curr = ((left and center and not right)
                or ((not left) and center and right)
                or (left and (not center) and (not right))
                or ((not left) and (not center) and right))
        res += [1 if curr else 0]
    return res + [0]


def solve(state, n_rows=40):
    res = 0
    for i in range(n_rows):
        res += (len(state) - 2) - sum(state)  # do not count delimiters
        state = step(state)
    return res


def part1(state):
    return solve(state, 40)


def part2(state):
    return solve(state, 400000)


if __name__ == "__main__":
    # delimiters to avoid special case
    # DANGER! take into account when counting!
    data = [0] + [x == '^' for x in get_data(DAY, year=YEAR)[0]] + [0]
    # res = part1(data)
    res = part2(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    # submit(DAY, 2, res,year=YEAR)
