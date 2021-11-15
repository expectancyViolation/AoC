from util import get_data, submit
import numpy as np

DAY = 5


def seat_id(code):
    bin_code = "".join(str(1 * (x in {'B', 'R'})) for x in code)
    return int(bin_code, 2)


def part1(data):
    return max(map(seat_id, data))


def part2(nums):
    ids = sorted(map(seat_id, data))
    id_diffs = np.diff(ids)
    jump_index = [*id_diffs].index(2)
    return ids[jump_index] + 1


if __name__ == "__main__":
    data = get_data(DAY)
    print(data)
    #res = part1(data)
    res = part2(data)
    print(res)
    #submit(DAY, 1, res)
    #submit(DAY, 2, res)
