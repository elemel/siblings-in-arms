# Copyright (c) 2007 Mikael Lind
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import time, sys
from HexGrid import HexGrid
from Grid import Grid
from TaskFacade import TaskFacade
from Unit import Unit
from Gridlocker import Gridlocker
from geometry import (rectangle_from_center_and_size, squared_distance,
                      diagonal_distance)
from balance import damage_factors
from shortest_path import shortest_path

from collections import deque
from geometry import diagonal_distance


SHORTEST_PATH_LIMIT = 100


class GameEngine:

    def __init__(self):
        self.task_facade = TaskFacade(self)
        self.grid = HexGrid((100, 100))
        self.gridlocker = Gridlocker()
        self.path_queue = deque()
        self.units = {}
        self.proximity_grid = Grid()
        
    def update(self, dt):
        self.__update_paths()
        self.__update_tasks(dt)
        self.__remove_dead_units()

    def __update_paths(self):
        if self.path_queue:
            unit, waypoint, callback = self.path_queue.popleft()
            if unit.pos is not None:
                def goal(pos):
                    return pos == waypoint
                def neighbors(pos):
                    return (n for n in self.grid.neighbors(pos)
                            if not self.gridlocker.locked(n))
                def heuristic(pos):
                    return diagonal_distance(pos, waypoint)
                def debug(nodes):
                    print ("%s found a path after searching %d node(s)."
                           % (unit, len(nodes)))
                path = shortest_path(unit.pos, goal, neighbors,
                                     diagonal_distance, heuristic,
                                     limit=SHORTEST_PATH_LIMIT, debug=debug)
                callback(path)

    def __update_tasks(self, dt):
        for unit in self.units.values():
            if unit.task is not None:
                self.task_facade.actor = unit
                self.task_facade.dt = dt
                unit.task.update(self.task_facade)
                if unit.task.done:
                    unit.task = None
            if unit.task is None and unit.task_queue:
                unit.task = unit.task_queue[0]
                unit.task_queue = unit.task_queue[1:]

    def add_unit(self, unit, pos):
        pos = self._find_unlocked_cell(pos)
        self.units[unit.key] = unit
        self._add_unit_to_grid(unit, pos)
        rect = rectangle_from_center_and_size(unit.pos, unit.size)
        self.proximity_grid[unit.key] = rect
        print "Added %s at %s." % (unit, unit.pos)

    def remove_unit(self, unit):
        del self.proximity_grid[unit.key]
        self._remove_unit_from_grid(unit)
        del self.units[unit.key]
        unit.pos = None
        print "Removed %s." % unit

    def request_path(self, unit, waypoint, callback):
        self.path_queue.append((unit, waypoint, callback))

    def get_damage_factor(self, attacker, defender):
        return damage_factors.get((type(attacker), type(defender)), 1.0)

    def __remove_dead_units(self):
        dead_units = [u for u in self.units.itervalues() if u.health <= 0.0]
        for unit in dead_units:
            self.remove_unit(unit)

    def _idle_callback(self, unit):
        if not unit.damage:
            return
        rect = rectangle_from_center_and_size(unit.pos, (10, 10))
        enemies = [self.units.get(key)
                   for key in self.proximity_grid.intersect(rect)
                   if key != unit.key]
        enemies = [enemy for enemy in enemies if enemy.player != unit.player]
        if enemies:
            def key_func(a):
                return squared_distance(a.pos, unit.pos)
            enemy = min(enemies, key=key_func)
            print "%s found an enemy in %s." % (unit, enemy)

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
