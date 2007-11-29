# Copyright 2007 Mikael Lind.

import time, sys
from a_star_search import a_star_search, grid_neighbors, diagonal_distance
from collections import deque

A_STAR_SEARCH_LIMIT = 1000

class GameEngine:
    def __init__(self):
        self.size = (100, 100)
        self.reservations = {}
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
        if unit.pos not in self.reservations:
            self.reservations[unit.pos] = unit.key
            unit.cells.add(unit.pos)
            print "Reserved cell %s for unit #%d." % (pos, unit.key)

    def remove_unit(self, unit):
        del self.units[unit.key]
        while unit.cells:
            p = unit.cells.pop()
            del self.reservations[p]

    def reserve_cell(self, unit, pos):
        if pos in self.reservations:
            return False
        else:
            self.reservations[pos] = unit.key
            print "Reserved cell %s for unit #%d." % (pos, unit.key)
            return True

    def release_cell(self, unit, pos):
        assert self.reservations.get(pos) == unit.key
        del self.reservations[pos]
        print "Unit #%d released cell %s." % (unit.key, pos)

    def _find_path(self, unit, waypoint):
        def contains(p):
            x, y = p
            width, height = self.size
            return x >= 0 and x < width and y >= 0 and y < height

        def passable(p):
            return self.reservations.get(p, unit.key) == unit.key

        def neighbors(p):
            return (n for n in grid_neighbors(p)
                    if contains(n) and passable(n))

        def heuristic(p):
            return diagonal_distance(p, waypoint)

        path, nodes = a_star_search(unit.pos, waypoint, neighbors,
                                    diagonal_distance, heuristic,
                                    A_STAR_SEARCH_LIMIT)
        print "Found path after searching %d node(s)." % len(nodes)
        d = deque()
        d.extendleft(node.p for node in path if node.p != unit.pos)
        return d
