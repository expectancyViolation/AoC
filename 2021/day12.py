from collections import defaultdict

from util import *

DAY = 12
YEAR = 2021


@timing
def solve(data):
    edges = defaultdict(lambda: set())
    for x, y in data:
        for a, b in (x, y), (y, x):
            if b != "start":
                edges[a].add(b)

    index_lookup = {}
    val = 1
    for node in edges:
        if node.islower():
            index_lookup[node] = val
            val *= 2
        else:
            index_lookup[node] = 0
    states = {(index_lookup["start"], False, "start"): 1}

    part1 = 0
    part2 = 0
    while states:
        new_states = defaultdict(lambda: 0)
        for (visited, double_visit, current), cnt in states.items():
            if current == "end":
                part2 += cnt
                if not double_visit:
                    part1 += cnt
            else:
                for neighbor in edges[current]:
                    nb_index = index_lookup[neighbor]
                    already_visited = visited & nb_index
                    if already_visited and double_visit:
                        continue
                    new_states[(visited | nb_index,
                                double_visit | already_visited,
                                neighbor)] += cnt
        states = new_states
    return part1, part2



if __name__ == "__main__":
    data = [line.split("-") for line in get_data(DAY, year=YEAR)]
    print(data)
    part1, part2 = solve(data)
    print(part1)
    # submit(DAY, 1, part1,year=YEAR)
    print(part2)
    # submit(DAY, 2, part2,year=YEAR)
