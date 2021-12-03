import re
from dataclasses import dataclass
from itertools import combinations
from math import inf
from typing import Tuple, Dict
from heapq import heappush, heappop

from util import *

DAY = 11
YEAR = 2016


@dataclass(frozen=True, eq=True, order=True)
class FacilityDevice:
    radioisotope: str
    is_generator: bool


word_pattern = r"(\w+)"


def parse_line(line):
    return tuple(
        FacilityDevice(radioisotope=m.group(1), is_generator=is_generator)
        for is_generator, detection_string in ((True, r"\sgenerator"),
                                               (False,
                                                r"\-compatible\smicrochip"))
        for m in re.finditer(f"{word_pattern}{detection_string}", line))


def get_initial_state(data):
    floors = tuple(parse_line(line) for line in data)
    elevator = 0
    return elevator, floors


def floor_is_valid(floor: Tuple[FacilityDevice, ...]):
    for device in floor:
        if not device.is_generator:
            # any chip
            if not any(other_device.is_generator
                       and other_device.radioisotope == device.radioisotope
                       for other_device in floor):
                # not protected
                if any(other_device.is_generator for other_device in floor):
                    # and radiated
                    return False
    return True


def gen_valid_neighbor_states(state):
    elevator, floors = state
    for new_floor in range(max(0, elevator - 1), min(4, elevator + 2)):
        if new_floor == elevator:
            continue
        for number_picked_up in range(1, 3):
            for items_picked_up in combinations(floors[elevator],
                                                number_picked_up):
                new_current_floor = tuple(
                    sorted((device for device in floors[elevator]
                            if device not in items_picked_up)))
                new_destination_floor = tuple(
                    sorted((*floors[new_floor], *items_picked_up)))
                if floor_is_valid(new_current_floor) and floor_is_valid(
                        new_destination_floor):
                    new_floors = [*floors]
                    new_floors[elevator] = new_current_floor
                    new_floors[new_floor] = new_destination_floor
                    yield new_floor, tuple(new_floors)


def heuristic(state) -> float:
    elevator, floors = state
    cost = 0
    to_carry = 0
    for floor in floors[:-1]:
        to_carry += len(floor)
        cost += max(1, to_carry - 1) if to_carry else 0
    return cost


def is_final_state(state):
    elevator, floors = state
    return all(len(x) == 0 for x in floors[:-1])


def part1(data):
    elevator, floors = get_initial_state(data)
    return dfs(gen_valid_neighbor_states, (elevator, floors),
               is_final_state=is_final_state).shortest_distance


def part2(data):
    elevator, floors = get_initial_state(data)
    extended_first_floor = tuple(
        (*floors[0],
         *(FacilityDevice(radioisotope=isotope, is_generator=is_generator)
           for isotope in ("elerium", "dilithium")
           for is_generator in (True, False))))
    floors = (extended_first_floor, *floors[1:])
    # return a_star_search(gen_valid_neighbor_states, (elevator, floors),
    #                      is_final_state=is_final_state, heuristic=heuristic)
    return dfs(gen_valid_neighbor_states, (elevator, floors),
               is_final_state=is_final_state).shortest_distance


test_data = """The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant."""

if __name__ == "__main__":
    data = get_data(DAY, raw=True).split("\n")
    # res = part1(test_data.split("\n"))
    # res = part1(data)
    res = part2(data)
    print(res)
    # submit(DAY, 1, res)
    submit(DAY, 2, res)
