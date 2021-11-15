from util import get_data, submit

DAY = 6


def count(group, op):
    return len(op(*map(set, group)))


def group_sum(groups, op):
    return sum([count(group, op) for group in groups])


if __name__ == "__main__":
    data = get_data(DAY, raw=True)
    groups = [g.split("\n") for g in data.split("\n\n")]
    #print(groups)
    part1 = group_sum(groups, set.union)
    part2 = group_sum(groups, set.intersection)
    print(f"part1:{part1}\npart2:{part2}")
    #submit(DAY, 1, part1)
    #submit(DAY, 2, part2)
