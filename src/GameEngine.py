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
from geometry import rectangle_from_center_and_size, squared_distance
from balance import damage_factors
from shortest_path import shortest_path
from collections import defaultdict, deque
from geometry import diagonal_distance


SHORTEST_PATH_LIMIT = 100


class GameEngine(object):

    def __init__(self):
        self.time_step = None
        self.time = 0.0
        self.__grid = HexGrid()
        self.__path_queue = deque()
        self.units = {}
        self.__proximity_grid = ProximityGrid(5)
        self.__cell_locks = {}
        
    def update(self, time_step):
        self.time_step = time_step
        self.time += time_step
        self.__update_paths()
        self.__update_tasks()
        self.__remove_dead_units()

    def __update_paths(self):
        while self.__path_queue and self.__path_queue[0][-1]:
            self.__path_queue.popleft()
        if self.__path_queue:
            unit, dest, set_path, aborting = self.__path_queue.popleft()
            if unit.cell is not None:
                def goal(cell):
                    return cell == dest
                def neighbors(cell):
                    return (n for n in self.__grid.neighbors(cell)
                            if self.lockable_cell(unit, n, with_moving=True))
                def heuristic(cell):
                    return self.__grid.cell_distance(cell, dest)
                def debug(nodes):
                    print ("%s found a path after searching %d cell(s)."
                           % (unit, len(nodes)))
                path = shortest_path(unit.cell, goal, neighbors,
                                     diagonal_distance, heuristic,
                                     limit=SHORTEST_PATH_LIMIT, debug=debug)
                set_path(path)

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
        unit.cell = self.__find_lockable_cell(unit, start)
        unit.pos = self.__grid.cell_to_pos(unit.cell)
        self.units[unit.key] = unit
        self.update_cell_locks(unit)
        rect = rectangle_from_center_and_size(unit.pos, unit.size)
        self.__proximity_grid[unit.key] = rect
        print "Added %s at %s." % (unit, unit.cell)

    def remove_unit(self, unit):
        del self.__proximity_grid[unit.key]
        del self.units[unit.key]
        unit.pos = None
        unit.cell = None
        self.update_cell_locks(unit)
        print "Removed %s." % unit

    def request_path(self, unit, dest, set_path):
        x, y = dest
        assert type(x) is int and type(y) is int
        path_request = [unit, dest, set_path, False]
        self.__path_queue.append(path_request)
        return path_request

    def abort_path(self, path_request):
        path_request[-1] = True

    def damage_factor(self, attacker, defender):
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
        enemies = [enemy for enemy in enemies if enemy.color != unit.color]
        if enemies:
            def key_func(a):
                return squared_distance(a.pos, unit.pos)
            enemy = min(enemies, key=key_func)
            print "%s found an enemy in %s." % (unit, enemy)

    def __find_lockable_cell(self, unit, start):
        def goal(cell):
            return self.lockable_cell(unit, cell)
        def debug(nodes):
            print ("Found an unlocked cell after searching %d node(s)."
                   % len(nodes))
        path = shortest_path(start, goal, self.__grid.neighbors,
                             diagonal_distance)
        return path[-1] if path else start

    def update_cell_locks(self, unit):
        if unit.cell_locks:
            for cell in unit.cell_locks:
                del self.__cell_locks[cell]
            unit.cell_locks.clear()
        if unit.cell is not None:
            unit.cell_locks.add(unit.cell)
            if unit.large:
                unit.cell_locks.update(self.__grid.neighbors(unit.cell))
            for cell in unit.cell_locks:
                self.__cell_locks[cell] = unit
            
    def lockable_cell(self, unit, cell, with_moving=False):
        def lockable(cell):
            return (self.__cell_locks.get(cell) in (unit, None)
                    or with_moving and self.__cell_locks[cell].moving)
        return (lockable(cell)
                and (not unit.large
                     or all(lockable(n) for n in self.__grid.neighbors(cell))))

    def move_unit(self, unit, pos):
        unit.pos = pos
        rect = rectangle_from_center_and_size(unit.pos, unit.size)
        self.__proximity_grid[unit.key] = rect

    def cell_to_pos(self, cell):
        return self.__grid.cell_to_pos(cell)

    def pos_to_cell(self, pos):
        return self.__grid.pos_to_cell(pos)
