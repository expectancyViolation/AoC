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


def perm_inversions(perm):
    return sum(perm[i] > perm[j] for i, j in combinations(range(len(perm)), 2))


def sign_inversions(signs):
    return sum(1 for x in signs if x == -1)


@lru_cache(maxsize=1)
def get_valid_transforms(d=3):
    return [(perm, signs) for perm in permutations(range(d))
            for signs in product([-1, 1], repeat=d)
            if (perm_inversions(perm) + sign_inversions(signs)) % 2 == 0]


def transform(v, perm, signs):
    return [v[i] * s for i, s in zip(perm, signs)]


def l2_sq(v1, v2):
    return sum((x1 - x2) ** 2 for x1, x2 in zip(v1, v2))


# this depends on the assumption that
# any triangle of 3 points in the scans is unique
# (i.e. its triple of side lengths)
def find_correspondences(scanners):
    tris = defaultdict(lambda: {})
    for i, scanner in enumerate(scanners):
        d_2 = [[l2_sq(p, q) for j, q in enumerate(scanner)]
               for i, p in enumerate(scanner)]
        for i1, i2, i3 in combinations(range(len(scanner)), 3):
            sides = ((d_2[i1][i2], i3), (d_2[i2][i3], i1), (d_2[i1][i3], i2))
            distances, indices = zip(*sorted(sides))
            tris[distances][i] = indices
    correspondences = defaultdict(lambda: [])
    for dist, lookups in tris.items():
        if len(lookups) <= 1:
            continue
        for i, j in combinations(lookups, 2):
            for i1, i2 in zip(lookups[i], lookups[j]):
                correspondences[(i, j)].append((i1, i2))
    mappings = defaultdict()
    for (i, j), items in correspondences.items():
        mapping = {x: y for x, y in items}
        inverse_mapping = {y: x for x, y in items}
        if len(mapping) >= 12:
            mappings[(i, j)] = mapping
            mappings[(j, i)] = inverse_mapping

    return mappings


def find_overlap_matching(correspondences, real_scan, scan2):
    for trafo in get_valid_transforms():
        offset = None
        for i1, i2 in correspondences.items():
            transformed = transform(scan2[i2], *trafo)
            candidate_offset = tuple(
                [x - y for x, y in zip(real_scan[i1], transformed)])
            if offset is None:
                offset = candidate_offset
            elif offset != candidate_offset:
                break
        else:
            coords = [transform(x, *trafo) for x in scan2]
            best_match_offset = np.array(offset, dtype=int)
            best_match_coords = [X + best_match_offset for X in coords]
            return best_match_coords, best_match_offset


@timing
def solve(scanners):
    correspondences = find_correspondences(scanners)
    not_matched_indices = {i for i in range(1, len(scanners))}
    real_coords = {0: [x for x in scanners[0]]}
    frontier = {0}
    offsets = {0: (0, 0, 0)}
    while frontier:
        nf = set()
        for i in frontier:
            coords = real_coords[i]
            for j in [*not_matched_indices]:
                if (i, j) not in correspondences:
                    continue
                overlap = find_overlap_matching(correspondences[i, j], coords,
                                                scanners[j])
                if overlap:
                    best_match_coords, offset = overlap
                    not_matched_indices.remove(j)
                    nf.add(j)
                    real_coords[j] = best_match_coords
                    offsets[j] = offset
        frontier = nf
    m = 0
    for v1, v2 in combinations(offsets.values(), 2):
        curr = sum(abs(x1 - x2) for x1, x2 in zip(v1, v2))
        m = max(m, curr)
    all_coords = defaultdict(lambda: [])
    for scanner_id, points in real_coords.items():
        for point in points:
            all_coords[tuple(point)] += [scanner_id]
    return len(all_coords), m, offsets, all_coords


def parse_scanner(scanner):
    return [
        np.array([*map(int, line.split(","))], dtype=int)
        for line in scanner.split("\n")[1:]
    ]


def plot_result(scanner_positions, all_coords):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    X, Y, Z = zip(
        *[x for i, x in enumerate(scanner_positions.values()) if i != 0])
    ax.scatter(X, Y, Z, marker="o")
    x, y, z = scanner_positions[0]
    ax.scatter(x, y, z, marker="o", color="red")
    X, Y, Z, W = zip(
        *[(*v, len(w)) for v, w in all_coords.items()])
    s = ax.scatter(X, Y, Z, c=W, marker="x")
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    for v, w in all_coords.items():
        for i in w:
            x, y, z = zip(*[v, scanner_positions[i]])
            ax.plot(x, y, z, color=colors[i % len(colors)])
    plt.colorbar(s)
    plt.show()


if __name__ == "__main__":
    raw_data = get_data(DAY, year=YEAR, raw=True)
    results = []
    times = []
    scanners = [*map(parse_scanner, raw_data.split("\n\n"))]
    part1, part2, scanner_positions, all_coords = solve(scanners)
    # C = Counter(all_coords.values())
    # print(C)
    print(part1, part2)

    plot_result(scanner_positions, all_coords)

    # submit(DAY, 1, part1,year=YEAR)
    # submit(DAY, 2, part2,year=YEAR)
