# Copyright 2007 Mikael Lind.

from collections import deque
from TaskFacade import TaskFacade

def percentage(fraction):
    return int(round(fraction * 100.0))

class TaskQueue:
    def __init__(self, unit):
        self._unit = unit
        self._running = None
        self._waiting = deque()
        self._abort = []
        self._gen = None
        self._progress = 0.0
        self._progress_time = 0.0
        self._last_progress = 0

    def append(self, task):
        self._waiting.append(task)

    def update(self, facade):
        facade.unit = self._unit
        if self._running is None:
            if self._waiting:
                print "Unit #%d is starting a task." % facade.unit.key
                self._running = self._waiting.popleft()
                del self._abort[:]
                self._gen = self._running.run(facade, self._abort)
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
                print ("Unit #%d has completed %d%% of its task."
                       % (facade.unit.key, perc))
                self._progress_time = 0.0
                self._last_progress = perc
        except StopIteration, e:
            self._running = None
            self._gen = None
            self._progress = 0.0
            self._progress_time = 0.0
            self._last_progress = 0
            print "Unit #%d completed its task." % facade.unit.key

    def clear(self):
        if self._waiting:
            self._waiting.clear()
        if self._running is not None and not self._abort:
            self._abort.append(None)
