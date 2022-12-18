from util import *

DAY = 12
YEAR = 2017


def get_gen_neighbors(data):
    def gen_neighbors(state):
        yield from data[state][2:]

    return gen_neighbors


def part1(data):
    gen_neighbors = get_gen_neighbors(data)
    res = bfs(gen_neighbors=gen_neighbors,
              initial_state=0,
              is_final_state=lambda x: False)
    return len(res.distances)


def part2(data):
    gen_neighbors = get_gen_neighbors(data)
    states = {line[0] for line in data}
    components = connected_components(gen_neighbors, states)
    return len(components)


def transform_part(part):
    if isinstance(part, str):
        try:
            part = int(part.strip(","))
        except:
            pass
    return part


if __name__ == "__main__":
    data = [[*map(transform_part, line)] for line in get_data(DAY, year=YEAR)]
    print(data)
    res = part1(data)
    print(res)
    res = part2(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    # submit(DAY, 2, res, year=YEAR)
