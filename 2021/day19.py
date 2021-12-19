import time
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations, permutations, product
from math import prod
from random import shuffle
import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import numpy as np

from util import *

DAY = 19
YEAR = 2021


def manhattan(v1, v2):
    return sum(abs(x - y) for x, y in zip(v1, v2))


# use distance "signature" to speed up point matching
# common points have to have same manhattan distance in both scans
def all_distances(scanner):
    distances = defaultdict(lambda: [])
    for (i1, v1), (i2, v2) in combinations(enumerate(scanner), 2):
        distances[manhattan(v1, v2)].append((i1, i2))
    return dict(distances)


def perm_inversions(perm):
    return sum(perm[i] > perm[j]
               for i, j in combinations(range(len(perm)), 2))


def sign_inversions(signs):
    return sum(1 for x in signs if x == -1)


@lru_cache(maxsize=1)
def get_valid_transforms(d=3):
    return [(perm, signs)
            for perm in permutations(range(d))
            for signs in product([-1, 1], repeat=d)
            if (perm_inversions(perm) + sign_inversions(signs)) % 2 == 0]


def transform(v, perm, signs):
    return [v[i] * s for i, s in zip(perm, signs)]


def find_overlap(d1, d2, scanner1, scanner2, score_limit=12):
    reference_distances = d1
    reference_vectors = defaultdict(lambda: [])
    for d, pairs in reference_distances.items():
        for i, j in pairs:
            reference_vectors[d].append(tuple(scanner1[j] - scanner1[i]))
    for perm, signs in get_valid_transforms():
        match = False
        coords = [np.array(transform(v, perm, signs)) for v in scanner2]
        offset_counts = defaultdict(lambda: 0)
        for x in reference_distances:
            if x not in d2:
                continue
            for i, j in d2[x]:
                vec = coords[j] - coords[i]
                vec = tuple(vec)
                vec_inv = tuple(vec)
                for v in reference_vectors[x]:
                    if vec == v or vec_inv == v:
                        match = True
                        for a in i, j:
                            for b in reference_distances[x][0]:
                                offset_counts[tuple(coords[a] -
                                                    scanner1[b])] += 1
        if match:
            cnt, offset = max((y, x) for x, y in offset_counts.items())
            if cnt >= score_limit:
                best_match_offset = np.array(offset, dtype=int)
                best_match_coords = [X - best_match_offset for X in coords]
                return best_match_coords, best_match_offset


@timing
def solve(scanners):
    not_matched_indices = {i for i in range(1, len(scanners))}
    distances = {
        i: all_distances(scanner)
        for i, scanner in enumerate(scanners)
    }
    real_coords = {0: [x for x in scanners[0]]}
    frontier = {0}
    offsets = [[0, 0, 0]]
    while not_matched_indices:
        print(frontier)
        print(not_matched_indices)
        nf = set()
        for i in frontier:
            coords = real_coords[i]
            for j in [*not_matched_indices]:
                overlap = find_overlap(distances[i], distances[j], coords,
                                       scanners[j])
                if overlap:
                    best_match_coords, offset = overlap
                    not_matched_indices.remove(j)
                    nf.add(j)
                    real_coords[j] = best_match_coords
                    offsets.append(offset)
        frontier = nf
    m = 0
    for v1, v2 in combinations(offsets, 2):
        curr = sum(abs(x1 - x2) for x1, x2 in zip(v1, v2))
        m = max(m, curr)
    scanner_positions = [(-x, -y, -z) for x, y, z in offsets]
    all_coords = defaultdict(lambda: 0)
    for scanner_id, points in real_coords.items():
        for point in points:
            all_coords[tuple(point)] += 1
    return len(all_coords), m, scanner_positions, all_coords


def parse_scatter(scanner):
    return [
        np.array([*map(int, line.split(","))], dtype=int)
        for line in scanner.split("\n")[1:]
    ]


if __name__ == "__main__":
    raw_data = get_data(DAY, year=YEAR, raw=True)
    results = []
    times = []
    scanners = [*map(parse_scatter, raw_data.split("\n\n"))]
    part1, part2, scanner_positions, all_coords = solve(scanners)
    C = Counter(all_coords.values())
    print(C)
    print(part1, part2)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    X, Y, Z = zip(*scanner_positions)
    ax.scatter(X, Y, Z, marker="o")
    X, Y, Z, W = zip(*[(*v, w) for v, w in all_coords.items() if w>1])
    s=ax.scatter(X, Y, Z,c=W, marker="x")
    plt.colorbar(s)
    plt.show()
    # submit(DAY, 1, part1,year=YEAR)
    # submit(DAY, 2, part2,year=YEAR)
