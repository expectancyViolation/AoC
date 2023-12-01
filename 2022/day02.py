from itertools import product

from util import *

DAY = 2
YEAR = 2022


def get_shape_id(letter):
    reference = 'A' if letter < 'D' else 'X'
    return ord(letter) - ord(reference)


def get_score(player_shape_id, outcome_id):
    return player_shape_id + 1 + 3 * outcome_id


def get_game_score_1(opponent_shape_id, player_shape_id):
    outcome_id = (player_shape_id - opponent_shape_id + 1) % 3
    return get_score(player_shape_id, outcome_id)


def get_game_score_2(opponent_shape_id, outcome_id):
    player_shape_id = (opponent_shape_id + outcome_id - 1) % 3
    return get_score(player_shape_id, outcome_id)


def solve(get_round_score, data):
    return sum(get_round_score(*(map(get_shape_id, row))) for row in data)


def part1(data):
    return solve(get_game_score_1, data)


def part2(data):
    return solve(get_game_score_2, data)


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
