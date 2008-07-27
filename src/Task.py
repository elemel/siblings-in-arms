# Copyright (c) 2007 Mikael Lind
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from __future__ import division
from collections import deque


class Task(object):

    def __init__(self):
        self.game = None
        self.unit = None

    def init(self, game, unit):
        self.game = game
        self.unit = unit

    def update(self):
        pass

    def abort(self):
        pass


class MoveTask(Task):

    def __init__(self, goal):
        Task.__init__(self)
        self.goal = goal
        self.path_request = None
        self.path = deque()
        self.stuck = False
        self.update = self.__request_path

    def __request_path(self):
        if self.goal is None:
            self.game.remove_task(self)
        else:
            self.path_request = self.game.request_path(self.unit, self.goal,
                                                       self.__set_path)

    def __set_path(self, path):
        self.path_request = None
        self.path.clear()
        self.path.extend(path)
        if self.path:
            self.unit.moving = True
            self.update = self.__follow_path
            self.game.schedule_task(self)
        elif self.stuck:
            self.game.remove_task(self)
        else:
            self.stuck = True
            self.update = self.__request_path
            self.game.schedule_task(self)

    def __follow_path(self):
        if self.path and self.game.lockable_cell(self.unit, self.path[0]):
            self.stuck = False
            dest = self.path.popleft()
            self.game.add_cell_locks(self.unit, dest)
            self.game.call_task(self.unit, StepTask(dest))
        else:
            self.unit.moving = False
            self.update = self.__request_path
            self.game.schedule_task(self)

    def abort(self):
        if self.path_request is not None:
            self.game.remove_path_request(self.path_request)
            self.path_request = None
            self.game.remove_task(self)
        else:
            self.path.clear()
            self.goal = None


class StepTask(Task):

    def __init__(self, dest):
        self.origin = None
        self.dest = dest
        self.dist = None
        self.step_time = 0
        self.departure_time = None
        self.update = self.__depart

    def __depart(self):
        self.origin = self.unit.cell
        self.dist = self.game.neighbor_dist(self.unit.cell, self.dest)
        self.step_time = self.dist / self.unit.speed
        self.departure_time = self.game.time
        self.update = self.__arrive
        self.game.schedule_task(self, self.step_time)

    def __arrive(self):
        self.unit.cell = self.dest
        self.game.normalize_cell_locks(self.unit)
        self.game.remove_task(self)


class ProduceTask(Task):

    def __init__(self, product_class):
        Task.__init__(self)
        self.product_class = product_class
        self.update = self.__start

    def __start(self):
        self.update = self.__finish
        self.game.schedule_task(self, self.product_class.build_time)

    def __finish(self):
        self.game.add_unit(self.product_class(self.unit.color), self.unit.cell)
        self.game.remove_task(self)


class BuildTask(Task):

    def __init__(self, building_class):
        Task.__init__(self)
        self.building_class = building_class
        self.update = self.__start

    def __start(self):
        self.update = self.__finish
        self.game.schedule_task(self, self.building_class.build_time)

    def __finish(self):
        self.game.add_unit(self.building_class(self.unit.color),
                           self.unit.cell)
        self.game.remove_task(self)


class AttackTask(Task):

    def __init__(self, target):
        Task.__init__(self)
        self.target = target

    def update(self):
        if self.target not in self.game.units:
            self.game.remove_task(self)
        else:
            target_dist = (self.game.cell_dist(self.unit.cell,
                                               self.target.cell)
                           - 1 - self.unit.large - self.target.large)
            if target_dist <= self.unit.max_range:
                self.game.call_task(self.unit, HitTask(self.target))
            else:
                self.game.call_task(self.unit, MoveTask(self.target.cell))

    def abort(self):
        self.target = None


class HitTask(Task):

    def __init__(self, target):
        Task.__init__(self)
        self.target = target
        self.update = self.__aim

    def __aim(self):
        self.update = self.__fire
        self.game.schedule_task(self, self.unit.attack_time / 2)

    def __fire(self):
        if self.target in self.game.units:
            damage_factor = self.game.damage_factor(self.unit, self.target)
            self.target.health -= self.unit.damage * damage_factor
            if self.target.health <= 0:
                self.game.remove_unit(self.target)
        self.update = self.__reload
        self.game.schedule_task(self, self.unit.attack_time / 2)

    def __reload(self):
        self.game.remove_task(self)
