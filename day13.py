from util import *
from sympy.ntheory.modular import crt

DAY = 13


def part1(time, departures):
    departure_scores = sorted(((-time) % dep, dep) for _, dep in departures)
    best_t, best_departure = departure_scores[0]
    return best_t * best_departure


def part2(time, departures):
    ids, modules = zip(*departures)
    remainders = [-x for x in ids]
    result, _ = crt(modules, remainders)
    return int(result)


if __name__ == "__main__":
    time, departure_string = get_data(DAY)
    departures = []
    for i, x in enumerate(departure_string.split(",")):
        if x != "x":
            try:
                departures += [(i, int(x))]
            except:
                print(x)
    print(time)
    print(departures)
    res = part1(time, departures)
    print(res)
    #submit(DAY, 1, res)
    res = part2(time, departures)
    print(res)
    #submit(DAY, 2, res)
