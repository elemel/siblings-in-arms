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


import sys


class Unit(object):

    next_key = iter(xrange(1, sys.maxint)).next

    speed = None
    size = 1, 1
    damage = None
    min_range = 0.0
    max_range = 1.0
    attack_time = 0.5
    max_health = 1.0
    build_time = 0.3

    def __init__(self, player=None):
        self.key = Unit.next_key()
        self.player = player
        self.pos = None
        self.health = self.max_health
        self.task = None
        self.task_queue = []

    def __str__(self):
        return "%s %s #%d" % (self.player.capitalize(), type(self).__name__,
                              self.key)


class Hero(Unit):
    speed = 1.0
    damage = 1.0


class Monk(Hero):
    speed = 4.0
    damage = 0.1


class Warrior(Hero):
    speed = 4.0
    damage = 0.4
    max_health = 1.2


class Knight(Hero):
    speed = 6.0
    damage = 0.3
    max_health = 1.5


class Ranger(Hero):
    speed = 5.0
    damage = 0.3


class Rogue(Hero):
    speed = 4.0
    damage = 0.2
    max_health = 0.8


class Priest(Hero):
    speed = 4.0
    damage = 0.2


class Wizard(Hero):
    speed = 3.0
    damage = 0.5
    attack_time = 2.0
    max_health = 0.6


class Building(Unit):
    pass


class Tavern(Building):
    size = (3, 3)
    max_health = 10.0
