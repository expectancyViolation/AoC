from collections import defaultdict

from util import *

DAY = 7
YEAR = 2022


def get_dirsizes(data):
    current_path = []
    sizes = defaultdict(lambda: 0)
    dirs = [tuple()]
    for line in data:
        match line[0]:
            case "$":
                if line[1] == "cd":
                    match line[2]:
                        case "/":
                            current_path = []
                        case "..":
                            current_path.pop()
                        case a:
                            current_path.append(a)
            case "dir":
                dirname = line[1]
                dirs.append(tuple([*current_path, dirname]))
            case _:
                size, filename = line
                size = int(size)
                sizes[tuple([*current_path, filename])] = size
    dir_sizes = defaultdict(lambda: 0)
    for pathname, size in sizes.items():
        for prefix_size in range(len(pathname) + 1):
            prefix = pathname[:prefix_size]
            if prefix in dirs:
                dir_sizes[prefix] += size
    return dir_sizes


def part1(data):
    res = 0
    dir_sizes = get_dirsizes(data)
    for dir, size in dir_sizes.items():
        if size <= 100000:
            res += size
    return res


def part2(data):
    dirsizes = get_dirsizes(data)
    free_space_needed = 30000000 - (70000000 - dirsizes[tuple()])
    return min(size for size in dirsizes.values() if size >= free_space_needed)


if __name__ == "__main__":
    # data = get_data(DAY, year=YEAR, filename="input/2022/07_test.txt")

    data = get_data(DAY, year=YEAR)
    print(data)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
