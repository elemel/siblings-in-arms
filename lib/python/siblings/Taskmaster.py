# Copyright 2007 Mikael Lind.

from TaskQueue import TaskQueue
from collections import deque
from geometry import rectangle_from_center_and_size

class Taskmaster:
    def __init__(self, task_facade, idle_callback):
        self._task_facade = task_facade
        self._idle_callback = idle_callback
        self._queues = {}
        self._empty_queues = []
        self._new_tasks = []
        self._idle_units = deque()
        
    def update(self, dt):
        self._task_facade.dt = dt
        for key, queue in self._queues.iteritems():
            queue.update(self._task_facade)
            if not queue:
                self._empty_queues.append(key)
        if self._empty_queues:
            for key in self._empty_queues:
                unit = self._queues[key]._actor
                del self._queues[key]
                print "%s fell asleep." % unit
            del self._empty_queues[:]
        if self._new_tasks:
            for unit, task in self._new_tasks:
                if not unit.key in self._queues:
                    self._queues[unit.key] = TaskQueue(unit)
                    print "%s woke up." % unit
                self._queues[unit.key].append(task)
            del self._new_tasks[:]
        if self._idle_units:
            unit = self._idle_units.popleft()
            self._idle_units.append(unit)
            if unit.key not in self._queues:
                self._idle_callback(unit)

    def add_unit(self, unit):
        self._idle_units.append(unit)

    def remove_unit(self, unit):
        if unit.key in self._queues:
            del self._queues[unit.key]
        self._idle_units.remove(unit)
        self._new_tasks = [(u, t) for u, t in self._new_tasks if u != unit]

    def append_task(self, unit, task):
        self._new_tasks.append((unit, task))

    def clear_tasks(self, unit):
        if unit.key in self._queues:
            self._queues[unit.key].clear()
