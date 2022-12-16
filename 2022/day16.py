import re
from collections import defaultdict
from itertools import product

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

@timing
def get_state_scores(valves, start_time=0):
    valve_indices = defaultdict(lambda: 0,
                                {valve: 1 << i for i, valve in enumerate(
                                    v for v, (flow, _) in valves.items() if
                                    flow > 0)})
    states = {(0, "AA"): 0}
    for i in range(start_time + 1, 31):
        remaining_time_after_move = (30 - i)
        new_states = defaultdict(lambda: 0)
        for (opened, pos), score in states.items():
            valve_score, neighbors = valves[pos]
            poss_steps = []
            if not (opened & valve_indices[pos]):
                open_state = (opened | valve_indices[pos], pos)
                score_diff = remaining_time_after_move * valve_score
                poss_steps += [(open_state, score_diff)]
            poss_steps += [((opened, nb), 0) for nb in neighbors]
            for new_state, score_diff in poss_steps:
                new_states[new_state] = max(new_states[new_state],
                                            score + score_diff)
        states = new_states
    return states


def part1(data):
    valves = parse_valve_plan(data)
    return max(get_state_scores(valves).values())


def part2(data):
    valves = parse_valve_plan(data)
    state_scores = get_state_scores(valves, 4)
    reduced_states = defaultdict(lambda: 0)
    for (opened, _pos), score in state_scores.items():
        reduced_states[opened] = max(reduced_states[opened], score)

    return max(reduced_states[a] + reduced_states[b]
               for a, b in product(reduced_states, repeat=2)
               if not (a & b))

if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True).split("\n")
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)