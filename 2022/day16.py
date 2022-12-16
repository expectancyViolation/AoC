import re
from collections import defaultdict

import numpy as np
from scipy.sparse.csgraph import floyd_warshall

from util import *

DAY = 16
YEAR = 2022


def parse_valve_plan(data):
    valves = {}
    for row in data:
        valve, value, *neighbors = re.findall(r"([A-Z]{2}|[0-9]+)", row)
        value = int(value)
        valves[valve] = (value, neighbors)
    return valves


# reduce graph to non-zero valves (using floyd-warshall)
# on this "transitive-hull" graph the optimal sequence of moves consists of
#   (non-revisiting) trips  between non-zero valves and
#   (directly) subsequent openings of the valve
# so by increasing the distances by 1 for each trip between valves
#   no "open-valve" moves have to be considered
def get_state_scores(valves, start_time=0):
    valve_list = sorted(valves)
    valve_indices = {valve_name: i for i, valve_name in enumerate(valve_list)}
    distances = np.zeros([len(valve_indices)] * 2, dtype=int)
    flows = [valves[valve_name][0] for valve_name in valve_list]
    for valve, (_flow, nbs) in valves.items():
        for nb in nbs:
            distances[valve_indices[valve], valve_indices[nb]] = 1
    distances = floyd_warshall(distances).astype(int)
    relevant_indices = [0] + [i for i, flow in enumerate(flows) if flow]
    relevant_flows = [flows[i] for i in relevant_indices]
    distances = distances[np.ix_(relevant_indices, relevant_indices)] + 1
    bests = {(start_time, 0, 0): 0}
    frontiers = [set() for _ in range(31)]
    frontiers[start_time].add((0, 0))
    # iterate though values in increasing time order to guarantee optimality
    for time_spent in range(30):
        frontier = frontiers[time_spent]
        while frontier:
            visited, curr_pos = frontier.pop()
            curr_state = (time_spent, visited, curr_pos)
            for new_pos in range(len(relevant_indices)):
                new_time_spent = time_spent + distances[curr_pos, new_pos]
                if new_time_spent <= 30:
                    pos_visit = 1 << new_pos
                    if pos_visit & visited:
                        continue
                    new_state = (new_time_spent, visited | pos_visit, new_pos)
                    score_diff=(30 - new_time_spent) * relevant_flows[new_pos]
                    new_best = bests[curr_state] + score_diff
                    if new_state not in bests:
                        bests[new_state] = 0
                        frontiers[new_time_spent].add(
                            (visited | pos_visit, new_pos))
                    bests[new_state] = max(
                        bests[new_state], new_best
                    )
    state_scores = defaultdict(lambda: 0)
    for (_time_spent, visited, _curr_pos), score in bests.items():
        state_scores[visited] = max(state_scores[visited], score)
    return state_scores


@timing
def part1(data):
    valves = parse_valve_plan(data)
    return max(get_state_scores(valves).values())


# consider disjoint paths (with 26 minute time budget) and add their scores
# to avoid having to check path pairs that do not cover all valves
#   use the maximum of all subset scores are score
#   this maximum can be found by DP (in order of number of set bits)
@timing
def part2(data):
    valves = parse_valve_plan(data)
    n_relevant_valves = 1 + sum(1 for flow, _ in valves.values() if flow)
    state_scores = get_state_scores(valves, 4)
    numbers_by_bitcount = sorted(range(2 ** n_relevant_valves),
                                 key=lambda x: bin(x).count("1"))
    for number in numbers_by_bitcount:
        for addition_bit in range(n_relevant_valves):
            new_number = number | (1 << addition_bit)
            state_scores[new_number] = max(state_scores[new_number],
                                           state_scores[number])
    all_bits_set = (1 << n_relevant_valves) - 1
    return max(state_scores[a] + state_scores[all_bits_set ^ a]
               for a in state_scores)


if __name__ == "__main__":
    # data = get_data(DAY, year=YEAR, raw=True,
    #                 filename="input/2022/16_test.txt").split("\n")
    data = get_data(DAY, year=YEAR, raw=True).split("\n")
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
