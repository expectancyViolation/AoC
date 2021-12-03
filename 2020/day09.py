from util import *
from collections import defaultdict
import numpy as np

DAY = 9


@timing
def part1(data, p_len=25):
    valid_combs = defaultdict(lambda: 0)
    for i in range(len(data)):
        if i >= p_len and valid_combs[data[i]] <= 0:
            return data[i]
        for d in data[max(0, i - p_len + 1):i]:
            valid_combs[data[i] + d] += 1
        if i > p_len:
            for j in range(i - p_len + 1, i):
                valid_combs[data[i - p_len] + data[j]] -= 1


@timing
def part2(data, missing_val):
    cum_sum = np.cumsum(data)
    cum_sum_dict = {cum_sum: j for (j, cum_sum) in enumerate(cum_sum)}
    for i, cs in enumerate(cum_sum):
        total = cs + missing_val
        if total in cum_sum_dict:
            end = cum_sum_dict[total]
            if end > i + 1:
                cont_array = data[i + 1:end + 1]
                return min(cont_array) + max(cont_array)


if __name__ == "__main__":
    data = get_data(DAY)
    #print(data)
    res1 = part1(data, p_len=25)
    print(res1)
    #submit(DAY, 1, res1)

    res = part2(data, res1)
    print(res)
    #submit(DAY, 2, res)
