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
        self.unit_manager = UnitManager(self.path_grid)
        self._dead = []
        
    def update(self, dt):
        self.pathfinder.update()
        self.taskmaster.update(dt)
        for unit in self.unit_manager._units.itervalues():
            if unit.health <= 0:
                self._dead.append(unit)
        if self._dead:
            for unit in self._dead:
                self.taskmaster.remove_unit(unit)
                self.unit_manager.remove_unit(unit)
                print "Unit #%d died." % unit.key
            del self._dead[:]
