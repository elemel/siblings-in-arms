# Copyright 2007 Mikael Lind.

from geometry import grid_neighbors, diagonal_distance
from a_star_search import breadth_first_search

class Gridlocker:
    def __init__(self):
        self.size = (100, 100)
        self.locked_cells = {}
        
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

    def find_unlocked_cell(self, start):
        def predicate(pos):
            return pos not in self.locked_cells
    
        def contains(pos):
            width, height = self.size
            x, y = pos
            return x >= 0 and x < width and y >= 0 and y < height
    
        def neighbors(pos):
            return (n for n in grid_neighbors(pos) if contains(n))
    
        path, nodes = breadth_first_search(start, predicate, neighbors,
                                           diagonal_distance)
        print "Found an unlocked cell after searching %d node(s)." % len(nodes)
        return path.p
