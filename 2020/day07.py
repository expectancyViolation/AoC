from util import *
import re
import networkx as nx
from networkx.algorithms.dag import topological_sort
import time

DAY = 7

ROOT_BAG = "shiny gold bag"


def parse_line(line):
    matches = re.match(r"^(.*)\ contain\ (.*)$", line)
    containing_bag, rest_of_string = matches.groups()
    containing_bag = containing_bag.rstrip("s")
    contained_bags = [(int(n), x.rstrip("s")) for n, x, _ in re.findall(
        r"([0-9]+)\ ([^\,\.]*)(\,|\.)", rest_of_string)]
    return containing_bag, contained_bags


# graph where edge (x,y) with weight w means:
# w bags of x are contained in bag y
def build_containment_graph(data):
    lines = data.split("\n")
    edges = ((bag, containing_bag, n)
             for (containing_bag, contained_bags) in map(parse_line, lines)
             for (n, bag) in contained_bags)
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)
    return G


def part1(G):
    bfs = nx.bfs_tree(G, ROOT_BAG)
    return len(bfs) - 1


def part2(G):
    vals = {}
    for node in topological_sort(G):
        curr_val = 1 + sum(vals[other] * G[other][node]['weight']
                           for (other, _) in G.in_edges(node))
        vals[node] = curr_val
    return vals[ROOT_BAG] - 1


if __name__ == "__main__":
    started = time.time()
    data = get_data(DAY, raw=True)
    #data = open("input/7_bigboi.txt", "r").read().strip()
    G = build_containment_graph(data)
    res = part1(G)
    print(res)
    res = part2(G)
    print(res)
    #submit(DAY, 1, res)
    # submit(DAY, 2, res)
    print(f"took {time.time()-started:.2f}s")
