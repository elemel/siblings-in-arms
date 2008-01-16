# Copyright 2007 Mikael Lind.

from a_star_search import a_star_search
from collections import deque
from geometry import grid_neighbors, diagonal_distance

A_STAR_SEARCH_LIMIT = 100

class Pathfinder:
    def __init__(self, grid, gridlocker):
        self._grid = grid
        self._gridlocker = gridlocker
        self._path_requests = deque()
        
    def update(self):
        if self._path_requests:
            unit, waypoint, callback = self._path_requests.popleft()
            if unit.pos is not None:
                path = self._find_path(unit, waypoint)
                callback(path)

    def request_path(self, unit, waypoint, callback):
        self._path_requests.append((unit, waypoint, callback))

    def _find_path(self, unit, waypoint):
        def predicate(pos):
            return pos == waypoint

        def neighbors(cell_key):
            return (n for n in self._grid.neighbors(cell_key)
                    if not self._gridlocker.locked(n))

        def heuristic(pos):
            return diagonal_distance(pos, waypoint)

        path, nodes = a_star_search(unit.pos, predicate, neighbors,
                                    diagonal_distance, heuristic,
                                    A_STAR_SEARCH_LIMIT)
        print ("%s found a path after searching %d node(s)."
               % (unit, len(nodes)))
        d = deque()
        d.extendleft(node.pos for node in path if node.pos != unit.pos)
        return d
