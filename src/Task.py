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


from geometry import (diagonal_distance, vector_add, vector_mul, vector_sub,
                      vector_abs, vector_div)


def interpolate_pos(old_p, new_p, progress):
    return vector_add(vector_mul(old_p, 1 - progress),
                      vector_mul(new_p, progress))


class Task(object):

    def __init__(self, game_engine, unit, *args):
        self.game_engine = game_engine
        self.unit = unit
        self.progress = None
        self.aborting = False
        self.alive = True
        self.result = None
        self.__next = None
        self._init(*args)

    def _init(self, *args):
        pass

    def update(self):
        if self.alive:
            if self.__next is None:
                self.__next = iter(self._run()).next
            try:
                progress = self.__next()
                if progress is not None:
                    self.progress = progress
            except StopIteration:
                self.alive = False

    def _run(self):
        while False:
            yield

    def __nonzero__(self):
        return self.alive


class MoveTask(Task):

    def _init(self, dest):
        self.dest = dest
        self.path_request = None
        self.path = None
        self.old_pos = None
        self.new_pos = None
        self.step_dist = None
        self.subprogress = None
        self.update = self.__request_path
        self.stuck = False

    def __request_path(self):
        self.path = None
        self.path_request = self.game_engine.request_path(self.unit, self.dest,
                                                          self.__set_path)
        self.update = self.__wait_for_path
        self.update()

    def __wait_for_path(self):
        if self.aborting:
            self.game_engine.abort_path(self.path_request)
            self.alive = False
        elif self.path is not None:
            if not self.path:
                if self.stuck:
                    self.alive = False
                else:
                    self.stuck = True
                    self.update = self.__request_path
                    self.update()
            else:
                self.update = self.__follow_path
                self.update()

    def __follow_path(self):
        if self.aborting or self.unit.cell == self.dest:
            self.unit.moving = False
            self.alive = False
        elif (not self.path
              or not self.game_engine.lockable_cell(self.unit, self.path[0])):
            self.unit.moving = False
            self.update = self.__request_path
            self.update()
        else:
            self.unit.moving = True
            self.stuck = False
            self.unit.cell = self.path[0]
            self.game_engine.update_cell_locks(self.unit)
            self.old_pos = self.unit.pos
            self.new_pos = self.game_engine.cell_to_pos(self.path[0])
            self.step_dist = diagonal_distance(self.old_pos, self.new_pos)
            self.subprogress = 0.0
            self.update = self.__step
            self.update()

    def __step(self):
        self.subprogress += (self.game_engine.time_step * self.unit.speed
                             / self.step_dist)
        if self.subprogress < 1.0:
            self.game_engine.move_unit(self.unit,
                                       interpolate_pos(self.old_pos,
                                                       self.new_pos,
                                                       self.subprogress))
        else:
            self.game_engine.move_unit(self.unit, self.new_pos)
            self.path = self.path[1:]
            self.update = self.__follow_path

    def __set_path(self, path):
        self.path = path


class StepTask(Task):

    def _init(self, from_cell, to_cell):
        self.from_cell = from_cell
        self.to_cell = to_cell

    def _run(self):
        dist = self.game_engine.cell_distance(self.from_cell, self.to_cell)
        self.progress = 0.0
        while self.progress < 1.0:
            self.progress += (self.game_engine.time_step * self.unit.speed
                              / dist)
            yield


class ProduceTask(Task):

    def _init(self, product_class):
        self.product_class = product_class

    def _run(self):
        self.progress = 0.0
        while True:
            self.progress += (self.game_engine.time_step
                              / self.product_class.build_time)
            if self.progress < 1.0:
                yield
            else:
                break
        self.game_engine.add_unit(self.product_class(self.unit.color),
                                  self.unit.pos)


def in_range(unit, target):
    if target.pos is None:
        return False
    distance = abs(diagonal_distance(unit.pos, target.pos)
                   - unit.size[0] / 2.0 - target.size[0] / 2.0)
    return unit.min_range <= distance < unit.max_range


def attack_progress(target):
    progress = 1.0 - target.health
    return max(0.0, min(progress, 1.0))


class AttackTask(Task):

    def _init(self, target):
        self.target = target
        self.update = self.__hit_or_move
        self.subtask = None
        self.subprogress = 0.0

    def __hit_or_move(self):
        if self.aborting or self.target.pos is None:
            self.alive = False
        elif in_range(self.unit, self.target):
            self.old_pos = self.unit.pos
            offset = vector_sub(self.target.pos, self.unit.pos)
            self.new_pos = vector_add(self.unit.pos,
                                      vector_div(offset, vector_abs(offset)))
            self.update = self.__before_hit
            self.subprogress = 0.0
            self.update()
        else:
            self.update = self.__move
            self.subtask = MoveTask(self.game_engine, self.unit,
                                    self.target.cell)
            self.subtask.game_engine = self.game_engine
            self.subtask.unit = self.unit
            self.update()

    def __before_hit(self):
        self.subprogress += (self.game_engine.time_step
                             / (self.unit.attack_time))
        self.game_engine.move_unit(self.unit,
                                   interpolate_pos(self.old_pos,
                                                   self.new_pos,
                                                   self.subprogress))
        if self.subprogress >= 0.5:
            damage_factor = self.game_engine.damage_factor(self.unit,
                                                           self.target)
            self.target.health -= self.unit.damage * damage_factor
            self.update = self.__after_hit
        self.progress = attack_progress(self.target)

    def __after_hit(self):
        self.subprogress += self.game_engine.time_step / self.unit.attack_time
        if self.subprogress < 1.0:
            self.game_engine.move_unit(self.unit,
                                       interpolate_pos(self.old_pos,
                                                       self.new_pos,
                                                       1 - self.subprogress))
        else:
            self.game_engine.move_unit(self.unit, self.old_pos)
            self.update = self.__hit_or_move

    def __move(self):
        if (self.aborting or self.target.pos is None
            or in_range(self.unit, self.target)):
            self.subtask.aborting = True
        self.subtask.update()
        if not self.subtask:
            self.update = self.__hit_or_move
        self.progress = attack_progress(self.target)


class BuildTask(Task):

    def _init(self, building_class):
        self.building_class = building_class

    def _run(self):
        self.progress = 0.0
        while True:
            self.progress += (self.game_engine.time_step
                              / self.building_class.build_time)
            if self.progress < 1.0:
                yield
            else:
                break
        self.game_engine.add_unit(self.building_class(self.unit.color),
                                  self.unit.pos)
