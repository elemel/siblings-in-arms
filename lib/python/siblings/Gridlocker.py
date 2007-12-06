# Copyright 2007 Mikael Lind.

from geometry import grid_neighbors, diagonal_distance
from a_star_search import breadth_first_search

class Gridlocker:
    def __init__(self):
        self._size = (100, 100)
        self._locks = {}
        self._lockers = {}

    def _get_size(self):
        return self._size

    size = property(_get_size)
        
    def lock_cell(self, unit, pos):
        old_key = self._locks.get(pos, None)
        if old_key is None:
            self._locks[pos] = unit.key
            if not unit.key in self._lockers:
                self._lockers[unit.key] = set()
            self._lockers[unit.key].add(pos)
            print "Unit #%d locked cell %s." % (unit.key, pos)
            return True
        else:
            return unit.key == old_key

    def unlock_cell(self, unit, pos):
        if pos in self._locks:
            del self._locks[pos]
            self._lockers[unit.key].remove(pos)
            if not self._lockers[unit.key]:
                del self._lockers[unit.key]
            print "Unit #%d unlocked cell %s." % (unit.key, pos)

    def unlock_all_cells(self, unit):
        if unit.key in self._lockers:
            for pos in list(self._lockers[unit.key]):
                self.unlock_cell(unit, pos)

    def find_unlocked_cell(self, start):
        def predicate(pos):
            return pos not in self._locks
    
        def contains(pos):
            width, height = self._size
            x, y = pos
            return x >= 0 and x < width and y >= 0 and y < height
    
        def neighbors(pos):
            return (n for n in grid_neighbors(pos) if contains(n))
    
        path, nodes = breadth_first_search(start, predicate, neighbors,
                                           diagonal_distance)
        print "Found an unlocked cell after searching %d node(s)." % len(nodes)
        return path.p

    def get_locking_unit(self, pos):
        return self._locks.get(pos, 0)
