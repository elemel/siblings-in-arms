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


from balance import damage_factors
from collections import defaultdict, deque
from geometry import rectangle_from_center_and_size, squared_distance
from HexGrid import HexGrid
from ProximityGrid import ProximityGrid
from shortest_path import shortest_path
import random


SHORTEST_PATH_LIMIT = 100


class GameEngine(object):

    def __init__(self):
        self.time_step = None
        self.time = 0.0
        self.__grid = HexGrid()
        self.__path_queue = deque()
        self.units = set()
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
                def cost(from_cell, to_cell):
                    return self.__grid.neighbor_distance(from_cell, to_cell)
                def heuristic(cell):
                    return self.__grid.cell_distance(cell, dest)
                path = shortest_path(unit.cell, goal, neighbors, cost,
                                     heuristic, limit=SHORTEST_PATH_LIMIT)
                set_path(path)

    def __update_tasks(self):
        for unit in list(self.units):
            if unit.task_stack:
                unit.task_stack[-1].update()
                if unit.task_stack[-1].done:
                    unit.task_stack.pop()
            if not unit.task_stack and unit.task_queue:
                unit.task_stack.append(unit.task_queue.popleft())

    def add_unit(self, unit, pos):
        start = self.__grid.pos_to_cell(pos)
        unit.cell = self.__find_lockable_cell(unit, start)
        unit.pos = self.__grid.cell_to_pos(unit.cell)
        self.units.add(unit)
        self.update_cell_locks(unit)
        rect = rectangle_from_center_and_size(unit.pos, unit.size)
        self.__proximity_grid[unit] = rect

    def stop_unit(self, unit):
        for task in unit.task_stack:
            task.aborting = True
        unit.task_queue.clear()

    def remove_unit(self, unit):
        del self.__proximity_grid[unit]
        self.units.remove(unit)
        unit.pos = None
        unit.cell = None
        self.update_cell_locks(unit)

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
        dead_units = [u for u in self.units if u.health <= 0.0]
        for unit in dead_units:
            self.remove_unit(unit)

    def _idle_callback(self, unit):
        if not unit.damage:
            return
        rect = rectangle_from_center_and_size(unit.pos, (10, 10))
        enemies = [enemy for enemy in self.__proximity_grid.intersect(rect)
                   if enemy.color != unit.color]
        if enemies:
            def key_func(a):
                return squared_distance(a.pos, unit.pos)
            enemy = min(enemies, key=key_func)

    def __find_lockable_cell(self, unit, start):
        def goal(cell):
            return self.lockable_cell(unit, cell)
        def neighbors(cell):
            cells = list(self.__grid.neighbors(cell))
            random.shuffle(cells)
            return cells
        def cost(from_cell, to_cell):
            return self.__grid.neighbor_distance(from_cell, to_cell)
        path = shortest_path(start, goal, neighbors, cost)
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
        self.__proximity_grid[unit] = rect

    def cell_to_pos(self, cell):
        return self.__grid.cell_to_pos(cell)

    def pos_to_cell(self, pos):
        return self.__grid.pos_to_cell(pos)
