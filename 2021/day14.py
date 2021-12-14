from collections import Counter, defaultdict

from helpers import mat_pow_mod, mat_dot
from util import *

DAY = 14
YEAR = 2021


def parse_rule(line):
    (left, right), rhs = line.split(" -> ")
    rhs = (left + rhs, rhs + right)
    return left + right, rhs


def get_transition_matrix(rules):
    state_lookup = {state: i for i, state in enumerate(rules)}
    M = [[0] * len(state_lookup) for _ in range(len(state_lookup))]
    for from_state, to_states in rules.items():
        for to_state in to_states:
            M[state_lookup[to_state]][state_lookup[from_state]] = 1
    return M, state_lookup


def solve(M, N, initial_state, inverse_state_lookup, final_letter):
    M_N = mat_pow_mod(M, N, 10 ** 20)
    final_state_counts = mat_dot(M_N, initial_state)
    letter_counts = defaultdict(lambda: 0)
    for i, n in enumerate(final_state_counts):
        letter_counts[inverse_state_lookup[i][0]] += n
    letter_counts[final_letter] += 1
    return max(letter_counts.values()) - min(letter_counts.values())


if __name__ == "__main__":
    raw_data = get_data(DAY, year=YEAR, raw=True)
    initial_state, _, *rules = raw_data.split("\n")
    final_letter = initial_state[-1]
    initial_state_counts = Counter(
        (initial_state[i:i + 2] for i in range(len(initial_state) - 1)))
    rules = {pair: added for pair, added in map(parse_rule, rules)}
    M, states = get_transition_matrix(rules)
    inverse_state_lookup = {i: state for state, i in states.items()}
    initial_state = [initial_state_counts[inverse_state_lookup[i]] for i in
                     range(len(M))]
    part1 = solve(M, 10, initial_state, inverse_state_lookup, final_letter)
    print(part1)
    # submit(DAY, 1, part1,year=YEAR)
    part2 = solve(M, 40, initial_state, inverse_state_lookup, final_letter)
    print(part2)
    # submit(DAY, 2, part2, year=YEAR)
