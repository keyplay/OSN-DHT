# -*- coding: utf-8 -*-
"""
@author: Gao Chuanchao
"""
import random
import networkx as nx


def load_graph(filename, directed_flag=False):
    # load from a text file
    if directed_flag:
        G = nx.read_edgelist(filename, create_using=nx.DiGraph(), nodetype=int)
    else:
        G = nx.read_edgelist(filename, create_using=nx.Graph(), nodetype=int)

    # check if the data has been read properly or not.
    print(nx.info(G))

    return G

def strength(G, i, j):
    """
    Calculate the strength of two nodes in a Graph
    """
    com = len(sorted(nx.common_neighbors(G, i, j)))
    nei = len(sorted(nx.all_neighbors(G, i)))
    return com / nei


def assign_identifier(G):
    """
    Assign a random identifier to each node and generate the DHT with Symphony protocol
    """
    for node in nx.nodes(G):
        nx.set_node_attributes(G, {node: random.random()}, name="identifier")


def get_euclidean_distance(G, i, j):
    """
    Calculate Euclidean distance between two node ids.
    """
    return abs(G.nodes[i]["identifier"] - G.nodes[j]["identifier"])


def get_hop_count(G, i, j):
    """
    Calculate the lookup latency (hop count) between two nodes
    """
    pass

def get_symphony(G):
    """
    Generate the Symphony overlay based on the ids assigned to the nodes
    """
    DHT = nx.DiGraph()
    nodes = sorted(nx.get_node_attributes(G, "identifier").values())
    DHT.add_nodes_from(nodes)
    # add short links
    for i in range(len(nodes)-1):
        DHT.add_edge(nodes[i], nodes[i+1])
    DHT.add_edge(nodes[-1], nodes[0])
    # add long links


