from util import *

DAY = 25

MOD = 20201227


def part1(data):
    pk_1, pk_2 = data
    curr = 1
    ls = 0
    while curr != pk_1:
        curr = (7 * curr) % MOD
        ls += 1
    return pow(pk_2, ls, MOD)


if __name__ == "__main__":
    data = get_data(DAY)
    print(data)
    res = part1(data)
    print(res)
    #submit(DAY, 1, res)
