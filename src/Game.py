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
from config.units import *
from collections import defaultdict, deque
from Force import Force
from geometry import rect_from_center_and_size, squared_dist
from heapq import heappop, heappush
from HexGrid import HexGrid
from ProximityGrid import ProximityGrid
from shortest_path import shortest_path
from TechTree import TechTree
import random


SHORTEST_PATH_LIMIT = 100


def create_tech_tree():

    tech_tree = TechTree()

    # Building dependencies.
    for cls, deps in [(Tavern, []),
                      (Monastery, [Tavern]),
                      (Farm, [Monastery]),
                      (ArcheryRange, [Tavern]),
                      (Tower, [ArcheryRange]),
                      (Barracks, [Tavern]),
                      (Temple, [Tavern]),
                      (Inn, [Barracks, Temple]),
                      (GamblingDen, [Inn]),
                      (Laboratory, [Inn]),
                      (Stables, [Inn]),
                      (Hall, [Laboratory, Stables])]:
        tech_tree.depends(cls, deps)

    # Unit dependencies.
    for cls, deps in [(Monk, []),
                      (Ranger, [ArcheryRange]),
                      (Warrior, [Barracks]),
                      (Priest, [Temple]),
                      (Thief, [GamblingDen]),
                      (Knight, [Stables]),
                      (Wizard, [Laboratory])]:
        tech_tree.depends(cls, deps)

    return tech_tree


class Game(object):

    def __init__(self):
        self.time_step = None
        self.time = 0.0
        self.__grid = HexGrid()
        self.__path_queue = deque()
        self.__task_queue = []
        self.units = set()
        self.__proximity_grid = ProximityGrid(5)
        self.__cell_locks = {}
        self.tech_tree = create_tech_tree()
        self.forces = defaultdict(Force)
        
    def update(self, time_step):
        self.time_step = time_step
        self.time += time_step
        self.__update_paths()
        self.__update_tasks()

    def __update_paths(self):
        while self.__path_queue and self.__path_queue[0][-1]:
            self.__path_queue.popleft()
        if self.__path_queue:
            unit, goal, set_path, removed = self.__path_queue.popleft()
            if not removed and unit:
                def goal_func(cell):
                    return cell == goal
                def neighbors(cell):
                    result = [n for n in self.__grid.neighbors(cell)
                              if self.lockable_cell(unit, n, with_moving=True)]
                    random.shuffle(result)
                    return result
                def heuristic(cell):
                    return self.__grid.cell_dist(cell, goal)
                path = shortest_path(unit.cell, goal_func, neighbors,
                                     self.__grid.neighbor_dist,
                                     heuristic, limit=SHORTEST_PATH_LIMIT)
                set_path(path)

    def __update_tasks(self):
        while self.__task_queue and self.__task_queue[0][0] <= self.time:
            task = heappop(self.__task_queue)[-1]
            unit = task.unit
            if (unit in self.units and unit.task_stack and
                task is unit.task_stack[-1]):
                task.update()

    def add_unit(self, unit, cell):
        self.units.add(unit)
        unit.cell = self.__find_lockable_cell(unit, cell)
        self.normalize_cell_locks(unit)
        point = self.cell_to_point(unit.cell)
        rect = rect_from_center_and_size(point, unit.size)
        self.__proximity_grid[unit] = rect
        self.forces[unit.color].add_unit(unit)

    def stop_unit(self, unit):
        for task in unit.task_stack:
            task.abort()
        unit.task_queue.clear()

    def add_task(self, unit, task):
        if not unit.task_stack:
            self.call_task(unit, task)
        else:
            unit.task_queue.append(task)

    def call_task(self, unit, task):
        unit.task_stack.append(task)
        task.init(self, unit)
        self.schedule_task(task)

    def schedule_task(self, task, delay=0):
        heappush(self.__task_queue, (self.time + delay, task))

    def remove_task(self, task):
        unit = task.unit
        assert unit.task_stack and unit.task_stack[-1] is task
        unit.task_stack.pop()
        if unit.task_stack:
            self.schedule_task(unit.task_stack[-1])
        elif unit.task_queue:
            self.call_task(unit, unit.task_queue.popleft())

    def remove_unit(self, unit):
        self.forces[unit.color].remove_unit(unit)
        del self.__proximity_grid[unit]
        unit.cell = None
        self.normalize_cell_locks(unit)
        self.units.remove(unit)

    def request_path(self, unit, goal, set_path):
        path_request = [unit, goal, set_path, False]
        self.__path_queue.append(path_request)
        return path_request

    def remove_path_request(self, path_request):
        path_request[-1] = True

    def damage_factor(self, attacker, defender):
        return damage_factors.get((type(attacker), type(defender)), 1.0)

    def __find_lockable_cell(self, unit, start):
        def goal(cell):
            return self.lockable_cell(unit, cell)
        def neighbors(cell):
            cells = list(self.__grid.neighbors(cell))
            random.shuffle(cells)
            return cells
        path = shortest_path(start, goal, neighbors,
                             self.__grid.neighbor_dist)
        return path[-1] if path else start

    def add_cell_locks(self, unit, dest):
        unit.cell_locks.add(dest)
        if unit.large:
            unit.cell_locks.update(self.__grid.neighbors(dest))
        for cell in unit.cell_locks:
            self.__cell_locks[cell] = unit

    def normalize_cell_locks(self, unit):
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

    def move_unit(self, unit, cell):
        unit.cell = cell
        point = self.cell_to_point(cell)
        rect = rect_from_center_and_size(point, unit.size)
        self.__proximity_grid[unit] = rect

    def cell_to_point(self, cell):
        return self.__grid.cell_to_point(cell)

    def point_to_cell(self, point):
        return self.__grid.point_to_cell(point)

    def cell_dist(self, start, goal):
        return self.__grid.cell_dist(start, goal)

    def neighbor_dist(self, start, goal):
        return self.__grid.neighbor_dist(start, goal)
