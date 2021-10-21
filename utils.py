# -*- coding: utf-8 -*-
"""
@author: Gao Chuanchao
"""
import random
import networkx as nx
import snap


def load_graph(filename, directed_flag=False):
    # load from a text file
    if directed_flag:
        G = nx.read_edgelist(filename, create_using=nx.DiGraph(), nodetype=int)
    else:
        G = nx.read_edgelist(filename, create_using=nx.Graph(), nodetype=int)

    # check if the data has been read properly or not.
    print(nx.info(G))

    return G

def load_snap(filename):
    # load from a text file
    G = snap.LoadEdgeList(snap.TUNGraph, filename, 0, 1)  #snap.TNGraph: directed, snap.TUNGraph: undirect
    print("Graph: Nodes %d, Edges %d" % (G.GetNodes(), G.GetEdges()))

    for NI in G.Nodes():
        print("node: %d, out-degree %d, in-degree %d" % ( NI.GetId(), NI.GetOutDeg(), NI.GetInDeg()))

    CntV = G.GetOutDegCnt()
    for p in CntV:
        print("degree %d: count %d" % (p.GetVal1(), p.GetVal2()))

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
    Calculate Euclidean distance between two node ids, follow clockwise direction
    """
    if G.nodes[i]["identifier"] <= G.nodes[j]["identifier"]:
        return abs(G.nodes[j]["identifier"] - G.nodes[i]["identifier"])
    else:
        return 1 + abs(G.nodes[j]["identifier"] - G.nodes[i]["identifier"])


def get_hop_count(G, ol, i, j):
    """
    Calculate the lookup latency (hop count) between two nodes, follow clockwise direction
        G: social network graph
        ol: the symphony overlay
        i: the social network graph node
    """
    return ol.get_hop_count(G.nodes[i]["identifier"], G.nodes[j]["identifier"])


def link_overlay(G, ol):
    """
    link the social network graph with the symphony overlay
    """
    for n in nx.nodes(G):
        ol.add_ids(G.nodes[n]["identifier"])


def node_j_selection(G, ol, m):
    peer_m = ol.get_peer(G.nodes[m]["identifier"])

    return random.choice(peer_m.out_link + [peer_m.successor])


def direct_selection(G, ol, i):
    node_m = random.choice(list(nx.neighbors(G, i)))

    return node_j_selection(G, ol, node_m)


def greedy_selection(G, ol, i):
    node_m = None
    strength_m = 0
    for n in nx.neighbors(G, i):
        strength_n = strength(G, i, n)
        if strength_n > strength_m:
            node_m = n
            strength_m = strength_n

    return node_j_selection(G, ol, node_m)


def get_k_friends(G, i, k):
    """
    generate the top k strongest friends of node i
    """
    result = []
    k_neighbors = {}

    for n in nx.all_neighbors(G, i):
        k_neighbors[n] = strength(G, i, n)
    values = sorted(k_neighbors.values(), reverse=True)
    if len(values) > k:
        threshold = values[k - 1]
        for k, v in k_neighbors.items():
            if v >= threshold:
                result.append(k)
        return result
    else:
        return nx.neighbors(G, i)


def smart_selection(G, ol, nei, i):
    """
    :param nei: the dictionary of top k friends of node, {node : [friend1, friend2, ...]}
    """
    node_m = random.choice(nei[i])

    return node_j_selection(G, ol, node_m)


def random_selection(G, ol, i):
    node_m = random.choice(list(nx.nodes(G)))
    if i == node_m:
        node_m = random.choice(list(nx.nodes(G)))

    return node_j_selection(G, ol, node_m)


def node_selection(G, ol, nei, i, select_scheme):
    """
    choose node for exchange with the given scheme.
        scheme: direct, greedy, smart, random
    """
    if "direct" == select_scheme:
        return direct_selection(G, ol, i)
    elif "greedy" == select_scheme:
        return greedy_selection(G, ol, i)
    elif "smart" == select_scheme:
        return smart_selection(G, ol, nei, i)
    elif "random" == select_scheme:
        return random_selection(G, ol, i)


def get_cost(G, ol, i, j, cost_scheme):
    """
    Calculate the cost of a node i in the social network graph G
    """
    cost = 0
    neighbors = list(nx.all_neighbors(G, i))
    if "euclidean" == cost_scheme:
        for n in neighbors:
            cost += strength(G, i, n) * get_euclidean_distance(G, j, n)
    elif "hop" == cost_scheme:
        for n in neighbors:
            cost += strength(G, i, n) * get_hop_count(G, ol, j, n)

    return cost


def cost_evaluation(G, ol, i, j, cost_scheme):
    """
    Calculate the cost of swapping.
    """
    if "euclidean" == cost_scheme:
        old_cost = get_cost(G, ol, i, i, "euclidean") + get_cost(G, ol, j, j, "euclidean")
        new_cost = get_cost(G, ol, i, j, "euclidean") + get_cost(G, ol, j, i, "euclidean")
        if old_cost >= new_cost:
            identifier_exchange(G, i, j)
    elif "hop" == cost_scheme:
        old_cost = get_cost(G, ol, i, i, "hop") + get_cost(G, ol, j, j, "hop")
        new_cost = get_cost(G, ol, i, j, "hop") + get_cost(G, ol, j, i, "hop")
        if old_cost >= new_cost:
            identifier_exchange(G, i, j)


def identifier_exchange(G, i, j):
    """
    Change identifier of node i and node j if the cost is smaller after changing ids
    """
    id_i = G.nodes[i]["identifier"]
    id_j = G.nodes[j]["identifier"]
    G.nodes[i]["identifier"] = id_j
    G.nodes[j]["identifier"] = id_i
