from math import prod
from operator import lt, gt, eq

import bitstruct as bs

from util import *

DAY = 16
YEAR = 2021

POS_QUERY = "pos"


# generator that parsea the data "stream" and keeps track of current position
# use it by "send"-ing in format specifiers
# the special specifier POS_QUERY returns the current position in the stream
def gen_stream(data):
    values = None
    pos = 0
    while True:
        fmt_string = yield values
        if fmt_string == POS_QUERY:
            values = pos
        else:
            values = bs.unpack_from(fmt_string, data, pos)
            pos += bs.calcsize(fmt_string)


def parse_packet(stream):
    version, packet_id = stream.send("u3u3")
    version_sum = version
    if packet_id == 4:
        num = 0
        while True:
            cont, nibble = stream.send("u1u4")
            num = 16 * num + nibble
            if not cont:
                break
        res = num
    else:
        len_id, = stream.send("u1")
        args = []
        if len_id == 0:
            subsize, = stream.send("u15")
            end_pos = stream.send(POS_QUERY) + subsize
            while stream.send(POS_QUERY) != end_pos:
                res, ver_sum = parse_packet(stream)
                version_sum += ver_sum
                args.append(res)
        else:
            subpackets, = stream.send("u11")
            for _ in range(subpackets):
                res, ver_sum = parse_packet(stream)
                version_sum += ver_sum
                args.append(res)
        if packet_id < 4:
            op = [sum, prod, min, max][packet_id]
            res = op(args)
        else:
            op = [gt, lt, eq][packet_id - 5]
            res = int(op(*args))

    return res, version_sum


@timing
def main():
    str_data = get_data(DAY, year=YEAR)[0]
    data = bytes.fromhex(str_data)
    stream = gen_stream(data)
    next(stream)
    part2, part1 = parse_packet(stream)
    print(part1)
    # submit(DAY, 1, part1, year=YEAR)
    print(part2)
    # submit(DAY, 2, part2, year=YEAR)


if __name__ == "__main__":
    main()
