from collections import defaultdict

import networkx as nx

from util import *

DAY = 12
YEAR = 2021


@timing
def solve(data):
    edges = [set() for _ in range(len(data) + 1)]
    node_lookup = {}
    num = 0
    for x, y in data:
        for v in x, y:
            if v not in node_lookup:
                node_lookup[v] = num
                num += 1
        for a, b in (x, y), (y, x):
            if b != "start":
                edges[node_lookup[a]].add(node_lookup[b])
    start = node_lookup["start"]
    end = node_lookup["end"]
    inverse_node_lookup = {y: x for x, y in node_lookup.items()}

    index_lookup = [0] * (len(edges) + 1)
    val = 1
    for node in inverse_node_lookup:
        if inverse_node_lookup[node].islower():
            index_lookup[node] = val
            val *= 2
        else:
            index_lookup[node] = 0
    visited_code = val
    encode_offset = visited_code * 2
    states = {start * encode_offset + index_lookup[start]: 1}

    def subsolve(initial, final, final_double_ok=True):
        states = {initial * encode_offset + index_lookup[initial]: 1}
        double_state_counts = defaultdict(lambda: 0)
        single_state_counts = defaultdict(lambda: 0)
        while states:
            new_states = defaultdict(lambda: 0)
            for n, cnt in states.items():
                visited = n % encode_offset
                current = n // encode_offset
                double_visit = visited & visited_code
                if current == final:
                    double_state_counts[n] += cnt
                    if not double_visit:
                        single_state_counts[n] += cnt
                    if not final_double_ok:
                        continue
                for neighbor in edges[current]:
                    nb_index = index_lookup[neighbor]
                    already_visited = not not (visited & nb_index)
                    if already_visited and double_visit:
                        continue
                    already_visited_code = already_visited * visited_code
                    new_states[visited | nb_index | already_visited_code +
                               encode_offset * neighbor] += cnt
            states = new_states
            # print("blub", time(), len(states))
        return single_state_counts, double_state_counts

    ssc, dsc = subsolve(start, end, False)
    part1 = sum(ssc.values())
    part2 = sum(dsc.values())
    return part1, part2


if __name__ == "__main__":
    data = [
        line.split("-") for line in get_data(
            DAY, year=YEAR, filename="output/12_bigboi_40_nodes.txt")
    ]

    data = [line.split("-") for line in get_data(DAY, year=YEAR)]
    print(data)
    part1, part2 = solve(data)
    print(part1)
    # submit(DAY, 1, part1,year=YEAR)
    print(part2)
    # submit(DAY, 2, part2,year=YEAR)
