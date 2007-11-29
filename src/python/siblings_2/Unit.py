# Copyright 2007 Mikael Lind.

import sys
from collections import deque
from TaskFacade import TaskFacade

def percentage(fraction):
    return int(round(fraction * 100.0))

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
