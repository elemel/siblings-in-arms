# Copyright 2007 Mikael Lind.

import time, sys
from a_star_search import a_star_search
from collections import deque
from geometry import grid_neighbors, diagonal_distance

A_STAR_SEARCH_LIMIT = 100

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
            t.update(self, dt)

    def find_path(self, unit, waypoint, callback):
        self.path_queue.append((unit, waypoint, callback))

    def add_unit(self, unit, pos):
        print "Adding unit #%d at %s." % (unit.key, pos)
        self.units[unit.key] = unit
        unit.pos = pos
        x, y = unit.pos
        width, height = unit.size
        min_x = int(x - (width - 1) / 2)
        min_y = int(y - (height - 1) / 2)
        max_x = min_x + (width - 1)
        max_y = min_y + (height - 1)
        for x in xrange(min_x, max_x + 1):
            for y in xrange(min_y, max_y + 1):
                self.lock_cell(unit, (x, y))

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
            return unit.key == old_key

    def unlock_cell(self, unit, pos):
        if pos in unit.locked_cells:
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
        print ("Unit #%d found a path after searching %d node(s)."
               % (unit.key, len(nodes)))
        d = deque()
        d.extendleft(node.p for node in path if node.p != unit.pos)
        return d
