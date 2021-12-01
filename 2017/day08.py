import re

from util import *

DAY = 8
YEAR = 2017

# templated "exec"-shenanigans and globals :D

test_data = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""

if __name__ == "__main__":

    data = get_data(DAY, year=YEAR, raw=True)
    # data = test_data
    code = [
        line.split("if")
        for line in data.replace(
            "dec", "-=").replace("inc", "+=").split("\n")
    ]
    registers = [x for line in code for part in line for x in re.findall("([a-z]+)", part)]
    init_code = [f"{register}=0" for register in registers]
    code = [f"if {condition}:\n\t{instruction}\n" for (instruction, condition) in code]
    total_max = res = 0
    exec("\n".join(init_code))
    for step in code:
        exec(step)
        res = max(globals()[reg] for reg in registers)
        total_max = max(total_max, res)
    print(res)
    print(total_max)
    # res = part2(data)
    # submit(DAY, 1, res, year=YEAR)
    # submit(DAY, 2, total_max, year=YEAR)
