# Copyright 2007 Mikael Lind.

from a_star_search import a_star_search
from collections import deque
from geometry import grid_neighbors, diagonal_distance

A_STAR_SEARCH_LIMIT = 100

class Pathfinder:
    def __init__(self, gridlocker):
        self._gridlocker = gridlocker
        self._path_queue = deque()
        
    def update(self):
        if self._path_queue:
            unit, waypoint, callback = self._path_queue.popleft()
            path = self._find_path(unit, waypoint)
            callback(path)

    def find_path(self, unit, waypoint, callback):
        self._path_queue.append((unit, waypoint, callback))

    def _find_path(self, unit, waypoint):
        width, height = self._gridlocker.size

        def predicate(p):
            return p == waypoint

        def contains(p):
            x, y = p
            return x >= 0 and x < width and y >= 0 and y < height

        def lockable(p):
            return self._gridlocker.get_locking_unit(p) in (0, unit.key)

        def neighbors(p):
            return (n for n in grid_neighbors(p)
                    if contains(n) and lockable(n))

        def heuristic(p):
            return diagonal_distance(p, waypoint)

        path, nodes = a_star_search(unit.pos, predicate, neighbors,
                                    diagonal_distance, heuristic,
                                    A_STAR_SEARCH_LIMIT)
        print ("Unit #%d found a path after searching %d node(s)."
               % (unit.key, len(nodes)))
        d = deque()
        d.extendleft(node.p for node in path if node.p != unit.pos)
        return d
