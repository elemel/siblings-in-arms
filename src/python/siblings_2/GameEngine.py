# Copyright 2007 Mikael Lind.

import time, sys
from a_star_search import a_star_search, grid_neighbors, diagonal_distance
from collections import deque

A_STAR_SEARCH_LIMIT = 1000

class GameEngine:
    def __init__(self):
        self.size = (100, 100)
        self.locked_cells = {}
        self.units = {}
        self.path_queue = deque()
        
    def update(self, dt):
        if self.path_queue:
            unit, waypoint, callback = self.path_queue.popleft()
            path = self._find_path(unit, waypoint)
            callback(path)
        for t in self.units.itervalues():
            t.update(dt, self)

    def find_path(self, unit, waypoint, callback):
        self.path_queue.append((unit, waypoint, callback))

    def add_unit(self, unit, pos):
        self.units[unit.key] = unit
        unit.pos = pos
        self.lock_cell(unit, unit.pos)

    def remove_unit(self, unit):
        while unit.locked_cells:
            p = unit.locked_cells.pop()
            del self.locked_cells[p]
        del self.units[unit.key]

    def lock_cell(self, unit, pos):
        old_key = self.locked_cells.get(pos, None)
        if old_key is None:
            self.locked_cells[pos] = unit.key
            unit.locked_cells.add(pos)
            print "Unit #%d locked cell %s." % (unit.key, pos)
            return True
        else:
            return key == old_key

    def unlock_cell(self, unit, pos):
        del self.locked_cells[pos]
        unit.locked_cells.remove(pos)
        print "Unit #%d unlocked cell %s." % (unit.key, pos)

    def _find_path(self, unit, waypoint):
        def contains(p):
            x, y = p
            width, height = self.size
            return x >= 0 and x < width and y >= 0 and y < height

        def lockable(p):
            return self.locked_cells.get(p, unit.key) == unit.key

        def neighbors(p):
            return (n for n in grid_neighbors(p)
                    if contains(n) and lockable(n))

        def heuristic(p):
            return diagonal_distance(p, waypoint)

        path, nodes = a_star_search(unit.pos, waypoint, neighbors,
                                    diagonal_distance, heuristic,
                                    A_STAR_SEARCH_LIMIT)
        print "Found path after searching %d node(s)." % len(nodes)
        d = deque()
        d.extendleft(node.p for node in path if node.p != unit.pos)
        return d
