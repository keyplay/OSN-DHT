# -*- coding: utf-8 -*-
"""
@author: Gao Chuanchao
"""
import random
import math


class Peer:
    """
    This class defines the peer manager of the Symphony DHT overlay.
    Each peer manages the identifier between its predecessor and itself.
    Each peer contains:
        peer value
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

    def add_node(self, node):
        self.ids.append(node)

    def add_out_link(self, peer):
        if len(peer.in_link) < peer.k:
            self.out_link.append(peer)
            peer.in_link.append(self)


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
        self.peers = dict()
        for i in range(N):
            self.peers[i] = Peer(i, k)

        print("create short link...")
        # ========== add short link =============
        # handle first node and last node
        peer = self.peers[0]
        peer.predecessor = self.peers[N - 1]
        peer.successor = self.peers[1]

        peer = self.peers[N - 1]
        peer.predecessor = self.peers[N - 2]
        peer.successor = self.peers[0]

        # handle intermediate nodes
        for i in range(1, N-1):
            peer = self.peers[i]
            peer.predecessor = self.peers[i - 1]
            peer.successor = self.peers[i + 1]

        print("create long link...")
        # ========== add long link =============
        for i in range(N):
            # print("peer " + str(i) + " finished")
            peer = self.peers[i]
            while len(peer.out_link) < k:
                x = math.ceil(math.exp(math.log(N) * (random.random() - 1)) * N) + i
                if x > (N - 1):
                    x = x - N
                if x == i:
                    continue
                peer.add_out_link(self.peers[x])

    def add_ids(self, node, identifier):
        """
        add identifier of social network nodes to the overlay
        """
        peer_id = math.ceil(identifier * self.N)
        if peer_id > (self.N - 1):
            peer_id = 0
        self.peers[peer_id].add_node(node)

    def get_peer(self, identifier):
        """
        get the peer for given identifier of social network node
        """
        peer_id = math.ceil(identifier * self.N)
        if peer_id > (self.N - 1):
            peer_id = 0
        return self.peers[peer_id]

    def distance(self, a, b):
        """
        Calculate the distance between peer a and peer b
        """
        if a <= b:
            return b - a
        else:
            return self.N + b - a

    def find_finger(self, peer, end_peer):
        """
        Find the next node that is closest to the destination
        """
        current = peer
        out_nodes = peer.out_link + [peer.successor]
        for n in out_nodes:
            if self.distance(n.v, end_peer.v) < self.distance(current.v, end_peer.v):
                current = n
        return current

    def get_hop_count(self, id1, id2):
        """
        Get the hop count for id1 to find id2 in clockwise direction
        """
        idx1 = math.ceil(id1 * self.N)
        idx2 = math.ceil(id2 * self.N)
        if idx1 == idx2:
            return 0
        if idx1 == self.N:
            idx1 = 0
        if idx2 == self.N:
            idx2 = 0

        start_peer = self.peers[idx1]
        end_peer = self.peers[idx2]
        next_node = self.find_finger(start_peer, end_peer)
        count = 1
        while next_node.v != end_peer.v:
            next_node = self.find_finger(next_node, end_peer)
            count += 1

        return count










