# Copyright 2007 Mikael Lind.

from a_star_search import a_star_search, grid_neighbors, diagonal_distance

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
    for n in nodes.itervalues():
        x, y = n.p
        grid[x][y] = symbol

def paint_path(grid, path, symbol):
    while path is not None:
        x, y = path.p
        grid[x][y] = symbol
        path = path.parent

def create_blocked_grid():
    grid = create_grid(75, 20, " ")
    paint_block(grid, (6, 2), (16, 3), "#")
    paint_block(grid, (17, 2), (19, 15), "#")
    paint_block(grid, (35, 5), (38, 18), "#")
    paint_block(grid, (39, 17), (63, 18), "#")
    paint_block(grid, (39, 5), (53, 6), "#")
    return grid

def print_grid(g):
    height = len(g[0])
    for y in xrange(height - 1, -1, -1):
        print "".join(g[x][y] for x in xrange(len(g)))

def main():
    grid = create_blocked_grid()
    width, height = len(grid), len(grid[0])
    start, goal = (5, 9), (45, 12)

    def contains(p):
        x, y = p
        return x >= 0 and x < width and y >= 0 and y < height

    def passable(p):
        x, y = p
        return grid[x][y] != "#"

    def neighbors(p):
        return (n for n in grid_neighbors(p) if contains(n) and passable(n))

    def heuristic(p):
        return diagonal_distance(p, goal)

    path, nodes = a_star_search(start, goal, neighbors, diagonal_distance,
                                heuristic)

    print "Path:", path
    print "Path cost:", path.f()
    print "Examined nodes:", len(nodes)
    paint_nodes(grid, nodes, ".")
    paint_path(grid, path, "@")
    print_grid(grid)
    print "Legend: '@' = path, '#' = obstacle, '.' = examined node"

if __name__ == "__main__":
    main()
