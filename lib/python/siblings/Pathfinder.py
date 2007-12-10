# Copyright 2007 Mikael Lind.

from a_star_search import a_star_search
from collections import deque
from geometry import grid_neighbors, diagonal_distance

A_STAR_SEARCH_LIMIT = 100

class Pathfinder:
    def __init__(self, path_grid):
        self._path_grid = path_grid
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

        def neighbors(pos):
            width, height = self._path_grid.size
            is_locked = self._path_grid.is_cell_locked
            for n in grid_neighbors(pos):
                x, y = n
                if (x >= 0 and x < width and y >= 0 and y < height
                    and not is_locked(n)):
                    yield n

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
