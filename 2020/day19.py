from lark import Lark
import re

from util import *

DAY = 19


def check(word, grammar):
    try:
        grammar.parse(word)
        return True
    except:
        return False


if __name__ == "__main__":
    raw_rules, word_list = get_data(DAY, raw=True).split("\n\n")
    r_rules = re.sub(r"([0-9]+)", r"r\1", raw_rules)
    grammar1 = Lark(r_rules, start="r0")

    part1 = sum(1 for word in word_list.split("\n") if check(word, grammar1))
    print(part1)
    #submit(DAY, 1, part1)

    r_rules = r_rules.replace("r8: r42", "r8: r42 | r42 r8")
    r_rules = r_rules.replace("r11: r42 r31", "r11: r42 r31 | r42 r11 r31")

    grammar2 = Lark(r_rules, start="r0")
    part2 = sum(1 for word in word_list.split("\n") if check(word, grammar2))
    print(part2)
    #submit(DAY, 1, part1)
