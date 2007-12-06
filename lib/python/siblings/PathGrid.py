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
        
    def lock_cell(self, key, pos):
        old_key = self._locks.get(pos, None)
        if old_key is None:
            self._locks[pos] = key
            if not key in self._lockers:
                self._lockers[key] = set()
            self._lockers[key].add(pos)
            print "Unit #%d locked cell %s." % (key, pos)
            return True
        else:
            return key == old_key

    def unlock_cell(self, key, pos):
        if pos in self._locks:
            del self._locks[pos]
            self._lockers[key].remove(pos)
            if not self._lockers[key]:
                del self._lockers[key]
            print "Unit #%d unlocked cell %s." % (key, pos)

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
        return path.p

    def get_cell_locker(self, pos):
        return self._locks.get(pos, 0)

    def remove_cell_locker(self, key):
        if key in self._lockers:
            for pos in list(self._lockers[key]):
                self.unlock_cell(key, pos)
