# Copyright 2007 Mikael Lind.

import sys

class Unit(object):

    next_key = iter(xrange(1, sys.maxint)).next

    speed = None
    size = 1, 1
    damage = None
    min_range = 0.0
    max_range = 1.0
    preattack_time = 0.5
    postattack_time = 0.5
    max_health = 1.0
    build_time = 0.3

    def __init__(self, player=None):
        self.key = Unit.next_key()
        self.player = player
        self.pos = None
        self.health = self.max_health

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
    preattack_time = 1.0
    postattack_time = 0.5
    max_health = 0.6

class Building(Unit):
    pass

class Tavern(Building):
    size = (3, 3)
    max_health = 10.0
