# Copyright 2007 Mikael Lind.

from collections import deque
from geometry import grid_neighbors, diagonal_distance
from shortest_path import shortest_path

SHORTEST_PATH_LIMIT = 100

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
        def goal(pos):
            return pos == waypoint

        def neighbors(pos):
            return (n for n in self._grid.neighbors(pos)
                    if not self._gridlocker.locked(n))

        def heuristic(pos):
            return diagonal_distance(pos, waypoint)

        def debug(nodes):
            print ("%s found a path after searching %d node(s)."
                   % (unit, len(nodes)))
            
        return shortest_path(unit.pos, goal, neighbors, diagonal_distance,
                             heuristic, limit=SHORTEST_PATH_LIMIT, debug=debug)
