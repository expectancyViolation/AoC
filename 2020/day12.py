from util import *
from enum import IntEnum, Enum
from dataclasses import dataclass

DAY = 12


class Orientation(IntEnum):
    East = 0
    South = 1
    West = 2
    North = 3

    def __add__(self, other):
        ori_num = (int(self) + int(other)) % 4
        return Orientation(ori_num)

    def to_vector(self):
        if self == Orientation.East:
            return 1, 0
        elif self == Orientation.South:
            return 0, -1
        elif self == Orientation.West:
            return -1, 0
        elif self == Orientation.North:
            return 0, 1


class Action(Enum):
    N = "north"
    S = "south"
    E = "east"
    W = "west"
    L = "left"
    R = "right"
    F = "forward"


@dataclass
class ActionPair:
    action: Action
    value: int

    @staticmethod
    def parse(inp: str):
        action_str, *val_str = inp.strip()
        action = Action[action_str]
        val = int("".join(val_str))
        return ActionPair(action, val)


@dataclass
class FerryState:
    x: int
    y: int
    orientation: Orientation

    def update(self, action_pair: ActionPair):
        action = action_pair.action
        value = action_pair.value
        x, y = self.x, self.y
        ori = self.orientation
        if action == Action.N:
            y += value
        elif action == Action.E:
            x += value
        elif action == Action.S:
            y -= value
        elif action == Action.W:
            x -= value
        elif action == Action.L:
            turns = -value // 90
            ori = ori + turns
        elif action == Action.R:
            turns = value // 90
            ori = ori + turns
        elif action == Action.F:
            dx, dy = ori.to_vector()
            x, y = x + value * dx, y + value * dy
        return FerryState(x, y, ori)


@dataclass
class WaypointFerryState:
    x: int
    y: int
    wx: int
    wy: int

    def update(self, action_pair: ActionPair):
        action = action_pair.action
        value = action_pair.value
        x, y = self.x, self.y
        wx, wy = self.wx, self.wy
        if action == Action.N:
            wy += value
        elif action == Action.E:
            wx += value
        elif action == Action.S:
            wy -= value
        elif action == Action.W:
            wx -= value
        elif action == Action.L:
            turns = (value // 90) % 4
            for _ in range(turns):
                wx, wy = -wy, wx
        elif action == Action.R:
            turns = (value // 90) % 4
            for _ in range(turns):
                wx, wy = wy, -wx
        elif action == Action.F:
            x, y = x + value * wx, y + value * wy
        return WaypointFerryState(x, y, wx, wy)


@timing
def part1(actions):
    ferry = FerryState(0, 0, Orientation.East)
    for action in actions:
        ferry = ferry.update(action)
    return abs(ferry.x) + abs(ferry.y)


@timing
def part2(data):
    ferry = WaypointFerryState(0, 0, 10, 1)
    for action in actions:
        ferry = ferry.update(action)
    return abs(ferry.x) + abs(ferry.y)


if __name__ == "__main__":
    data = get_data(DAY)
    actions = [ActionPair.parse(line) for line in data]
    res = part1(actions)
    print(res)
    #submit(DAY, 1, res)
    res = part2(data)
    print(res)
    submit(DAY, 2, res)
