import re
from collections import defaultdict

from util import *

DAY = 25
YEAR = 2017

br = r".*"
state_regex = f"""
In state (?P<state>\w):
  If the current value is 0:
    - Write the value (?P<zero_write>\d).
    - Move one slot to the (?P<zero_move>.*).
    - Continue with state (?P<zero_cont_state>\w).
  If the current value is 1:
    - Write the value (?P<one_write>\d).
    - Move one slot to the (?P<one_move>.*).
    - Continue with state (?P<one_cont_state>\w)."""

header_regex = """Begin in state (?P<inital_state>\w).
Perform a diagnostic checksum after (?P<n_steps>\d+) steps.
"""


def to_val(s):
    if s in {"left", "right"}:
        return 1 if s == "right" else -1
    try:
        return int(s)
    except ValueError:
        return s


@timing
def simulate(data):
    tape = defaultdict(lambda: 0)
    curr_pos = 0
    curr_state, n_steps = map(to_val, re.search(header_regex, data).groups())
    states = {state: [*map(to_val, vals)]
              for
              state, *vals in re.findall(state_regex, data)}
    for _ in range(n_steps):
        vals = states[curr_state]
        ops_i = 3 if tape[curr_pos] == 1 else 0
        tape[curr_pos], move_dir, curr_state = vals[ops_i:ops_i + 3]
        curr_pos += move_dir
    return sum(tape.values())


def part1(data):
    return simulate(data)


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
