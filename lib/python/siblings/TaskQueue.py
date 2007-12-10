# Copyright 2007 Mikael Lind.

from collections import deque
from TaskFacade import TaskFacade

def percentage(fraction):
    return int(round(fraction * 100.0))

class TaskQueue:
    def __init__(self, actor):
        self._actor = actor
        self._running = None
        self._waiting = deque()
        self._aborting = False
        self._gen = None
        self._progress = 0.0
        self._progress_time = 0.0
        self._last_progress = 0

    def __len__(self):
        return int(self._running is not None) + len(self._waiting)

    def append(self, task):
        self._waiting.append(task)

    def update(self, facade):
        facade.actor = self._actor
        facade.aborting = self._aborting
        if self._running is None:
            if self._waiting:
                print "%s is starting a task." % facade.actor
                self._running = self._waiting.popleft()
                self._aborting = False
                self._gen = self._running.run(facade)
                self._progress = 0.0
                self._progress_time = 0.0
                self._last_progress = 0
            else:
                return
        try:
            self._progress = self._gen.next()
            self._progress_time += facade.dt
            perc = percentage(self._progress)
            if perc != self._last_progress and self._progress_time >= 1.0:
                print ("%s has completed %d%% of its task."
                       % (facade.actor, perc))
                self._progress_time = 0.0
                self._last_progress = perc
        except StopIteration, e:
            self._running = None
            self._aborting = False
            self._gen = None
            self._progress = 0.0
            self._progress_time = 0.0
            self._last_progress = 0
            print "%s completed its task." % facade.actor

    def clear(self):
        if self._waiting:
            self._waiting.clear()
        if self._running is not None and not self._aborting:
            self._aborting = True
