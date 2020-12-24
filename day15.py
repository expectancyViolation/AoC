from util import *
from itertools import count

DAY = 15


# slooooooow
def gen_part1(data):
    last_spoken = {}
    last_num = None
    for i, x in enumerate(data[:-1]):
        yield x
        last_spoken[x] = i
    last_num = data[-1]
    for i in count(len(data)):
        if i % 10000 == 0:
            print(i, max(last_spoken))
        yield last_num  #, last_spoken
        if last_num in last_spoken:
            next_num = i - 1 - last_spoken[last_num]
        else:
            next_num = 0
        last_spoken[last_num] = i - 1
        last_num = next_num


@timing
def n_th_slow(data, n):
    g = gen_part1(data)
    for i in range(n):
        curr = next(g)
    return curr


def part1(data):
    return n_th_slow(data, 2020)


def part2(data):
    return n_th_slow(data, 30000000)


if __name__ == "__main__":
    data = get_data(DAY)
    data = [int(x) for x in data[0].split(",")]
    print(data)
    # res = part1(data)
    # print(res)
    #submit(DAY, 1, res)
    res = part2(data)
    print(res)
    #submit(DAY, 2, res)
