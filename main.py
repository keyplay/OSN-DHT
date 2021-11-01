# -*- coding: utf-8 -*-
"""
@author: Yubo, Chuanchao
"""
import math
import networkx as nx
import os
import utils
from overlay import Overlay
import matplotlib.pyplot as plt
import numpy as np

filename = 'facebook_combined.txt'
folder = 'data'


if __name__ == '__main__':
    # load social network graph
    G = utils.load_graph(os.path.join(folder, filename))
    N = 1000
    T = 500
    K = int(math.log(N))
    order_type = 'random' # ascending, random
    target = "hop" #two setting: hop  euclidean
    select_method = 'greedy'  # direct greedy smart random
    utils.assign_identifier(G)


    # generate the top k strongest friends for each node for smart selection
    print("Start to generate top k friends...")
    nei = {}
    #for node in nx.nodes(G):
     #   nei[node] = utils.get_k_friends(G, node, K)

    # initialize symphony overlay and connect with social network
    print("Initialize symphony overlay...")
    ol = Overlay(N, K)
    print("Link to social network...")
    utils.link_overlay(G, ol)

    if order_type == 'descending':
        ordered_node_list = sorted(G.degree, key=lambda x: x[1], reverse=True)
    elif order_type == 'ascending':
        ordered_node_list = sorted(G.degree, key=lambda x: x[1], reverse=False)
    elif order_type == 'random':
        ordered_node_list = nx.nodes(G)

    # =========== Refinement ===========
    # node selection
    print("Node refinement...")
    hop_cost_list = []
    migration_cost_list = []
    reliability_1_list = []
    reliability_2_list = []
    reliability_3_list = []
    for t in range(T):
        # initialize a dict to indicate whether a node has been swapped or not
        swap_nodes = {}
        for n in nx.nodes(G):
            swap_nodes[n] = False
            
        ex_count = 0
        gossip_cnt = 0
        
        
        for node in ordered_node_list:  #nx.nodes(G):
            if order_type in ['descending', 'ascending']:
                node = node[0]
                
            # if the node has already been swapped in iteration-t, then skip it
            if swap_nodes[node]:
                continue
            
            node_j, sub_gossip_cnt = utils.node_selection(G, ol, nei, node, select_method)
            sub_ex_count = utils.cost_evaluation(G, ol, node, node_j, "euclidean")  #two setting: hop  euclidean
            # if the two nodes has been swapped, change their status
            if sub_ex_count == 1:
                swap_nodes[node] = True
                swap_nodes[node_j] = True
                
            gossip_cnt += sub_gossip_cnt
            ex_count += sub_ex_count
        migration_cost = ex_count / gossip_cnt
        
        # performance
        hop_cost = 0
        friends_hop_list = []
        for node in nx.nodes(G):
            sub_hop_cost = 0
            neighbors = list(nx.all_neighbors(G, node))
            for node_nei in neighbors:
                sub_hop_cost += utils.get_hop_count(G, ol, node, node_nei)
                friends_hop_list.append(sub_hop_cost)
            sub_hop_cost /= len(neighbors)
            hop_cost += sub_hop_cost
        hop_cost /= len(nx.nodes(G))
        hop_cost_list.append(hop_cost)
        migration_cost_list.append(migration_cost)
        
        unique, counts = np.unique(np.array(friends_hop_list), return_counts=True)
        friend_hop_dict = dict(zip(unique, counts))
        reliability_1 = friend_hop_dict[1] / N / K
        reliability_1_list.append(reliability_1)
        reliability_2 = friend_hop_dict[2] / N / K
        reliability_2_list.append(reliability_2)
        reliability_3 = friend_hop_dict[3] / N / K
        reliability_3_list.append(reliability_3)
        
        print(t, hop_cost, migration_cost, reliability_1, reliability_2, reliability_3)

    cost_list = np.array([hop_cost_list, migration_cost_list]).T
    np.savetxt(target+'_cost.csv', cost_list, delimiter=',') 

    plt.figure()
    plt.plot(np.arange(len(hop_cost_list)), hop_cost_list)
    plt.title('Loopup Latency')
    plt.savefig('Loopup Latency '+select_method+order_type+'.png')
    
    plt.figure()
    plt.plot(np.arange(len(migration_cost_list)), migration_cost_list)
    plt.title('Migration Cost')
    plt.savefig('Migration Cost '+select_method+order_type+'.png')
    
    plt.figure()
    plt.plot(np.arange(len(reliability_1_list)), reliability_1_list)
    plt.title('Reliability 1')
    plt.savefig('Reliability 1 '+select_method+order_type+'.png')
    
    plt.figure()
    plt.plot(np.arange(len(reliability_2_list)), reliability_2_list)
    plt.title('Reliability 2')
    plt.savefig('Reliability 2 '+select_method+order_type+'.png')
    
    plt.figure()
    plt.plot(np.arange(len(reliability_3_list)), reliability_3_list)
    plt.title('Reliability 3')
    plt.savefig('Reliability 3 '+select_method+order_type+'.png')

