from util import *

DAY = 17
YEAR = 2016

DIRECTIONS = [
    ("U", (-1, 0)),
    ("D", (1, 0)),
    ("L", (0, -1)),
    ("R", (0, 1)),
]


def get_gen_neighbors(passcode):
    def gen_neighbors(state):
        x, y, travelled = state
        if 3 == x == y:
            return
        word = f"{passcode}{travelled}"
        directions_are_open = [x in "bcdef" for x in md5_hash(word)[:4]]
        for is_open, (direction, (dx, dy)) in zip(directions_are_open,
                                                  DIRECTIONS):
            if is_open:
                nx, ny = x + dx, y + dy
                if (0 <= nx < 4) and (0 <= ny < 4):
                    yield nx, ny, travelled + direction

    return gen_neighbors


def is_end(state):
    x, y, travelled = state
    return 3 == x == y


def part1(data):
    gen_neighbors = get_gen_neighbors(data)
    result = dfs(gen_neighbors=gen_neighbors,
                 initial_state=(0, 0, ""),
                 is_final_state=is_end)
    _x, _y, path = result.shortest_node
    return path


def part2(data):
    gen_neighbors = get_gen_neighbors(data)
    result = dfs(gen_neighbors=gen_neighbors,
                 initial_state=(0, 0, ""),
                 is_final_state=is_end,
                 short_circuit=False)
    return max(distance for (x, y, _), distance in result.distances.items()
               if 3 == x == y)


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    print(data)
    # res = part1(data[0])
    # res = part2("kglvqrro")

    res = part2(data[0])
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    submit(DAY, 2, res, year=YEAR)
