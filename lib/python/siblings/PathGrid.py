# Copyright 2007 Mikael Lind.

from geometry import grid_neighbors, diagonal_distance
from a_star_search import breadth_first_search

class PathGrid:
    def __init__(self):
        self._size = (100, 100)
        self._locks = {}
        self._lockers = {}

    def _get_size(self):
        return self._size

    size = property(_get_size)
        
    def lock_cell(self, unit, pos):
        if pos in self._locks:
            raise RuntimeError("cell %s is already locked" % pos)
        self._locks[pos] = unit.key
        if unit.key not in self._lockers:
            self._lockers[unit.key] = set()
        self._lockers[unit.key].add(pos)
        print "%s locked cell %s." % (unit, pos)

    def unlock_cell(self, unit, pos):
        del self._locks[pos]
        self._lockers[unit.key].remove(pos)
        if not self._lockers[unit.key]:
            del self._lockers[unit.key]
        print "%s unlocked cell %s." % (unit, pos)

    def find_unlocked_cell(self, start):
        width, height = self.size

        def predicate(pos):
            return pos not in self._locks
    
        def contains(pos):
            x, y = pos
            return x >= 0 and x < width and y >= 0 and y < height
    
        def neighbors(pos):
            return (n for n in grid_neighbors(pos) if contains(n))
    
        path, nodes = breadth_first_search(start, predicate, neighbors,
                                           diagonal_distance)
        print "Found an unlocked cell after searching %d node(s)." % len(nodes)
        return path.pos

    def is_cell_locked(self, pos):
        return pos in self._locks

    def add_unit(self, unit, pos):
        pos = self.find_unlocked_cell(pos)
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
        if unit.key in self._lockers:
            for pos in list(self._lockers[unit.key]):
                self.unlock_cell(unit, pos)
