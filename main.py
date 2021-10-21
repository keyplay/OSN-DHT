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
    N = nx.number_of_nodes(G)
    K = math.log(N)
    utils.assign_identifier(G)

    # generate the top k strongest friends for each node for smart selection
    nei = {}
    for node in nx.nodes(G):
        nei[node] = utils.get_k_friends(G, node, K)

    # initialize symphony overlay and connect with social network
    ol = Overlay(N, K)
    utils.link_overlay(G, ol)

    # =========== Refinement ===========
    # node selection
    for node in nx.nodes(G):
        node_j = utils.node_selection(G, ol, nei, node, "direct")
        utils.cost_evaluation(G, ol, node, node_j, "euclidean")




    
    

    
  