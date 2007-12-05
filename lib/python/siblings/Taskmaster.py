# Copyright 2007 Mikael Lind.

from TaskQueue import TaskQueue

class Taskmaster:
    def __init__(self, task_facade):
        self._tasks = {}
        self._old_tasks = []
        self._new_tasks = []
        self._task_facade = task_facade
        
    def update(self, dt):
        self._task_facade.dt = dt
        for key, tasks in self._tasks.iteritems():
            tasks.update(self._task_facade)
            if not tasks:
                self._old_tasks.append(key)
        if self._old_tasks:
            for key in self._old_tasks:
                del self._tasks[key]
                print "Unit #%d fell asleep." % key
            del self._old_tasks[:]
        if self._new_tasks:
            for unit, task in self._new_tasks:
                if unit.key not in self._tasks:
                    self._tasks[unit.key] = TaskQueue(unit)
                    print "Unit #%d woke up." % unit.key
                self._tasks[unit.key].append(task)
            del self._new_tasks[:]

    def append_task(self, unit, task):
        self._new_tasks.append((unit, task))

    def clear_tasks(self, unit):
        if unit.key in self._tasks:
            self._tasks[unit.key].clear()
