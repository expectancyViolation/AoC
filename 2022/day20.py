from util import *

DAY = 20
YEAR = 2022


@dataclass
class Node:
    value: int
    next: Optional[None] = None
    prev: Optional[None] = None


def simulate(data, rounds=1):
    n = len(data)
    nodes = [Node(x) for x in data]
    for i in range(n):
        nodes[i].next = nodes[(i + 1) % n]
        nodes[i].prev = nodes[(i - 1) % n]

    for _ in range(rounds):
        for node in nodes:
            if node.value == 0:
                continue
            pred = node.prev
            old_next = node.next
            curr_next = node
            for _ in range(node.value % (n - 1)):
                curr_next = curr_next.next
            pred.next = old_next
            old_next.prev = pred
            curr_next_next = curr_next.next
            node.next = curr_next_next
            curr_next_next.prev = node
            curr_next.next = node
            node.prev = curr_next

    zero_index = data.index(0)
    curr = nodes[zero_index]
    vals = []
    for _ in range(3):
        for _ in range(1000):
            curr = curr.next
        vals += [curr.value]
    print(vals)
    return sum(vals)


def part1(data):
    return simulate(data, 1)


def part2(data):
    data = [x * 811589153 for x in data]
    return simulate(data, 10)


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
