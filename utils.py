# -*- coding: utf-8 -*-
"""
@author: Gao Chuanchao
"""
import random

import math
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
    for n in G.nodes:
        ol.add_ids(n["identifier"])


def node_selection(scheme):
    """
    choose node for exchange with the given scheme.
        scheme: direct, greedy, smart, random
    """
    pass

def get_cost(G, ol, i, j, scheme):
    """
    Calculate the cost of a node i in the social network graph G
    """
    cost = 0
    neighbors = nx.neighbors(G, i)
    if "euclidean" == scheme:
        for n in neighbors:
            cost += strength(G, i, n) * get_euclidean_distance(G, j, n)
    elif "hop" == scheme:
        for n in neighbors:
            cost += strength(G, i, n) * get_hop_count(G, ol, j, n)

    return cost


def cost_evaluation(G, ol, i, j, scheme):
    """
    Calculate the cost of swapping.
    """
    if "euclidean" == scheme:
        old_cost = get_cost(G, ol, i, i, "euclidean") + get_cost(G, ol, j, j, "euclidean")
        new_cost = get_cost(G, ol, i, j, "euclidean") + get_cost(G, ol, j, i, "euclidean")
        if old_cost >= new_cost:
            identifier_exchange(G, i, j)
    elif "hop" == scheme:
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



