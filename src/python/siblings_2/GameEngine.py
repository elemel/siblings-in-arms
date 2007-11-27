# Copyright 2007 Mikael Lind.

import time, sys
from a_star_search import a_star_search, grid_neighbors, diagonal_distance
from collections import deque

A_STAR_SEARCH_LIMIT = 1000

class Grid:
    def __init__(self, size):
        self.size = size
        width, height = size
        self._slots = [[0] * height for x in xrange(width)]

    def get(self, pos):
        x, y = pos
        return self._slots[x][y]

    def set(self, pos, num):
        x, y = pos
        self._slots[x][y] = num

class GameEngine:
    def __init__(self):
        self.grid = Grid((100, 100))
        self.units = {}
        self.path_queue = deque()
        
    def update(self, dt):
        if self.path_queue:
            unit, waypoint = self.path_queue.popleft()
            path = self._find_path(unit, waypoint)
            unit.set_path(path)
        for t in self.units.itervalues():
            t.update(dt, self)

    def request_path(self, unit, waypoint):
        self.path_queue.append((unit, waypoint))

    def add_unit(self, unit, pos):
        self.units[unit.num] = unit
        unit.old_pos = unit.new_pos = pos
        if self.grid.get(unit.pos) == 0:
            self.grid.set(unit.pos, unit.num)

    def remove_unit(self, unit):
        del self.units[unit.num]
        self.grid.set(unit.pos, 0)

    def reserve_slot(self, unit, pos):
        if self.grid.get(pos) == 0:
            self.grid.set(pos, unit.num)
            print "Grid: Reserved slot %s for unit #%d." % (pos, unit.num)
            return True
        else:
            return False

    def release_slot(self, unit, pos):
        assert self.grid.get(pos) == unit.num
        self.grid.set(pos, 0)
        print "Grid: Unit #%d released slot %s." % (unit.num, pos)

    def _find_path(self, unit, waypoint):
        def neighbors(p):
            def contains(p):
                x, y = p
                width, height = self.grid.size
                return x >= 0 and x < width and y >= 0 and y < height

            def passable(p):
                x, y = p
                return self.grid.get((x, y)) in (0, unit.num)

            return (n for n in grid_neighbors(p) if contains(n) and passable(n))

        def heuristic(p):
            return diagonal_distance(p, waypoint)

        path, nodes = a_star_search(unit.pos, waypoint, neighbors,
                                    diagonal_distance, heuristic,
                                    A_STAR_SEARCH_LIMIT)
        print "A* search: Examined %d node(s)." % len(nodes)
        d = deque()
        d.extendleft(node.p for node in path if node.p != unit.pos)
        return d

MIN_TIME_STEP = 0.01
MAX_TIME_STEP = 0.1
