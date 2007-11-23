import math, sys
from heapq import heappush, heappop, heapify

SQRT_2 = math.sqrt(2)

class Node:
    def __init__(self, id_, p, h, g = 0.0, parent = None, closed = False):
        self.id_ = id_
        self.p = p
        self.h = h
        self.g = g
        self.parent = parent
        self.closed = closed

    def f(self):
        return self.g + self.h

    def __cmp__(self, other):
        # break ties with ID, preferring newly created nodes
        return cmp(self.f(), other.f()) or -cmp(self.id_, other.id_)

    def __str__(self):
        return "[%s]" % self._str()
    
    def _str(self):
        if self.parent is None:
            return str(self.p)
        else:
            return "%s, %s" % (self.p, self.parent._str())

    def __repr__(self):
        return "Node#%d" % self.id_

def grid_neighbors(p):
    x, y = p
    return [(x - 1, y + 1), (x + 0, y + 1), (x + 1, y + 1),
            (x - 1, y + 0),                 (x + 1, y + 0),
            (x - 1, y - 1), (x + 0, y - 1), (x + 1, y - 1)]

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def diagonal_distance(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return min(dx, dy) * SQRT_2 + abs(dx - dy)

def true_predicate(a):
    return True

def a_star(start, goal, neighbors = grid_neighbors, predicate = true_predicate,
           cost = diagonal_distance, heuristic = diagonal_distance):
    ids = iter(xrange(sys.maxint))
    nodes = {}
    best_h = heuristic(start, goal)
    best = Node(ids.next(), start, best_h)
    nodes[start] = best
    q = []
    heappush(q, best)
    while q:
        current = heappop(q)
        current.closed = True
        for n in filter(predicate, neighbors(current.p)):
            neighbor = nodes.get(n, None)
            neighbor_g = current.g + cost(current.p, n)
            if neighbor is None:
                neighbor = Node(ids.next(), n, heuristic(n, goal), neighbor_g,
                                current)
                if neighbor.p == goal:
                    return neighbor, nodes
                nodes[n] = neighbor
                heappush(q, neighbor)
            elif neighbor_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = neighbor_g
                if neighbor.closed:
                    neighbor.closed = False
                    heappush(q, neighbor)
                else:
                    heapify(q)
    return best, nodes

def create_grid(width, height, symbol):
    grid = []
    for x in range(width):
        grid.append([symbol] * height)
    return grid    

def paint_block(grid, min_, max_, symbol):
    for x in xrange(min_[0], max_[0] + 1):
        for y in xrange(min_[1], max_[1] + 1):
            grid[x][y] = symbol

def paint_nodes(grid, nodes, symbol):
    for id_, n in nodes.iteritems():
        x, y = n.p
        grid[x][y] = symbol

def paint_path(grid, path, symbol):
    while path is not None:
        x, y = path.p
        grid[x][y] = symbol
        path = path.parent

def print_grid(g):
    height = len(g[0])
    for y in xrange(height - 1, -1, -1):
        print "".join(g[x][y] for x in xrange(len(g)))

def test():
    width, height = 75, 20
    grid = create_grid(width, height, " ")
    paint_block(grid, (17, 2), (19, 15), "#")
    paint_block(grid, (35, 5), (38, 18), "#")

    def predicate(p):
        x, y = p
        return (x >= 0 and x < width and y >= 0 and y < height
                and grid[x][y] != "#")

    path, nodes = a_star((4, 13), (44, 7), predicate = predicate)
    print "Examined nodes: %d" % len(nodes)
    print "Path cost: %f" % path.f()
    paint_nodes(grid, nodes, ".")
    paint_path(grid, path, "@")
    print_grid(grid)

if __name__ == "__main__":
    test()
