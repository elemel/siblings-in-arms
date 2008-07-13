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
from ProximityGrid import ProximityGrid
from TaskFacade import TaskFacade
from Unit import Unit
from geometry import rectangle_from_center_and_size, squared_distance
from balance import damage_factors
from shortest_path import shortest_path
from collections import defaultdict, deque
from geometry import diagonal_distance


SHORTEST_PATH_LIMIT = 100


class GameEngine:

    def __init__(self):
        self.task_facade = TaskFacade(self)
        self.grid = HexGrid()
        self.__path_queue = deque()
        self.units = {}
        self.proximity_grid = ProximityGrid(3)
        self.__cell_locks = {}
        self.__unit_locks = defaultdict(set)
        
    def update(self, dt):
        self.__update_paths()
        self.__update_tasks(dt)
        self.__remove_dead_units()

    def __update_paths(self):
        if self.__path_queue:
            unit, waypoint, callback = self.__path_queue.popleft()
            if unit.pos is not None:
                def goal(pos):
                    return pos == waypoint
                def neighbors(pos):
                    return (n for n in self.grid.neighbors(pos)
                            if not self.locked_cell(n))
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
        cell = self.__find_unlocked_cell(pos)
        unit.pos = cell
        self.units[unit.key] = unit
        self.__add_unit_locks(unit, cell)
        rect = rectangle_from_center_and_size(unit.pos, unit.size)
        self.proximity_grid[unit.key] = rect
        print "Added %s at %s." % (unit, unit.pos)

    def remove_unit(self, unit):
        del self.proximity_grid[unit.key]
        self.__remove_unit_locks(unit)
        del self.units[unit.key]
        unit.pos = None
        print "Removed %s." % unit

    def request_path(self, unit, waypoint, callback):
        self.__path_queue.append((unit, waypoint, callback))

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

    def __find_unlocked_cell(self, start):
        def goal(cell):
            return not self.locked_cell(cell)
        def debug(nodes):
            print ("Found an unlocked cell after searching %d node(s)."
                   % len(nodes))
        path = shortest_path(start, goal, self.grid.neighbors,
                             diagonal_distance)
        return path[-1] if path else start

    def __add_unit_locks(self, unit, cell):
        self.lock_cell(unit, cell)

    def __remove_unit_locks(self, unit):
        if unit in self.__unit_locks:
            for cell in list(self.__unit_locks[unit]):
                self.unlock_cell(cell)

    def lock_cell(self, unit, cell):
        if cell in self.__cell_locks:
            raise RuntimeError("cell %s is already locked" % (cell,))
        self.__cell_locks[cell] = unit
        self.__unit_locks[unit].add(cell)
        print "%s locked cell %s." % (unit, cell)

    def unlock_cell(self, cell):
        unit = self.__cell_locks.pop(cell)
        self.__unit_locks[unit].remove(cell)
        if not self.__unit_locks[unit]:
            del self.__unit_locks[unit]
        print "%s unlocked cell %s." % (unit, cell)

    def locked_cell(self, cell):
        return cell in self.__cell_locks
