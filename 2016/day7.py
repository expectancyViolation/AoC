import re

from util import *

DAY = 7


def gen_hypernets(ip):
    for match in re.finditer(r"\[(.*?)\]", ip):
        yield match.group(1)


def contains_abba(word):
    return any(word[i:i + 2] == word[i + 3:i + 1:-1] and word[i] != word[i + 1]
               for i in range(len(word) - 3))


def gen_abas(word):
    inside_subnet = False
    for i in range(len(word) - 2):
        if word[i] in "[]":
            inside_subnet = not inside_subnet
        if (word[i] == word[i + 2] and word[i + 1] != word[i]):
            if not inside_subnet:
                yield word[i:i + 3]


# filtering for "[]" unnecessary since abba containing any bracket is not properly "bracketed"
def is_valid_1(ip):
    overall_abba = contains_abba(ip)
    no_hypernet_abba = not any(contains_abba(net) for net in gen_hypernets(ip))
    return overall_abba and no_hypernet_abba


def is_valid_2(ip):
    for a, b, _ in gen_abas(ip):
        bab = f"{b}{a}{b}"
        if any(bab in net for net in gen_hypernets(ip)):
            return True
    return False


def part1(data):
    return sum(1 for ip in data if is_valid_1(ip))


def part2(data):
    return sum(1 for ip in data if is_valid_2(ip))


if __name__ == "__main__":
    data = get_data(DAY)
    # print(data)
    # res = part1(data)
    # submit(DAY, 1, res)
    # res = part2(data)
    # lower than 1616
    # submit(DAY, 2, res)
