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

def a_star(start, goal, neighbors, cost, heuristic):
    best_h = heuristic(start)
    best = Node(start, best_h)
    nodes = {start: best}
    q = [best]
    while q:
        current = heappop(q)
        current.state = CLOSED
        for n in neighbors(current.p):
            neighbor_g = current.g + cost(current.p, n)
            neighbor = nodes.get(n, None)
            if neighbor is None:
                neighbor = Node(n, heuristic(n), neighbor_g, current)
                if neighbor.p == goal:
                    return neighbor, nodes
                nodes[n] = neighbor
                heappush(q, neighbor)
                if neighbor.h < best_h:
                    best_h = neighbor.h
                    best = neighbor
            elif neighbor_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = neighbor_g
                if neighbor.state == CLOSED:
                    # reopen neighbor node
                    neighbor.state = OPEN
                    heappush(q, neighbor)
                else:
                    # reestablish heap invariant
                    heapify(q)
    return best, nodes
