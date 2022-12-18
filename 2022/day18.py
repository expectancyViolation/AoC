from util import *

DAY = 18
YEAR = 2022


def parse_cube(line):
    return tuple((int(x) for x in line.split(",")))


def get_gen_neighbors(cubes):
    occupied = set(cubes)
    m_max = max(x for state in occupied for x in state)
    m_min = min(x for state in occupied for x in state)

    def gen_neighbors(state):
        cx, cy, cz = state
        for i in range(3):
            for dc in (-1, 1):
                deltas = [0, 0, 0]
                deltas[i] = dc
                dx, dy, dz = deltas
                neighbor = cx + dx, cy + dy, cz + dz
                if not all(m_min - 1 <= x <= m_max + 1 for x in neighbor):
                    continue
                if neighbor not in occupied:
                    yield neighbor

    return gen_neighbors


@timing
def part1(data):
    cubes = [*map(parse_cube, data)]
    occupied = set(cubes)
    gen_nbs = get_gen_neighbors(cubes)
    return sum(1 for point in cubes for nb in gen_nbs(point)
               if nb not in occupied)


@timing
def part2(data):
    cubes = [*map(parse_cube, data)]
    occupied = set(cubes)
    m_min = min(x for state in occupied for x in state)
    initial_state = (m_min - 1, m_min - 1, m_min - 1)
    gen_nbs = get_gen_neighbors(cubes)
    search_result = dfs(gen_nbs, initial_state)
    return sum(1 for point in cubes for nb in gen_nbs(point)
               if nb not in occupied and (nb in search_result.distances))


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    # print(data)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
