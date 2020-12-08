from pathlib import Path
import os

import requests
from bs4 import BeautifulSoup

from functools import wraps
from time import time


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r took: %2.4f sec' % \
          (f.__name__, te-ts))
        return result

    return wrap


SESSION_ID_FILE = "session.txt"
#SESSION_ID_FILE = "test_session.txt"
INPUT_URL = "https://adventofcode.com/2020/day/{day}/input"
ANSWER_URL = "https://adventofcode.com/2020/day/{day}/answer"
INPUT_DIRECTORY = "input"


def get_session_id():
    with open(SESSION_ID_FILE, "r") as f:
        return f.read().strip()


def get_cookie():
    session_id = get_session_id()
    return {'session': session_id}


def get_input(day):
    r = requests.get(INPUT_URL.format(day=day), cookies=get_cookie())
    return r.text


def get_input_cached(day):
    Path(INPUT_DIRECTORY).mkdir(parents=True, exist_ok=True)
    filename = os.path.join(INPUT_DIRECTORY, f"{day}.txt")
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError as e:
        print("not found. fetching from source")
        fetched_input = get_input(day)
        with open(filename, "w") as f:
            f.write(fetched_input)
        return fetched_input


def parse_entry(entry):
    for test_type in int, float, str:
        try:
            return test_type(entry)
        except:
            pass


def get_data(day, raw=False, separator=None, filename=None):
    if filename:
        raw_data = open(filename, "r").read().strip()
    else:
        raw_data = get_input_cached(day).strip()
    if raw:
        return raw_data
    lines = raw_data.split("\n")
    if len(lines[0].split(separator)) > 1:
        return [[*map(parse_entry, l.split())] for l in lines]
    else:
        return [*map(parse_entry, lines)]


def submit(day, level, answer):
    data = {"level": level, "answer": answer}
    r = requests.post(ANSWER_URL.format(day=day),
                      data=data,
                      cookies=get_cookie())

    soup = BeautifulSoup(r.text, 'html.parser')

    response = soup.find_all("main")[0].get_text()
    print(response)
    return response
