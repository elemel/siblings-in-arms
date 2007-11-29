# Copyright 2007 Mikael Lind.

import sys
from collections import deque
from a_star_search import diagonal_distance

IDLE = 1
REQUEST_PATH = 2
WAIT_FOR_PATH = 3
START_MOVING = 4
MOVE = 5

def percentage(fraction):
    return int(round(fraction * 100.0))

class TaskFacade:
    def __init__(self, unit):
        self.unit = unit
        self.dt = 0.0
        self.game = None

    def find_path(self, waypoint):
        return self.game.find_path(self.unit, waypoint)

    def reserve_cell(self, pos):
        if self.game.reserve_cell(self.unit, pos):
            self.unit.cells.add(pos)
            return True
        else:
            return False

    def release_cell(self, pos):
        if pos in self.unit.cells:
            self.unit.cells.remove(pos)
            self.game.release_cell(self.unit, pos)

class Unit:
    _keys = iter(xrange(1, sys.maxint))

    def __init__(self):
        self.key = Unit._keys.next()
        self.pos = (0, 0)
        self.speed = 5
        self.cells = set()
        self.task_facade = TaskFacade(self)
        self.task_queue = deque()
        self.task = None
        self.task_gen = None
        self.task_progress = 0.0

    def update(self, dt, game):
        self.task_facade.dt = dt
        self.task_facade.game = game
        if self.task is None:
            if self.task_queue:
                self.task = self.task_queue.popleft()
                self.task_gen = self.task.run(self.task_facade)
                self.task_progress = 0.0
            else:
                return
        try:
            old_progress = percentage(self.task_progress)
            self.task_progress = self.task_gen.next()
            new_progress = percentage(self.task_progress)
            if old_progress // 10 != new_progress // 10:
                print ("Unit #%d is %d%% finished with its task."
                       % (self.key, new_progress))
        except StopIteration, e:
            self.task = None
            self.task_gen = None
            self.task_progress = 0.0
            print "Unit #%d finished its task." % self.key

    def add_task(self, task):
        self.task_queue.append(task)
