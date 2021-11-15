from util import get_data, submit, timing
from copy import deepcopy

import networkx as nx
#import matplotlib.pyplot as plt
from networkx.algorithms import bfs_tree
#from networkx.drawing.nx_agraph import write_dot

DAY = 8


def part1(data):
    visited = set()
    pos_pointer = 0
    acc = 0
    while not (pos_pointer in visited) and (0 <= pos_pointer < len(data)):
        visited.add(pos_pointer)
        inst, arg = data[pos_pointer]
        pos_pointer += 1
        if inst == "acc":
            acc += arg
        elif inst == "jmp":
            pos_pointer += arg - 1
    return acc, pos_pointer


@timing
def part2(data):
    for i, (inst, arg) in enumerate(data):
        if inst in ("jmp", "nop"):
            swapped_inst = next(x for x in ("jmp", "nop") if x != inst)
            swapped_data = deepcopy(data)
            swapped_data[i] = (swapped_inst, arg)
            acc, pos_pointer = part1(swapped_data)
            if pos_pointer == len(data):
                #print(i)
                return acc, pos_pointer


def to_edge(line_nr, inst, arg):
    if inst == "acc":
        return (line_nr, line_nr + 1, arg)
    elif inst == "jmp":
        return (line_nr, line_nr + arg, 0)
    return (line_nr, line_nr + 1, 0)


@timing
def part2_fast(data):
    edges = [to_edge(i, *op) for i, op in enumerate(data)]
    start_vertex, end_vertex = 0, len(data)
    G = nx.DiGraph()
    G.add_nodes_from([*range(len(data))])
    G.add_weighted_edges_from(edges)
    # TODO remove
    #write_dot(G, "test.dot")
    #print("G done")
    T = bfs_tree(G, start_vertex)
    Ts = set(T)
    G_rev = nx.DiGraph.reverse(G)
    T_rev = bfs_tree(G_rev, end_vertex)
    Ts_rev = set(T_rev)
    #print("prep done")
    for i, (inst, arg) in enumerate(data):
        #print(i)
        if inst in ("jmp", "nop"):
            swapped_inst = next(x for x in ("jmp", "nop") if x != inst)
            swapped_edge = to_edge(i, swapped_inst, arg)
            v1, v2, w = swapped_edge
            if (v1 in Ts) and (v2 in Ts_rev):
                G.add_edge(v1, v2, weight=w)
                # path = next(nx.all_simple_paths(G, start_vertex, end_vertex))
                return nx.shortest_path_length(G,
                                               start_vertex,
                                               end_vertex,
                                               weight="weight")
                # total_weight = sum(G[path[i]][path[i + 1]]['weight']
                #                    for i in range(len(path) - 1))
                # return total_weight


if __name__ == "__main__":
    data = get_data(DAY)
    #print(data)
    res, _ = part1(data)
    print(res)
    #res, _ = part2(data)
    res_fast = part2_fast(data)
    print(res_fast)
    #print(res)
    #print(res_fast)
    #assert res == res_fast
    #submit(DAY, 1, res)
    #submit(DAY, 2, res)
