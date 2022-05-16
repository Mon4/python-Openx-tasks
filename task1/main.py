import pickle
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, domain, seller_type, children):
        self.domain = domain
        self.seller_type = seller_type
        self.children = children


handle = open('filename.pickle', 'rb')
file = pickle.load(handle)


graph = nx.Graph()

max_depth = 0
color_map = []


def foo(node, parent, depth):
    global graph
    global max_depth
    if depth > max_depth:
        max_depth = depth

    if not node.seller_type == 'publisher':
        graph.add_node(node.domain, depth=depth)

        if parent is not None:
            graph.add_edge(parent.domain, node.domain)
    if node.children is not None:
        for i in node.children.values():
            foo(i, node, depth+1)


foo(file, None, 0)

nodes = graph.nodes()
colors = [graph.nodes[n]['depth'] for n in nodes]

pos = nx.spring_layout(graph)
ec = nx.draw_networkx_edges(graph, pos, alpha=0.2)
nc = nx.draw_networkx_nodes(graph, pos, nodelist=nodes, node_color=colors, cmap=plt.get_cmap("Blues_r"))
plt.colorbar(nc)
plt.show()

