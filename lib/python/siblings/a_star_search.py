# Copyright 2007 Mikael Lind.

import sys
from heapq import heappush, heappop, heapify
from geometry import diagonal_distance

OPEN = 1
CLOSED = 2

class Node(object):
    def __init__(self, pos, h, g = 0.0, parent = None, state = OPEN):
        self.pos = pos
        self.h = h
        self.g = g
        self.parent = parent
        self.state = OPEN

    def __cmp__(self, other):
        # Break ties using object ID.
        return (cmp(self.g + self.h, other.g + other.h)
                or cmp(id(self), id(other)))

    def __iter__(self):
        current = self
        while current is not None:
            yield current
            current = current.parent

    def __str__(self):
        return str([n.pos for n in self])

def a_star_search(start, predicate, neighbors, cost, heuristic,
                  limit = sys.maxint):
    start_node = Node(start, heuristic(start))
    nodes = {start: start_node}
    if predicate(start_node.pos):
        return start_node, nodes
    open_list = [start_node]

    # Track which node is closest to goal.
    closest = start_node 
    closest_h = start_node.h

    while open_list and len(nodes) < limit:
        # Continue search from node with lowest f.
        current = heappop(open_list)
        current.state = CLOSED

        # Process neighbors of current node.
        for n in neighbors(current.pos):
            neighbor_g = current.g + cost(current.pos, n)
            neighbor = nodes.get(n, None)
            if neighbor is None:
                neighbor = Node(n, heuristic(n), neighbor_g, current)
                nodes[n] = neighbor
                if predicate(neighbor.pos):
                    # Found path to goal.
                    return neighbor, nodes
                heappush(open_list, neighbor)
                if neighbor.h < closest_h:
                    # Neighbor is closest to goal so far.
                    closest = neighbor
                    closest_h = neighbor.h
            elif neighbor_g < neighbor.g:
                # Update neighbor with shorter path.
                neighbor.parent = current
                neighbor.g = neighbor_g  # May break heap invariant.
                if neighbor.state == CLOSED:
                    # Reopen neighbor.
                    neighbor.state = OPEN
                    heappush(open_list, neighbor)
                else:
                    # Reestablish heap invariant.
                    heapify(open_list)

    # No path to goal; return closest path.
    return closest, nodes

def breadth_first_search(start, predicate, neighbors, cost,
                         limit = sys.maxint):
    def heuristic(pos):
        return 0
    
    return a_star_search(start, predicate, neighbors, diagonal_distance,
                         heuristic, limit)
