from util import *

DAY = 24
YEAR = 2015


def solve(data,n_packs):
    data = data[::-1]
    target_val = sum(data) // n_packs
    print("target", target_val)
    states = {(0, 0, 1)}
    remaining = sum(data)
    best_cnt = (inf, inf)
    for val in data + [0]:
        # print(val)
        remaining -= val
        new_states = set()
        for weight, cnt, entanglement in states:
            if (cnt, entanglement) > best_cnt:
                continue
            if weight == target_val:
                # print(cnt,entanglement)
                if (cnt, entanglement) < best_cnt:
                    best_cnt = (cnt, entanglement)
                    print("new best", best_cnt)
            if remaining >= target_val - weight:
                new_states.add((weight, cnt, entanglement))
            new_states.add((weight + val, cnt + 1, entanglement * val))
        states = new_states
    return best_cnt[-1]


def part1(data):
    return solve(data,3)


def part2(data):
    return solve(data,4)


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    # data = [*range(1, 6)] + [*range(7, 12)]
    print(data)
    res = part1(data)
    print(res)
    # 31547027103 too high
    # 32395160463
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    submit(DAY, 2, res,year=YEAR)
