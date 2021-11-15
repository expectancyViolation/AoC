from collections import defaultdict, Counter

from util import *

DAY = 21


# inefficient (quadratic) but "good enough" (TM)
def assign_by_elimination(possible_assignments):
    assignments = {}
    to_assign = {*possible_assignments}
    while to_assign:
        item = next(x for x in to_assign if len(possible_assignments[x]) == 1)
        assigned_value = next(y for y in possible_assignments[item])
        assignments[item] = assigned_value
        to_assign.remove(item)
        for possibilities in possible_assignments.values():
            possibilities -= {assigned_value}
    return assignments


def match_allergenes(data):
    all_ingredients = {ing for ings, _ in data for ing in ings}
    allergene_candidates = defaultdict(lambda: all_ingredients.copy())
    for ingredients, allergenes in data:
        for allergene in allergenes:
            allergene_candidates[allergene] &= ingredients
    assignment = assign_by_elimination(allergene_candidates)
    return assignment


@timing
def part1(data):
    assignment = match_allergenes(data)
    dangerous_ingredients = {*assignment.values()}
    ingredient_counts = Counter(ing for ings, _ in data for ing in ings)
    return sum(cnt for ing, cnt in ingredient_counts.items()
               if ing not in dangerous_ingredients)


@timing
def part2(data):
    assignment = match_allergenes(data)
    return ",".join(ing for (_all, ing) in sorted(assignment.items()))


def parse_line(line):
    parts = line.strip().split("(contains")
    ingredients_str = parts[0]
    ingredients = {x.strip() for x in ingredients_str.split()}
    if len(parts) > 1:
        allergene_str = parts[1]
        allergenes = {x.strip() for x in allergene_str.strip(")").split(",")}
    else:
        allergenes = set()
    return ingredients, allergenes


if __name__ == "__main__":
    raw_data = get_data(DAY, raw=True)
    data = [*map(parse_line, raw_data.split("\n"))]
    res = part1(data)
    print(res)
    # submit(DAY, 1, res)

    res = part2(data)
    print(res)
    # submit(DAY, 2, res)
