# Copyright 2007 Mikael Lind.

from collections import deque
from TaskFacade import TaskFacade

def percentage(fraction):
    return int(round(fraction * 100.0))

class TaskQueue:
    def __init__(self, unit):
        self._facade = TaskFacade(unit)
        self._tasks = deque()
        self._current = None
        self._gen = None
        self._progress = 0.0
        self._progress_time = 0.0

    def __len__(self):
        return len(self._tasks)

    def append(self, task):
        self._tasks.append(task)

    def update(self, game, dt):
        self._facade.dt = dt
        self._facade.game = game
        if self._current is None:
            if self._tasks:
                print "Unit #%d is starting a task." % self._facade.unit.key
                self._current = self._tasks.popleft()
                self._gen = self._current.run(self._facade)
                self._progress = 0.0
                self._progress_time = 0.0
            else:
                return
        try:
            self._progress = self._gen.next()
            self._progress_time += dt
            if self._progress_time >= 1.0:
                print ("Unit #%d has completed %d%% of its task."
                       % (self._facade.unit.key, percentage(self._progress)))
                self._progress_time = 0.0
        except StopIteration, e:
            self._current = None
            self._gen = None
            self._progress = 0.0
            print "Unit #%d completed its task." % self._facade.unit.key

    def clear(self):
        if self._tasks:
            self._tasks.clear()
        if self._current:
            self._current.abort()
