import math
from heapq import heappush, heappop, heapify

SQRT_2 = math.sqrt(2)
OPEN = 1
CLOSED = 2

class Node(object):
    def __init__(self, p, h, g = 0.0, parent = None, state = OPEN):
        self.p = p
        self.h = h
        self.g = g
        self.parent = parent
        self.state = OPEN

    def f(self):
        return self.g + self.h

    def __cmp__(self, other):
        # break ties with object ID
        return cmp(self.f(), other.f()) or cmp(id(self), id(other))

    def __iter__(self):
        node = self
        while node is not None:
            yield node
            node = node.parent

    def __str__(self):
        return str([n.p for n in self])

def grid_neighbors(p):
    x, y = p
    yield x - 1, y + 1; yield x + 0, y + 1; yield x + 1, y + 1
    yield x - 1, y + 0;                     yield x + 1, y + 0
    yield x - 1, y - 1; yield x + 0, y - 1; yield x + 1, y - 1

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def diagonal_distance(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return min(dx, dy) * SQRT_2 + abs(dx - dy)

def a_star_search(start, goal, neighbors, cost, heuristic):
    # initialization
    start_node = Node(start, heuristic(start)) # create start node
    nodes = {start: start_node} # register start node
    open_list = [start_node] # add start node to open list

    # track which node is closest to goal
    closest = start_node 
    closest_h = start_node.h

    while open_list:
        # continue search from node with lowest f
        current = heappop(open_list)
        current.state = CLOSED

        # process neighbors of current node
        for n in neighbors(current.p):
            neighbor_g = current.g + cost(current.p, n) # total cost of path
            neighbor = nodes.get(n, None) # find neighbor if registered
            if neighbor is None:
                # create node for neighbor
                neighbor = Node(n, heuristic(n), neighbor_g, current)
                if neighbor.p == goal:
                    # found path to goal
                    return neighbor, nodes
                nodes[n] = neighbor # register neighbor
                heappush(open_list, neighbor) # add neighbor to open list
                if neighbor.h < closest_h:
                    # neighbor is closest to goal so far
                    closest = neighbor
                    closest_h = neighbor.h
            elif neighbor_g < neighbor.g:
                # update neighbor with shorter path
                neighbor.parent = current
                neighbor.g = neighbor_g # may break heap invariant
                if neighbor.state == CLOSED:
                    # reopen neighbor
                    neighbor.state = OPEN
                    heappush(open_list, neighbor) # add neighbor to open list
                else:
                    heapify(open_list) # reestablish heap invariant
    return closest, nodes # return closest path
