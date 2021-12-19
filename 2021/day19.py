import time
from collections import Counter, defaultdict
from itertools import combinations, permutations, product
from random import shuffle

import numpy as np

from util import *

DAY = 19
YEAR = 2021


def manhattan(v1, v2):
    return sum(abs(x - y) for x, y in zip(v1, v2))


def all_distances(scanner):
    distances = defaultdict(lambda: [])
    for (i1, v1), (i2, v2) in combinations(
            enumerate(scanner), 2):
        distances[manhattan(v1, v2)].append((i1, i2))
    return dict(distances)


def find_overlap(d1, d2, scanner1, scanner2, score_limit=12):
    reference_scanner = [tuple(x) for x in scanner1]
    reference_distances = d1
    reference_vectors = defaultdict(lambda: [])
    for d, pairs in reference_distances.items():
        for i, j in pairs:
            reference_vectors[d].append(tuple(scanner1[j] - scanner1[i]))
    for perm in permutations([0, 1, 2]):
        for signs in product([-1, 1], repeat=3):
            match = 0
            coords = [np.array([x[v] * s for v, s in zip(perm, signs)]) for
                      x in
                      scanner2]
            offsets = defaultdict(lambda: 0)
            for x in reference_distances:
                if x not in d2:
                    continue
                for i, j in d2[x]:
                    vec = coords[j] - coords[i]
                    if vec[0] < 0:
                        vec = -vec
                    vec = tuple(vec)
                    v = reference_vectors[x][0]
                    for v in reference_vectors[x]:
                        if vec == v:
                            match += 1
                            for a in i, j:
                                for b in reference_distances[x][0]:
                                    offsets[
                                        tuple(coords[a] - reference_scanner[
                                            b])] += 1
            if match > 0:
                cnt, transform = max((y, x) for x, y in offsets.items())
                if cnt >= score_limit:
                    best_match_offset = transform
                    best_match_coords = [
                        np.array([x - t for x, t in zip(X, transform)]) for X in
                        coords]
                    return best_match_coords, best_match_offset
    return None, None


@timing
def part1(scanners):
    not_matched_indices = {i for i in range(1, len(scanners))}
    distances = {i: all_distances(scanner) for i, scanner in
                 enumerate(scanners)}
    all_coords = {tuple(x) for x in scanners[0]}
    # current_reference_points = scanners[0]
    real_coords = {0: [x for x in scanners[0]]}
    frontier = {0}
    offsets = []
    score_limit = 12
    while not_matched_indices:
        nf = set()
        for i in frontier:
            coords = real_coords[i]
            for j in [*not_matched_indices]:
                best_match_coords, offset = find_overlap(distances[i],
                                                         distances[j],
                                                         coords, scanners[j],
                                                         score_limit)
                if best_match_coords:
                    all_coords |= {tuple(x) for x in best_match_coords}
                    not_matched_indices.remove(j)
                    nf.add(j)
                    real_coords[j] = best_match_coords
                    offsets.append(offset)
        frontier = nf
    print(all_coords)

    m = 0
    for v1, v2 in combinations(offsets, 2):
        curr = sum(abs(x1 - x2) for x1, x2 in zip(v1, v2))
        m = max(m, curr)
    print(m)
    return len(all_coords)


def part2(data):
    return None


def parse_scatter(scanner):
    # print(scanner)
    return [np.array([*map(int, line.split(","))], dtype=int) for line in
            scanner.split("\n")[1:]]


if __name__ == "__main__":
    raw_data = get_data(DAY, year=YEAR, raw=True)
    # raw_data = datata
    results = []
    times = []
    scanners = [*map(parse_scatter, raw_data.split("\n\n"))]
    print(len(scanners))
    shuffle(scanners)
    res = part1(scanners)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    # res = part2(data)
    # print(res)
    # submit(DAY, 2, res,year=YEAR)
