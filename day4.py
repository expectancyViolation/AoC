from util import get_data, submit
import re
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
DAY = 4


def parse_entries(data):
    records = data.split("\n\n")
    return [dict(re.findall(r"(\S+):(\S+)", record)) for record in records]


def entry_is_valid(schema, entry):
    try:
        validate(instance=entry, schema=schema)
        return True
    except ValidationError:
        return False


def num_valid_entries(schema_file, entries):
    with open(schema_file, "r") as f:
        schema = json.load(f)
    return sum(1 for entry in entries if entry_is_valid(schema, entry))


def part1(data):
    return num_valid_entries("day4_schema_part1.json", parse_entries(data))


def part2(data):
    return num_valid_entries("day4_schema_part2.json", parse_entries(data))


if __name__ == "__main__":
    data = get_data(DAY, raw=True)
    res = part1(data)
    print(f"part 1:{res}")
    #submit(DAY, 1, res)
    res = part2(data)
    print(f"part 2:{res}")
    #submit(DAY, 2, res)
