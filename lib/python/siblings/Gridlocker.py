# Copyright 2007 Mikael Lind.

from geometry import grid_neighbors, diagonal_distance
from a_star_search import breadth_first_search

class Gridlocker:
    def __init__(self):
        self._size = (100, 100)
        self._locked_cells = {}
        self._locking_units = {}

    def _get_size(self):
        return self._size

    size = property(_get_size)
        
    def lock_cell(self, unit, pos):
        old_key = self._locked_cells.get(pos, None)
        if old_key is None:
            self._locked_cells[pos] = unit.key
            if not unit.key in self._locking_units:
                self._locking_units[unit.key] = set()
            self._locking_units[unit.key].add(pos)
            print "Unit #%d locked cell %s." % (unit.key, pos)
            return True
        else:
            return unit.key == old_key

    def unlock_cell(self, unit, pos):
        if pos in self._locked_cells:
            del self._locked_cells[pos]
            self._locking_units[unit.key].remove(pos)
            if not self._locking_units[unit.key]:
                del self._locking_units[unit.key]
            print "Unit #%d unlocked cell %s." % (unit.key, pos)

    def unlock_all_cells(self, unit):
        if unit.key in self._locking_units:
            for pos in list(self._locking_units[unit.key]):
                self.unlock_cell(unit, pos)

    def find_unlocked_cell(self, start):
        def predicate(pos):
            return pos not in self._locked_cells
    
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
        return self._locked_cells.get(pos, 0)
