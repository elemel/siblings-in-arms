# Copyright 2007 Mikael Lind.

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
