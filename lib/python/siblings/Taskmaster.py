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
            for actor, task in self._new_tasks:
                if actor.key not in self._queues:
                    self._queues[actor.key] = TaskQueue(actor)
                    print "Unit #%d woke up." % actor.key
                self._queues[actor.key].append(task)
            del self._new_tasks[:]

    def append_task(self, actor, task):
        self._new_tasks.append((actor, task))

    def clear_tasks(self, actor):
        if actor.key in self._queues:
            self._queues[actor.key].clear()

    def remove_actor(self, actor):
        if actor.key in self._queues:
            del self._queues[actor.key]
