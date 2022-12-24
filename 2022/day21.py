import re

import networkx as nx
from networkx import topological_sort
import sympy as sp

from util import *

DAY = 21
YEAR = 2022


@timing
def solve(data):
    lcl = locals()
    rows = [row.split(": ") for row in data]

    G = nx.DiGraph()

    h = sp.symbols("h")
    humn_value = root_left = root_right = None
    rules = {}
    for rule in rows:
        left, right = rule
        if left == 'humn':
            lcl[left] = h
            humn_value = int(right)
            continue
        if left == 'root':
            root_left, root_right = re.findall("[a-z]+", right)
        try:
            lcl[left] = int(right)
        except Exception as e:
            for right_el in re.findall("[a-z]+", right):
                G.add_edge(right_el, left)
            rules[left] = right
    for node in topological_sort(G):
        if node not in lcl:
            lcl[node] = eval(rules[node])
    part1 = int(lcl["root"].replace(h, humn_value))
    part2 = int(sp.solve(lcl[root_left] - lcl[root_right], h)[0])
    return part1, part2


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True).split("\n")
    part1, part2 = solve(data)
    print(part1)
    # submit(DAY, 1, part1, year=YEAR)
    print(part2)
    # submit(DAY, 2, part2, year=YEAR)
