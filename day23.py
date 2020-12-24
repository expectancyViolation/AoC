from util import get_data, submit, timing

DAY = 23

# "clean" BUT: this is kinda slow
# the complexity is right, but still too much indirection and temporary object


class LinkedCycle:
    def __init__(self, inital_cycle):
        self._list_ = [0] * len(inital_cycle)
        assert set(inital_cycle) == set(range(len(inital_cycle)))
        for i, x in enumerate(inital_cycle[:-1]):
            self._list_[x] = inital_cycle[i + 1]
        self._list_[inital_cycle[-1]] = inital_cycle[0]

    def get_next(self, x, n_steps=1):
        curr = x
        for _ in range(n_steps):
            curr = self._list_[curr]
        return curr

    def set_next(self, x, y):
        self._list_[x] = y

    def __len__(self):
        return len(self._list_)

    def get_cycles(self):
        res = []
        remaining = set(range(len(self._list_)))
        while remaining:
            cycle_start = remaining.pop()
            curr = [cycle_start + 1]
            next_node = cycle_start
            while (next_node := self.get_next(next_node)) in remaining:
                remaining.remove(next_node)
                curr += [next_node + 1]
            res += [curr]
        return res

    def __repr__(self):
        return f"cycle_list({self.get_cycles()})({self._list_})"


def quick_step(cycle: LinkedCycle, start_node):
    next_nodes = []
    curr_node = start_node
    for _ in range(4):
        curr_node = cycle.get_next(curr_node)
        next_nodes += [curr_node]
    destination_node = (start_node - 1) % len(cycle)
    while destination_node in next_nodes[:3]:
        destination_node = (destination_node - 1) % len(cycle)
    after_dest = cycle.get_next(destination_node)
    cycle.set_next(destination_node, next_nodes[0])
    cycle.set_next(next_nodes[2], after_dest)
    cycle.set_next(start_node, next_nodes[3])
    return next_nodes[3]


def solve(start_vals, n):
    cyc = LinkedCycle([x - 1 for x in start_vals])
    curr_val = data[0] - 1
    for i in range(n):
        if i % 1000000 == 0:
            print(i)
        curr_val = quick_step(cycle=cyc, start_node=curr_val)
    res = cyc.get_cycles()[0]
    #print(res)
    return res


@timing
def part1(data):
    res = solve(data, 100)
    return "".join(map(str, res[1:]))


@timing
def part2(data):
    long_data = data + [*range(len(data) + 1, 10**6 + 1)]
    res = solve(long_data, 10**7)
    return res[1] * res[2]


if __name__ == "__main__":
    data = get_data(DAY)
    #data = ["389125467"]
    data = [int(x) for x in str(data[0])]
    #print(data)

    res = part1(data)
    print(res)
    #submit(DAY, 1, res)

    res = part2(data)
    print(res)
    submit(DAY, 2, res)
