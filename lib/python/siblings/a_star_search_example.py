# Copyright 2007 Mikael Lind.

from a_star_search import a_star_search
from geometry import grid_neighbors, diagonal_distance

def paint_block(grid, min_, max_, symbol):
    for x in xrange(min_[0], max_[0] + 1):
        for y in xrange(min_[1], max_[1] + 1):
            grid[x, y] = symbol

def paint_nodes(grid, nodes, symbol):
    for n in nodes.itervalues():
        grid[n.p] = symbol

def paint_path(grid, path, symbol):
    while path is not None:
        grid[path.p] = symbol
        path = path.parent

def create_blocked_grid():
    grid = {}
    paint_block(grid, (6, 2), (16, 3), "#")
    paint_block(grid, (17, 2), (19, 15), "#")
    paint_block(grid, (35, 5), (38, 18), "#")
    paint_block(grid, (39, 17), (63, 18), "#")
    paint_block(grid, (39, 5), (53, 6), "#")
    return grid

def print_grid(g, width, height):
    for y in xrange(height - 1, -1, -1):
        print "".join(g.get((x, y), " ") for x in xrange(width))

def main():
    grid = create_blocked_grid()
    width, height = 75, 20
    start, goal = (5, 9), (45, 12)

    def predicate(p):
        return p == goal

    def contains(p):
        x, y = p
        return x >= 0 and x < width and y >= 0 and y < height

    def passable(p):
        return grid.get(p) != "#"

    def neighbors(p):
        return (n for n in grid_neighbors(p) if contains(n) and passable(n))

    def heuristic(p):
        return diagonal_distance(p, goal)

    path, nodes = a_star_search(start, predicate, neighbors, diagonal_distance,
                                heuristic)

    print "Path:", path
    print "Path cost:", path.g + path.h
    print "Examined nodes:", len(nodes)
    paint_nodes(grid, nodes, ".")
    paint_path(grid, path, "@")
    print_grid(grid, 75, 20)
    print "Legend: '@' = path, '#' = obstacle, '.' = examined node"

if __name__ == "__main__":
    main()
