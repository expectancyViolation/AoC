from collections import namedtuple
from dataclasses import replace
from typing import NamedTuple

from util import *

DAY = 22
YEAR = 2015


@dataclass(frozen=True)
class State:
    my_hp: int
    boss_hp: int
    mana: int
    shield: int
    poison: int
    recharge: int

    def __lt__(self, other: "State"):
        return self.mana < other.mana


def simulate(data, hard_mode=False):
    boss_hp = data[0][-1]
    boss_dmg = data[1][-1]

    def calculate_dmg(state, boss_turn):
        new_hp = state.my_hp
        new_boss_hp = state.boss_hp
        new_mana = state.mana
        if state.poison:
            new_boss_hp = max(0, new_boss_hp - 3)
        if hard_mode and not boss_turn:
            new_hp = max(0, new_hp - 1)
        # boss only attacks if poison did not kill them
        if boss_turn and new_boss_hp > 0:
            dmg_taken = max(0, boss_dmg - (state.shield > 0) * 7)
            new_hp = max(0, new_hp - dmg_taken)
        if state.recharge:
            new_mana += 101
        new_shield = max(0, state.shield - 1)
        new_poison = max(0, state.poison - 1)
        new_recharge = max(0, state.recharge - 1)
        return State(my_hp=new_hp, boss_hp=new_boss_hp, mana=new_mana,
                     shield=new_shield, poison=new_poison,
                     recharge=new_recharge)

    def gen_my_turn(state):
        state = calculate_dmg(state, False)
        if state.mana >= 53:
            new_boss_hp = max(0, state.boss_hp - 4)
            yield replace(state, boss_hp=new_boss_hp, mana=state.mana - 53), 53
        if state.mana >= 73:
            new_boss_hp = max(0, state.boss_hp - 2)
            new_hp = state.my_hp + 2
            yield replace(state, mana=state.mana - 73, boss_hp=new_boss_hp,
                          my_hp=new_hp), 73
        if state.mana >= 113 and state.shield == 0:
            yield replace(state, shield=6, mana=state.mana - 113), 113
        if state.mana >= 173 and state.poison == 0:
            yield replace(state, poison=6, mana=state.mana - 173), 173
        if state.mana >= 229 and state.recharge == 0:
            yield replace(state, mana=state.mana - 229,
                          recharge=5), 229

    def gen_neighbors(state):
        if state.my_hp == 0:
            return
        for new_state, cost in gen_my_turn(state):
            if new_state.boss_hp <= 0:
                yield new_state, cost
            else:
                newer_state = calculate_dmg(new_state, True)
                yield newer_state, cost

    initial_state = State(50, boss_hp, 500, 0, 0, 0)

    def is_final(state: State):
        return state.boss_hp <= 0 and state.my_hp > 0

    # no heuristic => dijkstra
    def heuristic(state):
        return 0

    cost, came_from, current = a_star_search(gen_neighbors, initial_state,
                                             is_final, heuristic)
    return cost


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    print(data)
    part1 = simulate(data, hard_mode=False)
    print(part1)

    part2 = simulate(data, hard_mode=True)
    print(part2)
    # 1242 too high
    # 900 too low
    # submit(DAY, 1, res,year=YEAR)
    # res = part2(data)
    # print(res)
    # submit(DAY, 2, res,year=YEAR)
