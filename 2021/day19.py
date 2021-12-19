import time
from collections import Counter, defaultdict
from itertools import combinations, permutations, product
from random import shuffle

import numpy as np

from util import *

DAY = 19
YEAR = 2021


def all_distances(scanner):
    distances = defaultdict(lambda: [])
    for (i1, (x1, y1, z1)), (i2, (x2, y2, z2)) in combinations(
            enumerate(scanner), 2):
        distances[abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)].append((i1, i2))
    return distances


def find_overlap(scanner1, scanner2, score_limit=12):
    d1 = all_distances(scanner1)
    d2 = all_distances(scanner2)
    reference_scanner = [tuple(x) for x in scanner1]
    reference_distances = d1
    reference_vectors = defaultdict(lambda: [])
    for d, pairs in reference_distances.items():
        for i, j in pairs:
            reference_vectors[d].append(tuple(scanner1[j] - scanner1[i]))
    best_match_offset = None
    best_match_coords = None
    best_match_score = 0
    for perm in permutations([0, 1, 2]):
        for signs in product([-1, 1], repeat=3):
            match = 0
            coords = [np.array([x[v] * s for v, s in zip(perm, signs)]) for
                      x in
                      scanner2]
            offsets = []
            for x in reference_distances:
                # if len(reference_distances[x]) > 1:
                #     continue
                for i, j in d2[x]:
                    vec = coords[j] - coords[i]
                    if vec[0] < 0:
                        vec = -vec
                    vec = tuple(vec)
                    v = reference_vectors[x][0]
                    for v in reference_vectors[x]:
                        if vec == v:
                            match += 1
                            # print("match")
                            for a in i, j:
                                for b in reference_distances[x][0]:
                                    offsets.append(
                                        tuple(coords[a] - reference_scanner[b]))
                        else:
                            # print("nomatch")
                            # print(tuple(vec))
                            # print(reference_vectors[x])
                            pass
            if match > 0:
                cnt, transform = max(
                    (y, x) for x, y in Counter(offsets).items())
                if cnt > best_match_score:
                    best_match_score = cnt
                    best_match_offset = transform
                    best_match_coords = [
                        np.array([x - t for x, t in zip(X, transform)]) for X in
                        coords]
                    # print("match", match)
                    # print(transform, cnt)
                    # print(coords)
    if best_match_score < 12:
        # print("abandoning too low match score",best_match_score)
        return None, None
    else:
        pass
        # print("!!!!!!!",best_match_score)
    return best_match_coords, best_match_offset

@timing
def part1(scanners):
    not_matched_indices = {i for i in range(1, len(scanners))}
    all_coords = {tuple(x) for x in scanners[0]}
    # current_reference_points = scanners[0]
    real_coords = {0: [x for x in scanners[0]]}
    offsets = []
    score_limit = 12
    while not_matched_indices:
        for i, coords in [*real_coords.items()]:
            for j in [*not_matched_indices]:
                best_match_coords, offset = find_overlap(
                    coords, scanners[j],
                    score_limit)
                if best_match_coords:
                    # print(f"matched {i}")
                    all_coords |= {tuple(x) for x in best_match_coords}
                    not_matched_indices.remove(j)
                    real_coords[j]=best_match_coords
                    offsets.append(offset)
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
    res = part1(scanners)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    # res = part2(data)
    # print(res)
    # submit(DAY, 2, res,year=YEAR)
