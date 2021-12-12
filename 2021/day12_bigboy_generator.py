import random
import string

import networkx as nx


def get_bigboy_graph(n, edge_probability=0.1):
    G = nx.gnp_random_graph(n, edge_probability)
    largest_cc = max(nx.connected_components(G), key=len)
    G = G.subgraph(largest_cc).copy()
    names = {i: "".join(random.sample(string.ascii_lowercase, 2)) for i in
             range(N)}
    G = nx.relabel_nodes(G, names)
    uppercasers = nx.maximal_independent_set(G)
    names = {letters: letters.upper() if letters in uppercasers else letters for
             letters in G.nodes}
    a, b, *_ = names
    names[a] = "start"
    names[b] = "end"
    G = nx.relabel_nodes(G, names)
    return G


N = 30
G = get_bigboy_graph(N)
lines = [f"{node1}-{node2}\n" for node1, node2 in G.edges()]
with open(f"output/12_bigboi_{N}_nodes.txt", "w") as f:
    f.write("".join(lines))
