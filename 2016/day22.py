import re
from collections import namedtuple
from itertools import combinations, product

from util import *

DAY = 22
YEAR = 2016

Node = namedtuple("Node", ("x", "y", "size", "used", "avail", "use_per"))


def to_val(s):
    try:
        return int(s)
    except ValueError:
        return s


def parse_line(line):
    m = re.match(
        r"^/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)\%",
        line)
    args = [*map(int, m.groups())]
    return Node(*args)


def part1(nodes):
    nonempty = [node for node in nodes if node.used > 0]
    res = 0
    for node1, node2 in product(nonempty, nodes):
        if node1 == node2:
            continue
        res += node1.used < node2.avail
    print(max(n.used for n in nonempty))
    print(min(n.size for n in nonempty))
    return res


def part2(data):
    return None


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True).split("\n")
    print(data)
    nodes = [*map(parse_line, data[2:])]
    for node in nodes:
        print(node)
    res = part1(nodes)
    # res = part2(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    # submit(DAY, 2, res,year=YEAR)
