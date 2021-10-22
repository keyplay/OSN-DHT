# -*- coding: utf-8 -*-
"""
@author: Chuanchao
"""
import math
import networkx as nx
import os
import utils
from overlay import Overlay

filename = 'facebook_combined.txt'
folder = 'data'


if __name__ == '__main__':
    # load social network graph
    G = utils.load_graph(os.path.join(folder, filename))
    N = 10000
    K = int(math.log(N))
    utils.assign_identifier(G)

    # generate the top k strongest friends for each node for smart selection
    print("Start to generate top k friends...")
    nei = {}
    # for node in nx.nodes(G):
    #     nei[node] = utils.get_k_friends(G, node, K)

    # initialize symphony overlay and connect with social network
    print("Initialize symphony overlay...")
    ol = Overlay(N, K)
    print("Link to social network...")
    utils.link_overlay(G, ol)

    # =========== Refinement ===========
    # node selection
    print("Node refinement...")
    T = 10
    for t in range(T):
        # initialize a dict to indicate whether a node has been swapped or not
        swap_nodes = {}
        for n in nx.nodes(G):
            swap_nodes[n] = False

        for node in nx.nodes(G):
            # if the node has already been swapped in iteration-t, then skip it
            if swap_nodes[node]:
                continue
            node_j = utils.node_selection(G, ol, nei, node, "direct")
            # if node j is already swapped, find another one
            while swap_nodes[node_j]:
                node_j = utils.node_selection(G, ol, nei, node, "direct")
            swapped = utils.cost_evaluation(G, ol, node, node_j, "euclidean")
            # if the two nodes has been swapped, change their status
            if swapped:
                swap_nodes[node] = True
                swap_nodes[node_j] = True




