from util import *

DAY = 13


def is_wall(x, y, my_number):
    val = x * x + 3 * x + 2 * x * y + y + y * y
    val += my_number
    n_bits = 0
    while val:
        n_bits += val % 2
        val //= 2
    return n_bits % 2


def get_get_neighbors(my_number):
    def get_neighbors(pos):
        x, y = pos
        for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
            nx, ny = x + dx, y + dy
            if nx<0 or ny<0:
                continue
            if not is_wall(nx, ny, my_number):
                yield (nx, ny)

    return get_neighbors


def is_end(pos):
    x, y = pos
    return x == 31 and y == 39


def part1(data):
    my_number = data[0]
    return dfs(get_get_neighbors(my_number), (1, 1), is_end)


def part2(data):
    my_number = data[0]
    distances = dfs(get_get_neighbors(my_number), (1, 1),
                    is_end,
                    get_distances=True)
    print(distances)
    return sum(1 for x, d in distances.items() if d <= 50)


if __name__ == "__main__":
    data = get_data(DAY)
    print(data)
    # res = part1(data)
    res = part2(data)
    print(res)
    # submit(DAY, 1, res)
    submit(DAY, 2, res)
