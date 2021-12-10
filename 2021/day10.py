from util import *

DAY = 10
YEAR = 2021

pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}

error_score = {")": 3, "]": 57, "}": 1197, ">": 25137}


def score_errors(line):
    stack = []
    res = 0
    for x in line:
        if x in pairs:
            stack.append(pairs[x])
        else:
            expected = stack.pop()
            if expected != x:
                res += error_score[x]
    return res, stack


def score_remainder(remainder):
    result = 0
    for character in remainder[::-1]:
        result = 5 * result + ["", ")", "]", "}", ">"].index(character)
    return result

@timing
def part1(data):
    return sum(score_errors(line)[0] for line in data)

@timing
def part2(data):
    completions = [
        score[1] for line in data if (score := score_errors(line))[0] == 0
    ]
    completion_sums = sorted(map(score_remainder, completions))
    l = len(completion_sums)
    return completion_sums[l // 2]


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    print(data)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
