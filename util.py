import logging
from dataclasses import dataclass
from hashlib import md5
from math import inf
from heapq import heappush, heappop
from pathlib import Path
import os
from typing import Dict, Optional

import requests

from bs4 import BeautifulSoup
from functools import wraps
from time import time


# from pytesseract import pytesseract

def n_timing(n=10):
    def timing(f):
        @wraps(f)
        def wrap(*args, **kw):
            ts = time()
            for _ in range(n):
                result = f(*args, **kw)
            te = time()
            print('func:%r took: %2.4f sec for %s executions' % \
                  (f.__name__, te - ts, n))
            return result

        return wrap

    return timing


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r took: %2.4f sec' % \
              (f.__name__, te - ts))
        return result

    return wrap


this_file_location = os.path.dirname(os.path.abspath(__file__))
SESSION_ID_FILE = f"{this_file_location}/session.txt"

# SESSION_ID_FILE = f"{this_file_location}/test_session.txt"
# SESSION_ID_FILE = "test_session.txt"
INPUT_URL = "https://adventofcode.com/{year}/day/{day}/input"
ANSWER_URL = "https://adventofcode.com/{year}/day/{day}/answer"
INPUT_DIRECTORY = "input"


def get_session_id():
    with open(SESSION_ID_FILE, "r") as f:
        return f.read().strip()


def get_cookie():
    session_id = get_session_id()
    return {'session': session_id}


def get_input(day, year):
    url = INPUT_URL.format(day=day, year=year)
    logging.warning("fetching [url]=%s", url)
    r = requests.get(url, cookies=get_cookie())
    return r.text


def get_input_cached(day, year):
    year_path = os.path.join(INPUT_DIRECTORY, f"{year}")
    Path(year_path).mkdir(parents=True, exist_ok=True)
    filename = os.path.join(year_path, f"{day:02}.txt")
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError as e:
        print("not found. fetching from source")
        fetched_input = get_input(day, year)
        with open(filename, "w") as f:
            f.write(fetched_input)
        return fetched_input


def parse_entry(entry):
    for test_type in int, float, str:
        try:
            return test_type(entry)
        except:
            pass


def parse_data(raw_data, separator=None):
    lines = raw_data.split("\n")
    if len(lines[0].split(separator)) > 1:
        return [[*map(parse_entry, l.split())] for l in lines]
    else:
        return [*map(parse_entry, lines)]


def get_data(day, raw=False, separator=None, filename=None, year=2021):
    if filename:
        raw_data = open(filename, "r").read().strip()
    else:
        raw_data = get_input_cached(day, year=year).strip("\n")
    if raw:
        return raw_data
    return parse_data(raw_data, separator)


def submit(day, level, answer, year=2021):
    data = {"level": level, "answer": answer}
    r = requests.post(ANSWER_URL.format(day=day, year=year),
                      data=data,
                      cookies=get_cookie())

    soup = BeautifulSoup(r.text, 'html.parser')

    response = soup.find_all("main")[0].get_text()
    print(response)
    return response


# general util:


def md5_hash(word: str):
    return md5(word.encode("ASCII")).hexdigest()


@dataclass(frozen=True)
class SearchResult:
    distances: Dict[any, int]
    shortest_distance: int
    shortest_node: any
    predecessors: Dict[any, any]


# graph stuff:


def connected_components(gen_neighbors, nodes):
    nodes = set(nodes)
    components = []
    while nodes:
        node = nodes.pop()
        res = dfs(gen_neighbors=gen_neighbors, initial_state=node)
        connected = set(res.distances)
        components += [connected]
        nodes -= connected
    return components


def dfs(gen_neighbors,
        initial_state,
        is_final_state=None,
        short_circuit=True) -> Optional[SearchResult]:
    distances = {initial_state: 0}
    predecessors = {}
    predecessors[initial_state] = None
    frontier = {initial_state}
    shortest_node = None
    while frontier:
        # print(len(frontier))
        new_frontier = set()
        for val in frontier:
            for neighbor in gen_neighbors(val):
                if neighbor in distances:
                    continue
                distances[neighbor] = distances[val] + 1
                predecessors[neighbor] = val
                if is_final_state is not None and is_final_state(neighbor):
                    shortest_node = neighbor
                    if short_circuit:
                        return SearchResult(
                            distances=distances,
                            shortest_distance=distances[neighbor],
                            predecessors=predecessors,
                            shortest_node=neighbor)
                new_frontier.add(neighbor)
        frontier = new_frontier
        # print(len(frontier))

    return SearchResult(distances=distances,
                        shortest_distance=distances[shortest_node]
                        if shortest_node is not None else inf,
                        predecessors=predecessors,
                        shortest_node=shortest_node)


def a_star_search(gen_neighbors, initial_state, is_final_state, heuristic):
    frontier = []
    heappush(frontier, (0, initial_state))
    came_from = {}
    cost_so_far = {}
    came_from[initial_state] = None
    cost_so_far[initial_state] = 0
    min_heuristic = inf
    while len(frontier):
        # print("---")
        if len(cost_so_far) % 10000 == 0:
            print(len(cost_so_far), min_heuristic)
        _, current = heappop(frontier)

        if is_final_state(current):
            print("visited", len(cost_so_far))
            return cost_so_far[current], came_from, current

        for next, cost in gen_neighbors(current):
            new_cost = cost_so_far[current] + cost
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                heur = heuristic(next)
                min_heuristic = min(min_heuristic, heur)
                priority = new_cost + heur
                heappush(frontier, (priority, next))
                came_from[next] = current


def ocr_array(im):
    image = Image.fromarray(im)
    return pytesseract.image_to_string(image)
