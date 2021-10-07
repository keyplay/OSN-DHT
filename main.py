# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 14:56:53 2021

@author: Hou Yubo
"""

import snap
import networkx as nx
import os

filename = 'facebook_combined.txt'
folder = 'data'

def load_snap(filename):
    # load from a text file
    G = snap.LoadEdgeList(snap.TUNGraph, filename, 0, 1)  #snap.TNGraph: directed, snap.TUNGraph: undirect
    print("Graph: Nodes %d, Edges %d" % (G.GetNodes(), G.GetEdges()))
    
    for NI in G.Nodes():
        print("node: %d, out-degree %d, in-degree %d" % ( NI.GetId(), NI.GetOutDeg(), NI.GetInDeg()))
    
    CntV = G.GetOutDegCnt()
    for p in CntV:
        print("degree %d: count %d" % (p.GetVal1(), p.GetVal2()))


def load_graph(filename, directed_flag=False):
    # load from a text file
    if directed_flag:
        G = nx.read_edgelist(filename, create_using=nx.DiGraph(), nodetype = int)
    else:
        G = nx.read_edgelist(filename, create_using=nx.Graph(), nodetype = int)
    
    # check if the data has been read properly or not.
    print(nx.info(G))
 
    return G


def get_cost(G, method):
    def get_distance(x1, x2, method):
        if method == 'euclidean':
            dist = abs(x1-x2)
        else:
            pass  # to do
        
        return dist
    
    cost = 0
    for node in nx.nodes(G):
        neighbors = list(nx.neighbors(G, node))
        for neig_node in neighbors:
            common_neighbors = sorted(nx.common_neighbors(G, node, neig_node))
            strength = len(common_neighbors) / len(neighbors)
            dist = get_distance(node, neig_node, method)
            cost += dist * strength
            
    return cost
        

if __name__ == '__main__':
    G = load_graph(os.path.join(folder, filename))
    #Adj_mat = nx.adjacency_matrix(G)
    
    print(get_cost(G, 'euclidean'))
    
    

    
  