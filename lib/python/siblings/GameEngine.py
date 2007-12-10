# Copyright 2007 Mikael Lind.

import time, sys
from Pathfinder import Pathfinder
from PathGrid import PathGrid
from TaskFacade import TaskFacade
from Taskmaster import Taskmaster
from Unit import Unit, UnitSpec
from UnitManager import UnitManager
from Grid import Grid
from geometry import rectangle_from_center_and_size
from tasks.AttackTask import AttackTask

class GameEngine:
    def __init__(self):
        self.task_facade = TaskFacade(self)
        self.taskmaster = Taskmaster(self.task_facade, self._on_idle)
        self.path_grid = PathGrid()
        self.pathfinder = Pathfinder(self.path_grid)
        self.unit_manager = UnitManager()
        self.dead_units = []
        self.grid = Grid(5.0)
        
    def update(self, dt):
        self.pathfinder.update()
        self.taskmaster.update(dt)
        self._remove_dead_units()

    def add_unit(self, unit, pos):
        self.unit_manager.add_unit(unit)
        self.path_grid.add_unit(unit, pos)
        rect = rectangle_from_center_and_size(unit.pos, unit.size)
        self.grid[unit.key] = rect
        self.taskmaster.add_unit(unit)
        print "Added %s at %s." % (unit, unit.pos)

    def remove_unit(self, unit):
        self.taskmaster.remove_unit(unit)
        del self.grid[unit.key]
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

    def _on_idle(self, unit):
        rect = rectangle_from_center_and_size(unit.pos, (10, 10))
        for key in self.grid.intersect(rect):
            other_unit = self.unit_manager.find_unit(key)
            if unit.player != other_unit.player:
                print "%s found an enemy in %s." % (unit, other_unit)
                self.taskmaster.append_task(unit, AttackTask(other_unit))
                break
