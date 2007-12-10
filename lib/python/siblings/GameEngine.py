# Copyright 2007 Mikael Lind.

import time, sys
from Pathfinder import Pathfinder
from PathGrid import PathGrid
from TaskFacade import TaskFacade
from Taskmaster import Taskmaster
from Unit import Unit, UnitSpec
from UnitManager import UnitManager

class GameEngine:
    def __init__(self):
        self.task_facade = TaskFacade(self)
        self.taskmaster = Taskmaster(self.task_facade)
        self.path_grid = PathGrid()
        self.pathfinder = Pathfinder(self.path_grid)
        self.unit_manager = UnitManager()
        self.dead_units = []
        
    def update(self, dt):
        self.pathfinder.update()
        self.taskmaster.update(dt)
        self._remove_dead_units()

    def add_unit(self, unit, pos):
        self.unit_manager.add_unit(unit)
        self.path_grid.add_unit(unit, pos)
        print "Added %s at %s." % (unit, unit.pos)

    def remove_unit(self, unit):
        self.taskmaster.remove_actor(unit)
        self.path_grid.remove_unit(unit)
        self.unit_manager.remove_unit(unit)
        print "Removed %s." % unit

    def _remove_dead_units(self):
        for unit in self.unit_manager._units.itervalues():
            if unit.health <= 0:
                self.dead_units.append(unit)
        if self.dead_units:
            for unit in self.dead_units:
                self.remove_unit(unit)
            del self.dead_units[:]
