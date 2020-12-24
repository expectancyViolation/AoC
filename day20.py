from collections import defaultdict
from itertools import product
from math import prod

import numpy as np
from scipy.signal import convolve2d

from util import submit, get_data, timing

DAY = 20


def get_edge_hashes(tile_dict):
    hashes = defaultdict(lambda: defaultdict(set))
    for tile_id, tile in tile_dict.items():
        for dir, vec in (("up", tile[0, :]), ("down", tile[-1, :]),
                         ('left', tile[:, 0]), ("right", tile[:, -1])):
            hashes[dir][tuple(vec)].add(tile_id)
    return hashes


def connections_from_edge_hashes(hashes):
    connections = defaultdict(lambda: {})
    for dir1, dir2 in ("up", "down"), ("left", "right"):
        for val, trafo_ids in hashes[dir1].items():
            if val in hashes[dir2]:
                other_ids = hashes[dir2][val]
                for trafo_id, other_id in product(trafo_ids, other_ids):
                    # do not connect to same tile_id
                    if other_id[0] != trafo_id[0]:
                        connections[dir1][trafo_id] = other_id
                        connections[dir2][other_id] = trafo_id
    return connections


def transform(tile, rot, flip):
    transformed = np.rot90(tile, rot)
    if flip:
        transformed = np.flip(transformed, 1)
    return transformed


def parse_tiles(data):
    tiles = {}
    for part in data:
        tile_id_line, *arr_lines = part.split("\n")
        tile_id = int(tile_id_line[-5:-1])
        arr = np.array([[x == "#" for x in line] for line in arr_lines],
                       dtype=np.int)
        tiles[tile_id] = arr
    return tiles


def get_tiles_with_connections(data):
    tiles = parse_tiles(data)

    # hash every possibe transformation of a tile
    #   => inefficiency of factor 8, but still "fast enough"
    trafo_tiles = {(tile_id, rot, flip): transform(tile, rot, flip)
                   for tile_id, tile in tiles.items() for rot in range(4)
                   for flip in (0, 1)}

    edge_hashes = get_edge_hashes(trafo_tiles)

    connections = connections_from_edge_hashes(edge_hashes)
    return trafo_tiles, connections


def neighbors(tile_id, connections):
    return {
        dir: conn[tile_id]
        for (dir, conn) in connections.items() if tile_id in conn
    }


def get_corners(tiles, connections):
    return {
        tile_id
        for tile_id in tiles if len(neighbors(tile_id, connections)) == 2
    }


def grid_bfs(tiles, connections):
    corners = get_corners(tiles, connections)
    left_upper_corner = next(
        tile_id for tile_id in corners
        if set(neighbors(tile_id, connections)) == {"down", "right"})
    frontier = {left_upper_corner}
    tile_positions = {left_upper_corner: (0, 0)}
    # bfs keeping track of tile positions
    while frontier:
        curr = frontier.pop()
        x, y = tile_positions[curr]
        for (dx, dy), direction in ((1, 0), "down"), ((0, 1), "right"):
            if curr in connections[direction]:
                new_el = connections[direction][curr]
                new_pos = (x + dx, y + dy)
                tile_positions[new_el] = new_pos
                frontier.add(new_el)
    return tile_positions


def stitch_tiles(tiles, tile_positions):
    width_in_tiles = 1 + max(y for (x, y) in tile_positions.values())
    height_in_tiles = 1 + max(x for (x, y) in tile_positions.values())
    trimmed_tile_size = 8
    full_image = np.zeros([
        width_in_tiles * trimmed_tile_size, height_in_tiles * trimmed_tile_size
    ],
                          dtype=np.int)
    for tile_id, (x, y) in tile_positions.items():
        tile = tiles[tile_id]
        full_image[trimmed_tile_size * x:trimmed_tile_size * (x + 1),
                   trimmed_tile_size * y:trimmed_tile_size *
                   (y + 1)] = tile[1:-1, 1:-1]
    return full_image


def get_monster_matrix():
    with open("input/20_monster.txt", "r") as f:
        lines = f.readlines()
        monster = np.array([[x == "#" for x in line.strip("\n")]
                            for line in lines],
                           dtype=np.int)
    return monster


@timing
def part1(data):
    trafo_tiles, connections = get_tiles_with_connections(data)
    trafo_corners = get_corners(trafo_tiles, connections)
    corners = {tile_id for (tile_id, _, _) in trafo_corners}
    print(corners)
    return prod(corners)


@timing
def part2(data):
    trafo_tiles, connections = get_tiles_with_connections(data)
    tile_positions = grid_bfs(trafo_tiles, connections)

    full_image = stitch_tiles(trafo_tiles, tile_positions)
    monster = get_monster_matrix()
    monster_count = np.sum(monster)

    # count the number of unoccupied positions
    # DANGER this assumes non-overlapping monsters
    res = np.sum(full_image)
    for rot in range(4):
        for flip in (0, 1):
            transformed_monster = np.rot90(monster, rot)
            if flip:
                transformed_monster = np.flip(transformed_monster, 1)
            match_scores = convolve2d(full_image, transformed_monster)
            res -= monster_count * np.sum(match_scores == monster_count)
    return res


if __name__ == "__main__":
    data = get_data(DAY, raw=True).split("\n\n")

    res = part1(data)
    print(res)
    #submit(DAY, 1, res)

    res = part2(data)
    print(res)
    #submit(DAY, 2, res)
