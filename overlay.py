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





