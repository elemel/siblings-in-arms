# Copyright 2007 Mikael Lind.

import time, sys
from Pathfinder import Pathfinder
from HexGrid import HexGrid
from Grid import Grid
from TaskFacade import TaskFacade
from Taskmaster import Taskmaster
from Unit import Unit
from UnitManager import UnitManager
from Gridlocker import Gridlocker
from geometry import (rectangle_from_center_and_size, squared_distance,
                      diagonal_distance)
from tasks.AttackTask import AttackTask
from config import damage_factors
from shortest_path import shortest_path

class GameEngine:
    def __init__(self):
        self.task_facade = TaskFacade(self)
        self.taskmaster = Taskmaster(self.task_facade, self._idle_callback)
        self.grid = HexGrid((100, 100))
        self.gridlocker = Gridlocker()
        self.pathfinder = Pathfinder(self.grid, self.gridlocker)
        self.unit_manager = UnitManager()
        self.proximity_grid = Grid()
        self.dead_units = []
        
    def update(self, dt):
        self.pathfinder.update()
        self.taskmaster.update(dt)
        self._remove_dead_units()

    def add_unit(self, unit, pos):
        pos = self._find_unlocked_cell(pos)
        self.unit_manager.add_unit(unit)
        self._add_unit_to_grid(unit, pos)
        rect = rectangle_from_center_and_size(unit.pos, unit.size)
        self.proximity_grid[unit.key] = rect
        self.taskmaster.add_unit(unit)
        print "Added %s at %s." % (unit, unit.pos)

    def remove_unit(self, unit):
        self.taskmaster.remove_unit(unit)
        del self.proximity_grid[unit.key]
        self._remove_unit_from_grid(unit)
        self.unit_manager.remove_unit(unit)
        unit.pos = None
        print "Removed %s." % unit

    def get_damage_factor(self, attacker, defender):
        return damage_factors.get((attacker.spec.name,
                                   defender.spec.name), 1.0)

    def _remove_dead_units(self):
        for unit in self.unit_manager._units.itervalues():
            if unit.health <= 0:
                self.dead_units.append(unit)
        if self.dead_units:
            for unit in self.dead_units:
                self.remove_unit(unit)
            del self.dead_units[:]

    def _idle_callback(self, unit):
        if not unit.damage:
            return
        rect = rectangle_from_center_and_size(unit.pos, (10, 10))
        enemies = [self.unit_manager.find_unit(key)
                   for key in self.proximity_grid.intersect(rect)
                   if key != unit.key]
        enemies = [enemy for enemy in enemies if enemy.player != unit.player]
        if enemies:
            def key_func(a):
                return squared_distance(a.pos, unit.pos)
            enemy = min(enemies, key=key_func)
            print "%s found an enemy in %s." % (unit, enemy)
            self.taskmaster.append_task(unit, AttackTask(enemy))

    def _find_unlocked_cell(self, start):
        width, height = self.grid.size

        def goal(cell_key):
            return not self.gridlocker.locked(cell_key)

        def debug(nodes):
            print ("Found an unlocked cell after searching %d node(s)."
                   % len(nodes))
    
        path = shortest_path(start, goal, self.grid.neighbors,
                             diagonal_distance)
        return path[-1] if path else start

    def _add_unit_to_grid(self, unit, pos):
        pos = self._find_unlocked_cell(pos)
        unit.pos = pos
        x, y = unit.pos
        width, height = unit.size
        min_x = int(x - (width - 1) / 2)
        min_y = int(y - (height - 1) / 2)
        max_x = min_x + (width - 1)
        max_y = min_y + (height - 1)
        for x in xrange(min_x, max_x + 1):
            for y in xrange(min_y, max_y + 1):
                self.gridlocker.lock((x, y), unit)

    def _remove_unit_from_grid(self, unit):
        if unit.key in self.gridlocker._units:
            for cell_key in list(self.gridlocker._units[unit.key]):
                self.gridlocker.unlock(cell_key)
