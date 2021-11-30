from collections import defaultdict
import trio
from operator import add, mul, mod

from util import *

DAY = 18
YEAR = 2017

OPS = {
    "add": add,
    "set": lambda x, y: y,
    "mul": mul,
    "mod": mod
}


async def run_program(data, snd, rcv, p_val=None):
    position = 0
    registers = defaultdict(lambda: 0)
    if p_val is not None:
        registers["p"] = p_val

    def get_value(arg):
        if isinstance(arg, str):
            return registers[arg]
        return arg

    while True:
        instruction, *args = data[position]
        position += 1
        if instruction == "snd":
            await snd(get_value(args[0]))
        elif instruction == "rcv":
            res = await rcv(args[0])
            if res is not None:
                registers[args[0]] = res
        elif instruction == "jgz":
            x, y = args
            if get_value(x) > 0:
                position += get_value(y) - 1
        else:
            x, y = args
            op = OPS[instruction]
            registers[x] = op(registers[x], get_value(y))


async def part1(data):
    last_sound = 0

    async def snd(val):
        nonlocal last_sound
        last_sound = val

    async with trio.open_nursery() as n:
        async def rcv(val):
            if val != 0:
                n.cancel_scope.cancel()
                # we need a checkpoint since everything else is synchronous
                await trio.sleep(0)

        n.start_soon(run_program, data, snd, rcv)
        # n.start_soon(rcv,1)

    return last_sound


async def part2(data):
    send_counts = [0, 0]

    inputs = [trio.open_memory_channel(inf) for _ in range(2)]

    # detect deadlock via 1 sec timeout (this is kinda hack-y)
    with trio.move_on_after(1) as m:
        def get_send(i):
            async def send(val):
                snd, _recv = inputs[i]
                await snd.send(val)
                send_counts[i] += 1
                m.deadline = trio.current_time() + 1

            return send

        def get_recv(i):
            async def recv(_val):
                _snd, recv = inputs[i]
                res = await recv.receive()
                m.deadline = trio.current_time() + 1
                return res

            return recv

        async with trio.open_nursery() as n:
            n.start_soon(run_program, data, get_send(0), get_recv(1), 0)
            n.start_soon(run_program, data, get_send(1), get_recv(0), 1)
        # n.start_soon(rcv,1)

    return send_counts[1]


if __name__ == "__main__":
    # data = get_data(DAY, filename="day18_test.txt", year=YEAR)

    data = get_data(DAY, year=YEAR)
    print(data)
    res = trio.run(part1, data)
    print(res)
    # res = part2(data)
    res = trio.run(part2, data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    # submit(DAY, 2, res, year=YEAR)
