from util import *
import re
import numpy as np
from math import prod
from scipy.optimize import linear_sum_assignment
DAY = 16


def invalid_entries(ticket, rules):
    return [
        val for val in ticket
        if not any(1 for rule in rules for x, y in rule[1:] if x <= val <= y)
    ]


@timing
def part1(rules, nearby):
    return sum(sum(invalid_entries(ticket, rules)) for ticket in nearby)


@timing
def part2(rules, your_ticket, nearby):
    valid_tickets = np.array([
        *filter(lambda ticket: len(invalid_entries(ticket, rules)) == 0,
                nearby)
    ])

    def match(rule_id, column_id):
        (l1, u1), (l2, u2) = rules[rule_id][1:]
        col = valid_tickets[:, column_id]
        return all((l1 <= x <= u1) or (l2 <= x <= u2) for x in col)

    allowed_matches = np.array([[1 - match(i, j) for j in range(len(rules))]
                                for i in range(len(rules))],
                               dtype=np.uint)
    row_indices, col_indices = linear_sum_assignment(
        allowed_matches)  # maximize keyword does not work?
    return prod(
        int(your_ticket[col_indices[i]]) for i, rule in enumerate(rules)
        if "departure" in rule[0])


def parse_rule(line):
    m = re.match(r"^(.*)\:\ ([0-9]+)\-([0-9]+)\ or\ ([0-9]+)\-([0-9]+)$", line)
    g = m.groups()
    return g[0], [int(g[1]), int(g[2])], [int(g[3]), int(g[4])]


def parse_csv(line):
    return [*map(int, line.split(","))]


if __name__ == "__main__":
    data = get_data(DAY, raw=True)
    rules, you, other = data.split("\n\n")
    parsed_rules = [*map(parse_rule, rules.split("\n"))]
    nearby = [parse_csv(row) for row in other.split("\n")[1:]]
    you = parse_csv(you.split("\n")[1])
    res = part1(parsed_rules, nearby)
    print(res)
    #submit(DAY, 1, res)
    res = part2(parsed_rules, you, nearby)
    print(res)
    submit(DAY, 2, res)
