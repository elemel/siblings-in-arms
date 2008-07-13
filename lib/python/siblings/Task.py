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


from geometry import diagonal_distance, vector_add, vector_mul


def interpolate_pos(old_p, new_p, progress):
    return vector_add(vector_mul(old_p, 1 - progress),
                      vector_mul(new_p, progress))


class Task(object):

    def __init__(self):
        self.progress = None
        self.aborting = False
        self.done = False

    def update(self, facade):
        pass


class MoveTask(Task):

    def __init__(self, waypoint):
        Task.__init__(self)
        self.waypoint = waypoint
        self.path_request = None
        self.path = None
        self.path = None
        self.old_pos = None
        self.step_dist = None
        self.subprogress = None
        self.update = self.__request_path

    def __request_path(self, facade):
        self.path_request = facade.request_path(facade.actor, self.waypoint,
                                                self.__set_path)
        self.update = self.__wait_for_path
        self.update(facade)

    def __wait_for_path(self, facade):
        if self.path is not None:
            if not self.path:
                self.done = True
            else:
                self.update = self.__follow_path
                self.update(facade)

    def __follow_path(self, facade):
        if self.aborting or facade.actor.pos == self.waypoint:
            self.done = True
        elif not self.path:
            self.update = self.__request_path
            self.update(facade)
        elif facade.locked_cell(self.path[0]):
            self.done = True
        else:
            facade.lock_cell(facade.actor, self.path[0])
            self.old_pos = facade.actor.pos
            self.step_dist = diagonal_distance(self.old_pos, self.path[0])
            self.subprogress = 0.0
            self.update = self.__step
            self.update(facade)

    def __step(self, facade):
        self.subprogress += facade.dt * facade.actor.speed / self.step_dist
        if self.subprogress < 1.0:
            facade.set_pos(facade.actor,
                           interpolate_pos(self.old_pos, self.path[0],
                                           self.subprogress))
        else:
            facade.set_pos(facade.actor, self.path[0])
            facade.unlock_cell(self.old_pos)
            self.path = self.path[1:]
            self.update = self.__follow_path

    def __set_path(self, path):
        self.path = path


class BuildTask(Task):

    def __init__(self, product_cls):        
        Task.__init__(self)
        self.product_cls = product_cls
        self.progress = 0.0

    def update(self, facade):
        self.progress += facade.dt / self.product_cls.build_time
        if self.progress >= 1.0:
            facade.add_unit(self.product_cls(facade.actor.player),
                            facade.actor.pos)
            self.done = True


def in_range(attacker, target):
    if target.pos is None:
        return False
    distance = (diagonal_distance(attacker.pos, target.pos)
                - attacker.size[0] / 2.0 - target.size[0] / 2.0)
    return distance >= attacker.min_range and distance <= attacker.max_range


def attack_progress(target):
    progress = 1.0 - target.health
    return min(max(progress, 1.0), 0.0)


class AttackTask(Task):

    def __init__(self, target):
        Task.__init__(self)
        self.target = target
        self.update = self.__hit_or_move
        self.subtask = None
        self.subprogress = 0.0

    def __hit_or_move(self, facade):
        if self.target.pos is None:
            self.done = True
        elif in_range(facade.actor, self.target):
            self.update = self.__before_hit
            self.subprogress = 0.0
            self.update(facade)
        else:
            self.update = self.__move
            self.subtask = MoveTask(self.target.pos)
            self.update(facade)

    def __before_hit(self, facade):
        self.subprogress += facade.dt / (facade.actor.attack_time)
        if self.subprogress >= 0.5:
            damage_factor = facade.get_damage_factor(facade.actor, self.target)
            self.target.health -= facade.actor.damage * damage_factor
            print "%s hit %s." % (facade.actor, self.target)
            self.update = self.__after_hit
        self.progress = attack_progress(self.target)

    def __after_hit(self, facade):
        self.subprogress += facade.dt / (facade.actor.attack_time)
        if self.subprogress >= 1.0:
            self.update = self.__hit_or_move

    def __move(self, facade):
        self.subtask.update(facade)
        if self.subtask.done:
            self.update = self.__hit_or_move
        self.progress = attack_progress(self.target)
        
        
