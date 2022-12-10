import numpy as np
from PIL import Image
import pytesseract

# Adding custom options

from util import *

DAY = 10
YEAR = 2022


def simulate(data):
    X = 1
    cycle = 0
    res = 0

    crt = [["X"] * 40 for _ in range(6)]

    def step_cycle():
        nonlocal cycle, res
        crt_x, crt_y = cycle // 40, cycle % 40
        is_drawn = abs(crt_y - X) <= 1
        crt[crt_x][crt_y] = "#" if is_drawn else " "
        cycle += 1
        if (cycle - 20) % 40 == 0:
            res += X * cycle

    for instruction in data:
        parts = instruction.split()
        if len(parts) == 1:
            step_cycle()
        else:
            addition = int(parts[1])
            step_cycle()
            step_cycle()
            X += addition
    crt = np.array(crt)
    im = np.array(crt == "#", dtype=np.uint8) * 255
    im = np.kron(im, np.ones((2, 2))).astype(np.uint8)
    im = 255 - np.pad(im, 5)
    crt_res = ocr_array(im)
    return res, crt_res


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    part1, part2 = simulate(data)
    print(part1)
    # submit(DAY, 1, res, year=YEAR)
    print(part2)
    # submit(DAY, 2, res,year=YEAR)
