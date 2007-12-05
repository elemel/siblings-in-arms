# Copyright 2007 Mikael Lind.

import time, sys
from Unit import Unit, UnitSpec
from TaskFacade import TaskFacade
from Pathfinder import Pathfinder
from Gridlocker import Gridlocker
from Taskmaster import Taskmaster

tavern_spec = UnitSpec("tavern")
tavern_spec.speed = 0.0
tavern_spec.size = (3, 3)

warrior_spec = UnitSpec("warrior")
warrior_spec.speed = 5.0

class GameEngine:
    def __init__(self):
        self.units = {}
        self.task_facade = TaskFacade(self)
        self.taskmaster = Taskmaster(self.task_facade)
        self.gridlocker = Gridlocker()
        self.pathfinder = Pathfinder(self.gridlocker)
        
    def update(self, dt):
        self.pathfinder.update()
        self.taskmaster.update(dt)

    def add_unit(self, unit, pos):
        pos = self.gridlocker.find_unlocked_cell(pos)
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
                self.gridlocker.lock_cell(unit, (x, y))

    def remove_unit(self, unit):
        while unit.locked_cells:
            p = unit.locked_cells.pop()
            del self.locked_cells[p]
        del self.units[unit.key]

    def get_build_time(self, name):
        return 3.0

    def create_unit(self, name, pos):
        unit = Unit(warrior_spec)
        self.add_unit(unit, pos)
