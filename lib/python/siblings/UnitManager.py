# Copyright 2007 Mikael Lind.

from Unit import Unit, UnitSpec

tavern_spec = UnitSpec("tavern")
tavern_spec.speed = 0.0
tavern_spec.size = (3, 3)

warrior_spec = UnitSpec("warrior")
warrior_spec.speed = 5.0

class UnitManager:
    def __init__(self, path_grid):
        self._path_grid = path_grid
        self._units = {}
        
    def add_unit(self, unit, pos):
        pos = self._path_grid.find_unlocked_cell(pos)
        print "Adding unit #%d at %s." % (unit.key, pos)
        self._units[unit.key] = unit
        unit.pos = pos
        x, y = unit.pos
        width, height = unit.size
        min_x = int(x - (width - 1) / 2)
        min_y = int(y - (height - 1) / 2)
        max_x = min_x + (width - 1)
        max_y = min_y + (height - 1)
        for x in xrange(min_x, max_x + 1):
            for y in xrange(min_y, max_y + 1):
                self._path_grid.lock_cell(unit.key, (x, y))

    def remove_unit(self, unit):
        self._path_grid.remove_cell_locker(unit.key)
        del self._units[unit.key]

    def get_build_time(self, name):
        return 3.0

    def create_unit(self, name, player):
        return Unit(warrior_spec, player)
