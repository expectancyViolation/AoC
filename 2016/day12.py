from util import *

DAY = 12
YEAR = 2016


def execute(data, registers=None):
    if registers is None:
        registers = [0] * 4
    register_names = ['a', 'b', 'c', 'd']

    def get_value(val):
        if isinstance(val, int):
            return val
        return registers[register_names.index(val)]

    position = 0
    while 0 <= position < len(data):
        instruction = data[position]
        if instruction[0] == 'cpy':
            _, src, dest = instruction
            val = get_value(src)
            registers[register_names.index(dest)] = val
            position += 1
        elif instruction[0] == 'inc':
            _, reg = instruction
            registers[register_names.index(reg)] += 1
            position += 1
        elif instruction[0] == 'dec':
            _, reg = instruction
            registers[register_names.index(reg)] -= 1
            position += 1
        elif instruction[0] == 'jnz':
            _, reg, dist = instruction
            if get_value(reg) != 0:
                position += get_value(dist)
            else:
                position += 1

    return registers, position


def part1(data):
    registers, position = execute(data)
    return registers[0]


def part2(data):
    registers, position = execute(data, registers=[0, 0, 1, 0])
    return registers[0]


test_data = """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""

if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    # data = parse_data(test_data)
    print(data)
    # res = part1(data)
    # res = part1(data)
    res = part2(data)
    print(res)
    # submit(DAY, 1, res)
    submit(DAY, 2, res)
