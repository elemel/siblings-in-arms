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
from Unit import Building
from geometry import rectangle_from_center_and_size, squared_distance
from balance import damage_factors
from shortest_path import shortest_path
from collections import defaultdict, deque
from geometry import diagonal_distance


SHORTEST_PATH_LIMIT = 100


class GameEngine:

    def __init__(self):
        self.time_step = None
        self.time = 0.0
        self.__grid = HexGrid()
        self.__path_queue = deque()
        self.units = {}
        self.__proximity_grid = ProximityGrid(5)
        self.__cell_locks = {}
        self.__unit_locks = defaultdict(set)
        
    def update(self, time_step):
        self.time_step = time_step
        self.time += time_step
        self.__update_paths()
        self.__update_tasks()
        self.__remove_dead_units()

    def __update_paths(self):
        if self.__path_queue:
            unit, waypoint, callback = self.__path_queue.popleft()
            if unit.cell is not None:
                def goal(cell):
                    return cell == waypoint
                def neighbors(cell):
                    return (n for n in self.__grid.neighbors(cell)
                            if not self.locked_cell(n))
                def heuristic(cell):
                    return self.__grid.cell_distance(cell, waypoint)
                def debug(nodes):
                    print ("%s found a path after searching %d cell(s)."
                           % (unit, len(nodes)))
                path = shortest_path(unit.cell, goal, neighbors,
                                     diagonal_distance, heuristic,
                                     limit=SHORTEST_PATH_LIMIT, debug=debug)
                callback(path)

    def __update_tasks(self):
        for unit in self.units.values():
            if unit.task is not None:
                unit.task.update()
                if unit.task.done:
                    unit.task = None
            if unit.task is None and unit.task_queue:
                unit.task = unit.task_queue[0]
                unit.task_queue = unit.task_queue[1:]
                unit.task.unit = unit


    def add_unit(self, unit, pos):
        start = self.__grid.pos_to_cell(pos)
        unit.cell = self.__find_unlocked_cell(start)
        unit.pos = self.__grid.cell_to_pos(unit.cell)
        self.units[unit.key] = unit
        self.__add_unit_locks(unit)
        rect = rectangle_from_center_and_size(unit.pos, unit.size)
        self.__proximity_grid[unit.key] = rect
        print "Added %s at %s." % (unit, unit.cell)

    def remove_unit(self, unit):
        del self.__proximity_grid[unit.key]
        self.__remove_unit_locks(unit)
        del self.units[unit.key]
        unit.pos = None
        unit.cell = None
        print "Removed %s." % unit

    def request_path(self, unit, waypoint, callback):
        x, y = waypoint
        assert type(x) is int and type(y) is int
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
                   for key in self.__proximity_grid.intersect(rect)
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
        path = shortest_path(start, goal, self.__grid.neighbors,
                             diagonal_distance)
        return path[-1] if path else start

    def __add_unit_locks(self, unit):
        self.lock_cell(unit, unit.cell)
        if isinstance(unit, Building):
            for neighbor in self.__grid.neighbors(unit.cell):
                self.lock_cell(unit, neighbor)

    def __remove_unit_locks(self, unit):
        if unit in self.__unit_locks:
            for cell in list(self.__unit_locks[unit]):
                self.unlock_cell(cell)

    def lock_cell(self, unit, cell):
        x, y = cell
        assert type(x) is int and type(y) is int
        if cell in self.__cell_locks:
            raise RuntimeError("cell %s is already locked" % (cell,))
        self.__cell_locks[cell] = unit
        self.__unit_locks[unit].add(cell)
        print "%s locked cell %s." % (unit, cell)

    def unlock_cell(self, cell):
        x, y = cell
        assert type(x) is int and type(y) is int
        unit = self.__cell_locks.pop(cell)
        self.__unit_locks[unit].remove(cell)
        if not self.__unit_locks[unit]:
            del self.__unit_locks[unit]
        print "%s unlocked cell %s." % (unit, cell)

    def locked_cell(self, cell):
        x, y = cell
        assert type(x) is int and type(y) is int
        return cell in self.__cell_locks

    def move_unit(self, unit, pos):
        unit.pos = pos
        rect = rectangle_from_center_and_size(unit.pos, unit.size)
        self.__proximity_grid[unit.key] = rect

    def cell_to_pos(self, cell):
        return self.__grid.cell_to_pos(cell)

    def pos_to_cell(self, pos):
        return self.__grid.pos_to_cell(pos)
