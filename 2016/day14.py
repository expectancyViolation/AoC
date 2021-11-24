from collections import defaultdict
from functools import lru_cache
from itertools import groupby, count

from util import *

DAY = 14
YEAR = 2016


def get_hash(salt, streches=1):
    @lru_cache(maxsize=10**5)
    def hash_signature(i):
        val = f"{salt}{i}"
        for _ in range(streches):
            val = md5_hash(val)
        first_triplet = None
        fiver_runs = set()
        for val, it in groupby(val):
            l = sum(1 for x in it)
            if l >= 3 and first_triplet is None:
                first_triplet = val
            if l >= 5:
                fiver_runs.add(val)
        return first_triplet, fiver_runs

    return hash_signature


# going backwards from 5+ runs for previous 3+ run
# issue: indices might be hit in different order
# so: weird break condition needed, which continues for 1000 indices after having found 64
# this gives no noticable performance increase since the complexity is dominated by the (stretched) hash
def solve(hasher):
    pads = []
    last_triplet_indices = defaultdict(lambda: [])
    pre_break_index = None
    for index in count():
        if pre_break_index is not None and index - pre_break_index > 1000:
            break
        first_triplet, fiver_runs = hasher(index)
        for val in fiver_runs:
            for last_index in last_triplet_indices[val][::-1]:
                if index - last_index > 1000:
                    break
                print("pad", len(pads), last_index)
                pads.append(last_index)
        if first_triplet is not None:
            last_triplet_indices[first_triplet].append(index)
        if len(pads) >= 64 and pre_break_index is None:
            pre_break_index = index
    return sorted(pads)[63]


def part1(data):
    hasher = get_hash(data[0])
    return solve(hasher)

@timing
def part2(data):
    hasher = get_hash(data[0], streches=2017)
    return solve(hasher)


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    print(data)
    # res = part1(data)

    # res = part2(["abc"])
    res = part2(data)

    print(res)
    # submit(DAY, 1, res, year=YEAR)
    submit(DAY, 2, res, year=YEAR)
