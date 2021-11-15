import re
from collections import Counter
from hashlib import md5

from itertools import count, islice
from util import *

DAY =5
YEAR = 2016




def gen_password(door_id):
    for i in count():
        word=f"{door_id}{i}"
        current_hash = md5_hash(word)
        if current_hash[:5] == "00000":
            yield current_hash[5]


def get_password_2(door_id):
    result = [-1] * 8
    seen = set()
    for i in count():
        current_hash = md5_hash(door_id, i)
        if current_hash[:5] == "00000":
            try:
                position = int(current_hash[5])
                assert position < 8
                assert position not in seen
                seen.add(position)
                result[position] = current_hash[6]
                if len(seen) == 8:
                    return "".join(result)
            except Exception as e:
                print(e)


def part1(data):
    return "".join(islice(gen_password(data[0]), 8))


def part2(data):
    return get_password_2(data[0])


assert md5_hash("abc", 3231929)[:5] == "00000"

if __name__ == "__main__":
    my_input = get_data(DAY,year=YEAR)
    print(my_input)
    # res = part1(my_input)
    # res = part1(my_input)
    res = part2(my_input)
    # res = part2(["abc"])
    print(res)
    # submit(DAY, 1, res)
    submit(DAY, 2, res)
