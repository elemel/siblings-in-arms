# Copyright 2007 Mikael Lind.

from TaskQueue import TaskQueue

class Taskmaster:
    def __init__(self, task_facade):
        self._queues = {}
        self._empty_queues = []
        self._new_tasks = []
        self._task_facade = task_facade
        
    def update(self, dt):
        self._task_facade.dt = dt
        for key, queue in self._queues.iteritems():
            queue.update(self._task_facade)
            if not queue:
                self._empty_queues.append(key)
        if self._empty_queues:
            for key in self._empty_queues:
                del self._queues[key]
                print "Unit #%d fell asleep." % key
            del self._empty_queues[:]
        if self._new_tasks:
            for unit, task in self._new_tasks:
                if unit.key not in self._queues:
                    self._queues[unit.key] = TaskQueue(unit)
                    print "Unit #%d woke up." % unit.key
                self._queues[unit.key].append(task)
            del self._new_tasks[:]

    def append_task(self, unit, task):
        self._new_tasks.append((unit, task))

    def clear_tasks(self, unit):
        if unit.key in self._queues:
            self._queues[unit.key].clear()

    def remove_unit(self, unit):
        if unit.key in self._queues:
            del self._queues[unit.key]
