import numpy as np

from util import *

DAY = 8
YEAR = 2022


def part1(data):
    data = np.array([[int(x) for x in row] for row in data.split("\n")])
    visible = np.zeros(data.shape, dtype=int)
    for _ in range(4):
        for i in range(len(visible)):
            curr_val = -1
            j = 0
            row = data[i]
            while j < len(row):
                if row[j] > curr_val:
                    visible[i, j] = 1
                curr_val = max(row[j], curr_val)
                j += 1
        data = np.rot90(data)
        visible = np.rot90(visible)
    return np.sum(visible)


def part2(data):
    data = np.array([[int(x) for x in row] for row in data.split("\n")])
    total_scores = np.ones(data.shape, dtype=int)
    for _ in range(4):
        dir_score = np.zeros(data.shape, dtype=int)
        for i in range(len(data)):
            row = data[i]
            for j in range(len(row)):
                cnt = 1
                k = j + 1
                while k < len(row):
                    if row[k] >= row[j]:
                        break
                    cnt += 1
                    k += 1
                if k == len(row):
                    cnt -= 1
                dir_score[i][j] = cnt

        total_scores *= dir_score
        data = np.rot90(data)
        total_scores = np.rot90(total_scores)
    return np.max(total_scores[1:-1, 1:-1])


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
