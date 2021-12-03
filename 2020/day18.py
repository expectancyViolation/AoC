from util import *
import re

DAY = 18

#%%


class WeirdInt:
    def __init__(self, val):
        self.val = val

    def __sub__(self, other):
        return WeirdInt(self.val * other.val)

    def __add__(self, other):
        return WeirdInt(self.val + other.val)

    def __or__(self, other):
        return WeirdInt(self.val * other.val)

    def __repr__(self):
        return f"weird({self.val})"


#%%
def eval_weird(line, mulsub="-"):
    line = line.strip()
    weird_subbed = re.sub(r"([0-9]+)", r"WeirdInt(\1)", line)
    very_weird = weird_subbed.replace("*", mulsub)
    return eval(very_weird).val


@timing
def part1(data):
    return sum(map(eval_weird, data))


@timing
def part2(data):
    return sum(eval_weird(line, "|") for line in data)


if __name__ == "__main__":
    data = get_data(DAY, raw=True).split("\n")
    print(data)
    res = part1(data)
    print(res)
    #submit(DAY, 1, res)
    res = part2(data)
    print(res)
    #submit(DAY, 2, res)
