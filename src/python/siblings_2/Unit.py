# Copyright 2007 Mikael Lind.

import sys
from collections import deque
from a_star_search import diagonal_distance

IDLE = 1
REQUEST_PATH = 2
WAIT_FOR_PATH = 3
START_MOVING = 4
MOVE = 5

class TaskFacade:
    def __init__(self, unit):
        self.unit = unit
        self.dt = 0.0
        self.game = None

    def find_path(self, waypoint):
        return self.game.find_path(self.unit, waypoint)

    def reserve_cell(self, pos):
        return self.game.reserve_cell(self.unit, pos)

    def release_cell(self, pos):
        return self.game.release_cell(self.unit, pos)

class Unit:
    _keys = iter(xrange(1, sys.maxint))

    def __init__(self):
        self.key = Unit._keys.next()
        self.pos = (0, 0)
        self.speed = 5
        self.cells = set()
        self.task_facade = TaskFacade(self)
        self.tasks = deque()
        self.current_task = None
        self.current_task_gen = None

    def update(self, dt, game):
        self.task_facade.dt = dt
        self.task_facade.game = game
        if self.current_task is None:
            if self.tasks:
                self.current_task = self.tasks.popleft()
                self.current_task.facade = self.task_facade
                self.current_task_gen = self.current_task.run()
            else:
                return
        try:
            self.current_task_gen.next()
        except StopIteration, e:
            self.current_task = None
            self.current_task_gen = None
            print "Unit #%d finished a task." % self.key

    def add_task(self, task):
        self.tasks.append(task)
