# -*- coding: utf-8 -*-
"""
@author: Gao Chuanchao
"""
import random
import math


class Node:
    """
    This class defines the node manager of the Symphony DHT overlay.
    Each node manages the identifier between its predecessor and itself.
    Each node contains:
        node value
        predecessor
        successor
        the identifier it manages
    """
    def __init__(self, v, k):
        self.v = v
        self.k = k
        self.predecessor = None
        self.successor = None
        self.out_link = []
        self.in_link = []
        self.ids = []

    def add_id(self, identifier):
        self.ids.append(identifier)

    def add_out_link(self, node):
        if len(node.in_link) < self.k:
            self.out_link.append(node)
            node.in_link.append(self)


class Overlay:
    """
    This class defines the Symphony DHT overlay
    """
    def __init__(self, N, k):
        """
        Given the number of nodes in the overlay, initialize the DHT overlay
        """
        self.N = N
        self.k = k
        self.nodes = dict()
        for i in range(0, N):
            self.nodes[i] = Node(i, k)

        # ========== add short link =============
        # handle first node and last node
        node = self.nodes[0]
        node.predecessor = self.nodes[N-1]
        node.successor = self.nodes[1]

        node = self.nodes[N-1]
        node.predecessor = self.nodes[N-2]
        node.successor = self.nodes[0]

        # handle intermediate nodes
        for i in range(1, N-1):
            node = self.nodes[i]
            node.predecessor = self.nodes[i-1]
            node.successor = self.nodes[i+1]

        # ========== add long link =============
        for i in range(N):
            while len(self.nodes[i].out_link) < k:
                x = math.ceil(math.exp(math.log(N) * (random.random() - 1)) * N)
                if x > (N - 1):
                    x = 0
                if x == i:
                    continue
                self.nodes[i].add_out_link(self.nodes[x])

    def add_ids(self, identifier):
        """
        add identifier of social network nodes to the overlay
        """
        node_id = math.ceil(identifier * self.N)
        if node_id > (self.N - 1):
            node_id = 0
        self.nodes[node_id].add_id(identifier)

    def distance(self, a, b):
        """
        Calculate the distance between peer a and peer b
        """
        if a <= b:
            return b - a
        else:
            return self.N + b - a

    def find_finger(self, node, end_node):
        """
        Find the next node that is closest to the destination
        """
        current = node
        out_nodes = node.out_link + [node.successor]
        for n in out_nodes:
            if self.distance(n.v, end_node.v) < self.distance(current.v, end_node.v):
                current = n
        return current

    def get_hop_count(self, id1, id2):
        """
        Get the hop count for id1 to find id2 in clockwise direction
        """
        start_node = self.nodes[math.ceil(id1 * self.N)]
        end_node = self.nodes[math.ceil(id2 * self.N)]
        if start_node.v == end_node.v:
            return 0

        next_node = self.find_finger(start_node, end_node)
        count = 1
        while next_node.v != end_node.v:
            next_node = self.find_finger(next_node, end_node)
            count += 1

        return count










