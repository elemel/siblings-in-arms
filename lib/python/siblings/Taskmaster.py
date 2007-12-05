# Copyright 2007 Mikael Lind.

from TaskQueue import TaskQueue

class Taskmaster:
    def __init__(self, task_facade):
        self.tasks = {}
        self.new_tasks = []
        self.task_facade = task_facade
        
    def update(self, dt):
        self.task_facade.dt = dt
        for key, tasks in self.tasks.iteritems():
            tasks.update(self.task_facade)
        if self.new_tasks:
            for unit, task in self.new_tasks:
                if unit.key not in self.tasks:
                    self.tasks[unit.key] = TaskQueue(unit)
                self.tasks[unit.key].append(task)
            del self.new_tasks[:]

    def append_task(self, unit, task):
        self.new_tasks.append((unit, task))

    def clear_tasks(self, unit):
        if unit.key in self.tasks:
            self.tasks[unit.key].clear()
