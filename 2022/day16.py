import re
from collections import defaultdict

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


def part1(data):
    valves = parse_valve_plan(data)
    valve_indices = defaultdict(lambda: 0,
                                {valve: 1 << i for i, valve in enumerate(
                                    v for v, (flow, _) in valves.items() if
                                    flow > 0)})
    states = {(0, "AA"): 0}
    for i in range(1, 31):
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
    return max(states.values())


def part2(data):
    valves = parse_valve_plan(data)
    valve_indices = defaultdict(lambda: 0,
                                {valve: 1 << i for i, valve in enumerate(
                                    v for v, (flow, _) in valves.items() if
                                    flow > 0)})
    states = {(0, "AA", "AA"): 0}
    print(len(valve_indices))
    print(len(valves))
    print(2 ** len(valve_indices) * (len(valves) ** 2))
    all_open = sum(valve_indices.values())
    for i in range(5, 31):
        remaining_time_after_move = (30 - i)
        for k in [0, 1]:
            new_states = defaultdict(lambda: 0)
            for (opened, *positions), score in states.items():
                pos = positions[k]
                valve_score, neighbors = valves[pos]
                if valve_indices[pos] > 0 and not (opened & valve_indices[pos]):
                    open_state = (opened | valve_indices[pos], *positions)
                    score_diff = remaining_time_after_move * valve_score
                    new_states[open_state] = max(new_states[open_state],
                                                 score + score_diff)
                for nb in neighbors:
                    new_positions = [*positions]
                    new_positions[k] = nb
                    new_states[(opened, *new_positions)] = max(
                        new_states[(opened, *new_positions)],
                        score)
            states = new_states
            print(i, len(states))
            print(max(states.values()))
            if all_open in states:
                break
    return max(states.values())


if __name__ == "__main__":
    # data = get_data(DAY, year=YEAR, raw=True,
    #                 filename="input/2022/16_test.txt").split("\n")
    data = get_data(DAY, year=YEAR, raw=True).split("\n")
    # print(data)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # 2076 too low
    # 2106 wrong
    # submit(DAY, 2, res, year=YEAR)
