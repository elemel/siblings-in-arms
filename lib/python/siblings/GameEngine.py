# Copyright 2007 Mikael Lind.

import time, sys
from a_star_search import a_star_search
from geometry import grid_neighbors, diagonal_distance
from Unit import Unit, UnitSpec
from TaskQueue import TaskQueue
from TaskFacade import TaskFacade
from Pathfinder import Pathfinder
from Gridlocker import Gridlocker

tavern_spec = UnitSpec("tavern")
tavern_spec.speed = 0.0
tavern_spec.size = (3, 3)

warrior_spec = UnitSpec("warrior")
warrior_spec.speed = 5.0

def find_nearest_lockable(key, pos, size, locked_cells):
    width, height = size

    def predicate(p):
        return locked_cells.get(p, key) == key
    
    def contains(p):
        x, y = p
        return x >= 0 and x < width and y >= 0 and y < height
    
    def neighbors(p):
        return (n for n in grid_neighbors(p) if contains(n))
    
    def heuristic(p):
        return 0

    path, nodes = a_star_search(pos, predicate, neighbors, diagonal_distance,
                                heuristic)
    return path.p

class GameEngine:
    def __init__(self):
        self.units = {}
        self.tasks = {}
        self.new_tasks = []
        self.task_facade = TaskFacade(self)
        self.gridlocker = Gridlocker()
        self.pathfinder = Pathfinder(self.gridlocker)
        
    def update(self, dt):
        self.task_facade.dt = dt
        self.pathfinder.update()
        for key, tasks in self.tasks.iteritems():
            self.task_facade.unit = self.units[key]
            tasks.update(self.task_facade)
        if self.new_tasks:
            for unit, task in self.new_tasks:
                if unit.key not in self.tasks:
                    self.tasks[unit.key] = TaskQueue()
                self.tasks[unit.key].append(task)
            del self.new_tasks[:]

    def find_path(self, unit, waypoint, callback):
        self.pathfinder.find_path(unit, waypoint, callback)

    def append_task(self, unit, task):
        self.new_tasks.append((unit, task))

    def clear_tasks(self, unit):
        self.tasks[unit.key].clear()

    def add_unit(self, unit, pos):
        pos = find_nearest_lockable(unit.key, pos, self.gridlocker.size,
                                    self.gridlocker.locked_cells)
        print "Adding unit #%d at %s." % (unit.key, pos)
        self.units[unit.key] = unit
        unit.pos = pos
        x, y = unit.pos
        width, height = unit.size
        min_x = int(x - (width - 1) / 2)
        min_y = int(y - (height - 1) / 2)
        max_x = min_x + (width - 1)
        max_y = min_y + (height - 1)
        for x in xrange(min_x, max_x + 1):
            for y in xrange(min_y, max_y + 1):
                self.gridlocker.lock_cell(unit, (x, y))
        self.tasks[unit.key] = TaskQueue()

    def remove_unit(self, unit):
        while unit.locked_cells:
            p = unit.locked_cells.pop()
            del self.locked_cells[p]
        del self.units[unit.key]

    def get_build_time(self, name):
        return 3.0

    def create_unit(self, name, pos):
        unit = Unit(warrior_spec)
        self.add_unit(unit, pos)
