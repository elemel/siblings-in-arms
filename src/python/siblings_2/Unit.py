# Copyright 2007 Mikael Lind.

import sys
from TaskQueue import TaskQueue

class Unit:
    _keys = iter(xrange(1, sys.maxint))

    def __init__(self):
        self.key = Unit._keys.next()
        self.pos = (0, 0)
        self.speed = 5
        self.locked_cells = set()
        self.task_queue = TaskQueue(self)

    def update(self, game, dt):
        self.task_queue.update(game, dt)

    def add_task(self, task):
        self.task_queue.append(task)
